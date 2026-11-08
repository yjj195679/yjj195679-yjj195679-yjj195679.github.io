"""Build the standalone 408 review supplement without altering existing study records."""
import json, re
from pathlib import Path
from html import escape as esc
ROOT=Path(__file__).resolve().parents[1]
items=[]
def add(subject, chapter, rows):
    for line in rows.strip().splitlines():
        title, core, detail, example, trap = line.split('|')
        items.append(dict(id=f'k{len(items)+1:03}',subject=subject,chapter=chapter,title=title,core=core,detail=detail,example=example,trap=trap))

add('数据结构','特殊结构与图', '''
特殊矩阵的压缩存储|对称矩阵只存一个三角区；三角矩阵还需统一存放非三角区的相同常量；三对角矩阵只存主对角线及相邻两条对角线。|先明确下标从 0 还是 1 开始、按行还是按列、元素字节数和首地址，再数排在目标元素之前的元素。|1 起始下标、按行存下三角（含对角线）：A[i,j] 的 0 起始序号为 i(i−1)/2+j−1（i≥j）；对称矩阵 i<j 时交换 i、j。三对角矩阵按行压缩、下标从 1 开始时，带内元素 0 起始序号为 2i+j−3，共存 3n−2 个元素。|稀疏矩阵三元组不支持按普通二维数组公式直接随机定位；压缩存储并不总保留随机存取能力。
循环队列的三种判满方式|牺牲一格、计数器、标志位都能区分队空与队满。|约定 front 指向队头，rear 指向下一插入位置。牺牲一格时空：front=rear；满：(rear+1)%m=front；长度：(rear−front+m)%m。|数组长度 6，front=4、rear=2，牺牲一格实现下队长为 4，最多可放 5 个元素。|使用计数器或标志位时可以放满 m 个元素，不能继续套用牺牲一格的容量结论。
线索二叉树的前驱与后继|线索标志用于区分孩子指针和遍历前驱／后继线索；必须先确定采用哪一种遍历。|中序线索树：若右指针为线索，它直接指向后继；若为右孩子，后继是右子树沿左孩子到达的最左结点。|中序序列为 D B E A C，则 B 的后继是 E。左指针为孩子时，前驱是左子树中的最右结点。|中序线索树找后继方便，不代表先序／后序线索树的每一种前驱后继都能用相同步骤得到。
树、森林与二叉树转换|用左孩子、右兄弟表示法：左指针连第一个孩子，右指针连下一个兄弟。|树的先根遍历对应二叉树先序，树的后根遍历对应二叉树中序；森林先序对应二叉树先序，森林中序对应二叉树中序。|A 有孩子 B、C：转换后 A.left=B，B.right=C；树的后根 B C A 与转换二叉树中序 B C A 一致。|树的后根并非对应二叉树后序；一棵树转换后的二叉树根通常没有右孩子，森林转换则可能有。
十字链表与邻接多重表|十字链表用于有向图，一条弧同时加入弧尾的出边链和弧头的入边链；邻接多重表用于无向图，一条边同时属于两个端点的边链。|有向弧结点含尾、头顶点及同尾、同头链接；无向边结点含两个端点及分别关联两端的链接。|删除无向边 {u,v} 时，邻接多重表可以找到同一个边结点，并从 u、v 的两条链摘除。|普通无向图邻接表常为一条边建两个表结点；邻接多重表只有一个共享边结点。不要混淆边数与表结点数。
连通、强连通与弱连通|无向图的极大连通子图是连通分量；有向图任意两点互相可达才强连通。|弱连通是把有向边忽略方向后连通；强连通分量是极大强连通子图，每个顶点恰属于一个强连通分量。|u→v 的图弱连通，但 v 无法到 u，因此不是强连通图。|强连通分量允许只有一个顶点；从某一点能到所有顶点不足以说明整个有向图强连通。
关键路径与活动余量|AOE 网中顶点表示事件、边表示活动；活动最早开始 e(i,j)=ve(i)，最迟开始 l(i,j)=vl(j)−w(i,j)。|按拓扑序求 ve(j)=max(ve(i)+w)，逆拓扑序求 vl(i)=min(vl(j)−w)；余量 l−e=0 的活动为关键活动。|ve(i)=3，vl(j)=10，活动历时 4，则最早开始 3、最迟开始 6、余量 3。|缩短一项关键活动不一定缩短工期：可能存在另一条同长度关键路径；事件余量和活动余量不是同一公式。
并查集：按秩与路径压缩|find 查代表元；union 合并不同集合；按秩／按大小合并控制高度，路径压缩让访问过的结点更接近根。|只按秩合并时树高为 O(log n)；两种优化配合时操作序列的均摊复杂度近似 O(α(n))，不是每次最坏 O(1)。|find(x) 沿 x→p→r 找到根 r，再把 x 的父指针改成 r，不改变集合成员关系。|路径压缩后的秩通常是历史上界，不应理解为实时树高；同根结点再 union 不会增加集合大小。
''')
add('数据结构','查找与排序', '''
分块查找与平均查找长度|索引表通常记录各块的最大关键字和块起始位置；块间有序、块内可以无序。|先查索引定位块，再块内顺序查找。等长 b 块、每块 s 个且等概率成功，顺序查索引时 ASL=(b+1)/2+(s+1)/2。|n=100，分成 10 块各 10 个，索引也顺序查时成功 ASL=5.5+5.5=11。|若索引采用折半查找，或各块不等长／概率不同，必须重算；块内无需有序不意味着块间可以任意交叉。
红黑树性质与调整|根及 NIL 叶结点为黑，红结点的孩子为黑；从任一结点到其后代 NIL 的路径黑结点数相等。|插入先按 BST 定位再调整；通常新结点着红。通过变色和旋转恢复性质。删除黑结点可能破坏黑高，需分兄弟颜色与侄子颜色处理。|若插入结点与父亲均红且叔叔也红，可把父、叔变黑，祖父变红并向上继续检查。|红黑树不要求左右子树等高，也不要求像 AVL 一样高度差≤1；NIL 叶与存关键字的结点要区分。
B+ 树的内部结点与叶结点|内部结点承担索引，完整记录集中在叶层；叶结点通常按关键字顺序链接，适合范围查询。|精确查找一般要落到叶层，内部关键字相等也不能据此认为已取得完整记录；分支数与关键字数按题目定义判断。|查区间 [20,40]：先定位首个≥20 的叶项，再沿叶链扫描到超过 40。|B 树内部结点可以保存记录；B+ 树内部关键字与子树分界的具体约定可能不同，阶数规则以题设为准。
KMP 的 next 与 nextval|失配时主串指针通常不回退，模式串依照 next 跳转；nextval 跳过某些必然再次失败的比较。|先写清下标从 0／1 开始、next[0] 是 −1 还是长度定义。前缀函数 π 与传统 next 的数值不能不经转换混用。|模式 aaaa 在某个 a 上与主串字符 b 失配时，逐次退到前面的 a 都必失败，nextval 可合并这些跳转。|求数组和使用数组必须采用同一种定义；KMP 的线性复杂度是整个匹配过程的总比较量界，不是每轮固定一次比较。
基数排序：LSD、MSD 与稳定性|LSD 从最低位到最高位处理；每趟必须保留已排低位的相对次序，因此通常使用稳定的分配收集过程。|MSD 先按高位分组，再在各组内递归处理下一位；不等于把 LSD 的循环顺序简单反过来后全局收集。|LSD 对 21、12、11：先按个位稳定排成 21、11、12，再按十位稳定排成 11、12、21。|基数排序的复杂度还依赖位数 d 和基数 r，常写 O(d(n+r))；它不受比较排序 Ω(n log n) 下界直接约束。
外部排序、置换选择与败者树|外排的主要成本常是外存 I/O；败者树用于多路归并的胜者选择，置换选择用于形成初始有序段。|r 个初始段做 k 路归并，通常需 ⌈logₖr⌉ 趟；常规 k 路归并至少要 k 个输入缓冲区及一个输出缓冲区，具体以缓冲策略为准。|9 个初始段进行 3 路归并需 2 趟。败者树每输出一个元素后，沿该路到根更新，比较次数为 O(log k)。|置换选择的初始段长度不是固定等于工作区容量；随机输入下常约为 2M，但这是平均表现，不是每段保证。
排序的稳定性与初始有序性|稳定性看相等关键字的原相对顺序；是否受初始有序影响要分别看比较次数和移动次数。|直接插入在有序时约 n−1 次比较、很少移动；选择排序比较次数基本固定；快速排序表现依赖枢轴策略。|带序号 3a、3b：若排序后仍为 3a、3b 才符合稳定要求。判断某种实现时应观察交换是否跨越相等项。|归并排序通常稳定，但合并相等项必须优先取左段；冒泡应只交换逆序项。不能只凭算法名称忽略实现条件。
''')
add('计算机组成原理','性能、运算与表示', '''
性能指标：CPI、MIPS、MFLOPS|CPU 时间=指令条数×平均 CPI／时钟频率；MIPS=指令条数／(时间×10⁶)，MFLOPS=浮点操作数／(时间×10⁶)。|平均 CPI 是按指令动态执行比例加权的平均数。MIPS 值受指令集和工作负载影响，跨机器比较必须保证完成的任务可比。|主频 2 GHz、平均 CPI=2，则指令吞吐率为 1000 MIPS；任务含 10⁹ 条指令时 CPU 时间为 1 s。|一条浮点指令未必恰好对应一次浮点操作；主频更高、MIPS 更大均不足以独立推出某程序更快。
OF、CF、SF、ZF 的边界|CF 反映相应指令的无符号进位／借位，OF 反映有符号溢出；SF 通常取结果符号位，ZF 反映结果是否为零。|加法 OF 可由同号相加异号结果判断，或最高位进位入与进位出异或；减法的 CF 借位约定依 ISA 而定。|8 位 0x7F+1 得 0x80：有符号溢出 OF=1，无符号未产生最高位进位 CF=0。|并非所有 ISA 都有这些标志，所有指令也不一定更新它们。MIPS 的分支通常直接比较寄存器，不依赖 x86 式 OF／CF。
串行进位与并行进位加法器|串行进位逐位传播进位；先行进位用生成项和传播项提前计算多位进位。|若 Pᵢ=Aᵢ⊕Bᵢ，Gᵢ=AᵢBᵢ，则 Cᵢ₊₁=Gᵢ+PᵢCᵢ；这里乘表示与、加表示或。传播项也有采用或定义的教材，须配套。|C₂=G₁+P₁G₀+P₁P₀C₀，体现进位可以由输入直接并行计算。|并行进位不代表零延时；分组级联仍有门级延时与组间进位路径。
乘除运算电路与结果位宽|n 位×n 位的完整乘积通常需 2n 位；乘法可用部分积加法和移位实现，除法可用比较、减法与移位实现。|有符号乘积放回 n 位时，检查高 n 位是否都是低 n 位符号位的扩展；除法还须检查除数为零和商是否可表示。|8 位有符号 −128÷−1 得数学结果 128，超出 8 位有符号范围；−128×1 的完整结果可由高位符号扩展表示。|结果超出数学范围、CPU 的异常行为及 OF／CF 如何变化是不同问题，要按 ISA 指令语义回答，不能统一说清零。
IEEE 754 特殊值|单精度指数 8 位、尾数域 23 位：指数全 0 用于零／非规格化，指数全 1 用于无穷大／NaN。|非规格化数的有效数为 0.f，指数为 1−127；规格化数为 1.f，指数为 E−127；符号位可区分正零与负零。|最小正非规格化单精度数为 2⁻¹⁴⁹；最大有限值的指数域是 254，而非 255。|NaN 不是无穷大。不能把隐含前导 1 套到非规格化数；正负零数值比较相等但位模式不同。
''')
add('计算机组成原理','存储、指令与控制', '''
存储芯片的字扩展与位扩展|位扩展增加每个地址可同时读写的数据位数；字扩展增加地址空间，需要片选区分芯片组。|先用目标容量除以单片容量核对片数，再看地址线低位送片内、高位用于选组；位扩展的同组芯片共用地址和片选。|用 8K×8 芯片组成 32K×16：每组并联 2 片，共 4 组，总计 8 片，片内需 13 根地址线。|容量单位必须统一；数据线数量、地址线数量、片选线数量不可互换。
DRAM 刷新的三种方式|集中刷新在一段连续时间完成所有行；分散刷新把刷新分散到各周期；异步刷新在刷新周期内均匀安排各行。|DRAM 按行刷新，列数不直接决定刷新次数；刷新周期要求每一行在规定时间内至少刷新一次。|有 1024 行、每 64 ms 全部刷新一遍，均匀调度时平均约每 62.5 μs 刷新一行。|刷新与读写访问不同；刷新不依赖 CPU 逐个读取单元。集中刷新会形成一段集中不能正常访问的时间。
高位／低位交叉存储|高位交叉用高位选模块，连续地址通常落在同一模块；低位交叉用低位选模块，连续地址轮流落在不同模块。|m 个模块、单模块存储周期 T、总线传送节拍 τ，要每 τ 连续启动，常需 mτ≥T，并同时满足地址分散和总线条件。|4 模块低位交叉按字编址时，字地址 0、1、2、3 分到不同模块；0、4、8、12 却集中到同一模块。|满足模块数量还不够；跨步访问可能产生模块冲突。按字节编址时应先分离字内偏移。
Flash、SSD 与磨损均衡|Flash 通常按页读写、按更大的擦除块擦除；覆盖更新常通过写入新位置并更新映射完成。|控制器负责逻辑到物理地址映射、垃圾回收和磨损均衡。擦除次数有限，写放大使实际写入量可能大于主机请求量。|只修改 4 KiB 逻辑数据，内部垃圾回收可能还要搬移有效页和擦除块，因此主机写入量不等于闪存写入量。|SSD 没有机械寻道和旋转延迟，但访问成本仍不是零；不能把机械磁盘的调度收益直接套到 SSD。
Cache 写策略的组合|写直达每次写命中同步更新下层；写回先改 Cache 并置脏，替换脏块时才写回下层。|写分配／非写分配处理写不命中。写回配写分配、写直达配非写分配是常见组合，但不是逻辑上唯一合法组合。|写回 Cache 中修改块 A，随后把它替换出去：若 A 为脏块，必须先将修改写回，干净块可直接丢弃。|写命中策略与写不命中策略属于两个维度；写缓冲能缓解等待，不等于取消主存更新。
TLB、页表与 Cache 的职责|TLB 缓存虚页号到物理页框号及相关权限；页表保存映射；Cache 缓存指令／数据副本。|TLB 未命中先查页表；页表项合法且页面在内存可补 TLB，页面不在内存才触发缺页；物理 Cache 的定位须得到物理地址。|TLB 未命中但页表项 present=1：地址翻译可完成，不发生换入页面操作。|TLB 未命中不等于缺页，Cache 未命中也不等于缺页；某些实现可并行访问 TLB 与 Cache，不能一概说一定串行。
大端与小端|大端把多字节对象最高有效字节放在最低地址；小端把最低有效字节放在最低地址。|先把对象拆成字节，再按地址递增填写；大小端只规定字节顺序，不会把每个字节里的比特再倒序。|0x12345678 存于地址 A 起：大端 A..A+3 为 12 34 56 78；小端为 78 56 34 12。|寄存器中的数值不因内存大小端而变；单字节对象没有字节序差别。
数据对齐与结构体填充|对齐约束和填充受 ABI、类型及编译选项影响；结构体中可能同时存在内部填充和末尾填充。|逐成员将偏移上调到该成员的对齐倍数；最后把总大小上调到结构体对齐倍数。位域／打包规则须另看题设。|假定 char 对齐 1、int 大小及对齐均为 4，则 {char c; int x; char d;} 常用偏移 0、4、8，总大小 12。|上述例子不是所有平台的无条件标准；sizeof 结构体一般不等于各成员 sizeof 的简单和。
函数调用与栈帧|调用过程需传递参数、保存返回位置，并按约定保护仍需使用的寄存器；栈帧可容纳局部变量、溢出参数及保存区。|调用者保存与被调用者保存由调用约定区分；栈增长方向、参数使用寄存器还是栈也由 ABI 决定。|递归函数每次调用都需要独立保存仍存活的局部状态和返回位置，否则下一次调用会覆盖前一次状态。|栈帧不一定使用帧指针；叶函数不一定建栈帧，不能把某一平台的固定布局推广到所有 ISA。
异常：故障、陷阱、中止与外部中断|故障、陷阱、中止是常见教材的异常分类；外部中断来自 CPU 执行指令以外的请求。|典型缺页故障修复后重新执行原指令；陷阱常在指令执行后处理并转向后续指令；中止常无法可靠恢复。具体返回地址依架构与异常类型。|缺页处理把所需页调入后，返回导致缺页的指令重新执行；时钟中断用于定时服务，未必切换进程。|不要用“所有异常都在同一时刻响应／都返回下一条”概括；软件陷入由指令触发，不等于外部中断。
流水线三类冲突与相关|结构冲突来自硬件资源竞争；数据冲突来自依赖；控制冲突来自改变控制流的指令。|经典顺序五级流水常关注 RAW；转发可消除部分等待，但 load-use 仍可能停顿。是否出现 WAR／WAW 要看发射、读写和完成次序。|lw 后紧接使用其结果的 add：若结果在 MEM 末尾才可用，下一条 EX 太早，即使转发仍可能需一个气泡。|相关是程序语义关系，冲突是特定流水实现产生的时序问题；有相关不代表必定停顿。
总线定时与异步握手|同步通信以公共时钟协调；异步通信依请求、应答等握手信号确定传输进度。|常见异步方式包括不互锁、半互锁、全互锁，分别观察信号撤销是否等待对方确认。半同步结合时钟与等待信号。|慢设备未就绪时，通过应答或等待信号延长本次传送，避免按固定节拍采入无效数据。|总线并非一定有时钟信号；突发传输中首字的地址阶段与后续数据阶段成本不同。
I/O 端口独立编址与统一编址|独立编址给 I/O 端口单独的地址空间和专用指令；统一编址把端口映射到存储地址空间。|端口地址通常对应接口中的数据、状态、控制寄存器；统一编址可用访存指令访问，但需要区分普通 RAM 与设备语义。|轮询设备状态后写数据寄存器，是访问接口寄存器，不是直接把地址发到设备介质的每个单元。|统一编址不意味着设备寄存器可以任意缓存，也不意味着 I/O 端口就是物理连接插口。
DMA 周期挪用与总线竞争|DMA 在设备与主存间传送数据，CPU 先设置参数，完成或异常时通常再处理通知。|周期挪用只在需要传输时取得相关总线使用权；停止 CPU 访问主存、周期挪用、交替访存是不同安排。|CPU 当前只访问寄存器而不使用被 DMA 占用的总线时，可能继续执行；当需要同一主存总线时才受竞争影响。|DMA 不等于完全不用 CPU，也不保证 CPU 一直停止；传送单位与完成中断频率需按题设。
SISD、SIMD、MIMD 与硬件多线程|分类依据指令流和数据流：SIMD 为单指令流处理多数据流，MIMD 为多个指令流处理多个数据流。|超标量指同一周期可发射多条指令；硬件多线程保留多个线程的硬件状态，粗粒度、细粒度与同时多线程调度方式不同。|向量加法用同一操作处理多组元素体现 SIMD；多核分别运行不同程序体现 MIMD。|超标量不自动等于多核或多线程；硬件线程数不等于物理核心数。
''')
add('操作系统','系统、进程与同步', '''
宏内核、微内核、外核与模块化|宏内核在内核态集成较多服务；微内核保留较少核心机制并将较多服务放到用户态；外核强调安全分配资源并由库操作系统提供抽象。|模块化关注组件组织和动态装卸，可以与宏内核结合，并非所有名称都构成互斥分类。|文件服务移到用户态后可通过 IPC 与其他组件协作，但带来通信和切换成本。|微内核不意味着没有内核态代码；内核小也不自动保证所有负载都更快。
操作系统引导|上电后由固件完成初始化并选择启动设备，引导程序加载内核，内核再初始化管理结构和运行环境。|BIOS／UEFI 是不同固件环境；引导过程可能经过多级引导，具体流程取决于平台与启动方式。|UEFI 可从系统分区加载启动文件，再把控制交给 OS 加载程序和内核。|不能断言所有机器都执行同一套 MBR 引导流程，也不能把固件当作已加载的操作系统内核。
进程内存映像：代码、数据、BSS、堆、栈|代码段放指令；数据段常放已初始化静态存储期对象；BSS 常表示零初始化对象；堆用于动态分配；栈用于调用相关状态。|BSS 可在可执行文件中主要记录大小，装入时分配并清零；线程通常共享进程地址空间但各有执行栈与寄存器状态。|全局 int a; 常进入 BSS，malloc 得到的空间位于动态分配区域，局部自动变量通常依调用实现放置。|“未初始化全局对象”为零初始化，不是内容随机；局部变量不保证全放栈，编译器可能将其放寄存器。
链接、装入与重定位|链接解决模块间符号引用并形成可装入映像；装入把映像放入内存；重定位将相关地址与实际布局对应。|静态链接在运行前把所需模块组合；装入时动态链接与运行时动态链接的时机不同。动态重定位通常在执行访存时完成。|共享库的函数可在装载阶段解析，也可延迟到首次调用时绑定，取决于系统和链接设置。|静态／动态链接与静态／动态重定位不是同一组概念；动态链接不代表完全不占内存。
用户级与内核级线程|纯用户级线程由用户态线程库管理；内核级线程由内核识别和调度。|多对一模型中一个线程的阻塞系统调用可能阻塞整个进程；一对一／多对多模型不能直接套用这一结论。|一个进程内只有用户线程且内核只识别该进程时，用户线程不能因此同时占用多个核执行。|“线程阻塞则整个进程阻塞”有模型前提；用户线程切换较轻也不表示涉及系统调用时不会进内核。
管道、消息、共享内存与信号|管道传递字节流，消息传递保留消息语义，共享内存让多个进程访问同一映射区域；信号用于异步事件通知。|普通匿名管道通常用于有亲缘关系的进程；共享内存本身不自动解决同步互斥；信号处理需遵守相应语义。|生产者写共享缓冲区、消费者读同一区域时，仍需锁／信号量等约束访问顺序。|把共享区映射好不等于读写天然原子或可见；信号不是用来高效搬运大块数据的通用通道。
闲逛进程／空闲任务|没有其他可运行任务时，CPU 可以运行空闲任务，执行低功耗等待或平台相关维护。|空闲任务保证调度器在无普通就绪任务时仍有可选择的执行上下文；多核常各有空闲上下文。|等待外设期间所有普通任务都阻塞，CPU 可进入空闲等待，下一次中断唤醒后再检查就绪任务。|空闲任务不是普通用户进程无限占满 CPU 的同义词；CPU 利用率一般不把空闲执行计为有效忙碌。
多处理机调度与处理器亲和性|负载均衡让各处理器承担较均匀的工作；处理器亲和性尽量维持任务与原处理器的关联。|迁移有助于均衡但会损失 Cache／TLB 局部性；软亲和是倾向，硬亲和对可运行 CPU 集合施加限制。|任务刚在核 0 运行，继续留在核 0 可能复用其 Cache；若核 0 很忙，迁到空闲核可能更划算。|负载均衡与亲和性有取舍，不能认为迁移越频繁越好；全局队列与每核队列是不同实现选择。
条件变量与信号量|条件变量配合互斥锁等待某个状态条件；典型 wait 原子地释放锁并睡眠，返回前重新获得锁。|Mesa 语义下被唤醒并不保证条件仍成立，应在 while 中重新检查。条件变量 signal 通常不积累为未来可消费的许可，信号量的 V 可增加计数。|while(buffer_empty) wait(not_empty, mutex); 被唤醒后重新持锁检查，成立才取元素。|wait 返回时是否持锁、唤醒是否立即让出 CPU 依具体语义；不能把条件变量 signal 当成信号量 V 的同义操作。
调度、上下文切换与中断|调度是选择接下来运行谁；上下文切换是保存／恢复执行状态；一次调度可以再次选中当前任务。|中断进入内核先保存必要现场，处理完可返回原任务，也可在满足条件时调度到另一任务。模式切换不必然切换进程。|磁盘完成中断唤醒进程 B，但若 A 仍继续运行，则发生了中断处理而没有从 A 到 B 的进程切换。|“发生中断必切进程”“调用调度器必换进程”都过于绝对；同一进程的线程切换也可能需要保存执行上下文。
''')
add('操作系统','内存与文件', '''
地址变换机构 MMU 与 OS 的分工|MMU 按配置执行地址翻译、保护检查并维护相关硬件状态；OS 建立和管理页表／段表、分配物理空间并处理缺页等异常。|页表／段表通常在内存中，CPU 的相应寄存器记录其位置或相关标识；TLB 保存近期映射以减少访表。|访存时 MMU 查 TLB／页表；若缺页则陷入内核，由 OS 调页并更新映射后恢复执行。|不能把每次地址加法都说成由 OS 软件完成，也不能把换页调度都归给 MMU 硬件自动完成。
段表与页表的越界检查|段表项含段基址、段长及权限等；页表项含页框号及存在、权限、修改等状态，具体字段依系统。|段号 s 先检查 s<段表长度；段内偏移 d 再检查 d<段长，合法时物理地址=基址+d。分页的页号／虚拟地址合法性与 present 状态分别检查。|段长为 1000 B，则偏移 999 合法、1000 越界；页表项 present=0 但地址属于合法映射时可构成缺页。|有的题用最大合法偏移作为界限字段，此时判定是 d≤limit；先读“长度”还是“上界”，不要机械套不等式。
页框分配与回收|分配可固定／可变，置换可局部／全局；两者从配额与牺牲页来源两个角度描述。|固定分配通常配局部置换；可变分配可配局部或全局置换。全局置换可从其他进程的可置换页中选择。|局部置换只替换本进程页，不能简单通过牺牲其他进程的页缓解本进程缺页；OS 可另行调整配额。|不能把“分配固定”等同“所有页永不改变”；常规教材不把固定分配＋全局置换作为自然组合。
内存映射文件与普通 I/O|把文件范围映射到虚拟地址空间后，可通过读写内存地址访问文件内容；页面可按需调入，OS 管理相应缓存与回写。|共享映射的修改可反映到文件并与其他映射共享；私有映射常用写时复制，修改不直接回写原文件。映射并不代表立即把整个文件读进 RAM。|对共享映射 p[i] 赋值会弄脏相关页，回写时机由系统机制及显式同步要求确定。|解除映射不等于简单替代一切持久化保证；映射访问也可能发生缺页，不能说永不触发磁盘 I/O。
进程打开文件表、系统打开文件表与 inode|文件描述符索引进程表；进程表项引用系统打开文件对象；该对象记录文件偏移、访问状态等，并关联文件元数据。|dup 得到的新 fd 通常共享同一打开对象和偏移；独立 open 同一文件通常产生不同打开对象。fork 继承的描述符通常也共享原打开对象。|fd3=open(f)，fd4=dup(fd3)，从 fd3 读 10 B 后，fd4 的位置也前移；再次独立 open 得 fd5，其偏移独立。|inode 不保存每次 open 各自的当前偏移；同文件不等于所有描述符都共享一个偏移。
硬链接、软链接与文件删除|同一文件的硬链接对应同一文件系统中的同一 inode；软链接是保存目标路径的独立文件。|删除一个硬链接会减少链接计数；最后一个名字被删时，若仍有打开引用，常需等最后引用释放才回收文件对象与空间。|a、b 为同一文件的硬链接，删 a 后 b 仍可用；c 是指向 a 的软链接，删 a 后 c 可能成为悬空链接。|硬链接通常不能跨文件系统，通常限制对目录建立；软链接可以指向不存在的路径，链接计数也不等于打开次数。
虚拟文件系统 VFS|VFS 为不同文件系统提供统一抽象与接口，把通用文件操作分派给具体文件系统实现。|统一的是访问机制，不意味着磁盘布局、inode 编号规则或全部特性完全一样。|应用用同一套 open/read 接口访问不同挂载文件系统，由 VFS 路由到各自实现。|VFS 不是一个只存在内存中的普通文件系统，也不保证每种底层文件系统都有相同语义细节。
文件系统挂载|挂载把一个文件系统的根关联到目录树中的挂载点，从而通过统一路径访问它。|挂载点原目录中的内容通常被挂载内容遮住，卸载后可重新看到；遮住不等于删除。|将文件系统挂到 /mnt/data 后，访问 /mnt/data/x 会进入新挂载文件系统查找 x。|路径看起来同一棵树，不代表所有文件都位于同一物理分区；挂载和格式化是不同操作。
外存空闲空间管理|位示图每位对应一个块的空闲／占用状态；空闲链连接空闲块；成组链接将多个空闲块地址成组组织。|位是 0 还是 1 表示空闲按题设；成组链接用部分地址带出下一组，不能把所有项都当普通空闲数据块地址。|块号 b、每字 w 位且块号从 0 开始时，字号=⌊b/w⌋，位号=b mod w。|换算字节号、字编号和位编号时要分别计算；块号从 1 开始时通常先减 1。
物理格式化、分区与逻辑格式化|物理／低级格式化建立底层扇区组织及相关控制信息；分区划分逻辑区域；逻辑格式化建立文件系统元数据。|逻辑格式化可初始化超级块、空闲空间管理、根目录等；具体结构依文件系统。现代硬盘低级格式化一般在制造阶段完成。|建立分区后对其创建文件系统，属于逻辑格式化；删建分区表不等于逐个重建介质扇区结构。|快速格式化通常不逐字节擦除全部旧数据；不要把低级格式化、分区、创建文件系统和安全擦除混为一谈。
''')
add('操作系统','设备与 I/O', '''
I/O 软件层次|常见层次为用户级 I/O、设备独立软件、设备驱动、中断处理以及硬件，教材可能合并部分层次。|设备独立软件处理统一接口、命名、保护、缓冲等；驱动把通用请求转换为设备相关命令；中断程序响应设备中断。|read 经过系统调用进入内核，文件／设备相关层次形成请求，驱动配置控制器，完成中断通知上层。|不要用“所有缓冲仅属于某一层”概括实现；层次是职责划分，具体系统可交叉组织。
字符、块、网络设备接口|块设备以块为单位并通常支持寻址；字符设备常提供字节流；网络接口通常围绕分组收发和网络协议栈工作。|设备物理属性与 OS 暴露的接口应区分；同样的 read 名字可能有不同阻塞和定位语义。|磁盘适合按块定位，终端常顺序读字节，网络套接字还区分流式与数据报服务。|不能断言所有设备都支持 seek；网络接口不能只因为有字节数据就归为普通字符设备。
阻塞与非阻塞 I/O|阻塞调用在无法满足条件时可令调用线程等待；非阻塞调用会及时返回当前可用结果或“暂不可用”状态。|同步／异步关注操作完成及通知方式，阻塞／非阻塞关注调用等待行为，二者是不同维度；非阻塞常需轮询或就绪通知配合。|非阻塞读在暂无数据时返回 EAGAIN 一类状态，并不代表已经完成所期待的数据传输。|非阻塞不等于异步，不等于无 CPU 成本；一次 read 也不必把请求字节数全部读满。
SPOOLing 与逻辑共享设备|SPOOLing 使用磁盘上的输入／输出井和相关管理程序，把独占设备的申请转为对作业队列的访问。|多个进程可提交请求，后台服务按序驱动物理设备；逻辑共享不代表物理设备同一时刻服务多个作业。|多个用户同时提交打印作业，每个作业先排队，打印机一次仍实际打印一个作业流。|SPOOLing 不等于单一内存缓冲；“虚拟设备”不代表硬件凭空增加。
SSD 管理与机械磁盘的差异|SSD 管理关注擦除块、页、映射、垃圾回收和磨损；机械磁盘管理还关注柱面寻道与旋转等待。|逻辑连续位置不保证在 SSD 上物理相邻；OS 的块层与 SSD 控制器各自管理不同抽象层次。|频繁更新同一逻辑页，控制器可把新版本写到不同物理页以分散磨损。|SSD 仍有 I/O 调度和队列管理，但 SSTF 这类机械寻道优化的原有依据不再适用。
''')
add('计算机网络','基础、物理与链路', '''
协议三要素与协议／服务|语法规定格式，语义规定字段和动作的意义，同步规定事件顺序及时间关系；协议约束对等实体，服务由下层向上层提供。|看选项在讲报文字段布局、收到后做什么，还是先后顺序／时序；同一过程可涉及多个方面，选择题看强调点。|确认号字段占多少位偏语法；确认号表示已期望收到哪一字节偏语义；何时发确认、超时多久重发偏同步。|实现了某协议并不等于直接向应用暴露同名服务；协议是水平关系，服务是层间垂直关系。
物理层四类接口特性|机械规定连接器外形与引脚等；电气规定电压、电流等；功能规定信号线用途；过程规定事件与操作顺序。|把“某根线表示什么”与“该线上电平取值”分开判断；过程特性也称规程特性。|某引脚用作发送请求是功能；电平多少伏表示 1 是电气；先请求后应答是过程。|不能因为含“信号”二字就一律判电气，要看问的是物理数值、意义还是时序。
波特率、比特率与码元信息量|波特率是每秒码元数；等概率 M 种码元时每码元可表示 log₂M 比特，理想映射下比特率=波特率×log₂M。|带宽限制对应奈奎斯特，噪声限制对应香农；码元种类数与物理线路数不是同一概念。|2400 Baud、每码元 16 种状态时，毛比特率为 9600 bit/s，未扣信道编码等开销。|不能把 Baud 与 bit/s 无条件等同；实际净数据率还可能受冗余和协议开销影响。
曼彻斯特与差分曼彻斯特|曼彻斯特每位中间都有跳变，可提供时钟；差分曼彻斯特用位开始处是否跳变表示数据，并保留位中间跳变。|曼彻斯特中跳变方向与 0／1 的对应约定可能不同，须看题设；差分曼彻斯特也要固定起始电平和编码约定。|先标位边界与位中点，再画强制的中点跳变，最后按给定约定处理每位开始处。|图中电平翻转次数不等于数据 1 的个数；不能忽略首位之前的参考电平。
FDM、TDM、WDM、CDM|FDM 按频带划分，TDM 按时隙，WDM 按光波长，CDM 用不同码序列区分用户。|同步 TDM 的固定时隙即使无数据也可能闲置；CDM 解码常对接收叠加信号与目标用户码做归一化内积。|采用 ±1 码、正交码长 m 时，将接收向量与用户码点积再除 m，可提取该用户在理想同步下的符号。|不同用户码不只是“彼此不相同”，还需满足相应相关特性；码分正交结论有理想同步等条件。
虚电路与数据报|虚电路先建立逻辑路径，沿途可维护映射；数据报一般携完整目的地址，每个分组独立选择下一跳。|虚电路标识通常局部有效并可逐跳改写；虚电路不同于为连接独占整个物理电路。|交换机可将入端口上的 VCI 5 映射为另一出端口的 VCI 9，无须全网使用同一个编号。|不能仅凭面向连接就断言“必可靠”；可靠性还依赖相应协议机制。
组帧：字节填充与零比特填充|字节填充以转义字节区分数据中的特殊字节；零比特填充在出现连续五个 1 后插入 0，避免伪造标志序列。|零比特填充的处理对象是数据／相关帧字段，不把边界标志也递归填充；接收端按规则去掉填充。|原数据 111111 经填充成为 1111101，即五个 1 后加 0，再继续处理剩余的 1。|填充位不算原始有效载荷；连续 1 的计数规则不能误写成连续六个 1 后再填。
海明距离与检错／纠错|最小码距 dmin 的码可保证检出至多 dmin−1 位错，纠正至多 ⌊(dmin−1)/2⌋ 位错。|若要同时纠正 t 位并保证检出额外 s 位，可按具体要求利用码距界判断；普通海明码与扩展海明码能力不同。|dmin=4 可保证检测 3 位错，或纠正 1 位错；不能因此说能纠正 3 位错。|检错和纠错能力不是同一个数；海明校验位数量条件 2ʳ≥m+r+1 对应单错纠正编码的基本构造。
GBN 与 SR 的窗口限制|m 位序号，经典 GBN 接收窗口为 1，发送窗口≤2ᵐ−1；经典 SR 收发窗口相等时窗口≤2ᵐ⁻¹。|SR 接收可缓存窗口内乱序分组，只选择性重传；GBN 常丢弃失序分组，超时后重传一段未确认分组。|3 位序号：GBN 最大常用发送窗口 7；SR 等大窗口最大 4。|不等大 SR 窗口可按 Ws+Wr≤2ᵐ 判断，不能把等大窗口的上界直接用于所有变式。
令牌传递协议|只有持有令牌的站点可以按规则占用共享信道，令牌传递提供受控的发送机会。|令牌是控制信息；需处理令牌丢失、重复、持有时间和站点失效等问题。拓扑的逻辑环与物理布线未必相同。|某站无数据时可很快转发令牌；有数据也通常只能在允许的持有时间内发送。|无争用发送不等于没有控制开销，更不保证任意负载下等待时间为零。
PPP 的组帧、控制与 ARP|PPP 用于点到点链路，包括封装、LCP 和网络层配置相关 NCP；常规 PPP 通过 FCS 检错，不提供可靠重传机制。|异步链路常采用字节填充，同步链路可用比特填充；链路只有两个端点，不需以太网式 ARP 来寻找下一跳 MAC。|IP 分组经 PPP 封装给唯一对端；不需要先广播“谁有这个 IP”的 ARP 请求。|不使用 ARP 不意味着链路不需任何配置；PPP 有地址字段也不能据此认为存在以太网 MAC 地址解析过程。
VLAN 与 802.1Q|VLAN 划分二层广播域，跨 VLAN 通信通常需要三层转发。802.1Q 在常见以太帧中加入 4 B 标签。|标签含 TPID、优先级等以及 12 位 VID；VID 0 和 4095 有特殊／保留含义，不能全部当普通 VLAN 使用。|同一交换机的两个端口属于不同 VLAN，广播通常不会直接在两个 VLAN 间传播；Trunk 可承载多个 VLAN。|标签使帧长度增加但不等于 IP 首部增加 4 B；Access／Trunk 的具体无标签处理按配置与题设。
''')
add('计算机网络','网络、传输与应用', '''
SDN 控制平面与数据平面|控制平面决定转发规则，数据平面按规则处理分组；SDN 强调两者分离以及可编程控制。|控制器通常逻辑集中，物理实现可分布；交换设备仍能依据已有流表本地转发。|新流无匹配规则时可向控制器请求决策，规则下发后后续分组直接按流表转发。|不能说每个分组都一定先送到控制器，也不能把逻辑集中理解成只允许一台物理服务器。
IPv4 首部校验和与复用分用|IPv4 首部校验和只覆盖 IPv4 首部，包括选项，不覆盖 IP 数据部分；TTL 等首部变化时需相应更新。|IPv4 的 Protocol 字段识别上层协议，可向 TCP／UDP 等分用；端口号则进一步区分传输层端点。|路由器转发使 TTL 减 1，因此校验和需随之调整；TCP 校验和覆盖 TCP 首部、数据并纳入伪首部。|IP 不校验载荷不等于 TCP／UDP 不校验数据；不能把 IP 的协议号与 TCP 端口号混为一谈。
IPv6 基本首部、扩展首部与载荷长度|IPv6 基本首部固定 40 B，没有 IPv4 式首部校验和；Next Header 串联扩展首部或指向上层协议。|普通 IPv6 Payload Length 包含扩展首部和上层数据，不含 40 B 基本首部；扩展首部长度因类型而异，分片首部固定 8 B。|有效载荷长度 1200 B，其中扩展首部共 16 B，则其后上层部分为 1184 B，总 IPv6 包长为 1240 B。|不能说所有扩展首部都是 8 B；分片通常由源端做，路由器不会像 IPv4 那样替源端进行分片。巨型载荷选项另有规则。
IP 组播与分组复制|主机通过组成员管理协议表达接收意愿；组播路由依据组播转发状态，在分叉点向所需出接口复制。|IPv4 本地成员关系常用 IGMP；跨路由器的组播树由组播路由协议等维护；转发表可按 (*,G) 或 (S,G) 组织。|某组在出接口 1、3 下游有接收者，路由器仅向这两条接口转发副本，并按相应反向路径检查等规则防环。|不能说路由器向所有端口复制，也不能只靠普通单播路由表完成所有组播决策；IGMP 不负责全网组播选路。
移动 IPv4 的通信过程|移动结点保留归属地址，离开归属网络后取得转交地址并向归属代理登记；归属代理可把发往归属地址的包隧道转交。|传统模型可用外地代理转交地址或同址转交地址；回程可能直接发往通信对端，也可能采用反向隧道。|对端→归属网络→归属代理封装→转交地址→移动结点；这体现可能出现的三角路由。|移动 IPv4 的外地代理不是移动 IPv6 的无条件必备组件；不要混合两个版本的流程。
UDP 伪首部与全 0／全 1|UDP 校验覆盖伪首部、UDP 首部及数据；奇数字节时计算末尾补零，补零不作为实际数据发送。|伪首部提供源／目的 IP、协议号和 UDP 长度等信息，不是 UDP 实际首部字段。IPv4 中首部校验和全 0 表示未使用校验。|若求和取反后校验值恰为 0x0000，发送时用 0xFFFF 表示；若计算所得本来就是 0xFFFF，也可以发送全 1。|不能说“UDP 校验和不可能全 1”；IPv6 中 UDP 校验和通常必须使用，特定隧道例外不应推广成一般规则。
TCP 四类计时器|重传计时器用于确认迟迟未到的重传；持续计时器解决零窗口后窗口更新丢失；保活检测长期空闲连接；TIME-WAIT 维持相应等待状态。|零窗口探测关注接收窗口恢复；保活并非所有连接必须开启。教材 TIME-WAIT 常按 2MSL 讨论。|接收方从零窗口恢复后发出的窗口更新丢失，发送方通过持续计时器触发探测，避免一直互等。|持续计时器不是拥塞超时，保活不是重传计时器；不能把四者的触发条件和目的互换。
TCP URG 与紧急指针|URG=1 表示紧急指针字段有意义，用于标记 TCP 字节流中的紧急数据边界相关位置。|紧急指针是相对本报文段序号的偏移；边界细节存在历史实现差异，考题按给定教材／协议约定处理。|URG 与 PSH 不同：前者标记紧急机制，后者提示尽快把已接收数据交给应用。|紧急数据仍属于同一 TCP 字节流，不是建立了第二条独立传输连接，也不保证绕过网络拥塞立刻送达。
DNS 递归与迭代|递归查询要求被询问者代为取得最终答案或报告错误；迭代查询可返回下一步应询问的服务器信息。|主机到本地递归解析器常用递归；解析器向根、顶级域、权威服务器常用迭代并利用缓存。传统 DNS 常用 UDP 53，也使用 TCP 53。|解析器先问根得到顶级域服务器线索，再逐级查询，得到权威答案后缓存并回复客户端。|不能说 DNS 只用 UDP；缓存命中时不必重新走完整根到权威路径。
FTP 控制连接与数据连接|传统 FTP 服务器控制端口是 TCP 21；数据连接端口依主动／被动模式和配置而定。|经典主动模式服务器常从 TCP 20 发起数据连接；被动模式客户端连接服务器协商出的数据监听端口。|客户端发 PASV 后获得服务器选定端口，再主动连接该端口用于传文件，控制连接仍独立存在。|数据端口不是永远 20；21 是默认控制端口，服务也可配置其他端口。“始终为 21”不能脱离题设说。
SMTP、POP3、MIME 的分工|SMTP 用于提交／转发邮件；POP3 用于从邮箱服务器取信；MIME 描述非 ASCII 内容、多媒体及多部分邮件的编码格式。|发送人与接收人使用同一邮件系统时，可直接本地投递，无须一定再经过服务器间 SMTP；用户代理到服务器的提交仍需相应机制。|带附件的邮件借 MIME 描述内容类型与编码，再经 SMTP 传输；MIME 本身不是负责在两台主机间运送邮件的传输协议。|POP3 不负责发送邮件，MIME 不等于邮件加密；邮件服务器与用户代理的角色应分开。
HTTP 持续连接、Cookie 与条件请求|持续连接复用连接传多个请求／响应；Cookie 随后按域、路径等匹配规则由浏览器携带；条件请求可验证缓存是否仍有效。|服务器通过 Set-Cookie 设置浏览器状态；服务端可将 Cookie 标识映射到会话，也可采用签名等无独立会话表的设计。ETag／Last-Modified 用于缓存验证。|客户端带 If-None-Match，资源未变时服务器可回 304，客户端复用缓存正文。|Cookie 并不要求服务器必有一条对应记录；304 通常没有该资源的完整响应正文；持续连接不等于请求天然并行。
''')

