"""Build static, script-independent 408 study pages from the reviewed JSON source."""
import json, re
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/408-knowledge.json').read_text())
subjects=['数据结构','计算机组成原理','操作系统','计算机网络']
slugs=['ds','co','os','net']
base=(ROOT/'courses.html').read_text()
header=base[base.index('<header'):base.index('<main')]
# Chinese material has no pretend English translation.
header=re.sub(r'<div class="language-switch">.*?</div>','',header)
footer=base[base.index('<footer'):base.index('<script src="js/main.js')]
def page(filename,title,description,body):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f"><title>{e(title)} · True Path M</title><meta name="description" content="{e(description)}"><link rel="canonical" href="https://1956799.xyz/{filename}"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/tpm-serif.woff2" as="font" type="font/woff2" crossorigin><script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20260909-15"><link rel="stylesheet" href="css/408.css?v=20261012-3"></head><body data-page="study" class="study408"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>{header}<main id="main">{body}</main>{footer}<script src="js/main.js?v=20261012-408" defer></script><script src="js/408.js?v=20261020-1" defer></script></body></html>'''
def hero(title,lead,calc=False):
    return f'''<section class="subhero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="courses.html">← 返回学习</a><div class="kicker">408 · {'计算训练' if calc else '概念复习'}</div><h1>{title}</h1><p>{lead}</p><nav class="hero-actions" aria-label="408 板块"><a class="button {'primary' if not calc else ''}" href="408.html" {'aria-current="page"' if not calc else ''}>易错易混与冷门考点</a><a class="button {'primary' if calc else ''}" href="408-calculations.html" {'aria-current="page"' if calc else ''}>计算专项</a></nav></article></div></section>'''
def controls(calc=False):
    tags=['个人错题','易错','易混','冷门','近年考查','记忆概念','图解']
    return f'''<section class="section study-controls" id="filters"><div class="container"><div class="panel glass"><h2 class="study-sr-only">筛选知识点</h2><fieldset id="study-filters" hidden><legend>筛选知识点</legend><div class="study-filter-grid"><label class="study-search">搜索<input id="study-search" type="search" placeholder="知识点、关键词或错误认识" autocomplete="off"></label><label>科目<select id="study-subject"><option value="">全部科目</option>{''.join(f'<option>{x}</option>' for x in subjects)}</select></label><label>章节<select id="study-chapter"><option value="">全部章节</option></select></label>{'' if calc else '<label>分类<select id="study-tag"><option value="">全部分类</option>'+''.join(f'<option>{x}</option>' for x in tags)+'</select></label>'}<label>复习状态<select id="study-state"><option value="">全部状态</option><option value="review">待复习</option><option value="mastered">已掌握</option><option value="unmarked">未标记</option></select></label></div><div class="study-actions"><button type="button" class="button" id="study-reset">重置筛选</button><button type="button" class="button" id="study-expand">展开当前解析</button><button type="button" class="button" id="study-collapse">收起当前解析</button></div></fieldset><p id="study-count" role="status" aria-live="polite">共 {len(data['calculations'] if calc else data['items'])} 条，按科目与章节分类。点击知识点展开解析。</p><p class="study-note" id="study-storage">复习标记只保存在当前浏览器；重置筛选不会清除标记。</p><noscript><p>当前未启用脚本：仍可展开全部解析，搜索、筛选和复习标记暂不可用。</p></noscript></div></div></section>'''
def state_controls(id):
    return f'''<div class="study-mark" hidden aria-label="复习标记"><button type="button" class="button" data-mark="review" aria-pressed="false">待复习</button><button type="button" class="button" data-mark="mastered" aria-pressed="false">已掌握</button><span class="study-state-text">未标记</span><a href="#{id}" class="button-link" aria-label="定位此知识点">定位链接</a></div>'''
