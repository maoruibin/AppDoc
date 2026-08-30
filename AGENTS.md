# AGENTS.md（AppDoc 文档站）

> 本文件是每次会话的常驻上下文：**项目快照 + 目录地图 + 开发规矩**。易变信息用指针（"以 X 为准"），不抄数值。
> **最后核实：2026-08-30（对照 main `cee290d` 实际代码）**

上级规范必读，本文只写 AppDoc 特化，不重复其内容：

- [`../AGENTS.md`](../AGENTS.md) —— 生态总纲：日志 / 提交纪律 / intent 总规范 / 设计规范
- [`../docs/ai-logging-verification.md`](../docs/ai-logging-verification.md) —— AI 日志与验证规范

## 0. 项目快照

**一句话**：咕咚全系 App 的使用文档站（doc.gudong.site），纯内容仓库——Markdown + VuePress 配置，无业务代码；每个 App 一个目录，改完 push 即自动上线。

| 维度 | 值 |
|---|---|
| 技术栈 | VuePress 2（rc 版，以 `package.json` 为准）+ webpack bundler + 默认主题 + sass，配置集中在 `docs/.vuepress/config.js` |
| 仓库 / 线上 | `github.com/maoruibin/AppDoc` / https://doc.gudong.site |
| 部署 | Cloudflare Pages Git 集成：push 到 main 自动构建部署；**无 CI、无 wrangler** |
| 环境 | Node >= 18（建议 20）；`npm install` 必须加 `--legacy-peer-deps` |
| 测试 / lint | 无测试框架、无 lint，验证 = 本地 `docs:dev` 预览 + 构建通过 |
| 语言 | 所有内容简体中文 |

## 1. 目录地图（先查地图再动手）

```
docs/
├── README.md                    首页（home: true，手写 .app-grid 卡片，非脚本生成）
├── download.md                  ★ 全局下载页；卡片网格区域由脚本从 apps.yml 生成，勿手改生成区
├── .vuepress/
│   ├── config.js                ★ 全站配置：navbar（作品集合下拉）/ sidebar（按 App 路径前缀）/ bundler
│   ├── apps.yml                 ★ 全应用元数据唯一源：包名/icon/蒲公英链接/visible/sort
│   ├── generate_apps_json.py    读 apps.yml → 生成 .vuepress/public/apps.json + download.md 卡片区
│   ├── client.js                按路径前缀切换导航栏 logo（logoMap）
│   ├── styles/index.scss        全站自定义样式
│   └── public/                  apps.json（生成产物）+ 少量静态资源
├── public/img/                  站内静态图片（引用路径 /img/...）
├── inbox/                       ★ 最大文档目录（40+ 页：指南/数据备份/WebDAV/S3/各端同步）
├── inbox/download.md            旧下载页，现仅剩跳转 /download 的重定向脚本
├── voice/ ...                   每个 App 一个目录，URL 路径 = 目录名（清单见下表）
└── software/                    软件列表（Obsidian 等非自研软件说明）
```

### App 文档目录清单（对照 docs/ 实际子目录，2026-08-30）

| 目录 | App | 包名（apps.yml） | 文档完整度 |
|---|---|---|---|
| `inbox/` | inBox 笔记 | `name.gudong.think` | 全套 + 大量专题页 |
| `voice/` | inVoice 语记 | `name.gudong.voice` | 全套（**写作范式最佳实践**） |
| `light/` | 点亮 | `name.gudong.habit` | 全套 |
| `cang/` | 仓咚咚 | `name.gudong.assets` | 全套 + data_security / pro_version |
| `rssplus/` | 咕咚订阅 | `name.gudong.rss` | 全套 |
| `picplus/` | 咕咚云图 | `name.gudong.pic` | 全套 + 图床教程多篇 |
| `passbox/` | PassBox 密匣 | `name.gudong.passbox` | 全套 + pro_version |
| `time/` | 咚时光 | `name.gudong.time` | 全套 + family / sync-guide |
| `music/` | 听咚咚 | `name.gudong.music` | 全套 |
| `measure/` | 量咚咚 | `name.gudong.measure` | 仅 changelog + private（待补全） |
| `mai/` | 脉咚咚 | `name.gudong.mai` | 仅 README + changelog + private |
| `echo/` | EchoRead | `name.gudong.content` | 全套 |
| `audio/` | 声咚咚 | `name.gudong.audio` | 全套 |
| `niushuo/` | 小牛说 | `name.gudong.inputvc` | 全套 |
| `tudongdong/` | 图咚咚 | `name.gudong.pictoon` | 全套（图咚咚文档权威目录） |
| `dream/` | 梦咚咚 | —（apps.yml 未登记） | 全套 |
| `picpoem/` | 诗图 | —（apps.yml 未登记） | 全套 |
| `douyin/` | 抖音保存 | —（工具类不注册） | 全套 |
| `sparrow/` | 麻雀 MD | `com.gudong.sparrow` | 仅 README + changelog + 协议 |
| `dongalbum/` | 随机相册 | —（apps.yml 未登记） | 仅 README + changelog + private |
| `health/` | 康咚咚 | —（apps.yml 未登记） | 仅 changelog + private |
| `imagetools/` | （图咚咚旧目录残留） | — | 仅一份滞后于 `tudongdong/` 的 changelog，**勿在此更新，待清理** |

