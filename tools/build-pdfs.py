"""Build the complete, directly downloadable versions of document pages.

Requires WeasyPrint, lxml and a full Chinese serif TTF. Pass --font explicitly.
The math source is data defined in math-formulas.js; extract it with --math-data.
PDFs are snapshots of the full page; browser printing retains active filters.
"""
import argparse, json, re, logging, hashlib, subprocess
from pathlib import Path
from datetime import date
from lxml import html, etree
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['projects', 'education', 'courses', 'achievements', 'life']
SOURCES = [f'{p}.html' for p in PAGES] + [f'en/{p}.html' for p in PAGES] + ['408.html', '408-calculations.html', '408-handbook.html', 'politics.html', 'math-formulas.html']
logging.getLogger('weasyprint').setLevel(logging.ERROR)

def build(source, font, math_data, output_root):
    page = html.fromstring((ROOT/source).read_text())
    main = page.xpath('//main')[0]
    for node in main.xpath('.//script | .//button | .//input | .//select | .//fieldset | .//nav | .//aside | .//noscript'):
        node.drop_tree()
    remove = {'hero-actions','back-link','study-controls','formula-controls','study-mark','formula-actions','sim-interactive','visual-interactive','formula-stat-row','formula-card-parts','handbook408-card-parts','politics-card-parts','visual-badges','study-legend','formula-reference'}
    for node in list(main.iterdescendants()):
        if node.getparent() is not None and (set(node.get('class','').split()) & remove or node.get('hidden') is not None):
            node.drop_tree()
    # Details are fully expanded in a PDF, including explanations and worked steps.
    for node in main.xpath('.//details'):
        node.tag='section';node.attrib.pop('open',None)
    for node in main.xpath('.//summary'):
        node.tag='h3';node.set('class','pdf-card-heading')
    for node in main.xpath('.//svg'):
        node.attrib.pop('width',None);node.attrib.pop('height',None)
    for node in main.xpath('.//*[@style]'):
        node.attrib.pop('style',None)
    if source=='math-formulas.html':
        groups=main.get_element_by_id('formula-groups')
        current=None
        for item in math_data:
            if current != item['chapter']:
                current=item['chapter'];etree.SubElement(groups,'h2').text=item['subject']+' · '+current
            card=etree.SubElement(groups,'section',{'class':'pdf-formula','id':item['id']})
            etree.SubElement(card,'h3').text=item['id'][1:]+' · '+item['title']
            etree.SubElement(card,'pre',{'class':'formula-text'}).text=item['formula']
            etree.SubElement(card,'p').text='适用条件：'+item['condition']
            etree.SubElement(card,'p').text='易错提醒：'+item['pitfall']
    title=page.xpath('//h1')[0].text_content().strip()
    english=source.startswith('en/')
    notice=etree.Element('p',{'class':'pdf-notice'})
    notice.text=('Complete page · ' if english else '完整内容 · ')+date.today().isoformat()
    main.insert(1,notice)
    text=etree.tostring(main,encoding='unicode',method='html')
    text=re.sub(r'var\(--[\w-]+,\s*([^()]+)\)',r'\1',text)
    text=re.sub(r'font-family:[^;}]*SimSun[^;}]*', 'font-family:Chinese,serif', text)
    name=source.replace('/','-').replace('.html','.pdf')
    dest=output_root/name;dest.parent.mkdir(parents=True,exist_ok=True)
    css=f'''@font-face{{font-family:Chinese;src:url("{font.as_uri()}")}}
    @page{{size:A4;margin:18mm 17mm 19mm;@bottom-center{{content:counter(page);font:9pt serif;color:#444}}}}
    *{{box-sizing:border-box}}body{{font-family:Chinese,"DejaVu Serif",serif;font-size:10pt;line-height:1.65;color:#111}}
    h1{{font-size:24pt;line-height:1.4;margin:0 0 8mm}}h2{{font-size:16pt;margin:9mm 0 4mm;border-bottom:1pt solid #999;padding-bottom:2mm;break-after:avoid}}
    h3{{font-size:12pt;line-height:1.6;break-after:avoid;margin:6mm 0 2mm}}h4{{font-size:10.5pt;break-after:avoid;margin:4mm 0 2mm}}
    p{{margin:2mm 0;orphans:2;widows:2}}a{{color:#174a77;text-decoration:none}}ul,ol{{padding-left:6mm}}li{{margin:1.2mm 0}}
    pre{{font-family:"DejaVu Sans Mono",Chinese,monospace;font-size:8pt;white-space:pre-wrap;overflow-wrap:anywhere;border:0.4pt solid #ccc;padding:3mm;line-height:1.6}}
    .formula-text{{font-family:"DejaVu Serif",Chinese,serif;font-size:10.5pt}}
    .pdf-formula{{break-inside:avoid;margin-bottom:5mm}}.pdf-notice{{font-size:9pt;color:#555}}
    table{{width:100%;border-collapse:collapse;table-layout:fixed;font-size:8.5pt;margin:3mm 0}}th,td{{border:.4pt solid #aaa;padding:2mm;overflow-wrap:anywhere;vertical-align:top}}
    th{{background:#eee}}thead{{display:table-header-group}}tr{{break-inside:avoid}}
    svg,img{{display:block;max-width:100%;height:auto;margin:3mm auto}}figure{{margin:4mm 0;break-inside:avoid}}figcaption{{font-size:8.5pt}}
    .sim-transcript,.visual-transcript{{font-size:9pt}}.pdf-card-heading span{{margin-right:3mm}}
    .formula-card-number,.study-number{{font-size:9pt;color:#555}}
    .katex{{font-family:KaTeX_Main,Chinese,serif;font-size:1.05em}}.katex .katex-mathml{{display:none}}
    '''
    # Keep the existing KaTeX typesetting where the source has rendered formulas.
    katex=ROOT/'js/vendor/katex/katex.min.css'
    document='<!doctype html><html><head><meta charset="utf-8"><title>'+title+'</title></head><body>'+text+'</body></html>'
    font_config=FontConfiguration()
    HTML(string=document,base_url=str((ROOT/source).parent)+'/').write_pdf(str(dest),stylesheets=[CSS(filename=str(katex),font_config=font_config),CSS(string=css,font_config=font_config)],font_config=font_config)
    digest=hashlib.sha256((ROOT/source).read_bytes()).hexdigest()
    if source=='math-formulas.html':digest=hashlib.sha256((ROOT/source).read_bytes()+(ROOT/'js/math-formulas.js').read_bytes()).hexdigest()
    return {'page':source,'pdf':'documents/exports/'+name,'title':title,'source_sha256':digest}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--math-data',type=Path);parser.add_argument('--only',nargs='*')
    args=parser.parse_args()
    if args.math_data:math_data=json.loads(args.math_data.read_text())
    else:
        script="const fs=require('fs'),vm=require('vm');const s=fs.readFileSync('js/math-formulas.js','utf8');console.log(JSON.stringify(vm.runInNewContext(s.slice(0,s.indexOf('  const STORAGE_KEY'))+'\\nreturn formulas;})();')));"
        math_data=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,text=True))
    output=ROOT/'documents/exports';records=[]
    for source in args.only or SOURCES:
        record=build(source,args.font.resolve(),math_data,output);records.append(record);print(record['pdf'],flush=True)
    if not args.only:
        (ROOT/'data/pdf-exports.json').write_text(json.dumps({'updated':date.today().isoformat(),'documents':records},ensure_ascii=False,indent=2)+'\n')
