# inBox 同步插件（思源笔记）

把 inBox 云端的笔记同步到 [思源笔记](https://b3log.org/siyuan/) 的第三方插件。

> 这是个独立插件，跟你 [在 inBox App 里配 API Token 同步到思源收集箱](siyuan.md) 是两套不同的机制，互不冲突，按需选用。

## 它能做什么

- **双向同步**：inBox 云端 ↔ 思源笔记本
  - 云端 → 思源：下载笔记，渲染为思源文档
  - 思源 → 云端：在思源里改了笔记内容或标题，下次同步上传覆盖云端；删了思源文档，云端对应笔记标记软删除
  - **不支持新建**：新笔记请在 inBox App 创建
- **多存储后端**：WebDAV / S3 兼容存储（Bitiful、腾讯云 COS、阿里云 OSS 等）
- **增量同步**：基于 ETag + mtime，未变化的笔记直接跳过
- **资源同步**：图片、视频、录音、附件，落到 `data/assets/inbox-sync/`
- **批注支持**：ver=2 内联批注渲染为父笔记末尾的 blockquote；独立批注作为父笔记末尾的块引用
- **盒子分文件夹**：按盒子归到 `/<盒子名>/` 子文档下，无盒子进根目录平铺。盒子改名/删除时自动对账（批量 move 文档 + 同步 `custom-box`）
- **笔记间链接**：保留 inBox 原文 `[[note-xxx]]`（v0.2 以纯文本展示，块级转换在后续版本）

## 跟 inBox App 内置的思源同步有什么区别？

| | inBox App 的"同步至思源收集箱" | 本插件（siyuan-inbox-sync） |
| --- | --- | --- |
| 工作方式 | inBox 调思源 API 推到收集箱 | 思源插件主动从云端拉 |
| 同步方向 | 单向（inBox → 思源） | 双向（修改/软删除都同步） |
| 数据来源 | inBox 本地数据 | inBox 云端数据（WebDAV/S3） |
| 资源同步 | 不支持 | 支持（图片/录音/附件） |
| 盒子分文件夹 | 不支持 | 支持 |
| 增量同步 | 否（每次全量推一条） | 是（ETag + mtime） |
| 配置位置 | inBox App 设置 | 思源插件设置 |
| 是否 PRO | PRO 功能 | 完全免费开源 |

简单说：

- **App 内置**：每发一条笔记推一条到思源，适合只想"随手备份到思源"的用户
- **本插件**：把思源当作 inBox 的桌面端，能完整拉历史、能双向同步，适合"在思源里管理 inBox 笔记"的用户

## 安装

### 方式 1：手动安装（推荐）

1. 从 GitHub Releases 下载最新的 `package.zip`
2. 在思源笔记里打开文件管理器，进入工作空间的 `data/plugins/` 目录
3. 新建文件夹 `siyuan-inbox-sync/`，把 `package.zip` 里的所有文件解压到该目录
4. 重启思源或在 **设置 → 饥饿插件** 中点 **刷新**，然后启用 **inBox 同步**

> 项目地址：[github.com/maoruibin/siyuan-inbox-sync](https://github.com/maoruibin/siyuan-inbox-sync)

### 方式 2：从源码构建

```bash
git clone https://github.com/maoruibin/siyuan-inbox-sync.git
cd siyuan-inbox-sync
npm install
npm run package     # 一键构建 + 打包成 package.zip
```

把生成的 `package.zip` 解压到 `data/plugins/siyuan-inbox-sync/` 即可。

## 配置

### 第 1 步：选目标笔记本

在思源里建一个专门存放同步笔记的笔记本（比如叫「inBox」），后面在插件设置里要选它。

建议单独建一个新笔记本，别跟现有笔记本混用，方便管理。

### 第 2 步：配置云存储

打开插件设置（顶栏图标 → 设置），按你的存储类型填。

**WebDAV**：

- URL：你的 WebDAV 服务地址（如 `https://dav.jianguoyun.com/dav/`）
- 用户名 / 密码（坚果云需要用应用专属密码，详见 [WebDAV 教程](lesson-webdav.md)）
- 云端根目录：默认 `inBox`，对应 inBox App 的同步根

**S3 兼容**：

- Endpoint：如 `https://s3.bitiful.net` 或腾讯云 COS 地址
- Access Key / Secret Key / Bucket / Region
- 同上，云端根目录默认 `inBox`

> 这里的云端配置要跟 inBox App 端配置的云存储是同一份，否则同步不到同一个数据源。

### 第 3 步：选笔记本 + 子路径

- **目标笔记本**：下拉选第 1 步建的那个
- **子路径**：可选，比如填 `/inBox`，所有笔记会落到笔记本下的 `/inBox/` 文档下；留空就是笔记本根

### 第 4 步：测试连接 → 立即同步

点 **测试连接**，验证云存储可达。然后点顶栏的同步图标（或设置里 **立即同步**），第一次会拉全部笔记，之后只拉变化的。

## 文档树结构

同步后的思源笔记本按盒子组织：

```
{笔记本}/
├── inBox/                         # 子路径（可在设置里改）
│   ├── 默认笔记.md                # 无盒子笔记(根平铺)
│   ├── 工作/                      # "工作"盒子下所有笔记
│   │   ├── project-xxx.md
│   │   └── meeting-notes.md
│   └── 生活/                      # "生活"盒子
│       └── shopping.md
└── assets/inbox-sync/             # 资源(所有盒子共享, 不按盒子分)
    ├── images/
    ├── videos/
    ├── audios/
    └── attachments/
```

**盒子文件夹规则：**

- 笔记 `content.box_id` 在云端 `boxes.json` 里查到 → 进 `<盒子名>/` 子文档
- 否则（无盒子 / 盒子被删墓碑 / boxes.json 为空）→ 根平铺
- 盒子在 inBox App 改名 → 该 boxId 下所有文档 move 到新路径 + 同步更新 `custom-box`
- 盒子在 inBox App 删除 → 该 boxId 下所有文档 move 回根 + 清 `custom-box`
- 资源统一放 `data/assets/inbox-sync/`，不按盒子分

## 字段映射

inBox 的 atomicNote → 思源文档：

| inBox 字段 | 思源落点 |
| --- | --- |
| `id` (note-xxx) | 文档自定义属性 `custom-inbox-id` |
| `content.title` | 文档名（无标题时用创建时间） |
| `content.content` | 文档正文块 |
| `meta.created_at` / `updated_at` | `custom-inbox-created` / `-updated` |
| `content.box_id`（经 boxes.json 解析为名称） | `custom-box`（无盒子不写） |
| `tags`（从正文 `#tag` 提取） | `custom-inbox-tags`，正文保留 `#tag` |
| `parentId` | `custom-inbox-parent`（noteId） |
| ver=2 内联 `annotations[]` | 父笔记末尾的 `> **批注**` 引用块 |
| 独立批注子笔记（有 `parentId`） | 独立文档 + 父笔记末尾的块引用 `((childDocId))` |

## 双向同步说明

### 上传触发条件

每次同步结束时扫描本地变更：

| 场景 | 行为 |
| --- | --- |
| 文档的 `updated` 时间 > 上次同步基线 | 上传修改 |
| 思源文档被删除（在 metadata 里有记录） | 上传软删除（`is_removed=true`） |
| 笔记本次同步刚被下载/写入 | 不上传（基线已重置为新时间） |

### 冲突处理（LWW，云端优先）

如果同一笔记在云端和本地都改了：

1. 下载阶段先发生 → 本地修改被覆盖
2. 基线重置为覆盖后的时间
3. 上传阶段比对发现无变化 → 不上传

结果：云端版本胜出，本地修改丢失。这是有意为之的简单策略，避免双向合并的复杂性。建议同步前确认网络稳定。

### 软删除语义

- 思源里删除文档 → 云端对应笔记 `flags.is_removed = true`（不物理删除文件）
- 跟 inBox App 的删除行为一致，App 端下次同步看到 `is_removed` 会做对应清理

## 已知限制

- **不支持在思源里新建笔记**：新建请在 inBox App 完成，插件只同步已有 noteId 的笔记
- **盒子管理**：盒子的创建/重命名/删除需在 inBox App 完成（插件只读 boxes.json）
- **资源回传**：在思源里新增的图片不会上传到云端（只同步文本）
- **批注块**：用户在思源里改父笔记末尾的「批注引用块」不会同步到云端（上传时会自动剥离这部分）
- **冲突处理**：LWW，可能丢一边修改
- `[[note-xxx]]` 笔记间链接暂未转换为思源块引用，正文里以纯文本展示
- 桌面端思源优先；移动端有 CORS 限制，可能需要走 `/api/network/forwardProxy`（未实现）

## 反馈与问题

- GitHub Issues：[siyuan-inbox-sync/issues](https://github.com/maoruibin/siyuan-inbox-sync/issues)
- 联系方式：见 [联系我们](contact.md)
