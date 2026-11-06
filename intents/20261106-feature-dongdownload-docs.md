# intent：新增存咚咚文档子站

- **id**：20261106-feature-dongdownload-docs
- **project**：AppDoc
- **type**：feature
- **source**：DongDownload intent 20261106-feature-account-sdk-quota；咕咚确认开工
- **status**：accepted
- **date**：2026-11-06

## 问题是什么

gudong_account SDK 的关于页、隐私门、协议、在线文档和更新日志依赖 `app.gudong.site/download/` 文档子站。存咚咚目前没有任何文档页。

## 成功标准

- [ ] 新增 `docs/download/`，包含 `README.md`、`download.md`、`agreement.md`、`private.md`、`changelog.md`
- [ ] 文档站首页/下载入口包含存咚咚
- [ ] 本地构建或静态检查通过

## 不做什么

- 不做营销长文
- 不写未经确认的具体下载链接与价格，先用占位或既有生态格式

## 约束

- 遵守 AppDoc AGENTS.md
- 隐私政策必须覆盖：剪贴板、WebView、账号、解析配额、MediaStore、日志与更新检查

## 结果回填（完成后由 AI 填，咕咚核）

- **commit**：0e9bff6
- **验证证据**：`npm run docs:build` 成功，渲染 260 页；生成 apps.json 24 个应用、可见 18 个
- **结论**：done（未 push，上线由咕咚决定）
