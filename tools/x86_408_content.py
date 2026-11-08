"""IA-32 study supplement: Intel syntax, with AT&T comparisons and original examples."""
X86_CHAPTERS=[('x86 · 数据、运算与标志', '''
x86 范围、寄存器与操作数顺序|本节以 IA-32 的 32 位整数指令为主，默认采用 Intel 语法：目的在前、源在后；另列 AT&T 对照。|EAX、EBX、ECX、EDX、ESI、EDI、EBP、ESP 是常见 32 位通用寄存器；AX 是 EAX 的低 16 位，AL／AH 分别是 AX 的低／高 8 位。|Intel：mov eax,ebx；AT&T：movl %ebx,%eax。两者都把 EBX 的内容复制给 EAX。|x86 常规指令为变长编码，不能按 MIPS 一律加 4；64 位模式下 RAX／RSP、调用约定及写 EAX 的零扩展规则须另辨。
MOV、MOVSX、MOVZX 与位宽|MOV 复制位模式，通常不改变算术标志；MOVSX 扩展符号位，MOVZX 高位补 0。|一般 MOV 的两操作数宽度相同；不同宽度需显式扩展。普通整数 MOV 不支持内存到内存直接复制，串操作 MOVS 是另一类指令。|若内存字节为 0x80：movsx eax,BYTE PTR [esi] 得 0xFFFFFF80；movzx 得 0x00000080；mov al,0x80 只改 EAX 的低 8 位。|MOV 不会因为复制负数就更新 SF；写 AL／AX 不会把 EAX 剩余高位自动清零。64 位模式写 EAX 清 RAX 高 32 位，是另一个规则。
LEA 与基址＋变址×比例＋位移|32 位常见有效地址可写成 base+index×scale+disp，scale 取 1、2、4、8；LEA 只计算该表达式的地址值，不读取所指内存。|一般 32 位 SIB 寻址不能把 ESP 用作 index；内存中的最终访问地址还涉及分段／分页。LEA 不改变算术标志。|EBX=0x1000、ECX=3：lea eax,[ebx+ecx*4+8] 得 0x1014；mov eax,[ebx+ecx*4+8] 则读取该地址的 4 B 内容。|方括号在 LEA 中描述地址表达式，不代表实际取内存；LEA 也可用作不改标志的某些加法／常数倍运算。
ADD、SUB、ADC、SBB 的进位与借位|ADD／SUB 更新 CF、OF、SF、ZF 等；ADC 把旧 CF 加进去，SBB 把旧 CF 作为借位再减去。|无符号加法看 CF，有符号越界看 OF；x86 的 SUB 在发生无符号借位时置 CF。ADC／SBB 常用于多字长运算。|8 位 0xFF+1 得 0：CF=1、OF=0、ZF=1；0x7F+1 得 0x80：CF=0、OF=1、SF=1。|同一位模式可同时按有符号／无符号解释，不能只看 SF 判定数学正负；ADD 置 OF 不等于自动像 MIPS add 一样触发整数溢出异常。
INC、DEC、NEG、NOT 的标志差异|INC／DEC 改变结果相关的算术标志但保留 CF；NEG 求补码相反数，NOT 逐位取反且不改标志。|NEG 相当于 0−操作数：原操作数非 0 时 CF=1；最小有符号数取负不可表示，OF=1。INC／DEC 仍会影响 OF。|AL=0x7F、旧 CF=1，inc al 得 0x80，OF=1 且 CF 仍为 1；AL=0x80 时 neg al 结果仍为 0x80，OF=1。|INC 不完全等价于 ADD 1，关键差别是 CF；NOT 不等于 NEG，也不按结果重算 ZF／SF。
CMP、TEST 与不写回结果|CMP 按目的−源计算标志但不保存差；TEST 按位与计算标志但不保存与结果。|TEST 清 CF、OF，按与结果设置 SF、ZF、PF，AF 未定义；CMP 的算术标志与对应 SUB 一致。之后的 Jcc／SETcc 读取这些标志。|cmp eax,ebx 后 JE 检查相等；test eax,eax 后 JZ 检查 EAX 是否为 0；两条检查指令都不修改 EAX。|CMP 不是设置一个“大小标志”；同一组标志供有符号与无符号条件分别解释。TEST 不能用来一般性判断两数大小。
AND、OR、XOR 与逻辑标志|AND／OR／XOR 写回按位结果，CF=OF=0，SF／ZF／PF 按结果更新，AF 未定义。|xor eax,eax 是常见清零写法，也会改变标志；or eax,eax 保留 EAX 位模式但更新标志。NOT 则不改标志。|and eax,0xFF 保留最低字节；xor eax,eax 得 0 并置 ZF=1、SF=0、CF=OF=0。|逻辑操作清 CF／OF 是特定指令语义，不能推广为所有非加减指令都清标志；AF 未定义不等于 AF=0。
SHL／SAL、SHR、SAR 与旋转|SHL 与 SAL 是同一左移操作；SHR 逻辑右移高位补 0，SAR 算术右移补原符号位。ROL／ROR 旋转，RCL／RCR 把 CF 也纳入旋转。|非零有效移位次数时，CF 通常为最后移出的位；移位 OF 只在有效次数为 1 时有定义，次数为 0 时相关标志不变。32 位传统移位计数常取低 5 位。|AL=0x80：shr al,1 得 0x40、OF=1；sar al,1 得 0xC0、OF=0。SHL 1 位时 OF=结果最高位异或 CF。|不要用多位移位后的 OF 判溢出；8／16 位操作数的超宽移位还涉及 CF 未定义边界。SAR 对负数的舍入方向与 IDIV 向零取整不同。
'''),('x86 · 乘除、分支与调用', '''
MUL 与 IMUL：隐含操作数及溢出|单操作数 MUL 做无符号乘法，IMUL 做有符号乘法；32 位形式都用 EAX 乘显式源，完整结果写 EDX:EAX。|MUL 的高半部非 0 时 CF=OF=1，否则均为 0；IMUL 的完整结果不能由低半部符号扩展得到时 CF=OF=1。SF／ZF／AF／PF 未定义。|EAX=0xFFFFFFFF、ECX=2：mul ecx 得 0x00000001:FFFFFFFE，CF=OF=1；单操作数 imul ecx 按 −1×2 得 0xFFFFFFFF:FFFFFFFE，CF=OF=0。|两／三操作数 IMUL 把截断结果写到显式目的寄存器，不自动写 EDX:EAX；不能把 MUL 的“高半部是否为零”判据套到 IMUL。
DIV、IDIV 与 CDQ：商、余数和异常|32 位 DIV／IDIV 的被除数是 EDX:EAX，显式源是除数；商写 EAX，余数写 EDX。DIV 无符号，IDIV 有符号。|若被除数本来只是一个 32 位无符号数，通常先 xor edx,edx；有符号数常先 CDQ，把 EAX 的符号扩展到 EDX:EAX。除数为 0 或商超出目的范围触发 #DE。|EAX=−17，cdq 后 idiv ecx（ECX=5），商为 −3、余数为 −2；余数绝对值小于除数绝对值，非零时与被除数同号。|DIV／IDIV 后 CF、OF、SF、ZF、AF、PF 均未定义，不能说溢出时 CF／OF 置 0／1；CDQ 不执行除法，也不改变算术标志。
Jcc：有符号与无符号条件跳转|JE／JZ 看 ZF=1，JNE／JNZ 看 ZF=0；无符号大小用 JA／JAE／JB／JBE，有符号大小用 JG／JGE／JL／JLE。|CMP a,b 后：JA 为 CF=0 且 ZF=0，JB 为 CF=1；JG 为 ZF=0 且 SF=OF，JL 为 SF≠OF。Jcc 本身不修改标志。|AL=0xFF、BL=1，cmp al,bl 后：无符号 255>1 可用 JA 转移；有符号 −1<1 可用 JL 转移，两种判断可同时成立。|JG 不等于只看 SF=0，JL 不等于只看 SF=1；要合并 OF 还原有符号数学比较。中间若有改标志的指令，分支读到的是新标志。
JMP、LOOP、JECXZ、SETcc、CMOVcc|JMP 无条件改变控制流；常见 IA-32 LOOP 先使 ECX 减 1，再按非 0 决定跳转，且不改变算术标志。JECXZ 直接检查 ECX 是否为 0。|LOOPE／LOOPNE 还检查旧 ZF；SETcc 把条件结果 0／1 写入一个字节；CMOVcc 条件成立才把源值写到目的寄存器。具体编码范围依指令。|sete al 只写 AL；若想使整个 EAX 变成 0／1，可再 movzx eax,al。jecxz 不会先把 ECX 减 1。|LOOP 的计数寄存器受地址大小影响，本节按 32 位 ECX；不要把 LOOP 当成会修改 ZF 的 DEC＋JNZ 在所有情形下等价替换。
PUSH、POP 与 ESP 的变化|本节默认普通 32 位栈操作：PUSH 先使 ESP 减 4 再写入栈顶；POP 先从旧栈顶读取再调整栈指针。|通常压入／弹出的是双字；16 位操作数等变体的步长不同。PUSH imm8 的立即数会先符号扩展到相应操作数宽度。普通 PUSH／POP 不改变算术标志。|ESP=0x1000，push eax 后 ESP=0x0FFC；pop ebx 将栈顶值取到 EBX，正常情况下 ESP 回到 0x1000。|POP ESP 属于需单独分析的情况：目标写入 ESP 后，最终 ESP 不是机械地旧值＋4。不要把所有模式的 PUSH／POP 步长都说成 4。
CALL、RET、LEAVE 与函数栈帧|普通 32 位近 CALL 把下一条指令地址压栈后转移；RET 从栈顶取回返回地址；LEAVE 可用于撤销基于 EBP 的栈帧。|常见序言 push ebp; mov ebp,esp; sub esp,N。常见结尾 leave; ret，其中 LEAVE 相当于先恢复 ESP 到 EBP，再弹出旧 EBP；参数位置依调用约定。|采用常见 32 位 cdecl 栈传参和上述序言时，[ebp] 是保存的旧 EBP，[ebp+4] 是返回地址，[ebp+8] 可为首个参数。|返回地址不是无条件“当前 EIP+4”，必须按变长指令长度定位；RET n 在取回地址后还调整栈，不是跳到地址 n。64 位 ABI 不直接套本例。
串操作、方向标志与端口 I/O|MOVSB 从源串向目的串搬一个字节，STOSB 把 AL 写到目的串；REP 可按计数重复；CLD 清 DF、STD 置 DF 以控制递增／递减方向。|按常见 32 位地址大小，MOVSB 使用 ESI／EDI，REP 使用 ECX。IN／OUT 访问独立端口地址空间，常见端口操作数为 imm8 或 DX，数据用 AL／AX／EAX。|cld; rep movsb 在通常模型下按地址递增复制 ECX 个字节；in al,dx 从 DX 所指定端口读一个字节。|串 MOVSB 与 SIMD 标量 MOVSD 等同名写法需看上下文；I/O 指令受权限限制，普通内存 MOV 不等于执行端口 IN／OUT。
x86 与 MIPS：机器级阅读的边界|两者都要看操作数宽度与指令语义；经典 MIPS 常见三操作数与 load/store，x86 常见两操作数以及显式内存操作数。|x86 CMP→Jcc 使用条件码；经典 MIPS 可用寄存器比较分支或 SLT 结果。MIPS 常规指令固定 4 B，x86 变长；调用返回地址保存方式也不同。|x86 add eax,[ebx] 可读取内存并与 EAX 相加；经典 MIPS 通常先 lw 到寄存器再 add。x86 CALL 压返回地址，经典 MIPS JAL 常写 $ra。|这些是本页选取子集的对照，不代表每条 x86 都有两个操作数、每条 MIPS 都有三个；x86 普通 ADD 的 OF 与 MIPS ADD 的异常不是同一机制。
''')]

