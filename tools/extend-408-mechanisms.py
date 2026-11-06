"""Second expansion: exact algorithm states and mechanism examples, idempotently attached."""
from pathlib import Path
import json,copy,html
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'data/408-handbook.json').read_text());by={x['title']:x for x in items};examples=[]
def node(id,x,y,label,w=150,h=62,tone='base'):return dict(id=str(id),x=x,y=y,label=str(label),w=w,h=h,tone=tone)
def edge(a,b,label='',directed=True):return dict(a=str(a),b=str(b),label=label,directed=directed)
def frame(title,explain,nodes,edges=(),note='',wires=()):return dict(title=title,explain=explain,nodes=copy.deepcopy(nodes),edges=copy.deepcopy(edges),note=note,wires=copy.deepcopy(wires))
def add(card,slug,title,steps,static=-1):
 assert card in by,card
 examples.append((card,'mechanism-'+slug,dict(scene='board',title=title,steps=steps,height=420),static))
def row(values,active=(),done=(),y=100,prefix='v'):
 w=min(260,790/max(1,len(values)));return [node(prefix+str(i),40+i*w,y,v,w-8,80,'active' if i in active else 'done' if i in done else 'base') for i,v in enumerate(values)]
def story(card,slug,title,states,note=''):
 add(card,slug,title,[frame(t,e,row(v,a),note=note) for t,v,e,a in states])
def tree(values,links):
 return [node(id,x,y,label,130,60,tone+(' rb-red' if '红' in label else ' rb-black' if '黑' in label else '')) for id,x,y,label,tone in values],[edge(a,b) for a,b in links]
# 1-8 DATA STRUCTURES
rb=[('g',390,20,'20 · 黑','base'),('p',200,145,'10 · 红','base'),('u',610,145,'30 · 红','base')];links=[('g','p'),('g','u')];steps=[]
for t,e,vals,ls in [
 ('原树','省略的NIL叶子均为黑色；初始根20为黑、孩子10与30为红，满足红黑性质。',rb,links),
 ('插入5，出现红红相邻','按BST规则把5插在10左侧，新增结点先红。父10与叔30都红，不能只把5改黑。',rb+[('x',65,275,'5 · 红','active')],links+[('p','x')]),
 ('父叔变黑，祖父变红','把10、30改黑，把20改红，抵消子树黑高变化；红色冲突可能向祖先传播。',[('g',390,20,'20 · 红','active'),('p',200,145,'10 · 黑','done'),('u',610,145,'30 · 黑','done'),('x',65,275,'5 · 红','base')],links+[('p','x')]),
 ('根恢复黑色','20恰好是根，最后把根改黑。所有根到NIL路径具有相同黑高；本次不需旋转。',[('g',390,20,'20 · 黑','done'),('p',200,145,'10 · 黑','done'),('u',610,145,'30 · 黑','done'),('x',65,275,'5 · 红','base')],links+[('p','x')])]:
 n,es=tree(vals,ls);steps.append(frame(t,e,n,es,note='颜色同时用文字标明；未画出的左右NIL均为黑色。'))
add('红黑树插入的父叔祖父分类','rbt-red-uncle','红黑树插入：红叔叔时为何先变色',steps)
steps=[]
for t,e,v,l in [
 ('插入20后形成LR','原树根30黑、左孩子10红。插入20红成为10右孩子，父红，叔是黑色NIL。',[('g',520,20,'30 · 黑','base'),('p',180,145,'10 · 红','base'),('x',340,280,'20 · 红','active')],[('g','p'),('p','x')]),
 ('先对10左旋','先把折线变成直线：20代替10成为30的左孩子，10转为20的左孩子；中序仍为10、20、30。',[('g',520,20,'30 · 黑','base'),('x',340,145,'20 · 红','active'),('p',180,280,'10 · 红','base')],[('g','x'),('x','p')]),
 ('再右旋30并重新着色','20上升后改黑，30下沉改红，10仍红。根黑、无相邻红结点，黑高一致。',[('x',390,20,'20 · 黑','done'),('p',180,200,'10 · 红','base'),('g',610,200,'30 · 红','base')],[('x','p'),('x','g')])]:
 n,es=tree(v,l);steps.append(frame(t,e,n,es,note='标准红黑树插入修复的LR示例；不是删除修复规则。'))
add('红黑树插入的父叔祖父分类','rbt-black-uncle','红黑树插入：黑叔叔与LR双旋',steps)
steps=[]
for t,e,root,left,right in [('删除前','3阶B树每个非根至少1个、至多2个关键字。根[20]，左右叶分别[10]、[30,40]。','20','10','30 | 40'),('删10后左叶下溢','左叶变空，右兄弟有2个关键字，可借；不能把30直接跳过父结点搬到左叶。','20','空','30 | 40'),('父键下移，兄弟最小键上移','20下移到左叶，右兄弟30上移替换父键，右叶留下40；范围顺序仍成立。','30','20','40')]:
 n=[node('r',375,30,root),node('l',150,250,left,210,75,'active'),node('s',600,250,right,210,75)];steps.append(frame(t,e,n,[edge('r','l'),edge('r','s')]))
