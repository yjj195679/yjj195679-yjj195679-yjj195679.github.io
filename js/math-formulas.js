(() => {
  'use strict';

  const formulas = [];
  const add = (subject, chapter, rows) => rows.forEach((row) => {
    const [title, formula, condition, pitfall, level = '核心'] = row;
    formulas.push({ id: `m${String(formulas.length + 1).padStart(3, '0')}`, subject, chapter, title, formula, condition, pitfall, level });
  });

  add('高等数学', '函数、极限与连续', [
    ['复合函数与反函数导数', 'y=f(u), u=g(x) ⇒ y=f(g(x))\n若 y=f(x) 可逆：g′(y)=1/f′(x)', '反函数导数要求 f′(x)≠0，且对应点满足 y=f(x)。', '反函数的导数是在对应点取倒数，不是把变量直接互换。'],
    ['数列极限的四则运算', 'aₙ→A, bₙ→B\n则 aₙ±bₙ→A±B，aₙbₙ→AB\n若 B≠0，则 aₙ/bₙ→A/B', '参与运算的极限存在；除法还要求分母极限非零。', '∞−∞、0·∞、0/0、∞/∞均不能直接代入。'],
    ['函数极限的四则运算', 'lim(f±g)=lim f±lim g\nlim(fg)=lim f·lim g\nlim(f/g)=lim f / lim g', '各极限存在；商的分母极限不为 0。', '极限不存在时不能拆开运算。'],
    ['夹逼准则', '若 g(x)≤f(x)≤h(x)，且\nlim g(x)=lim h(x)=A\n则 lim f(x)=A', '不等式在去心邻域内成立，上下界趋于同一极限。', '只比较大小但上下界极限不同，不能推出中间极限。'],
    ['单调有界准则', '单调递增且有上界 ⇒ 收敛\n单调递减且有下界 ⇒ 收敛', '用于数列；单调性与对应方向的有界性缺一不可。', '有界数列未必收敛，如 (−1)ⁿ。'],
    ['第一个重要极限', 'lim(x→0) sin x / x = 1\n推广：sin u ~ u（u→0）', '角度必须用弧度；复合量 u→0。', 'sin u/u 的极限点是 u→0，不能机械约掉。'],
    ['第二个重要极限', 'lim(x→0) (1+x)^(1/x)=e\nlim(n→∞) (1+1/n)ⁿ=e\n推广：(1+u)^v→eᴬ 若 u→0 且 uv→A', '底数在实数范围内有定义；幂指型先取对数最稳妥。', '只知道底数→1、指数→∞，不能直接判为 e。'],
    ['常用等价无穷小（一）', 'x→0 时：\nsin x ~ x，tan x ~ x，arcsin x ~ x\narctan x ~ x，eˣ−1 ~ x，ln(1+x) ~ x', '只能在乘除结构中直接替换；复合量必须趋于 0。', '加减结构直接替换可能丢失主项。'],
    ['常用等价无穷小（二）', 'x→0 时：\n1−cos x ~ x²/2\naˣ−1 ~ x ln a\n(1+x)^α−1 ~ αx\n√(1+x)−1 ~ x/2', 'a>0 且 a≠1；α 为常数。', '1−cos x 的阶数是 2，常数因子 1/2 不能漏。'],
    ['高阶等价展开', 'x→0 时：\nx−sin x ~ x³/6\ntan x−x ~ x³/3\narcsin x−x ~ x³/6\nx−arctan x ~ x³/3', '用于一阶等价发生抵消后的极限。', '先确认符号：arctan x−x ~ −x³/3。', '高频'],
    ['无穷小阶的比较', '若 lim β/α = 0：β 是 α 的高阶无穷小\n若 lim β/α = c≠0：同阶\n若 c=1：等价', 'α、β 均为同一过程下的无穷小。', '“高阶”表示趋零更快，不表示数值更大。'],
    ['洛必达型判别入口', '0/0 型：f→0, g→0\n∞/∞ 型：|f|→∞, |g|→∞\n满足条件时 lim f/g = lim f′/g′', '在去心邻域可导、g′≠0，且导数比极限存在或为无穷。', '其他未定式必须先变形成商；不能仅因结果方便就使用。'],
    ['连续的运算', 'f,g 在 x₀ 连续 ⇒ f±g、fg 连续\n若 g(x₀)≠0，则 f/g 连续\n复合函数在对应点连续', '分母非零，复合函数内外层连续点要对应。', '分段函数连接点必须分别检查左极限、右极限与函数值。'],
    ['间断点分类', '第一类：左右极限都存在\n可去：左右极限相等但不等于函数值\n跳跃：左右极限不等\n第二类：至少一个单侧极限不存在或为无穷', '分类只看该点左右极限。', '无穷间断点属于第二类，不属于跳跃间断点。'],
    ['闭区间连续函数性质', 'f∈C[a,b] ⇒ 有界且取得最大最小值\n若 f(a)f(b)<0 ⇒ 至少有一点 ξ 使 f(ξ)=0\n介值：介于 f(a),f(b) 的值均能取到', '闭区间连续是关键条件。', '零点定理给存在性，不保证唯一性。'],
    ['Stolz 定理常用式', '若 bₙ 严格递增且 bₙ→∞，则在条件满足时\nlim aₙ/bₙ = lim (aₙ₊₁−aₙ)/(bₙ₊₁−bₙ)', '右端极限存在；常用于数列 ∞/∞ 型。', '不是所有数列极限都能直接差分；先核对分母条件。', '拓展']
  ]);

  add('高等数学', '一元函数微分学', [
    ['导数定义', 'f′(x₀)=lim(Δx→0)[f(x₀+Δx)−f(x₀)]/Δx\n=lim(x→x₀)[f(x)−f(x₀)]/(x−x₀)', '极限为有限数时可导。', '可导必连续，连续不一定可导。'],
    ['基本导数表（一）', '(C)′=0，(x^α)′=αx^(α−1)\n(eˣ)′=eˣ，(aˣ)′=aˣ ln a\n(ln x)′=1/x，(logₐx)′=1/(x ln a)', '幂函数按实际定义域使用；对数要求 x>0。', 'ln|x| 的导数在 x≠0 时也是 1/x。'],
    ['基本导数表（二）', '(sin x)′=cos x，(cos x)′=−sin x\n(tan x)′=sec²x，(cot x)′=−csc²x\n(sec x)′=sec x tan x，(csc x)′=−csc x cot x', '函数在相应点有定义。', 'cot、csc 的导数带负号。'],
    ['反三角函数导数', '(arcsin x)′=1/√(1−x²)\n(arccos x)′=−1/√(1−x²)\n(arctan x)′=1/(1+x²)\n(arccot x)′=−1/(1+x²)', 'arcsin、arccos 的导数公式用于 |x|<1。', 'arccos 与 arccot 的导数带负号。'],
    ['四则与复合求导', '(u±v)′=u′±v′\n(uv)′=u′v+uv′\n(u/v)′=(u′v−uv′)/v²\n[f(g(x))]′=f′(g(x))g′(x)', '各函数可导；商要求 v≠0。', '复合函数必须乘内层导数。'],
    ['参数方程求导', 'x=φ(t), y=ψ(t)\ndy/dx=ψ′(t)/φ′(t)\nd²y/dx²=[d/dt(dy/dx)]/φ′(t)', 'φ′(t)≠0。', '二阶导不是 ψ″/φ″，还要再除以 dx/dt。'],
    ['隐函数求导', 'F(x,y)=0 ⇒ y′=−Fₓ/Fᵧ', 'F 可微且 Fᵧ≠0。', '偏导计算后再代入曲线点；二阶导需对等式继续求导。'],
    ['对数求导法', '若 y=u(x)^v(x)>0：\nln y=v ln u\ny′=y[v′ln u+v·u′/u]', '实数范围通常要求 u>0。', '幂指函数不能套普通幂函数求导。'],
    ['高阶导数莱布尼茨公式', '(uv)⁽ⁿ⁾=Σ(k=0→n) Cₙᵏ u⁽ᵏ⁾v⁽ⁿ⁻ᵏ⁾', 'u、v 具有 n 阶导数。', '组合数与两个函数的导数阶数要对应。'],
    ['微分', 'dy=f′(x)dx\nΔy=f′(x)Δx+o(Δx)\n当 Δx 很小时：Δy≈dy', 'f 在该点可微。', 'dy 是线性主部，不等同于任意大小的 Δy。'],
    ['线性近似', 'f(x₀+Δx)≈f(x₀)+f′(x₀)Δx', 'Δx 足够小，且函数在 x₀ 可微。', '近似误差阶数取决于更高阶导数。'],
    ['曲率', 'K=|y″|/[1+(y′)²]^(3/2)\n曲率半径 ρ=1/K', '平面曲线 y=f(x) 二阶可导。', '分母指数是 3/2；直线曲率为 0。'],
    ['参数曲线曲率', 'K=|x′y″−y′x″|/(x′²+y′²)^(3/2)', 'x′²+y′²≠0。', '分子是二维叉积绝对值。'],
    ['弧微分', '直角坐标：ds=√[1+(y′)²] dx\n参数方程：ds=√[(x′)²+(y′)²] dt\n极坐标：ds=√[r²+(r′)²] dθ', '曲线分段光滑。', '极坐标中不能漏掉 r²。']
  ]);

  add('高等数学', '中值定理与导数应用', [
    ['费马引理', '若 x₀ 为可导函数的内点极值点，则 f′(x₀)=0', 'x₀ 是定义域内点且 f 在 x₀ 可导。', '驻点不一定是极值点。'],
    ['罗尔定理', 'f∈C[a,b]，在 (a,b) 可导，且 f(a)=f(b)\n⇒ ∃ξ∈(a,b)，f′(ξ)=0', '三个条件必须同时成立。', '结论点在开区间内。'],
    ['拉格朗日中值定理', '∃ξ∈(a,b)：\nf′(ξ)=[f(b)−f(a)]/(b−a)', 'f∈C[a,b] 且在 (a,b) 可导。', '证明不等式时常把差值转成某点导数。'],
    ['柯西中值定理', '[f(b)−f(a)]/[g(b)−g(a)]=f′(ξ)/g′(ξ)', 'f,g 在闭区间连续、开区间可导，并通常要求 g′≠0。', '分母差与导数分母都要有意义。'],
    ['泰勒公式（佩亚诺余项）', 'f(x)=Σ(k=0→n) f⁽ᵏ⁾(x₀)(x−x₀)ᵏ/k!\n+o((x−x₀)ⁿ)', 'f 在 x₀ 具有 n 阶导数。', '佩亚诺余项适合局部极限，不能直接给全区间误差界。'],
    ['泰勒公式（拉格朗日余项）', 'f(x)=Σ(k=0→n) f⁽ᵏ⁾(x₀)(x−x₀)ᵏ/k!\n+f⁽ⁿ⁺¹⁾(ξ)(x−x₀)ⁿ⁺¹/(n+1)!', '函数在两点间满足相应连续可导条件，ξ 位于 x 与 x₀ 之间。', '余项的导数阶数是 n+1。'],
    ['常用麦克劳林展开（一）', 'eˣ=1+x+x²/2!+x³/3!+…\nsin x=x−x³/3!+x⁵/5!−…\ncos x=1−x²/2!+x⁴/4!−…', '在收敛范围内成立；用于极限时按所需阶截断。', '发生相减时必须展开到首个不抵消项。'],
    ['常用麦克劳林展开（二）', 'ln(1+x)=x−x²/2+x³/3−…（−1<x≤1）\n(1+x)^α=1+αx+α(α−1)x²/2!+…（|x|<1）', '端点收敛需单独判断；α 为常数。', '二项式系数是下降幂 α(α−1)…。'],
    ['常用麦克劳林展开（三）', '1/(1−x)=1+x+x²+…（|x|<1）\narctan x=x−x³/3+x⁵/5−…（|x|≤1，端点条件收敛）', '按收敛区间使用。', '1/(1+x) 应由 x→−x 得到交错展开。'],
    ['单调性判定', 'f′(x)>0 ⇒ 严格递增\nf′(x)<0 ⇒ 严格递减', '在区间内可导；非严格结论可用 f′≥0 或 ≤0。', '只看一个点的导数符号不能判断整个区间。'],
    ['极值判别', '第一充分条件：f′ 左正右负 ⇒ 极大；左负右正 ⇒ 极小\n第二充分条件：f′(x₀)=0 且 f″(x₀)>0 ⇒ 极小；f″(x₀)<0 ⇒ 极大', '二阶判别要求二阶导存在且非零。', 'f″(x₀)=0 时不能下结论，回到符号法或高阶判别。'],
    ['凹凸性与拐点', 'f″(x)>0 ⇒ f′递增，图形开口向上\nf″(x)<0 ⇒ f′递减，图形开口向下\n拐点要求曲线的凹凸性发生改变', '以二阶导数的符号与变化为准，避免不同教材“凹/凸”术语方向差异。', 'f″(x₀)=0 只是拐点候选条件，不是充分条件。'],
    ['渐近线', '竖直：lim(x→x₀)f(x)=∞ ⇒ x=x₀\n水平：lim(x→±∞)f(x)=b ⇒ y=b\n斜渐近线：a=lim f(x)/x，b=lim[f(x)−ax] ⇒ y=ax+b', '相应极限存在；左右或正负无穷方向分别判断。', '两个无穷方向可能对应不同渐近线。']
  ]);

  add('高等数学', '一元函数积分学', [
    ['不定积分定义', '若 F′(x)=f(x)，则\n∫f(x)dx=F(x)+C', '在所讨论区间内。', '不定积分必须写任意常数 C。'],
    ['基本积分表（一）', '∫x^α dx=x^(α+1)/(α+1)+C（α≠−1）\n∫dx/x=ln|x|+C\n∫eˣdx=eˣ+C\n∫aˣdx=aˣ/ln a+C', '按函数定义域分区间理解。', '幂积分 α=−1 必须单列为对数。'],
    ['基本积分表（二）', '∫sin x dx=−cos x+C\n∫cos x dx=sin x+C\n∫sec²x dx=tan x+C\n∫csc²x dx=−cot x+C', '被积函数在区间内连续。', 'sin 与 csc² 的原函数带负号。'],
    ['基本积分表（三）', '∫dx/(1+x²)=arctan x+C\n∫dx/√(1−x²)=arcsin x+C\n∫dx/(a²+x²)=(1/a)arctan(x/a)+C（a>0）', '平方根式要求实数范围有定义。', '缩放后前面的 1/a 不能漏。'],
    ['基本积分表（四）', '∫dx/(a²−x²)=(1/2a)ln|(a+x)/(a−x)|+C\n∫dx/√(x²+a²)=ln|x+√(x²+a²)|+C', 'a>0；按定义域分区间。', '根式积分的对数绝对值按定义域处理。'],
    ['第一类换元法', '∫f(g(x))g′(x)dx=∫f(u)du=F(g(x))+C', 'u=g(x) 可微。', '必须把与 du 对应的因子完整配出。'],
    ['第二类换元法', '令 x=φ(t)：\n∫f(x)dx=∫f(φ(t))φ′(t)dt', '换元后要回代；定积分则同时换上下限。', '根式换元要结合原变量范围选取三角函数符号。'],
    ['分部积分', '∫u dv=uv−∫v du', 'u 可微，v 是 dv 的原函数。', '选择 u 时优先让求导后简化；定积分边界项要代上下限。'],
    ['有理函数部分分式', 'P(x)/Q(x)=整式+真分式\n线性因子：(Ax+B)/(不可约二次因子)\n重因子按 1/(x−a)^k 逐项展开', '先做多项式除法，使分子次数低于分母。', '不可约二次因子的分子必须是一阶式 Ax+B。'],
    ['三角有理式换元', 't=tan(x/2)\nsin x=2t/(1+t²)，cos x=(1−t²)/(1+t²)\ndx=2dt/(1+t²)', '用于 sin x、cos x 的有理函数积分。', '这是通用换元，不一定是最简方法。'],
    ['定积分定义与可积性', '∫ₐᵇf(x)dx=lim Σ f(ξᵢ)Δxᵢ', '分割最大长度趋于 0；连续或只有有限个第一类间断点的函数可积。', '定积分是数，不含积分变量。'],
    ['牛顿—莱布尼茨公式', '若 F′(x)=f(x)，则\n∫ₐᵇ f(x)dx=F(b)−F(a)', 'f 在 [a,b] 连续，或满足相应可积与原函数条件。', '上下限顺序颠倒会变号。'],
    ['变上限积分求导', 'Φ(x)=∫ₐˣ f(t)dt ⇒ Φ′(x)=f(x)\nΦ(x)=∫ᵤ⁽ˣ⁾ᵛ⁽ˣ⁾ f(t)dt ⇒ Φ′=f(v)v′−f(u)u′', 'f 连续，u、v 可导。', '下限项前有负号。'],
    ['定积分换元', '∫ₐᵇ f(g(x))g′(x)dx=∫g(a)^g(b) f(u)du', 'g 连续可导；换元时同步更换上下限。', '换元后若已改上下限，不再回代 x。'],
    ['定积分分部积分', '∫ₐᵇ u v′ dx=[uv]ₐᵇ−∫ₐᵇ u′v dx', 'u、v 具有所需连续性。', '边界项 [uv]ₐᵇ=u(b)v(b)−u(a)v(a)。'],
    ['积分中值定理', '若 f 连续，g≥0 且可积，则\n∫ₐᵇ f(x)g(x)dx=f(ξ)∫ₐᵇg(x)dx\n特别地：∫ₐᵇf(x)dx=f(ξ)(b−a)', 'ξ∈[a,b]；第一积分中值定理要求 g 不变号。', '结论给存在性，通常不能直接求 ξ。'],
    ['区间对称性', '∫₋ₐᵃ 奇函数 dx=0\n∫₋ₐᵃ 偶函数 dx=2∫₀ᵃ f(x)dx\n∫₀ᵃ f(x)dx=∫₀ᵃ f(a−x)dx', '函数可积，区间关于原点或中点对称。', '先看整体被积函数奇偶性，不要只看某个因子。'],
    ['Wallis 递推', 'Iₙ=∫₀^(π/2) sinⁿx dx=∫₀^(π/2) cosⁿx dx\nIₙ=(n−1)/n·Iₙ₋₂\nI₀=π/2，I₁=1', 'n 为正整数。', '偶数链最终乘 I₀，奇数链最终乘 I₁。'],
    ['反常积分 p 判别', '∫₁^∞ dx/xᵖ：p>1 收敛，p≤1 发散\n∫₀¹ dx/xᵖ：p<1 收敛，p≥1 发散', '比较判别时被积函数通常非负。', '无穷远与有限瑕点的临界条件方向相反。'],
    ['反常积分比较判别', '0≤f≤g：若 ∫g 收敛，则 ∫f 收敛\n若 ∫f 发散，则 ∫g 发散\n若 f/g→c∈(0,∞)，二者同敛散', '在瑕点邻域或充分大区间成立。', '比较方向不要写反。']
  ]);

  add('高等数学', '定积分应用与空间解析几何', [
    ['平面图形面积', '直角坐标：A=∫ₐᵇ|f(x)−g(x)|dx\n参数形式：A=|∫y dx|（按闭曲线方向处理）\n极坐标：A=(1/2)∫ r²(θ)dθ', '边界分段光滑；直角坐标需明确上下曲线。', '交点变化处要分段，不能让面积相消。'],
    ['旋转体体积（圆盘/垫片）', '绕 x 轴：V=π∫ₐᵇ[R²(x)−r²(x)]dx\n绕 y 轴同理按 y 积分', '截面垂直于旋转轴。', '半径是到旋转轴的距离，不是函数值的符号。'],
    ['旋转体体积（柱壳）', '绕 y 轴：V=2π∫ₐᵇ x·高度(x) dx\n绕 x 轴：V=2π∫ y·宽度(y) dy', '壳半径非负；必要时取绝对值或分段。', '壳法截条与旋转轴平行。'],
    ['平面曲线弧长', 'y=f(x)：L=∫ₐᵇ√[1+(y′)²]dx\n参数：L=∫α^β√[(x′)²+(y′)²]dt\n极坐标：L=∫√[r²+(r′)²]dθ', '曲线分段光滑。', '参数区间要覆盖曲线一次，避免重复计长。'],
    ['旋转曲面面积', '绕 x 轴：S=2π∫ y ds=2π∫ₐᵇ|y|√[1+(y′)²]dx\n绕 y 轴：S=2π∫|x|ds', '曲线分段光滑，半径取到轴的非负距离。', '侧面积公式没有端面面积。'],
    ['定积分物理应用', '变力做功：W=∫ F(s)ds\n液体静压力：P=∫ ρg·深度·条宽 dy\n平均值：f̄=(1/(b−a))∫ₐᵇf(x)dx', '先统一单位并选择合适微元。', '压力积分中的深度从液面量起。'],
    ['向量数量积', 'a·b=|a||b|cosθ=a₁b₁+a₂b₂+a₃b₃\na⊥b ⇔ a·b=0', '零向量与夹角概念要单独处理。', '点积结果是标量。'],
    ['向量叉积', 'a×b=(a₂b₃−a₃b₂, a₃b₁−a₁b₃, a₁b₂−a₂b₁)\n|a×b|=|a||b|sinθ', '按右手定则确定方向。', '交换次序会变号：b×a=−a×b。'],
    ['平面方程', '点法式：A(x−x₀)+B(y−y₀)+C(z−z₀)=0\n一般式：Ax+By+Cz+D=0', '法向量 n=(A,B,C)≠0。', '平面平行看法向量平行，垂直看法向量点积为 0。'],
    ['空间直线方程', '(x−x₀)/l=(y−y₀)/m=(z−z₀)/n\n参数式：(x,y,z)=(x₀,y₀,z₀)+t(l,m,n)', '方向向量 s=(l,m,n)≠0。', '直线与平面平行：s·n=0；若还过平面上一点则直线在平面内。'],
    ['点到平面距离', 'd=|Ax₀+By₀+Cz₀+D|/√(A²+B²+C²)', '平面法向量非零。', '分子必须取绝对值。'],
    ['两平面夹角', 'cosθ=|n₁·n₂|/(|n₁||n₂|)', '通常取锐二面角。', '若求有向夹角才保留点积符号。']
  ]);

  add('高等数学', '多元函数微分学', [
    ['全微分', 'dz=fₓdx+fᵧdy\nΔz=fₓΔx+fᵧΔy+o(ρ)，ρ=√(Δx²+Δy²)', '函数在该点可微；偏导连续是可微的充分条件。', '偏导存在不一定可微。'],
    ['多元复合函数链式法则', 'z=f(u,v), u=u(x,y), v=v(x,y)\n∂z/∂x=fᵤuₓ+fᵥvₓ\n∂z/∂y=fᵤuᵧ+fᵥvᵧ', '各函数在对应点可微。', '每条依赖路径都要相加。'],
    ['一阶隐函数偏导', 'F(x,y,z)=0，z=z(x,y)\nzₓ=−Fₓ/F_z，zᵧ=−Fᵧ/F_z', 'F_z≠0 且满足隐函数存在条件。', 'F 的偏导先按 x,y,z 独立变量计算。'],
    ['隐函数组求导', 'F(x,y,u,v)=0，G(x,y,u,v)=0\n对 x 或 y 分别求导，解关于 uₓ,vₓ 或 uᵧ,vᵧ 的线性方程组', '关于 (u,v) 的雅可比行列式 ∂(F,G)/∂(u,v)≠0。', '不要漏掉 u、v 对自变量的链式项。'],
    ['方向导数', '沿单位向量 e=(cosα,cosβ)：\nDₑf=fₓcosα+fᵧcosβ=∇f·e', 'f 在该点可微，方向向量必须单位化。', '题目给的普通向量要先除以模。'],
    ['梯度', '∇f=(fₓ,fᵧ,f_z)\n最大方向导数=max Dₑf=|∇f|，方向为 ∇f/|∇f|', '∇f≠0 时最大增长方向确定。', '梯度垂直于等值面，不是沿曲面切向。'],
    ['空间曲线切线与法平面', '曲线 r(t)=(x(t),y(t),z(t))\n切向量 r′(t₀)\n法平面：r′(t₀)·[(x,y,z)−r(t₀)]=0', 'r′(t₀)≠0。', '法平面的法向量正是曲线切向量。'],
    ['曲面切平面与法线', 'F(x,y,z)=0\n切平面：∇F(P₀)·(P−P₀)=0\n法线：P=P₀+t∇F(P₀)', '∇F(P₀)≠0。', '显式曲面 z=f(x,y) 可写 F=f−z。'],
    ['二元泰勒公式（二阶）', 'f(x₀+h,y₀+k)=f₀+fₓh+fᵧk\n+1/2(fₓₓh²+2fₓᵧhk+fᵧᵧk²)+o(h²+k²)', '二阶偏导在邻域满足相应条件。', '混合项系数在括号内是 2。'],
    ['二元函数极值必要条件', '若 (x₀,y₀) 是内点极值且偏导存在，则\nfₓ(x₀,y₀)=fᵧ(x₀,y₀)=0', '内点极值。', '驻点只是候选点，仍需判别。'],
    ['二元函数极值充分判别', 'A=fₓₓ，B=fₓᵧ，C=fᵧᵧ，D=AC−B²\nD>0,A>0 ⇒ 极小；D>0,A<0 ⇒ 极大\nD<0 ⇒ 鞍点；D=0 ⇒ 失效', '二阶偏导连续，且点为驻点。', 'D=0 时不能判定。'],
    ['拉格朗日乘数法', '约束 g(x,y,z)=0：\n∇f=λ∇g，连同 g=0 求候选点\n多约束：∇f=λ∇g+μ∇h', '约束面正则，且不要遗漏约束边界或退化点。', '求出的点还需比较函数值；闭区域还要检查边界与角点。']
  ]);

  add('高等数学', '多重积分', [
    ['二重积分定义与性质', '∬ᴰ f(x,y)dσ\n若 f≥0，表示曲顶柱体有向体积\n|∬ᴰf|≤∬ᴰ|f|', 'f 在有界闭区域上可积。', '积分区域本身是计算的一部分，必须准确描述。'],
    ['直角坐标累次积分', 'X 型区域：D={a≤x≤b, φ₁(x)≤y≤φ₂(x)}\n∬ᴰf dσ=∫ₐᵇdx∫φ₁^φ₂ f(x,y)dy', '区域能用该方向单值表示；否则分片。', '先写外层变量范围，再按竖线或横线写内层。'],
    ['极坐标二重积分', 'x=r cosθ，y=r sinθ，dσ=r dr dθ\n∬ᴰf dσ=∫∫ f(r cosθ,r sinθ)·r dr dθ', '区域适合由射线扫描；r≥0。', '雅可比因子 r 不能漏。'],
    ['二重积分对称性', 'D 关于 y 轴对称：f 对 x 为奇 ⇒ 积分 0\nD 关于原点对称：f(−x,−y)=−f(x,y) ⇒ 积分 0\n对称变量可用交换 x,y', '区域和被积函数必须同时满足对应对称关系。', '区域不对称时仅凭函数奇偶性不能消掉。'],
    ['三重积分直角坐标', '∭Ω f(x,y,z)dv\n投影法：∬ᴰxy dxdy ∫z₁(x,y)^z₂(x,y) f dz', 'Ω 可沿 z 方向单值表示；否则分片或换投影。', '先定投影区域，再写上下曲面。'],
    ['柱坐标', 'x=r cosθ，y=r sinθ，z=z\ndv=r dr dθ dz', '绕 z 轴具有圆柱对称时常用。', '仍有雅可比 r。'],
    ['球坐标', 'x=ρ sinφ cosθ，y=ρ sinφ sinθ，z=ρ cosφ\ndv=ρ²sinφ dρ dφ dθ', 'ρ≥0，通常 0≤φ≤π，0≤θ<2π。', 'φ 是与正 z 轴的夹角；雅可比是 ρ²sinφ。'],
    ['三重积分对称性', '若 Ω 关于坐标面对称，被积函数关于对应变量为奇函数，则积分为 0\n球对称时常先积角变量', '区域与函数的对称性都要成立。', '含绝对值会改变奇偶性。'],
    ['一般变量代换', 'x=x(u,v), y=y(u,v)\ndxdy=|∂(x,y)/∂(u,v)| dudv', '变换在区域内一一对应或分片一一对应，雅可比非零。', '面积元取雅可比绝对值。'],
    ['二重积分的几何应用', '面积 A=∬ᴰ1 dσ\n质量 m=∬ᴰρ(x,y)dσ\n质心 x̄=(1/m)∬ᴰxρdσ，ȳ=(1/m)∬ᴰyρdσ', '密度非负且总质量不为 0。', '均匀薄片可令 ρ 为常数并约去。'],
    ['转动惯量', 'Iₓ=∬ᴰ y²ρ dσ，Iᵧ=∬ᴰ x²ρ dσ\nI₀=∬ᴰ(x²+y²)ρ dσ=Iₓ+Iᵧ', '薄片关于指定轴。', '到 x 轴的距离是 |y|，所以平方为 y²。']
  ]);

  add('高等数学', '曲线积分与曲面积分', [
    ['第一类曲线积分', '∫ᴸ f(x,y,z)ds\n参数 r(t)：∫α^β f(r(t))|r′(t)|dt', '曲线分段光滑。', '第一类曲线积分与路径方向无关。'],
    ['第二类曲线积分', '∫ᴸPdx+Qdy+Rdz\n参数 r(t)：∫α^β[P x′+Q y′+R z′]dt', '曲线定向且分段光滑。', '反向积分变号。'],
    ['格林公式', '∮∂D Pdx+Qdy=∬ᴰ(Qₓ−Pᵧ)dxdy', 'D 为平面有向区域，边界取正向（外边界逆时针，内边界顺时针），P,Q 有连续偏导。', '边界有洞时内边界方向相反。'],
    ['平面曲线积分与路径无关', '在单连通区域内：\n∫Pdx+Qdy 与路径无关 ⇔ Pᵧ=Qₓ\n⇔ 存在势函数 u，使 du=Pdx+Qdy', 'P,Q 有连续偏导且区域单连通。', '挖孔区域不能只凭 Pᵧ=Qₓ 就全局判定。'],
    ['势函数求法', '由 uₓ=P 积分得 u=∫Pdx+φ(y)\n再用 uᵧ=Q 求 φ′(y)\n积分值=u(B)−u(A)', '微分形式为全微分。', '对 x 积分时“常数”是 y 的函数。'],
    ['第一类曲面积分', '∬Σ f dS\nz=z(x,y)：dS=√(1+zₓ²+zᵧ²)dxdy\n参数曲面：dS=|rᵤ×rᵥ|dudv', '曲面分片光滑。', '第一类曲面积分与曲面定向无关。'],
    ['第二类曲面积分', '∬Σ P dydz+Q dzdx+R dxdy = ∬Σ F·n dS', '曲面需定向。', '改变曲面侧向，积分变号。'],
    ['图形曲面的第二类积分', 'z=z(x,y)，取上侧：\n∬Σ P dydz+Q dzdx+R dxdy\n=∬ᴰ[−Pzₓ−Qzᵧ+R]dxdy\n下侧取相反号', '曲面能投影为单值图形。', '上侧法向量可取 (−zₓ,−zᵧ,1)。'],
    ['高斯公式', '∯∂Ω P dydz+Q dzdx+R dxdy\n=∭Ω(Pₓ+Qᵧ+R_z)dv', 'Ω 为有界空间区域，边界取外侧，分量具有连续偏导。', '封闭曲面且外侧定向；有奇点时需挖去或另行处理。'],
    ['散度', 'div F=∇·F=Pₓ+Qᵧ+R_z', 'F=(P,Q,R) 可微。', '散度是标量，描述净流出强度。'],
    ['斯托克斯公式', '∮∂Σ Pdx+Qdy+Rdz\n=∬Σ (curl F)·n dS', '曲面定向与边界方向满足右手规则，分量有连续偏导。', '边界方向由所选法向决定。'],
    ['旋度', 'curl F=∇×F\n=(Rᵧ−Q_z, P_z−Rₓ, Qₓ−Pᵧ)', 'F 一阶偏导存在。', '三分量符号按行列式展开，第二分量最易错。']
  ]);

  add('高等数学', '无穷级数', [
    ['级数收敛必要条件', 'Σuₙ 收敛 ⇒ uₙ→0', '任何数项级数。', 'uₙ→0 不是充分条件，调和级数反例。'],
    ['等比级数', 'Σ(n=0→∞) aqⁿ=a/(1−q)，当 |q|<1\n|q|≥1 时发散', '首项按 n=0 书写。', '从 n=1 开始时和少一个首项。'],
    ['p 级数', 'Σ1/nᵖ：p>1 收敛，p≤1 发散', 'n 从正整数开始。', '临界值 p=1 发散。'],
    ['正项级数比较判别', '0≤uₙ≤vₙ：Σvₙ 收敛 ⇒ Σuₙ 收敛\nΣuₙ 发散 ⇒ Σvₙ 发散', '从某项起成立即可。', '注意推理方向。'],
    ['正项级数极限比较', 'uₙ,vₙ>0，lim uₙ/vₙ=c\n0<c<∞ ⇒ 同敛散\nc=0 且 Σvₙ 收敛 ⇒ Σuₙ 收敛\nc=∞ 且 Σvₙ 发散 ⇒ Σuₙ 发散', '正项级数。', 'c=0 或 ∞ 时只能使用相应单向结论。'],
    ['比值判别', 'ρ=lim uₙ₊₁/uₙ\nρ<1 收敛；ρ>1 或 =∞ 发散；ρ=1 失效', '正项级数；极限存在或用上下极限版本。', 'ρ=1 不能判定。'],
    ['根值判别', 'ρ=lim ⁿ√uₙ\nρ<1 收敛；ρ>1 发散；ρ=1 失效', '正项级数。', '带 n 次幂的通项优先考虑。'],
    ['交错级数判别', 'Σ(−1)ⁿ⁻¹uₙ，若 uₙ 单调递减且 uₙ→0，则收敛\n余项 |Rₙ|≤uₙ₊₁', 'uₙ≥0，从某项起单调下降。', '只能保证收敛；是否绝对收敛需再看 Σuₙ。'],
    ['绝对与条件收敛', 'Σ|uₙ| 收敛 ⇒ Σuₙ 收敛（绝对收敛）\nΣuₙ 收敛但 Σ|uₙ| 发散 ⇒ 条件收敛', '一般数项级数。', '条件收敛级数不可随意重排。'],
    ['幂级数收敛半径', 'Σaₙ(x−x₀)ⁿ\n若 lim|aₙ₊₁/aₙ|=ρ，则 R=1/ρ\n若 lim ⁿ√|aₙ|=ρ，则 R=1/ρ', '约定 ρ=0 时 R=∞，ρ=∞ 时 R=0。', '端点 x=x₀±R 必须分别代回判定。'],
    ['幂级数逐项求导积分', '[Σaₙ(x−x₀)ⁿ]′=Σn aₙ(x−x₀)ⁿ⁻¹\n∫Σaₙ(x−x₀)ⁿdx=C+Σaₙ(x−x₀)ⁿ⁺¹/(n+1)', '在收敛区间内部；新级数半径不变。', '端点敛散性可能变化。'],
    ['函数展开为幂级数', '间接展开常用：代换、求导、积分、四则运算\n基础：1/(1−x)=Σxⁿ，|x|<1', '运算在共同收敛区间内进行。', '最终必须写收敛区间，尤其检查端点。'],
    ['傅里叶系数（−π,π）', 'f(x)~a₀/2+Σ(n=1→∞)[aₙcos nx+bₙsin nx]\na₀=(1/π)∫₋π^πf dx\naₙ=(1/π)∫₋π^πf cos nx dx\nbₙ=(1/π)∫₋π^πf sin nx dx', 'f 满足狄利克雷条件。', '常数项是 a₀/2。'],
    ['傅里叶系数（−l,l）', 'f(x)~a₀/2+Σ[aₙcos(nπx/l)+bₙsin(nπx/l)]\naₙ=(1/l)∫₋l^l f cos(nπx/l)dx\nbₙ=(1/l)∫₋l^l f sin(nπx/l)dx', '周期为 2l。', '三角函数频率是 nπ/l。'],
    ['傅里叶级数的点值', '连续点：级数和=f(x)\n跳跃点 x₀：级数和=[f(x₀−0)+f(x₀+0)]/2', '周期延拓后满足狄利克雷条件。', '端点要看周期延拓后的左右极限。'],
    ['奇偶函数傅里叶简化', 'f 偶 ⇒ bₙ=0，余弦级数\nf 奇 ⇒ a₀=aₙ=0，正弦级数', '积分区间关于原点对称。', '先判断周期延拓后的奇偶性。']
  ]);

  add('高等数学', '常微分方程', [
    ['可分离变量方程', 'dy/dx=f(x)g(y)\n∫dy/g(y)=∫f(x)dx+C', '分离前若除以 g(y)，要补查 g(y)=0 对应的常数解。', '除法可能丢失平衡解。'],
    ['齐次一阶方程', 'dy/dx=F(y/x)\n令 y=ux，则 y′=u+xu′，化为可分离变量', 'x≠0，在相应区间求解。', '这里“齐次”指可化为 y/x，不是线性齐次。'],
    ['一阶线性非齐次方程', 'y′+P(x)y=Q(x)\ny=e^(−∫Pdx)[∫Q(x)e^(∫Pdx)dx+C]', 'P,Q 在区间内连续。', '积分因子 μ=e^(∫Pdx)，指数符号最易错。'],
    ['一阶线性齐次方程', 'y′+P(x)y=0\ny=Ce^(−∫Pdx)', 'P 连续。', 'C=0 包含零解。'],
    ['伯努利方程', 'y′+P(x)y=Q(x)yⁿ（n≠0,1）\n令 z=y^(1−n)，得到\nz′+(1−n)Pz=(1−n)Q', '变换时注意可能丢失 y=0 解。', 'z 的指数是 1−n。'],
    ['可降阶方程 y⁽ⁿ⁾=f(x)', '连续积分 n 次：\ny=多项式常数项+对 f 的 n 次原函数', '右端仅含 x。', '每积分一次增加一个独立常数。'],
    ['不显含 y 的二阶方程', 'y″=F(x,y′)\n令 p=y′，则 p′=F(x,p)', '先解一阶方程求 p，再积分求 y。', '最后一次积分不要漏常数。'],
    ['不显含 x 的二阶方程', 'y″=F(y,y′)\n令 p(y)=y′，则 y″=p·dp/dy', '在可用 y 作局部变量的区间。', '链式法则得到 p·pᵧ，不是 pᵧ。'],
    ['二阶常系数齐次方程', 'y″+py′+qy=0，特征方程 r²+pr+q=0\nr₁≠r₂：y=C₁e^(r₁x)+C₂e^(r₂x)\n重根 r：y=(C₁+C₂x)e^(rx)\nα±iβ：y=e^(αx)(C₁cosβx+C₂sinβx)', '系数为常数。', '重根第二个解要乘 x。'],
    ['n 阶常系数齐次方程', '特征根 r，重数 k ⇒\ne^(rx), xe^(rx), …, x^(k−1)e^(rx)\n复根 α±iβ 的每个重数层乘 xʲ', '线性常系数齐次方程。', '复根必须成对转成实解。'],
    ['常系数非齐次特解设法', '若 f(x)=e^(λx)Pₘ(x)：设 y*=xˢe^(λx)Qₘ(x)\ns 为 λ 作为特征根的重数\n三角型用 e^(αx)(P cosβx+Q sinβx)', '待定系数法用于特定右端形式。', '共振时必须乘 xˢ；多项式次数通常保持。'],
    ['欧拉方程', 'x²y″+pxy′+qy=f(x)\n令 x=eᵗ（t=ln|x|）\nxy′=D y，x²y″=D(D−1)y', '在 x>0 或 x<0 的区间分别处理。', 'x²y″ 对应 D(D−1)，不是 D²。']
  ]);

  add('线性代数', '行列式与矩阵', [
    ['二阶与三阶行列式', '|a b; c d|=ad−bc\n三阶可按任一行（列）展开', '行列式只对方阵定义。', '行列式是数，不是矩阵。'],
    ['行列式交换与倍乘', '交换两行（列）：行列式变号\n某行（列）乘 k：行列式乘 k\n某行（列）加另一行（列）的 k 倍：行列式不变', '对整行或整列操作。', '把一行提取 k 后，矩阵该行要除以 k。'],
    ['行列式按行列展开', '|A|=Σⱼ aᵢⱼAᵢⱼ=Σᵢ aᵢⱼAᵢⱼ\nAᵢⱼ=(−1)^(i+j)Mᵢⱼ', '固定一行或一列展开。', '代数余子式含符号因子。'],
    ['伴随矩阵恒等式', 'AA*=A*A=|A|E\n若 |A|≠0，则 A⁻¹=A*/|A|', 'A 为方阵；求逆要求可逆。', '伴随矩阵由代数余子式矩阵转置得到。'],
    ['乘积行列式', '|AB|=|A||B|\n|Aᵀ|=|A|\n|A⁻¹|=1/|A|', 'A,B 为同阶方阵；逆矩阵存在。', '一般 |A+B|≠|A|+|B|。'],
    ['分块三角行列式', '|A B; 0 D|=|A||D|\n|A 0; C D|=|A||D|', '对角块 A,D 为方阵。', '非对角块不必为零矩阵的另一侧。'],
    ['矩阵乘法', '(AB)ᵢⱼ=Σₖaᵢₖbₖⱼ\n(AB)ᵀ=BᵀAᵀ\n(AB)⁻¹=B⁻¹A⁻¹', '维数匹配；逆矩阵存在。', '乘法通常不可交换，转置与求逆都要倒序。'],
    ['矩阵可逆等价条件', 'A 为 n 阶：\nA 可逆 ⇔ |A|≠0 ⇔ r(A)=n ⇔ Ax=0 仅零解\n⇔ 0 不是特征值 ⇔ 列（行）向量组线性无关', 'A 为方阵。', '非方阵不谈通常意义下的逆矩阵。'],
    ['初等矩阵与逆', '对 A 作一次初等行变换等于左乘初等矩阵 P\n[A | E] 经行变换化为 [E | A⁻¹]', 'A 可逆。', '列变换对应右乘初等矩阵。'],
    ['矩阵秩基本不等式', 'r(A+B)≤r(A)+r(B)\nr(AB)≤min{r(A),r(B)}\nr(A)+r(B)−n≤r(AB)（A:m×n, B:n×s）', '维数匹配。', '乘积的秩不会超过任一因子的秩。'],
    ['可逆矩阵不改变秩', 'P,Q 可逆 ⇒ r(PAQ)=r(A)\nr(AᵀA)=r(A)（实矩阵）', 'P,Q 维数适配；AᵀA 结论在实数域。', 'AᵀA=0 可推出 A=0。'],
    ['分块矩阵逆（对角）', 'diag(A,B)⁻¹=diag(A⁻¹,B⁻¹)', 'A,B 均可逆。', '非对角分块矩阵不能直接逐块求逆。']
  ]);

  add('线性代数', '向量与线性方程组', [
    ['线性相关定义式', 'α₁,…,αₘ 线性相关 ⇔ 存在不全为 0 的 kᵢ，使 Σkᵢαᵢ=0\n线性无关 ⇔ 只有全零系数', '向量维数相同。', '含零向量的向量组必线性相关。'],
    ['秩与极大无关组', '向量组秩=极大线性无关组所含向量个数\nr(α₁,…,αₘ)=矩阵的列秩=行秩', '把向量作列或行时保持一致。', '极大无关组不唯一，但所含向量数相同。'],
    ['线性表示与秩', 'β 可由 α₁,…,αₘ 线性表示\n⇔ r(α₁,…,αₘ)=r(α₁,…,αₘ,β)', '向量维数一致。', '秩不增加才表示 β 在原向量组张成空间内。'],
    ['两个向量组等价', '两组互相线性表示 ⇔ 张成空间相同\n有限向量组等价 ⇒ 秩相同', '向量属于同一线性空间。', '秩相同不一定推出两组等价。'],
    ['齐次方程解空间维数', 'Ax=0，A 为 m×n\n基础解系含 n−r(A) 个向量\ndim N(A)=n−r(A)', '未知数个数为 n。', '用列数减秩，不是行数减秩。'],
    ['非齐次方程有解判定', 'Ax=b 有解 ⇔ r(A)=r(A|b)\n唯一解 ⇔ r(A)=r(A|b)=n\n无穷多解 ⇔ r(A)=r(A|b)<n', 'n 为未知数个数。', '增广矩阵秩大于系数矩阵秩时无解。'],
    ['非齐次通解结构', '若 x₀ 是 Ax=b 的一个特解，η 为 Ax=0 的通解\n则 Ax=b 的通解 x=x₀+η', '非齐次方程有解。', '非齐次解集一般不是线性空间，是仿射空间。'],
    ['同解方程组', '齐次方程 Ax=0 与 Bx=0 同解\n⇔ A、B 的行向量组等价\n⇔ 行空间相同', '未知数个数相同。', '仅 r(A)=r(B) 不足以保证同解。'],
    ['克拉默法则', 'n 元 n 方程 Ax=b，|A|≠0\nxᵢ=Dᵢ/D', '系数矩阵为方阵且行列式非零。', 'Dᵢ 是用 b 替换第 i 列得到的行列式。'],
    ['基础解系通解', '若 η₁,…,ηₛ 为 Ax=0 的基础解系\n则 x=k₁η₁+…+kₛηₛ，s=n−r(A)', 'ηᵢ 线性无关且张成全部解。', '自由变量个数等于基础解系向量个数。'],
    ['正交向量与单位化', 'α⊥β ⇔ αᵀβ=0\n单位化：e=α/|α|\n|α|=√(αᵀα)', '实向量；α≠0 才能单位化。', '正交非零向量组必线性无关。'],
    ['Schmidt 正交化', 'β₁=α₁\nβₖ=αₖ−Σ(j<k)[(αₖ,βⱼ)/(βⱼ,βⱼ)]βⱼ\neₖ=βₖ/|βₖ|', '原向量组线性无关。', '投影分母是 (βⱼ,βⱼ)，不是 |βⱼ|。']
  ]);

  add('线性代数', '特征值、相似与二次型', [
    ['特征值与特征向量', 'Aξ=λξ（ξ≠0）\n特征方程 |λE−A|=0\n特征向量为 (A−λE)x=0 的非零解', 'A 为方阵。', '零向量永远不是特征向量。'],
    ['迹与行列式', 'Σλᵢ=tr(A)=Σaᵢᵢ\nΠλᵢ=|A|', '特征值按代数重数计，在复数域完整计数。', '矩阵元素总和不是特征值之和。'],
    ['矩阵多项式的特征值', 'Aξ=λξ ⇒ f(A)ξ=f(λ)ξ\nAⁿ 的对应特征值为 λⁿ\nA⁻¹ 的对应特征值为 1/λ', '逆矩阵结论要求 λ≠0 且 A 可逆。', 'f(A) 可能有新的特征向量合并，但给定 ξ 仍成立。'],
    ['相似矩阵', 'B=P⁻¹AP\n则 A、B 有相同特征多项式、特征值、行列式、迹、秩', 'P 可逆。', '特征值相同不一定相似。'],
    ['可相似对角化判定', 'A 可对角化 ⇔ 有 n 个线性无关特征向量\n⇔ 对每个特征值，几何重数=代数重数\n有 n 个互异特征值 ⇒ 可对角化', 'A 为 n 阶方阵。', '有重根不代表一定不可对角化。'],
    ['对角化计算', 'P=(ξ₁,…,ξₙ)，Λ=diag(λ₁,…,λₙ)\nP⁻¹AP=Λ，A=PΛP⁻¹\nAᵏ=PΛᵏP⁻¹', 'ξᵢ 为与 λᵢ 对应的线性无关特征向量。', 'P 的列顺序必须与 Λ 对角元顺序一致。'],
    ['实对称矩阵谱性质', 'A=Aᵀ ⇒ 特征值全为实数\n不同特征值的特征向量正交\n存在正交矩阵 Q：QᵀAQ=Λ', 'A 为实对称矩阵。', '一般矩阵不保证正交对角化。'],
    ['二次型矩阵表示', 'f(x)=xᵀAx，其中 A 取实对称矩阵\n交叉项 2aᵢⱼxᵢxⱼ', '二次型矩阵按对称形式唯一确定。', '交叉项系数要平分到 aᵢⱼ 与 aⱼᵢ。'],
    ['合同变换', 'x=Cy（C 可逆） ⇒ xᵀAx=yᵀ(CᵀAC)y\nA 与 CᵀAC 合同', 'C 可逆。', '合同与相似是不同关系；二次型化标准形用合同。'],
    ['惯性定理', '实二次型经可逆线性变换化为\ny₁²+…+yₚ²−yₚ₊₁²−…−yₚ₊q²\np,q 分别为正、负惯性指数，且在合同变换下不变', '实对称二次型。', '标准形系数可规范为 ±1；规范形与对角形不要混淆。'],
    ['正定判定（特征值）', '实对称 A 正定 ⇔ 所有特征值 λᵢ>0\n负定 ⇔ 所有 λᵢ<0', 'A 实对称。', '非对称矩阵不能直接用此结论判二次型正定。'],
    ['正定判定（顺序主子式）', 'A 正定 ⇔ 各阶顺序主子式 Δ₁>0,…,Δₙ>0\nA 负定 ⇔ (−1)ᵏΔₖ>0', 'A 实对称。', '是顺序主子式，不是任取主子式（正定时所有主子式也正）。'],
    ['正交变换化二次型', 'A=QΛQᵀ，令 x=Qy\n则 xᵀAx=yᵀΛy=Σλᵢyᵢ²', 'A 实对称，Q 的列为单位正交特征向量。', '重特征值对应空间内也要正交化。'],
    ['秩一矩阵 αβᵀ', 'A=αβᵀ ⇒ r(A)≤1\ntr(A)=βᵀα\n非零特征值（若有）为 βᵀα', 'α、β 为列向量。', '当 βᵀα=0 时矩阵仍可能非零，但所有特征值为 0。', '高频']
  ]);

  add('概率论与数理统计', '随机事件与概率', [
    ['概率加法公式', 'P(A∪B)=P(A)+P(B)−P(AB)\n若 A,B 互斥：P(A∪B)=P(A)+P(B)', '互斥指 AB=∅。', '独立不等于互斥；两个非零概率事件不可能既独立又互斥。'],
    ['条件概率', 'P(A|B)=P(AB)/P(B)，P(B)>0\n乘法公式：P(AB)=P(B)P(A|B)', '条件事件概率非零。', '条件概率改变了样本空间。'],
    ['全概率公式', '若 B₁,…,Bₙ 为完备事件组，则\nP(A)=ΣᵢP(Bᵢ)P(A|Bᵢ)', 'Bᵢ 两两互斥、并集为样本空间，且 P(Bᵢ)>0。', '分组事件必须完整且互斥。'],
    ['贝叶斯公式', 'P(Bᵢ|A)=P(Bᵢ)P(A|Bᵢ) / ΣⱼP(Bⱼ)P(A|Bⱼ)', 'P(A)>0，Bⱼ 为完备事件组。', '分母就是由全概率公式得到的 P(A)。'],
    ['独立性', 'A,B 独立 ⇔ P(AB)=P(A)P(B)\n若独立，则 A 与 B̄、Ā 与 B、Ā 与 B̄ 也独立', '事件概率可以为 0。', 'P(A|B)=P(A) 需要 P(B)>0 才能写。'],
    ['至少一次概率', 'n 次独立试验，单次成功概率 p\nP(至少一次成功)=1−(1−p)ⁿ', '各次试验独立且成功概率相同。', '“至少一次”优先用对立事件。'],
    ['古典概型', 'P(A)=A 所含等可能基本事件数 / 基本事件总数', '样本空间有限且基本事件等可能。', '不等可能时不能只数个数。'],
    ['几何概型', 'P(A)=μ(A)/μ(Ω)', '样本点在区域 Ω 上按长度、面积或体积均匀分布。', '边界通常测度为 0，不影响概率。']
  ]);

  add('概率论与数理统计', '一维随机变量及分布', [
    ['分布函数', 'F(x)=P(X≤x)\nP(a<X≤b)=F(b)−F(a)\nF(−∞)=0，F(+∞)=1', 'F 单调不减、右连续。', '端点是否取到要按事件与跳跃点处理。'],
    ['离散型概率分布', 'P(X=xₖ)=pₖ，pₖ≥0，Σpₖ=1\nF(x)=Σ(xₖ≤x)pₖ', '可数个取值。', '分布函数在取值点跳跃，跳跃大小为该点概率。'],
    ['连续型密度', 'F(x)=∫₋∞ˣ f(t)dt\nf(x)≥0，∫₋∞^∞f(x)dx=1\nP(a<X≤b)=∫ₐᵇf(x)dx', 'F 绝对连续时存在密度。', '连续型随机变量单点概率为 0，但密度值不是概率。'],
    ['0-1 分布', 'X~B(1,p)\nP(X=1)=p，P(X=0)=1−p\nE(X)=p，D(X)=p(1−p)', '0≤p≤1。', '伯努利分布是二项分布 n=1 的情形。'],
    ['二项分布', 'X~B(n,p)\nP(X=k)=Cₙᵏpᵏ(1−p)ⁿ⁻ᵏ\nE(X)=np，D(X)=np(1−p)', 'n 次独立同分布伯努利试验。', 'k=0,1,…,n。'],
    ['泊松分布', 'X~P(λ)\nP(X=k)=e^(−λ)λᵏ/k!\nE(X)=D(X)=λ', 'λ>0，k=0,1,2,…。', '二项分布在 n 大、p 小且 np≈λ 时可近似泊松。'],
    ['几何分布', 'P(X=k)=(1−p)^(k−1)p，k=1,2,…\nE(X)=1/p，D(X)=(1−p)/p²', 'X 表示首次成功所需试验次数。', '若定义为失败次数，取值从 0 开始，公式会平移。'],
    ['均匀分布', 'X~U(a,b)\nf(x)=1/(b−a)，a<x<b\nE(X)=(a+b)/2，D(X)=(b−a)²/12', 'a<b。', '区间外密度为 0。'],
    ['指数分布', 'X~Exp(λ)\nf(x)=λe^(−λx)，x>0\nF(x)=1−e^(−λx)\nE(X)=1/λ，D(X)=1/λ²', 'λ>0。', '参数若采用均值尺度记法会不同，先看题目定义。'],
    ['指数分布无记忆性', 'P(X>s+t | X>s)=P(X>t)=e^(−λt)', 'X 为指数分布，s,t≥0。', '连续分布中指数分布具有此无记忆性。'],
    ['标准正态分布', 'Z~N(0,1)\nφ(z)=e^(−z²/2)/√(2π)\nΦ(z)=P(Z≤z)，Φ(−z)=1−Φ(z)', '查表时按所用表格定义。', 'P(|Z|≤z)=2Φ(z)−1（z≥0）。'],
    ['一般正态标准化', 'X~N(μ,σ²) ⇒ Z=(X−μ)/σ~N(0,1)\nP(a<X≤b)=Φ((b−μ)/σ)−Φ((a−μ)/σ)', 'σ>0。', '标准化除以标准差 σ，不是方差 σ²。'],
    ['随机变量函数的分布（离散）', 'Y=g(X)：\nP(Y=y)=Σ(x:g(x)=y)P(X=x)', '把映射到同一 y 的所有原像概率相加。', 'g 非一一对应时不能只取一个原像。'],
    ['单调变换密度', 'Y=g(X)，g 严格单调，可逆 x=h(y)\nf_Y(y)=f_X(h(y))|h′(y)|', '在对应取值范围内，变换可逆。', '雅可比必须取绝对值；非单调要分支求和。']
  ]);

  add('概率论与数理统计', '多维随机变量', [
    ['联合分布函数', 'F(x,y)=P(X≤x,Y≤y)\n矩形概率=P(a<X≤b,c<Y≤d)\n=F(b,d)−F(a,d)−F(b,c)+F(a,c)', '二维随机变量。', '四项符号按容斥排列。'],
    ['联合密度与边缘密度', 'f(x,y)≥0，∬f dxdy=1\nf_X(x)=∫₋∞^∞f(x,y)dy\nf_Y(y)=∫₋∞^∞f(x,y)dx', '连续型二维随机变量。', '积分范围要结合联合密度的实际支撑区域。'],
    ['条件密度', 'f_{X|Y}(x|y)=f(x,y)/f_Y(y)\nf_{Y|X}(y|x)=f(x,y)/f_X(x)', '相应边缘密度大于 0。', '分母是所给条件变量的边缘密度。'],
    ['随机变量独立判定', '连续型：f(x,y)=f_X(x)f_Y(y)（几乎处处）\n离散型：pᵢⱼ=pᵢ·p·ⱼ\n分布函数：F(x,y)=F_X(x)F_Y(y)', '在全部取值范围成立。', '协方差为 0 一般不能推出独立。'],
    ['二维变量变换密度', 'U=g₁(X,Y), V=g₂(X,Y)\n若逆变换 x=x(u,v),y=y(u,v)，则\nf_{U,V}(u,v)=f_{X,Y}(x,y)|∂(x,y)/∂(u,v)|', '变换分片一一对应，雅可比非零。', '先确定新变量取值区域。'],
    ['和的密度（卷积）', 'Z=X+Y，X,Y 独立：\nf_Z(z)=∫₋∞^∞f_X(x)f_Y(z−x)dx', '连续型且独立。', '不独立时不能用边缘密度直接卷积。'],
    ['差的密度', 'Z=X−Y，X,Y 独立：\nf_Z(z)=∫₋∞^∞f_X(z+y)f_Y(y)dy', '连续型且独立。', '可把差写成 X+(−Y) 再卷积。'],
    ['最大值与最小值分布', 'M=max(X₁,…,Xₙ)：F_M(x)=ΠFᵢ(x)\n若独立同分布：F_M(x)=F(x)ⁿ\nN=min：F_N(x)=1−Π[1−Fᵢ(x)]', '随机变量相互独立。', '最小值用生存函数更直接。'],
    ['二维正态独立性', '(X,Y) 为二维正态时：\nX,Y 独立 ⇔ Cov(X,Y)=0 ⇔ ρ=0', '必须是联合二维正态。', '边缘各自正态且不相关，不一定推出联合正态或独立。']
  ]);

  add('概率论与数理统计', '数字特征与极限定理', [
    ['数学期望', '离散：E(X)=Σxₖpₖ\n连续：E(X)=∫₋∞^∞x f(x)dx\nE[g(X)]=Σg(xₖ)pₖ 或 ∫g(x)f(x)dx', '绝对收敛或期望存在。', '求函数期望通常不必先求新变量分布。'],
    ['期望线性性质', 'E(aX+bY+c)=aE(X)+bE(Y)+c', '只要求相关期望存在，不要求 X,Y 独立。', '期望可拆不代表乘积期望可拆。'],
    ['方差', 'D(X)=E[(X−EX)²]=E(X²)−[E(X)]²\nD(aX+b)=a²D(X)', '二阶矩存在。', '常数平移不改变方差，缩放系数要平方。'],
    ['协方差', 'Cov(X,Y)=E[(X−EX)(Y−EY)]\n=E(XY)−E(X)E(Y)\nCov(aX+b,cY+d)=ac Cov(X,Y)', '二阶矩存在。', 'Cov(X,X)=D(X)。'],
    ['和的方差', 'D(X±Y)=D(X)+D(Y)±2Cov(X,Y)\n一般：D(ΣaᵢXᵢ)=Σaᵢ²D(Xᵢ)+2Σ(i<j)aᵢaⱼCov(Xᵢ,Xⱼ)', '二阶矩存在。', '只有不相关或独立时协方差项才消失。'],
    ['相关系数', 'ρXY=Cov(X,Y)/√[D(X)D(Y)]\n|ρ|≤1\n|ρ|=1 ⇔ Y=aX+b 几乎处处成立（a≠0）', 'D(X),D(Y)>0。', 'ρ=0 只表示线性不相关，一般不等于独立。'],
    ['独立变量的期望与方差', 'X,Y 独立且期望存在 ⇒ E(XY)=E(X)E(Y)\n方差存在 ⇒ D(X±Y)=D(X)+D(Y)', '独立性是充分条件。', '不相关也足以让和的方差相加，但不保证乘积期望在更一般条件下无问题。'],
    ['矩', 'k 阶原点矩：E(Xᵏ)\nk 阶中心矩：E[(X−EX)ᵏ]\n二阶中心矩即方差', '相应期望存在。', '原点矩与中心矩不要混淆。'],
    ['切比雪夫不等式', 'P(|X−μ|≥ε)≤σ²/ε²\nP(|X−μ|<ε)≥1−σ²/ε²', 'E(X)=μ、D(X)=σ²<∞，ε>0。', '给的是上界或下界，通常不是精确概率。'],
    ['大数定律（常用结论）', 'X₁,…,Xₙ 独立同分布，E(Xᵢ)=μ，方差有限\n则样本均值 X̄ 依概率收敛于 μ', '满足相应大数定律条件。', '结论是依概率收敛，不是每个有限样本都等于 μ。'],
    ['中心极限定理', 'Xᵢ iid，E(Xᵢ)=μ，D(Xᵢ)=σ²>0\n(ΣXᵢ−nμ)/(σ√n) ⇒ N(0,1)\n等价：√n(X̄−μ)/σ ⇒ N(0,1)', '独立同分布且方差有限。', '标准化分母是 σ√n；样本均值形式是 σ/√n。'],
    ['二项分布正态近似', 'X~B(n,p)，n 较大时\n(X−np)/√[np(1−p)]≈N(0,1)', 'np 与 n(1−p) 均不太小。', '离散到连续近似可视题意使用连续性修正。']
  ]);

  add('概率论与数理统计', '数理统计基础与参数估计', [
    ['样本均值与样本方差', 'X̄=(1/n)ΣXᵢ\nS²=[1/(n−1)]Σ(Xᵢ−X̄)²\n=[ΣXᵢ²−nX̄²]/(n−1)', 'Xᵢ 为简单随机样本。', '无偏样本方差分母是 n−1。'],
    ['样本均值的期望方差', 'E(X̄)=μ\nD(X̄)=σ²/n', '样本独立同分布，方差存在。', '标准差为 σ/√n。'],
    ['正态总体的抽样分布', '总体 N(μ,σ²)：\nX̄~N(μ,σ²/n)\n(n−1)S²/σ²~χ²(n−1)\nX̄ 与 S² 独立', '来自正态总体的简单随机样本。', 'X̄ 与 S² 独立是正态样本的重要特性。'],
    ['t 分布统计量', 'T=(X̄−μ)/(S/√n)~t(n−1)', '总体正态，σ² 未知。', '用 S 替代 σ 后是 t 分布，不再是标准正态。'],
    ['两个正态总体均值差（方差已知）', 'Z=[(X̄−Ȳ)−(μ₁−μ₂)]/√(σ₁²/n₁+σ₂²/n₂)~N(0,1)', '两独立正态样本，方差已知。', '分母是两项方差之和再开根。'],
    ['合并样本方差', 'Sₚ²=[(n₁−1)S₁²+(n₂−1)S₂²]/(n₁+n₂−2)', '两正态总体方差未知但相等，样本独立。', '不是两个样本方差的简单平均。'],
    ['两个均值差的 t 统计量', 'T=[(X̄−Ȳ)−(μ₁−μ₂)] / [Sₚ√(1/n₁+1/n₂)]\n~t(n₁+n₂−2)', '两独立正态总体、方差未知但相等。', '若方差不等，考纲常规公式不能直接套合并方差。'],
    ['方差比的 F 分布', '(S₁²/σ₁²)/(S₂²/σ₂²)~F(n₁−1,n₂−1)', '两独立正态样本。', '交换分子分母时自由度也要交换。'],
    ['矩估计法', '用样本矩替换总体矩：\n(1/n)ΣXᵢᵏ = Eθ(Xᵏ)\n解出参数 θ̂', '选择与参数个数相同的矩方程。', '矩估计量是样本的函数，不含未知参数。'],
    ['最大似然估计（离散）', 'L(θ)=ΠᵢPθ(X=xᵢ)\nθ̂=arg max L(θ)', '样本独立同分布，参数属于给定空间。', '最大化时要检查参数边界。'],
    ['最大似然估计（连续）', 'L(θ)=Πᵢf(xᵢ;θ)\nℓ(θ)=ln L(θ)=Σln f(xᵢ;θ)\n解 ℓ′(θ)=0 并核验最大值', '联合密度由独立性写成乘积。', '似然是参数的函数，样本值视为已知。'],
    ['无偏性', '若 E(θ̂)=θ，则 θ̂ 为 θ 的无偏估计\n样本均值是 μ 的无偏估计；S² 是 σ² 的无偏估计', '期望存在。', '无偏不等于估计误差一定小。'],
    ['有效性', '在同类无偏估计量中，方差更小者更有效', '比较对象都无偏，并估计同一参数。', '有效性是相对概念。'],
    ['一致性', 'θ̂ₙ 依概率收敛于 θ', '样本量 n→∞。', '一致性是大样本性质，与无偏性不同。']
  ]);

  add('概率论与数理统计', '区间估计与假设检验', [
    ['正态均值置信区间（σ 已知）', 'μ 的 1−α 置信区间：\nX̄ ± z_(α/2)·σ/√n', '总体正态；或大样本近似，σ 已知。', 'z_(α/2) 通常满足 P(Z>z_(α/2))=α/2。'],
    ['正态均值置信区间（σ 未知）', 'μ 的 1−α 置信区间：\nX̄ ± t_(α/2)(n−1)·S/√n', '总体正态，σ 未知。', '自由度为 n−1。'],
    ['正态方差置信区间', 'σ² 的 1−α 置信区间：\n((n−1)S²/χ²_(α/2)(n−1),\n (n−1)S²/χ²_(1−α/2)(n−1))', '总体正态；这里 χ²_p 表示右尾概率为 p 的临界值时注意所用表定义。', '上下端点因分母大小而反序；先确认教材临界值记号。'],
    ['单总体均值 Z 检验', 'H₀:μ=μ₀，σ 已知\nZ=(X̄−μ₀)/(σ/√n)\n双侧拒绝域 |Z|≥z_(α/2)', '正态总体或大样本，σ 已知。', '单侧检验临界值和方向由备择假设决定。'],
    ['单总体均值 t 检验', 'H₀:μ=μ₀，σ 未知\nT=(X̄−μ₀)/(S/√n)\n双侧拒绝域 |T|≥t_(α/2)(n−1)', '总体正态，σ 未知。', '不要把未知 σ 直接写进统计量。'],
    ['单总体方差 χ² 检验', 'H₀:σ²=σ₀²\nχ²=(n−1)S²/σ₀²~χ²(n−1)', '正态总体。', '双侧检验有两个临界区域，且 χ² 分布不对称。'],
    ['两总体均值差 Z 检验', 'H₀:μ₁−μ₂=δ₀\nZ=[(X̄−Ȳ)−δ₀]/√(σ₁²/n₁+σ₂²/n₂)', '独立正态样本，方差已知。', '若配对样本，应先转化为差值的单样本问题。'],
    ['两总体均值差 t 检验', 'H₀:μ₁−μ₂=δ₀\nT=[(X̄−Ȳ)−δ₀]/[Sₚ√(1/n₁+1/n₂)]', '独立正态总体，方差未知但相等。', '自由度 n₁+n₂−2。'],
    ['两总体方差比 F 检验', 'H₀:σ₁²=σ₂²\nF=S₁²/S₂²~F(n₁−1,n₂−1)', '两独立正态总体。', '双侧检验两端临界值可用倒数关系转换。'],
    ['第一、第二类错误', '第一类错误：H₀ 真却拒绝，概率 α\n第二类错误：H₀ 假却未拒绝，概率 β\n检验功效=1−β', '在给定检验规则与具体备择参数下。', '样本量固定时压低 α 往往会增大 β。'],
    ['P 值判决', 'P 值=在 H₀ 下获得当前或更极端样本结果的概率\nP≤α ⇒ 拒绝 H₀', '“更极端”的方向由单侧或双侧备择决定。', 'P 值不是 H₀ 为真的概率。']
  ]);

  const STORAGE_KEY = 'tpm-math-formulas-v1';
  const $ = (selector) => document.querySelector(selector);
  const groupsRoot = $('#formula-groups');
  const indexRoot = $('#formula-index');
  const searchInput = $('#formula-search');
  const subjectSelect = $('#formula-subject');
  const chapterSelect = $('#formula-chapter');
  const stateSelect = $('#formula-state');
  let marks = {};

  try { marks = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {}; } catch (_) { marks = {}; }
  const saveMarks = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(marks)); } catch (_) {} };
  const escapeHTML = (value) => String(value).replace(/[&<>"]/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));
  const slug = (value) => `fm-${Array.from(value).map((ch) => ch.codePointAt(0).toString(16)).join('-')}`;

  const chapterOrder = [];
  const subjectChapters = new Map();
  formulas.forEach((item) => {
    if (!subjectChapters.has(item.subject)) subjectChapters.set(item.subject, []);
    const list = subjectChapters.get(item.subject);
    if (!list.includes(item.chapter)) list.push(item.chapter);
    if (!chapterOrder.includes(item.chapter)) chapterOrder.push(item.chapter);
    item.search = `${item.subject} ${item.chapter} ${item.title} ${item.formula} ${item.condition} ${item.pitfall} ${item.level}`.toLowerCase();
  });

  function cardHTML(item) {
    const mark = marks[item.id] || '';
    const status = mark === 'review' ? '待复习' : mark === 'mastered' ? '已掌握' : '未标记';
    return `<details class="formula-card" id="${item.id}" data-id="${item.id}" data-subject="${escapeHTML(item.subject)}" data-chapter="${escapeHTML(item.chapter)}">
      <summary><span class="formula-card-title">${escapeHTML(item.title)}</span><span class="formula-card-number">${item.id.toUpperCase()}</span><span class="formula-card-summary">${escapeHTML(item.formula.split('\n')[0])}</span></summary>
      <div class="formula-card-body">
        <div class="formula-box"><pre class="formula-expression">${escapeHTML(item.formula)}</pre></div>
        <div class="formula-meta"><h4>适用条件</h4><p>${escapeHTML(item.condition)}</p></div>
        <div class="formula-meta warning"><h4>易错提醒</h4><p>${escapeHTML(item.pitfall)}</p></div>
        <div class="formula-actions"><span class="formula-level">${escapeHTML(item.level)}</span><button class="button" type="button" data-mark="review" aria-pressed="${mark === 'review'}">待复习</button><button class="button" type="button" data-mark="mastered" aria-pressed="${mark === 'mastered'}">已掌握</button><a class="button-link" href="#${item.id}">定位链接</a><span class="formula-state-text">${status}</span></div>
      </div>
    </details>`;
  }

  function renderStructure() {
    const html = [];
    for (const [subject, chapters] of subjectChapters) {
      const subjectItems = formulas.filter((item) => item.subject === subject);
      html.push(`<section class="formula-subject" data-formula-subject="${escapeHTML(subject)}"><div class="formula-subject-head"><div><div class="kicker">数学一 · 公式</div><h2>${escapeHTML(subject)}</h2></div><p>${subjectItems.length} 条 · ${chapters.length} 章</p></div>`);
      chapters.forEach((chapter) => {
        const items = formulas.filter((item) => item.subject === subject && item.chapter === chapter);
        html.push(`<section class="formula-chapter" id="${slug(chapter)}" data-formula-chapter="${escapeHTML(chapter)}"><div class="formula-chapter-head"><h3>${escapeHTML(chapter)}</h3><span>${items.length} 条</span></div><div class="formula-card-list">${items.map(cardHTML).join('')}</div></section>`);
      });
      html.push('</section>');
    }
    groupsRoot.innerHTML = html.join('');
    indexRoot.innerHTML = Array.from(subjectChapters, ([subject, chapters]) => `<div class="index-subject">${escapeHTML(subject)}</div>${chapters.map((chapter) => `<a href="#${slug(chapter)}"><span>${escapeHTML(chapter)}</span><span class="index-count">${formulas.filter((item) => item.chapter === chapter).length}</span></a>`).join('')}`).join('');
    chapterSelect.innerHTML = '<option value="">全部章节</option>' + chapterOrder.map((chapter) => `<option value="${escapeHTML(chapter)}">${escapeHTML(chapter)}</option>`).join('');
    $('#formula-total').textContent = formulas.length;
    $('#chapter-total').textContent = chapterOrder.length;
  }

  function applyFilters() {
    const keyword = searchInput.value.trim().toLowerCase();
    const subject = subjectSelect.value;
    const chapter = chapterSelect.value;
    const state = stateSelect.value;
    let visible = 0;
    document.querySelectorAll('.formula-card').forEach((card) => {
      const item = formulas.find((entry) => entry.id === card.dataset.id);
      const mark = marks[item.id] || '';
      const stateMatch = !state || (state === 'unmarked' ? !mark : mark === state);
      const show = (!keyword || item.search.includes(keyword)) && (!subject || item.subject === subject) && (!chapter || item.chapter === chapter) && stateMatch;
      card.hidden = !show;
      if (show) visible += 1;
    });
    document.querySelectorAll('.formula-chapter').forEach((section) => { section.hidden = !section.querySelector('.formula-card:not([hidden])'); });
    document.querySelectorAll('.formula-subject').forEach((section) => { section.hidden = !section.querySelector('.formula-chapter:not([hidden])'); });
    $('#formula-count').textContent = `显示 ${visible} / ${formulas.length} 条`;
    $('#formula-empty').hidden = visible !== 0;
    [...chapterSelect.options].forEach((option, index) => {
      if (index === 0) return;
      option.hidden = Boolean(subject) && !formulas.some((item) => item.subject === subject && item.chapter === option.value);
    });
  }

  renderStructure();
  applyFilters();
  [searchInput, subjectSelect, chapterSelect, stateSelect].forEach((control) => control.addEventListener(control === searchInput ? 'input' : 'change', applyFilters));
  subjectSelect.addEventListener('change', () => {
    if (chapterSelect.selectedOptions[0]?.hidden) chapterSelect.value = '';
    applyFilters();
  });
  groupsRoot.addEventListener('click', (event) => {
    const button = event.target.closest('[data-mark]');
    if (!button) return;
    const card = button.closest('.formula-card');
    const id = card.dataset.id;
    const next = button.dataset.mark;
    marks[id] = marks[id] === next ? '' : next;
    if (!marks[id]) delete marks[id];
    saveMarks();
    card.querySelectorAll('[data-mark]').forEach((item) => item.setAttribute('aria-pressed', String(marks[id] === item.dataset.mark)));
    card.querySelector('.formula-state-text').textContent = marks[id] === 'review' ? '待复习' : marks[id] === 'mastered' ? '已掌握' : '未标记';
    applyFilters();
  });
  $('#formula-reset').addEventListener('click', () => { searchInput.value = ''; subjectSelect.value = ''; chapterSelect.value = ''; stateSelect.value = ''; applyFilters(); searchInput.focus(); });
  $('#formula-collapse').addEventListener('click', () => { document.querySelectorAll('.formula-card[open]').forEach((card) => { card.open = false; }); });
  $('#formula-print').addEventListener('click', () => window.print());
  $('#formula-random').addEventListener('click', () => {
    const visible = [...document.querySelectorAll('.formula-card:not([hidden])')];
    if (!visible.length) return;
    const card = visible[Math.floor(Math.random() * visible.length)];
    card.open = true;
    card.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
    card.classList.remove('formula-flash');
    requestAnimationFrame(() => card.classList.add('formula-flash'));
  });
  window.addEventListener('storage', (event) => {
    if (event.key !== STORAGE_KEY) return;
    try { marks = JSON.parse(event.newValue || '{}') || {}; } catch (_) { marks = {}; }
    renderStructure(); applyFilters();
  });
  if (location.hash && /^#m\d{3}$/.test(location.hash)) {
    requestAnimationFrame(() => { const card = document.querySelector(location.hash); if (card) card.open = true; });
  }
})();
