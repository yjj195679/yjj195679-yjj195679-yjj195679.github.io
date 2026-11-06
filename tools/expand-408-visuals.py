"""Reproducible worked examples. Each scene supplies a vector figure and reversible frames."""
from pathlib import Path
import json, copy, html
R=Path(__file__).resolve().parents[1]
items=json.loads((R/'data/408-handbook.json').read_text())
by={x['title']:x for x in items}; examples=[]
def node(id,x,y,label,w=150,h=62,tone='base'):
 return dict(id=str(id),x=x,y=y,label=str(label),w=w,h=h,tone=tone)
def edge(a,b,label=''):return dict(a=str(a),b=str(b),label=label)
def frame(title,explain,nodes,edges=(),note=''):
 return dict(title=title,explain=explain,nodes=copy.deepcopy(nodes),edges=copy.deepcopy(edges),note=note)
def add(card,slug,title,steps,static=-1):
 assert card in by,card
 examples.append((card,slug,dict(scene='board',title=title,steps=steps,height=420),static))
def row(values,active=(),done=(),y=100,prefix='v'):
 w=min(260,790/max(1,len(values)));return [node(prefix+str(i),40+i*w,y,v,w-8,64,'active' if i in active else 'done' if i in done else 'base') for i,v in enumerate(values)]
