"""Build the complete, logically ordered politics handbook (no browser data fetch)."""
import json,re,hashlib
from pathlib import Path
from html import escape
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'data/politics-knowledge.json').read_text())
assert items and all('sections' in x for x in items),'Expected complete structured knowledge data'
assert len({x['id'] for x in items})==len(items)

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
            if section.get('points'):
                points+=len(section['points']);text+='<ul>'+''.join('<li>'+rich(p)+'</li>' for p in section['points'])+'</ul>'
            if section.get('rows'):
                points+=len(section['rows']);cols=section['columns']
                assert all(len(r)==len(cols) for r in section['rows'])
                text+='<div class="politics-table-scroll" role="region" tabindex="0" aria-label="'+escape(section['heading'])+'对照表"><table><thead><tr>'+''.join('<th scope="col">'+rich(c)+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(c)+'</td>' for c in r)+'</tr>' for r in section['rows'])+'</tbody></table></div>'
            assert text, row['title']
            blocks.append(f'<section class="politics-section kind-{kind}"><h4>{escape(section["heading"])}</h4>{text}</section>')
        badge=' · '.join(dict.fromkeys({'concept':'概念','key':'重点','contrast':'辨析','example':'例算','memory':'助记','detail':'展开'}[s['kind']] for s in row['sections']))
        cards.append(f'''<details class="formula-card politics-card" id="{row['id']}" data-subject="{escape(subject)}" data-legacy-ids="{escape(" ".join(row.get("legacyIds",[])))}" data-chapter="{key}"><summary><span class="formula-card-title">{rich(row['title'])}</span><span class="formula-card-number">{row['number']}</span><span class="formula-card-summary">{escape(row['lead'])}</span><span class="politics-card-parts">{escape(badge)}</span></summary><div class="formula-card-body">{''.join(blocks)}<div class="formula-actions" hidden><button class="button" type="button" data-mark="review" aria-pressed="false">待复习</button><button class="button" type="button" data-mark="mastered" aria-pressed="false">已掌握</button><a class="button" href="#{row['id']}" aria-label="{escape(row['title'])}的固定链接">定位链接</a><span class="formula-state-text">未标记</span></div></div></details>''')
    chapters.append(f'<section class="formula-chapter" id="{key}" data-subject="{escape(subject)}"><div class="formula-chapter-head"><h2>{escape(chapter)}</h2><span>{escape(subject)} · <span data-chapter-count>{len(rows)}</span> 条</span></div><div class="formula-card-list">{"".join(cards)}</div></section>')