add('B 树删除后的借位、合并与根收缩','btree-borrow','B树删除：经父结点向右兄弟借位',steps)
steps=[]
for t,e,ns,es in [
 ('删除前','3阶B树根[20]，两个叶为[10]、[30]，兄弟都只有最低允许的1个关键字。',[node('r',375,30,'20'),node('l',150,240,'10'),node('s',600,240,'30')],[edge('r','l'),edge('r','s')]),
 ('删除10，不能再借','左叶变空，右叶只有30，不能再借；必须把父分隔键20与右叶合并。',[node('r',375,30,'20'),node('l',150,240,'空',tone='active'),node('s',600,240,'30')],[edge('r','l'),edge('r','s')]),
 ('合并并收缩根','把空左叶、父键20、右叶30合成[20,30]。旧根变空且仅余一个孩子，因此该孩子提升为新根，高度减1。',[node('l',325,100,'20 | 30',250,90,'done')],[])]:steps.append(frame(t,e,ns,es))
add('B 树删除后的借位、合并与根收缩','btree-merge','B树删除：兄弟不能借时合并与根收缩',steps)
coords={'A':(60,40),'B':(300,40),'C':(60,245),'D':(300,245)};gedges=[edge('A','B',directed=False),edge('A','C',directed=False),edge('B','D',directed=False),edge('C','D',directed=False)]
steps=[];visited=[]
for current,stack,exp in [('A',['A'],'从A开始，发现即标记；邻接访问顺序按字母升序。'),('B',['A','B'],'A先访问B，保留A尚未完成的递归状态。'),('D',['A','B','D'],'B的A已访问，转而深入D。'),('C',['A','B','D','C'],'D的B已访问，再深入C；C邻居A、D均已访问。'),('D',['A','B','D'],'C结束，返回调用者D；回退不再次输出D。'),('B',['A','B'],'D结束，返回B。'),('A',['A'],'B结束，返回A；A的另一邻居C已访问，不再递归。'),('',[],'A结束，递归栈清空；DFS发现顺序A、B、D、C。')]:
 if current and current not in visited:visited.append(current)
 ns=[node(v,*xy,v,95,65,'active' if v==current else 'done' if v in visited else 'base') for v,xy in coords.items()]+[node('stack',550,65,'递归栈（右端为栈顶）\n'+' → '.join(stack),310,120),node('out',550,265,'发现顺序\n'+' → '.join(visited),310,85)]
 steps.append(frame('深入 '+current if current and exp.startswith(('从','A先','B的','D的')) else '返回 / 结束',exp,ns,gedges))
add('DFS 与生成森林','dfs-stack','DFS：深入与回退时递归栈怎样变化',steps)
steps=[];chosen=[]
for a,b,w,take in [('A','B',1,True),('B','C',2,True),('A','C',3,False),('C','D',4,True)]:
 if take:chosen.append(f'{a}{b}({w})')
 ns=[node(v,*xy,v,95,65,'active' if v in (a,b) else 'base') for v,xy in coords.items()]+[node('sel',530,70,'已选边\n'+'\n'.join(chosen),330,190)]
 es=[edge('A','B','1',False),edge('B','C','2',False),edge('A','C','3',False),edge('C','D','4',False)]
 steps.append(frame(('接受' if take else '拒绝')+f'边{a}{b}，权{w}', '两个端点属于不同连通分量，合并它们并选边。' if take else 'A和C已通过A—B—C连通，再选AC会成环，故跳过。',ns,es,note='边按权1、2、3、4考察；最终3条边，总权7。'))
add('Kruskal 算法与并查集判环','kruskal-cycle','Kruskal：为什么要跳过一条较轻的边',steps)
D=[[0,3,10],[999,0,2],[999,999,0]];steps=[]
for k in range(-1,3):
 before=copy.deepcopy(D)
 if k>=0:
  for i in range(3):
   for j in range(3):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
 ns=[]
 for i in range(3):
  ns.append(node('r'+str(i),40,50+i*95,'ABC'[i],65,70))
  for j in range(3):ns.append(node(f'{i}{j}',150+j*150,50+i*95,'∞' if D[i][j]>=999 else D[i][j],130,70,'active' if D[i][j]!=before[i][j] else 'base'))
 ns.append(node('ex',650,85,'列依次A、B、C\n允许中间点：'+('无' if k<0 else 'ABC'[:k+1]),220,150))
 steps.append(frame('初始距离' if k<0 else '允许经过'+ 'ABC'[k], '原有向边A→B=3、B→C=2、A→C=10。' if k<0 else ('以B作中间点，A→C更新为min(10,3+2)=5。' if k==1 else '检查D[i][k]+D[k][j]，本轮没有更短路径。'),ns))
add('Floyd 的动态规划与适用范围','floyd-intermediate','Floyd：距离矩阵为何要把k放在最外层',steps)
L=[(2,'左'),(5,'左'),(7,'左')];Q=[(2,'右'),(4,'右'),(8,'右')];i=j=0;out=[];steps=[]
while i<len(L) or j<len(Q):
 if j==len(Q) or (i<len(L) and L[i][0]<=Q[j][0]):v=L[i];i+=1
 else:v=Q[j];j+=1
 out.append(v)
 ns=row([f'{v}{tag}' for v,tag in out],active=[len(out)-1],y=250)+[node('l',35,40,'左路剩余\n'+' '.join(str(v) for v,t in L[i:]),370,95),node('r',485,40,'右路剩余\n'+' '.join(str(v) for v,t in Q[j:]),370,95)]
 steps.append(frame(f'输出 {v[0]}（{v[1]}路）','比较两路当前最小值；相等时先取左路，保持同关键字记录的原始先后次序。',ns,note='两路输入都必须已经有序；元素后面的左右标签只用于核对稳定性。'))
