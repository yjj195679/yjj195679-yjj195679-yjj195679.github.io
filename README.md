# True Path M · Personal Portfolio

> 一个用于长期记录个人经历、研究项目、学习路径与阶段成果的纯静态多页面网站。

- 在线访问：[https://1956799.xyz](https://1956799.xyz)
- GitHub 主页：[https://github.com/yjj195679](https://github.com/yjj195679)
- 当前仓库：[yjj195679/yjj195679-yjj195679-yjj195679.github.io](https://github.com/yjj195679/yjj195679-yjj195679-yjj195679.github.io)

本项目使用原生 HTML、CSS 和 JavaScript 编写，不依赖 Node.js、前端框架或第三方 JavaScript CDN。网站由 GitHub Pages 托管，`1956799.xyz` 作为自定义域名；公开留言通过 Supabase Data REST API 读写，首页天气通过 Open-Meteo API 按需获取。

---

## 1. 项目定位

网站主要展示：

- 图像复原、深度学习与优化算法相关项目；
- Primal–Dual 去模糊、DPSR、UNet、Restormer 等实践经历；
- 数据结构、计算机组成原理、操作系统、计算机网络等 408 学习内容；
- 高等数学、线性代数、概率论与优化方法的学习路径；
- 阶段成果、生活记录和后续计划；
- 访客公开留言。

网站采用“首页概览 + 独立子页面”的多页面结构。各页面共享统一导航、视觉变量和交互脚本，同时保留独立背景和内容组织，便于以后继续增加项目、文档、图片或新的栏目。

---

## 2. 已实现功能

### 2.1 页面与内容

| 页面 | 文件 | 主要内容 |
| --- | --- | --- |
| 首页 | `index.html` | 个人简介、研究方向、工具栈、代表项目、学习路径、快捷入口、天气与联系方式 |
| 项目 | `projects.html` | DPSR、Primal–Dual 去模糊、UNet / Restormer 实验及工程问题处理 |
| 教育与学习路径 | `education.html` | 计算机与数学基础、论文复现、实验验证和个人学习闭环 |
| 学习地图 | `courses.html` | 408、数学、图像处理、深度学习与优化方法 |
| 阶段成果 | `achievements.html` | 已完成的研究复现、实验工程、报告和网站建设成果 |
| 生活 | `life.html` | 近期状态、学习记录、网站维护与技术之外的内容 |
| 留言板 | `guestbook.html` | 公开留言的读取、展示、输入校验与提交 |
| 404 | `404.html` | 无效路径的友好提示与返回入口 |

### 2.2 视觉与交互

- 深色学术风格，主色为黑、白、灰和低饱和浅蓝；
- 半透明玻璃面板、细边框、柔和阴影和背景渐变遮罩；
- 中文优先使用宋体字形，英文优先使用 Times New Roman；
- 首页及各子页面使用独立 WebP 背景图；
- 固定顶部导航，当前页面通过 `aria-current="page"` 高亮；
- 导航项保留下划线悬停动效；
- 桌面端和移动端响应式布局；
- 屏幕宽度不大于 980 px 时切换为折叠菜单；
- 屏幕宽度不大于 640 px 时进一步压缩间距和字号；
- 使用 `IntersectionObserver` 实现元素滚动渐入；
- 使用 `requestAnimationFrame` 实现轻量背景视差；
- 实时时钟每秒刷新，页脚年份自动更新；
- 支持 Esc 关闭移动菜单，窗口变宽时自动复位菜单状态；
- 为键盘用户提供跳转到正文链接和清晰的焦点样式；
- 尊重 `prefers-reduced-motion: reduce`，减少或关闭非必要动画。

### 2.3 数据与外部服务

- 留言板直接调用 Supabase 自动生成的 PostgREST 接口；
- 仅加载 `is_visible = true` 的最近 30 条留言；
- 留言按创建时间倒序显示；
- 名字限制为 1–40 个字符，正文限制为 1–500 个字符；
- 使用隐藏蜜罐字段过滤最基础的机器人提交；
- 使用 `localStorage` 设置 30 秒前端提交冷却；
- 网络请求设置 12 秒超时；
- 使用 `textContent` 渲染访客输入，不把留言拼接为 HTML；
- 天气功能只有在访客主动点击后才请求浏览器定位；
- 坐标只用于向 Open-Meteo 发起当次查询，本站不保存定位结果。

### 2.4 SEO 与基础站点文件

- 每个主要页面都有独立的 `title`、`description` 和 canonical URL；
- 首页提供 Open Graph 标题、描述、网址和分享图；
- `robots.txt` 允许搜索引擎抓取并声明站点地图；
- `sitemap.xml` 收录全部主要页面；
- `favicon.svg` 提供站点图标；
- `404.html` 作为 GitHub Pages 自定义错误页面；
- `CNAME` 固定记录当前自定义域名 `1956799.xyz`。

---

## 3. 技术架构

| 层级 | 使用技术 | 职责 |
| --- | --- | --- |
| 页面结构 | HTML5 | 语义化页面、导航、栏目、表单和 SEO 元信息 |
| 视觉样式 | CSS3 | 主题变量、网格布局、玻璃效果、背景、响应式和可访问性样式 |
| 通用交互 | 原生 JavaScript | 时钟、年份、移动菜单、滚动显现、背景视差和天气查询 |
| 留言功能 | 原生 JavaScript + Fetch API | 表单校验、Supabase REST 请求、超时、状态提示和安全渲染 |
| 数据存储 | Supabase Postgres | 留言表、字段约束、权限授予与 RLS 策略 |
| 天气服务 | Open-Meteo | 根据浏览器授权的位置返回当前天气 |
| 静态托管 | GitHub Pages | 从 `main` 分支根目录发布网站 |
| 域名解析 | DNS / Cloudflare | 将 `1956799.xyz` 指向 GitHub Pages |

数据流如下：

1. 浏览器从 GitHub Pages 获取 HTML、CSS、JavaScript 和 WebP 图片；
2. 普通页面在浏览器内完成全部交互，不需要应用服务器；
3. 留言页通过 HTTPS 请求 Supabase `/rest/v1/messages`；
4. Supabase 根据 Postgres grants 和 RLS 决定是否允许查询或插入；
5. 天气按钮被点击后，浏览器先请求定位权限，再直接访问 Open-Meteo；
6. GitHub Pages 与 Supabase 相互独立，留言服务异常不会影响其他静态页面打开。

---

## 4. 目录结构

```text
.
├── index.html
├── projects.html
├── education.html
├── courses.html
├── achievements.html
├── life.html
├── guestbook.html
├── 404.html
├── CNAME
├── favicon.svg
├── robots.txt
├── sitemap.xml
├── README.md
├── css/
│   └── style.css
├── js/
│   ├── main.js
│   └── guestbook.js
└── images/
    ├── hero.webp
    ├── project.webp
    ├── edu.webp
    ├── course.webp
    ├── achieve.webp
    └── life.webp
```

当前六张 WebP 背景图均小于 150 KB，适合在保证清晰度的同时控制首屏资源体积。

---

## 5. 从零实现本网站的步骤

### 5.1 建立静态项目骨架

创建项目目录，并在根目录建立 `index.html`。随后将公共资源按类型放入 `css/`、`js/` 和 `images/`，子页面继续放在根目录中。这样所有页面都可以使用一致的相对路径：

```html
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js" defer></script>
```

本项目没有构建步骤，也不会生成 `dist/` 或 `build/` 目录；仓库中的文件就是浏览器最终读取的文件。

### 5.2 统一每个页面的基础结构

每个页面都应至少包含：

1. `<!doctype html>` 和 `lang="zh-CN"`；
2. UTF-8 编码和移动端 viewport；
3. 独立的页面标题、描述和 canonical URL；
4. `favicon.svg` 与 `css/style.css`；
5. 跳转到正文的 `.skip-link`；
6. `.site-bg` 和 `.noise` 背景层；
7. 统一顶部导航；
8. 带有 `id="main"` 的主要内容；
9. 统一页脚；
10. 使用 `defer` 加载 `js/main.js`。

`body` 的 `data-page` 决定页面背景，例如：

```html
<body data-page="projects">
```

`css/style.css` 中再通过同名属性映射背景：

```css
body[data-page="projects"] {
  --page-image: url("../images/project.webp");
}
```

当前可用值包括 `home`、`projects`、`education`、`study`、`achievements`、`life`、`guestbook` 和 `404`。没有单独映射的页面会使用 `hero.webp` 作为默认背景。

### 5.3 维护统一导航和当前页面高亮

各页面的导航链接应保持相同顺序。当前页面对应的链接添加：

```html
aria-current="page"
```

例如在项目页中：

```html
<a href="projects.html" aria-current="page">Projects</a>
```

添加新页面时，需要同步修改所有现有 HTML 页面中的导航。如果只修改其中一个页面，桌面端和移动端就会出现入口不一致的问题。

### 5.4 建立全局视觉系统

全站颜色、圆角、阴影、最大内容宽度和字体位于 `css/style.css` 顶部的 `:root` 中：

```css
:root {
  --bg: #080a0f;
  --surface: rgba(14, 18, 27, 0.72);
  --text: #f5f7fb;
  --muted: #aeb7c6;
  --accent: #b9d5ff;
  --radius-lg: 30px;
  --radius-md: 22px;
  --max-width: 1180px;
  --font-serif: "Times New Roman", "Songti SC", SimSun, serif;
}
```

需要更换主题时，优先修改这些变量，而不是逐个修改组件。主要复用组件包括：

- `.container`：统一内容宽度；
- `.glass`：玻璃面板；
- `.panel`：通用内容卡片；
- `.button` / `.button-link`：操作按钮；
- `.section-head`：栏目标题；
- `.tags` / `.tag`：技术标签；
- `.timeline`：时间线；
- `.reveal`：滚动显现目标；
- `.page-hero`：子页面首屏区域。

### 5.5 实现公共 JavaScript 交互

`js/main.js` 使用立即执行函数包裹，避免变量污染全局作用域，主要完成以下工作：

1. 根据系统时间更新页脚年份；
2. 每秒刷新顶部中文格式时钟；
3. 切换移动端导航的 `.open` 和 `body.menu-open` 状态；
4. 同步 `aria-expanded`，让辅助技术识别菜单状态；
5. 监听 Esc、导航点击和窗口尺寸变化以关闭菜单；
6. 使用 `IntersectionObserver` 为可见元素添加 `.visible`；
7. 使用被动滚动监听与 `requestAnimationFrame` 控制背景位移；
8. 在减少动态效果模式下跳过背景视差；
9. 处理定位授权、天气请求、中文天气代码映射和错误提示。

天气服务不需要 API Key。接口在点击按钮后按以下顺序运行：

1. 访客点击天气按钮；
2. 浏览器请求定位权限；
3. 获得经纬度后请求 Open-Meteo；
4. 解析温度、体感温度、湿度、天气代码和风速；
5. 更新页面中的天气信息。

定位通常要求 HTTPS 或本地开发环境。拒绝定位、请求超时或服务异常时，页面会给出对应提示，不会阻塞网站其他功能。

### 5.6 准备并压缩背景图片

推荐为每个主要栏目准备一张横向图片，统一转换为 WebP，并尽量控制在 150 KB 内。替换图片时应：

1. 保持文件名不变，或同步修改所有 HTML / CSS 引用；
2. 使用小写英文文件名，避免服务器大小写差异；
3. 在桌面和手机尺寸上检查主体是否被裁切；
4. 确认文字区域仍有足够对比度；
5. 清理浏览器缓存后再次确认新图片已加载；
6. 不要把原始超大图片与压缩图一起提交到发布目录。

---

## 6. 本地运行与开发

### 6.1 克隆仓库

```bash
git clone https://github.com/yjj195679/yjj195679-yjj195679-yjj195679.github.io.git
cd yjj195679-yjj195679-yjj195679.github.io
```

### 6.2 启动本地服务器

如果已经安装 Python 3，可在仓库根目录执行：

```bash
python -m http.server 8000
```

Windows 中如果 `python` 命令不可用，可以尝试：

```bash
py -m http.server 8000
```

然后访问：

```text
http://localhost:8000/
```

停止服务器时在终端按 `Ctrl + C`。

不建议直接双击 HTML 后通过 `file://` 预览，因为浏览器在本地文件模式下对网络请求、路径和安全策略的处理可能与 HTTP 环境不同，尤其会影响留言板和天气功能的排查。

### 6.3 推荐开发顺序

1. 修改 HTML 文案或栏目结构；
2. 在本地逐页检查链接；
3. 调整 `css/style.css`；
4. 检查 980 px 和 640 px 两个响应式区间；
5. 检查 `js/main.js` 与 `js/guestbook.js` 的控制台错误；
6. 测试留言读取与提交；
7. 更新 `sitemap.xml` 和相关 SEO 元信息；
8. 提交并推送到 `main`；
9. 等待 GitHub Pages 完成新版本发布；
10. 在正式域名上再次做一次完整检查。

---

## 7. Supabase 留言板配置

### 7.1 工作原理

`js/guestbook.js` 不引入 `supabase-js`，而是直接使用浏览器 Fetch API 请求：

```text
https://<project-ref>.supabase.co/rest/v1/messages
```

脚本中需要配置两个公开值：

```js
const SUPABASE_URL = "https://<project-ref>.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "<publishable-key>";
```

publishable key 本来就是供浏览器使用的公开标识，不应被当作数据库安全边界。真正的权限边界必须由 Postgres grants、字段约束和 Row Level Security（RLS）共同建立。任何 `secret` 或 `service_role` key 都不能写入 HTML、JavaScript、Git 仓库或浏览器代码。

### 7.2 建表示例

在 Supabase Dashboard 的 SQL Editor 中执行下面的配置，可以建立与当前前端相匹配的 `messages` 表：

```sql
create table if not exists public.messages (
  id bigint generated always as identity primary key,
  name text not null,
  content text not null,
  created_at timestamptz not null default now(),
  is_visible boolean not null default true,
  constraint messages_name_length
    check (char_length(btrim(name)) between 1 and 40),
  constraint messages_content_length
    check (char_length(btrim(content)) between 1 and 500)
);

alter table public.messages enable row level security;

revoke all on table public.messages from anon, authenticated;
grant select (name, content, created_at, is_visible)
  on table public.messages to anon, authenticated;
grant insert (name, content)
  on table public.messages to anon, authenticated;
grant usage on sequence public.messages_id_seq to anon, authenticated;

drop policy if exists "public can read visible messages" on public.messages;
create policy "public can read visible messages"
on public.messages
for select
to anon, authenticated
using (is_visible = true);

drop policy if exists "public can create messages" on public.messages;
create policy "public can create messages"
on public.messages
for insert
to anon, authenticated
with check (
  char_length(btrim(name)) between 1 and 40
  and char_length(btrim(content)) between 1 and 500
);
```

如果表不是由上述 SQL 新建，identity sequence 的实际名称可能不同。可以在 Supabase 的 Table Editor 或 SQL Editor 中确认序列名后再执行 `grant usage`。

这组权限达到的效果是：

- 匿名访客只能读取公开留言；
- 匿名访客只能插入 `name` 和 `content`；
- 客户端不能自行设置 `id`、`created_at` 或 `is_visible`；
- 客户端不能更新或删除任何留言；
- 即使访客直接绕过网页调用 REST API，数据库仍会执行字段约束和 RLS。

### 7.3 前端查询

当前加载请求等价于：

```text
?select=name,content,created_at
&is_visible=eq.true
&order=created_at.desc
&limit=30
```

提交请求只发送：

```json
{
  "name": "访客昵称",
  "content": "留言正文"
}
```

### 7.4 留言审核

网页端不提供管理员入口。需要隐藏某条留言时，在 Supabase Dashboard 的 Table Editor 中把该行的 `is_visible` 改为 `false`。前端下一次加载时将不再显示该留言，但数据仍保留在数据库中。

如果确认不再需要某条数据，可以在 Supabase 后台删除；不要为了管理留言而把更新或删除权限开放给 `anon`。

### 7.5 防滥用说明

蜜罐字段、长度校验和 30 秒 `localStorage` 冷却只能降低普通误操作和简单机器人提交，不能替代服务端限流。若未来遭遇大量垃圾留言，应把写入过程迁移到 Supabase Edge Function 或其他受控后端，并增加验证码、IP / 会话限流和内容审核。

官方参考：

- [Supabase Data REST API](https://supabase.com/docs/guides/api)
- [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase API keys](https://supabase.com/docs/guides/getting-started/api-keys)

---

## 8. GitHub Pages 发布

### 8.1 发布源设置

本项目是无需构建的静态站点，适合直接从分支发布：

1. 打开仓库的 **Settings**；
2. 进入 **Pages**；
3. 在 **Build and deployment** 中选择 **Deploy from a branch**；
4. Branch 选择 `main`；
5. Folder 选择 `/(root)`；
6. 保存并等待首次部署完成。

`index.html` 必须位于所选发布目录的顶层。本仓库不需要 npm install、打包命令或 GitHub Actions 构建脚本。

### 8.2 提交并发布修改

```bash
git status
git add .
git commit -m "Update portfolio content"
git push origin main
```

推送完成后，GitHub Pages 会重新发布站点。可以在仓库的 **Actions** 或 **Settings / Pages** 中查看部署状态。

官方参考：[Configuring a publishing source for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

---

## 9. 自定义域名 `1956799.xyz`

### 9.1 仓库配置

仓库根目录中的 `CNAME` 只能包含一行：

```text
1956799.xyz
```

同时依次进入 **Settings**、**Pages**、**Custom domain**，填写 `1956799.xyz` 并保存。不要把协议、路径或多余空格写入 `CNAME`，例如不要写 `https://1956799.xyz/`。

### 9.2 Cloudflare / DNS 配置

`1956799.xyz` 是根域名，可为主机名 `@` 添加 GitHub Pages 官方 A 记录：

| 类型 | 名称 | 内容 | 代理状态 |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | DNS only |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |

如需 IPv6，可同时添加：

| 类型 | 名称 | 内容 | 代理状态 |
| --- | --- | --- | --- |
| AAAA | `@` | `2606:50c0:8000::153` | DNS only |
| AAAA | `@` | `2606:50c0:8001::153` | DNS only |
| AAAA | `@` | `2606:50c0:8002::153` | DNS only |
| AAAA | `@` | `2606:50c0:8003::153` | DNS only |

如果还希望 `www.1956799.xyz` 可访问，可增加：

| 类型 | 名称 | 内容 | 代理状态 |
| --- | --- | --- | --- |
| CNAME | `www` | `yjj195679.github.io` | DNS only |

这里的 CNAME 目标应是账户默认 Pages 域名 `yjj195679.github.io`，不要附加仓库名、协议或路径。配置期间建议保持 Cloudflare 灰云，即 **DNS only**，避免代理缓存或证书状态干扰 GitHub Pages 的域名检查。

### 9.3 HTTPS

DNS 检查通过后，在 GitHub Pages 设置中启用 **Enforce HTTPS**。证书签发和 DNS 传播可能不是立即完成的；变更后应先等待状态更新，不要反复删除和新增记录。

可以使用以下命令检查 Windows 上的 DNS：

```powershell
Resolve-DnsName 1956799.xyz -Type A
Resolve-DnsName www.1956799.xyz -Type CNAME
```

也可以使用：

```bash
nslookup 1956799.xyz
```

官方参考：[Managing a custom domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

---

## 10. 如何修改和扩展内容

### 10.1 修改现有内容

- 首页简介、项目概览和联系方式：编辑 `index.html`；
- 项目技术细节：编辑 `projects.html`；
- 学习路径：编辑 `education.html`；
- 408、数学和视觉知识地图：编辑 `courses.html`；
- 阶段成果：编辑 `achievements.html`；
- 生活和近期状态：编辑 `life.html`；
- 留言表单结构：编辑 `guestbook.html`；
- 全局视觉：编辑 `css/style.css`；
- 导航、动画、时钟和天气：编辑 `js/main.js`；
- 留言数据逻辑：编辑 `js/guestbook.js`。

### 10.2 新增一个子页面

建议按以下顺序操作：

1. 复制与内容类型最接近的现有 HTML；
2. 修改 `title`、`description`、canonical 和 `body[data-page]`；
3. 删除旧页面链接上的 `aria-current`，并给新页面导航项添加它；
4. 将新入口加入所有页面的统一导航；
5. 在 `style.css` 中新增页面背景变量；
6. 将背景图压缩后放入 `images/`；
7. 在 `sitemap.xml` 中加入正式 URL；
8. 检查新页面的桌面端、平板端和手机端布局；
9. 检查所有相对路径和页面间链接；
10. 推送后确认正式域名能够访问。

示例：新增 `notes.html` 时，可以添加：

```html
<body data-page="notes">
```

```css
body[data-page="notes"] {
  --page-image: url("../images/notes.webp");
}
```

## 11. 发布前检查清单

### 内容与链接

- [ ] 首页和六个主要子页面均能正常打开；
- [ ] 顶部导航在每页顺序一致；
- [ ] 当前页面高亮正确；
- [ ] 所有站内链接不存在 404；
- [ ] GitHub 外链使用 HTTPS 并能正常打开；
- [ ] 文案中没有隐私信息、临时占位符或错误日期。

### 视觉与响应式

- [ ] 背景图、卡片图和 favicon 都能加载；
- [ ] 1920 px、1366 px、平板和手机宽度下布局正常；
- [ ] 980 px 以下移动菜单能打开、关闭和滚动；
- [ ] 640 px 以下文字不溢出，按钮可正常点击；
- [ ] 文本与背景有足够对比度；
- [ ] 键盘 Tab 导航和焦点样式清晰；
- [ ] 减少动态效果模式下没有强制动画。

### 留言板

- [ ] 页面能读取最近公开留言；
- [ ] 合法名字和留言可以提交；
- [ ] 空内容、超长内容和蜜罐字段会被阻止；
- [ ] 提交后页面状态提示正确；
- [ ] 新留言能重新加载并显示；
- [ ] `is_visible = false` 的留言不会出现在公开列表；
- [ ] 浏览器代码中不存在 secret / service_role key。

### 部署与 SEO

- [ ] `CNAME` 仍然只有 `1956799.xyz`；
- [ ] GitHub Pages 发布源为 `main` 和 `/(root)`；
- [ ] 自定义域名 DNS 检查通过；
- [ ] HTTPS 已启用；
- [ ] canonical 和 Open Graph URL 使用正式域名；
- [ ] `robots.txt` 中的 sitemap 地址正确；
- [ ] `sitemap.xml` 已包含所有公开页面。

---

## 12. 常见问题排查

### 12.1 CSS 没有生效

依次检查：

1. 页面是否引用 `css/style.css`；
2. 文件名大小写是否完全一致；
3. Pages 发布源是否仍指向 `main` 根目录；
4. CSS 是否已经提交并推送，而不只存在于本地；
5. 浏览器是否仍在使用缓存，可尝试强制刷新；
6. 开发者工具 Network 中 `style.css` 是否返回 200；
7. Console 中是否有 MIME 类型或路径错误。

### 12.2 子页面背景没有变化

确认三个位置相互匹配：

- HTML 中的 `body[data-page]`；
- CSS 中对应的 `body[data-page="..."]` 规则；
- `images/` 中真实存在且大小写一致的图片文件。

例如 HTML 使用 `data-page="study"`，CSS 也必须匹配 `study`，不能写成 `courses`。

### 12.3 留言返回 401 或 403

重点检查：

- Supabase URL 和 publishable key 是否属于同一个项目；
- 请求头是否包含 `apikey`；
- `messages` 表是否位于暴露的 `public` schema；
- RLS 是否已启用并存在 SELECT / INSERT policy；
- `anon` 是否获得所需列的 SELECT / INSERT 权限；
- 是否误把服务端 secret key 放进前端；
- 字段名是否仍为 `name`、`content`、`created_at` 和 `is_visible`。

### 12.4 留言提交成功但列表不显示

检查新记录的 `is_visible` 是否为 `true`，`created_at` 是否存在，以及 SELECT policy 是否允许读取。再检查浏览器 Network 中重新加载留言的 GET 请求和返回内容。

### 12.5 自定义域名无法打开

检查：

1. `CNAME` 文件内容；
2. Pages 设置中的 Custom domain；
3. 根域名四条 A 记录；
4. 是否存在冲突的旧 A、AAAA、CNAME、ALIAS 或转发记录；
5. Cloudflare 是否处于 DNS only；
6. DNS 是否已经传播；
7. Pages 是否部署成功；
8. HTTPS 证书是否仍在签发。

### 12.6 天气无法显示

天气依赖浏览器定位和第三方接口。请确认：

- 页面通过 HTTPS 或 localhost 打开；
- 浏览器允许网站读取位置；
- 系统定位服务已开启；
- 网络可以访问 `api.open-meteo.com`；
- 控制台没有定位或 Fetch 错误。

---

## 13. 安全与隐私原则

- 静态仓库中的任何内容都会被公开访问，不提交密码、Token、数据库连接串或个人敏感文件；
- Supabase 前端只使用 publishable key；
- secret / service_role key 只能保存在受控服务端；
- 留言权限遵循最小权限原则，匿名用户不获得更新和删除权限；
- 用户输入使用 `textContent` 渲染，避免将留言当作 HTML 执行；
- 定位必须由访客主动点击触发，且不保存坐标；
- 留言表单明确提醒访客不要填写联系方式、账号或其他敏感信息；
- DNS 不使用通配符记录，减少域名接管风险；
- 修改数据库策略后，应使用匿名浏览器重新测试，而不能只用管理员会话测试。

