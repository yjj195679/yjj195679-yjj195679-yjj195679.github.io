"""Generate original SVG study schematics; no external fonts, images, or scripts."""
from pathlib import Path
from html import escape as esc
ROOT=Path(__file__).resolve().parents[1]/'images/408'
ROOT.mkdir(parents=True,exist_ok=True)
def text(x,y,label,size=24,anchor='middle',klass=''):
 label=label.replace('⌈m/2⌉','ceil(m/2)').replace('₋₁','-1').replace('₀','0').replace('≥','>=').replace('≤','<=').replace('−','-')
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" class="{klass}">{esc(label)}</text>'
def box(x,y,w,h,lines):
 s=f'<rect class="d-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
 for i,line in enumerate(lines):s+=text(x+w/2,y+h/2+(i-(len(lines)-1)/2)*30+8,line)
 return s
def arrow(points,prefix,control=False):
 return f'<polyline class="d-arrow {"d-control" if control else ""}" points="{points}" marker-end="url(#{prefix}-arrow)"/>'
def save(name,title,desc,body,height):
 style='''<style>.d-bg{fill:var(--diagram-bg,#fff)}.d-box{fill:var(--diagram-fill,#f1f4f8);stroke:var(--diagram-line,#58677a);stroke-width:2}.d-arrow{fill:none;stroke:var(--diagram-line,#58677a);stroke-width:2.5}.d-control{stroke-dasharray:8 6}text{fill:var(--diagram-text,#17212f);font-family:"TPM Serif","Songti SC",STSong,SimSun,"Times New Roman",serif}.d-muted{fill:var(--diagram-muted,#46566b)}.d-emphasis{font-weight:700}.d-band{fill:var(--diagram-fill,#f1f4f8)}</style>'''
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {height}" role="img" aria-labelledby="{name}-title {name}-desc"><title id="{name}-title">{esc(title)}</title><desc id="{name}-desc">{esc(desc)}</desc>{style}<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--diagram-line,#58677a)"/></marker></defs><rect class="d-bg" width="960" height="{height}" rx="12"/>{text(40,45,title,30,"start","d-emphasis")}{body}</svg>'
 (ROOT/(name+'.svg')).write_text(svg+'\n')
