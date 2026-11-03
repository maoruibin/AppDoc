#  我的图床探索之路

如果只对结果感兴趣，可以一言以蔽之：

+   使用 [码云 ](https://gitee.com/) 作为图片存储仓库
+   PC 平台上使用 [PicGo ](https://picgo.github.io/PicGo-Doc/zh/) 作为上传工具
+   Android 平台使用 [PicPlus ](https://www.coolapk.com/apk/name.gudong.pic) 作为上传工具

更多探索过程，请阅读正文。

##  正文

自己从 2015 年开始折腾博客，要折腾博客，就免不了要跟图床打交道，因为博客文章不可避免的要使用远程图片。

##  我用过的那些图床

在很长一段时间内，博客中使用的图片都是存储在微博图床，也有存储在 [SM.MS ](https://sm.ms/) 图床，后来还使用过一段时间的七牛云图床。

不过到现在为止，他们大都有各种各样的问题。

微博图床很稳定、速度很快，曾是很多人钟爱的图床，但是从 2019 年开始加入防盗链，导致很多图片不能正常访问。而且上传到微博图床的图片，你根本没法管理，上传后你只知道它在微博的服务器上，但是却**不能删除或者管理它**，因为上传是匿名的。

后来使用过一段时间的 [SM.MS ](https://sm.ms/) 图床，这是一个小众图床，一开始也是匿名图床，不支持删除，后来加入了账户系统，登录后可以管理自己上传的图片，也不错，不过它是一家小厂商，而且 SM.MS 的访问速度并不快，所以也并没有用很久。

后来知道了七牛云。七牛云有一定量的免费使用空间，而且上传、下载速度很快，但是好景不长，后来有了各种限制，现在需要绑定已备案的域名才可以正常使用，所以后来便放弃了七牛。

##  发现 GitHub 图床

直到后来使用了 [PicGo ](https://picgo.github.io/PicGo-Doc/zh/)，这个跨平台图床软件后，才知道了原来可以使用 [GitHub ](https://github.com/) 作为图床。

![](https://cdn.nlark.com/yuque/0/2020/png/159409/1584167693943-7aa288f9-6b56-4570-8e59-08a0c98ea97f.png#align=left&display=inline&height=900&originHeight=900&originWidth=1600&size=0&status=done&style=none&width=1600)

> GitHub 世界上最广为人知的代码、文件托管平台，它是一个基本免费的服务，普通用户只需要注册一个账号即可免费使用大部分功能。

要使用它做图床，只需要创建一个代码仓库，然后进行一些配置，即可把图片上传到 GitHub，然后就可以访问了，具体配置可查看文章：[如何配置 Github 为自己的图床服务-PicPlus ](https://www.yuque.com/gudong-osksb/twgz5k/mdtyxi)。

而且，尽管 GitHub 在国外，但是服务一直相对稳定，很少有这样那样的限制，你要做的就是创建一个 GitHub 账号、然后创建一个仓库，接着配置就 OK，而且图片都存储在自己的账号下面，自己**随时去统一的管理删除**。

唯一不足的地方就是**它的访问速度**，因为它在国外，所以访问速度会受限，不过兵来将挡，水来土掩，有一个 CDN 加速服务商 [jsdelivr ](https://www.jsdelivr.com/) 可以为 GitHub 提供 CDN 加速。有了 jsdelivr 的加持，让 GitHub 做图床便更加顺畅。

![](https://cdn.nlark.com/yuque/0/2020/jpeg/159409/1584167693918-44fd471d-d9eb-4cb5-add0-a79a796a2784.jpeg#align=left&display=inline&height=964&originHeight=964&originWidth=1080&size=0&status=done&style=none&width=1080)

本来图床探索到这就结束了，但是后来发现还有更好的图床解决方案，那便是-**码云（英文名：gitee）**

##  更好的图床方案 - 码云

上面说了，GitHub 稳定，但是访问慢，因为它的服务器不在中国。那换个思路，如果国内有类似 GitHub 的服务，岂不是可以有更好的图床体验？

**是的，国内有[码云 ](https://gitee.com/)**，它是国内的代码托管平台，访问速度明显快于 GitHub。

使用过了一段时间的 GitHub 图床后，再使用码云做图床，上传和访问速度明显比 GitHub 快太多。

不过码云也有一些限制，但是基本不影响日常写作。

+   容量限制

> 规定每个仓库的大小上限为1个G，单个用户总容量为5个G  [from gitee terms ](https://gitee.com/terms)

+   图片大小限制

> 单个图片大小超过 1M 需要登录才可访问。

尽管有上面的两个限制，但是如果你在**上传前启用压缩**，则也不是什么大问题。

* * *

上面说过，我是使用 PicGo 这个软件后，才知道用 GitHub 可以做图床，后来通过 PicGo 还知道了可以用码云的服务做图床。但是 PicGo 是一个 **PC 软件**，而我经常在手机上写作，所以我需要在手机上也能有工具，可以便捷的把图片传到 GitHub、码云等图床。

##  手机端的图床上传方案

其实手机上的图床软件，之前也搜过，一直没有找到特别合适的。

sm.ms 很早就提供了 Android 客户端，但是速度慢，不支持自定义图床。

后来找到了[图床猫 ](https://www.coolapk.com/apk/com.by_syk.imagehosting)，但是作者弃更了，从 18年4月后再没有更新，APP 处于基本不可用的状态，而且支持的图床也有限，所以自己便开发了一款 Android 端的图床上传软件 - [PicPlus ](https://www.coolapk.com/apk/name.gudong.pic)，它支持 GitHub、码云做为图床，同时还支持了七牛云、阿里云、又拍云等主流图床。

![](https://cdn.nlark.com/yuque/0/2020/jpeg/159409/1584167693980-0978d1dd-15af-42b9-a621-ea960249d24a.jpeg#align=left&display=inline&height=2340&originHeight=2340&originWidth=1080&size=0&status=done&style=none&width=1080)

于此同时，为了更好的上传、使用体验，PicPlus 支持了以下几个特性：

+   支持上传前自动压缩图片
+   支持删除已上传的图片(本地图片以及云服务器中的图片)
+   支持格式化 URL 为 Markdown、HTML 格式
+   支持通过系统分享上传图片
+   支持自动复制链接
+   等等

PicPlus（现名咕咚云图）目前可在[应用宝](https://sj.qq.com/appdetail/name.gudong.pic)下载，最新版本也可通过[蒲公英](https://www.pgyer.com/picplus-android)获取。

##  关于我

咕咚同学，Android 工程师，独立软件开发者，喜欢篮球，喜欢写作，喜欢分享。

+   微博：[大侠咕咚 ](https://weibo.com/maoruibin)
+   公众号：咕咚同学
+   博客：[咕咚的个人博客 ](https://gudong.site/)
+   酷安：[咕咚 ](http://www.coolapk.com/u/509587)