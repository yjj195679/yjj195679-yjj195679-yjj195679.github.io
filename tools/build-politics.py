"""Build the static politics handbook from its reviewed knowledge data."""
import json
from pathlib import Path
from html import escape as e
from collections import defaultdict
root = Path(__file__).resolve().parents[1]
items = json.loads((root / 'data/politics-knowledge.json').read_text())
assert len({x['id'] for x in items}) == len(items)
groups = defaultdict(list)
for x in items:
    assert all(x.get(k) for k in ('id', 'subject', 'chapter', 'title', 'body', 'pitfall'))
    groups[(x['subject'], x['chapter'])].append(x)
chapters = []
nav = []
last = None
for n, ((subject, chapter), rows) in enumerate(groups.items(), 1):
    key = f'chapter-{n:02}'
    if subject != last:
        nav.append(f'<span class="index-subject">{e(subject)}</span>')
        last = subject
    nav.append(f'<a href="#{key}" data-chapter-link="{key}"><span>{e(chapter)}</span><span class="index-count">{len(rows)}</span></a>')
    cards = []
    for x in rows:
        body = ''.join(f'<li>{e(p)}</li>' for p in x['body'])
        cards.append(f'''<details class="formula-card politics-card" id="{x['id']}" data-subject="{e(subject)}" data-chapter="{key}">
<summary><span class="formula-card-title">{e(x['title'])}</span><span class="formula-card-number">{x['id'].upper()}</span><span class="formula-card-summary">{e(subject)} · 点击展开复习</span></summary>
<div class="formula-card-body"><div class="politics-conclusion"><h4>知识结论</h4><ul>{body}</ul></div><div class="formula-meta warning"><h4>易混辨析</h4><p>{e(x['pitfall'])}</p></div>
<div class="formula-actions" hidden><button class="button" type="button" data-mark="review" aria-pressed="false">待复习</button><button class="button" type="button" data-mark="mastered" aria-pressed="false">已掌握</button><a class="button" href="#{x['id']}" aria-label="{e(x['title'])}的固定链接">定位链接</a><span class="formula-state-text">未标记</span></div></div></details>''')
    chapters.append(f'<section class="formula-chapter" id="{key}" data-subject="{e(subject)}"><div class="formula-chapter-head"><h2>{e(chapter)}</h2><span>{e(subject)} · <span data-chapter-count>{len(rows)}</span> 条</span></div><div class="formula-card-list">{"".join(cards)}</div></section>')
subjects = list(dict.fromkeys(x['subject'] for x in items))
options = ''.join(f'<option value="{e(s)}">{e(s)}</option>' for s in subjects)
template = (root/'math-formulas.html').read_text()
header = template[template.index('  <header'):template.index('\n\n  <main')]
page = f'''<!doctype html>
<html lang="zh-CN" class="politics-root"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f">
<title>政治 · 知识点手册 · True Path M</title><meta name="description" content="考研政治知识点手册：马原、史纲、毛中特、习近平新时代中国特色社会主义思想、思想道德与法治。按章节整理知识结论、会议时间线、政经计算和易混辨析。">
<link rel="canonical" href="https://1956799.xyz/politics.html"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/tpm-serif.woff2" as="font" type="font/woff2" crossorigin>
<script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20260909-15"><link rel="stylesheet" href="css/math-formulas.css?v=20261025-3"><link rel="stylesheet" href="css/politics.css?v=20261105-1"></head>
<body data-page="study" class="math-handbook politics-handbook"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>
{header}
<main id="main">
<section class="subhero formula-hero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="courses.html">← 返回学习</a><div class="kicker">2027 考研 · 政治</div><h1>政治知识点手册</h1><p>从原理到历史，从会议到概念。把知识结论与易混辨析放在一起，沿章节建立联系，在反复回看中查漏补缺。</p><div class="formula-stat-row"><span><strong>{len(items)}</strong> 条知识点</span><span><strong>{len(groups)}</strong> 个章节</span><span><strong>5</strong> 大模块</span><span><strong id="politics-progress">0</strong> 条已掌握</span></div></article></div></section>
<section class="section formula-controls" aria-labelledby="politics-filter-title"><div class="container"><article class="panel glass"><div class="formula-controls-head"><div><div class="kicker">快速定位</div><h2 id="politics-filter-title">搜索与筛选</h2></div><p id="politics-count" role="status" aria-live="polite">共 {len(items)} 条知识点</p></div>
<div id="politics-controls" hidden><div class="formula-filter-grid"><label><span>关键词</span><input id="politics-search" type="search" placeholder="如：遵义会议、剩余价值、宪法" autocomplete="off"></label><label><span>模块</span><select id="politics-subject"><option value="">全部模块</option>{options}</select></label><label><span>章节</span><select id="politics-chapter"><option value="">全部章节</option></select></label><label><span>掌握状态</span><select id="politics-state"><option value="">全部状态</option><option value="review">待复习</option><option value="mastered">已掌握</option><option value="unmarked">未标记</option></select></label></div>
<div class="formula-toolbar"><button class="button primary" id="politics-random" type="button">随机抽查一条</button><button class="button" id="politics-reset" type="button">重置筛选</button><button class="button" id="politics-expand" type="button">展开结果</button><button class="button" id="politics-collapse" type="button">收起结果</button><button class="button" id="politics-print" type="button">打印当前结果</button></div><p class="formula-storage-note" id="politics-storage">复习标记保存在当前浏览器。再次点击同一标记可取消；随机抽查仅从当前筛选结果中选取。</p></div><noscript><p>可直接展开下方知识卡片阅读；启用 JavaScript 后可搜索、筛选和记录复习状态。</p></noscript></article></div></section>
<section class="section formula-layout"><div class="container formula-layout-grid"><aside class="formula-index panel glass" aria-label="章节目录"><details class="politics-directory" open><summary>章节目录</summary><nav id="politics-index">{''.join(nav)}</nav></details></aside><div class="formula-content"><p id="politics-empty" class="panel glass" hidden>没有匹配的知识点。请减少关键词或重置筛选。</p><div id="politics-groups">{''.join(chapters)}</div></div></div></section>
<section class="section"><div class="container"><article class="panel glass formula-reference"><div class="section-head"><div><div class="kicker">复习方法</div><h2>把结论放回语境</h2></div><p class="section-intro">2026-11-05 整理</p></div><ul><li>先看标题尝试回忆，再展开核对；容易混淆的条目标为待复习。</li><li>会议按年份、任务、结论对应记忆；政经计算先分清条件与分母，再代入数值。</li><li>同一表述要结合历史阶段和问题层次理解，不能把关键词当成脱离条件的万能判断。</li><li>本页以基础理论和专题梳理为主，动态时政需结合后续公布的权威文件另行复习。</li></ul></article></div></section>
</main><footer class="footer"><div class="container footer-inner"><div>© <span id="year">2026</span> True Path M · Personal Website</div><div class="footer-links"><a href="index.html">首页</a><a href="courses.html">学习</a><a href="math-formulas.html">数学一</a><a href="408.html">408</a></div></div></footer>
<script src="js/main.js?v=20261105-politics" defer></script><script src="js/politics.js?v=20261105-1" defer></script></body></html>
'''
(root/'politics.html').write_text(page)
print(f'Built {len(items)} cards in {len(groups)} chapters.')