add('二路归并排序的合并与稳定性','merge-stability','有序归并：两个相等的2应该先取谁',steps)
# 9-16 COMPUTER ORGANIZATION
steps=[]
for a,b,title in [(7,1,'0111+0001'),(15,1,'1111+0001'),(8,8,'1000+1000'),(3,2,'0011+0010')]:
 res=(a+b)&15;carry=int(a+b>15);signed=lambda n:n-16 if n&8 else n;overflow=int(not(-8<=signed(a)+signed(b)<=7))
 ns=row([f'A={a:04b}',f'B={b:04b}',f'结果={res:04b}'],[2])+row([f'CF={carry}',f'OF={overflow}',f'SF={(res>>3)&1}',f'ZF={int(res==0)}'],y=270,prefix='f')
 steps.append(frame(title,f'无符号解释：{a}+{b}={a+b}；4位有符号解释：{signed(a)}+{signed(b)}={signed(a)+signed(b)}。CF看最高位进位，OF看有符号真值是否超出[−8,7]。',ns,note='4bit加法模型；只保留低4位。CF和OF可独立为0或1。'))
add('ZF、SF、OF、CF：四个标志的含义','flags-cf-of','同一加法器：CF和OF为何可能不相同',steps)
story('整数类型转换：位串不变、截断与扩展','sign-extension','1111扩成8位：符号扩展与零扩展',[
 ('原始4bit',['原位串=1111','有符号=-1','无符号=15'],'同一位串在4bit补码与无符号解释下真值不同。',[0]),
 ('有符号扩宽',['1111 → 11111111','补复制的符号位1','8bit补码仍=-1'],'要保持有符号真值，扩宽时在高位复制符号位。',[0,1]),
 ('无符号扩宽',['1111 → 00001111','高位补0','8bit无符号仍=15'],'要保持无符号真值，扩宽时高位补0。',[0,1]),
 ('同宽重新解释',['11111111','补码解释=-1','无符号解释=255'],'同宽改变解释不改位串；实际C表达式还要先按整数提升与类型转换规则确定位宽。',[1,2])])
# Booth: 4bit two's complement, one arithmetic shift for each multiplier bit.
A=0;Q=(-3)&15;M=3;qm=0;steps=[frame('初始化','4bit补码，M=0011(+3)，Q=1101(−3)，A=0000，附加位Q−1=0。目标3×(−3)=−9。',row(['M=0011','A=0000','Q=1101','Q−1=0']))]
for k in range(4):
 pair=((Q&1)<<1)|qm;op={0:'不加减',1:'A=A+M',2:'A=A−M',3:'不加减'}[pair]
 if pair==1:A=(A+M)&15
 if pair==2:A=(A-M)&15
 steps.append(frame(f'轮{k+1}，Q₀Q−1={pair:02b}',op+'；Booth规则：01加M、10减M、00/11不变，然后整体算术右移。',row([f'A={A:04b}',f'Q={Q:04b}',f'Q−1={qm}'],[0]),note='每轮加减按4bit补码截断，整体算术右移保留A的符号。'))
 combined=(A<<5)|(Q<<1)|qm;combined=(combined>>1)|(combined&256);A=(combined>>5)&15;Q=(combined>>1)&15;qm=combined&1
 steps.append(frame(f'轮{k+1}整体算术右移','把A、Q和附加位连接后右移1位，最高位复制原A符号位。',row([f'A={A:04b}',f'Q={Q:04b}',f'Q−1={qm}'],[0,1,2]),note=f'A|Q={A:04b}{Q:04b}'))
assert (A<<4)|Q==247
steps[-1]['explain']+=' 四轮后A|Q=11110111，8bit补码为−9；附加位不属于乘积。'
add('加法器、进位链与 ALU','booth-multiply','Booth补码乘法：3×(−3)的寄存器变化',steps)
# Hamming(7,4), even parity, positions counted left to right for this diagram.
bits=[0,0,1,0,0,1,1];steps=[]
for pos,cover in [(1,[1,3,5,7]),(2,[2,3,6,7]),(4,[4,5,6,7])]:
 bits[pos-1]=sum(bits[i-1] for i in cover if i!=pos)%2
 ns=row([f'{i+1}:{b}' for i,b in enumerate(bits)],[i-1 for i in cover]);steps.append(frame(f'计算校验位p{pos}',f'偶校验覆盖位置{cover}，计算p{pos}={bits[pos-1]}，使该组1的总数为偶数。',ns,note='数据1011依次放位置3、5、6、7；校验位放1、2、4。'))
code=bits[:];received=bits[:];received[5]^=1;syndrome=sum(pos*(sum(received[i-1] for i in cover)%2) for pos,cover in [(1,[1,3,5,7]),(2,[2,3,6,7]),(4,[4,5,6,7])]);assert syndrome==6
steps.append(frame('传输中第6位翻转','接收端按相同覆盖组检查，得到s1=0、s2=1、s4=1；综合征s4s2s1=110₂=6，定位到第6位。',row([f'{i+1}:{b}' for i,b in enumerate(received)],[5]),note='本例假定至多1bit出错；普通(7,4)码不能可靠区分全部双bit错误。'))
steps.append(frame('翻转第6位恢复','把第6位从0改回1，重新检验各组均为偶校验，得到码字'+''.join(map(str,code))+'。',row([f'{i+1}:{b}' for i,b in enumerate(code)],[5]),note='位置1→7从左到右绘制；综合征仍按s4s2s1解释。'))
add('检错纠错编码：码距、奇偶校验与海明码','hamming-correct','海明(7,4)码：校验组与综合征怎样定位错位',steps)
story('同步、异步、半同步与分离事务','four-phase-handshake','四相异步握手：REQ和ACK不是同一条信号',[
 ('空闲',['REQ=0','ACK=0','无有效请求'],'主从双方无未完成握手。',[]),
 ('主方提出请求',['REQ=1','ACK=0','地址/写数据保持有效'],'主方准备好本次信息后置REQ=1，并保持规定信号稳定。',[0]),
 ('从方完成响应',['REQ=1','ACK=1','读数据有效或写入完成'],'从方准备完成后置ACK=1；主方看到ACK再接受结果或确认完成。',[1,2]),
 ('主方撤销请求',['REQ=0','ACK=1','进入复位阶段'],'主方处理确认后撤销REQ。',[0]),
 ('从方撤销确认',['REQ=0','ACK=0','回到空闲'],'从方看到REQ撤销后撤销ACK，四相互锁握手完成；不是所有异步总线都采用此种握手。',[1])])
