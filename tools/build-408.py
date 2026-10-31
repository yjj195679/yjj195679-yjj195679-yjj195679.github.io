"""Build static, script-independent 408 study pages from the reviewed JSON source."""
import json, re, subprocess
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/408-knowledge.json').read_text())
math_data=json.loads((ROOT/'data/408-math.json').read_text())
inline_math=math_data['inline']
expressions=set(inline_math.values())
for item in data['items']+data['calculations']:
    expressions.update(f['tex'] for f in item.get('formulas',[]))
math_html=json.loads(subprocess.run(['node',str(ROOT/'tools/render-408-math.cjs')],input=json.dumps(sorted(expressions)),capture_output=True,text=True,check=True).stdout)
math_pattern=re.compile('|'.join(re.escape(k) for k in sorted(inline_math,key=len,reverse=True)))
def rich(text):
    text=str(text)
    parts=[]; end=0
    for match in math_pattern.finditer(text):
        parts.extend([e(text[end:match.start()]), math_html[inline_math[match.group()]]]); end=match.end()
    parts.append(e(text[end:]))
    return '<span class="study-text" data-plain-text="'+e(text,quote=True)+'">'+''.join(parts)+'</span>'
def formula_block(x):
    return '<div class="study-formula-set">'+''.join('<div class="study-formula"><div class="study-formula-scroll" tabindex="0" aria-label="公式，可横向滚动">'+math_html[f['tex']]+'</div><p>'+rich(f['note'])+'</p></div>' for f in x.get('formulas',[]))+'</div>' if x.get('formulas') else ''
subjects=['数据结构','计算机组成原理','操作系统','计算机网络']
slugs=['ds','co','os','net']
base=(ROOT/'courses.html').read_text()
header=base[base.index('<header'):base.index('<main')]
# Chinese material has no pretend English translation.
header=re.sub(r'<div class="language-switch">.*?</div>','',header)
footer=base[base.index('<footer'):base.index('<script src="js/main.js')]
def page(filename,title,description,body):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f"><title>{e(title)} · True Path M</title><meta name="description" content="{e(description)}"><link rel="canonical" href="https://1956799.xyz/{filename}"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/tpm-serif.woff2" as="font" type="font/woff2" crossorigin><script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20260909-15"><link rel="stylesheet" href="js/vendor/katex/katex.min.css"><link rel="stylesheet" href="css/408.css?v=20261030-1"></head><body data-page="study" class="study408"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>{header}<main id="main">{body}</main>{footer}<script src="js/main.js?v=20261012-408" defer></script><script src="js/408.js?v=20261030-1" defer></script></body></html>'''
def hero(title,lead,calc=False):
    return f'''<section class="subhero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="courses.html">← 返回学习</a><div class="kicker">408 · {'计算训练' if calc else '概念复习'}</div><h1>{title}</h1><p>{lead}</p><nav class="hero-actions" aria-label="408 板块"><a class="button {'primary' if not calc else ''}" href="408.html" {'aria-current="page"' if not calc else ''}>易错易混与冷门考点</a><a class="button {'primary' if calc else ''}" href="408-calculations.html" {'aria-current="page"' if calc else ''}>计算专项</a></nav></article></div></section>'''