subjects=list(dict.fromkeys(x['subject'] for x in items))
options=''.join('<option value="'+escape(s)+'">'+escape(s)+'</option>' for s in subjects)
base=(root/'math-formulas.html').read_text();header=base[base.index('  <header'):base.index('\n\n  <main')]
html=f'''<!doctype html>
<html lang="zh-CN" class="politics-root"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f"><title>政治 · 完整知识手册 · True Path M</title><meta name="description" content="完整整理政治手册中的概念、原理、史纲时间线、会议政策、政经计算、助记与易混辨析，按知识逻辑重新编排，重点分色。"><link rel="canonical" href="https://1956799.xyz/politics.html"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/tpm-serif.woff2" as="font" type="font/woff2" crossorigin><script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20260909-15"><link rel="stylesheet" href="css/math-formulas.css?v=20261025-3"><link rel="stylesheet" href="css/politics.css?v=20261105-full-1"></head>
<body data-page="study" class="math-handbook politics-handbook"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>{header}
<main id="main"><section class="subhero formula-hero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="courses.html">← 返回学习</a><div class="kicker">2027 考研 · 政治</div><h1>政治知识点手册</h1><p>沿知识本身的逻辑展开：概念与原理相连，历史与会议相照。完整保留关键表述、限定条件、推导例子与助记，把重合内容合并，把易混关系讲清。</p><div class="formula-stat-row"><span><strong>{len(items)}</strong> 条知识卡片</span><span><strong>{len(groups)}</strong> 个章节</span><span><strong>{points}</strong> 个展开分点</span><span><strong id="politics-progress">0</strong> 条已掌握</span></div></article></div></section>
<section class="section formula-controls" aria-labelledby="politics-filter-title"><div class="container"><article class="panel glass"><div class="formula-controls-head"><div><div class="kicker">搜索 · 定位 · 复习</div><h2 id="politics-filter-title">按线索查找知识</h2></div><p id="politics-count" role="status" aria-live="polite">共 {len(items)} 条知识卡片</p></div><div class="politics-legend" aria-label="重点配色说明"><span class="legend-concept">蓝 · 概念与关系</span><span class="legend-key">红 · 结论与条件</span><span class="legend-contrast">橙 · 易混辨析</span><span class="legend-example">紫 · 计算与例子</span><span class="legend-memory">绿 · 口诀与助记</span></div>
<div id="politics-controls" hidden><div class="formula-filter-grid"><label><span>关键词</span><input id="politics-search" type="search" placeholder="如：必要劳动、八大、出发点、权利保障" autocomplete="off"></label><label><span>模块</span><select id="politics-subject"><option value="">全部模块</option>{options}</select></label><label><span>章节</span><select id="politics-chapter"><option value="">全部章节</option></select></label><label><span>掌握状态</span><select id="politics-state"><option value="">全部状态</option><option value="review">待复习</option><option value="mastered">已掌握</option><option value="unmarked">未标记</option></select></label></div><div class="formula-toolbar"><button class="button primary" id="politics-random" type="button">随机抽查一条</button><button class="button" id="politics-reset" type="button">重置筛选</button><button class="button" id="politics-expand" type="button">展开结果</button><button class="button" id="politics-collapse" type="button">收起结果</button><button class="button" id="politics-print" type="button">打印当前结果</button></div><p class="formula-storage-note" id="politics-storage">点击卡片查看完整内容。标记保存在当前浏览器；再次点击同一标记可取消。随机抽查只从当前筛选结果中选取。</p></div><noscript><p>可直接展开下方知识卡片阅读；启用 JavaScript 后可搜索、筛选和保存复习标记。</p></noscript></article></div></section>
<section class="section formula-layout"><div class="container formula-layout-grid"><aside class="formula-index panel glass" aria-label="章节目录"><details class="politics-directory" open><summary>知识脉络与章节</summary><nav id="politics-index">{''.join(nav)}</nav></details></aside><div class="formula-content"><p id="politics-empty" class="panel glass" hidden>没有匹配的知识点。请减少关键词或重置筛选。</p><div id="politics-groups">{''.join(chapters)}</div></div></div></section>
<section class="section"><div class="container"><article class="panel glass formula-reference"><div class="section-head"><div><div class="kicker">学习顺序</div><h2>先建立主线，再对照细节</h2></div><p class="section-intro">2026-11-05 更新</p></div><ul><li>马原按基础概念、原理联系、政治经济学与计算展开；先辨对象，再看条件和关系。</li><li>史纲先看历史分期与社会矛盾，再按时间推进；会议另作专题，便于交叉对照任务、结论和意义。</li><li>理论体系和新时代思想按基本问题、方法、治理领域组织；思法从人生与道德转向法治和权利义务。</li><li>颜色与文字标签共同提示层次，蓝、红、橙、紫、绿分别标记概念、重点、辨析、例算和助记；记忆时仍须读全限定条件。</li><li>2025年时政材料单独归档，年份和会议背景均予保留，避免同基础理论或后续动态混为一谈。</li></ul></article></div></section></main>
<footer class="footer"><div class="container footer-inner"><div>© <span id="year">2026</span> True Path M · Personal Website</div><div class="footer-links"><a href="index.html">首页</a><a href="courses.html">学习</a><a href="math-formulas.html">数学一</a><a href="408.html">408</a></div></div></footer><script src="js/main.js?v=20261105-full-1" defer></script><script src="js/politics.js?v=20261105-full-1" defer></script></body></html>
'''
(root/'politics.html').write_text(html)
(root/'data/politics-stats.json').write_text(json.dumps(dict(cards=len(items),chapters=len(groups),points=points,subjects=len(subjects)),ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(items)} complete cards, {len(groups)} chapters, {points} detailed points.')