INSTRUCTIONS=[
('传送','MOV','mov eax,[ebx+4]','EAX ← 该地址的双字','不变','目的在前，通常不能内存到内存'),
('扩展','MOVSX / MOVZX','movsx eax,BYTE PTR [esi]','读入小宽度数并符号／零扩展','不变','先确定源宽度'),
('地址','LEA','lea eax,[ebx+ecx*4+8]','EAX ← 有效地址表达式值','不变','不读取地址指向的数据'),
('算术','ADD / SUB','sub eax,ebx','EAX ← EAX−EBX','CF OF SF ZF AF PF 更新','SUB 的 CF=1 表示无符号借位'),
('多字长','ADC / SBB','adc edx,0','EDX ← EDX+旧 CF','算术标志更新','带入的是执行前的 CF'),
('增减','INC / DEC','inc eax','EAX ← EAX+1','保留 CF，其余相关算术标志更新','与 ADD 1 不完全等价'),
('取负','NEG','neg eax','EAX ← 0−EAX','算术标志更新','最小有符号数取负时 OF=1'),
('取反','NOT','not eax','逐位取反','不变','与 NEG 不同'),
('逻辑','AND / OR / XOR','and eax,0xFF','写回按位运算结果','CF=OF=0；SF ZF PF 更新；AF 未定义','xor eax,eax 清零并改标志'),
('比较','CMP','cmp eax,ebx','仅计算 EAX−EBX 的标志','与 SUB 一致','不写回差值'),
('测试','TEST','test eax,eax','仅计算按位与的标志','CF=OF=0；SF ZF PF 更新；AF 未定义','不写回与结果'),
('移位','SHL / SAL / SHR / SAR','sar eax,1','左移／逻辑右移／算术右移','0 次不变；OF 只在有效次数 1 时有定义','SHL 与 SAL 同义；SAR 保留符号'),
('旋转','ROL / ROR / RCL / RCR','rcl eax,1','循环移动比特；带 C 的含 CF','不改 SF ZF AF PF；CF／OF 按次数与形式','旋转不是补 0 移位'),
('无符号乘','MUL','mul ecx','EDX:EAX ← EAX×ECX','CF=OF=(高半部非 0)，其他算术标志未定义','单操作数，完整结果双倍宽度'),
('有符号乘','IMUL','imul eax,ecx,5','EAX ← ECX×5 的低 32 位','CF=OF 表示截断后的有符号结果不可表示；其余未定义','单操作数形式才隐含写 EDX:EAX'),
('除法','DIV / IDIV','idiv ecx','EDX:EAX÷ECX，商 EAX、余数 EDX','CF OF SF ZF AF PF 未定义','除零／商溢出触发 #DE'),
('符号扩展','CBW / CWDE / CWD / CDQ','cdq','分别 AL→AX、AX→EAX、AX→DX:AX、EAX→EDX:EAX','不变','CDQ 为有符号除法准备高半部'),
('无条件分支','JMP','jmp L','跳转到目标','不变','相对位移按字节，以后继指令地址为基准'),
('相等分支','JE / JZ / JNE / JNZ','je L','按 ZF 决定跳转','不变','JE=JZ；JNE=JNZ'),
('无符号分支','JA / JAE / JB / JBE','ja L','按 CF、ZF 判断无符号大小','不变','CMP 后解释为目的与源比较'),
('有符号分支','JG / JGE / JL / JLE','jl L','按 SF、OF、ZF 判断有符号大小','不变','JL 检查 SF≠OF'),
('标志分支','JO / JNO / JS / JNS','jo L','检查 OF 或 SF','不变','JS 本身不等于一般有符号小于'),
('计数分支','LOOP / LOOPE / LOOPNE / JECXZ','loop L','减计数再判断；JECXZ 直接检查零','不变','LOOPE／LOOPNE 还读取旧 ZF'),
('条件结果','SETcc / CMOVcc','setl al','SETcc 写字节 0／1；CMOVcc 条件传送','不变','SETcc 不会清目的寄存器的其他位'),
('栈','PUSH / POP','push eax','普通 32 位形式压／弹 4 B','普通形式不变','栈向低地址增长；特殊目的需单独分析'),
('调用','CALL / RET','call f','保存／恢复返回位置并转移','普通近形式不改算术标志','CALL 压下一条指令地址，RET 可另清理参数'),
('栈帧','LEAVE','leave','ESP←EBP；弹出旧 EBP（本页 32 位模型）','不变','不是简单跳转指令'),
('串处理','MOVSB / STOSB / REP','rep movsb','按源／目的指针处理串并更新指针、计数','MOVSB／STOSB 不改算术标志','按 DF 决定指针递增／递减'),
('方向','CLD / STD','cld','DF←0／DF←1','只修改 DF','不把 CF 当方向标志'),
('端口','IN / OUT','in al,dx','在 AL／AX／EAX 与 I/O 端口间传送','不变','端口用 imm8 或 DX，受权限约束'),
('交换／空操作','XCHG / NOP','xchg eax,ebx','交换／空操作','不变','基本 XCHG 交换两者，不是单向复制'),
('中断','INT / IRET','int n','进入中断服务／从相应中断栈帧返回','依模式和类型处理控制标志','IRET 与普通 RET 保存／恢复内容不同')]

