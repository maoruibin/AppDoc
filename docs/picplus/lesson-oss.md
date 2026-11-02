# 配置 阿里云 OSS 为个人图床

## 写在前面

使用阿里云 OSS 做图床之前，需要先注册阿里云账号并开通对象存储 OSS 服务：

[https://www.aliyun.com/](https://www.aliyun.com/)

OSS 按量计费，个人图床的图片量级下费用极低（存储 + 少量请求流量，通常每月几毛钱以内），无需预付费套餐。

> 阿里云 OSS 通过 S3 兼容协议接入，App 内不需要安装任何厂商 SDK。配置入口：图床管理 → 新增图床 → 选择「阿里云 OSS」。

## 配置需要的参数

+ Access Key（AccessKeyId，LTAI 开头）
+ Access Secret（AccessKey Secret）
+ Bucket（存储桶名称）
+ 地域（Region，如 oss-cn-beijing）
+ Endpoint（如 oss-cn-beijing.aliyuncs.com，填了地域可自动推导）

## 第一步：创建 Bucket

打开 OSS 控制台的 Bucket 列表页：

[https://oss.console.aliyun.com/bucket](https://oss.console.aliyun.com/bucket)

点击「创建 Bucket」，注意三项：

+ **Bucket 名称**：全局唯一，小写字母开头，可含数字和中划线，例如 `gudong-img-bucket`。App 里只填这个名称，不带地域后缀。
+ **地域**：选离你近的即可（如华北 2（北京）对应 `oss-cn-beijing`、华东 1（杭州）对应 `oss-cn-hangzhou`）。创建后在 Bucket 概览页可以看到完整地域 ID，记下来备用。
+ **读写权限**：做图床选「**公共读**」（图片链接可直接在浏览器打开）；如果想保持私有，也可以选「私有」，但必须在 App 高级配置里填写「公开访问域名」（如绑定了 CDN 的自定义域名），否则上传成功后拿不到能直接访问的图片链接。

## 第二步：获取 AccessKey

**强烈建议使用 RAM 子账号的密钥，不要使用阿里云主账号的 AccessKey**——子账号密钥泄露后影响范围可控，且可以随时单独吊销。

打开 RAM 控制台的用户列表页：

[https://ram.console.aliyun.com/users](https://ram.console.aliyun.com/users)

1. 点击「创建用户」，登录方式无需勾选控制台访问，只需 OpenAPI 调用。
2. 为该用户授权 `AliyunOSSFullAccess`（OSS 完整权限）；图床只用上传 / 下载 / 删除的话，也可以用自定义权限最小化到 `oss:PutObject`、`oss:GetObject`、`oss:DeleteObject`。
3. 创建完成后进入用户详情，点击「创建 AccessKey」，得到一对 AccessKeyId（LTAI 开头）和 AccessKey Secret。

> AccessKey Secret 只在创建时完整显示一次，务必当场复制保存，发送到手机备用即可。

## 第三步：在 App 中填写

打开 PicPlus 的阿里云 OSS 配置表单，逐项填入：

| 表单项 | 填什么 | 示例 |
|---|---|---|
| Access Key (RAM) | RAM 用户的 AccessKeyId | `LTAI5t...` |
| Access Secret | 对应的 AccessKey Secret | — |
| Bucket | Bucket 名称（不带地域后缀） | `gudong-img-bucket` |
| 地域 (Region) | Bucket 概览页的地域 ID | `oss-cn-beijing` |
| Endpoint | 所在地域的外网 Endpoint | `oss-cn-beijing.aliyuncs.com` |

地域填 `cn-beijing` 这种短写法也可以，App 会自动补全为 `oss-cn-beijing` 并推导出 Endpoint；两项不一致时以实际地域为准。

**高级配置**（一般不用动）：

+ **存储路径**：图片在 Bucket 里的目录前缀，如 `images/blog`，留空则传到根目录。
+ **自动按日期分目录**：默认开启，图片按 `2026/11/02/` 这样的日期目录归类，方便回源管理。
+ **公开访问域名**：私有 Bucket 必填；公共读 Bucket 留空即可，图片链接形如 `https://<bucket>.<endpoint>/<路径>`。

填写完毕后，点击右上角的「测试一下」，测试成功后点小对勾保存配置即可正常使用。如果测试失败，会弹出具体的错误信息，按提示检查参数（最常见的是 Bucket 名称带了地域后缀、地域与 Bucket 实际地域不一致、或 RAM 用户没有 OSS 权限）。

## 关于 PRO

阿里云 OSS 属于 PRO 图床：免费用户可以先试用上传 10 张（按成功上传次数累计），确认好用后再升级 PRO 不限量使用。上传记录的删除（本地 + 远端）不占额度，全免费。

## 其他

- PicPlus 下载地址：[去下载](/download)
- 阿里云 OSS 官方文档：[https://help.aliyun.com/product/31815.html](https://help.aliyun.com/product/31815.html)