story('中断响应、向量入口与嵌套屏蔽','interrupt-nesting','中断嵌套：高优先级处理完返回哪里',[
 ('执行主程序',['主程序P','中断现场栈：空'],'假设允许嵌套，H的处理优先级高于L，均未被屏蔽。',[0]),
 ('进入低优先级L',['处理中断L','栈：P断点与状态'],'响应L时保存P的必要现场；L处理程序按体系结构要求保存额外寄存器。',[0,1]),
 ('L中允许更高优先级中断',['处理中断H','栈底：P现场\n栈顶：L断点与状态'],'仅在允许嵌套并满足屏蔽/优先级条件时，H才可打断L；不是所有处理中断时都开放全部中断。',[0,1]),
 ('H先返回L',['继续处理L','栈：P断点与状态'],'H完成后弹出L的现场，先继续L，不直接跳回P。',[0]),
 ('L再返回P',['恢复主程序P','中断现场栈：空'],'L完成再恢复P的断点与状态；优先级与进程调度是不同概念。',[0])])
story('指令周期、机器周期、时钟周期与四类阶段','fetch-microops','取指微操作：PC如何把下一条指令送入IR',[
 ('PC送地址',['PC=0x1000','MAR ← PC','发出主存读请求'],'以按字节编址、定长4B指令的简化CPU为例；这里只演示取指阶段。',[1]),
 ('读出指令',['主存[0x1000]','MDR ← 指令位串','等待存储器就绪'],'MAR提供地址，MDR暂存返回数据；实际访存可能跨多个时钟周期。',[1]),
 ('进入指令寄存器',['IR ← MDR','PC ← PC+4','PC=0x1004'],'把指令送入IR并按定长指令长度更新PC；两项能否同拍由数据通路决定。',[0,1]),
 ('译码后执行',['IR中的操作码','控制器形成控制信号','本例尚未做操作数运算'],'取指完成不代表整条指令完成。变长指令、分支与不同架构的PC更新规则另按题设。',[0,1])])
story('SRAM、DRAM 与刷新','dram-refresh','DRAM刷新：周期、行数与死区怎样联系',[
 ('刷新要求',['128行','每行2ms内刷新一次','每行刷新100ns'],'假设逐行刷新，所有行都必须在2ms保持期内刷新至少一次。',[]),
 ('集中刷新',['128次连续刷新','死区=128×100ns','总计12.8μs'],'把各行刷新集中执行，这一段内普通访存受到阻塞。',[1,2]),
 ('异步分散安排',['平均行刷新间隔','2ms÷128','15.625μs'],'均匀分散时平均每15.625μs启动一次行刷新；不是每个存储周期都必须刷新。',[1,2]),
 ('区分三个时间',['保持期：2ms','行刷新耗时：100ns','行启动间隔：15.625μs'],'三者含义不同。实际DRAM内部行数、刷新命令粒度和并行行为由器件规定，此为考试简化模型。',[0,1,2])])
# 17-24 OPERATING SYSTEMS
story('记录型信号量的P、V与负值含义','semaphore-queue','记录型信号量：负数与等待队列同时变化',[
 ('初始',['S=1','CPU持有者：无','等待队列：空'],'按408常见记录型定义：P先减1，若<0则入队阻塞；V先加1，若≤0则唤醒一个等待者。',[]),
 ('P0执行P(S)',['S=0','P0进入临界区','等待队列：空'],'P0把1减为0，仍非负，获得资源。',[0,1]),
 ('P1执行P(S)',['S=−1','P0仍在临界区','等待队列：P1'],'P1减到−1而阻塞；负值绝对值对应本模型中等待者数。',[0,2]),
 ('P2执行P(S)',['S=−2','P0仍在临界区','等待队列：P1,P2'],'P2也阻塞；图按FIFO唤醒约定演示，真实队列策略可不同。',[0,2]),
 ('P0执行V(S)',['S=−1','P1被唤醒','等待队列：P2'],'加到−1仍≤0，唤醒P1。P1转为可运行状态，何时真正执行还取决于调度。',[0,1,2]),
 ('P1完成后V(S)',['S=0','P2被唤醒','等待队列：空'],'P1获得CPU并完成临界区后释放，唤醒P2；被唤醒者从原P操作之后继续。',[0,1]),
 ('P2完成后V(S)',['S=1','持有者：无','等待队列：空'],'所有等待都完成，资源重新空闲。',[0])])
