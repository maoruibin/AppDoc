# 配置 SM.MS 免费图床

## 写在前面

SM.MS（[https://sm.ms](https://sm.ms)）是一个老牌免费图床，注册即可使用，无需绑定信用卡或云账号。PicPlus 通过它的 API 上传，全程只需要一个 Token。

配置入口：图床管理 → 新增图床 → 选择「SM.MS / S.EE」。

> S.EE 是 SM.MS 的接口域名（同一家服务），App 会自动使用，无需额外配置。

## 获取 Token

1. 打开 [https://sm.ms](https://sm.ms)，注册并登录账号。
2. 进入个人中心的 API Token 页面：[https://sm.ms/home/apitoken](https://sm.ms/home/apitoken)
3. 页面上会显示一串 Token，复制后发送到手机备用。

## 在 App 中填写

SM.MS 只有一项配置：

| 表单项 | 填什么 |
|---|---|
| Token | 上一步复制的 API Token |

填写完毕后，点击右上角的「测试一下」，测试成功后点小对勾保存即可正常使用。

## 使用须知

+ 免费账户有总容量与单张图片大小限制，超出会在上传时提示，具体额度以 [SM.MS 官网说明](https://sm.ms) 为准。
+ SM.MS 属于**免费图床**，不占 PRO 名额，无需升级即可不限量使用。
+ 上传后的图片支持在图库中直接删除远端文件。

## 其他

- PicPlus 下载地址：[去下载](/download)
