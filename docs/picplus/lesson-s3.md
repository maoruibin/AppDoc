# 配置 S3 兼容存储为个人图床

## 写在前面

PicPlus 支持所有 **S3 兼容协议**的对象存储作为图床，包括不限于：

+ AWS S3
+ Cloudflare R2
+ Bitiful
+ MinIO（自建）
+ 其他任何 S3 兼容对象存储

阿里云 OSS 和腾讯云 COS 也走同一协议，但 App 内有专门入口和[专属教程](/picplus/lesson-oss.html)，本文只讲通用 S3 接入。

配置入口：图床管理 → 新增图床 → 选择「S3」。

## 配置需要的参数

+ Access Key（访问密钥 ID）
+ Access Secret（访问密钥密码）
+ Endpoint（接口域名）
+ Bucket（存储桶名称）
+ Region（地域）

各家厂商的参数获取方式见下方速查表。

## 各厂商参数速查

| 厂商 | Endpoint | Region | Access Key 获取 |
|---|---|---|---|
| AWS S3 | `s3.<region>.amazonaws.com`，如 `s3.ap-northeast-1.amazonaws.com` | 桶所在地域，如 `ap-northeast-1` | 控制台 → IAM → 创建 AccessKey（建议只授予该桶的读写权限） |
| Cloudflare R2 | `<账户ID>.r2.cloudflarestorage.com`（控制台 R2 概览页可复制） | 填 `auto` | R2 概览 → 管理 API 令牌 → 创建（得到 Access Key ID 和 Secret） |
| Bitiful | `s3.bitiful.net` | 以控制台存储桶所在区域为准 | 控制台 → API Key（类型选 S3 兼容） |
| MinIO 自建 | 你的服务地址，如 `http://minio.example.com:9000` | 按服务端配置，常见 `us-east-1` | MinIO 控制台 → Access Keys → 创建 |

> Bucket 都在各家控制台先创建好。做图床的桶需要能公开读，或绑定公开访问域名（见下文高级配置）。

## 在 App 中填写

| 表单项 | 填什么 | 示例 |
|---|---|---|
| Access Key | 服务商给的 Access Key ID | — |
| Access Secret | 对应的 Secret | — |
| Endpoint | 接口域名（不带桶名） | `s3.bitiful.net` |
| Bucket | 桶名 | `my-bucket` |
| Region | 地域，不确定就按速查表 | `us-east-1` / `auto` |

**高级配置**（一般不用动）：

+ **存储路径**：图片在桶里的目录前缀，如 `images/blog`，留空则传到根目录。
+ **公开访问域名**：桶是私有读或需要走 CDN 时必填。Cloudflare R2 需要先在控制台绑定自定义域名（或开启 r2.dev 子域）再填到这里；公共读的桶留空即可。
+ **自动按日期分目录**：默认开启，图片按 `2026/11/02/` 这样的日期目录归类。

填写完毕后，点击右上角的「测试一下」，测试成功后点小对勾保存配置即可正常使用。测试失败时按弹窗提示检查，最常见的原因是 Endpoint 写成了带桶名的完整地址、Region 与桶实际地域不符、或该密钥没有这个桶的读写权限。

## 关于 PRO

S3 属于 PRO 图床：免费用户可以先试用上传 10 张（按成功上传次数累计），确认好用后再升级 PRO 不限量使用。上传记录的删除（本地 + 远端）不占额度，全免费。

## 其他

- PicPlus 下载地址：[去下载](/download)
