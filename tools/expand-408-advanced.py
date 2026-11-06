"""Advanced reversible examples. Re-running replaces only this script's own sections."""
from pathlib import Path
import json,copy,html,heapq
from visual408 import node,edge,frame,row,tree,draw,styles
R=Path(__file__).resolve().parents[1];items=json.loads((R/'data/408-handbook.json').read_text());by={x['title']:x for x in items};examples=[]
def add(card,slug,title,steps,static=-1):
 assert card in by,card
 examples.append((card,'advanced-'+slug,dict(scene='board',title=title,steps=steps,height=420),static))
def story(card,slug,title,states,note=''):
 add(card,slug,title,[frame(t,e,row(v,a),note=note) for t,v,e,a in states])
# DATA STRUCTURES (8). Red-black deletion examples are complete tiny trees, with explicit NIL.
steps=[]
for t,e,vals,links in [
 ('删除10之前','根20黑，两个孩子10黑、30黑，30右孩子40红；省略的NIL全黑。这棵树初始黑高一致。',[('p',360,20,'20 · 黑','base'),('x',100,145,'10 · 黑','base'),('s',600,145,'30 · 黑','base'),('f',720,280,'40 · 红','base')],[('p','x'),('p','s'),('s','f')]),
 ('删除黑叶，左侧少一重黑','删除10后用NIL代替；用“双黑”标记缺少的那一重黑，只是修复算法的记号，不是真实第三种颜色。',[('p',360,20,'20 · 黑','base'),('x',100,145,'NIL · 双黑','active'),('s',600,145,'30 · 黑','base'),('f',720,280,'40 · 红','base')],[('p','x'),('p','s'),('s','f')]),
 ('黑兄弟的远侄为红','x在左，兄弟30在右，远侄是40。令兄弟继承父色、父20和远侄40变黑，再对20左旋。',[('s',360,20,'30 · 黑','done'),('p',100,200,'20 · 黑','base'),('f',600,200,'40 · 黑','done')],[('s','p'),('s','f')])]:
 n,es=tree(vals,links);steps.append(frame(t,e,n,es,note='“远侄”相对双黑位置定义：双黑在左时，兄弟的右孩子为远侄。'))
add('红黑树删除的黑高修复','rbt-far-nephew','红黑树删除：黑兄弟、红远侄时怎样旋转',steps)
steps=[]
for t,e,v,l in [
 ('原树三个黑结点','根20黑，左10黑，右30黑，未画出的NIL均黑。',[('p',360,20,'20 · 黑','base'),('x',100,200,'10 · 黑','base'),('s',600,200,'30 · 黑','base')],[('p','x'),('p','s')]),
 ('删去黑叶10','x由NIL替代，左侧路径少一重黑。兄弟30为黑，近侄与远侄都是黑NIL。',[('p',360,20,'20 · 黑','base'),('x',100,200,'NIL · 双黑','active'),('s',600,200,'30 · 黑','base')],[('p','x'),('p','s')]),
 ('兄弟改红，把缺黑上推','把30改红，使右侧也少一重黑；将修复位置上推到父20。父若非根，还需继续看新的父、兄弟、侄。',[('p',360,20,'20 · 双黑','active'),('x',100,200,'NIL · 黑','base'),('s',600,200,'30 · 红','base')],[('p','x'),('p','s')]),
 ('到根后消去额外黑标记','20恰好是根，去掉额外黑标记即可结束；所有路径的黑高一起减少1，但仍彼此相同。',[('p',360,20,'20 · 黑','done'),('s',600,200,'30 · 红','base')],[('p','s')])]:
 n,es=tree(v,l);steps.append(frame(t,e,n,es))
add('红黑树删除的黑高修复','rbt-propagate','红黑树删除：兄弟两侄全黑为何要向上修复',steps)
# Linear probing with tombstones.
slots=['空']*7;steps=[]
for key in [10,17,24]:
 at=key%7;probes=[]
 while slots[at]!='空':probes.append(at);at=(at+1)%7
 probes.append(at);slots[at]=str(key);steps.append(frame('插入'+str(key),f'h(k)=k mod 7，从槽{key%7}开始线性探查{probes}，放入槽{at}。',row([str(i)+':'+v for i,v in enumerate(slots)],[at]),note='表长7，探查依次+1并模7回绕；“空”表示从未占用。'))
