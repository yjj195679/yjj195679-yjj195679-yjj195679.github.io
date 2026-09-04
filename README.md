# True Path M

个人作品与学习档案，主要记录图像复原、深度学习、优化算法、计算机基础与数学学习中的项目、实验和阶段成果。

[中文网站](https://1956799.xyz/) · [English](https://1956799.xyz/en/) · [GitHub 主页](https://github.com/yjj195679)

## 网站内容

| 页面 | 中文 | English | 内容 |
| --- | --- | --- | --- |
| 首页 | `index.html` | `en/index.html` | 个人简介、研究方向与代表项目 |
| 项目 | `projects.html` | `en/projects.html` | DPSR、Primal–Dual、UNet、Restormer |
| 教育 | `education.html` | `en/education.html` | 学习路径、研究实践与学习方法 |
| 学习 | `courses.html` | `en/courses.html` | 408、数学、图像处理与优化方法 |
| 成果 | `achievements.html` | `en/achievements.html` | 已完成的研究、实验与文档成果 |
| 生活 | `life.html` | `en/life.html` | 近期学习、实验推进与项目整理 |
| 留言板 | `guestbook.html` | `en/guestbook.html` | 公开留言 |
| 404 | `404.html` | `en/404.html` | 无效路径提示 |

网站默认进入中文版。每个主要页面都提供对应的英文页面，顶部语言开关会切换到当前页面的另一语言版本。

## 内容原则

网站只保留真实、明确并且可以持续维护的个人内容：

- 图像复原、超分辨率与去模糊项目；
- DPSR、Primal–Dual、UNet、Restormer 等实验；
- 数据结构、计算机组成原理、操作系统和计算机网络；
- 高等数学、线性代数、概率论与优化方法；
- 能够由代码、实验结果或文档支持的阶段成果；
- 当前仍在推进的学习与研究工作。

不添加未经确认的经历、爱好、成果或个人信息。公开页面不讲解网站自身的实现过程；技术内容仅用于呈现真实完成的项目与研究。

## 双语维护

中文页面位于仓库根目录，英文页面位于 `en/`。

修改内容时应同时检查两种语言：

1. 中文与英文页面结构保持对应；
2. 英文采用自然表达，不逐字翻译；
3. 模型、论文、数据集和技术缩写保留原名；
4. 两种语言中的时间、数值、实验结果和链接保持一致；
5. `lang`、`canonical`、`hreflang` 与当前页面一致；
6. 新增或删除页面时同步更新导航和 `sitemap.xml`。

根目录是默认中文入口，`x-default` 同样指向中文版。

## 项目结构

```text
.
├── 404.html
├── CNAME
├── README.md
├── achievements.html
├── courses.html
├── education.html
├── favicon.svg
├── guestbook.html
├── index.html
├── life.html
├── projects.html
├── robots.txt
├── sitemap.xml
├── css
│   └── style.css
├── en
│   ├── 404.html
│   ├── achievements.html
│   ├── courses.html
│   ├── education.html
│   ├── guestbook.html
│   ├── index.html
│   ├── life.html
│   └── projects.html
├── images
│   ├── achieve.webp
│   ├── course.webp
│   ├── edu.webp
│   ├── hero.webp
│   ├── life.webp
│   └── project.webp
└── js
    ├── guestbook.js
    └── main.js
```

## 本地预览

网站为原生 HTML、CSS 和 JavaScript 项目，不需要安装构建依赖。

在仓库根目录运行：

```bash
python -m http.server 8000
```

访问：

- 中文：`http://localhost:8000/`
- English：`http://localhost:8000/en/`

也可以使用 VS Code 的静态服务器扩展进行预览。

## 内容更新

### 项目与成果

项目内容位于 `projects.html` 和 `en/projects.html`，成果位于 `achievements.html` 和 `en/achievements.html`。

更新实验内容时，应核对：

- 模型与数据集名称；
- 训练和推理条件；
- 指标、数值与时间；
- 已完成工作和后续计划的边界；
- 中英文页面的一致性。

计划中的内容不能写成已经完成的成果。

### 学习内容

学习路径和知识地图位于：

- `education.html`
- `courses.html`
- `en/education.html`
- `en/courses.html`

新增内容时应归入最合适的分类，避免相同知识点在多个区域重复出现。

### 近期状态

`life.html` 和 `en/life.html` 只记录当前仍有意义的学习、实验和项目整理。内容过期后应更新或删除。

### 图片

本地图片统一放在 `images/`，优先使用 WebP。替换图片时需要确认：

- 图片与页面内容直接相关；
- 桌面端和移动端裁切合理；
- 暗色背景上的文字清晰；
- 文件体积适合网页加载；
- 图片具有明确的使用许可；
- 外部图片在本文件中保留来源。

### 排版与组件

全站样式集中在 `css/style.css`。修改时应复用已有的字体层级、间距、颜色和响应式规则，避免在单个页面重复写样式。

站内箭头、返回、外部链接与回到顶部图标使用统一的线性 SVG。新增图标应保持一致的尺寸、线宽和视觉语言。

## 发布

仓库默认分支为 `main`，推送后由 GitHub Pages 更新网站。自定义域名记录在 `CNAME` 中。

发布前检查：

- [ ] 默认入口为中文版
- [ ] 每个主要页面都有对应英文版
- [ ] 语言开关指向正确页面
- [ ] 导航、按钮与页脚链接有效
- [ ] 中文和英文内容保持一致
- [ ] 没有无关或未经确认的内容
- [ ] 项目数据、时间和结果准确
- [ ] 图片可以正常加载并保留来源
- [ ] 桌面端和移动端没有文字溢出
- [ ] 页面标题、描述和语言标记正确
- [ ] `sitemap.xml` 已同步
- [ ] 仓库中没有密钥、令牌或私人信息

## 图片来源

首页图片由 Komorebi Photo 发布于 Unsplash：

[Blurred lights streak through a dark library with bookshelves](https://unsplash.com/photos/blurred-lights-streak-through-a-dark-library-with-bookshelves-QeICm1euWuE)

其余页面使用仓库内的 WebP 图片。

## 许可

网站中的个人文字、项目结果与第三方资源分别遵循其原始许可。引用图片、论文、模型、数据集或代码时，应保留原始来源。
