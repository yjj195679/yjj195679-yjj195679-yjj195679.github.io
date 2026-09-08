# True Path M · 个人网站

[中文网站](https://1956799.xyz/) · [English](https://1956799.xyz/en/) · [GitHub](https://github.com/yjj195679)

这是一个使用原生 HTML、CSS 和 JavaScript 构建的双语个人网站，直接托管于 GitHub Pages。当前版本保留完整的网站结构和交互，只提供内容框架，具体经历、项目、笔记和成果将在确认后逐步填写。

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
- 多页面导航、当前栏目高亮和页内导航；
- 跟随系统、浅色、深色三种外观模式；
- 每个栏目独立背景图；
- 桌面端与移动端响应式布局；
- 快捷搜索、阅读模式、复制链接、打印与返回顶部；
- 当前时间、日期与按需天气；
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
