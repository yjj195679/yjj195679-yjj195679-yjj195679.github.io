"""Build the complete, logically ordered handbook408 handbook (no browser data fetch)."""
import json,re,hashlib,subprocess
from pathlib import Path
from html import escape
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'data/408-handbook.json').read_text())
assert items and all('sections' in x for x in items),'Expected complete structured knowledge data'
assert len({x['id'] for x in items})==len(items)
expressions=sorted(set(f['tex'] for x in items for s in x['sections'] for f in s.get('formulas',[])))
math_html=json.loads(subprocess.run(['node',str(root/'tools/render-408-math.cjs')],input=json.dumps(expressions),capture_output=True,text=True,check=True).stdout)


def rich(value):
    # Only **emphasis** is interpreted; all source text is otherwise escaped.
    return ''.join('<strong>'+escape(part)+'</strong>' if i%2 else escape(part) for i,part in enumerate(re.split(r'\*\*(.*?)\*\*',str(value))))

groups=defaultdict(list)
for item in items:groups[(item['subject'],item['chapter'])].append(item)
nav=[];chapters=[];last=None;points=0
for n,((subject,chapter),rows) in enumerate(groups.items(),1):
    key='chapter-'+hashlib.sha1((subject+'|'+chapter).encode()).hexdigest()[:10]
    if subject!=last:
        nav.append(f'<span class="index-subject">{escape(subject)}</span>');last=subject
    nav.append(f'<a href="#{key}" data-chapter-link="{key}"><span>{escape(chapter)}</span><span class="index-count">{len(rows)}</span></a>')
    cards=[]
    for row in rows:
        blocks=[]
        for section in row['sections']:
            kind=section['kind'];assert kind in {'concept','key','contrast','example','memory','detail'}
            text=''
            if section.get('paragraphs'):
                points+=len(section['paragraphs']);text+=''.join('<p>'+rich(p)+'</p>' for p in section['paragraphs'])
            if section.get('bullets'):
                points+=len(section['bullets']);text+='<ul>'+''.join('<li>'+rich(p)+'</li>' for p in section['bullets'])+'</ul>'
            if section.get('points'):
                points+=len(section['points']);text+='<ul>'+''.join('<li>'+rich(p)+'</li>' for p in section['points'])+'</ul>'
            if section.get('rows'):
                points+=len(section['rows']);cols=section['columns']
                assert all(len(r)==len(cols) for r in section['rows'])
                text+='<div class="handbook408-table-scroll" role="region" tabindex="0" aria-label="'+escape(section['heading'])+'对照表"><table><thead><tr>'+''.join('<th scope="col">'+rich(c)+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(c)+'</td>' for c in r)+'</tr>' for r in section['rows'])+'</tbody></table></div>'
            if section.get('table'):
                table=section['table'];cols=table['headers'];table_rows=table['rows'];points+=len(table_rows)
                assert all(len(r)==len(cols) for r in table_rows),row['title']
                text+='<div class="handbook408-table-scroll" role="region" tabindex="0" aria-label="'+escape(section['heading'])+'对照表"><table><thead><tr>'+''.join('<th scope="col">'+rich(c)+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(c)+'</td>' for c in r)+'</tr>' for r in table_rows)+'</tbody></table></div>'
            if section.get('diagram'):
                name=section['diagram'];assert re.fullmatch(r'[a-z-]+',name)
                svg=(root/'images/408'/f'{name}.svg').read_text().replace(name+'-',row['id']+'-'+name+'-')
                text+='<figure class="handbook408-diagram"><div class="handbook408-diagram-scroll" tabindex="0" aria-label="图解，可横向滚动">'+svg+'</div><figcaption><a href="images/408/'+name+'.svg" target="_blank" rel="noopener noreferrer">单独查看图片</a></figcaption></figure>';points+=1
            if section.get('simulation'):
                sim=section['simulation'];payload=json.dumps(sim,ensure_ascii=False).replace('<','\\u003c')
                transcript='<ol>'+''.join('<li><strong>'+escape(step['title'])+'</strong>：'+escape(step['explain'])+'</li>' for step in sim['steps'])+'</ol>'
                text+='<div class="study-sim"><p class="sim-title">'+escape(sim['title'])+'</p><script type="application/json" class="sim-data">'+payload+'</script><div class="sim-interactive" hidden></div><details class="sim-transcript"><summary>查看完整步骤（也可离线阅读）</summary>'+transcript+'</details></div>';points+=len(sim['steps'])
            if section.get('code'):
                text+='<pre tabindex="0" aria-label="算法代码，可横向滚动"><code>'+escape(section['code'])+'</code></pre>';points+=1
            if section.get('formulas'):
                for formula in section['formulas']:
                    text+='<div class="handbook408-formula" tabindex="0" aria-label="公式，可横向滚动">'+math_html[formula['tex']]+'</div><p class="handbook408-formula-note">'+rich(formula.get('note',''))+'</p>';points+=1
            assert text, row['title']
            blocks.append(f'<section class="handbook408-section kind-{kind}"><h4>{escape(section["heading"])}</h4>{text}</section>')
        badge=' · '.join(dict.fromkeys({'concept':'概念','key':'重点','contrast':'辨析','example':'例算','memory':'助记','detail':'展开'}[s['kind']] for s in row['sections']))
        visual_diagrams=sum(bool(sec.get('diagram')) for sec in row['sections']);visual_animations=sum(bool(sec.get('simulation')) for sec in row['sections'])
        visual_badges=('<span class="visual-badges">'+(' <span>图解 '+str(visual_diagrams)+'</span>' if visual_diagrams else '')+(' <span>动画 '+str(visual_animations)+'</span>' if visual_animations else '')+'</span>') if visual_diagrams or visual_animations else ''
        cards.append(f'''<details class="formula-card handbook408-card" id="{row['id']}" data-subject="{escape(subject)}" data-has-diagram="{int(visual_diagrams>0)}" data-has-animation="{int(visual_animations>0)}" data-legacy-ids="{escape(" ".join(row.get("legacyIds",[])))}" data-chapter="{key}"><summary><span class="formula-card-title">{rich(row['title'])}</span><span class="formula-card-number">{row['number']}</span><span class="formula-card-summary">{escape(row['lead'])}</span><span class="handbook408-card-parts">{escape(badge)}{visual_badges}</span></summary><div class="formula-card-body">{''.join(blocks)}<div class="formula-actions" hidden><button class="button" type="button" data-mark="review" aria-pressed="false">待复习</button><button class="button" type="button" data-mark="mastered" aria-pressed="false">已掌握</button><a class="button" href="#{row['id']}" aria-label="{escape(row['title'])}的固定链接">定位链接</a><span class="formula-state-text">未标记</span></div></div></details>''')
    chapters.append(f'<section class="formula-chapter" id="{key}" data-subject="{escape(subject)}"><div class="formula-chapter-head"><h2>{escape(chapter)}</h2><span>{escape(subject)} · <span data-chapter-count>{len(rows)}</span> 条</span></div><div class="formula-card-list">{"".join(cards)}</div></section>')