slots[4]='已删';steps.append(frame('删除17只留墓碑','槽4标为已删，不能直接标成从未用过的空槽，否则查找24会错误提前停止。',row([str(i)+':'+v for i,v in enumerate(slots)],[4])))
steps.append(frame('查找24越过墓碑','沿3→4→5：槽3是10，槽4已删仍继续，槽5命中24。只有真正未使用的空槽才可据此判失败。',row([str(i)+':'+v for i,v in enumerate(slots)],[5]),note='插入可复用墓碑；若需排除重复关键字，应继续检查探查链后部。'))
add('开放定址的探查与链地址法','hash-tombstone','线性探查：为什么不能把删除位置直接清空',steps)
steps=[]
for t,e,ns,es in [
 ('删除有两个孩子的20','取右子树中最小关键字25作为中序后继；不是随便用右孩子30替换。',[node('r',330,20,'20'),node('l',100,160,'10'),node('b',590,160,'30'),node('s',420,290,'25'),node('c',720,290,'40')],[edge('r','l'),edge('r','b'),edge('b','s'),edge('b','c')]),
 ('后继关键字移到目标位置','复制或移植后继记录25到原20的位置；若用复制法，原后继结点暂时还在，需继续删除它。',[node('r',330,20,'25',tone='active'),node('l',100,160,'10'),node('b',590,160,'30'),node('s',420,290,'25（待删）'),node('c',720,290,'40')],[edge('r','l'),edge('r','b'),edge('b','s'),edge('b','c')]),
 ('删除原后继位置','本例后继25是叶子，可直接摘除；一般后继无左孩子，但可能有右孩子，须接回其右子树。',[node('r',330,20,'25',tone='done'),node('l',100,160,'10'),node('b',590,160,'30'),node('c',720,290,'40')],[edge('r','l'),edge('r','b'),edge('b','c')])]:steps.append(frame(t,e,ns,es,note='中序序列从10,20,25,30,40变成10,25,30,40，排序性保持。'))
add('二叉排序树的查找、插入与删除','bst-successor','BST删除：用后继替换后还要删除哪个结点',steps)
story('B+ 树与 B 树的区别','bplus-range','B+树范围查询：定位一次，再沿叶链继续',[
 ('查询[18,45]',['根索引：20 | 40 | 60','叶1：10,20','叶2：30,40；叶3：50,60'],'沿用子树最大键约定，先从根选择上界20对应的第一个孩子，定位第一个≥18的记录。',[0,1]),
 ('在第1个叶命中20',['叶1输出：20','叶链接 → 叶2','结果：20'],'10小于18，不输出；20满足区间条件。',[0]),
 ('顺序扫描第2个叶',['叶2输出：30,40','叶链接 → 叶3','结果：20,30,40'],'进入后继叶无需每个记录都重新从根定位。',[0,2]),
 ('见到50停止',['50 > 上界45','停止沿叶链扫描','最终：20,30,40'],'叶层整体有序，后面所有键也不会再满足上界，因此可以停止。',[0,2])])
story('k 路平衡归并与磁盘 I/O','external-merge','外部排序：8个初始段用3路归并需几趟',[
 ('初始段已形成',['8个有序初始段','3个输入缓冲+1个输出缓冲','每次最多合并3段'],'假设每个缓冲一块，归并路数3。这里只数形成初始段之后的归并趟数。',[]),
 ('第1趟',['段1,2,3 → 段A','段4,5,6 → 段B','段7,8 → 段C'],'8个段按最多3路合并，得到ceil(8/3)=3个更长有序段。',[0,1,2]),
 ('第2趟',['段A,段B,段C','3路合并为最终段','共2趟归并'],'ceil(log₃8)=2；每趟读完并写出全部记录。',[1,2]),
 ('计算I/O',['文件共B块','2趟归并：4B块I/O','含初始段生成：通常6B'],'按无额外缓存、每趟全文件读写模型，初始段生成另算一次读和写。只有题目要求完整外排时才加上该部分。',[1,2])])
# Replacement selection with a 3-record workspace.
stream=[5,1,4,2,6,3,0];active=stream[:3];heapq.heapify(active);rest=iter(stream[3:]);frozen=[];run=[];runs=[];steps=[]
while active or frozen:
 if not active:
  runs.append(run);run=[];active=frozen;frozen=[];heapq.heapify(active)
 v=heapq.heappop(active);run.append(v);incoming=next(rest,None)
 if incoming is not None:heapq.heappush(active if incoming>=v else frozen,incoming)
 ns=row(['活动：'+','.join(map(str,sorted(active))),'冻结：'+','.join(map(str,sorted(frozen))),'本段输出：'+','.join(map(str,run))],[2])
 steps.append(frame('输出'+str(v)+(f'，读入{incoming}' if incoming is not None else '，输入已尽'),('新记录不小于刚输出值，继续参与当前段。' if incoming is not None and incoming>=v else '新记录更小，冻结到下一段。' if incoming is not None else '不再补入新值，继续排空活动区。')+' 活动区为空才开始新段。',ns,note='工作区3条记录；输入顺序5,1,4,2,6,3,0。'))