name='multiplier';b=text(40,82,'无符号 n 位操作数 · C:A:Q 组合右移模型',22,'start','d-muted')
b+=box(60,120,240,80,['M：被乘数','n 位，保持不变'])+box(360,120,220,80,['n 位加法器','A + M → C:A'])+box(670,120,240,80,['控制器读取 Q₀','1：加 M；0：保持'])
b+=arrow('300,160 360,160',name)+arrow('470,200 470,285',name)
b+=arrow('245,285 245,235 395,235 395,200',name)+text(155,240,'A 反馈',22)
b+=arrow('790,285 790,200',name,True)+arrow('670,160 580,160',name,True)
b+=box(60,285,90,85,['C','进位'])+box(155,285,355,85,['A：高半部分积','n 位，初始为 0'])+box(515,285,395,85,['Q：低半积 / 乘数','n 位，初始装乘数'])
b+=arrow('85,425 875,425',name)+text(480,409,'每轮将 C:A:Q 联合逻辑右移一位',25)
b+=text(480,474,'加法进位先保留，右移时最高位补 0',24)+text(480,525,'重复 n 轮：最终 A:Q 为 2n 位乘积',27,'middle','d-emphasis')
save(name,'串行乘法器：判位 → 加法 → 联合右移','M 输入加法器，A 反馈到加法器，结果写入 C 和 A。Q 的最低位控制是否相加；C A Q 一起右移，进行 n 轮后 A Q 是乘积。',b,565)
name='booth';b=text(40,83,'补码乘法 · 观察顺序固定为 (Q0, Q-1)',22,'start','d-muted')
b+=box(330,115,300,70,['检查 (Q0, Q-1)'])
b+=box(40,235,270,80,['00 或 11','A 保持不变'])+box(345,235,270,80,['01','A ← A + M'])+box(650,235,270,80,['10','A ← A − M'])
for center in [175,480,785]:b+=arrow(f'480,185 480,205 {center},205 {center},235',name)
b+=box(80,395,800,85,['A:Q:Q₋₁ 联合算术右移一位','最高位补 A 的符号位'])
for center in [175,480,785]:b+=arrow(f'{center},315 {center},355 480,355 480,395',name)
b+=text(480,525,'Q₋₁ 初始为 0；重复 n 轮后读取 A:Q',25)+text(480,568,'M 为最小负数时，A 与 ±M 须用足够位宽',23,'middle','d-muted')
save(name,'Booth 判位规则：01 加、10 减', 'Q 零位和附加位为 00 或 11 则不变，为 01 则加 M，为 10 则减 M。然后联合算术右移，保留符号。',b,610)
name='divider';b=text(40,82,'无符号恢复余数模型 · M > 0 · A 留额外试减位',22,'start','d-muted')
b+=box(230,110,500,75,['初始 A = 0，Q = 被除数，M = 除数'])
b+=box(230,225,500,80,['A:Q 左移一位','试减 A ← A − M'])+arrow('480,185 480,225',name)
b+=box(65,375,365,100,['试减后 A < 0','A ← A + M（恢复）','Q₀ ← 0'])+box(530,375,365,100,['试减后 A ≥ 0','保留试减结果','Q₀ ← 1'])
b+=arrow('480,305 480,340 247,340 247,375',name)+arrow('480,305 480,340 712,340 712,375',name)
b+=box(200,535,560,75,['循环 n 轮：Q 为商，A 为余数'])
b+=arrow('247,475 247,505 480,505 480,535',name)+arrow('712,475 712,505 480,505 480,535',name)
b+=text(480,655,'核对：被除数 = M × Q + A，且 0 ≤ A < M',24,'middle','d-emphasis')
save(name,'除法器：左移 → 试减 → 判商位','Q 从被除数逐轮变成商，A 从零成为余数。每轮左移后减 M，负则恢复余数并置商位零，非负置一。结束核对等式和余数范围。',b,695)
name='btree-height';b=text(40,82,'m>=3；a=ceil(m/2)；根为第 1 层；n 为关键字数',21,'start','d-muted')
b+=text(250,125,'最稀疏：关键字下限',25,'middle','d-emphasis')+text(715,125,'最充满：关键字上限',25,'middle','d-emphasis')
b+=box(80,150,340,70,['第 1 层：1 个根','1 个关键字'])+box(535,150,360,70,['第 1 层：1 个根','m−1 个关键字'])
b+=box(80,260,340,85,['第 2 层：2 个结点','每个 a−1 个关键字'])+box(535,260,360,85,['第 2 层：m 个结点','每个 m−1 个关键字'])
b+=arrow('250,220 250,260',name)+arrow('715,220 715,260',name)
b+=box(65,405,370,85,['第 h 层：2a^(h−2) 个结点','每个 a−1 个关键字'])+box(520,405,390,85,['第 h 层：m^(h−1) 个结点','每个 m−1 个关键字'])
b+=arrow('250,345 250,405',name)+arrow('715,345 715,405',name)
b+=text(250,540,'n_min = 2*a^(h-1) - 1',24,'middle','d-emphasis')+text(715,540,'n_max = m^h - 1',24,'middle','d-emphasis')
b+=text(480,590,'反解高度，再按整数取整；h=1 时最少关键字为 1',23)
b+=text(480,629,'图中第 h 层展开适用于 h≥2；失败结点不计入高度',22,'middle','d-muted')
save(name,'B 树高度：先记两端关键字数','最少情况下根含一个关键字并有两个孩子，其余结点至少含 a 减一个关键字。最大情况下所有结点含 m 减一个关键字。两端总数分别为二乘 a 的 h减一次方减一，和 m 的 h 次方减一。',b,665)
name='tcp-timers';b=text(40,82,'同属 TCP，但触发条件不同；不是一套固定的秒数',23,'start','d-muted')
rows=[('已发送数据未获确认','重传计时器 RTO','重传最早未确认数据'),('对端公告零窗口','持续计时器 Persist','探测接收窗口是否恢复'),('启用保活且长期空闲','保活计时器 Keepalive','探测对端存活状况'),('主动关闭进入等待状态','TIME_WAIT / 2MSL','防旧段混淆；可补发最后 ACK')]
for i,(trigger,timer,action) in enumerate(rows):
 y=125+i*112;b+=box(35,y,265,82,[trigger])+box(340,y,280,82,[timer])+box(660,y,270,82,(['防旧段混淆','可补发最后 ACK'] if i==3 else [action]));b+=arrow(f'300,{y+41} 340,{y+41}',name)+arrow(f'620,{y+41} 660,{y+41}',name)
b+=text(480,600,'“窗口更新丢失”想持续；“闲置连接”想保活',25,'middle','d-emphasis')
save(name,'TCP 计时器：四种场景对照','从未确认数据、零窗口、长时间空闲和主动关闭四种场景，分别对应重传、持续、保活和时间等待机制。',b,640)
name='network-timers';b=text(40,82,'字段、重组等待、路由老化：先辨机制，再记数值',23,'start','d-muted')
b+=box(45,125,400,100,['IPv4 首部 TTL','转发时递减；归零丢弃'])+box(515,125,400,100,['目的端的 IP 重组超时','分片不全到期后丢弃'])
b+=text(245,267,'TTL 不是 TCP 重传计时器',24)+text(715,267,'IP 不自动按缺片重传',24)
b+=text(40,340,'RIP 的典型标准参数',27,'start','d-emphasis')
b+=box(45,385,250,95,['周期更新','约 30 s'])+box(355,385,250,95,['最后更新后 180 s','路由失效，度量 = 16'])+box(665,385,250,95,['失效后再 120 s','垃圾收集删除'])
b+=arrow('605,432 665,432',name)
b+=text(480,533,'RIP：左框是周期事件；中→右是无更新时的失效流程',22,'middle','d-muted')
b+=text(480,580,'协议参数/实现配置以题设为准，不套用成所有网络的秒数',23)
save(name,'网络层相关时间机制：TTL / 重组 / RIP','TTL 是逐跳递减字段，IP 重组端维护分片等待超时。RIP 周期更新约三十秒，路由无更新一百八十秒失效，再经一百二十秒垃圾收集删除。',b,620)
print('Built 6 original SVG diagrams')