def controls(calc=False):
    tags=['个人错题','易错','易混','冷门','近年考查','记忆概念','图解']
    return f'''<section class="section study-controls" id="filters"><div class="container"><div class="panel glass"><h2 class="study-sr-only">筛选知识点</h2><fieldset id="study-filters" hidden><legend>筛选考点</legend><div class="study-quick" aria-label="快速选择科目"><button class="button" type="button" data-subject-filter="" aria-pressed="true">全部科目</button>{''.join(f'<button class="button" type="button" data-subject-filter="{x}" aria-pressed="false">{x}</button>' for x in subjects if not calc or any(r['subject']==x for r in data['calculations']))}</div><div class="study-filter-grid"><label class="study-search">搜索<input id="study-search" type="search" placeholder="例如：Cache 组号、TCP 窗口、读写指针" autocomplete="off"></label><label>科目<select id="study-subject"><option value="">全部科目</option>{''.join(f'<option>{x}</option>' for x in subjects)}</select></label><label>章节<select id="study-chapter"><option value="">全部章节</option></select></label>{'' if calc else '<label>分类<select id="study-tag"><option value="">全部分类</option>'+''.join(f'<option>{x}</option>' for x in tags)+'</select></label>'}<label>复习状态<select id="study-state"><option value="">全部状态</option><option value="review">待复习</option><option value="mastered">已掌握</option><option value="unmarked">未标记</option></select></label></div><div class="study-actions"><button type="button" class="button" id="study-reset">重置筛选</button><button type="button" class="button" id="study-expand">展开筛选结果</button><button type="button" class="button" id="study-collapse">收起筛选结果</button></div></fieldset><div class="study-progress" id="study-progress" hidden><label for="study-mastery">当前筛选范围的掌握进度</label><progress id="study-mastery" max="100" value="0">0%</progress><span id="study-progress-text"></span></div><p id="study-count" role="status" aria-live="polite">共 {len(data['calculations'] if calc else data['items'])} 条，按科目与章节分类。点击知识点展开解析。</p><p class="study-note" id="study-storage">复习标记只保存在当前浏览器；重置筛选不会清除标记。</p><noscript><p>当前未启用脚本：仍可展开全部解析，搜索、筛选和复习标记暂不可用。</p></noscript></div></div></section>'''
def state_controls(id):
    return f'''<div class="study-mark" hidden aria-label="复习标记"><button type="button" class="button" data-mark="review" aria-pressed="false">待复习</button><button type="button" class="button" data-mark="mastered" aria-pressed="false">已掌握</button><span class="study-state-text">未标记</span><a href="#{id}" class="button-link" aria-label="定位此知识点">定位链接</a></div>'''