> 上线/隐藏状态（visible）、下载链接、排序**以 `docs/.vuepress/apps.yml` 为准**，不抄进本文。

## 2. 开发约定（项目特有）

### 元数据唯一源：apps.yml

- 新增 App、改下载链接 / icon / 展示与否：**只改 `apps.yml`**，然后跑生成脚本（`docs:build` 也会自动先跑）
- `download` 字段用蒲公英**主页**链接 `pgyer.com/{shortcut}`（永久不变）；**不用** `pgyer.com/app/install/{key}` 直链——每次上传都会变
- `visible: false` 的 App 不进下载页（未上线 / 隐藏期）

### 入口管理（改入口时逐项检查）

| 入口 | 文件 | 说明 |
|---|---|---|
| 下载页卡片 | `apps.yml` | 脚本生成，别手改 `download.md` 生成区 |
| 首页卡片 | `docs/README.md` | 手写 `.app-grid` / `a.app-card`，与 apps.yml 需人工保持一致 |
| 导航 + 侧边栏 | `docs/.vuepress/config.js` | navbar「作品集合」下拉 + sidebar 按路径前缀分 App 配置 |

- **隐藏/恢复统一用注释**（HTML 注释 `<!-- 已隐藏 ... -->` 或 JS 注释），不删内容；搜「已隐藏」可定位所有隐藏点
- 当前临时状态（易变，以 config.js 注释为准）：iOS 审核期间 navbar 的「下载地址」「购买 PRO」被临时注释，过审后恢复

### 文档写作 SOP（基于代码补文档，不编造）

每个 App 文档目标形态 = **核心 5 件套 + 协议 3 件套**（结构参照 `voice/` 最佳实践）：

| 文件 | 定位 |
|---|---|
| `readme.md` / `guide.md` / `features.md` / `qa.md` / `why.md` | 介绍页（icon + 一句话 + 功能列表 + 下载）/ 快速上手（界面概览→基础操作分步骤→进阶）/ 功能详解（表格列参数）/ 8-12 个 Q&A / 缘起 |
| `contact.md` / `changelog.md` | 联系我们 / 更新日志 |
| `agreement.md` / `private.md` | 服务协议 / 隐私政策；`private.md` 参照 `music/private.md`，公司名统一「北京小茅屋科技有限公司」 |

- 纯文字，不放图片占位符（软著审核和文档站都不需要）
- `readme.md` 引用的页面必须真实存在，避免死链
- 内容以各项目仓库代码（README / AGENTS.md / 源码）为准，不凭空写

### 资源

- App 图标存冰封云 S3：`https://gudong.s3.bitiful.net/icon/<名称>`，可加 `?no-wait=on` 加速
- 部分老图在 `docs/public/img/` 与 jsdelivr CDN

## 3. 常用命令

```bash
npm install --legacy-peer-deps        # 必须 legacy-peer-deps
npm run docs:dev                      # 本地预览 http://localhost:8080
vuepress dev docs --port 5173        # 8080 被占用时
python3 docs/.vuepress/generate_apps_json.py   # 改 apps.yml 后单独重生成（含 download.md）
npm run docs:build                    # 自动先跑生成脚本再构建，产物 docs/.vuepress/dist
```

## 4. 部署（无发版概念）

- 流程：本地改 md / 配置 → commit → **push 到 main** → Cloudflare Pages 自动构建（`npm run docs:build`）并部署到 doc.gudong.site
- 无 `.github/workflows`、无 wrangler、无服务器运维；本地一般不需要手动 build，预览用 `docs:dev`
- 按上级规范默认只本地 commit 不 push；文档何时上线由咕咚决定

## 5. 维护本文

- 新增/删除 App 文档目录、改部署方式后，更新第 1 节清单与「最后核实」日期
- 上线状态、下载链接等易变数值一律指向 `apps.yml`，不在本文维护
