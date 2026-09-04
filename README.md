# True Path M · Personal Portfolio

`1956799.xyz` 的纯静态多页面个人网站，使用原生 HTML、CSS 和 JavaScript 构建，通过 GitHub Pages 发布，并用 Supabase 提供公开留言数据。

## 当前特性

- 深色学术风格与半透明玻璃面板
- 中文宋体、英文 Times New Roman 字体栈
- 首页、项目、教育、学习、成果、生活、留言与 404 页面
- 每页独立背景图、统一导航和当前页面高亮
- 移动端折叠菜单与完整键盘焦点样式
- 滚动渐入、轻量背景位移和减少动态效果兼容
- 本地天气按需加载；仅在访客主动点击后请求定位
- Supabase 留言读取与提交，无需前端框架或第三方 JS CDN
- WebP 背景资源均小于 150 KB
- Open Graph、canonical、`robots.txt` 和 `sitemap.xml`

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
├── 404.html
├── CNAME
├── favicon.svg
├── robots.txt
├── sitemap.xml
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

## 本地预览

```bash
python -m http.server 8000
```

然后访问 `http://localhost:8000`。不要直接使用 `file://` 打开留言页，因为浏览器对跨域请求的处理可能不同。

## Supabase 留言板

前端使用 publishable key，权限边界由 Postgres grants 和 RLS 共同控制：

- `anon` / `authenticated` 只可读取 `is_visible = true` 的留言；
- 只可向 `name`、`content` 两列插入数据；
- 不可更新、删除，也不可自行写入 `id`、`created_at` 或 `is_visible`；
- 前端不会包含 secret key 或 `service_role` key。

表字段约束为：名字 1–40 字符，留言 1–500 字符。审核时可在 Supabase 后台把 `is_visible` 设置为 `false`。

## 部署

仓库根目录由 GitHub Pages 直接发布，`CNAME` 固定为 `1956799.xyz`。合并到 `main` 后检查：

1. 自定义域名 HTTPS 状态；
2. `css/style.css`、`js/main.js` 和 WebP 图片是否返回 200；
3. 留言页能否读取公开留言并提交一条测试消息；
4. 首页移动端菜单、页面导航与定位天气按钮是否正常。