story('软件互斥：单标志、双标志与Peterson','peterson-race','Peterson：同时想进入时turn让谁先走',[
 ('双方表达意愿',['flag[0]=true','flag[1]=true','尚未判断while'],'假设普通教材的顺序一致内存模型，读写原子且执行顺序不被重排。',[]),
 ('P0让P1先行',['flag均为true','P0写turn=1','P0尚未进入'],'P0完成自己的入口赋值；此时若P0立即检查，会暂时等待P1。',[1]),
 ('P1最后写turn=0',['flag均为true','turn=0','检查两人的while'],'P1把优先进入权让给P0；最后一次turn写入决定本次竞争结果。',[1]),
 ('P0通过，P1等待',['P0：flag1 && turn==1 为假','P1：flag0 && turn==0 为真','P0进入临界区'],'只有P0可进入；P1自旋等候。',[0,2]),
 ('P0退出',['flag[0]=false','P1条件变假','P1可以进入'],'P0退出时清自己的意愿，P1继续；现代语言/硬件实现须使用适当原子与内存顺序，不能直接照抄普通变量代码。',[0,1])])
story('读者—写者：读者优先及其饥饿问题','readers-count','读者优先：只有第一位读者锁住写者',[
 ('初始',['readcount=0','rw=1','mutex=1'],'rw控制读者组与写者互斥，mutex保护readcount；图省略每次计数临界区外的mutex恢复过程。',[]),
 ('第一位读者R1进入',['readcount=1','P(rw) → rw=0','R1开始读'],'R1在mutex保护下把计数从0加到1，第一位读者执行P(rw)。',[0,1]),
 ('R2进入并发读',['readcount=2','rw仍=0','R1与R2并发读'],'后续读者只增加计数，不再P(rw)。计数修改受mutex保护，读文件本身可并发。',[0,2]),
 ('写者W到达',['readcount=2','W执行P(rw)后阻塞','已有读者继续'],'W等待整组读者离开；按记录型实现rw.value可变为−1，此处rw=0的前两步只表示无等待时资源占用。',[1]),
 ('R1退出',['readcount=1','W仍等待','R2继续读'],'非最后一位读者不释放rw。',[0]),
 ('R2退出',['readcount=0','最后读者V(rw)','W被唤醒'],'计数归零时释放写锁。若读者持续到达使计数永不归零，写者可能饥饿；入口闸门可用于改进。',[0,1,2])])
# Circular resource allocation drawn as a genuine cycle.
ns=[node('p0',50,40,'哲学家P0'),node('p1',650,40,'哲学家P1'),node('p2',350,290,'哲学家P2')];steps=[]
for t,e,labels in [('各拿左筷','以3位哲学家构成的简化环为例，每人已获得一根筷子；若所有人都这样做，仍可能等待下一根。',['P0持C0','P1持C1','P2持C2']),('再请求右筷','P0等C1、P1等C2、P2等C0，形成循环等待。此处箭头表示等待持有者。',['P0持C0等C1','P1持C1等C2','P2持C2等C0']),('按筷子编号递增申请','统一先申请编号小的筷子，再申请编号大的筷子。原来的持有分配不会同时形成，消除循环等待。',['P0先C0后C1','P1先C1后C2','P2先C0后C2'])]:
 n=copy.deepcopy(ns)
 for q,l in zip(n,labels):q['label']=l;q['w']=190
 steps.append(frame(t,e,n,[edge('p0','p1'),edge('p1','p2'),edge('p2','p0')] if t=='再请求右筷' else [],note='有序申请防死锁；是否公平、是否饥饿是另外的问题。'))
add('哲学家进餐：多资源申请的死锁与解决','dining-order','哲学家进餐：循环等待怎样被统一顺序打破',steps)
steps=[]
for t,e,blocks in [('初始64KiB','把物理空间抽象为[0,64)KiB一个空闲块。',[(0,64,'空闲64')]),('申请13KiB，需16KiB块','向上取2的幂：16KiB；64先拆32，再把一个32拆成两个16。',[(0,16,'占用16'),(16,32,'空闲16'),(32,64,'空闲32')]),('申请9KiB，再取16KiB块','使用[16,32)块。两个16块互为伙伴，但有占用时不能合并。',[(0,16,'占用16'),(16,32,'占用16'),(32,64,'空闲32')]),('释放第一块','[0,16)变空闲，伙伴[16,32)仍占用，所以暂不能合并。',[(0,16,'空闲16'),(16,32,'占用16'),(32,64,'空闲32')]),('释放第二块并逐级合并','两个16伙伴合为[0,32)，再与空闲伙伴[32,64)合为64KiB。',[(0,64,'空闲64')])]:
 ns=[node(str(a),40+a*12,110,label+'\n['+str(a)+','+str(b)+')KiB',(b-a)*12-8,125,'active' if '占用' in label else 'done') for a,b,label in blocks];steps.append(frame(t,e,ns,note='只有大小相同、地址对齐且互为伙伴的空闲块才能合并。'))
add('伙伴系统与物理页框回收','buddy-coalesce','伙伴系统：13KiB为何要分配16KiB',steps)
story('调页时机、工作集与抖动','working-set','工作集窗口：最近4次访问会留下哪些页',[
 ('最近访问1,2,3,1',['最近4次：1,2,3,1','工作集={1,2,3}','共3个不同页面'],'工作集按访问历史窗口定义，不是简单最近新装入的页。',[1]),
 ('下一次访问4',['最近4次：2,3,1,4','工作集={1,2,3,4}','现在需要4个页面'],'窗口向前推进一次，取窗口中的不同页集合。',[1,2]),
 ('下一次再访问4',['最近4次：3,1,4,4','工作集={1,3,4}','重复4只算一页'],'页2退出窗口；窗口中访问次数不等于不同页个数。',[1]),
 ('驻留集小于活跃需求',['若仅3个页框','活跃工作集可能要4页','频繁置换导致抖动风险'],'工作集用于判断局部性与内存需求；具体是否抖动仍取决于实际访问序列和分配策略。',[1,2])])