add('计算机组成原理','MIPS · 格式与运算', '''
MIPS 范围、寄存器与三种指令格式|本节以经典 32 位 MIPS 整数子集为主；32 个通用寄存器，$zero 读为 0；常规指令长 32 位。|R 型：op6、rs5、rt5、rd5、shamt5、funct6；I 型：op6、rs5、rt5、imm16；J 型：op6、index26。寄存器号可参照下方速查。|add $t0,$t1,$t2 把两个源寄存器相加写入 $t0；汇编的 rd,rs,rt 顺序不同于机器字段 rs,rt,rd 的顺序。|经典 MIPS 没有 x86 式统一算术条件码 OF／CF；MIPS16、microMIPS、Release 6 等有差异，不套用本节全部假设。
add／addu／sub／subu 与立即数加法|add、sub、addi 在有符号整数溢出时产生异常；addu、subu、addiu 保留低 32 位，不产生相应整数溢出异常。|addi、addiu 都先对 16 位立即数作符号扩展；u 不能简单解释为“立即数零扩展”。基本整数子集没有独立 subi，可用加负立即数。|addiu $t0,$zero,-1 得 0xFFFFFFFF；0x7FFFFFFF+1 用 addu 得 0x80000000，而 add 触发整数溢出异常。|addu 也可用于不检查溢出的位级有符号加法；不要说发生异常时 MIPS 把 OF、CF 置成某个值。
and／or／xor／nor 与逻辑立即数|按位与、或、异或、或非不做十进制算术；andi、ori、xori 把 16 位立即数零扩展到 32 位。|nor rd,rs,$zero 实现按位取反；lui rt,imm 将立即数放到高 16 位、低 16 位清零。|lui $t0,0x1234；ori $t0,$t0,0xABCD 得 0x1234ABCD；andi $t1,$t0,0x00FF 只保留最低字节。|lui 是 I 型但不能套“所有 I 型立即数都符号扩展”；按位取反不同于算术取负。
sll／srl／sra 与可变移位|sll 左移低位补 0，srl 右移高位补 0，sra 右移高位补原符号位；移出的位丢弃。|固定移位 sll rd,rt,shamt；可变移位 sllv／srlv／srav rd,rt,rs 使用 rs 的低 5 位作为移位量。|0x80000000 右移 1：srl 得 0x40000000，sra 得 0xC0000000；sll $t0,$t1,2 可生成 4 倍字节偏移。|对负整数做 sra 不总等于向零取整除法：−3 算术右移 1 常得 −2，而整数除法向零取整得 −1。
slt／sltu／slti／sltiu|比较结果写为 0 或 1；slt／slti 用有符号比较，sltu／sltiu 用无符号比较。|slti 和 sltiu 都对 16 位立即数符号扩展；sltiu 在扩展后再按无符号数比较，结果写入 rt。|$t1=0xFFFFFFFF、$t2=1 时，slt $t0,$t1,$t2 得 1，sltu 得 0。sltiu $t0,$zero,-1 得 1。|slt 不会直接改变 PC，也不通过全局标志寄存器传结果；“u”不等于立即数零扩展。
mult／multu／div／divu 与 HI、LO|经典 mult／multu 产生 64 位乘积放 HI:LO；div／divu 把商放 LO、余数放 HI；mfhi、mflo 读出结果。|mult、div 按有符号解释源操作数，带 u 的版本按无符号解释；mthi／mtlo 可将 GPR 写入 HI／LO。不同版本的 mul 等指令需单独确认。|$t0=17、$t1=5，div $t0,$t1 后 mflo $s0 得 3，mfhi $s1 得 2；除数为零时不能推导正常商余数。|经典这些指令不能沿用 x86 OF／CF；除零与商溢出的架构行为按题目指定，不能默认总有除法异常。
''')
add('计算机组成原理','MIPS · 访存与控制流', '''
lw／sw、lb／lbu、lh／lhu、sb／sh|访存地址=基址寄存器+符号扩展的 16 位字节偏移；load 将内存读到 rt，store 把 rt 的低相应位写到内存。|lb／lh 符号扩展，lbu／lhu 零扩展；lw 读整字。经典 lw／sw 地址通常须 4 B 对齐，lh／sh 须 2 B 对齐。|lw $t0,12($s0) 在 $s0=0x10010000 时访问 0x1001000C；若字节为 0x80，lb 得 0xFFFFFF80，lbu 得 0x00000080。|sw 的 rt 是源，不是目的；偏移以字节计而不是以字计。sb／sh 不会把完整 32 位寄存器全部写入。
beq／bne 的 PC 相对分支|beq 在两源相等时分支，bne 在不等时分支；经典目标=PC+4+(signext(imm16) 左移 2)。|PC 是当前分支指令地址；偏移是相对下一条指令的有符号指令字距离。未转移的后续行为还取决于是否采用延迟槽模型。|分支在 0x00400020，目标在 0x00400010，立即数=(0x10−0x24)/4=−5，即 16 位编码 0xFFFB。|不能相对当前 PC 直接除 4；负偏移先符号扩展再左移，不是零扩展。
bltz／bgez／blez／bgtz|分别在 rs<0、rs≥0、rs≤0、rs>0 时转移，按有符号解释，常采用与 beq 同类 PC 相对目标计算。|与零比较的这些指令可以直接使用；一般寄存器间的 blt／bge 常是汇编器伪指令组合。|bltz $t0,L 可检测负数；比较 $t0<$t1 可先 slt $at,$t0,$t1，再 bne $at,$zero,L。|把伪指令展开后才统计机器指令数、代码长度和流水时间；不能把汇编每一行都当成一条机器指令。
j／jal、jr／jalr 与延迟槽|j／jal 使用伪直接目标：拼接 (PC+4) 高 4 位、index26 和 00；jr／jalr 的目标取自寄存器。|经典有延迟槽的 jal 将 PC+8 写入 $ra，jalr 通常写指定 rd（省略时常用 $ra）；教材若明确采用无延迟槽简化模型，可规定保存 PC+4。|经典 jal func 调用后以 jr $ra 返回；嵌套调用会覆盖 $ra，调用者应按约定保存仍需使用的返回位置。|j 不是完整 32 位绝对地址，也不是 PC 相对；不要把 PC+4 与 PC+8 脱离所用模型强行统一。
常见伪指令 move／li／la／nop／b|伪指令是汇编器方便写法，可能展开成一条或多条真实指令；展开方式依工具链和常量／地址范围。|move 可用 addu rd,rs,$zero；nop 常用 sll $zero,$zero,0；b 可用 beq $zero,$zero,label；li 装立即数、la 装地址。|li $t0,0x12345678 可展开 lui $t0,0x1234 与 ori $t0,$t0,0x5678；li 一个小常量可能只用一条。|la 与 lw 不同：前者获得地址，后者从地址读取数据；不要认为 li 无论常量多大都只需一条。
MIPS 调用约定、数组与函数例子|常见 o32 约定：$a0–$a3 传前四个参数，$v0–$v1 返回值，$t0–$t9 由调用者按需保存，$s0–$s7 由被调用者按需保存，$sp 管理栈。|这些是调用约定而非每条指令硬性规定。int 数组地址 A+i 常需先把索引 i 左移 2，再与基址相加。|sll $t0,$s1,2；addu $t0,$s0,$t0；lw $v0,0($t0)：假定 $s0=A、$s1=i、int 为 4 B，结果为 A[i]。|寄存器别名和保存责任不能混淆；函数修改 $s0 后若未恢复，会违反相应调用约定。
''')

