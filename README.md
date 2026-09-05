# True Path M · 个人网站

一个以研究、项目和学习记录为核心的双语个人网站，当前部署域名为 [1956799.xyz](https://1956799.xyz/)。网站使用原生 HTML、CSS 和 JavaScript 构建，不依赖前端框架或打包工具，适合直接托管在 GitHub Pages。

[中文网站](https://1956799.xyz/) · [English](https://1956799.xyz/en/) · [GitHub 主页](https://github.com/yjj195679)

## 1. 网站定位

网站用于整理和展示真实完成的个人工作，主要包括：

- 图像复原、去模糊与超分辨率研究；
- DPSR、Primal–Dual、UNet、Restormer 等实验；
- 数据结构、计算机组成原理、操作系统和计算机网络；
- 高等数学、线性代数、概率论与优化方法；
- 可由代码、实验结果或文档支持的阶段成果；
- 当前仍在推进的学习、研究与工程整理。

内容维护遵循一个原则：不添加未经确认的经历、成果、爱好或个人信息，计划中的内容也不写成已经完成的成果。

## 2. 设计思路

整体视觉参考了 [imsyy/home](https://github.com/imsyy/home) 的沉浸式个人主页体验，但没有复制其页面或技术栈。第二轮优化继续研究了 [Brittany Chiang v4](https://github.com/bchiang7/v4)、[Academic Pages](https://github.com/academicpages/academicpages.github.io) 和 [Magic Portfolio](https://github.com/once-ui-system/magic-portfolio)，分别吸收其章节导航、学术内容组织和项目案例化表达方式。本站始终保留自己的多页面结构、真实内容和纯静态技术路线。

- 全屏背景与暗色遮罩，确保背景存在感和正文可读性同时成立；
- 毛玻璃面板、圆角悬浮导航和轻量卡片动效；
- 首屏当前状态、日期、实时时钟和天气信息；
- 页面滚动进度与导航滚动状态；
- 子页面自动生成页内章节导航，并随阅读位置高亮；
- 桌面端指针光感、滚动入场和背景轻微视差；
- 项目页先展示可核对的实验摘要，再进入详细过程；
- 完整移动端适配，并尊重系统的“减少动态效果”设置。

本站的视觉方向是“暗黑、克制、学术、可长期维护”。中文正文优先使用宋体体系，英文优先使用 Times New Roman。蓝灰色高光只用于层级、状态和交互提示，不改变内容本身的严肃感。

## 3. 当前功能

- 中英文双语页面；
- 多页面导航与当前栏目高亮；
- 每个栏目独立背景图；
- 首页项目、学习、教育、成果、生活与留言板入口；
- 图像复原项目与实验过程展示；
- 408、数学和图像复原知识地图；
- 浏览器本地时间与日期；
- 基于 Open-Meteo 的当前位置天气；
- 基于 Supabase REST API 的公开留言板；
- 响应式移动导航；
- 滚动进度、分组入场、背景视差和卡片指针光感；
- 子页面章节导航、当前章节高亮和返回顶部；
- 全站快捷搜索，支持按钮、`Ctrl/Command + K` 和 `/` 唤起；
- 项目关键结果摘要；
- 学习页内置 25/5/15 分钟专注计时器；
- 生活页提供按日期固定的中英对照“每日哲思”，内容仅限哲学；
- `prefers-reduced-motion` 无障碍降级；
- 面向论文阅读与归档的打印样式；
- 长页面离屏内容延迟渲染；
- SEO 基础信息、双语 `hreflang`、站点地图和自定义 404 页面。

## 4. 页面说明

| 页面 | 中文 | English | 主要内容 |
| --- | --- | --- | --- |
| 首页 | `index.html` | `en/index.html` | 个人简介、当前方向、精选项目与快速入口 |
| 项目 | `projects.html` | `en/projects.html` | DPSR、Primal–Dual、UNet、Restormer |
| 教育 | `education.html` | `en/education.html` | 学习路径、研究实践与学习闭环 |
| 学习 | `courses.html` | `en/courses.html` | 408、数学、图像处理与优化方法 |
| 成果 | `achievements.html` | `en/achievements.html` | 已完成的研究、实验和文档成果 |
| 生活 | `life.html` | `en/life.html` | 近期状态与中英双语每日哲思 |
| 留言板 | `guestbook.html` | `en/guestbook.html` | 访客公开留言 |
| 404 | `404.html` | `en/404.html` | 无效路径提示和返回入口 |

网站默认进入中文版。每个主要页面都提供对应英文版，语言开关会切换到当前页面的另一语言版本。

## 5. 项目结构

```text
.
├── index.html                 # 中文首页
├── projects.html              # 中文项目页
├── education.html             # 中文教育页
├── courses.html               # 中文学习页
├── achievements.html          # 中文成果页
├── life.html                  # 中文生活页
├── guestbook.html             # 中文留言板
├── 404.html                   # 中文 404
├── en/                        # 对应英文页面
│   ├── index.html
│   ├── projects.html
│   ├── education.html
│   ├── courses.html
│   ├── achievements.html
│   ├── life.html
│   ├── guestbook.html
│   └── 404.html
├── css/
│   └── style.css              # 全站设计系统、布局、动效和响应式规则
├── js/
│   ├── main.js                # 导航、时钟、日期、天气、滚动和交互效果
│   ├── guestbook.js           # 留言加载、校验、提交和冷却控制
│   └── extras.js              # 专注计时器与每日哲思
├── images/                    # WebP 背景与栏目图片
├── favicon.svg                # 网站图标
├── CNAME                     # GitHub Pages 自定义域名
├── robots.txt                # 搜索引擎抓取规则
├── sitemap.xml               # 中英文页面站点地图
└── README.md                  # 项目说明
```

## 6. 从零运行网站

### 6.1 获取源码

```bash
git clone https://github.com/yjj195679/yjj195679-yjj195679-yjj195679.github.io.git
cd yjj195679-yjj195679-yjj195679.github.io
```

### 6.2 本地预览

本项目不需要安装 Node.js 依赖。在仓库根目录启动任意静态文件服务器即可：

```bash
python -m http.server 8000
```

然后访问：

- 中文首页：`http://localhost:8000/`
- 英文首页：`http://localhost:8000/en/`

不要直接双击 HTML 文件测试全部功能。天气请求、留言板请求和部分浏览器安全策略在 `file://` 协议下可能表现不同，使用本地 HTTP 服务更可靠。

## 7. 样式系统

全站样式集中在 `css/style.css`。颜色、圆角、阴影、字体和字号都由文件顶部的 CSS 变量控制：

```css
:root {
  --bg: #080a0f;
  --surface: rgba(14, 18, 27, 0.72);
  --text: #f5f7fb;
  --muted: #aeb7c6;
  --accent: #b9d5ff;
  --radius-lg: 30px;
  --max-width: 1180px;
  --font-latin: "Times New Roman", Times, serif;
  --font-cjk: SimSun, "Songti SC", "STSong", serif;
}
```

修改主题时优先调整变量，不要在各页面重复写颜色。新增卡片应尽量复用 `.glass`、`.panel`、`.content-card`、`.tag`、`.button` 等现有组件类。

各页面通过 `body` 的 `data-page` 属性选择背景：

```html
<body data-page="projects">
```

对应关系定义在 `css/style.css` 中。背景图统一放入 `images/`，推荐使用 WebP，并控制在适合网页加载的体积内。

## 8. JavaScript 功能

### 8.1 全站交互

`js/main.js` 负责：

- 自动更新页脚年份；
- 根据当前语言格式化时间和首页日期；
- 打开、关闭移动端导航，并支持 `Esc` 关闭；
- 使用 `IntersectionObserver` 实现分组入场；
- 根据页面位置更新顶部滚动进度；
- 滚动后增强导航栏背景，保证复杂背景上的可读性；
- 为桌面端玻璃面板提供跟随指针的柔和高光；
- 以较低幅度移动背景，形成轻量视差；
- 自动读取子页面直属章节，生成可滚动的页内导航；
- 使用 IntersectionObserver 更新当前章节状态；
- 在长页面中提供返回顶部按钮；
- 提供支持关键字过滤、方向键选择和回车跳转的全站快捷导航；
- 请求地理位置并从 Open-Meteo 获取当前天气。

所有主要动效都会检查 `prefers-reduced-motion`。在触摸屏或不支持精细指针的设备上，不启用指针光感。

快捷导航会根据当前语言显示首页、主要栏目和核心研究项目。点击导航栏中的搜索按钮，或按 `Ctrl/Command + K`、`/` 即可打开；按方向键选择，回车进入，`Esc` 关闭。功能完全在浏览器本地运行，不会上传搜索内容。

### 8.2 天气

天气功能使用浏览器 Geolocation API 获取经纬度，再请求 Open-Meteo。只有用户点击“使用当前位置”后才会请求定位权限。

如果天气无法显示，依次检查：

1. 页面是否通过 HTTPS 或本地 HTTP 服务访问；
2. 浏览器是否允许当前站点使用位置；
3. 系统定位服务是否开启；
4. 网络是否能够访问 `api.open-meteo.com`；
5. 浏览器控制台是否存在跨域或网络错误。

### 8.3 专注计时器与每日哲思

学习页提供 25 分钟专注、5 分钟短休息和 15 分钟长休息三种模式。计时由浏览器本地完成，支持开始、暂停、重置和切换时长；运行期间标签页标题会显示剩余时间，不会上传学习记录。

生活页的“每日哲思”使用仓库内置的中英配对内容，不请求第三方语录接口。初始内容由本地日期确定，因此同一天刷新页面仍会看到同一则哲思；点击“再看一句”可以顺序浏览下一则。中英文页面显示同一条内容，只调整主语言与译文的先后顺序。语料只收录哲学命题、哲学家观点和明确标注的思想概述，不混入诗词，也不会因为接口超时而留下空白。

## 9. 留言板与 Supabase

留言板前端代码位于 `js/guestbook.js`，通过 Supabase REST API 读取和写入 `messages` 表。

前端当前使用以下字段：

| 字段 | 建议类型 | 用途 |
| --- | --- | --- |
| `id` | `bigint` 或 `uuid` | 主键 |
| `name` | `text` | 留言者昵称，前端限制 1–40 字符 |
| `content` | `text` | 留言内容，前端限制 1–500 字符 |
| `created_at` | `timestamptz` | 创建时间 |
| `is_visible` | `boolean` | 是否在公开列表显示 |

安全要求：

- 浏览器中只能使用 Supabase publishable/anon key，绝不能放入 `service_role` 密钥；
- 必须在 Supabase 中启用 Row Level Security；
- 公开查询只允许读取 `is_visible = true` 的留言；
- 插入策略只允许写入必要字段，并在数据库端再次限制长度；
- 管理、审核和删除应在可信后台完成，不应暴露到公开网页；
- 前端的 30 秒冷却和蜜罐字段只用于降低普通滥用，不能替代数据库策略或服务端限流。

更换 Supabase 项目时，修改 `js/guestbook.js` 顶部的 `SUPABASE_URL` 和 publishable key，并同步检查表名、字段和 RLS 策略。

## 10. 内容更新方法

### 10.1 更新项目

项目详情位于 `projects.html` 和 `en/projects.html`。更新实验内容时应核对模型、数据集、训练条件、推理条件、指标、时间和结果。中文版与英文版的事实必须一致，英文可以按自然表达重新组织，不要求逐字翻译。

### 10.2 更新学习与成果

- 学习路径：`education.html`、`en/education.html`
- 知识地图：`courses.html`、`en/courses.html`
- 阶段成果：`achievements.html`、`en/achievements.html`
- 近期状态：`life.html`、`en/life.html`

新增内容时放入最合适的栏目，避免同一段内容在多个页面重复。过期的“近期状态”应更新或删除。

### 10.3 更新图片

1. 将新图片裁切为适合背景或卡片的比例；
2. 转换为 WebP；
3. 尽量压缩到 150 KB 左右或更小；
4. 替换 `images/` 中对应文件，或修改 HTML/CSS 中的路径；
5. 分别检查桌面端和移动端裁切；
6. 确认暗色遮罩下文字仍清晰；
7. 在 README 中保留作者、来源和许可信息。

## 11. 双语与 SEO 维护

修改页面时需要同时检查：

1. `html lang` 是否正确；
2. 页面标题和描述是否与内容匹配；
3. `canonical` 是否指向当前语言页面；
4. `zh-CN`、`en` 和 `x-default` 的 `hreflang` 是否成组对应；
5. 语言切换是否落到相同栏目；
6. 中英文页面中的时间、数值、实验结果和链接是否一致；
7. 新增或删除页面后是否同步更新 `sitemap.xml`；
8. 社交分享图是否使用完整 HTTPS 地址。

根目录是默认中文入口，`x-default` 同样指向中文版。

## 12. GitHub Pages 发布

1. 将修改提交并推送到仓库的 `main` 分支；
2. 打开仓库 `Settings → Pages`；
3. 将发布来源设置为分支部署，并选择 `main` 与根目录；
4. 等待 GitHub Pages 构建完成；
5. 在 Custom domain 中填写 `1956799.xyz`；
6. 保留仓库根目录中的 `CNAME` 文件；
7. DNS 记录应以 GitHub Pages 设置页当前给出的值为准；
8. 如果 DNS 使用 Cloudflare，解析期间保持“仅 DNS”，不要开启代理；
9. 域名验证完成后开启 Enforce HTTPS。

通常推送后需要等待短暂缓存刷新。如果代码已经更新但页面样式仍旧，可先使用无痕窗口或强制刷新检查，再确认 GitHub Pages 的最新部署是否成功。

## 13. 发布前检查清单

- [ ] 中文和英文首页都能打开
- [ ] 每个主要页面都有对应英文页面
- [ ] 语言切换指向同一栏目
- [ ] 导航、按钮、页脚和卡片链接有效
- [ ] 当前栏目高亮正确
- [ ] 所有背景和卡片图片可以加载
- [ ] 桌面端、平板和手机没有横向溢出
- [ ] 200% 文字缩放下内容仍可阅读
- [ ] 减少动态效果模式下没有持续动画干扰
- [ ] 天气按钮有成功与失败反馈
- [ ] 每日哲思在中英文页面内容一致，且未混入诗词
- [ ] 留言可以加载、校验并提交
- [ ] 页面标题、描述、canonical 与 hreflang 正确
- [ ] `sitemap.xml` 已同步
- [ ] `CNAME` 内容正确
- [ ] 仓库中没有私钥、service role key、令牌或私人信息
- [ ] 图片来源和许可记录完整

## 14. 常见问题

### CSS 已修改，但网站外观没有变化

先确认 `css/style.css` 已推送到发布分支，再查看 GitHub Pages 部署记录。部署成功后强制刷新或清除该站点缓存。不要只修改本地文件后直接检查线上页面。

### 子页面没有背景

检查子页面的 `body data-page` 值是否存在，并确认 `css/style.css` 中有对应的 `--page-image`。图片路径以 CSS 文件所在的 `css/` 目录为基准，因此本地图片通常写为 `../images/example.webp`。

### 英文页面资源加载失败

英文页面位于 `en/` 子目录。HTML 中引用根目录资源时需要使用 `../css/style.css`、`../js/main.js` 和 `../images/...`。

### 自定义域名无法绑定

检查 `CNAME` 是否只包含域名本身、DNS 是否与 GitHub Pages 当前说明一致、Cloudflare 是否为“仅 DNS”，并等待 DNS 传播。不要同时在多个 Pages 仓库中声明同一个域名。

### 留言板显示加载失败

检查 Supabase URL、publishable key、`messages` 表字段、RLS 查询策略以及浏览器控制台中的请求状态。若读取成功但列表为空，还要确认记录的 `is_visible` 是否为 `true`。

## 15. 图片来源与许可

网站使用的本地 WebP 图片包含来自公开图片资源的网页裁切版本。现有来源记录包括：

- 首页氛围图：[Blurred lights streak through a dark library with bookshelves](https://unsplash.com/photos/blurred-lights-streak-through-a-dark-library-with-bookshelves-QeICm1euWuE)，Komorebi Photo，Unsplash License；
- 项目与图像复原：[Camera lens](https://unsplash.com/photos/a-close-up-of-a-camera-lens-hRz3-M5PTT0)，Claudio Schwarz，Unsplash License；
- 课程与数学学习：[Blackboard of mathematical formulas](https://unsplash.com/photos/a-blackboard-with-a-lot-of-writing-on-it-OPpCbAAKWv8)，Thomas T，Unsplash License；
- 教育与研究环境：[Rubin Observatory Control Room](https://commons.wikimedia.org/wiki/File:Rubin_Observatory_Control_Room_(rubin-Revelado-Rubin-N30-CC).jpg)，Rubin Observatory / NSF / AURA / A. Pizarro D.，CC BY 4.0。

替换图片时应重新核对来源和许可，不要假定网络图片可以自由使用。

## 16. 许可说明

网站中的个人文字、项目结果、代码和第三方资源分别遵循其各自许可。引用图片、论文、模型、数据集或代码时，应保留原始来源和许可信息。
