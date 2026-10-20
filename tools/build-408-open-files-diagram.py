"""Compare the textbook two-table abstraction with UNIX open-file descriptions."""
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
name='open-file-tables'
def text(x,y,s,size=22):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{e(s)}</text>'
def box(x,y,w,h,lines):
 return f'<rect class="of-node" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'+''.join(text(x+w/2,y+h/2+8+(i-(len(lines)-1)/2)*29,s) for i,s in enumerate(lines))
def arrow(p,dash=False):return f'<polyline class="of-arrow" points="{p}" marker-end="url(#{name}-arrow)"'+(' stroke-dasharray="7 6"' if dash else '')+'/>'
b=text(480,45,'打开文件表：进程记用法，系统记公共信息',29)
b+=text(480,90,'408 常见教材二表模型',22)
b+=box(40,130,390,130,['进程 P：fd = 3','读写位置 = 20；本次只读','系统表索引 = 7'])
b+=box(530,130,390,130,['进程 Q：fd = 4','读写位置 = 80；本次读写','系统表索引 = 7'])
b+=arrow('235,260 235,300 350,300 350,345')+arrow('725,260 725,300 610,300 610,345')
b+=box(215,345,530,130,['系统打开文件表：第 7 项','外存位置、大小等公共信息或引用','打开计数 = 2（两进程各打开一次）'])
b+=text(480,535,'fd → 进程表项 → 系统表项；同一文件，使用位置和权限可不同。',22)
style='''<style>.of-bg{fill:var(--diagram-bg,#fff)}.of-node{fill:var(--diagram-fill,#f1f4f8);stroke:var(--diagram-line,#58677a);stroke-width:2}.of-arrow{fill:none;stroke:var(--diagram-line,#58677a);stroke-width:2.3}.of-separator{stroke:var(--diagram-line,#58677a);stroke-width:1;stroke-dasharray:6 6}text{fill:var(--diagram-text,#17212f);font-family:"TPM Serif",SimSun,serif}</style>'''
desc='教材二表模型：进程 P、Q 的 fd 分别索引各自进程表项，各自记录读写位置和本次访问权限；二者引用系统表同一项，共享外存位置、大小等公共信息。图示两进程各打开一次，打开计数为二。'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 580" role="img" aria-labelledby="{name}-title {name}-desc"><title id="{name}-title">打开文件表的关系与字段归属</title><desc id="{name}-desc">{e(desc)}</desc>{style}<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="var(--diagram-line,#58677a)"/></marker></defs><rect class="of-bg" width="960" height="580" rx="12"/>{b}</svg>\n'
(ROOT/'images/408'/f'{name}.svg').write_text(svg)
print('Built open-file-tables.svg')