if run:runs.append(run)
assert runs==[[1,2,4,5,6],[0,3]],runs
steps.append(frame('得到两个初始段','最终初始段为[1,2,4,5,6]和[0,3]。段可长于内存容量，但长度取决于输入，不保证每段恰为2M。',row(['段1：1,2,4,5,6','段2：0,3'],[0,1])))
add('置换选择与初始归并段长度','replacement-freeze','置换选择：为什么有的较小记录必须冻结',steps)
# Loser tree for four heads; internal nodes store losers, winner is held separately.
steps=[]
for heads,exp in [([3,8,5,7],'叶子为四路段首。比较3与8，败者8留左内部结点；比较5与7，败者7留右内部结点；再比3与5，根内部留败者5，总冠军3另存。'),([9,8,5,7],'输出冠军3后，只从其所属第0路补9。9先与缓存败者8比，8胜、9留原内部点；8再与缓存败者5比，5胜、8留根。其他分支不用重赛。')]:
 a,b,c,d=heads;w1,l1=min(a,b),max(a,b);w2,l2=min(c,d),max(c,d);winner,rootloser=min(w1,w2),max(w1,w2)
 ns=[node(str(i),40+i*210,295,'路'+str(i)+'：'+str(v),170,70,'active' if v==winner else 'base') for i,v in enumerate(heads)]+[node('l',150,165,'存败者 '+str(l1),190,65),node('r',570,165,'存败者 '+str(l2),190,65),node('root',350,55,'存败者 '+str(rootloser),190,65),node('winner',30,30,'总冠军 '+str(winner),210,65,'done')]
 steps.append(frame('建立比赛' if heads[0]==3 else '只重赛冠军路径',exp,ns,[edge(0,'l'),edge(1,'l'),edge(2,'r'),edge(3,'r'),edge('l','root'),edge('r','root'),edge('root','winner')],note='图按自底向上比赛画箭头；内部存败者，冠军单独保存。'))
add('最佳归并树与败者树','loser-replay','败者树：内部存输家，为什么只重赛一条路径',steps)
# COMPUTER ORGANIZATION (8)
story('补码加减与溢出：符号、进位和双符号位','negate-minimum','补码最小负数：按位取反加1为何仍是自己',[
 ('4bit补码最小值',['位串1000','真值−8','4bit有符号范围[−8,7]'],'取相反数应为+8，但+8不在4bit有符号范围内。',[]),
 ('按位取反',['1000 → 0111','再加0001','得到1000'],'电路按低4位执行取反加1，结果位串回到1000。',[0,2]),
 ('识别有符号溢出',['位串仍1000','解释仍为−8','不能当作+8'],'这是固定宽度补码取负的边界溢出，位串结果不代表数学真值已正确保存。',[1,2]),
 ('先扩宽再取负',['符号扩展：11111000','8bit取负：00001000','真值+8'],'扩大到能表示+8的位宽后再做取负，便可得到正确结果。实际C最小整数取负须遵循类型范围与溢出规则。',[1,2])])
story('尾数规格化与浮点加减的五个步骤','round-even','舍入到最近偶数：正好一半时看哪一位',[
 ('只保留3位有效尾数',['精确值1.011₂','保留候选1.01₂','丢弃部分为恰好半ULP'],'1.011₂位于1.01₂与1.10₂正中间；ULP是本例相邻可表示数间隔。',[0,1]),
 ('看保留末位奇偶',['下候选1.01₂末位1','上候选1.10₂末位0','选择1.10₂'],'最近偶数中的偶数指保留尾数整数编码的最低位为0，不是要求数值本身为偶整数。',[2]),
 ('另一半值1.001₂',['下候选1.00₂末位0','上候选1.01₂末位1','选择1.00₂'],'这次正好一半时不进位，仍选择最低保留位0的候选。',[2]),
 ('不是恰好一半时',['1.0111₂','更靠近1.10₂','不再用奇偶打破平局'],'保护位与粘滞信息用于判断大于、等于还是小于半ULP，不能把所有丢弃首位1都机械当作同一种情况。',[1,2])])
# Two-way set associative cache, LRU within the set.
steps=[];order=[]
for b in [0,2,0,4]:
 hit=b in order;victim=None
 if hit:order.remove(b)
 elif len(order)==2:victim=order.pop(0)
 order.append(b)
 steps.append(frame('访问主存块'+str(b),('命中，刷新该块为最近使用。' if hit else '失效，装入空行。' if victim is None else f'失效，同组已满，淘汰最久未用块{victim}。'),row(['组号=b mod 2=0','组内LRU→MRU\n'+','.join(map(str,order)),'命中' if hit else '失效'],[1]),note='Cache共4行，2路组相联→2组；块0、2、4都映射组0。'))