def flow(labels,current=0,states=None):
 ns=[node(i,65+(i%3 if i//3==0 else 2-i%3)*285,65+(i//3)*150,s,230,82,'active' if i==current else 'done' if i<current else 'base') for i,s in enumerate(labels)]
 return ns,[edge(i,i+1) for i in range(len(ns)-1)]
def flows(card,slug,title,labels,explanations):
 steps=[]
 for i,(lab,exp) in enumerate(zip(labels,explanations)):
  ns,es=flow(labels,i);steps.append(frame(lab.replace('\n',' · '),exp,ns,es))
 add(card,slug,title,steps)
def sequence(card,slug,title,actors,messages,explanations):
 # Message labels stay on their own row; each new row reveals another exchange.
 steps=[]
 for k in range(len(messages)+1):
  ns=[node('a'+str(i),70+i*int(700/max(1,len(actors)-1)),25,a,130,52,'active') for i,a in enumerate(actors)]
  es=[]
  for i,(a,b,msg) in enumerate(messages[:k]):
   y=110+i*58;ns.extend([node('l'+str(i),135+a*int(700/max(1,len(actors)-1)),y,'',2,2),node('r'+str(i),135+b*int(700/max(1,len(actors)-1)),y,'',2,2)])
   es.append(edge('l'+str(i),'r'+str(i),msg))
  steps.append(frame('起点' if not k else messages[k-1][2], '先确认参与者，再沿时间向下阅读。' if not k else explanations[k-1],ns,es))
 add(card,slug,title,steps)
# DATA STRUCTURES: computed movement, trees, graphs, searches, sorting.
ns=[node('p',60,100,'p：结点 A'),node('q',620,100,'原后继 B'),node('s',340,270,'新结点 S')]
add('单链表的查找、插删与资源释放','linked-insert','单链表插入：先接后继，再改前驱',[
 frame('原链 A → B','已找到前驱p，先分配新结点s。这里只演示定位之后的链接修改。',ns,[edge('p','q')]),
 frame('s.next = p.next','先保存原后继，使s指向B；p仍指向B。',ns,[edge('p','q'),edge('s','q')]),
 frame('p.next = s','再让A指向S，形成A→S→B。若先覆盖p.next再用它找B，就会丢失原后继。',[ns[0],node('s',340,100,'新结点 S',tone='active'),ns[1]],[edge('p','s'),edge('s','q')])])
steps=[];arr=[2,4,6,8]
for title,exp,vals,act in [('原表','在下标1插入3；先保证容量足够，当前长度4。',[2,4,6,8,'空'],[]),('移动8','从后向前搬移，避免覆盖尚未搬走的数据。',[2,4,6,'空',8],[3,4]),('移动6','把下标2的6搬到下标3。',[2,4,'空',6,8],[2,3]),('移动4','把4搬到下标2，下标1空出。',[2,'空',4,6,8],[1,2]),('填入3','写入3，长度增加为5；共搬移3个已有元素。',[2,3,4,6,8],[1])]:steps.append(frame(title,exp,row(vals,act),note='下标从0起；插入点之后的元素从后向前移动。'))
add('顺序表的寻址、插入与删除','array-insert','顺序表插入：为什么从后往前搬',steps)
steps=[]
for title,stack,exp in [('读入 (',['('],'左括号入栈，等待匹配。'),('读入 [',['(','['],'左括号继续入栈。'),('读入 ]',['('],'与栈顶[匹配，弹出[。'),('读入 )',[],'与栈顶(匹配，弹出(；输入结束且栈空，匹配成功。')]:
 ns=[node('b',320,330,'栈底',200,40)]+[node('s'+str(i),320,260-i*70,x,200,60,'active' if i==len(stack)-1 else 'base') for i,x in enumerate(stack)]
 steps.append(frame(title,exp,ns,note='输入：([])；只允许在栈顶入栈、出栈。'))
add('括号匹配、表达式求值与递归','stack-brackets','括号匹配与栈顶的变化',steps)
ns=[node('A',370,40,'A',100),node('B',170,165,'B',100),node('C',570,165,'C',100),node('D',70,290,'D',100),node('E',270,290,'E',100)];es=[edge('A','B'),edge('A','C'),edge('B','D'),edge('B','E')]
steps=[]
for i,v in enumerate(['D','B','E','A','C']):
 n=copy.deepcopy(ns)
 for q in n:q['tone']='active' if q['id']==v else 'done' if q['id'] in ['D','B','E','A','C'][:i] else 'base'
 steps.append(frame('访问 '+v,'中序规则：左子树→根→右子树。这里的“访问”是输出结点，沿边经过不等于输出。',n,es,note='已输出：'+' → '.join(['D','B','E','A','C'][:i+1])))
add('二叉树的顺序存储、链式存储与遍历','tree-inorder','一棵树逐步走完中序遍历',steps)
vals=[3,7,11,15,19,23,27];steps=[];lo=0;hi=6
while lo<=hi:
 mid=(lo+hi)//2;ns=row(vals,[mid],range(lo,hi+1));steps.append(frame(f'low={lo}，high={hi}，mid={mid}',f'查找23：比较a[{mid}]={vals[mid]}。'+('命中，结束。' if vals[mid]==23 else '23较大，low移到mid+1；已排除位置不会重新进入。'),ns,note='闭区间 [low, high]；数组有序，下标从0起。'))
 if vals[mid]==23:break
 lo=mid+1
add('折半查找的边界与判定树','binary-search','折半查找：区间怎样一半一半缩小',steps)
steps=[];a=[5,2,4,1]
steps.append(frame('初始数组','采用稳定的直接插入排序：每次把一个元素插入左侧有序前缀。',row(a),note='有序前缀初始只有5。'))
for i in range(1,len(a)):
 key=a[i];j=i-1
 while j>=0 and a[j]>key:a[j+1]=a[j];j-=1
 a[j+1]=key;steps.append(frame(f'插入 {key}',f'只把严格大于{key}的元素右移；相等元素不越过，所以稳定。',row(a,[j+1],range(i+1)),note='左侧有序前缀长度：'+str(i+1)))
add('直接插入排序的移动与稳定性','insertion-sort','直接插入排序：有序区逐轮扩大',steps)
steps=[];a=[4,2,6,1,5,3];pivot=a[-1];i=0
steps.append(frame('选择枢轴3','采用Lomuto划分示例，枢轴固定为末尾元素3；不同教材划分实现的中间数组可能不同。',row(a,[5])))
for j in range(5):
 if a[j]<pivot:a[i],a[j]=a[j],a[i];i+=1
 steps.append(frame('扫描下标'+str(j),f'检查{a[j] if j>=i else a[i-1]}，维护左侧[0,{i})中的元素均小于3；本步只完成划分扫描，不代表全部有序。',row(a,[j,5],range(i))))
a[i],a[-1]=a[-1],a[i];steps.append(frame('枢轴归位','3落在最终位置2；左侧均小于3，右侧均大于3；两侧仍需递归排序。',row(a,[i]),note='一次划分结果：2，1，3，4，5，6'))
add('快速排序的划分与递归边界','quick-partition','快速排序：完整的一次划分',steps)
steps=[];a=[9,7,8,2,4,3];coords=[(380,30),(180,150),(580,150),(80,285),(280,285),(540,285)]
for title,vals,exp in [('最大堆',a[:],'数组表示完全二叉树，父结点关键字不小于孩子；孩子下标为2i+1、2i+2。'),('根与末尾交换',[3,7,8,2,4,9],'把9移到末尾有序区；有效堆规模从6减为5。'),('向下筛选',[8,7,3,2,4,9],'3与较大的孩子8交换，得到规模5的最大堆；9不再参与调整。')]:
 ns=[node(i,*coords[i],v,90,60,'done' if i==5 and title!='最大堆' else 'active' if i==0 else 'base') for i,v in enumerate(vals)];steps.append(frame(title,exp,ns,[edge(0,1),edge(0,2),edge(1,3),edge(1,4)]+([edge(2,5)] if title=='最大堆' else []),note='数组：'+str(vals)))
add('堆排序与堆的插入删除','heap-extract','最大堆取出堆顶与向下筛选',steps)
ns=[node('A',70,55,'A',90),node('B',350,55,'B',90),node('C',70,255,'C',90),node('D',350,255,'D',90)];es=[edge('A','B'),edge('A','C'),edge('B','D'),edge('C','D')];steps=[]
for i,(v,indeg,queue) in enumerate([('A','A:0 B:1 C:1 D:2','A'),('B','A:已删 B:0 C:0 D:2','B,C'),('C','B:已删 C:0 D:1','C'),('D','C:已删 D:0','D')]):
 n=copy.deepcopy(ns)
 for q in n:q['tone']='active' if q['id']==v else 'done' if q['id'] in 'ABCD'[:i] else 'base'
 n.append(node('state',520,75,'剩余入度\n'+indeg.replace(' ','\n'),310,220));steps.append(frame('输出 '+v,'选择零入度顶点并输出，删除它的出边，再把新出现的零入度顶点加入队列。',n,es,note='本步开始时零入度队列：'+queue+'；若有多个零入度点，顺序可不唯一。'))
add('DAG、AOV 网与拓扑排序','topological','拓扑排序：删除边怎样让入度变为0',steps)
steps=[];forest=[2,3,7,8];mergecost=0
steps.append(frame('四个叶子','初始权值2、3、7、8，每次取出当前最小的两个树根。',row(forest)))
for t in range(3):
 forest.sort();x,y=forest.pop(0),forest.pop(0);forest.append(x+y);forest.sort();mergecost+=x+y
 steps.append(frame(f'合并 {x}+{y}={x+y}','每个叶子的权值在每上升一层时贡献一次；所有合并权值之和等于最终WPL。',row(forest,[forest.index(x+y)]),note='累计合并代价 / 最终WPL：'+str(mergecost)))
add('哈夫曼树的构造与带权路径长度','huffman-merge','哈夫曼构造：最小两棵树反复合并',steps)
# COMPUTER ORGANIZATION: bit-accurate states and resource timelines.
steps=[];a=7;b=3;carry=0;bits=[]
for i in range(4):
 ai=(a>>i)&1;bi=(b>>i)&1;ci=carry;s=ai^bi^ci;carry=int(ai+bi+ci>=2);bits.append(s)
 ns=[node('a',70,60,f'A{i}={ai}'),node('b',70,170,f'B{i}={bi}'),node('c',70,280,f'C{i}={ci}'),node('fa',360,160,'全加器',160,82,'active'),node('sum',650,85,f'S{i}={s}'),node('carry',650,240,f'C{i+1}={carry}')]
 steps.append(frame(f'第{i}位相加',f'{ai}+{bi}+{ci}={ai+bi+ci}，本位和{s}，向高位进位{carry}。',ns,[edge('a','fa'),edge('b','fa'),edge('c','fa'),edge('fa','sum'),edge('fa','carry')],note='4位：0111 + 0011 = 1010；无符号10，有符号+7+3溢出。'))
add('加法器、进位链与 ALU','ripple-add-steps','逐位看进位：0111 + 0011',steps)
steps=[];A=0;Q=0b0011;M=0b0101
steps.append(frame('初始化','无符号4位乘法，M=0101(5)，Q=0011(3)，A=0000；使用5位部分积保留加法进位。',row(['M=0101','A=0000','Q=0011']),note='目标：5×3=15；进行4轮条件加法与整体右移。'))
for k in range(4):
 bit=Q&1
 if bit:A+=M
 steps.append(frame(f'轮{k+1}：检查Q₀={bit}', 'Q₀为1，加M到部分积A。' if bit else 'Q₀为0，本轮不加M。',row([f'M={M:04b}',f'A={A:05b}',f'Q={Q:04b}'],[1] if bit else [2])))
 combined=((A<<4)|Q)>>1;A=combined>>4;Q=combined&15
 steps.append(frame(f'轮{k+1}：整体右移','把进位、部分积和乘数寄存器连接后逻辑右移；左端补0。',row([f'M={M:04b}',f'A={A:04b}',f'Q={Q:04b}'],[1,2]),note=f'目前 A|Q = {A:04b}{Q:04b}'))
add('加法器、进位链与 ALU','unsigned-multiply','寄存器逐轮演示：5×3的无符号乘法',steps)
# Move multiplication scene to the existing multiplication subsection's card, if one exists under another title.
steps=[];rem=0;quo=0
for k,bit in enumerate('1101'):
 rem=rem*2+int(bit);before=rem;q=int(rem>=3)
 if q:rem-=3
 quo=quo*2+q
 steps.append(frame(f'处理第{k+1}位：{bit}',f'余数左移并移入该位：{before}。'+('够减3，减后置商位1。' if q else '不够减3，置商位0。'),row([f'部分商={quo:0{k+1}b}',f'余数={rem}',f'除数=3'],[0,1]),note='无符号长除法：1101₂ ÷ 0011₂；最终商0100₂，余数1。'))
add('加法器、进位链与 ALU','unsigned-division','长除法逐位试减：13÷3=4余1',steps)
steps=[]
for title,vals,exp in [('原数与阶码',['1.5 = 1.100₂ × 2⁰','0.25 = 1.000₂ × 2⁻²'],'用可精确表示的二进制数说明流程；尚未考虑IEEE字段编码。'),('小阶向大阶对齐',['1.100₂ × 2⁰','0.010₂ × 2⁰'],'第二个尾数右移2位，阶码加2；不能把大阶向小阶硬移。'),('尾数相加',['1.100₂','+ 0.010₂','= 1.110₂'],'相同阶码下尾数相加，得1.110₂。'),('规格化与舍入',['1.110₂ × 2⁰','= 1.75','精确，无舍入损失'],'结果已规格化；一般还需按保留位、保护位和舍入规则处理并检查阶码范围。')]:steps.append(frame(title,exp,row(vals),note='示例保留足够有效位；不要把移出的有效位一律丢弃。'))
add('尾数规格化与浮点加减的五个步骤','floating-add','浮点加法：1.5 + 0.25如何对阶',steps)
steps=[]
for title,labels,exp in [('大端',['地址1000\n12','地址1001\n34','地址1002\n56','地址1003\n78'],'32位数0x12345678，大端把最高有效字节0x12放在最低地址。'),('小端',['地址1000\n78','地址1001\n56','地址1002\n34','地址1003\n12'],'小端把最低有效字节0x78放在最低地址。字节内部bit顺序没有因此颠倒。')]:steps.append(frame(title,exp,row(labels),note='地址按字节递增；每格一个字节，图中文字为十六进制。'))
add('边界对齐与大小端存储','endian-bytes','同一个32位数的大端与小端布局',steps)
steps=[]
for t in range(1,8):
 ns=[]
 for i in range(3):
  for s in range(5):
   ns.append(node(f'{i}-{s}',140+s*135,45+i*95,['IF取指','ID译码','EX执行','MEM访存','WB写回'][s],125,65,'active' if t==i+s+1 else 'done' if t>i+s+1 else 'base'))
  ns.append(node('label'+str(i),20,45+i*95,'I'+str(i+1),100,65))
 steps.append(frame(f'第{t}个时钟周期','理想五段、每段1周期、无冒险：第i条指令第s段在i+s−1周期进行；同一时刻不同指令占用不同段。',ns,note='3条指令总时间：5+3−1=7个周期；首条延迟仍为5周期。'))
add('流水线的分段、锁存器与吞吐','pipeline-cycles','五段流水线：三条指令怎样重叠执行',steps)
flows('结构、数据和控制冒险','pipeline-load-use','load-use冒险：有转发也可能需要停顿',['I1：lw r1,0(r2)\nEX算地址','I1：MEM读数据\nI2：停顿一拍','I2：EX使用r1\n通过转发得到数据'],['假设经典五段流水线、完整转发，I2为add r3,r1,r4，紧接I1；I1在EX阶段还没有读到内存值。','I1在MEM结束才产生加载数据；I2原本同周期EX需要它，来不及，所以冻结相关前段并向EX插入气泡。','下一周期把MEM/WB中的值转发到I2的EX输入；具体停顿数取决于题设流水线和存储时序。'])
flows('DMA：控制器、传送方式和完整过程','dma-lifecycle','DMA整段传送：CPU何时参与',['CPU设置DMA\n地址、方向、长度','DMA取得总线\n设备↔主存','DMA更新计数\nCPU可执行其他工作','块传送完成\n中断通知CPU'],['CPU或驱动初始化DMA控制器。','控制器按请求方式取得总线/内存访问权，数据不必逐字经CPU寄存器中转。','每次传送更新地址与计数；CPU与DMA可能竞争内存，不能理解成永不互相影响。','控制器报告完成或错误；CPU在中断处理程序中收尾；DMA仍需要CPU初始化和结束处理。'])
flows('写策略：写命中与写失效分开选择','cache-write-back','写回Cache：脏块为什么要先写回',['写命中\n更新Cache置脏位','另一主存块映射到本行\n发生替换','检查旧行dirty=1\n写回旧主存块','读入新块\n更新标记清脏位'],['本例采用写回策略，写命中先只更新Cache，置dirty=1。','以直接映射为例，冲突失效要求替换旧块。','必须按旧标记定位旧主存块后写回，不能用新块地址写回旧数据。','本例新请求是读失效；新块装入后初始dirty=0。写失效是否装入另由写分配策略决定。'])
flows('立即、直接、间接与寄存器寻址','addressing-indirect','间接寻址：地址字段不是最终操作数',['指令地址字段A=100\n读M[100]','M[100]=500\n得到有效地址EA','M[500]=42\n取得操作数42'],['采用一次存储器间接寻址，指令给出指针所在地址100。','第一次数据访存取出指针500，有效地址是500。','第二次数据访存得到操作数42；这里不计取指本身和Cache影响。'])
# OPERATING SYSTEMS
flows('进程状态与状态转换','process-three-states','运行、就绪、阻塞：转换由什么事件触发',['就绪\n等CPU','运行\n获得CPU','阻塞\n等待I/O','就绪\nI/O完成','运行\n再次被调度'],['进程具备执行条件，只缺处理机。','调度程序分派CPU，恢复上下文。','发起需等待的I/O，主动阻塞，让出CPU。','I/O完成使进程具备运行条件，通常先进入就绪队列。','被再次选中才运行；运行进程时间片耗尽通常转就绪，阻塞进程不能直接因时间片耗尽而运行。'])
flows('中断、异常与处理流程','interrupt-return','中断返回：处理结束不必切换进程',['P在用户态运行','中断响应\n保存断点与必要现场','内核处理中断\n更新设备/唤醒任务','返回路径检查\n是否需要调度','恢复P继续执行\n本例不满足切换条件'],['本例P正在执行普通指令。','硬件按体系结构约定进入内核入口，保存返回所需状态；软件可能继续保存通用寄存器。','处理中断与进程调度是不同动作，唤醒任务也不等于必然立即抢占。','若调度策略和可抢占条件要求切换，可在适当返回点运行调度器。','本例继续P，说明中断不必导致进程切换；发生特权级转换也不等于发生进程切换。'])
steps=[];jobs=[('P1',5),('P2',3),('P3',1)];queue=jobs[:];time=0;slices=[]
steps.append(frame('全部在t=0到达','单CPU、时间片q=2、忽略切换开销，初始就绪队列P1、P2、P3。',row(['P1:5','P2:3','P3:1']),note='剩余CPU时间分别为5、3、1。'))
while queue:
 p,r=queue.pop(0);run=min(2,r);start=time;time+=run;r-=run;slices.append((p,start,time))
 if r:queue.append((p,r))
 ns=[node(str(i),35+st*86,85,f'{p}\n{st}→{en}',(en-st)*86-5,95,'active' if i==len(slices)-1 else 'done') for i,(p,st,en) in enumerate(slices)]
 steps.append(frame(f'{p}执行 [{start},{time})',f'{p}本次用{run}个时间单位，'+(f'剩余{r}，排回队尾。' if r else '完成并退出队列。'),ns,note='就绪队列（左端先运行）：'+', '.join(p+':'+str(r) for p,r in queue)))
add('优先级、时间片轮转与多级反馈队列','round-robin','时间片轮转：完整队列与甘特图',steps)
# Scalar resource banker demonstration.
steps=[];work=1;remain=[('P0',2,1),('P1',1,2),('P2',1,1)]
steps.append(frame('检查前','系统仅1类资源共5个：已分配2、1、1，可用1；最大需求分别3、3、2，因此Need=1、2、1。',row(['Work=1','P0 need=1\nalloc=2','P1 need=2\nalloc=1','P2 need=1\nalloc=1']),note='安全性算法只模拟归还，不真的给进程提前分配资源。'))
for p,a,n in [('P0',2,1),('P1',1,2),('P2',1,1)]:
 before=work;work+=a;steps.append(frame('模拟完成 '+p,f'{p}的Need={n}≤Work={before}，可假设它完成并归还已分配的{a}，Work增为{work}。',row([f'Work={work}',p+' 已完成'],[1]),note='找到安全序列P0→P1→P2；不安全不等于已经死锁。'))
add('安全状态与银行家算法','banker-safety','银行家安全性检查：Work怎样增加',steps)
flows('请求分页的表项、缺页处理与指令重启','page-fault','缺页处理：从异常到重新执行',['访问页P\n驻留位=0','陷入内核\n验证地址和权限','选页框\n必要时换出脏页','调入页面P\n进程等待I/O','更新页表/TLB\n进程转就绪','恢复执行\n重启原访存指令'],['合法虚拟页尚未驻留，触发缺页异常。','先区分合法但不驻留与非法地址/保护错误；后者不能按正常调页继续。','有空闲页框就直接用；无空闲页框才选择牺牲页，脏页必要时写回。','访问磁盘的调页可阻塞当前进程；其他进程可以被调度。','I/O完成后更新映射和状态，并按需要使相关TLB项失效。','获得CPU后重启导致缺页的指令；缺页服务时间与普通内存时间相差很大。'])
steps=[];pages=[1,2,3];bits=[1,0,1]
for k in range(3):
 idx=0 if k==0 else 1;ns=row([f'页{p}\nR={bits[i]}' for i,p in enumerate(pages)],[idx])
 if k==0:exp='指针指页1，R=1，给第二次机会：清R并前进。';bits[0]=0
 elif k==1:exp='指针指页2，R=0，选它淘汰；不是继续跳到页3。'
 else:pages[1]=4;bits[1]=1;ns=row([f'页{p}\nR={bits[i]}' for i,p in enumerate(pages)],[2]);exp='页4装入原页2的页框，完成本次访问置R=1；指针移到下一个页框。'
 steps.append(frame(['检查页1','选中页2','装入页4'][k],exp,ns,note='基本Clock，仅使用访问位R；初始指针指第一个页框。'))
add('Clock与改进型Clock','clock-replace','Clock扫描：清访问位与选择牺牲页',steps)
flows('索引分配、多级索引与混合索引','inode-indirect','间接索引：逻辑块号怎样变成磁盘块',['逻辑块号L=20\n先扣12个直接块','剩余索引=8\n进入一级间接块','索引块第8项\n给出数据块号900','读取数据块900\n再按块内偏移取字节'],['示例inode有12个直接指针，一个一级间接指针；4KiB块、4B块号，每个间接块存1024项。','L=20超出直接范围0～11；20−12=8（下标从0起）。','先读一级间接索引块，查第8项取得数据块号900。','若inode已在内存而间接块和数据块都不缓存，本次需要2次磁盘块读取；题目缓存条件会改变计数。'])
flows('硬链接、符号链接与共享计数','hard-soft-link','硬链接和软链接：名字指向哪里',['目录名a\n指向inode 42','再建硬链接b\n同指inode 42','另建软链接s\n独立inode存路径a','删除名字a\nb仍可访问文件','软链接s仍指路径a\n路径消失则悬空'],['目录项把文件名与inode对应，文件内容由inode关联数据块。','硬链接数增加；a、b是同一文件的两个名字，地位平等。','符号链接保存目标路径字符串，拥有自己的inode；不是把目标数据复制一份。','删除一个名字会减少链接数；只要还有b，目标文件仍有目录链接。','软链接按路径解析，删除a后s可能失效；b不因a删除而失效。最终释放还需考虑打开引用等条件。'])
steps=[];req=[82,170,43,140,24,16,190];head=50;path=[head];remaining=req[:];total=0
while remaining:
 nxt=min(remaining,key=lambda v:(abs(v-head),v));d=abs(nxt-head);total+=d;path.append(nxt);remaining.remove(nxt)
 ns=[node(str(v),35+v*4,160,str(v),44,55,'active' if v==nxt else 'done' if v in path[:-1] else 'base') for v in [16,24,43,50,82,140,170,190]]
 steps.append(frame(f'{head} → {nxt}',f'从当前磁头{head}选择最近请求{nxt}，移动{d}个柱面；累计{total}。',ns,note='实际服务路径：'+' → '.join(map(str,path))));head=nxt
add('磁盘调度：FCFS、SSTF、SCAN与LOOK','disk-sstf','SSTF磁盘调度：每次重新找最近请求',steps)
flows('双缓冲、循环缓冲与缓冲池','double-buffer','双缓冲：输入与处理怎样交叠',['设备→缓冲A\nCPU等待第一块','设备→缓冲B\nCPU处理缓冲A','设备→缓冲A\nCPU处理缓冲B','交替复用\n缓冲释放后再写'],['初始两个缓冲为空，设备先填A。','A填好后交给CPU处理，设备可同时填B。','A处理完成释放后，设备才可再次写A；CPU转而处理B。','理想稳态每块节拍取max(输入时间,处理时间)，首块/末块另计；若处理慢，设备仍可能等待。'])
# NETWORKS
sequence('TCP 三次握手、序号与状态','tcp-handshake','三次握手：seq、ack与状态逐条对照',['客户端','服务端'],[(0,1,'SYN seq=100'),(1,0,'SYN+ACK seq=500 ack=101'),(0,1,'ACK seq=101 ack=501')],['客户端发送SYN后为SYN-SENT；服务端收到后确认101，发送自己的SYN，进入SYN-RECEIVED。','SYN各占一个序号。客户端收到合法SYN+ACK后发送第三次ACK并进入ESTABLISHED。','服务端收到第三次ACK后进入ESTABLISHED；纯ACK不消耗序号。示例无数据、无丢包。'])
sequence('TCP 连接释放、半关闭与 TIME-WAIT','tcp-four-close','四次挥手：半关闭、序号和2MSL',['主动关闭A','被动关闭B'],[(0,1,'FIN seq=100 ack=500'),(1,0,'ACK seq=500 ack=101'),(1,0,'FIN seq=500 ack=101'),(0,1,'ACK seq=101 ack=501')],['双方已建立，假设A下个seq=100、B下个seq=500且无在途数据。A发送FIN进入FIN-WAIT-1，B接收后进入CLOSE-WAIT。','B确认A的FIN；A收到ACK后进入FIN-WAIT-2。B的发送方向仍可继续。','本例B没有再发数据；B发送FIN进入LAST-ACK，A收到后确认501并进入TIME-WAIT。','B收到最终ACK后CLOSED；A通常等待2MSL再关闭。ACK和FIN有时可合并；此处演示典型分离情形。'])
sequence('DNS 递归、迭代与缓存','dns-iteration','DNS：本地服务器代客户端逐级询问',['客户端','本地DNS','层次DNS'],[(0,1,'递归请求 example.com'),(1,2,'问根：获得 .com 服务器线索'),(1,2,'问 .com：获得权威服务器线索'),(1,2,'问权威：获得目标记录'),(1,0,'返回结果并按TTL缓存')],['假设客户端和本地服务器均无可用缓存，客户端向本地递归解析器请求最终答案。','右侧“层次DNS”合并表示根、顶级与权威服务器；向根的查询与响应在本步完成。','本地解析器继续发起新查询，顶级服务器通常返回权威服务器线索。','权威服务器返回相关记录；遇CNAME等情况还可能继续解析。','本地DNS返回结果；以后命中有效缓存时可以跳过部分或全部上游查询。图中一行代表一次问答或最终返回，不按箭头数量计算报文数。'])
sequence('DHCP：DORA、端口与初始地址','dhcp-dora','DHCP初次获取地址：DORA四步',['未配置客户端','DHCP服务器'],[(0,1,'Discover：寻找服务器'),(1,0,'Offer：提出可用地址'),(0,1,'Request：选择地址/服务器'),(1,0,'ACK：确认租约')],['典型初次申请：客户端0.0.0.0:68向255.255.255.255:67广播；图示同一网段无中继。','服务器提出地址和配置；回复可广播或按条件单播，不能一律认定只单播。','客户端典型广播Request，说明选择的服务器和请求地址，使其他服务器也获知选择。','服务器ACK确认配置和租期；客户端还应按协议处理地址冲突等情况；续租路径与初次申请不同。'])
flows('协议、接口、服务与分层封装','encapsulation','发送到接收：数据怎样逐层封装',['应用数据\nHTTP等','运输层加首部\nTCP段 / UDP数据报','网络层加首部\nIP数据报','链路层加首尾\n以太网帧','物理层传输比特\n跨路由逐跳转发','接收端逆向解封装\n交给对应应用'],['应用产生消息或字节。','端口标识运输层通信端点；TCP和UDP格式不同。','IP地址用于网络层寻址；分片等行为由协议和链路条件决定。','以太网头中使用当前链路下一跳的MAC地址，帧尾含检错信息。','路由器一般解开旧链路封装，处理IP转发，再重新封装下一跳帧；并非每跳都交给应用层。','终点逐层检查和去除封装；首部和尾部属于哪一层应分清。'])
steps=[]
for title,vals,exp in [('空转发表',['A在端口1','B在端口2','C在端口3'],'初始交换表为空。'),('A→B到达',['学习 A→1','B未知','泛洪到2、3'],'先按源MAC学习A的位置，再查目的B；未知单播向同VLAN除入端口外的端口泛洪。'),('B→A回应',['学习 B→2','查得 A→1','只向端口1转发'],'回应到达时学习B，再查A；已知单播按表定向转发。'),('再发A→B',['刷新 A→1','查得 B→2','只向端口2转发'],'表项可能老化，本例尚未老化；广播、组播、环路等机制另论。')]:steps.append(frame(title,exp,row(vals),note='同一VLAN；学习源地址，查找目的地址。'))
add('交换机自学习、转发与冲突域','switch-learning','交换机自学习：从泛洪到定向转发',steps)
steps=[]
for mask,name,match in [('/0','默认路由',True),('/16','10.1.0.0/16',True),('/24','10.1.2.0/24',True),('/25','10.1.2.128/25',True)]:
 ns=row(['10.1.2.130','当前匹配\n'+name,'前缀长度\n'+mask],[1,2]);steps.append(frame('检查 '+name,'目的地址10.1.2.130落在该范围，记录它并继续比较更长前缀。' if mask!='/25' else '四项都匹配，选择最长的/25；不是按路由表从上到下遇到第一项就结束。',ns,note='10.1.2.128/25范围：10.1.2.128～10.1.2.255'))
add('CIDR 地址块、聚合与最长前缀匹配','longest-prefix','最长前缀匹配：同一地址命中多条怎么办',steps)
sequence('SR：逐帧确认、缓存乱序与窗口滑动','sr-retransmit','选择重传SR：乱序缓存后一次交付',['发送方','接收方'],[(0,1,'帧0到达，单独确认0'),(0,1,'帧1丢失 ×'),(0,1,'帧2到达，缓存并确认2'),(0,1,'帧1超时，单独重传1'),(1,0,'交付1、2，窗口左边界推进')],['使用3bit编号、窗口4，满足窗口不超过序号空间一半；帧0按序交付。','帧1途中丢失，接收方还在等它。','SR可缓存窗口内乱序帧2并单独确认，区别于GBN通常丢弃乱序帧。','发送方只重传计时到期的帧1；已确认的帧2不用跟着重发。','帧1到达填补缺口，接收方向上层按序交付1和已缓存的2；图中单独ACK按帧编号约定，勿与TCP的期望字节ack混用。'])
steps=[];cwnds=[1,2,4,8,9,10]
for r,c in enumerate(cwnds,1):
 ns=[node(i,60+i*130,320-cw*23,f'{cw}',90,cw*23,'active' if i==r-1 else 'done') for i,cw in enumerate(cwnds[:r])]
 steps.append(frame(f'第{r}轮开始 cwnd={c} MSS','理想轮次模型：ssthresh=8 MSS；慢开始按轮次翻倍，达到门限后按拥塞避免每轮约增加1 MSS。',ns,note='轮初窗口序列：1，2，4，8，9，10；假设rwnd充足、每段确认、无丢包。'))
add('慢开始、拥塞避免与门限','tcp-cwnd','拥塞窗口：到门限后为什么不再翻倍',steps)
sequence('HTTP 持久连接与 RTT 计算','http-rtt','HTTP非持久连接：一个对象的2RTT',['客户端','服务器'],[(0,1,'0→RTT：建立TCP连接'),(0,1,'RTT→2RTT：HTTP请求与首字节'),(1,0,'2RTT之后：传输对象数据')],['以普通TCP建立连接为例，忽略DNS、TLS和握手处理开销；客户端约1RTT后可发请求，第三次ACK可携带请求。','请求到服务器，响应首字节返回，约再用1RTT；服务器处理时间忽略。','对象传输时间另加。复用已建连接时通常无需再算TCP握手RTT；并行、流水线和TLS会改变总时间模型。'])
# Emit exact vector assets and attach to the corresponding original card.
style='''<style>.bg{fill:var(--diagram-bg,#fff)}.vb{fill:var(--diagram-fill,#eff4f9);stroke:var(--diagram-line,#356493);stroke-width:2}.vt{fill:var(--diagram-text,#17212f);font-family:SimSun,"Times New Roman",serif;font-size:19px}.ve{stroke:var(--diagram-line,#356493);stroke-width:2;fill:none}.active .vb{stroke:var(--hand-example,#7444ad);stroke-width:4;fill:var(--diagram-fill,#f3eafb)}.done .vb{stroke:var(--hand-memory,#237352)}.vl{paint-order:stroke;stroke:var(--diagram-bg,#fff);stroke-width:7;stroke-linejoin:round}</style>'''
def svg_content(sim,idx,slug):
 s=sim['steps'][idx];nodes={n['id']:n for n in s['nodes']};chunks=[]
 for ed in s['edges']:
  a=nodes[ed['a']];b=nodes[ed['b']];ax=a['x']+a['w']/2;ay=a['y']+a['h']/2;bx=b['x']+b['w']/2;byy=b['y']+b['h']/2
  dx=bx-ax;dy=byy-ay;scale=min((a['w']/2+4)/abs(dx) if dx else 1e6,(a['h']/2+4)/abs(dy) if dy else 1e6);end=min((b['w']/2+8)/abs(dx) if dx else 1e6,(b['h']/2+8)/abs(dy) if dy else 1e6)
  if a['w']<5:scale=0;end=0
  chunks.append(f'<path class="ve" marker-end="url(#{slug}-arrow)" d="M{ax+dx*scale:.1f},{ay+dy*scale:.1f} L{bx-dx*end:.1f},{byy-dy*end:.1f}"/>')
  if ed['label']:
   edgefont=min(18,(abs(dx)-18 if abs(dx)>100 else 180)/max(1,sum(1 if ord(c)>255 else .58 for c in ed['label'])))
   chunks.append(f'<text style="font-size:{edgefont:.1f}px" class="vt vl" x="{(ax+bx)/2}" y="{(ay+byy)/2-12}" text-anchor="middle">{html.escape(ed["label"])}</text>')
 for n in s['nodes']:
  if n['w']<5:continue
  chunks.append(f'<g class="{n["tone"]}"><rect class="vb" x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="10"/>')
  lines=n['label'].split('\n')
  units=max(sum(1 if ord(c)>255 else .58 for c in line) for line in lines)
  font=min(19,(n['w']-14)/max(1,units),(n['h']-12)/len(lines)/1.3)
  for k,line in enumerate(lines):chunks.append(f'<text class="vt" style="font-size:{font:.1f}px" x="{n["x"]+n["w"]/2}" y="{n["y"]+n["h"]/2+(k-(len(lines)-1)/2)*26+7}" text-anchor="middle">{html.escape(line)}</text>')
  chunks.append('</g>')
 return ''.join(chunks)
for card,slug,sim,static in examples:
 slug='visual-'+slug
 s=sim['steps'][static]
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{html.escape(sim["title"])}</title><desc id="{slug}-desc">{html.escape(s["explain"])}</desc>{style}<defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path fill="var(--diagram-line,#356493)" d="M0 0 L10 5 L0 10z"/></marker></defs><rect class="bg" width="900" height="500"/><text class="vt" x="450" y="35" text-anchor="middle" style="font-size:24px">{html.escape(sim["title"])}</text><g transform="translate(0 55)">{svg_content(sim,static,slug)}</g></svg>'
 (R/'images/408'/f'{slug}.svg').write_text(svg)
 sections=by[card]['sections'];sections[:]=[x for x in sections if x.get('diagram')!=slug]
 sections.append(dict(kind='example',heading='图解与逐步推演：'+sim['title'],diagram=slug,simulation=sim))
(R/'data/408-handbook.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Attached',len(examples),'new figures and animations.',{s:sum(by[c]['subject']==s for c,*_ in examples) for s in dict.fromkeys(x['subject'] for x in items)})
# Structural comparisons complement the temporal scenes above.
static_count=0
def picture(card,slug,title,ns,es,explanations):
 global static_count
 assert card in by,card
 slug='atlas-'+slug;sim=dict(title=title,steps=[frame(title,'；'.join(explanations),ns,es)])
 markup=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{html.escape(title)}</title><desc id="{slug}-desc">{html.escape("；".join(explanations))}</desc>{style}<defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path fill="var(--diagram-line,#356493)" d="M0 0 L10 5 L0 10z"/></marker></defs><rect class="bg" width="900" height="500"/><text class="vt" x="450" y="35" text-anchor="middle" style="font-size:24px">{html.escape(title)}</text><g transform="translate(0 55)">{svg_content(sim,0,slug)}</g></svg>'
 (R/'images/408'/f'{slug}.svg').write_text(markup)
 sections=by[card]['sections'];sections[:]=[s for s in sections if s.get('diagram')!=slug];sections.append(dict(kind='example',heading='结构对照图：'+title,diagram=slug,paragraphs=explanations));static_count+=1
picture('B 树的查找、插入与分裂','btree-split','3阶B树：溢出时中间关键字上升',[
 node('before',35,55,'临时溢出结点\n10 | 20 | 30',300,105,'active'),node('root',580,40,'20',150),node('left',440,235,'10',150),node('right',700,235,'30',150)],
 [edge('before','root'),edge('root','left'),edge('root','right')],['3阶B树的一个结点最多2个关键字。图中是向原叶结点[10,20]插入30后的临时溢出状态。','把中间关键字20上提，10和30分别留在左右结点；若原结点为根，新建根，高度增加1。非根分裂时上提可能继续导致父结点溢出。'])
picture('B+ 树与 B 树的区别','bplus-leaves','B+树：内部索引与叶子顺序链',[
 node('r',320,30,'内部索引\n20 | 40 | 60',250,85),node('l1',25,235,'叶子\n10 | 20',230,80),node('l2',330,235,'叶子\n30 | 40',230,80),node('l3',635,235,'叶子\n50 | 60',230,80)],
 [edge('r','l1'),edge('r','l2'),edge('r','l3'),edge('l1','l2'),edge('l2','l3')],['本图沿用正文资料的子树最大键约定：内部键20、40、60分别对应三棵子树，关键字数与孩子数相等。查找35先选最大键40对应的中间子树。','所有记录入口在叶子，内部索引键20、40、60也在叶子出现；叶子顺序链接方便扫描区间。内部命中索引键仍要下降到叶子；其他实现可能采用最小键分隔，作题须跟随题设。'])
ns=[node('A',30,70,'A',80),node('B',300,70,'B',80),node('C',30,280,'C',80),node('D',300,280,'D',80),node('rule',520,70,'Prim：从已选顶点集合\n挑最小跨割边\n\nKruskal：全局边排序\n选最轻且不成环的边',330,240)]
picture('最小生成树与 Prim 算法','mst-cut','同一张图：Prim与Kruskal看边的方式',ns,[edge('A','B','1'),edge('A','C','4'),edge('B','C','2'),edge('B','D','5'),edge('C','D','3')],['从A做Prim：先AB(1)，再BC(2)，再CD(3)，总权6。Kruskal按边权1、2、3、4、5排序，前三条已连接全部顶点。','这里所有边权不同，最小生成树唯一。两种算法都解决带权无向连通图的最小生成树问题；不是从起点到各点的最短路径。'])
picture('AOE 网与关键路径的四组时间','critical-path','AOE网：最长工期与零余量活动',[
 node('s',30,160,'源点\nve=vl=0',150,90),node('a',330,30,'A\nve=2,vl=2',200,85),node('b',330,280,'B\nve=3,vl=4',200,85),node('t',700,160,'汇点\nve=vl=6',170,90)],
 [edge('s','a','2'),edge('s','b','3'),edge('a','t','4'),edge('b','t','2')],['两条路径工期分别2+4=6、3+2=5，因此最短完成工期6，关键路径源→A→汇。','活动B→汇的最早开始e=ve(B)=3，最迟开始l=vl(汇)−2=4，余量1。事件ve/vl与活动e/l不能混用。'])
picture('并查集的初始化、查找和合并','union-compress','并查集：路径压缩只改父指针',[
 node('a',30,45,'A → B → C → R',360,80),node('b',500,45,'find(A) 返回根R',350,80,'active'),node('r',600,220,'R',120),node('n1',420,345,'A',100),node('n2',590,345,'B',100),node('n3',760,345,'C',100)],
 [edge('a','b'),edge('n1','r'),edge('n2','r'),edge('n3','r')],['假设原父指针链A→B→C→R，R为根。递归路径压缩的find(A)在返回时把沿途A、B、C直接指向R。','集合划分和代表根不因此改变；压缩后的图仍是一棵树。按秩合并中的秩在压缩后一般不等于当前精确高度。'])
picture('图的基本操作与邻接矩阵','graph-storage','同一无向图：矩阵与邻接表',[
 node('g',30,55,'边集合\nAB、AC、BC',210,120),node('m',300,40,'矩阵（顶点A,B,C）\n0  1  1\n1  0  1\n1  1  0',260,220),node('l',620,40,'邻接表\nA：B→C\nB：A→C\nC：A→B',240,220)],
 [],['无向简单图邻接矩阵对称，每条无向边在邻接表中对应两个邻接项。矩阵占Θ(V²)，邻接表占Θ(V+E)。','使用邻接矩阵遍历全部邻边每个顶点要扫描一整行，完整BFS/DFS通常Θ(V²)；邻接表通常Θ(V+E)。'])
picture('AVL 的四种旋转与高度界','avl-cases','AVL四类失衡：先认插入方向再旋转',[
 node('ll',40,40,'LL：左孩子的左侧\n对失衡根右旋',370,110),node('rr',490,40,'RR：右孩子的右侧\n对失衡根左旋',370,110),node('lr',40,240,'LR：左孩子的右侧\n先左旋左孩子，再右旋根',370,110),node('rl',490,240,'RL：右孩子的左侧\n先右旋右孩子，再左旋根',370,110)],[],['图以插入后沿路径找到的最低失衡祖先为根，LL/RR/LR/RL描述其重侧及下一段方向。','旋转保持中序序列不变。删除后的平衡因子和修复传播有额外情况，不能机械套用插入时“只修复一次”的结论。'])
# ORGANIZATION
picture('浮点表示与 IEEE 754 编码','ieee-single','IEEE754单精度：1位符号、8位阶码、23位尾数',[
 node('s',35,55,'S\n1bit',110,90),node('e',155,55,'E\n8bit',260,90),node('f',425,55,'F\n23bit',435,90),node('normal',35,245,'规格化：0<E<255\n(−1)^S × 1.F × 2^(E−127)',395,110),node('special',465,245,'E=0：零 / 非规格化数\nE=255：无穷 / NaN',395,110)],[],['1.5的S=0，E=127（01111111），F为100…0，十六进制编码0x3FC00000。','隐含的首位1只适用于规格化数；E=0时指数采用1−127，尾数为0.F。E=255且F=0表示无穷，F非0表示NaN。'])
picture('主存容量扩展与 CPU 连接','memory-expansion','8片1K×8芯片：组成4K×16存储器',[
 node('cpu',25,130,'CPU地址\nA11…A0\n数据D15…D0',180,120),node('decode',285,30,'A11,A10 → 2-4译码\n选择一个芯片组',340,90),node('bank',320,230,'每组2片1K×8并联\n一片接D7…D0\n一片接D15…D8',350,130),node('all',720,210,'4组×2片\n共8片',150,90)],
 [edge('cpu','decode'),edge('decode','bank'),edge('cpu','bank'),edge('bank','all')],['A9…A0接每片芯片内部地址，共1024个字位置；A11、A10参与片选，扩展成4组。','数据位并联使字宽从8bit扩为16bit；总容量4K×16bit=8KiB。此图按16bit字编址说明，若CPU按字节编址还要处理字节选择和地址接法。'])
picture('双端口 RAM、单体多字与多体交叉存储','interleaved','低位交叉编址：相邻字轮流落入4个存储体',[
 node('b0',25,70,'体0\n字地址0,4,8…',200,150),node('b1',240,70,'体1\n字地址1,5,9…',200,150),node('b2',455,70,'体2\n字地址2,6,10…',200,150),node('b3',670,70,'体3\n字地址3,7,11…',200,150),node('n',130,300,'体号=字地址 mod 4；体内地址=⌊字地址/4⌋',650,65)],[],['低2位选择存储体，连续字可按启动间隔τ轮流启动。若存储周期T≤4τ，理想连续访问可维持每τ一个字的启动节拍。','传送n个字的常见理想模型为T+(n−1)τ；同一体冲突、总线占用、未满足轮流启动条件都会改变结果。'])
picture('Cache 三种映射与地址划分','cache-three','直接映射、组相联、全相联：候选位置有多少',[
 node('mem',35,115,'主存块号j',180,90),node('d',350,20,'直接映射\n只能进第 j mod L 行',480,90),node('s',350,160,'S组、每组E行\n进第 j mod S 组中的任一行',480,100),node('f',350,310,'全相联\n可进Cache任意行',480,80)],
 [edge('mem','d'),edge('mem','s'),edge('mem','f')],['块内偏移由块大小决定；直接映射的行号位数为log₂L，组相联的组号位数为log₂S，全相联没有组/行索引位。','同一组内比较候选标记并按替换策略选行；全相联灵活但比较开销大。容量计算要说明是否含标记、有效位和脏位。'])
picture('TLB、页表与 Cache：三种“命中”不能混为一谈','tlb-cache','地址变换与数据缓存：查到映射还要取数据',[
 node('v',20,45,'虚拟地址\n页号+偏移',170,90),node('t',300,45,'TLB\n缓存页号→页框号',260,90),node('p',300,260,'内存页表\nTLB未命中时查表',260,90),node('c',680,45,'物理地址\n访问数据Cache',200,90),node('m',680,260,'数据Cache未命中\n访问主存块',200,90)],
 [edge('v','t'),edge('t','c'),edge('t','p'),edge('p','c'),edge('c','m')],['图采用物理地址访问Cache的简化模型；TLB命中只说明地址映射较快得到，不能推断数据Cache也命中。','TLB未命中但页表项驻留有效，可以查表后继续，不一定发生缺页。真实处理器可能并行访问或使用VIPT等设计，计时要看题设。'])
picture('函数调用、栈帧与返回地址','call-stack','32位x86栈帧：EBP固定参照，ESP随栈变化',[
 node('args',250,10,'较高地址：参数\n[EBP+8] 常见首个栈参数',430,75),node('ret',250,95,'[EBP+4] 返回地址',430,65),node('old',250,170,'EBP → [EBP] 旧EBP',430,65,'active'),node('loc',250,245,'局部变量 / 保存寄存器\nESP → 当前栈顶（较低地址）',430,100)],[],['示例为常见32位x86、向低地址增长、使用push ebp; mov ebp,esp建立帧的约定，不代表所有ABI都这样传参。','call保存其后下一条指令的返回地址；递归每次建立独立栈帧。使用帧指针省略优化时不应照搬图中的EBP布局。'])
# CRC exact polynomial example.
def mod2(bits,g):
 a=list(map(int,bits));b=list(map(int,g))
 for i in range(len(a)-len(b)+1):
  if a[i]:
   for j in range(len(b)):a[i+j]^=b[j]
 return ''.join(map(str,a[-(len(b)-1):]))
rem=mod2('1101000','1011');assert rem=='001'
picture('CRC：补零、模 2 除与接收检验','crc-remainder','CRC示例：数据1101，生成多项式1011',[
 node('data',30,50,'数据1101\n末尾补3个0：1101000',370,90),node('div',500,50,'用1011模2除\n异或运算，无借位进位',360,90),node('send',30,270,'余数001\n发送码字1101001',370,90),node('recv',500,270,'接收后再模2除\n无误码时余数000',360,90)],
 [edge('data','div'),edge('div','send'),edge('send','recv')],['生成多项式最高次数r=3，所以补3个0，余数也按3bit写为001。1101000 ÷1011的模2余数为001。','发送码字为原数据拼余数1101001；接收端用同一除数得到000可通过检验，但余数为0并不能保证绝对没有任何未检出的差错。'])
# OPERATING SYSTEMS
picture('线程的资源、调度与实现方式','thread-resources','同一进程的线程：共享什么，各自保存什么',[
 node('shared',175,20,'进程共享地址空间\n代码、全局数据、堆、打开文件等进程资源',550,100),node('t1',50,240,'线程T1独有\n寄存器 / PC / 线程栈\n线程控制信息',350,125),node('t2',500,240,'线程T2独有\n寄存器 / PC / 线程栈\n线程控制信息',350,125)],
 [edge('t1','shared'),edge('t2','shared')],['线程共享进程资源，但每个执行流需要自己的寄存器现场和栈。某线程的栈在共享地址空间中，其他线程技术上可能访问其地址，不能把“独有使用”误解为天然硬件隔离。','用户级线程是否由内核直接调度，取决于线程映射模型；多对一模型下一个阻塞系统调用可能阻塞整个进程。'])
picture('分段、段表与段页式','segment-page','分段与分页：逻辑单位、映射方式与保护',[
 node('s',25,40,'分段：段号s + 段内偏移d\n段表给出base和limit\nd<limit 才允许 base+d',400,150),node('p',475,40,'分页：页号p + 页内偏移w\n页表给出页框号f\n物理地址 f×页大小+w',400,150),node('sp',120,285,'段页式：段号 → 该段页表 → 页框号；页内偏移保持不变',660,80)],[],['分段按逻辑模块划分，段长可变；分页按固定大小划分。段内越界先判断，不能直接拿基址加偏移而跳过保护。','段页式把段内地址继续分为页号和偏移，每段通过自己的页表映射到物理页框。所需访存次数取决于TLB及各级表缓存等条件。'])
picture('动态分区的四种适应算法与回收','partition-fit','申请18KiB：首次、最佳、最坏适应选谁',[
 node('a',30,75,'空闲区1\n20KiB',240,95,'active'),node('b',330,75,'空闲区2\n50KiB',240,95),node('c',630,75,'空闲区3\n30KiB',240,95),node('f',30,285,'首次适应\n按地址先找到20',240,90),node('best',330,285,'最佳适应\n最小可容纳区20',240,90),node('worst',630,285,'最坏适应\n最大区50',240,90)],[],['假设按地址排列的空闲分区大小依次20、50、30KiB，申请18KiB：首次与最佳均选20，最坏选50。','邻近适应从上次结束位置继续循环搜索，缺少上次指针就不能唯一判定。回收时须检查地址上相邻的空闲分区并合并，不能仅按分区表排列相邻就合并。'])
picture('资源分配图、死锁检测与解除','resource-cycle','单实例资源：请求边与分配边构成环',[
 node('p1',65,45,'进程P1',180,80),node('r1',625,45,'资源R1\n单实例',180,80),node('p2',625,275,'进程P2',180,80),node('r2',65,275,'资源R2\n单实例',180,80)],
 [edge('p1','r1','请求'),edge('r1','p2','已分配'),edge('p2','r2','请求'),edge('r2','p1','已分配')],['P1持有R2等R1，P2持有R1等R2，单实例且不可抢占时形成相互等待环。请求边从进程指向资源，分配边反向。','当各资源类型都只有一个实例时，环是死锁的充分必要条件；有多个实例时，存在环只是必要条件，仍须检查是否有进程可以完成。'])
picture('I/O软件分层与设备独立性','io-layers','I/O软件分层：请求向下，完成通知向上',[
 node('u',220,10,'用户层I/O库 / 应用',450,55),node('d',220,90,'设备独立软件：命名、保护、缓冲等',450,60),node('driver',220,175,'设备驱动：把请求转成设备操作',450,60),node('irq',220,260,'中断处理：响应并报告完成',450,60),node('hw',220,345,'控制器与设备硬件',450,55)],
 [edge('u','d'),edge('d','driver'),edge('driver','irq'),edge('irq','hw')],['图按概念层次展示，不表示每个请求都必须同步进入“中断处理程序”再访问硬件。驱动启动设备，设备完成后产生中断，由处理程序进入完成路径。','设备独立层使上层不必掌握每种控制器的寄存器细节；具体缓冲、调度和错误处理可以跨层实现。'])
picture('SPOOLing：用磁盘队列虚拟独占设备','spooling','假脱机打印：多个进程排队共享一台打印机',[
 node('p1',30,40,'进程A：打印作业',230,75),node('p2',30,280,'进程B：打印作业',230,75),node('disk',345,145,'磁盘输出井\n保存作业与数据',230,100),node('daemon',650,40,'假脱机输出进程\n按队列取作业',220,95),node('printer',650,280,'物理打印机\n一次处理一个作业',220,95)],
 [edge('p1','disk'),edge('p2','disk'),edge('disk','daemon'),edge('daemon','printer')],['用户进程把作业写入磁盘队列后可继续运行；输出进程再串行驱动物理打印机，形成逻辑上的多用户共享。','SPOOLing依赖外存中的输入/输出井和管理程序；它不等于只在主存里增加一个普通缓冲区，也不是把一台物理设备变成真正同时工作的多台硬件。'])
picture('编译、链接、装入与重定位','compile-load','源程序到运行：各阶段负责什么',[
 node('src',25,30,'源文件',190,70),node('obj',350,30,'可重定位目标文件',250,70),node('exe',350,205,'可执行文件\n链接符号与地址',250,90),node('run',350,345,'运行地址空间\n装入与动态地址变换',250,70)],
 [edge('src','obj','编译/汇编'),edge('obj','exe','链接'),edge('exe','run','装入')],['编译/汇编生成目标代码；链接把目标模块和所需库组合并处理符号引用，静态与动态链接的发生时点不同。','装入把程序映像准备到内存或虚拟地址空间。运行时地址变换由MMU等机制完成，不是每执行一条指令都重新链接整个程序。'])
# NETWORKS
picture('四种时延、往返时间和链路容量','network-delay','发送与传播：最后一bit何时到达',[
 node('send',30,55,'发送端把L bit推上链路\n发送时延 L/R',370,110),node('prop',500,55,'首bit沿介质传播\n传播时延 d/v',370,110),node('last',130,275,'忽略排队和处理：最后一bit到达用时 L/R + d/v',640,90)],
 [edge('send','prop'),edge('prop','last')],['L用bit、R用bit/s，传播距离d与速率v须使用相容单位；传播时延与报文长度无直接关系。','存储转发多跳时还要算每跳发送、传播、排队与处理；分组可流水重叠，不能把一整个报文的发送时间对所有分组和链路重复累加。'])
picture('数字编码与调制：时钟信息在哪里','manchester','曼彻斯特与差分曼彻斯特：先约定位值',[
 node('m',35,40,'曼彻斯特示例约定\n0：位中间高→低\n1：位中间低→高',380,140),node('d',485,40,'差分曼彻斯特示例约定\n每位中间必有跳变\n0：位开始跳变，1：不跳变',380,140),node('n',130,290,'传数据同时携带时钟信息；具体高低电平与0/1对应应遵题设',640,75)],[],['两种编码每个码元位中间都有跳变，接收方可据此恢复定时。曼彻斯特看位中间跳变方向；差分曼彻斯特看位边界是否发生跳变。','图给出一种常见约定，不同标准或题设可能把0和1的定义反过来。不要只记某个跳变图而不读编码规则。'])
picture('CSMA/CA、帧间间隔与无线确认','wifi-rts-cts','可选RTS/CTS交换：谁听到后需要保持安静',[
 node('s',35,50,'发送站',200,80),node('r',650,50,'接收站/AP',200,80),node('rt',70,230,'RTS → CTS → DATA → ACK\n相邻响应之间使用SIFS',750,90),node('nav',180,345,'邻站根据时长信息更新NAV，按规则延后竞争',540,55)],
 [edge('s','r','可选RTS/CTS保护')],['普通竞争访问典型先等待DIFS并随机退避，之后可以直接发DATA，也可采用RTS/CTS保护。CTS、ACK等响应采用更短的SIFS。','RTS/CTS能缓解隐藏站问题，但不是所有802.11数据帧发送前都必须有RTS/CTS；无线无法简单等同共享以太网的边发边检测碰撞。'])
picture('子网掩码与前缀规划','subnet-prefix','把192.168.1.0/24等分为4个/26',[
 node('p',210,10,'借2位：/24 → /26\n每块64个地址，掩码255.255.255.192',480,85),node('s0',20,235,'.0/26\n范围 .0～.63',205,100),node('s1',240,235,'.64/26\n范围 .64～.127',205,100),node('s2',460,235,'.128/26\n范围 .128～.191',205,100),node('s3',680,235,'.192/26\n范围 .192～.255',205,100)],
 [edge('p','s0'),edge('p','s1'),edge('p','s2'),edge('p','s3')],['网络前缀统一为192.168.1，图中省略了前三段。每个/26地址块大小2^(32−26)=64，起点必须按64对齐。','在常规IPv4子网中，每块扣除网络地址和广播地址后可分配62个主机地址；/31点到点和/32等特殊用途不能套同一个减2规则。'])
picture('NAT 与 NAPT：改写什么、怎样返回','napt-table','NAPT：两个内网端点映射为不同公网端口',[
 node('a',20,40,'10.0.0.2:5000',220,80),node('b',20,280,'10.0.0.3:5000',220,80),node('nat',320,140,'NAT映射表\n.2:5000 ↔ 203.0.113.1:40001\n.3:5000 ↔ 203.0.113.1:40002',550,120)],
 [edge('a','nat'),edge('b','nat')],['示例两个内网主机访问同一外部服务，NAPT把源IP和源端口改写为公网地址与不同端口。203.0.113.1使用文档示例地址。','返回报文到达不同公网端口后，按转换状态还原内网目的IP与端口；相关校验和也要更新。具体实现可以把远端元组纳入映射/过滤规则。'])
picture('TCP 首部与字节序号','tcp-byte-seq','TCP字节序号：seq和ack都是字节位置',[
 node('old',20,95,'已确认\n…999',180,90),node('seg',245,95,'本段seq=1000，数据600B\n覆盖字节1000～1599',410,90,'active'),node('new',700,95,'下一期待字节\nack=1600',180,90),node('n',155,290,'无丢失且此前数据连续：接收后累计确认1600',590,70)],
 [edge('old','seg'),edge('seg','new')],['seq=1000表示本段首个数据字节的序号；600字节使用1000～1599，不能把末字节写成1600。','ack=1600表示1600之前的字节都已连续收到。纯ACK不占序号，SYN和FIN各占一个序号；没有数据的段也仍有seq字段。'])
picture('电子邮件系统与发送/读取路径','email-path','邮件投递与读取：SMTP、POP3、IMAP各做什么',[
 node('ua',20,60,'发件人客户端',190,80),node('ms',320,60,'发件服务器',220,80),node('mr',650,60,'收件服务器',220,80),node('ub',650,300,'收件人客户端',220,80)],
 [edge('ua','ms','提交'),edge('ms','mr','SMTP'),edge('ub','mr','POP3 / IMAP')],['发件客户端通常通过SMTP提交到发送服务器，服务器之间通过SMTP投递。收件人用POP3或IMAP访问其邮箱；网页邮箱的浏览器到Web服务通常使用HTTPS。','图中POP3/IMAP箭头表示客户端发起访问请求，邮件数据响应方向相反。POP3是否删除服务器副本取决于客户端会话命令和保留设置；IMAP支持服务器端状态同步。'])
(R/'data/408-handbook.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Attached',static_count,'additional structural diagrams.')