def h(s): return esc(str(s),quote=True)
subjects=['数据结构','计算机组成原理','操作系统','计算机网络']
slugs=['ds','co','os','net']
base=(ROOT/'408-calculations.html').read_text()
header=base[base.index('<header'):base.index('<main')]
footer=base[base.index('<footer'):base.index('<script src="js/main.js')]
controls=base[base.index('<section class="section study-controls"'):base.index('<section class="section study-contents"')]
controls=controls.replace('共 8 条',f'共 {len(items)} 条').replace('例如：Cache 组号、TCP 窗口、读写指针','例如：MIPS addiu、文件偏移、IPv6、物理格式化')
controls=controls.replace('<button class="button" type="button" data-subject-filter="计算机组成原理"','<button class="button" type="button" data-subject-filter="数据结构" aria-pressed="false">数据结构</button><button class="button" type="button" data-subject-filter="计算机组成原理"',1)
def card(x):
    return f'''<details class="study-card glass" id="{x['id']}" data-subject="{h(x['subject'])}" data-chapter="{h(x['chapter'])}" data-tags="查漏" data-search="{h(' '.join(x.values()))}"><summary><span class="study-card-heading"><span class="study-card-title">{h(x['title'])}</span><span class="study-card-preview">{h(x['core'])}</span></span><span class="study-badges"><span class="study-badge">{'MIPS' if 'MIPS' in x['chapter'] else '查漏'}</span></span><span class="study-expand-hint" aria-hidden="true">要点</span></summary><div class="study-card-body"><section class="study-key"><h4>核心结论</h4><p>{h(x['core'])}</p></section><section class="study-detail-block"><h4>条件与过程</h4><p>{h(x['detail'])}</p></section><section class="study-detail-block study-example"><h4>例子</h4><p>{h(x['example'])}</p></section><section class="study-detail-block study-misconception"><h4>辨析边界</h4><p>{h(x['trap'])}</p></section><div class="study-mark" hidden aria-label="复习标记"><button type="button" class="button" data-mark="review" aria-pressed="false">待复习</button><button type="button" class="button" data-mark="mastered" aria-pressed="false">已掌握</button><span class="study-state-text">未标记</span><a class="button-link" href="#{x['id']}">定位链接</a></div></div></details>'''