assert order==[0,4]
add('Cache 三种映射与地址划分','set-associative-lru','2路组相联：别组有空行仍要替换吗',steps)
story('双端口 RAM、单体多字与多体交叉存储','bank-conflict','低位交叉：连续字与跨4字访问为何不同',[
 ('4个存储体',['体号=字地址 mod 4','每体存储周期T=4τ','总线启动间隔τ'],'每体启动一次后，至少隔4τ才能再次启动同体请求。',[]),
 ('连续字0,1,2,3,4',['体序列0,1,2,3,0','启动0,τ,2τ,3τ,4τ','各体都来得及恢复'],'连续访问轮流分散到不同体，可按τ间隔启动。',[0,1]),
 ('跨4字访问0,4,8,12',['体序列0,0,0,0','启动0,4τ,8τ,12τ','全部竞争同一体'],'地址跨度恰为体数，低位体号不变，必须等待该体恢复，不能继续每τ启动。',[0,1]),
 ('区分吞吐与首字延迟',['交叉提高连续访问吞吐','单次存储延迟仍约T','不是所有地址序列都加速'],'给出T、τ、体数以及访问地址序列后才能判断可否轮流启动。',[2])])
D0=0b1010;D1=0b0110;D2=0b1100;P=D0^D1^D2;recovered=P^D0^D2;assert recovered==D1
story('RAID：条带、镜像和校验的分工','raid-parity','RAID校验：一块盘丢失后怎样用异或恢复',[
 ('一个条带',['D0=1010','D1=0110','D2=1100'],'以三个数据块和一个校验块说明按位异或，图只画一个条带。',[]),
 ('计算校验块',['1010 XOR 0110 XOR 1100','P='+f'{P:04b}','校验与三个数据关联'],'异或满足交换律与a XOR a=0。RAID5的校验位置会在条带之间轮转，本条带只是某一位置的示例。',[1]),
 ('D1所在盘失效',['D1未知','P、D0、D2仍可读','D1=P XOR D0 XOR D2'],'相同数据异或两次抵消，留下缺失块。',[2]),
 ('恢复D1',['0000 XOR 1010 XOR 1100','D1=0110','校验恢复成功'],'本例P=0000。RAID5通常只能容忍一个成员盘失效；它不是文件误删或所有灾难情形的备份替代品。',[1])])
story('立即、直接、间接与寄存器寻址','addressing-compare','同一个地址字段100：立即、直接和间接寻址',[
 ('内存内容固定',['M[100]=500','M[500]=42','指令字段A=100'],'以下只改变寻址方式，不改变这两个内存单元内容。',[]),
 ('立即寻址',['操作数=字段值100','字段就是数据','不为取该操作数另访存'],'这里只是不为获取这个立即数额外访存，取指本身仍需从指令存储层次获得。',[0]),
 ('直接寻址',['有效地址EA=100','操作数=M[100]=500','需一次操作数访存'],'地址字段直接给出操作数位置。',[0,1]),
 ('一次存储器间接寻址',['EA=M[100]=500','操作数=M[500]=42','需两次数据访存'],'第一次取指针，第二次取数据；忽略Cache命中与取指开销。',[0,1])])
story('结构、数据和控制冒险','alu-forwarding','相邻ALU指令：转发如何消除RAW等待',[
 ('两条指令',['I1：add r1,r2,r3','I2：sub r4,r1,r5','I2要读取I1产生的r1'],'假设经典五段流水线，寄存器值在I1的EX结束时形成。',[]),
 ('I1在EX，I2在ID',['I1计算出r1新值','I2读寄存器可能仍是旧值','结果进入EX/MEM锁存器'],'仅靠ID阶段读到的寄存器值不一定满足数据相关。',[2]),
 ('下一周期I2进入EX',['EX/MEM中的r1结果','转发到I2的ALU输入','不必等I1写回WB'],'选择正确旁路输入，使I2使用新值；在此模型中ALU→ALU相关通常无需停顿。',[0,1]),
 ('与load-use区分',['lw的结果在MEM末才就绪','紧接的使用者EX要更早用','有转发也可能需停顿'],'是否停顿由数据何时产生与何时需要决定，不是见到RAW就固定停一拍。',[2])])
story('总线性能、复用与事务四阶段','burst-timing','突发总线传送：地址阶段不能每个字重复算',[
 ('题设模型',['地址阶段2个总线周期','每数据拍传8B','块大小32B'],'假设一次突发仅发一次地址，后续每周期传8B，忽略额外等待和结束开销。',[]),
 ('数据拍数',['32B ÷ 8B/拍','需要4个数据周期','总周期2+4=6'],'位宽、字节与总线周期必须统一；这里数据拍已经按8B计量。',[1,2]),
 ('总线周期10ns',['6×10ns=60ns','一次32B块传输','有效平均带宽约533MB/s'],'32B/60ns≈5.33×10⁸B/s，按十进制MB/s写约533；每拍峰值带宽为800MB/s，含地址开销的平均值更低。',[0,2]),
 ('题设增加等待时',['若内存首数据另需等待','必须再加对应等待周期','不能直接套6周期'],'主存访问延迟与总线传输时间是否重叠，应从题给时序确认。',[1])])
