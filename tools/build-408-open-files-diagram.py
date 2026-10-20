"""Compare the textbook two-table abstraction with UNIX open-file descriptions."""
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
name='open-file-tables'
def text(x,y,s,size=22):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{e(s)}</text>'
def box(x,y,w,h,lines):
 return f'<rect class="of-node" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'+''.join(text(x+w/2,y+h/2+8+(i-(len(lines)-1)/2)*29,s) for i,s in enumerate(lines))
def arrow(p,dash=False):return f'<polyline class="of-arrow" points="{p}" marker-end="url(#{name}-arrow)"'+(' stroke-dasharray="7 6"' if dash else '')+'/>'
b=text(480,45,'打开文件表：先区分模型，再判断字段位置',29)
b+=text(480,100,'A · 408 常见教材二表模型',26)
b+=box(40,135,390,145,['进程 P：fd = 3','读写指针 = 20；本次只读','系统表索引 = 7'])
b+=box(530,135,390,145,['进程 Q：fd = 4','读写指针 = 80；本次读写','系统表索引 = 7'])
b+=arrow('235,280 235,315 350,315 350,355')+arrow('725,280 725,315 610,315 610,355')
b+=box(215,355,530,150,['系统打开文件表：第 7 项','公共文件位置/大小/时间等信息或引用','打开计数 = 2（图示：两个进程各打开一次）','可引用 FCB / inode'])
b+=text(480,550,'共享公共文件信息，不要求两个进程使用相同位置或相同访问方式。',22)
b+='<line class="of-separator" x1="40" y1="585" x2="920" y2="585"/>'
b+=text(480,635,'B · UNIX/Linux 三层模型：fd 表 → 打开文件描述 → inode',25)
b+=text(160,680,'进程 fd 表',23)+text(485,680,'系统级打开实例',23)+text(810,680,'公共文件元数据',23)
b+=box(30,715,260,110,['P：fd3、fd4=dup(fd3)','各自有描述符标志','如 FD_CLOEXEC'])
b+=box(350,715,270,140,['打开文件描述 X','偏移量 = 20；读写方式','状态标志，如 O_APPEND','图示 fd 引用 = 3'])
b+=arrow('290,745 350,745')+arrow('290,790 350,790')
b+=box(30,890,260,85,['子进程 Q：继承 fd3','由仅有 fd3 时 fork 得到'])
b+=arrow('290,932 320,932 320,830 350,830',True)
b+=box(30,1040,260,100,['P：fd5 = 独立 open','再次打开同一文件'])
b+=box(350,1040,270,110,['打开文件描述 Y','偏移量 = 0；只读方式','图示 fd 引用 = 1'])
b+=arrow('290,1090 350,1090')
b+=box(700,850,230,220,['同一 inode','所有者 / 组','文件权限位等','文件大小、时间','数据块定位信息','不保存本次偏移量'])
b+=arrow('620,785 655,785 655,920 700,920')+arrow('620,1095 655,1095 655,1015 700,1015')
b+=text(480,1205,'fd3、fd4、继承的 fd3 共享 X 的位置；fd5 的 Y 独立，仍指向同一 inode。',22)
b+=text(480,1245,'本次打开方式不同于文件自身 rwx/ACL；两种模型的“系统表项”粒度不同。',22)
style='''<style>.of-bg{fill:var(--diagram-bg,#fff)}.of-node{fill:var(--diagram-fill,#f1f4f8);stroke:var(--diagram-line,#58677a);stroke-width:2}.of-arrow{fill:none;stroke:var(--diagram-line,#58677a);stroke-width:2.3}.of-separator{stroke:var(--diagram-line,#58677a);stroke-width:1;stroke-dasharray:6 6}text{fill:var(--diagram-text,#17212f);font-family:"TPM Serif",SimSun,serif}</style>'''
desc='上半部分为教材二表模型：P 与 Q 各自保存读写指针和访问方式，均指向系统表第 7 项，公共信息共享。下半部分为 UNIX/Linux：父进程 fd3、由 dup 产生的 fd4，以及在复制前仅有 fd3 时 fork 出的子进程 fd3，都引用同一打开文件描述 X，共享偏移量和打开方式；另一次 open 得到打开文件描述 Y，位置独立，X 与 Y 最终引用同一 inode。'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 1290" role="img" aria-labelledby="{name}-title {name}-desc"><title id="{name}-title">打开文件表的关系与字段归属</title><desc id="{name}-desc">{e(desc)}</desc>{style}<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="var(--diagram-line,#58677a)"/></marker></defs><rect class="of-bg" width="960" height="1290" rx="12"/>{b}</svg>\n'
(ROOT/'images/408'/f'{name}.svg').write_text(svg)
print('Built open-file-tables.svg')
