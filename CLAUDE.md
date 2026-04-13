# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppDoc is a static documentation website built with VuePress v2. It serves as the documentation portal for several personal applications (inBox 笔记, 仓咚咚, 点亮, 咕咚订阅, 咕咚云图). All content is in Simplified Chinese.

**Repository**: `git@github.com:maoruibin/AppDoc.git`
**Live**: https://doc.gudong.site

## Development Commands

```bash
# Install dependencies (must use legacy-peer-deps)
npm install --legacy-peer-deps

# Development server (runs on http://localhost:8080/)
npm run docs:dev

# Production build (outputs to docs/.vuepress/dist)
npm run docs:build

# Change port if 8080 is occupied
vuepress dev docs --port 5173
```

## Environment Requirements

- Node.js >= 18 (recommended: 20)
- npm >= 9

## Architecture

The site is organized by application, with each app having its own directory under `docs/`:

- `docs/inbox/` - inBox 笔记 (note-taking app)
- `docs/cang/` - 仓咚咚 (asset management)
- `docs/light/` - 点亮 (habit tracking)
- `docs/rssplus/` - 咕咚订阅 (RSS reader)
- `docs/picplus/` - 咕咚云图 (image hosting)

### Configuration

All site configuration is centralized in `docs/.vuepress/config.js`:
- Navigation bar (navbar)
- Sidebar structure for each app
- Theme settings
- Markdown extensions
- Webpack/Sass configuration

### Sidebar Structure

Each app has its own sidebar configuration with sections like:
- 你好 (Hello) - introduction, FAQ, changelog
- 数据 (Data) - backup, WebDAV
- 功能 (Features) - specific feature documentation
- 教程 (Tutorials) - how-to guides
- 服务协议 (Service Terms) - privacy policy, terms of service
- 关于 (About) - contact, download links

## Deployment

- **Platform**: Cloudflare Pages (Git integration)
- **Flow**: `git push` → Cloudflare auto-build → deploy to CDN
- **Build command**: `npm run docs:build`
- **Output directory**: `docs/.vuepress/dist`
- **Custom domain**: doc.gudong.site
- **No wrangler or CI scripts** — fully managed by Cloudflare Pages Git integration

## Important Notes

- The `--legacy-peer-deps` flag is required for npm install due to dependency compatibility
- External images use CDNs (jsdelivr.net, bitiful.net)
- No test framework or linting tools configured
- The site uses VuePress 2.0.0-rc (Release Candidate)