# OPERATING SYSTEMS (8)
# Banker request granted by resource count, rejected by safety test.
story('安全状态与银行家算法','banker-unsafe-request','银行家算法：资源够给，为何仍拒绝请求',[
 ('初始安全状态',['资源总量3；Available=1','P0：Alloc=1,Max=3,Need=2','P1：Alloc=1,Max=2,Need=1'],'只有一类资源。P1可先完成归还1，使Work=2，再让P0完成，所以初始安全。',[]),
 ('P0请求1',['Request=1≤Need0=2','Request=1≤Available=1','通过数量检查'],'两项检查只说明没超需求、当前资源够给，尚未证明试分配后安全。',[0,1]),
 ('试分配后',['Available=0','P0：Alloc=2,Need=1','P1：Alloc=1,Need=1'],'所有未完成进程都至少还需要1，而Work=0，找不到可假设完成的进程。',[0]),
 ('回滚并等待',['无安全序列','撤销本次试分配','P0请求暂不批准'],'不安全状态不等于此刻一定已经死锁；银行家避免进入无法保证完成顺序的状态。',[0,1])])
story('多级页表：层数、地址结构和访问次数','two-level-index','二级页表查找：10位目录、10位页号、12位偏移',[
 ('32bit虚拟地址',['目录号=1，页表索引=2','页内偏移0x034','页大小4KiB'],'本例虚拟地址=(1<<22)+(2<<12)+0x034=0x00402034；每页表项4B，一页可存1024项。',[]),
 ('先查页目录',['目录基址0x100000','目录项地址=0x100004','目录项给页表基址0x300000'],'目录项地址=页目录基址+目录号×4，不是把目录号当字节偏移直接相加。',[1]),
 ('再查二级页表',['页表项地址0x300008','条目给出页框号0x5A','检查驻留与权限'],'二级索引2，所以项地址加8B；图中两级表项都合法、有效且驻留。',[0,1]),
 ('拼出物理地址',['页框基址0x5A000','偏移仍为0x034','物理地址0x5A034'],'无TLB、各级页表不缓存时：两次表访问后再访问数据，共3次主存访问；不计缺页等额外处理。',[2])])
story('分段、段表与段页式','segment-limit','分段保护：先判断段内偏移，再做基址相加',[
 ('段表项',['段号2','base=4000B','limit=1000B'],'limit在本例定义为段长，因此合法偏移是0≤d<1000。若题设limit为最大合法偏移，上界比较要随之改变。',[]),
 ('访问(2,600)',['600<1000，合法','物理地址4000+600','结果4600B'],'段号有效且访问权限允许，先通过界限检查再形成地址。',[1,2]),
 ('访问(2,1000)',['1000不小于段长1000','发生越界异常','不能访问物理5000B'],'端点偏移等于段长时已经超出本段，不能把求得数值地址当成访问合法的证据。',[0,1]),
 ('段号越界另行检查',['段表只有0,1,2段','若给段号3则无对应项','不进入base+d计算'],'段号范围与段内偏移是两道检查；合法地址还必须满足读写执行权限。',[1])])
# The classic FIFO Belady sequence, computed for 3 and 4 frames together.
refs=[1,2,3,4,1,2,5,1,2,3,4,5];queues={3:[],4:[]};faults={3:0,4:0};steps=[]
for i,page in enumerate(refs):
 state=[]
 for size in (3,4):
  q=queues[size];miss=page not in q
  if miss:
   faults[size]+=1
   if len(q)==size:q.pop(0)
   q.append(page)
  state.append(f'{size}框：'+','.join(map(str,q))+f'\n缺页{faults[size]}次'+('（失效）' if miss else '（命中）'))
 steps.append(frame(f'第{i+1}次访问页{page}','FIFO只在装入时改变进入次序；命中不把页面移动到队尾。',row(state,[0,1]),note='队列从左到右为最早装入→最晚装入；参考串1,2,3,4,1,2,5,1,2,3,4,5。'))