def card(x,calc=False):
    search=' '.join(str(v) for k,v in x.items() if k!='id')
    tags=['计算专项'] if calc else x['tags']
    badges=''.join(f'<span class="study-badge" data-tag="{e(t)}">{e(t)}</span>' for t in tags)
    if calc:
        content=f'''<p class="study-question">{e(x['q'])}</p><h4>分步解析</h4><ol>{''.join('<li>'+e(s)+'</li>' for s in x['steps'])}</ol><p class="study-conclusion"><strong>答案：</strong>{e(x['answer'])}</p><p><strong>易错提醒：</strong>{e(x['pitfalls'])}</p><p class="study-note">自编变式 · 用于过程训练，不标注为原真题。</p>'''
    else:
        content=f'''<p class="study-origin">{e(x['origin'])}</p><div class="study-comparison"><div><h4>错误认识</h4><p>{e(x['wrong'])}</p></div><div><h4>定义与正确结论</h4><p>{e(x['right'])}</p></div></div><h4>原理、适用条件与辨析</h4><p>{e(x['why'])}</p><h4>简短例子</h4><p>{e(x['example'])}</p>'''
        if x.get('exams'):
            examlinks=[]
            urls={2022:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/aea64e47-90e0-4cb1-8e12-10eed1a3c5f7.pdf',2024:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/6b611f5c-55d9-4612-8ff9-30b028731314.pdf',2025:'https://www.xit.edu.cn/_upload/article/files/c1/ce/26986f79493495bbaacba9738587/d9fce855-72bd-4e00-9a48-5d4ec5ef6f72.pdf'}
            for ref in x['exams']:
                examlinks.append(f'<a href="{urls[ref["year"]]}" target="_blank" rel="noopener noreferrer">{ref["year"]} · 第 {ref["question"]} 题</a>')
            content += '<p class="study-exams"><strong>相关真题：</strong>'+'；'.join(examlinks)+'</p>'
        if x.get('table'):
            table=x['table']
            content+='<div class="study-table-wrap"><table class="study-table"><caption>'+e(x['title'])+' · 对照速记</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in table['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(str(cell))+'</td>' for cell in row)+'</tr>' for row in table['rows'])+'</tbody></table></div>'
        if x.get('diagram'):
            name=x['diagram']
            svg=(ROOT/'images/408'/f'{name}.svg').read_text()
            caption=x.get("diagram_caption", "概念结构示意图 · 已写明模型约定；具体电路和参数以题设为准。")
            content+='<figure class="study-figure"><div class="study-diagram-scroll" tabindex="0" aria-label="示意图，可横向滚动">'+svg+'</div><figcaption>'+e(caption)+' <a href="images/408/'+e(name)+'.svg" target="_blank" rel="noopener noreferrer">单独查看图片</a></figcaption></figure>'
        if x.get('sources'):
            content+='<p class="study-note">参考：'+'；'.join('<a href="'+e(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(r['title'])+'</a>' for r in x['sources'])+'</p>'
        if x.get('code'): content+=f'<h4>代码对照</h4><pre><code>{e(x["code"])}</code></pre>'
        content+=f'''<details class="study-recall"><summary>自检：{e(x['check'])}</summary><p>{e(x['answer'])}</p></details>'''
    return f'''<details class="study-card glass" id="{x['id']}" data-subject="{e(x['subject'])}" data-chapter="{e(x['chapter'])}" data-tags="{e(' '.join(tags))}" data-search="{e(search,quote=True)}"><summary><span class="study-card-title">{e(x['title'])}</span><span class="study-badges">{badges}</span><span class="study-expand-hint" aria-hidden="true">解析</span></summary><div class="study-card-body">{content}{state_controls(x['id'])}</div></details>'''
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
def directory():
    out='<section class="section" id="coverage"><div class="container"><div class="section-head"><h2>四科章节目录</h2></div><div class="study-directory">'
    for subject,slug in zip(subjects,slugs):
        chapters=list(dict.fromkeys(x['chapter'] for x in data['items'] if x['subject']==subject))
        out+='<article class="panel glass"><h3>'+subject+'</h3><ul>'+''.join(f'<li><a href="#{slug}-chapter-{i+1}">'+e(ch)+'</a></li>' for i,ch in enumerate(chapters))+'</ul></article>'
    return out+'</div><p class="study-note">结构：定义与正确结论 → 原理与适用条件 → 易混辨析 → 例子 → 自检解析。计时数值与公式均以各条约定为准。</p></div></section>'
refs='''<section class="section anchor-offset" id="references"><div class="container"><div class="section-head"><h2>内容说明与参考</h2></div><article class="panel glass study-reference"><p>个人错题包含近期答卷错误、概念疑问和不完整步骤；补充知识点单独标注。分类可重叠。“近年考查”标出已核对真题的年份与题号，供重点复习，不是下次考试的概率预测。冷门指容易漏复习的细节，不代表统计后的出题频率。概念解析为重新组织的讲解，具体真题仍以题设为准。</p><p>本页先整理已取回的近期问题，未核实的题号和成绩不填。按公开 408 四科章节组织，不把实现特例当作通用公式。更新：2026-10-20。</p><ul><li><a href="https://www.xit.edu.cn/yjsfk/kyzykwtkw/list.htm" target="_blank" rel="noopener noreferrer">厦门工学院公开真题资料：已核对 2022、2024、2025 年相关题目</a></li><li><a href="https://algs4.cs.princeton.edu/23quicksort/" target="_blank" rel="noopener noreferrer">Princeton Algorithms：快排实现边界</a>；<a href="https://algs4.cs.princeton.edu/43mst/index.php" target="_blank" rel="noopener noreferrer">最小生成树</a></li><li><a href="https://pages.cs.wisc.edu/~remzi/OSTEP/" target="_blank" rel="noopener noreferrer">OSTEP：进程、地址转换、并发与文件系统</a></li><li><a href="https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html" target="_blank" rel="noopener noreferrer">Intel 架构手册：指令与标志位（具体架构示例）</a></li><li><a href="https://www.rfc-editor.org/rfc/rfc9293.html" target="_blank" rel="noopener noreferrer">RFC 9293：TCP</a>；<a href="https://www.rfc-editor.org/rfc/rfc791" target="_blank" rel="noopener noreferrer">RFC 791：IPv4</a></li></ul></article></div></section>'''
for calc in (False,True):
    filename='408-calculations.html' if calc else '408.html'
    title='计算专项' if calc else '易错易混与冷门考点'
    lead='按题设列式，逐步核对。复杂计算集中在这里。8 道自编变式，全部配过程与易错提醒。' if calc else f'{len(data["items"])} 个知识点，按 408 四科章节整理。含个人错题、易错易混、冷门细节、记忆公式与结构图；复杂计算放在独立专项。'
    body=hero(title,lead,calc)+(directory() if not calc else '')+controls(calc)+'<p id="study-empty" class="container study-empty" hidden>没有匹配内容。试试减少关键词或重置筛选。</p>'+groups(calc)+refs
    (ROOT/filename).write_text(page(filename,'408 · '+title,lead,body))
print('Built 408.html and 408-calculations.html')

# Keep storage bounds in step with new content while preserving existing IDs.
js=ROOT/"js/408.js"
code=js.read_text()
limits={prefix:max(int(x["id"][1:]) for x in rows) for prefix,rows in [("k",data["items"]),("c",data["calculations"])]}
code=re.sub(r"const MARK_LIMITS = \{ k: \d+, c: \d+ \};", f"const MARK_LIMITS = {{ k: {limits['k']}, c: {limits['c']} }};", code)
js.write_text(code)
