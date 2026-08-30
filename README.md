# True Path M · Personal Portfolio

一个纯静态、低依赖、适合 GitHub Pages 的个人主页。

视觉方向参考了 `imsyy/home` 的沉浸式背景、玻璃卡片、站点导航与移动端体验，但页面结构、内容和代码均重新实现，并把重点放在“完整介绍个人”而不是天气/音乐等主页小组件。

## Features

- 沉浸式全屏首页
- Glassmorphism / 深色视觉
- Projects / Education / Study / Achievements / Life
- 响应式布局
- 动态本地时间
- 滚动渐入
- `prefers-reduced-motion` 兼容
- 无框架、无 npm、无 CDN、无第三方字体
- 本地 SVG 背景与项目封面，体积小、无版权依赖
- GitHub Pages + 自定义域名可直接部署

## Structure

```text
.
├── index.html
├── projects.html
├── education.html
├── achievements.html
├── courses.html
├── life.html
├── 404.html
├── CNAME
├── css/
│   └── style.css
├── js/
│   └── main.js
└── assets/
    └── images/
        ├── background.svg
        ├── project-dpsr.svg
        ├── project-deblur.svg
        ├── project-ecg.svg
        ├── project-modeling.svg
        └── favicon.svg
```

## Local Preview

直接打开 `index.html`，或在项目目录运行：

```bash
python -m http.server 8000
```

访问 `http://localhost:8000`。

## Deploy to GitHub Pages

1. 把本目录文件上传到 GitHub Pages 仓库根目录。
2. 确保入口文件名是 `index.html`。
3. 仓库 `Settings → Pages` 中选择从默认分支部署。
4. `CNAME` 已写入 `1956799.xyz`，如域名变化请同步修改。

## Before publishing

建议你优先修改：

- `education.html`：学校、专业、时间
- `achievements.html`：真实奖项/竞赛
- `life.html`：换成个人照片与文字
- 各页面中的项目文字与链接

## Design reference

- https://github.com/imsyy/home

本项目不复制其源码，也不依赖其 API / 字体 / 音乐服务。