assert faults=={3:9,4:10}
steps.append(frame('更多页框反而更多缺页','同一参考串，FIFO在3框缺页9次，在4框缺页10次，出现Belady异常。OPT和LRU具有栈性质，不出现该类异常。',row(['3页框：9次','4页框：10次'],[1])))
add('OPT、FIFO与LRU页面置换','fifo-belady','FIFO的Belady异常：3框9次，4框为什么10次',steps)
story('请求分页的表项、缺页处理与指令重启','dirty-victim','缺页置换：脏页为什么多一次磁盘写回',[
 ('新页P不驻留',['当前要访问P','没有空闲页框','选中牺牲页Q'],'假定P合法但不驻留，需要把P调入一个页框。',[]),
 ('Q的修改位M=1',['Q在内存被修改过','磁盘副本已过时','先将Q写回外存'],'若Q为干净页且有可复用磁盘副本，通常可省略本次写回；具体文件映射与后备存储策略另看题设。',[1,2]),
 ('撤销旧映射并调入P',['更新Q的驻留状态','处理相关TLB旧项','把P读入释放的页框'],'旧页框即将复用，不能让Q旧映射继续指向其中的新数据；更新顺序须保证映射一致。',[0,1]),
 ('建立P的新映射',['PTE指向新页框','设置合法权限与状态','恢复并重启原访存'],'一次缺页服务可能包含脏页写出和新页读入两次外存传送，不能只按一次普通主存访问算。',[2])])
story('FAT显式链接与表容量','fat-walk','FAT文件读取：逻辑第2块不一定是磁盘第2块',[
 ('目录起始块为5',['FAT[5]=9','FAT[9]=2','FAT[2]=EOF'],'文件块链为5→9→2→结束；逻辑块号从0起。',[]),
 ('逻辑块0',['从目录起始块5','对应物理块5','读取第一个数据块'],'文件目录给起始块，不需要先从物理块0扫描到它。',[1]),
 ('逻辑块1',['跟随FAT[5]=9','对应物理块9','读取第二个数据块'],'FAT表项记录链中下一物理块号，不是下一字节地址。',[1]),
 ('逻辑块2',['继续FAT[9]=2','对应物理块2','该块之后EOF'],'逻辑连续不要求物理连续。若FAT已整体在内存，沿链查FAT不必每次都读一次磁盘；缓存条件决定实际I/O数。',[1,2])])
story('进程映像、fork与exec','cow-fork','写时复制：fork之后谁真正复制物理页',[
 ('fork之前',['父虚拟页V → 物理页F','页中值=7','可写'],'为简化只跟踪一个私有可写数据页，不讨论共享映射。',[]),
 ('fork采用COW',['父V → F；子V → F','两者暂共享物理页F','映射受写保护并标记COW'],'内核复制必要管理信息，数据页暂不立即复制；父子逻辑地址空间仍独立。',[0,2]),
 ('子进程写值9',['子写入触发保护异常','识别合法COW写入','分配新页G并复制F'],'不是所有保护异常都允许复制后继续，必须确认该映射确为COW且有写权限语义。',[0,1]),
 ('修改子页表并重试',['父V → F，值7','子V → G，写为9','相关TLB项同步更新'],'子重新执行写操作后改G，不改变父的F。页引用计数减少后，原页可能恢复独占写权限。',[0,1])])
# SRTN event schedule from concrete arrivals and bursts.
jobs=[('A',0,7),('B',2,4),('C',4,1)];remain={p:b for p,a,b in jobs};t=0;slices=[];steps=[]
while any(remain.values()):
 ready=[(remain[p],a,p) for p,a,b in jobs if a<=t and remain[p]>0];p=min(ready)[2]
 if slices and slices[-1][0]==p:slices[-1]=(p,slices[-1][1],t+1)
 else:slices.append((p,t,t+1))
 remain[p]-=1;t+=1
 if t in [2,4,5,7,12]:
  ns=[node(str(i),40+a*65,100,f'{p}\n{a}→{b}',(b-a)*65-6,100,'active' if i==len(slices)-1 else 'done') for i,(p,a,b) in enumerate(slices)]
  steps.append(frame('推进到t='+str(t),'在就绪进程中选择剩余CPU时间最短者；每次有新到达或当前进程完成都重新比较。',ns,note='到达/总CPU量：A(0,7)、B(2,4)、C(4,1)；忽略切换开销。剩余：'+str(remain)))
assert slices==[('A',0,2),('B',2,4),('C',4,5),('B',5,7),('A',7,12)],slices
add('FCFS、SJF、SRTN与HRRN','srtn-preemption','最短剩余时间优先：新短作业到达时怎样抢占',steps)
# COMPUTER NETWORKS (8)
story('子网掩码与前缀规划','subnet-and','子网计算：192.168.10.130/26怎样确定网络',[
 ('拆分网络与主机位',['掩码255.255.255.192','末字节130=10000010₂','掩码末字节11000000₂'],'/26表示前26bit为网络位，最后6bit为主机位。',[]),
 ('按位与求网络号',['10000010','AND 11000000','=10000000₂=128'],'前三个字节均被掩码保留，所以网络地址为192.168.10.128。',[2]),
 ('将主机位全置1',['网络地址.128','主机位111111₂=63','广播地址.191'],'本块范围.128～.191，每块64个地址，常规可分配主机为.129～.190。',[2]),
 ('判断是否同子网',['.130 AND掩码 → .128','.190 AND掩码 → .128','.200 AND掩码 → .192'],'比较两地址各自与同一掩码相与的结果；不能仅看前三段相同就断言同一个/26子网。',[0,1,2])])
