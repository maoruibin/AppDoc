# 思源
[思源笔记](https://github.com/siyuan-note/siyuan) 是一款隐私优先的个人知识管理笔记系统。


由于 思源笔记 支持开放 Api，通过 Api 可以将笔记写入思源收集箱， 所以 inBox 笔记对 思源笔记的收集箱进行了支持，这样就可以通过在 inBox 中配置对应的 token，就可以将 inBox 笔记作为 思源笔记 的手机客户端。

> 这里的"同步至思源收集箱"是 inBox App 内置的功能（PRO），跟 [思源同步插件](plugin_siyuan.md) 是两套不同的机制。前者是 inBox 调思源 API 推一条笔记过去；后者是思源主动从云端拉全部历史并支持双向同步。按需选用，不冲突。

## 如何配置
> Tip: 同步到 思源笔记 为 inBox PRO 功能验。


1、下载 inBox 笔记，[去下载](./download.md)

2、打开 inBox 笔记，点击首页左上角菜单 > 设置 > 功能 > 同步至思源收集箱

<img src="../public/img/siyuan-two.jpg" width="60%" alt="">

在这里填入思源笔记的 API Token 即可，具体可以按照官方文档去获取：地址[https://siyuannote.com/docs/article/1725202960](https://siyuannote.com/docs/article/1725202960)

配置完毕后，打开同步开关，后面每次发送笔记后，都会自动同步到思源收集箱。

<img src="../public/img/siyuan-one.jpg" width="60%" alt="">



## QA

### 这个跟"思源同步插件"有什么区别？

- **App 内置（本页）**：你写一条笔记，inBox 推一条到思源收集箱。单向、按条推送，是 inBox App 的 PRO 功能。
- **[思源同步插件](plugin_siyuan.md)**：在思源里装个插件，主动从 inBox 云端拉全部历史笔记，支持双向同步（在思源里改了能传回去）。完全免费开源，但需要自行配置 WebDAV/S3。

如果你只是想把新写的笔记随手推到思源，用本页的方案就够了。如果你想在思源里完整管理 inBox 的所有历史笔记、并做双向同步，用插件。

