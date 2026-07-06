# Obsidian 同步插件

把 inBox 云端的笔记同步到 [Obsidian](https://obsidian.md/) vault 的社区插件。

> 项目地址：[github.com/maoruibin/obsidian-inbox-sync](https://github.com/maoruibin/obsidian-inbox-sync)

## 它能做什么

- **单向同步（云端 → Obsidian）**：只下载不上传
  - inBox App 是收集端，Obsidian 是工作台
  - 在 Obsidian 里编辑/删除文档不会回传到云端
  - 不支持在 Obsidian 里新建笔记（新笔记请在 inBox App 创建）
- **多存储后端**：WebDAV / S3 兼容存储（Bitiful、腾讯云 COS、阿里云 OSS 等）
- **增量同步**：基于 ETag + mtime，未变化的笔记直接跳过
- **资源同步**：图片、视频、录音、附件,落到 vault 内的 `assets/` 目录
- **批注支持**：ver=2 内联批注渲染为父笔记末尾的 blockquote;独立批注作为父笔记末尾的嵌入引用
- **盒子分文件夹**：按盒子归到 `<盒子名>/` 子文件夹下,无盒子进根目录平铺。盒子改名/删除时自动对账(rename 文件夹 + 同步 frontmatter `box` 字段)
- **标签 frontmatter**：自动从正文提取 `#tag` 写到 frontmatter `tags`,可在 Obsidian 标签面板直接看到
- **笔记间链接**：`[[note-xxx]]` / `[[Card123]]` 自动转换为 Obsidian 文件名引用

## 跟 inBox App 内置的"导出到 Obsidian"有什么区别？

| | inBox App 的"导出到 Obsidian" | 本插件(obsidian-inbox-sync) |
| --- | --- | --- |
| 工作方式 | inBox 调 Obsidian Local REST API 推 | Obsidian 插件主动从云端拉 |
| 同步方向 | 单向(inBox → Obsidian) | 单向(云端 → Obsidian,只读副本) |
| 数据来源 | inBox 本地数据 | inBox 云端数据(WebDAV/S3) |
| 资源同步 | 不支持 | 支持(图片/录音/附件) |
| 盒子分文件夹 | 不支持 | 支持 |
| 增量同步 | 否(每次全量推一条) | 是(ETag + mtime) |
| 配置位置 | inBox App 设置 | Obsidian 插件设置 |
| 依赖 | 需装 Local REST API 插件 | 不依赖其他插件 |

简单说：

- **App 内置**：每发一条笔记推一条到 Obsidian,适合只想"随手备份到 Obsidian"的用户
- **本插件**：把 Obsidian 当作 inBox 的只读工作台,能完整拉历史、能按盒子分文件夹,适合"在 Obsidian 里管理 inBox 笔记"的用户

## 安装

### 方式 1：BRAT 安装(推荐)

插件尚未进入 Obsidian 官方社区目录(审核排队中),目前推荐用 [BRAT](https://github.com/TfTHacker/obsidian42-brat) 从 GitHub 仓库直接安装,并自动接收更新。

1. 在 Obsidian 中安装并启用 **BRAT** 插件(社区目录可搜到)
2. 打开 BRAT 设置 → **Add Beta plugin** → 输入仓库地址：
   ```
   maoruibin/obsidian-inbox-sync
   ```
3. 回到 Obsidian 设置 → 社区插件,启用 **inBox Sync**

之后本仓库发版,BRAT 会自动拉取更新。

### 方式 2：手动安装

1. 从 [Releases](https://github.com/maoruibin/obsidian-inbox-sync/releases) 下载 `main.js`、`manifest.json`、`styles.css`
2. 把文件放到 Obsidian vault 的插件目录：`.obsidian/plugins/inbox-sync/`
3. 在 Obsidian 设置中启用 **inBox Sync**

> 升级时需要重复上述步骤手动替换文件,所以非开发者推荐用 BRAT。

## 配置

### WebDAV 配置

1. 在设置中选择存储类型为 "WebDAV"
2. 填写 WebDAV 服务器地址、用户名、密码
   - 坚果云需要用应用专属密码,详见 [WebDAV 教程](lesson-webdav.md)
3. 设置 inBox 数据路径(默认：`inBox`,对应 inBox App 的同步根)

### S3 配置

1. 在设置中选择存储类型为 "S3 Compatible"
2. 填写 S3 端点、Access Key、Secret Key、Bucket
3. 设置 Region 和云端根目录

> 这里的云端配置要跟 inBox App 端配置的云存储是同一份,否则同步不到同一个数据源。

### 同步设置

- **Vault 文件夹路径**：笔记在 vault 中的存储位置(默认：`inBox`)
- **自动同步间隔**：自动同步的时间间隔(分钟),设为 0 表示不自动同步
- **启用 frontmatter tags**：是否把笔记正文里的 `#tag` 写到 frontmatter `tags` 字段

## 目录结构

同步后的目录结构会按盒子组织：

```
inBox/
├── notes/                          # 无盒子笔记(根目录平铺)
│   ├── 2025-04-10 note-title.md
│   └── 2025-04-11 another.md
├── 工作/                            # "工作"盒子下的笔记
│   └── project-xxx.md
├── 生活/                            # "生活"盒子下的笔记
│   └── shopping-list.md
├── assets/                          # 资源文件(所有盒子共享)
│   ├── images/
│   │   └── photo.jpg
│   ├── videos/
│   │   └── video.mp4
│   ├── audios/
│   │   └── recording.mp3
│   └── attachments/
│       └── file.pdf
└── .inbox-sync-meta.json          # 同步元数据(含盒子文件夹映射)
```

**盒子文件夹规则：**

- 笔记的 `content.box_id` 在云端 `boxes.json` 里查得到 → 进 `<盒子名>/` 子文件夹
- 否则(无盒子 / 盒子被删墓碑)→ 根目录 `inBox/` 平铺
- 用户没配盒子时,所有笔记自然都在根目录
- 盒子重命名时,文件夹自动 rename,frontmatter `box:` 字段同步更新
- 盒子删除时,文件夹内笔记移回根目录,文件夹清空
- 资源文件统一放 `assets/`,不按盒子分

盒子名清洗规则：`/ \ : * ? " < > |` 替换为 `-`,空名 fallback 到 box_id 短码,撞名追加 box_id 后缀。

## Markdown 格式

同步后的笔记包含 YAML frontmatter：

```markdown
---
title: 今日记录
inbox_id: note-abc123
created: 2025-04-10T10:30:00.000Z
updated: 2025-04-10T10:30:00.000Z
box: 工作
tags:
  - 日记/生活
  - 心情/开心
---

#日记/生活
今天天气不错 #心情/开心

![[../assets/images/2025/04/photo.jpg]]
```

字段说明：

- `inbox_id`：笔记的唯一 ID(`note-xxx` 格式),**不要手动修改**,是同步的锚点
- `box`：笔记所属的[盒子](box.md)(来自云端 `boxes.json`),无盒子的笔记不会写这一行
- `created` / `updated`：ISO 时间戳
- `tags`：自动从正文 `#tag` 提取的标签
- `parent`：如果是批注笔记,会指向父笔记的文件名引用

## 删除语义

- 在 inBox App 删除笔记 → 云端 `flags.is_removed=true` → 插件下次同步时移除 Obsidian 对应文件
- 在 Obsidian 里删文件 → **不影响云端**(单向同步,Obsidian 是只读副本)

## 为什么是单向同步？

inBox 的定位是**收集箱**,所有笔记/批注/盒子都在 App 端创建。Obsidian 这边当作**只读工作台**:能完整拉历史、按盒子分文件夹、查标签,但不把 Obsidian 里的编辑/删除回传到云端。

之前版本试过双向同步(本地修改上传、本地删除软删云端),实际使用中暴露两个问题:

1. **基线机制脆弱**:`vault.modify` 写 frontmatter 会改 mtime,必须维护 `lastLocalMtime` 基线避免无限循环。一旦基线错乱(同步中断、手动改文件、跨设备),就会误判本地有改动而反复上传
2. **WebDAV 缓存导致脏数据**:坚果云等 WebDAV 服务会缓存旧版本,双向同步时上传的 `is_removed=true` 会被缓存,导致其他端拉到错误的软删除状态,笔记"删了又复活"

权衡之后回归单向:inBox 是收集端,Obsidian 是工作台,职责分离更清晰,也避免双向同步的复杂性 + 误删风险。

## 已知限制

- 不支持在 Obsidian 新建笔记(无 `inbox_id` 不会被同步,新笔记请在 inBox App 创建)
- 不支持回传:在 Obsidian 里编辑/删除文档不会影响云端(单向同步)
- 盒子的创建/重命名/删除需在 inBox App 完成(插件只读 boxes.json)
- 移动端 Obsidian 有 CORS 限制,WebDAV/S3 直连可能失败,桌面端优先

## 反馈与问题

- GitHub Issues：[obsidian-inbox-sync/issues](https://github.com/maoruibin/obsidian-inbox-sync/issues)
- 联系方式：见 [联系我们](contact.md)