story('NAT 与 NAPT：改写什么、怎样返回','napt-reverse','NAPT返回路径：外网端口怎样找到内网进程',[
 ('内网发起连接',['源10.0.0.2:5000','目的198.51.100.9:443','经过NAPT网关'],'198.51.100.0/24与203.0.113.0/24为文档示例地址。',[]),
 ('建立转换状态',['10.0.0.2:5000','映射203.0.113.1:40001','远端仍198.51.100.9:443'],'网关改写源IP和源端口，并更新相关校验和；具体映射键和过滤策略由实现决定。',[1]),
 ('响应从外网返回',['源198.51.100.9:443','目的203.0.113.1:40001','查已有转换状态'],'回复的目的端口对应外部映射，不是应用服务端的443。',[1,2]),
 ('反向改写后转内网',['目的还原10.0.0.2:5000','远端源地址和端口保持','交给内网原连接'],'返回方向通常改写目的IP/端口，不能仍向内网广播查找公网端口属于谁。',[0])])
story('ICMP、Ping 与路径探测','traceroute-ttl','Traceroute：TTL=1和TTL=2分别停在哪里',[
 ('路径假设',['源S → 路由R1 → 路由R2 → 目的D','路由器转发前递减TTL','TTL不是以秒直接倒计时'],'简化为两台中间路由器；终点通常不再转发该探测包。',[]),
 ('发送TTL=1',['R1递减后为0','丢弃该包','典型回ICMP时间超过'],'通过ICMP错误报文的源信息识别R1；某些设备可能不响应或限速。',[0,2]),
 ('发送TTL=2',['R1递减到1继续转发','R2递减到0后丢弃','识别R2'],'逐步增大TTL暴露沿途路由器；错误报文回程路径不一定与去程相同。',[1,2]),
 ('发送TTL=3到终点',['R1转发后2，R2转发后1','D收到终点探测','终结回复取决于探测方式'],'UDP探测通常由终点返回端口不可达，ICMP探测可用回显回答；不能把所有Traceroute都限定为一种运输协议。',[1,2])])
# Refragment one existing IPv4 fragment, all offsets are relative to the original payload.
# Original fragment carries payload [1480,2960), offset185, MF1; next link MTU620 -> 600 data each.
steps=[];remaining=1480;start=1480;pieces=[]
while remaining:
 length=min(600,remaining);pieces.append((start,length));remaining-=length;start+=length
 ns=[node(str(i),30+i*290,140,f'数据起点{st}B\n数据长{ln}B\n偏移{st//8}，MF=1',265,130,'active' if i==len(pieces)-1 else 'done') for i,(st,ln) in enumerate(pieces)]
 steps.append(frame('生成子片'+str(len(pieces)),f'本子片数据从原始数据的{pieces[-1][0]}B处开始，片偏移={pieces[-1][0]}÷8={pieces[-1][0]//8}。原片MF=1，所以最后一个子片的MF也仍为1。',ns,note='原片：20B首部+1480B数据，原偏移185、MF=1；新MTU620B，每片首部仍20B，无选项。'))
assert pieces==[(1480,600),(2080,600),(2680,280)]
add('IPv4 分片与再次分片','refragment-offset','IPv4再次分片：最后子片的MF为何仍可能是1',steps)
story('快恢复与拥塞曲线逐轮判读','reno-recovery','Reno快恢复：门限、临时膨胀与退出',[
 ('收到3个重复ACK',['FlightSize=12 MSS','假设rwnd充足','准备重传缺失段'],'采用RFC5681的经典Reno模型，SMSS相同；FlightSize是在途数据量，不必总等于cwnd。',[]),
 ('进入快恢复',['ssthresh=max(12/2,2)=6 MSS','cwnd=ssthresh+3=9 MSS','立即重传缺失段'],'额外3MSS是对触发恢复的三个重复ACK造成网络中已离开数据量的估计，不是将门限设为9。',[0,1]),
 ('又收到一个重复ACK',['cwnd临时增1至10 MSS','满足额度时可发新段','ssthresh仍6 MSS'],'窗口临时膨胀服务于恢复期间的ACK时钟；实际发送还受rwnd和在途量限制。',[0]),
 ('收到确认新数据的ACK',['退出本例快恢复','cwnd回落到ssthresh=6','进入拥塞避免'],'本例只有一次丢段且ACK覆盖所需恢复数据；多丢段与部分ACK可涉及NewReno/SACK等规则，不能直接混用。',[1]),
 ('若走超时分支',['RTO超时属于另一分支','经典模型cwnd降至1 MSS','从慢开始恢复'],'超时与三个重复ACK对cwnd的处理不同。门限按该次检测的在途量计算，不沿用这里临时膨胀后的10去机械对半。',[1,2])])