steps=[]
for t,e,labels in [('open一次','进程open文件得到fd3，系统打开文件实例记录共享偏移0。',['fd3','偏移=0']),('dup(fd3)→fd4','复制描述符指向同一个打开实例，因此fd3、fd4共享偏移。',['fd3 与 fd4','偏移=0']),('read(fd3,100)','假设成功读100B，共享偏移从0变100，fd4随后读取也从100继续。',['fd3 与 fd4','偏移=100']),('再次open得到fd5','新open创建另一个打开实例，偏移从0开始，仍可引用同一inode。',['fd3 与 fd4','共享偏移=100；fd5偏移=0'])]:
 ns=[node('fd',30,70,labels[0],220,90),node('of',350,70,labels[1],290,90,'active'),node('in',700,250,'同一个inode\n文件数据',180,95)]
 es=[edge('fd','of'),edge('of','in')]
 if t=='再次open得到fd5':ns.extend([node('f5',30,280,'fd5',220,70),node('o5',350,280,'独立打开实例\n偏移=0',260,90)]);es.extend([edge('f5','o5'),edge('o5','in')]);ns[1]['label']='打开实例A\n偏移=100'
 steps.append(frame(t,e,ns,es,note='忽略错误、文件尾、追加模式及并发读写；dup共享打开实例，再次open通常独立。'))
add('进程打开表、系统打开表与inode','dup-offset','dup与再次open：文件偏移到底是否共享',steps)
story('共享存储、消息传递与管道','pipe-eof','管道：读者为什么等不到EOF',[
 ('创建pipe后fork',['父：读端r、写端w','子：读端r、写端w','两进程都继承端点'],'常见Unix匿名管道场景，设父写子读。',[]),
 ('关闭不用的端点',['父关闭r，保留w','子关闭w，保留r','避免多余写端引用'],'fork继承的不用端点应关闭；特别是读进程自己也持有写端时会影响EOF。',[0,1]),
 ('父写入ABC',['父写入3B','子读出ABC','缓冲区随后为空'],'一次read可能读少于请求长度；管道是字节流，不保留应用消息边界。',[1]),
 ('父关闭最后写端',['写端引用数=0','缓冲区已空','子read返回0（EOF）'],'只有全部写端关闭且已有数据读完后，读端才见EOF。',[0,2]),
 ('若子忘记关闭继承的w',['仍有写端引用','空管道上阻塞read','此时不会返回EOF'],'即使父已经退出，子自己的写端引用仍阻止EOF；非阻塞模式下则按规则报告暂不可读。',[0,1])])
# 25-32 COMPUTER NETWORKS
story('停止等待：差错、确认丢失与重复帧','stopwait-ack-loss','停止等待：ACK丢失后如何避免重复交付',[
 ('发送数据帧0',['发送方：帧0在途','接收方：期待0'],'使用交替位0/1的简化可靠协议，发送方保存未确认帧并启动定时器。',[0]),
 ('帧0收到并交付',['接收方已交付0','改为期待帧1','发ACK0'],'ACK0在此表示确认帧0，勿与TCP确认下一个期望字节的ack混用。',[0,1]),
 ('ACK0丢失',['发送方仍等ACK0','接收方仍期待1','不重复交付'],'发送方不能凭空知道接收方已收到，等待确认直至超时。',[0]),
 ('超时重传帧0',['发送方重发0','接收方识别为重复0','丢弃副本并再发ACK0'],'接收方看到旧序号，避免再次交付，但再次确认以帮助发送方继续。',[1,2]),
 ('收到ACK0后发1',['发送方转发帧1','接收方期待1','双方重新同步'],'确认使发送窗口前移；序号帮助区分新数据与重传副本。',[0,1])])
raw='01111110';stuff=[];ones=0;steps=[]
for i,b in enumerate(raw):
 stuff.append(b);ones=ones+1 if b=='1' else 0;inserted=ones==5
 if inserted:stuff.append('0');ones=0
 steps.append(frame('扫描输入第'+str(i+1)+'位', '已连续看到5个1，立即插入一个0，使数据中不会出现定界标志。' if inserted else '按原样输出本位；连续1的计数遇0清零。',row(['原数据：'+raw,'输出：'+''.join(stuff)],[1]),note='零比特填充仅用于规定的数据范围；帧标志01111110本身不填充。'))
assert ''.join(stuff)=='011111010'
steps.append(frame('接收端删除填充0','接收端在数据区域每看到连续5个1，就删除紧随的填充0，恢复原数据01111110。',row(['线路数据：011111010','恢复数据：01111110'],[1])))
add('四种组帧方法及填充的逆过程','bit-stuffing','零比特填充：第五个1之后为什么插0',steps)
# CRC long division uses computed XOR rows; original codeword checked independently.
work=list(map(int,'1101000'));gen=list(map(int,'1011'));steps=[frame('补零','数据1101，生成多项式1011（次数3），先补3个0，得到1101000。',row(['被除数：1101000','除数：1011']))]
for i in range(4):
 if not work[i]:continue
 before=''.join(map(str,work))
 for j in range(4):work[i+j]^=gen[j]
 after=''.join(map(str,work));steps.append(frame('对齐第'+str(i+1)+'位并异或',f'{before} 与移位后的{("0"*i)+"1011"+("0"*(3-i))}异或，得到{after}。异或相同为0，不同为1，无借位。',row(['本步之前\n'+before,'异或之后\n'+after],[1]),note='只在当前首位为1时异或；首位为0时继续右移对齐。'))
