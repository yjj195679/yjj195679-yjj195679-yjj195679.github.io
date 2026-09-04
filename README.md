# True Path M · Personal Portfolio

这是 True Path M 的个人作品与学习档案网站，主要记录图像复原、深度学习、优化算法、计算机基础与数学学习中的项目、实验和阶段成果。

- 网站：[https://1956799.xyz](https://1956799.xyz)
- GitHub：[https://github.com/yjj195679](https://github.com/yjj195679)
- 仓库：[yjj195679-yjj195679-yjj195679.github.io](https://github.com/yjj195679/yjj195679-yjj195679-yjj195679.github.io)

网站默认显示中文，所有主要页面都提供对应英文版，并可在页面顶部自由切换。

---

## 1. 内容范围

网站只保留与个人经历直接相关、能够持续维护的内容：

- 图像复原、超分辨率与去模糊项目；
- DPSR、Primal–Dual、UNet、Restormer 等实验记录；
- 数据结构、计算机组成原理、操作系统、计算机网络等 408 学习内容；
- 高等数学、线性代数、概率论与优化方法；
- 已完成的研究复现、实验结果与文档成果；
- 近期学习方向和项目整理；
- 联系方式与公开留言。

公开页面不展示网站内部实现过程，也不添加未经确认的经历、爱好、成果或个人信息。项目中的技术说明仅用于呈现真实完成的工作。

---

## 2. 页面结构

| 中文页面 | 英文页面 | 内容 |
| --- | --- | --- |
| `index.html` | `en/index.html` | 个人简介、研究方向、代表项目、学习路径与联系方式 |
| `projects.html` | `en/projects.html` | DPSR、Primal–Dual、UNet 与 Restormer 项目 |
| `education.html` | `en/education.html` | 学习路径、研究实践与学习方法 |
| `courses.html` | `en/courses.html` | 408、数学、图像处理与优化方法 |
| `achievements.html` | `en/achievements.html` | 已完成的研究、实验与文档成果 |
| `life.html` | `en/life.html` | 近期学习、实验推进与项目整理 |
| `guestbook.html` | `en/guestbook.html` | 公开留言 |
| `404.html` | `en/404.html` | 无效路径提示 |

中文页面位于仓库根目录，因此访问域名时默认进入中文版。英文页面统一位于 `en/` 目录。

---

## 3. 中英文版本

每个主要页面都有一一对应的语言版本。顶部语言开关会保留当前页面语境，例如：

| 当前页面 | 切换后 |
| --- | --- |
| `projects.html` | `en/projects.html` |
| `en/courses.html` | `courses.html` |
| `guestbook.html` | `en/guestbook.html` |

维护内容时应遵循以下规则：

1. 先确认中文内容准确；
2. 同步更新对应英文页面；
3. 英文内容采用自然表达，不逐字直译；
4. 项目名称、模型名称、数据集和标准缩写保留原文；
5. 两种语言中的数字、时间、实验结果和链接保持一致；
6. 每个页面都要保留对应的 `canonical` 与 `hreflang`；
7. 新增页面时，同时补充中文页、英文页、导航和站点地图。

根目录是默认中文入口，`x-default` 也指向中文页面。

---

## 4. 目录

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

目录树只列出文件和文件夹名称，不在文件名后附加说明。

---

## 5. 本地预览

网站为静态页面，不需要安装前端框架或构建依赖。建议通过本地 HTTP 服务预览，避免直接打开文件时遇到浏览器安全限制。

### Python

```bash
python -m http.server 8000
```

访问：

```text
http://localhost:8000/
```

英文版：

```text
http://localhost:8000/en/
```

### VS Code

也可以使用 Live Server 等静态服务器扩展打开仓库根目录。

---

## 6. 内容维护

### 修改首页

中文首页位于 `index.html`，英文首页位于 `en/index.html`。修改简介、项目入口、学习方向或联系方式时，应同步检查两份文件。

### 修改项目

项目内容分别位于：

- `projects.html`
- `en/projects.html`

只写入真实完成或正在推进的内容。涉及实验结果时，应核对模型名称、数据集、指标、显存条件和数值，避免把计划写成成果。

### 修改学习内容

教育与学习地图分别由以下文件维护：

- `education.html`
- `courses.html`
- `en/education.html`
- `en/courses.html`

新增知识点时应放入最合适的分类，避免重复堆叠相近条目。

### 修改近期状态

近期状态位于 `life.html` 和 `en/life.html`。只保留当前仍有意义的学习、实验和整理工作，过期内容应更新或删除。

### 修改成果

成果位于 `achievements.html` 和 `en/achievements.html`。只有能够由代码、实验结果、报告或其他材料支持的内容才应列入。

---

## 7. 样式与图标

全站样式集中在 `css/style.css`。修改时应优先复用现有变量、组件和响应式断点，避免在单个页面重复添加样式。

站内方向与跳转图标使用统一的线性 SVG：

- 返回图标；
- 页面跳转图标；
- 外部链接图标；
- 回到顶部图标。

新增图标时应保持相同的线宽、尺寸与视觉语言，不使用独立的字符箭头替代。

---

## 8. 图片

本地图片统一放在 `images/`，优先使用 WebP，并根据实际显示尺寸压缩。更新图片时需同时检查：

- 图片与页面主题是否相关；
- 暗色背景下文字是否清晰；
- 桌面端与移动端裁切是否合理；
- 文件体积是否适合网页加载；
- 是否拥有使用权限；
- 外部图片是否保留来源与授权信息。

首页当前使用 Komorebi Photo 发布于 Unsplash 的图片：

[Blurred lights streak through a dark library with bookshelves](https://unsplash.com/photos/blurred-lights-streak-through-a-dark-library-with-bookshelves-QeICm1euWuE)

其余页面使用仓库内的 WebP 图片。后续替换外部图片时，应更新本节来源。

---

## 9. 外部服务

网站当前依赖以下外部服务：

| 服务 | 用途 |
| --- | --- |
| GitHub Pages | 网站托管 |
| Supabase | 留言数据 |
| Open-Meteo | 天气数据 |
| Unsplash | 首页图片来源 |

如果更换域名、数据服务或外部图片，应同步检查页面链接、浏览器控制台、隐私提示和本说明文件。

---

## 10. SEO 与可访问性

更新页面时请检查：

- 页面 `lang` 是否与语言版本一致；
- `title` 与 `description` 是否准确；
- `canonical` 是否指向当前页面；
- `hreflang` 是否包含中文、英文和 `x-default`；
- 导航当前项是否正确；
- 图片背景上的文字是否有足够对比度；
- 交互控件是否可通过键盘访问；
- 图标是否提供正确的辅助信息或被标记为装饰；
- 移动端菜单与语言开关是否正常显示；
- 减少动态效果的系统设置是否得到尊重。

站点地图位于 `sitemap.xml`。新增或删除主要页面时必须同步更新。

---

## 11. 部署

仓库的默认分支为 `main`。提交并推送后，GitHub Pages 会更新线上网站。

发布前建议依次检查：

1. 中文首页是否为默认入口；
2. 所有页面的中英文切换是否正确；
3. 导航、按钮与页脚链接是否可用；
4. 英文页面是否存在遗漏的中文正文；
5. 中文页面是否保留不必要的英文栏目名；
6. 项目数据、时间与文字是否准确；
7. 图片是否能正常加载；
8. 留言与天气入口是否正常；
9. `robots.txt`、`sitemap.xml` 与 `CNAME` 是否正确；
10. 桌面端和移动端是否存在溢出或遮挡。

GitHub 仓库文件列表右侧显示的是每个文件最后一次变更对应的提交信息，这是 GitHub 的固定界面，不能由仓库文件隐藏。本仓库使用简短提交信息，尽量减少这一列的视觉干扰。

---

## 12. 安全与隐私

- 不在仓库中提交服务端密钥、数据库密码或私人令牌；
- 公开配置只能使用允许暴露在浏览器中的信息；
- 留言为公开内容，不应填写联系方式、账号或敏感信息；
- 新增第三方脚本或服务前，应确认来源、权限和隐私影响；
- 个人经历和项目结果应以可核实内容为准。

---

## 13. 更新检查清单

```text
[ ] 中文内容准确
[ ] 英文内容同步
[ ] 当前页语言开关正确
[ ] 导航与页脚链接正确
[ ] 没有无关或未经确认的内容
[ ] 没有面向访客的实现过程说明
[ ] 图片来源与授权清楚
[ ] 页面标题与描述正确
[ ] canonical 与 hreflang 正确
[ ] sitemap.xml 已同步
[ ] 移动端布局正常
[ ] 外部服务入口正常
[ ] 未提交敏感信息
```

---

## 14. 许可与引用

网站代码与个人内容的再使用以仓库后续声明为准。第三方图片、模型、论文、数据集和库分别遵循其原始许可；引用相关内容时应保留来源。