links='''<nav class="hero-actions" aria-label="408 板块"><a class="button" href="408-handbook.html">系统知识手册</a><a class="button" href="408.html">易错辨析</a><a class="button" href="408-calculations.html">计算专项</a><a class="button primary" href="408-blindspots.html" aria-current="page">冷门考点查漏</a><a class="button" href="#mips-reference">MIPS 指令速查</a></nav>'''
hero=f'''<section class="subhero"><div class="container"><article class="subhero-card glass"><a class="back-link" href="index.html#408-study">← 返回首页</a><div class="kicker">2027 考研 408 · 查漏补缺</div><h1>冷门考点查漏</h1><p>四科 {len(items)-12} 个查漏考点 · 12 张 MIPS 专题卡 · 15 项优先检查。围绕定义、条件、过程和相近概念展开。</p><p class="study-note">“冷门”指容易遗漏或混淆，不代表真题低频或官方命题概率。按本页清单查漏，年度考试范围仍以正式大纲为准。</p>{links}</article></div></section>'''
priority_titles=['进程打开文件表、系统打开文件表与 inode','物理格式化、分区与逻辑格式化','内存映射文件与普通 I/O','异常：故障、陷阱、中止与外部中断','乘除运算电路与结果位宽','IPv6 基本首部、扩展首部与载荷长度','移动 IPv4 的通信过程','十字链表与邻接多重表','条件变量与信号量','I/O 端口独立编址与统一编址','树、森林与二叉树转换','UDP 伪首部与全 0／全 1','硬链接、软链接与文件删除','PPP 的组帧、控制与 ARP','外部排序、置换选择与败者树']
priority=[]
for n,title in enumerate(priority_titles):
    x=next(x for x in items if x['title']==title)
    label=title
    extra=''
    if n==9:
        y=next(x for x in items if x['title']=='总线定时与异步握手');extra=f' · <a href="#{y["id"]}">总线定时</a>'
    if n==13:
        for title2 in ['IP 组播与分组复制','VLAN 与 802.1Q']:
            y=next(x for x in items if x['title']==title2);extra+=f' · <a href="#{y["id"]}">{h(title2.split("与")[0])}</a>'
        label='PPP 协议'
    priority.append(f'<li><label><input type="checkbox" data-priority="p{n+1}"><span class="priority-name">{h(label)}<small>{h(x["subject"])}</small></span></label><span class="priority-links"><a href="#{x["id"]}">复习</a>{extra}</span></li>')
