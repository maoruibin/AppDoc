# AGENTS.md - AppDoc 文档站

> doc.gudong.site 的源码仓库。VuePress 2 静态文档站，记录咕咚所有 App 的使用说明。
> 部署在 Cloudflare Pages，git push 到 main 自动触发构建部署。

## AI 日志与验证规范（必读）

本项目属于 ReProject。AI 修改代码前必须先读并遵守 [`../docs/ai-logging-verification.md`](../docs/ai-logging-verification.md)。写代码时同步补关键日志，交付前说明使用了哪些日志、命令、构建结果或页面验证完成闭环。

## 快速上手

- 本地预览：npm run docs:dev（端口 8080，占用时 --port 5173）
- 构建生产：npm run docs:build（产物在 docs/.vuepress/dist）
- 安装依赖必须加 --legacy-peer-deps
- Node >= 18，建议 20

详细开发命令见 README.md，技术架构见 CLAUDE.md。

## App 清单

每个 App 对应 docs/ 下一个目录，URL 路径就是目录名。

| 目录 | App 名 | 状态 | 蒲公英 key |
|:---|:---|:---|:---|
| inbox/ | inBox 笔记 | 上线 | 6a195ff51fe902a120fcda1303fb0137 |
| light/ | 点亮 | 上线 | 3db7b5b3b01f09c85934fdb19f1da92b |
| cang/ | 仓咚咚 | 上线 | bf8dbdf68ee1cf0906813d136b1a4d74 |
| rssplus/ | 咕咚订阅 | 上线 | 99503fd847173ed64a1522df51d66658 |
| picplus/ | 咕咚云图 | 上线 | e35e31620ac6476c1e442e6ef72694af |
| voice/ | inVoice 语记 | 上线 | f1476b43a1f8980eadc61f88681bc6ed |
| passbox/ | PassBox | 上线 | c7feda00ffb8c14ef26768a5dda0819d |
| time/ | 咚时光 | 隐藏 | 51403673fc46a16d71dab3c8947a1295 |
| echo/ | EchoRead | 隐藏 | 92cb6c457e756d2f8cc6545d222562bd |
| audio/ | 声咚咚 | 隐藏 | 586fe4bb0e736b133c01bd313af47a30 |
| niushuo/ | 小牛说 | 隐藏 | 7856141f76eee28f17ae19b6b091ef1f |
| tudongdong/ | 图咚咚 | 隐藏 | 449fe465df1eb30c8aebc0e989b4a41d |

蒲公英完整链接格式：https://www.pgyer.com/app/install/<key>

## 入口管理

控制 App 展示的有三个文件，改入口时三个都要同步检查：

1. 主页卡片 - docs/README.md
   - frontmatter 里 home: true，内容是 .app-grid 下的一堆 a.app-card 元素
   - 隐藏/恢复：用 HTML 注释 <!-- 已隐藏，后续可恢复 ... --> 包裹

2. 导航栏 + 侧边栏 - docs/.vuepress/config.js
   - navbar 数组：顶部导航「作品集合」下拉菜单
   - sidebar 对象：按路径前缀配置各 App 的侧边栏菜单
   - 隐藏 navbar 单行：注释成 // { text: '咚时光', link: '/time/' }
   - 隐藏 sidebar 整块：用块注释 /* '/time/': [ ... ] */

3. 下载页表格 - docs/inbox/download.md
   - Markdown 表格，每行一个 App（图标 + 名称 + 简介 + 下载链接）
   - 隐藏/恢复：用 <!-- 已隐藏，后续可恢复 ... --> 包裹对应行

### 隐藏/恢复规范

统一用注释方式隐藏，不要删除内容，方便后续恢复：

- 搜索「已隐藏」能快速定位所有隐藏点
- 恢复时去掉注释标记即可

## 图标与资源

- App 图标存放在冰封云 S3：https://gudong.s3.bitiful.net/icon/<图标名>
- 部分图标在本地 docs/public/img/ 下（如 niushuo_icon.png、tudongdong_icon.png）
- S3 图片可加 ?no-wait=on 参数避免加载等待

## 约定

- 所有内容简体中文
- 新增 App 文档：在 docs/ 下建目录，在 config.js 配置 sidebar，在 README.md 和 download.md 加入口
- Git push 到 main 即触发 Cloudflare Pages 自动部署，无需手动操作