story('OSPF：数据库同步、最短路径与区域','ospf-lsa','OSPF链路变化：共享拓扑后各自算路由',[
 ('本地链路成本变化',['R1发现与R2链路变化','形成/更新链路状态通告','并非发送整张距离向量表'],'只概括协议逻辑，不逐一列出建立邻接与数据库同步的全部报文。',[0,1]),
 ('可靠泛洪至相应范围',['邻接路由器接收并确认','按序号等规则判断新旧','继续在协议规定范围传播'],'不是每收到一份旧通告都无限重新广播；区域与LSA类型限制传播范围。',[1,2]),
 ('形成一致的链路状态视图',['区域内相关数据库趋于同步','每台路由器以自身为源','各自执行SPF计算'],'拓扑数据库相近不代表所有路由器的最终路由表完全相同，因为源点不同。',[1,2]),
 ('更新转发表',['选择本机到各目的的下一跳','数据包按表逐跳转发','不需要每转一个包都泛洪LSA'],'OSPF控制过程与普通数据包转发属于不同工作；OSPF直接运行于IP之上，协议号89。',[0,1])])
story('VLAN、802.1Q 与跨交换机转发','vlan-broadcast','VLAN广播：交换机连在一起为何不一定都收到',[
 ('两台交换机S1和S2',['两台之间为trunk','各有VLAN10与VLAN20接入口','帧从S1的VLAN10接入口进入'],'假设链路与trunk均允许VLAN10，忽略Native VLAN等特殊配置。',[]),
 ('在S1内泛洪',['目的为广播MAC','只发VLAN10内其他端口','不发往VLAN20接入口'],'VLAN划分广播域；同一交换机上不同VLAN的接入口也不会因此收到同一广播。',[1,2]),
 ('经trunk发往S2',['携带对应VLAN标识','S2识别属于VLAN10','再仅在其VLAN10端口泛洪'],'通常使用802.1Q标签在共享trunk上区分VLAN，接入端口对普通主机的封装另按配置。',[0,1]),
 ('跨VLAN通信',['VLAN10到VLAN20','需要三层路由功能','普通二层转发不能直接跨越'],'路由器或三层交换机可提供互联；分开广播域不等于它们永远无法通信。',[1,2])])
story('HTTP 持久连接与 RTT 计算','http-pipeline','HTTP持久连接：三个小对象怎样数请求RTT',[
 ('计时前提',['TCP持久连接已经建立','3个独立小对象同时已知','忽略传输时间、DNS、TLS、处理'],'只比较理想化HTTP/1.1请求方式，不把建立连接的RTT重复算到每个对象。',[]),
 ('不采用流水线',['请求1→响应1：1 RTT','请求2→响应2：1 RTT','请求3→响应3：1 RTT'],'后一个请求等前一个响应完成后才发，串行共约3RTT。',[0,1,2]),
 ('理想流水线',['连续发出请求1,2,3','服务器按响应顺序返回','理想请求等待约1 RTT'],'在忽略数据传输与处理、请求可紧接发送的模型下，三个响应可在约1RTT后开始返回；实际完成时间仍受对象大小与队头阻塞影响。',[1,2]),
 ('对象先依赖基础HTML',['先请求HTML并发现引用','再发出已知内嵌对象请求','必须另算发现阶段'],'若对象URL必须先从HTML中解析，不能在收到HTML前就假定全部请求已发出；HTTP/2多路复用等模式需另建模型。',[0,2])])
# Emit vectors and attach each new example without changing previous section content.
for card,slug,sim,idx in examples:
 s=sim['steps'][idx];svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{html.escape(sim["title"])}</title><desc id="{slug}-desc">{html.escape(s["explain"])}</desc>{styles}<defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path fill="var(--diagram-line,#356493)" d="M0 0 L10 5 L0 10z"/></marker></defs><rect class="bg" width="900" height="500"/><text class="vt" font-size="24" text-anchor="middle" x="450" y="35">{html.escape(sim["title"])}</text><g transform="translate(0 55)">{draw(s,slug)}</g></svg>'
 (R/'images/408'/f'{slug}.svg').write_text(svg)
 secs=by[card]['sections'];secs[:]=[s for s in secs if s.get('diagram')!=slug];secs.append(dict(kind='example',heading='图解与逐步推演：'+sim['title'],diagram=slug,simulation=sim))
(R/'data/408-handbook.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Added',len(examples),'advanced figures and animations:',{s:sum(by[c]['subject']==s for c,*_ in examples) for s in dict.fromkeys(x['subject'] for x in items)})
