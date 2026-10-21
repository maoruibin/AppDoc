# Scheme 开放链接

好内容支持通过 `gucontent://` scheme 被其他应用直接打开。在笔记、网页、快捷指令、你自己的应用里写一条链接，点击即可：

- **打开某篇文章的精读页**（划线、想法、听内容全量可用）
- **把一个网址直接交给好内容收藏**（后台解析入库，与系统分享同一链路）
- **打开搜索并预填关键词**

> 典型用法：在 inBox 笔记里粘贴好内容文章的链接，之后任何时候点这条链接，都能直达那篇文章。

## 环境要求

| 应用 | 版本要求 | 说明 |
|---|---|---|
| 好内容（Android / iOS） | **0.2.25 及以上** | scheme 注册与全部四个动作 |
| inBox 笔记（Android） | 链接识别任意版本；**点击直达需 2026-10 之后发布的版本** | 旧版里链接已显示为可点，但点击不会有反应 |

## 能力总览

| URI | 作用 |
|---|---|
| `gucontent://article?id=[文章id]` | 打开指定文章的精读页 |
| `gucontent://add?url=[网页链接]` | 快速收藏一个网页 |
| `gucontent://search?keyword=[关键词]` | 打开搜索并预填关键词 |
| `gucontent://home` | 回到文章库（收藏流） |

---

## 打开文章精读页

**gucontent://article?id=[文章id]**

| 参数 | 必填 | 说明 |
|---|---|---|
| `id` | 是* | 文章 id。在好内容中打开这篇文章 → 底部「详情」面板 → **「复制文章链接」**，即可获得现成的链接 |
| `url` | 否 | 原文链接（URL 编码），作为兜底定位：id 未命中（文章未同步到本机 / 删后重存）时按原文链接查找 |

> *`id` 与 `url` 至少给一个。文章已删除或两参都未命中时，好内容会提示「文章不存在或已删除」。
> id 是不透明字符串，请原样传递（复制出来的链接不要改写 id 部分）。

**「复制文章链接」复制出来的是 Markdown 格式**（0.2.25 及以上）：

```markdown
[文章标题](gucontent://article?id=1761012345678)
```

粘贴到 inBox 等支持 Markdown 的笔记里，会正常按链接渲染——**显示文章标题、隐藏链接本体，点击直达精读页**；直接粘贴裸链接 `gucontent://article?id=…` 同样可点，只是显示完整链接文本。

## 快速收藏网页

**gucontent://add?url=[网页链接]**

| 参数 | 必填 | 说明 |
|---|---|---|
| `url` | 是 | 要收藏的文章链接，**必须 URL 编码** |
| `open` | 否 | `open=1`：收藏成功后直接打开这篇文章的精读页；缺省为留在文章库看保存进度 |

行为与「系统分享到好内容」完全一致：切到文章库、顶部出现保存进度卡片、后台解析入库（正文与图片本地化）；微信公众号、即刻、微博、B 站专栏、博客等均支持。免费版收藏上限 50 篇，超限会在应用内弹出升级提示。

## 搜索文章

**gucontent://search?keyword=[关键词]**
> keyword 中文需 URL 编码。打开搜索页并预填关键词，回车即出结果。

## 打开文章库

**gucontent://home**

---

## URL 编码（重要）

链接参数里的网址、关键词**必须 URL 编码**，否则参数中出现的 `&`、`?`、中文会破坏链接结构（最常见症状：参数被截断）。

```text
原始：https://mp.weixin.qq.com/s/abc?x=1
编码：https%3A%2F%2Fmp.weixin.qq.com%2Fs%2Fabc%3Fx%3D1

完整示例：
gucontent://add?url=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2Fabc
```

各语言编码方式：

```js
// JavaScript
encodeURIComponent('https://mp.weixin.qq.com/s/abc')
```

```dart
// Dart / Flutter
Uri.encodeComponent('https://mp.weixin.qq.com/s/abc')
```

```kotlin
// Android (Kotlin)
Uri.encode("https://mp.weixin.qq.com/s/abc")
```

```swift
// iOS (Swift)
"https://mp.weixin.qq.com/s/abc".addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)
```

## 各端调用示例

### 网页 / HTML

```html
<a href="gucontent://article?id=1761012345678">在好内容中打开这篇文章</a>
```

```js
// JS 跳转
window.location.href = 'gucontent://add?url=' + encodeURIComponent(currentUrl);
```

### Android 应用内（Kotlin）

```kotlin
// 隐式拉起（系统可能弹「打开方式」选择框）
startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("gucontent://article?id=$id")))

// 精确拉起好内容（跳过选择框；debug 包为 name.gudong.content.debug）
startActivity(
    Intent(Intent.ACTION_VIEW, Uri.parse("gucontent://add?url=$encoded"))
        .setPackage("name.gudong.content")
)
```

### iOS 应用内（Swift）

```swift
if let url = URL(string: "gucontent://article?id=\(id)") {
    UIApplication.shared.open(url)
}
```

### inBox 笔记

直接把好内容「复制文章链接」（详情面板里）得到的 **Markdown 链接**粘贴进笔记正文，它会按链接渲染：显示文章标题、隐藏链接，点击直达精读页——读到哪篇存哪篇，笔记里留下一排可点的文章标题。也可以手写 Markdown 链接自定义显示文字，或直接粘贴裸链接（显示完整链接文本，同样可点）：

```markdown
[这篇文章值得精读](gucontent://article?id=1761012345678)
```

### iOS 快捷指令

用「URL」动作拼接 `gucontent://add?url=` + 「URL 编码」动作处理目标网址，再用「打开 URL」动作运行——即可给任意 App 做「存到好内容」的快捷入口。

## 消费方需知（行为细节）

- **冷启动 / 热启动都支持**：好内容未运行时点链接会先启动应用再自动跳转。
- **未安装好内容时**：Android 一般提示「没有可执行此操作的应用」，iOS `open(url)` 返回 false；调用方可自行引导下载。
- **自定义 scheme 的通病**：微信、QQ 等应用的内置浏览器禁止 scheme 跳转，这类场景请改用「系统分享到好内容」或「复制链接后打开好内容」；系统浏览器（Chrome/Safari）点击 scheme 链接会先弹一次确认框。
- **scheme 可能被抢注**：任何应用都可声明同名 scheme，隐式拉起存在被其他应用截胡的可能——对确定性要求高的场景请用上面 Android 示例中的 `setPackage` 精确拉起。
- **文章定位的跨设备语义**：`id` 在已登录并云同步的设备间一致；仅存在于一台设备的文章，在其他设备上只能通过 `url` 兜底参数按原文链接找到。

## 反馈

对接中遇到问题欢迎[联系我们](/content/contact)。