checklist='''<section class="section anchor-offset" id="priority"><div class="container"><article class="panel glass"><div class="section-head"><div><div class="kicker">建议顺序 · 主观优先级</div><h2>考前查漏清单</h2></div><p id="priority-count" role="status" aria-live="polite">0 / 15 已掌握</p></div><progress id="priority-progress" max="15" value="0" aria-label="15 项查漏进度"></progress><ul class="priority-list">'''+''.join(priority)+'''</ul><p class="study-note" id="priority-storage">清单进度独立于下方卡片标记，只保存在当前浏览器。</p><button class="button" id="priority-reset" type="button">重置清单进度</button><span id="priority-reset-note" role="status"></span></article></div></section>'''
directory='<section class="section study-contents" id="coverage"><div class="container"><h2 class="study-sr-only">专题目录</h2><details class="panel glass study-directory-disclosure"><summary>按科目与专题浏览</summary><div class="study-directory">'
groups=''
for subject,slug in zip(subjects,slugs):
    rows=[x for x in items if x['subject']==subject];chapters=list(dict.fromkeys(x['chapter'] for x in rows))
    directory+=f'<article class="study-directory-subject"><h3>{subject}<span>{len(rows)} 条</span></h3><ul>'
    groups+=f'<section class="section anchor-offset study-subject" id="{slug}" data-group-subject="{subject}"><div class="container"><div class="section-head"><div><div class="kicker">408 · {slug.upper()}</div><h2>{subject}</h2></div><p class="section-intro">{len(rows)} 个考点</p></div>'
    for n,ch in enumerate(chapters):
        id=f'{slug}-chapter-{n+1}'
        directory+=f'<li><a href="#{id}">{h(ch)}</a></li>'
        groups+=f'<div class="study-chapter" id="{id}" data-group-chapter="{h(ch)}"><h3>{h(ch)}</h3><div class="study-card-list">'+''.join(card(x) for x in rows if x['chapter']==ch)+'</div></div>'
    directory+='</ul></article>';groups+='</div></section>'
