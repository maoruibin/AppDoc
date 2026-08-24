#  Api

inBox 笔记支持通过 Api 快速记录笔记

::: tip
该功能默认开放
:::



##  什么是 API

API 是一个 url 地址，每个 inBox 的注册用户都会有一个专属的 Api 地址，通过该地址，可以在任何平台，通过改 Api 地址快速将灵感笔记，记录到 inBox 中。

Api 地址位于账号页面，具体路径: **首页>侧边菜单>设置>账户>Api** 如下所示：

![](https://s2.loli.net/2022/08/17/DhTez9s8wMH4nPQ.jpg)

##  使用

开发者可以根据以下接口说明，在自己平台上使用 api 进行便捷的笔记输入，开发者有任何插件提交，可以联系作者，也可以在 github 上进行作品说明：[inBox Discussions ](https://github.com/maoruibin/inBox/discussions)

> 非开发者同学，可以关注 [api-周边](#api-%E5%91%A8%E8%BE%B9)

###  接口信息

+   **接口地址：**`https://api.gudong.site/inbox/${userToken}`
+   **请求方式**：`POST`
+   **Content-Type**：`application/json`

> 请求频率：每天最多上传 50 条

###  请求参数

| 参数 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| content | 字符串 | 是 | 笔记内容，最多3000字符 |
| title | 字符串 | 选填 | 笔记标题 |

###  请求响应

```json
{
  "code":0,
  "msg":"已提交，请打开inBox查看笔记"}
}
```

> tip：code 为 0 请求成功，非零状态均为失败

####  是否支持上传图片

inBox 不支持上传图片，但是支持解析 Markdown 格式的 img 标签，所以你可以在笔记内容中添加 markdown 格式的 img 标签，前提是图片上传到了图床，这样通过 Api 发送后，在 inBox 笔记中将会自动解析出远程图片。比如通过 Api 发送如下格式的笔记内容

```markdown
今天天气很好，![](https://s2.loli.net/2022/04/20/B6t4IMmLSQRN78E.jpg)
```

##  Api 周边

> 基于 Api 可以在任意平台上开发各种工具，然后将笔记通过 Api 发送到 inBox，下面是各位热心的用户朋友开发的一些工具。

| 插件&工具 | 详细说明 | 介绍 | 作者 |
| --- | --- | --- | --- |
| Chrome 插件 | [inBox 笔记 ](https://github.com/maoruibin/ChromeInBox) | 通过 Chrome 浏览器发送笔记到 inBox | 咕咚 |
| uTools 插件 | [inBox go ](https://www.coolapk.com/feed/49419369?shareKey=NjA0YTRiMmRiMzcxNjU1NzM2NzA~) | 结合 uTools 在 PC 上快速记录笔记到 inBox | lang |
| fooView 任务 | [FV悬浮球 ](https://kdocs.cn/l/ck9k72lZJBpG) | 自定义任务发送手机粘贴板等内容到 inBox | Runos |
| Quicker | [inbox同步到本地 ](https://getquicker.net/Sharedaction?code=f467416b-feed-440c-7c75-08dbeef8975e) | 同步 inBox 笔记到本地 | Runos |
| Python 脚本 | [inbox同步到本地 ](https://gitee.com/jjtenger/inbox-pc-sync) | 同步 inBox 笔记到本地 | tenger |
| Kindle2flomo | [kindle ](https://mp.weixin.qq.com/s/bukxVGAFLPX2jdU4yD7h2A) | 将 kindle 笔记发送到 inBox | 鲁鹏 |
| MCP 组件 v1 | [ mcp-server-inbox ](https://github.com/maoruibin/mcp-server-inbox) | 在 MCP 客户端中将笔记写入 inBox 笔记 | 咕咚 |
| MCP 组件 v2 | [ mcp-server-inbox-v2](https://github.com/sseaan/mcp-server-inbox) | 在 MCP 客户端中将笔记写入 inBox 笔记 | Him |