diagram_total=len({sec['diagram'] for item in items for sec in item['sections'] if sec.get('diagram')})
animation_total=sum(bool(sec.get('simulation')) for item in items for sec in item['sections'])
subjects=list(dict.fromkeys(x['subject'] for x in items))
options=''.join('<option value="'+escape(s)+'">'+escape(s)+'</option>' for s in subjects)
base=(root/'math-formulas.html').read_text();header=base[base.index('  <header'):base.index('\n\n  <main')]
html=f'''<!doctype html>
<html lang="zh-CN" class="handbook408-root"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f"><title>408 · 系统知识手册 · True Path M</title><meta name="description" content="按四科知识脉络整理数据结构、计算机组成原理、操作系统与计算机网络，保留原理、条件、计算、代码、图表与辨析。"><link rel="canonical" href="https://1956799.xyz/408-handbook.html"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/tpm-serif.woff2" as="font" type="font/woff2" crossorigin><script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20260909-15"><link rel="stylesheet" href="css/math-formulas.css?v=20261025-3"><link rel="stylesheet" href="js/vendor/katex/katex.min.css"><link rel="stylesheet" href="css/408-handbook.css?v=20261106-systems-9"></head>
<body data-page="study" class="math-handbook handbook408-handbook"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>{header}
<main id="main"><section class="subhero formula-hero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="courses.html">← 返回学习</a><div class="kicker">2027 考研 · 计算机专业基础</div><h1>408 系统知识手册</h1><p>从基础概念走向机制、算法与计算：按四科知识依赖重新组织讲解，保留关键表述、适用条件、步骤、例子与对照。系统学习与针对性纠错分开，阅读时可以交叉参照。</p><div class="formula-stat-row"><span><strong>{len(items)}</strong> 条知识卡片</span><span><strong>{len(groups)}</strong> 个章节</span><span><strong>{points}</strong> 个展开分点</span><span><strong>{diagram_total}</strong> 张机制图解</span><span><strong>{animation_total}</strong> 组逐步演示</span><span><strong id="handbook408-progress">0</strong> 条已掌握</span></div><nav class="hero-actions" aria-label="408 板块"><a class="button primary" href="408-handbook.html" aria-current="page">系统知识手册</a><a class="button" href="408.html">易错易混与冷门考点</a><a class="button" href="408-calculations.html">计算专项</a></nav></article></div></section>
<section class="section formula-controls" aria-labelledby="handbook408-filter-title"><div class="container"><article class="panel glass"><div class="formula-controls-head"><div><div class="kicker">搜索 · 定位 · 复习</div><h2 id="handbook408-filter-title">按线索查找知识</h2></div><p id="handbook408-count" role="status" aria-live="polite">共 {len(items)} 条知识卡片</p></div><div class="handbook408-legend" aria-label="重点配色说明"><span class="legend-concept">蓝 · 概念与原理</span><span class="legend-key">红 · 结论与条件</span><span class="legend-contrast">橙 · 易混辨析</span><span class="legend-example">紫 · 计算与例子</span><span class="legend-memory">绿 · 方法与助记</span></div>
<div id="handbook408-controls" hidden><div class="visual-filter-row" role="group" aria-label="图解与动画筛选"><button type="button" class="button" data-visual-filter="" aria-pressed="true">全部知识</button><button type="button" class="button" data-visual-filter="diagram" aria-pressed="false">含图解</button><button type="button" class="button" data-visual-filter="animation" aria-pressed="false">含逐步动画</button></div><div class="formula-filter-grid"><label><span>关键词</span><input id="handbook408-search" type="search" placeholder="如：补码、Cache、PV、子网、TCP" autocomplete="off"></label><label><span>模块</span><select id="handbook408-subject"><option value="">全部模块</option>{options}</select></label><label><span>章节</span><select id="handbook408-chapter"><option value="">全部章节</option></select></label><label><span>掌握状态</span><select id="handbook408-state"><option value="">全部状态</option><option value="review">待复习</option><option value="mastered">已掌握</option><option value="unmarked">未标记</option></select></label></div><div class="formula-toolbar"><button class="button primary" id="handbook408-random" type="button">随机抽查一条</button><button class="button" id="handbook408-reset" type="button">重置筛选</button><button class="button" id="handbook408-expand" type="button">展开结果</button><button class="button" id="handbook408-collapse" type="button">收起结果</button><button class="button" id="handbook408-print" type="button">打印当前结果</button></div><p class="formula-storage-note" id="handbook408-storage">点击卡片查看完整内容。标记保存在当前浏览器；再次点击同一标记可取消。随机抽查只从当前筛选结果中选取。</p></div><noscript><p>可直接展开下方知识卡片阅读；启用 JavaScript 后可搜索、筛选和保存复习标记。</p></noscript></article></div></section>
<section class="section formula-layout"><div class="container formula-layout-grid"><aside class="formula-index panel glass" aria-label="章节目录"><details class="handbook408-directory" open><summary>知识脉络与章节</summary><nav id="handbook408-index">{''.join(nav)}</nav></details></aside><div class="formula-content"><p id="handbook408-empty" class="panel glass" hidden>没有匹配的知识点。请减少关键词或重置筛选。</p><div id="handbook408-groups">{''.join(chapters)}</div></div></div></section>
<section class="section"><div class="container"><article class="panel glass formula-reference"><div class="section-head"><div><div class="kicker">学习顺序</div><h2>先建立主线，再对照细节</h2></div><p class="section-intro">2026-11-06 更新</p></div><ul><li>数据结构：先确认数据与存储模型，再学线性结构、树图、查找排序；复杂度、边界和实现条件贯穿其中。</li><li>计算机组成原理：从数据表示与运算出发，连接存储层次、指令、处理器、总线和输入输出。</li><li>操作系统：从运行机制和进程线程出发，理解调度、同步、存储、文件与设备管理。</li><li>计算机网络：按分层体系衔接链路、路由、传输与应用；区分协议规则、时间线、地址与计算条件。</li><li><a href="408.html">易错易混与冷门考点</a>保留原有个人错题与针对性辨析；<a href="408-calculations.html">计算专项</a>单独训练。手册的复习标记独立保存。</li><li>蓝、红、橙、紫、绿分别提示概念、关键条件、辨析、例算和方法。颜色只作辅助，公式与结论须连同适用条件阅读。</li><li>协议和实现细节可对照 <a href="https://www.rfc-editor.org/rfc/rfc9293.html" target="_blank" rel="noopener noreferrer">TCP 规范</a>、<a href="https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html" target="_blank" rel="noopener noreferrer">Intel 架构手册</a>与 <a href="https://pages.cs.wisc.edu/~remzi/OSTEP/" target="_blank" rel="noopener noreferrer">OSTEP</a>。具体架构和题设约定单独说明。</li></ul></article></div></section></main>
<footer class="footer"><div class="container footer-inner"><div>© <span id="year">2026</span> True Path M · Personal Website</div><div class="footer-links"><a href="index.html">首页</a><a href="courses.html">学习</a><a href="math-formulas.html">数学一</a><a href="408.html">408</a></div></div></footer><script src="js/main.js?v=20261105-408-separate-1" defer></script><script src="js/408-handbook.js?v=20261106-systems-9" defer></script><script src="js/408-visuals.js?v=20261106-systems-9" defer></script><script src="js/408-simulations.js?v=20261106-systems-9" defer></script></body></html>
'''
(root/'408-handbook.html').write_text(html)
(root/'data/408-handbook-stats.json').write_text(json.dumps(dict(cards=len(items),chapters=len(groups),points=points,subjects=len(subjects)),ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(items)} complete cards, {len(groups)} chapters, {points} detailed points.')