JUMPS=[('JE / JZ','ZF=1','相等'),('JNE / JNZ','ZF=0','不等'),('JA / JNBE','CF=0 且 ZF=0','无符号 >'),('JAE / JNB / JNC','CF=0','无符号 ≥'),('JB / JNAE / JC','CF=1','无符号 <'),('JBE / JNA','CF=1 或 ZF=1','无符号 ≤'),('JG / JNLE','ZF=0 且 SF=OF','有符号 >'),('JGE / JNL','SF=OF','有符号 ≥'),('JL / JNGE','SF≠OF','有符号 <'),('JLE / JNG','ZF=1 或 SF≠OF','有符号 ≤'),('JO / JNO','OF=1／OF=0','有符号溢出标志'),('JS / JNS','SF=1／SF=0','结果符号位')]

def build_reference(h):
    def table(headers,rows,caption):
        return '<div class="study-table-wrap" tabindex="0" aria-label="'+h(caption)+'，可横向滚动"><table class="study-table"><caption>'+h(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+h(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+h(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
    syntax=[('操作数顺序','mov eax,ebx','movl %ebx,%eax'),('立即数','mov eax,5','movl $5,%eax'),('间接访存','mov eax,[ebx]','movl (%ebx),%eax'),('基址＋变址＋位移','mov eax,[ebx+ecx*4+8]','movl 8(%ebx,%ecx,4),%eax'),('地址计算','lea eax,[ebx+ecx*4+8]','leal 8(%ebx,%ecx,4),%eax')]
    registers=[('EAX / AX / AH / AL','32／16／8／8 位重叠视图','乘除法与常见返回值约定'),('EBX / ECX / EDX','32 位通用寄存器','ECX 常用于计数；EDX 参与宽乘除'),('ESI / EDI','32 位通用寄存器','常见串操作源／目的指针'),('EBP / ESP','32 位通用寄存器','常用于帧指针／栈指针'),('EIP / EFLAGS','指令指针／标志寄存器','与通用寄存器的访问方式不同'),('RAX / RSP 等','64 位模式扩展视图','本页例题主体仍按 IA-32；写 EAX 会清 RAX 高 32 位')]
    compare=[('例子','x86（Intel）','经典 MIPS'),('加法','add eax,ebx：目的也是源','add $t0,$t1,$t2：常用三操作数'),('访存','mov eax,[ebx]；add eax,[ebx]','通常用 lw／sw 访存，再在寄存器上算'),('条件分支','cmp＋Jcc 读取 EFLAGS','beq／bne 或 slt 结果'),('指令长度','变长，按实际字节数定位后继','本页常规指令固定 4 B'),('调用返回','近 CALL 将返回地址压栈','经典 JAL 将返回地址写入 $ra'),('普通整数溢出','ADD 设置 OF，通常不因此直接陷入','ADD 有符号溢出可触发异常；ADDU 不触发')]
    return '''<section class="section anchor-offset" id="x86-reference"><div class="container"><div class="section-head"><div><div class="kicker">计组 · 机器级代码与标志位</div><h2>x86 常见指令速查</h2></div><p class="section-intro">IA-32 · Intel 语法 · AT&amp;T 对照</p></div><article class="panel glass"><p>默认采用 32 位 IA-32 与 Intel 的“目的，源”顺序。先确认位宽、显式／隐含操作数，再判断标志变化与跳转条件；64 位模式和调用约定有差别时按题设。</p>'''+table(['类别','助记符','Intel 示例','含义','标志影响','易错点'],INSTRUCTIONS,'x86 常见指令表')+'''<h3>Intel 与 AT&amp;T 语法对照</h3><p>AT&amp;T 常写“源，目的”，寄存器前加 %、立即数前加 $，常以 b／w／l／q 标示 8／16／32／64 位。以下是所列常见指令的对应写法，不能把操作数换序规则无条件推广到每一条特殊指令。</p>'''+table(['项目','Intel','AT&T'],syntax,'同一操作的两种写法')+table(['寄存器','位宽／类别','用途与条件'],registers,'常见寄存器与重叠关系')+'''<h3>CMP 后的条件跳转</h3><p>表中大小关系按 CMP 目的,源 解释。有符号关系必须结合 OF；Jcc 不重新执行比较，也不修改这些标志。</p>'''+table(['指令／别名','成立条件','CMP 后的含义'],JUMPS,'条件跳转与标志位')+'''<section class="x86-caution"><h4>乘除法最容易混淆的三条</h4><ul><li>MUL：按高半部是否为 0 决定 CF／OF。</li><li>IMUL：按截断结果能否符号扩展回完整乘积决定 CF／OF。</li><li>DIV／IDIV：算术标志未定义；除零或商放不下触发 #DE。</li></ul></section><h3>试算：8 位运算、标志与跳转</h3><p class="study-note">用 AL／BL 的 8 位模型观察同一位模式的两种解释。输入范围 −128～255；非负数也可写成 0x00～0xFF。</p><form id="x86-flags-form" hidden><div class="study-filter-grid"><label>运算<select id="x86-operation"><option>ADD</option><option>SUB</option><option>CMP</option><option>TEST</option></select></label><label>目的操作数 A<input id="x86-a" value="0x7F" required spellcheck="false"></label><label>源操作数 B<input id="x86-b" value="1" required spellcheck="false"></label></div><button class="button" type="submit">计算标志与跳转条件</button><div id="x86-flags-result" role="status" aria-live="polite"></div></form><noscript><p>未启用脚本时可直接阅读下方完整例子与卡片。</p></noscript><details class="study-recall"><summary>完整例子：CMP AL,BL 后为何 JA 与 JL 可以同时成立？</summary><ol><li>AL=0xFF、BL=1：无符号解释为 255 和 1，有符号解释为 −1 和 1。</li><li>8 位相减得到 0xFE：CF=0、ZF=0、SF=1、OF=0，两个操作数保持不变。</li><li>JA 要求 CF=0 且 ZF=0，因此满足无符号“大于”。</li><li>JL 要求 SF≠OF，因此也满足有符号“小于”。这两种解释并不矛盾。</li></ol></details><h3>和 MIPS 放在一起记</h3>'''+table(compare[0],compare[1:],'x86 与经典 MIPS 对照')+'''<p class="study-note">参考：<a href="https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html" target="_blank" rel="noopener noreferrer">Intel 64 and IA-32 Software Developer’s Manuals</a>（指令语义以 Volume 2、执行模式与题设为准）。</p></article></div></section>'''