assert ''.join(map(str,work[-3:]))=='001'
steps.append(frame('得到3位余数001','原数据拼余数得到发送码字1101001；不要把7位补零后的被除数再拼上余数。',row(['原数据1101','CRC余数001','发送1101001'],[2])))
add('检错、纠错与可靠交付','crc-xor','CRC模2长除：1101000除以1011的每次异或',steps)
# Genuine time/space diagram for the worst-case collision detection argument.
steps=[]
for t,e,elapsed in [('A刚开始发送','两端传播时延τ。最坏情形中，A先发送；B在A信号即将到达前一瞬仍听到空闲，也开始发送。',0),('B在接近τ时开始发送','B在t≈τ才感知碰撞；A尚需等待B的信号沿链路反向传播回来。',1),('A在接近2τ时检测到碰撞','要确保A尚未发完时能检测到最远端碰撞，最短帧发送时间必须至少2τ。此为共享半双工CSMA/CD模型。',2)]:
 ns=[node('a',20,25,'发送端A',150,55),node('b',720,25,'发送端B',150,55),node('n',160,330,'时间向下；横向表示链路空间；τ是单程传播时延',580,65)]
 wires=[dict(id='life-a',points=[[95,85],[95,310]]),dict(id='life-b',points=[[795,85],[795,310]])]
 if elapsed>=1:wires.append(dict(id='forward',points=[[95,95],[795,195]]))
 if elapsed>=2:wires.append(dict(id='back',points=[[795,195],[95,295]]))
 steps.append(frame(t,e,ns,wires=wires,note='忽略碰撞检测与中继器附加延迟；实际标准把相关开销纳入时隙设计。'))
add('CSMA/CD、争用期与最短帧','csma-propagation','CSMA/CD时空图：争用期为何是2τ',steps)
# Manchester waveform: mid-bit low-to-high represents 0 for this example.
wavebits='1010';points=[]
for i,b in enumerate(wavebits):
 x=100+i*170;left,right=(150,260) if b=='1' else (260,150)
 if points:points.append([x,left])
 else:points=[[x,left]]
 points.extend([[x+85,left],[x+85,right],[x+170,right]])
steps=[]
for i in range(4):
 ns=[node('v'+str(k),100+k*170,30,f'bit{k}={v}',160,80,'active' if k==i else 'base') for k,v in enumerate(wavebits)]+[node('high',15,135,'高',55,35),node('low',15,245,'低',55,35)]
 steps.append(frame('观察第'+str(i+1)+'位：'+wavebits[i],'本例沿用正文约定：0在位中间低→高，1在位中间高→低。每位中间必有跳变，可提取时钟；位边界是否跳变取决于相邻位。',ns,note='横轴为时间，图上150为高电平、260为低电平。不同教材可采用相反的0/1约定。',wires=[dict(id='signal',points=points[:(i+1)*4])]))
# Use a complete per-bit prefix, without depending on boundary deduplication.
for i,s in enumerate(steps):
 end=100+(i+1)*170;prefix=[p for p in points if p[0]<=end];s['wires']=[dict(id='signal',points=prefix)]
add('数字编码与调制：时钟信息在哪里','manchester-wave','曼彻斯特波形：把1010画成电平跳变',steps)
story('RIP 表项更新例子与报文长度','rip-update','RIP更新：原下一跳报坏消息时也必须改',[
 ('原路由表',['目的网N','距离2','下一跳B'],'路由器A当前通过邻居B到N，距离2。此处采用经典跳数模型。',[]),
 ('B报告距离4',['B到N距离4','A候选距离4+1=5','下一跳仍是B'],'先把邻居报告的距离加1，因为还要走A到B的一跳。',[1]),
 ('原下一跳变差，仍更新',['目的网N','新距离5','下一跳B'],'由于更新来自原下一跳，必须接受变差，不能永远只保留旧距离2。',[1]),
 ('另一邻居C报告距离3',['C报告3→候选4','4优于当前5','改走C，距离4'],'来自其他下一跳时，若候选更短则替换；相等时的实现选择按题设。',[1,2]),
 ('C随后报告不可达',['报告距离16','加1后仍按16封顶','当前经C路由不可达'],'RIP的16为无穷，15跳是最大可达距离。若存在其他已知可用路径，应重新选择；不能把17当新可达距离。',[1,2])])
story('零窗口死锁与持续计时器','zero-window-probe','零窗口探测：丢失的窗口更新怎样恢复',[
 ('接收方缓冲区满',['B通告rwnd=0','A停止新增发送','A保留连接'],'零窗口表示接收方暂时无可用空间，与网络拥塞不是同一原因。',[0,1]),
 ('B释放缓冲并通告',['B更新rwnd>0','窗口更新ACK丢失','A仍以为窗口为0'],'纯ACK通常不可靠重传，单靠这次更新可能导致双方一直等待。',[1,2]),
 ('A持续计时器到期',['A发送零窗口探测','B返回当前窗口','探测间隔按规则退避'],'发送方通过专门探测触发接收方报告当前窗口，不是直接把拥塞窗口翻倍。',[0,1]),
 ('窗口更新到达',['A获知rwnd>0','按min(cwnd,rwnd)限制','扣去在途量后继续发送'],'非零窗口报告到达后恢复发送；零窗口探测与超时重传、保活计时器的用途不同。',[0,2])])
