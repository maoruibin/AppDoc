# 本地开发与调试

## 环境要求
- Node.js `>= 18`（建议 20），npm `>= 9`

## 安装依赖
- 首次安装：`npm install --legacy-peer-deps`

## 本地启动
- 开发预览：`npm run docs:dev`
- 访问地址：`http://localhost:8080/`

## 构建生产
- 构建命令：`npm run docs:build`
- 构建产物目录：`docs/.vuepress/dist`

## 常见问题
- 端口占用：`vuepress dev docs --port 5173`
- 依赖冲突：使用 `npm install --legacy-peer-deps`
- 大文件限制：避免将 `*.apk` 加入仓库，或使用 Git LFS

## 仓库地址
- GitHub: https://github.com/maoruibin/AppDoc
- Git: `git@github.com:maoruibin/AppDoc.git`

## 部署（Cloudflare Pages）
- **方式**: GitHub Push → Cloudflare Pages 自动构建部署
- **Build 命令**: `npm run docs:build`
- **Output 目录**: `docs/.vuepress/dist`
- **域名**: doc.gudong.site
- **流程**: 本地修改 md → git push → Cloudflare 自动完成剩余工作

