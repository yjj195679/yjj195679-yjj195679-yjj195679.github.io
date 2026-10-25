# True Path M · 个人网站

[中文网站](https://1956799.xyz/) · [English](https://1956799.xyz/en/) · [GitHub](https://github.com/yjj195679)

这是一个使用原生 HTML、CSS 和 JavaScript 构建的双语个人网站，直接托管于 GitHub Pages。网站集中展示个人简介、项目实践、学习方向、方法总结、竞赛成果与生活记录，并提供公开留言板。

## 页面结构

| 栏目 | 中文页面 | 英文页面 | 内容结构 |
| --- | --- | --- | --- |
| 首页 | `index.html` | `en/index.html` | 总览、简介、项目入口、历程、天气、联系 |
| 项目 | `projects.html` | `en/projects.html` | 背景、过程、结果、复盘 |
| 方法 | `education.html` | `en/education.html` | 定义、推演、验证、复盘 |
| 学习 | `courses.html` | `en/courses.html` | 学习方向、专题与知识联系 |
| 成果 | `achievements.html` | `en/achievements.html` | 完成、证据、影响、反思 |
| 生活 | `life.html` | `en/life.html` | 日常、兴趣、阅读、片段 |
| 留言板 | `guestbook.html` | `en/guestbook.html` | 公开留言与反馈 |

## 保留功能

- 中文与英文页面一一对应；
- 多页面导航、当前栏目高亮、滚动联动页内导航与移动端章节折叠；
- 跟随系统、浅色、深色三种外观模式；
- 每个栏目独立背景图；
- 12 / 8 / 4 列栅格，对应桌面、平板与移动端三个核心断点；
- 快捷搜索、阅读模式、复制链接、打印与返回顶部；
- 当前时间、日期与按需天气，天气结果在当前会话短时缓存；
- 站内页面悬停预取、留言加载骨架与输入字符计数；
- Supabase 留言板及带 TOTP 验证的管理页；
- 键盘操作、减少动态效果和无脚本可读性支持；
- Open Graph、`hreflang`、站点地图与自定义 404 页面。

## 内容填写原则

1. 只填写已经确认的真实内容，不用无关文字填满版面。
2. 项目按“问题—过程—结果—复盘”组织，结果必须有可核对依据。
3. 学习页记录知识结构和关键联系，不机械堆砌目录。
4. 成果页区分事实、证据、影响和限制，不提前写结论。
5. 中英文页面同步修改，保持标题层级和锚点一致。

## 目录

```text
.
├── index.html
├── projects.html
├── education.html
├── courses.html
├── achievements.html
├── life.html
├── guestbook.html
├── admin.html
├── 404.html
├── en/
├── css/style.css
├── js/
│   ├── main.js
│   ├── theme.js
│   ├── guestbook.js
│   └── admin.js
├── images/
├── supabase/
├── CNAME
├── robots.txt
└── sitemap.xml
```

## 本地查看

这是纯静态网站，可以直接打开 `index.html`，也可以在仓库根目录启动任意静态文件服务器。天气定位与部分浏览器 API 在 `http://localhost` 或 HTTPS 环境下工作更稳定。

## 部署

仓库使用 GitHub Pages。发布时应确保 `index.html`、`CNAME`、`css/`、`js/`、`images/`、`en/` 等文件位于发布根目录，并保留 `.nojekyll` 处理逻辑。自定义域名为 `1956799.xyz`。

## 留言板

留言板连接 Supabase 项目，前端只包含可公开的 publishable key。管理员登录、TOTP 验证、公开/隐藏与回复逻辑位于 `admin.html` 和 `js/admin.js`；数据库策略脚本位于 `supabase/`。不要把 secret key、service role key、管理员密码或恢复码写入仓库。

## 408 复习专题

- `408.html`：四科分章节的 230 条概念辨析，个人错题、易错、易混、冷门与近年考查标签。
- `408-calculations.html`：8 道独立计算变式与步骤。
- `data/408-knowledge.json` 为内容源，`python tools/build-408.py` 重建两页。
- 内容以静态 HTML 提供，不依赖网络 API；关闭脚本仍可展开解析。
- 复习标记位于浏览器本地存储，两页共用并相互保留，未使用账户或数据库。
- 近年考查标注的是已核对题目，不代表下一年命题概率。

复习标记按知识点单独保存（v2），避免不同标签页覆盖彼此的独立修改；读取时兼容旧版 v1 标记。

交互逻辑回归测试：安装测试用 `linkedom` 后运行 `node tools/check-408.cjs`。测试涵盖站点脚本集成、筛选、标记、旧记录兼容、多标签页同步与打印状态恢复；测试依赖不参与线上页面加载。

## 408 记忆概念与结构图

230 条概念卡按四科章节目录组织，每条具备定义、条件、辨析、例子与自检。新增 B 树高度公式、乘除法、计时器及主要章节补全，保留独立计算专项。

`python tools/build-408-diagrams.py` 生成 6 张原创 SVG，再用 `python tools/build-408.py` 重建页面与同步标记编号上限。示意图使用自包含矢量、语义说明和可横向滚动容器；图中寄存器和位宽模型不冒充通用处理器的固定电路。

公式和图文检查可运行 `python tools/check-408-math.py`（Python 标准库），覆盖位宽边界、B 树高度和 SVG 语义/结构。

2026-10-20：补充 18 条阶段与状态名称对照（TCP 建立/释放/特殊转换、拥塞控制、DHCP、PPP、介质访问、指令周期/流水线、中断/DMA、进程状态/挂起、资源安全、临界区、DFS、内外排序）。原有 ID 和复习记录保留。

阶段/状态图解：运行 `python tools/build-408-state-diagrams.py` 生成并关联 18 张 SVG，再运行 `python tools/build-408.py` 重建页面。目前共 25 条图解卡；图解支持明暗主题、横向滚动、单独查看与文字说明。

2026-10-20：新增打开文件表关系卡 k230（文件系统），区分教材二表模型与 UNIX/Linux 三层实现，列明位置指针、打开方式、文件保护权限及引用计数，配原创图 `open-file-tables.svg`。运行 `python tools/build-408-open-files-diagram.py` 可重新生成该图。

打开文件表卡已精简为速记、两行字段对照和教材关系图；UNIX/Linux 实现差异与参考折叠展示。

## 408 全量内容复核与阅读层次（2026-10-20）

复核范围：230 条概念、25 张 SVG 图解、8 道计算变式。每条概念新增独立的 `review_tip`；默认先显示正确结论与易混提醒，表格/图解保留，原理、误解、例子、代码与参考放入可展开解析。计算专项先显示题目与提醒，答案和步骤按需展开。原编号及复习标记保持兼容。

明确关键路径延长、红黑树完整约束、不安全状态定义、调度等待时间、LRU 栈性质、驻留集与置换组合、TIME_WAIT 对 FIN 的确认以及延迟 ACK 的计时边界。教材二表模型与 UNIX/Linux 文件实现继续区分。相关真题引用沿用已有标注，本轮没有重新逐题比对全部外链原卷。

## 数学一公式库

- `math-formulas.html`：依据数学一考纲整理的 244 条公式与定理结论，覆盖高等数学、线性代数、概率论与数理统计共 19 章。
- 每条内容同时标注适用条件和易错提醒，长公式按移动端阅读拆行。
- 支持关键词搜索、科目/章节/掌握状态筛选、随机抽查、浏览器本地掌握度标记及打印导出。
- 页面逻辑位于 `js/math-formulas.js`，样式位于 `css/math-formulas.css`；不依赖网络 API。