story('TCP 可靠交付、RTO 与快速重传','three-dup-acks','快速重传：第3个重复ACK究竟数到哪里',[
 ('已有一次正常ACK',['原累计ACK=1000','期待下一个字节1000','重复ACK计数=0'],'设MSS=1000B，接收方已经发过ACK1000。原ACK不计入后面的3个重复ACK。',[]),
 ('1000段丢失，2000段到达',['段[1000,2000)丢失','收到[2000,3000)','重复ACK1000：第1个'],'假设接收端对每个乱序段立即回复同一累计ACK，无其他复杂选项或窗口变化干扰。',[1,2]),
 ('3000段到达',['收到[3000,4000)','仍缺[1000,2000)','重复ACK1000：第2个'],'即使乱序数据已缓存，累计确认也不能跨过缺口。',[2]),
 ('4000段到达',['收到[4000,5000)','重复ACK1000：第3个','发送方快速重传缺失段'],'发送方收到3个符合定义的重复ACK后触发快速重传，无须等RTO到期。',[1,2]),
 ('重传填补缺口',['收到[1000,2000)','若乱序段已缓存','累计ACK推进至5000'],'图采用缓存乱序的接收方；拥塞窗口如何调整取决于Reno、NewReno等算法，快速重传与快恢复不能混成同一步规则。',[2])])
# Exact vectors: shared visual conventions, plus optional arbitrary wires for waveform/time-space scenes.
styles='<style>.bg{fill:var(--diagram-bg,#fff)}.vb{fill:var(--diagram-fill,#eff4f9);stroke:var(--diagram-line,#356493);stroke-width:2}.vt{fill:var(--diagram-text,#17212f);font-family:SimSun,"Times New Roman",serif}.ve{stroke:var(--diagram-line,#356493);stroke-width:2;fill:none}.active .vb{stroke:var(--hand-example,#7444ad);stroke-width:4}.done .vb{stroke:var(--hand-memory,#237352);stroke-width:3}.vl{paint-order:stroke;stroke:var(--diagram-bg,#fff);stroke-width:7;stroke-linejoin:round}.rb-red .vb{stroke:var(--hand-key,#ac2537)}.rb-red .vt{fill:var(--hand-key,#ac2537)}.rb-black .vb{stroke:var(--diagram-text,#17212f);stroke-width:3}</style>'
def draw(s,slug):
 out=[];ns={n['id']:n for n in s['nodes']}
 for wire in s.get('wires',[]):out.append('<path class="ve" stroke-width="4" d="'+' '.join(('M' if i==0 else 'L')+str(x)+','+str(y) for i,(x,y) in enumerate(wire['points']))+'"/>')
 for ed in s['edges']:
  a,b=ns[ed['a']],ns[ed['b']];ax,ay=a['x']+a['w']/2,a['y']+a['h']/2;bx,byy=b['x']+b['w']/2,b['y']+b['h']/2;dx,dy=bx-ax,byy-ay
  start=min((a['w']/2+4)/abs(dx) if dx else 1e6,(a['h']/2+4)/abs(dy) if dy else 1e6);end=min((b['w']/2+8)/abs(dx) if dx else 1e6,(b['h']/2+8)/abs(dy) if dy else 1e6)
  mark=f' marker-end="url(#{slug}-arrow)"' if ed.get('directed',True) else ''
  out.append(f'<path class="ve"{mark} d="M{ax+dx*start},{ay+dy*start} L{bx-dx*end},{byy-dy*end}"/>')
  if ed['label']:out.append(f'<text class="vt vl" font-size="18" x="{(ax+bx)/2}" y="{(ay+byy)/2-12}" text-anchor="middle">{html.escape(ed["label"])}</text>')
 for n in s['nodes']:
  out.append(f'<g class="{n["tone"]}"><rect class="vb" x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="10"/>');lines=n['label'].split('\n');units=max(sum(1 if ord(c)>255 else .58 for c in line) for line in lines);font=min(19,(n['w']-14)/max(1,units),(n['h']-12)/len(lines)/1.3)
  for i,line in enumerate(lines):out.append(f'<text class="vt" font-size="{font}" text-anchor="middle" x="{n["x"]+n["w"]/2}" y="{n["y"]+n["h"]/2+(i-(len(lines)-1)/2)*26+7}">{html.escape(line)}</text>')
  out.append('</g>')
 return ''.join(out)
for card,slug,sim,idx in examples:
 s=sim['steps'][idx];svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{html.escape(sim["title"])}</title><desc id="{slug}-desc">{html.escape(s["explain"])}</desc>{styles}<defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path fill="var(--diagram-line,#356493)" d="M0 0 L10 5 L0 10z"/></marker></defs><rect class="bg" width="900" height="500"/><text class="vt" font-size="24" text-anchor="middle" x="450" y="35">{html.escape(sim["title"])}</text><g transform="translate(0 55)">{draw(s,slug)}</g></svg>'
 (R/'images/408'/f'{slug}.svg').write_text(svg)
 secs=by[card]['sections'];secs[:]=[s for s in secs if s.get('diagram')!=slug];secs.append(dict(kind='example',heading='图解与逐步推演：'+sim['title'],diagram=slug,simulation=sim))
(R/'data/408-handbook.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Added',len(examples),'mechanism figures and animations; distribution:',{s:sum(by[c]['subject']==s for c,*_ in examples) for s in dict.fromkeys(x['subject'] for x in items)})