directory+='</div></details></div></section>'

# Keep the instruction reference independent of collapsed cards and filters.
instructions=[
('算术','add / addu','rd, rs, rt','rd ← rs + rt','R','add 检测有符号溢出；addu 不触发该异常'),
('算术','sub / subu','rd, rs, rt','rd ← rs − rt','R','减数是 rt；sub 检测溢出'),
('算术','addi / addiu','rt, rs, imm','rt ← rs + signext(imm16)','I','两者均符号扩展；addiu 不触发整数溢出异常'),
('逻辑','and / or / xor / nor','rd, rs, rt','按位与／或／异或／或非','R','nor 是对 (rs OR rt) 整体取反'),
('逻辑','andi / ori / xori','rt, rs, imm','对 rs 和 zeroext(imm16) 做逻辑操作','I','立即数零扩展'),
('常量','lui','rt, imm','rt ← imm16 接 16 个 0','I','可配 ori 拼接 32 位常量'),
('移位','sll / srl / sra','rd, rt, shamt','左移／逻辑右移／算术右移','R','固定移位量 5 位，范围 0–31'),
('移位','sllv / srlv / srav','rd, rt, rs','移位量取 rs[4:0]','R','被移位数是 rt'),
('比较','slt / sltu','rd, rs, rt','rd ← (rs < rt ? 1 : 0)','R','有符号／无符号比较'),
('比较','slti / sltiu','rt, rs, imm','rt ← 比较结果 0／1','I','两者先符号扩展立即数，sltiu 再无符号比较'),
('乘除','mult / multu','rs, rt','HI:LO ← 64 位乘积','R','有符号／无符号'),
('乘除','div / divu','rs, rt','LO ← 商，HI ← 余数','R','经典 HI／LO 模型；特殊输入按架构'),
('乘除','mul','rd, rs, rt','rd ← 乘积的低 32 位','R','经典 MIPS32 的实际指令；HI／LO 内容不可依赖'),
('乘除','mfhi / mflo','rd','rd ← HI／LO','R','把结果移到通用寄存器'),
('乘除','mthi / mtlo','rs','HI／LO ← rs','R','把通用寄存器内容写入 HI／LO'),
('访存','lw / sw','rt, offset(base)','读／写 32 位字','I','地址按字节算；经典实现要求 4 B 对齐'),
('访存','lb / lbu','rt, offset(base)','读 8 位，符号／零扩展','I','有符号字节 0x80 扩为 0xFFFFFF80'),
('访存','lh / lhu','rt, offset(base)','读 16 位，符号／零扩展','I','经典实现要求 2 B 对齐'),
('访存','sb / sh','rt, offset(base)','写 rt 的低 8／16 位','I','不对内存执行“符号扩展写入”'),
('分支','beq / bne','rs, rt, label','相等／不等则分支','I','目标基准是 PC+4，偏移字段左移 2'),
('分支','bltz / bgez','rs, label','rs<0／rs≥0 则分支','I','有符号比较'),
('分支','blez / bgtz','rs, label','rs≤0／rs>0 则分支','I','与零比较'),
('跳转','j / jal','label','跳转／跳转并链接','J','目标用 PC+4 高 4 位拼接；jal 保存返回位置'),
('跳转','jr','rs','跳到 rs 所给地址','R','jr $ra 常用于返回'),
('跳转','jalr','rd, rs','跳到 rs 并保存返回位置到 rd','R','省略 rd 常表示 $ra；以汇编器规定为准'),
('伪指令','move / li / la / b','依指令','移动／装常量／取地址／无条件分支','伪','展开条数随工具链及操作数而变'),
('空操作','nop','无','常编码为 sll $zero,$zero,0','汇编写法','空操作仍是一条占 4 B 的经典指令'),
('异常','syscall / break','可有 code','触发系统调用／断点异常','特殊','具体服务号和传参方式由 OS／模拟器约定')]
table='<div class="study-table-wrap" tabindex="0" aria-label="MIPS 常见指令表，可横向滚动"><table class="study-table"><caption>MIPS 常见指令与伪指令 · 同组助记符合并展示</caption><thead><tr>'+''.join('<th scope="col">'+h(s)+'</th>' for s in ['类别','助记符','操作数格式','操作含义','类型','易错点'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+h(c)+'</td>' for c in row)+'</tr>' for row in instructions)+'</tbody></table></div>'
registers=[('$zero','$0','恒为 0'),('$at','$1','汇编器常用临时寄存器'),('$v0–$v1','$2–$3','返回值'),('$a0–$a3','$4–$7','参数'),('$t0–$t7','$8–$15','临时值'),('$s0–$s7','$16–$23','被调用者按需保存'),('$t8–$t9','$24–$25','临时值'),('$k0–$k1','$26–$27','内核保留'),('$gp','$28','全局指针'),('$sp','$29','栈指针'),('$fp / $s8','$30','帧指针／保存寄存器'),('$ra','$31','返回地址')]
regtable='<div class="study-table-wrap"><table class="study-table"><caption>常见 o32 寄存器别名与用途（调用约定）</caption><thead><tr><th scope="col">别名</th><th scope="col">编号</th><th scope="col">用途</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+h(c)+'</td>' for c in row)+'</tr>' for row in registers)+'</tbody></table></div>'
formats=''.join('<div class="mips-format"><strong>'+name+'</strong><div class="mips-bits" style="--columns:'+cols+'">'+''.join(f'<span>{field}<small>{width} bit</small></span>' for field,width in fields)+'</div></div>' for name,cols,fields in [('R 型','6fr 5fr 5fr 5fr 5fr 6fr',[('op',6),('rs',5),('rt',5),('rd',5),('shamt',5),('funct',6)]),('I 型','6fr 5fr 5fr 16fr',[('op',6),('rs',5),('rt',5),('imm',16)]),('J 型','6fr 26fr',[('op',6),('index',26)])])
steps=[('读懂题设','beq 位于 0x00400020，目标 0x00400010；需要求 16 位立即数字段。'),('定位基准','分支基准为 PC+4=0x00400024。'),('计算字节差','目标 − 基准 = 0x00400010 − 0x00400024 = −20 B。'),('换算指令字偏移','−20 / 4 = −5，16 位补码是 0xFFFB。'),('反代验证','符号扩展 0xFFFB 得 −5，再左移 2 得 −20；0x00400024−20=0x00400010。')]
stephtml='<div id="mips-stepper" class="mips-stepper" hidden><p id="mips-step-count" class="study-note"></p><h4 id="mips-step-title"></h4><p id="mips-step-text" aria-live="polite"></p><div class="hero-actions"><button class="button" id="mips-prev" type="button">上一步</button><button class="button primary" id="mips-next" type="button">下一步</button><button class="button" id="mips-restart" type="button">重来</button></div></div><details class="study-recall"><summary>查看完整计算过程</summary><ol>'+''.join('<li><strong>'+h(a)+'：</strong>'+h(b)+'</li>' for a,b in steps)+'</ol></details>'
calculator='''<form id="mips-address-form"><div class="study-filter-grid"><label>当前 PC（16 进制）<input id="mips-pc" value="0x00400020" required spellcheck="false"></label><label>目标地址（16 进制）<input id="mips-target" value="0x00400010" required spellcheck="false"></label></div><button class="button" type="submit">计算分支立即数</button><p id="mips-address-result" role="status" aria-live="polite"></p></form>'''
mips='''<section class="section anchor-offset" id="mips-reference"><div class="container"><div class="section-head"><div><div class="kicker">计组 · 指令格式与机器级程序</div><h2>MIPS 常见指令速查</h2></div><p class="section-intro">经典 32 位整数子集</p></div><article class="panel glass"><p>先认操作数，再看扩展方式与结果去向，最后计算访存／分支地址。延迟槽、ABI 与 ISA 版本有区别时，以题设为准。</p><div class="mips-formats">'''+formats+'</div>'+table+regtable+'<h3>一步一步：负偏移分支</h3>'+stephtml+'<h3>换一组地址试算</h3>'+calculator+'''<p class="study-note">参考：<a href="https://cgi.cse.unsw.edu.au/~cs1521/26T2/resources/MIPS32-II-r5.04.pdf" target="_blank" rel="noopener noreferrer">MIPS Architecture For Programmers · Volume II-A · Revision 5.04</a>。本页为复习整理，经典延迟槽模型的链接地址与无延迟槽教学模型分别说明。</p></article></div></section>'''
contrasts=[('缺页／地址越界','缺页：地址合法但页面暂不在内存；越界：地址不属于允许访问的范围。权限错误又是另一种保护问题。'),('中断／进程切换','处理完中断可返回原任务；是否调度和切换，取决于就绪状态、优先级和调度时机。'),('硬链接／软链接','硬链接与原名共享 inode，软链接保存路径且有自己的 inode。'),('缓冲／缓存','缓冲侧重协调传输单位与速度，缓存侧重复用已有副本以减少访问；实际机制可兼具两种作用。'),('物理／逻辑格式化','前者建立介质的底层组织，后者建立文件系统；分区划分逻辑区域，三者分开判断。')]
contrasttable='<div class="study-table-wrap"><table class="study-table"><caption>操作系统五组易混概念</caption><thead><tr><th>概念</th><th>判断边界</th></tr></thead><tbody>'+''.join('<tr><td>'+h(a)+'</td><td>'+h(b)+'</td></tr>' for a,b in contrasts)+'</tbody></table></div>'
review='''<section class="section anchor-offset" id="review-method"><div class="container"><article class="panel glass study-reference"><div class="kicker">辨析方法</div><h2>定义 → 条件 → 过程 → 区别</h2>'''+contrasttable+'''<p>遇到“总是”“一定”“仅”“必须”，先检查实现模型、指令语义、接口约定与适用范围。能用一个反例推翻绝对说法，比只背结论更可靠。</p><p>建议依次排查操作系统文件与 I/O、网络协议细节、计组硬件控制、数据结构特殊存储。保留 Cache、PV、分页计算和算法设计的主线复习时间。</p><p>结合各卡片的例子反查概念，再尝试改变题设中的一个条件，判断原结论是否仍成立。</p></article></div></section>'''
body=hero+checklist+controls+directory+'<p id="study-empty" class="container study-empty" hidden>没有匹配内容，请重置筛选或减少关键词。</p>'+mips+groups+review
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0f"><title>408 · 冷门考点查漏与 MIPS · True Path M</title><meta name="description" content="2027 考研 408 四科查漏清单、重点辨析与 MIPS 常见指令。"><link rel="canonical" href="https://1956799.xyz/408-blindspots.html"><link rel="icon" href="favicon.svg" type="image/svg+xml"><script src="js/theme.js?v=20260909-15"></script><link rel="stylesheet" href="css/style.css?v=20261106-document-tools-1"><link rel="stylesheet" href="css/408.css?v=20261105-separate-1"><link rel="stylesheet" href="css/408-blindspots.css?v=20261108-1"></head><body data-page="study" data-export-mode="print" class="study408 blindspots408"><a class="skip-link" href="#main">跳到主要内容</a><div class="site-bg" aria-hidden="true"></div><div class="noise" aria-hidden="true"></div>'''+header+'<main id="main">'+body+'</main>'+footer+'''<script src="js/main.js?v=20261108-blindspots-1" defer></script><script src="js/408-blindspots.js?v=20261108-1" defer></script><script src="js/408-blindspots-extras.js?v=20261108-1" defer></script></body></html>'''
(ROOT/'408-blindspots.html').write_text(html)
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data/408-blindspots.json').write_text(json.dumps(dict(items=items,priority=priority_titles,steps=steps,instructions=instructions),ensure_ascii=False,indent=2)+'\n')
js=(ROOT/'js/408.js').read_text().replace('const MARK_LIMITS = { k: 239, c: 8 };',f'const MARK_LIMITS = {{ k: {len(items)}, c: 0 }};').replace('true-path-408-marks-v1','true-path-408-blindspots-marks-v1').replace('true-path-408-mark-v2-','true-path-408-blindspots-mark-v1-')
(ROOT/'js/408-blindspots.js').write_text(js)
print(f'Built {len(items)} cards: '+', '.join(f'{s} {sum(x["subject"]==s for x in items)}' for s in subjects))