def card(x,calc=False):
    search=' '.join(str(v) for k,v in x.items() if k!='id')
    tags=['计算专项'] if calc else x['tags']
    badges=''.join(f'<span class="study-badge" data-tag="{e(t)}">{e(t)}</span>' for t in tags)
    if calc:
        content=f'''<p class="study-question">{rich(x['q'])}</p><p class="study-caution"><strong>关键：</strong>{rich(x['pitfalls'])}</p><details class="study-recall study-explanation"><summary>答案与解析</summary><p class="study-conclusion"><strong>答案：</strong>{rich(x['answer'])}</p>{formula_block(x)}<ol>{''.join('<li>'+rich(s)+'</li>' for s in x['steps'])}</ol><p class="study-note">自编变式</p></details>'''
    else:
        # Only the positive conclusion and a reviewed reminder lead the card.
        # Full conditions stay in the data, in search, and in an expandable explanation.
        content='<div class="study-key"><h4>核心结论</h4><p>'+rich(x['right'])+'</p></div>'
        content+='<p class="study-caution"><strong>别混淆</strong><span>'+rich(x['review_tip'])+'</span></p>'
        content+='<details class="study-recall study-explanation"><summary>详解</summary><div class="study-detail-content">'
        content+='<section class="study-detail-block"><h4><span>01</span> 解析</h4>'
        content+=formula_block(x)
        if x.get('reason_steps'):
            content+='<ol class="study-reason-steps">'+''.join('<li>'+rich(step)+'</li>' for step in x['reason_steps'])+'</ol><details class="study-recall study-context"><summary>补充原理与条件</summary><p>'+rich(x['why'])+'</p></details>'
        else:
            content+='<p>'+rich(x['why'])+'</p>'
        content+='</section>'
        content+='<section class="study-detail-block study-example"><h4><span>02</span> 例子</h4><p>'+rich(x['example'])+'</p></section>'
        content+='<section class="study-detail-block study-misconception"><h4><span>03</span> 易错点</h4><p><span class="study-wrong-label">错误说法</span>'+rich(x['wrong'])+'</p></section>'
        if x.get('table') or x.get('diagram'):
            content+='<section class="study-detail-block study-visuals"><h4><span>04</span> 图表</h4>'
        if x.get('table'):
            table=x['table']
            content+='<div class="study-table-wrap"><table class="study-table"><caption>要点对照</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in table['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(str(cell))+'</td>' for cell in row)+'</tr>' for row in table['rows'])+'</tbody></table></div>'
        if x.get('diagram'):
            name=x['diagram']
            svg=(ROOT/'images/408'/f'{name}.svg').read_text()
            content+='<figure class="study-figure"><div class="study-diagram-scroll" tabindex="0" aria-label="示意图，可横向滚动">'+svg+'</div><figcaption>'+e(x.get('diagram_caption',''))+'<a href="images/408/'+e(name)+'.svg" target="_blank" rel="noopener noreferrer">单独查看图片</a></figcaption></figure>'
        if x.get('table') or x.get('diagram'): content+='</section>'
        if x.get('code'):content+='<section class="study-detail-block"><h4>代码对照</h4><pre><code>'+e(x['code'])+'</code></pre></section>'
        if x.get('supplement'):content+='<section class="study-detail-block"><h4>教材模型与实现差异</h4><p>'+e(x['supplement'])+'</p></section>'
        if x.get('exam_focus'):
            focus=x['exam_focus']
            content+='<section class="study-detail-block study-exam-focus"><h4>真题关联</h4><a href="'+e(focus['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(focus['label'])+'</a><p>'+rich(focus['point'])+'</p></section>'
        if x.get('extension'):
            ext=x['extension']
            content+='<section class="study-detail-block study-extension"><h4>变式</h4><p class="study-extension-label">'+e(ext['label'])+' · '+e(ext['title'])+'</p><p>'+rich(ext['question'])+'</p><details class="study-recall study-variant-answer"><summary>答案与解析</summary><p>'+rich(ext['answer'])+'</p><p class="study-transfer"><strong>关键区别：</strong>'+rich(ext['lesson'])+'</p></details></section>'
        content+=('<details class="study-recall study-sources"><summary>相关真题与参考来源</summary>' if x.get('exams') or x.get('sources') else '')
        if x.get('exams'):
            urls={2022:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/aea64e47-90e0-4cb1-8e12-10eed1a3c5f7.pdf',2024:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/6b611f5c-55d9-4612-8ff9-30b028731314.pdf',2025:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/d9fce855-72bd-4e00-9a48-5d4ec5ef6f72.pdf'}
            links=[f'<a href="{urls[r["year"]]}" target="_blank" rel="noopener noreferrer">{r["year"]} · 第 {r["question"]} 题</a>' for r in x['exams']]
            content+='<p class="study-exams"><strong>相关真题：</strong>'+'；'.join(links)+'</p>'
        if x.get('sources'):
            links=['<a href="'+e(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(r['title'])+'</a>' for r in x['sources']]
            content+='<p class="study-note">参考：'+'；'.join(links)+'</p>'
        content+=('</details>' if x.get('exams') or x.get('sources') else '')+'</div></details>'
        content+=f'''<details class="study-recall"><summary>自检：{e(x['check'])}</summary><p>{rich(x['answer'])}</p></details>'''
    return f'''<details class="study-card glass" id="{x['id']}" data-subject="{e(x['subject'])}" data-chapter="{e(x['chapter'])}" data-tags="{e(' '.join(tags))}" data-search="{e(search,quote=True)}"><summary><span class="study-card-heading"><span class="study-card-title">{e(x['title'])}</span><span class="study-card-preview">{e(x['pitfalls'] if calc else x['review_tip'])}</span></span><span class="study-badges">{badges}</span><span class="study-expand-hint" aria-hidden="true">要点</span></summary><div class="study-card-body">{content}{state_controls(x['id'])}</div></details>'''

def groups(calc=False):
    allrows=data['calculations'] if calc else data['items']; out=''
    for subject,slug in zip(subjects,slugs):
        rows=[x for x in allrows if x['subject']==subject]
        if not rows: continue
        chapters=list(dict.fromkeys(x['chapter'] for x in rows))
        out+=f'<section class="section anchor-offset study-subject" id="{slug}" data-group-subject="{subject}"><div class="container"><div class="section-head"><div><div class="kicker">408 · {slug.upper()}</div><h2>{subject}</h2></div><p class="section-intro">{len(rows)} 条 · {len(chapters)} 个章节</p></div>'
        for n,ch in enumerate(chapters):
            out+=f'<div class="study-chapter" id="{slug}-chapter-{n+1}" data-group-chapter="{e(ch)}"><h3>{e(ch)}</h3><div class="study-card-list">'+''.join(card(x,calc) for x in sorted(rows,key=lambda x: '个人错题' not in x.get('tags',[])) if x['chapter']==ch)+'</div></div>'
        out+='</div></section>'
    return out
def directory(calc=False):
    out='<section class="section study-contents" id="coverage"><div class="container"><h2 class="study-sr-only">章节目录</h2><details class="panel glass study-directory-disclosure"><summary>按章节浏览</summary><div class="study-directory">'
    for subject,slug in zip(subjects,slugs):
        rows=[x for x in (data['calculations'] if calc else data['items']) if x['subject']==subject]
        if not rows: continue
        chapters=list(dict.fromkeys(x['chapter'] for x in rows))
        out+='<article class="study-directory-subject"><h3>'+subject+'<span>'+str(len(rows))+' 条</span></h3><ul>'+''.join(f'<li><a href="#{slug}-chapter-{i+1}">'+e(ch)+'</a></li>' for i,ch in enumerate(chapters))+'</ul></article>'
    return out+'</div></details></div></section>'
refs='''<section class="section anchor-offset" id="references"><div class="container"><div class="section-head"><h2>内容说明与参考</h2></div><article class="panel glass study-reference"><p>“近年考查”附对应年份与题号；“冷门”指易遗漏的细节。公式和实现约定以题设为准。</p><ul><li><a href="https://www.xit.edu.cn/yjsfk/kyzykwtkw/list.htm" target="_blank" rel="noopener noreferrer">厦门工学院公开真题资料：已核对 2022、2024、2025 年相关题目</a></li><li><a href="https://algs4.cs.princeton.edu/23quicksort/" target="_blank" rel="noopener noreferrer">Princeton Algorithms：快排实现边界</a>；<a href="https://algs4.cs.princeton.edu/43mst/index.php" target="_blank" rel="noopener noreferrer">最小生成树</a></li><li><a href="https://pages.cs.wisc.edu/~remzi/OSTEP/" target="_blank" rel="noopener noreferrer">OSTEP：进程、地址转换、并发与文件系统</a></li><li><a href="https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html" target="_blank" rel="noopener noreferrer">Intel 架构手册：指令与标志位（具体架构示例）</a></li><li><a href="https://www.rfc-editor.org/rfc/rfc9293.html" target="_blank" rel="noopener noreferrer">RFC 9293：TCP</a>；<a href="https://www.rfc-editor.org/rfc/rfc791" target="_blank" rel="noopener noreferrer">RFC 791：IPv4</a></li></ul></article></div></section>'''
for calc in (False,True):
    filename='408-calculations.html' if calc else '408.html'
    title='计算专项' if calc else '易错易混与冷门考点'
    lead='8 道自编变式，涵盖计组、操作系统与计算机网络。' if calc else f'{len(data["items"])} 个考点，涵盖数据结构、计算机组成原理、操作系统与计算机网络。'
    body=hero(title,lead,calc)+controls(calc)+directory(calc)+'<p id="study-empty" class="container study-empty" hidden>没有匹配内容。试试减少关键词或重置筛选。</p>'+groups(calc)+refs
    (ROOT/filename).write_text(page(filename,'408 · '+title,lead,body))
print('Built 408.html and 408-calculations.html')

# Keep storage bounds in step with new content while preserving existing IDs.
js=ROOT/"js/408.js"
code=js.read_text()
limits={prefix:max(int(x["id"][1:]) for x in rows) for prefix,rows in [("k",data["items"]),("c",data["calculations"])]}
code=re.sub(r"const MARK_LIMITS = \{ k: \d+, c: \d+ \};", f"const MARK_LIMITS = {{ k: {limits['k']}, c: {limits['c']} }};", code)
js.write_text(code)
