# 技术设计文档：自定义水印功能（最终版）

> 版本：v2.0 | 日期：2026-04-16 | 状态：待开发

---

## 一、现有流程分析

### 1.1 上传流程

```
选图(相册/拍照/分享) → 解析路径 → 构建 UploadInfo
  → uploadCheck(权限/重复检查)
  → prepareUpload(确认弹窗 ConfirmView)
  → startUpload → [压缩? → PicServerUtils.compressFile]
  → 上传到图床
```

关键代码路径：
- `ImageSharePresenter` — 上传总调度
- `ImageSharePresenter.prepareUpload()` — 确认弹窗（`ConfirmView`）
- `ImageSharePresenter.startUpload()` — 触发上传
- `PicServerUtils.compressFile()` — 压缩处理（在 `startUpload` 内调用）

### 1.2 水印插入点

**插入点：`startUpload` → 压缩之前**

```
startUpload()
  → [水印开关?] → WatermarkProcessor.apply() → 生成带水印文件
  → [压缩开关?] → PicServerUtils.compressFile()
  → 上传
```

理由：
1. 水印作用于原图，压缩作用于水印后的图（保证水印清晰）
2. 不侵入 `UploadInfo` 数据结构，只修改文件路径
3. 不影响 `ConfirmView` 预览（确认弹窗展示原图，上传时才加水印）

### 1.3 现有 PRO 限制模式

| 限制点 | 免费用户 | PRO 用户 |
|--------|----------|----------|
| 图床类型 | 仅免费图床 | 全部图床 |
| 多图上传 | 不支持 | 支持 |
| 视频上传 | 不支持 | 支持 |
| 免费图床数量 | 有上限 | 无限制 |

判断方式：`AccountCenter.getInstance().isPayUserV2()` / `PicUtils.isPayUser()`

---

## 二、PRO 分层设计

**原则：基础水印免费可用，进阶自定义 PRO 解锁。**

让免费用户先用上基础水印 → 产生依赖 → 遇到进阶需求自然升级。

| 功能 | 免费用户 | PRO 用户 |
|------|----------|----------|
| 水印开关 | ✅ | ✅ |
| 文字水印 | ✅ | ✅ |
| 透明度调节 | ✅ | ✅ |
| 描边 | ✅ | ✅ |
| 水印位置 | ✅ 仅右下角 | ✅ 九宫格全部 9 位 |
| 字体大小 | ✅ 仅中号 | ✅ 小/中/大三档 |
| 字体颜色 | ✅ 仅白色 | ✅ 白/黑/自定义 |
| 图片水印（Logo） | ❌ | ✅ |

### PRO 限制实现

在两个层面限制，简单可靠：

**1. UI 层 — WatermarkSettingActivity**

```kotlin
val isPro = AccountCenter.getInstance().isPayUserV2()

// 九宫格：非 PRO 只能选右下角，其他位置显示锁图标
// 点击锁定位置 → 弹窗 "升级 PRO 解锁全部位置" → PayActivity.start()

// 字体大小：非 PRO 强制选中号，其他两项灰显 + 锁

// 字体颜色：非 PRO 强制白色，其他选项灰显 + 锁

// 图片水印 Tab：非 PRO 整块灰显 + "PRO" 标签
```

**2. 处理层 — WatermarkProcessor.apply()**

```kotlin
// 双重保险：即使 UI 层被绕过，处理层也强制降级
val isPro = AccountCenter.getInstance().isPayUserV2()

val position = if (isPro) config.position else Position.BOTTOM_RIGHT
val textSize = if (isPro) config.textSize else TextSize.MEDIUM
val textColor = if (isPro) config.textColor else Color.WHITE
val type = if (isPro) config.type else Type.TEXT  // 图片水印需 PRO
```

---

## 三、方案设计

### 3.1 入口

在主设置页「上传设置」分类下新增「水印设置」入口：

```
上传设置 (PreferenceCategory)
├── 上传确认开关      ← 已有
├── 压缩质量          ← 已有
├── 时间戳重命名      ← 已有
├── 水印设置 →        ← 新增
```

### 3.2 文件变更清单

#### 新增 4 个文件

| 文件 | 说明 |
|------|------|
| `arch/base/.../watermark/WatermarkConfig.kt` | 水印配置数据类 |
| `arch/base/.../watermark/WatermarkProcessor.kt` | 水印绘制核心 |
| `app/.../activity/WatermarkSettingActivity.kt` | 水印配置页 |
| `app/.../res/layout/activity_watermark_setting.xml` | 配置页布局 |

#### 修改 3 个文件

| 文件 | 改动 |
|------|------|
| `app/.../res/xml/app_settings_main.xml` | 新增水印设置入口 |
| `app/.../activity/SettingsActivity.kt` | 绑定入口点击事件 |
| `app/.../present/ImageSharePresenter.kt` | startUpload 插入水印处理 |

---

## 四、核心设计

### 4.1 WatermarkConfig

```kotlin
// arch/base/src/main/java/name/gudong/base/watermark/WatermarkConfig.kt
package name.gudong.base.watermark

import android.graphics.Color

data class WatermarkConfig(
    val enabled: Boolean = false,
    val type: Type = Type.TEXT,
    val text: String = "",
    val textSize: TextSize = TextSize.MEDIUM,
    val textColor: Int = Color.WHITE,
    val strokeEnabled: Boolean = true,
    val imageUri: String = "",
    val imageScale: Float = 0.2f,
    val position: Position = Position.BOTTOM_RIGHT,
    val opacity: Int = 50
) {
    enum class Type { TEXT, IMAGE }
    enum class TextSize { SMALL, MEDIUM, LARGE }
    enum class Position {
        TOP_LEFT, TOP_CENTER, TOP_RIGHT,
        MIDDLE_LEFT, MIDDLE_CENTER, MIDDLE_RIGHT,
        BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT
    }

    /**
     * 非 PRO 用户强制降级配置
     */
    fun applyProLimit(isPro: Boolean): WatermarkConfig {
        if (isPro) return this
        return copy(
            type = Type.TEXT,
            position = Position.BOTTOM_RIGHT,
            textSize = TextSize.MEDIUM,
            textColor = Color.WHITE
        )
    }
}
```

### 4.2 WatermarkProcessor

```kotlin
// arch/base/src/main/java/name/gudong/base/watermark/WatermarkProcessor.kt
package name.gudong.base.watermark

import android.content.Context
import android.graphics.*
import androidx.exifinterface.media.ExifInterface
import name.gudong.account.AccountCenter
import java.io.File
import java.io.FileOutputStream

object WatermarkProcessor {

    fun apply(context: Context, originPath: String, config: WatermarkConfig): String {
        if (!config.enabled) return originPath

        // PRO 降级：双重保险
        val safeConfig = config.applyProLimit(AccountCenter.getInstance().isPayUserV2())

        return try {
            val originFile = File(originPath)
            val bitmap = decodeSampledBitmap(originPath, 4096, 4096) ?: return originPath

            val result = Bitmap.createBitmap(bitmap.width, bitmap.height, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(result)
            canvas.drawBitmap(bitmap, 0f, 0f, null)

            val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                alpha = (safeConfig.opacity / 100f * 255).toInt()
            }

            when (safeConfig.type) {
                WatermarkConfig.Type.TEXT ->
                    drawTextWatermark(canvas, safeConfig, paint, bitmap.width, bitmap.height)
                WatermarkConfig.Type.IMAGE ->
                    drawImageWatermark(context, canvas, safeConfig, paint, bitmap.width, bitmap.height)
            }

            val outputFile = File(context.cacheDir, "wm_${originFile.name}")
            FileOutputStream(outputFile).use { fos ->
                val fmt = if (originPath.endsWith(".png", true))
                    Bitmap.CompressFormat.PNG else Bitmap.CompressFormat.JPEG
                result.compress(fmt, 95, fos)
            }

            copyExif(originPath, outputFile.path)

            bitmap.recycle()
            result.recycle()
            outputFile.path
        } catch (e: Exception) {
            originPath
        }
    }

    private fun drawTextWatermark(
        canvas: Canvas, config: WatermarkConfig, paint: Paint, w: Int, h: Int
    ) {
        val sp = when (config.textSize) {
            WatermarkConfig.TextSize.SMALL -> 14f
            WatermarkConfig.TextSize.MEDIUM -> 18f
            WatermarkConfig.TextSize.LARGE -> 24f
        }
        val px = sp * canvas.density

        paint.textSize = px
        paint.color = config.textColor

        val textWidth = paint.measureText(config.text)
        val (x, y) = calcPosition(config.position, w, h, textWidth, px, 24f * canvas.density)

        if (config.strokeEnabled) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 2f * canvas.density / 2
            paint.color = if (config.textColor == Color.WHITE) Color.BLACK else Color.WHITE
            canvas.drawText(config.text, x, y, paint)

            paint.style = Paint.Style.FILL
            paint.color = config.textColor
        }
        canvas.drawText(config.text, x, y, paint)
    }

    private fun drawImageWatermark(
        context: Context, canvas: Canvas, config: WatermarkConfig,
        paint: Paint, w: Int, h: Int
    ) {
        if (config.imageUri.isEmpty()) return
        val wmBitmap = BitmapFactory.decodeFile(config.imageUri) ?: return
        val scale = config.imageScale
        val shortSide = minOf(w, h)
        val scaledW = (shortSide * scale).toInt()
        val scaledH = (wmBitmap.height * scaledW.toFloat() / wmBitmap.width).toInt()
        val scaled = Bitmap.createScaledBitmap(wmBitmap, scaledW, scaledH, true)

        val (x, y) = calcPosition(config.position, w, h, scaledW.toFloat(), scaledH.toFloat(), 24f * canvas.density)
        canvas.drawBitmap(scaled, x, y, paint)

        wmBitmap.recycle()
        scaled.recycle()
    }

    /**
     * 九宫格坐标，padding 为短边的 2%
     */
    private fun calcPosition(
        pos: WatermarkConfig.Position, imgW: Int, imgH: Int,
        wmW: Float, wmH: Float, padding: Float
    ): Pair<Float, Float> {
        val pad = padding
        return when (pos) {
            WatermarkConfig.Position.TOP_LEFT     -> pad to (wmH + pad)
            WatermarkConfig.Position.TOP_CENTER   -> (imgW - wmW) / 2 to (wmH + pad)
            WatermarkConfig.Position.TOP_RIGHT    -> (imgW - wmW - pad) to (wmH + pad)
            WatermarkConfig.Position.MIDDLE_LEFT  -> pad to (imgH + wmH) / 2
            WatermarkConfig.Position.MIDDLE_CENTER-> (imgW - wmW) / 2 to (imgH + wmH) / 2
            WatermarkConfig.Position.MIDDLE_RIGHT -> (imgW - wmW - pad) to (imgH + wmH) / 2
            WatermarkConfig.Position.BOTTOM_LEFT  -> pad to (imgH - pad)
            WatermarkConfig.Position.BOTTOM_CENTER-> (imgW - wmW) / 2 to (imgH - pad)
            WatermarkConfig.Position.BOTTOM_RIGHT -> (imgW - wmW - pad) to (imgH - pad)
        }
    }

    private fun decodeSampledBitmap(path: String, maxW: Int, maxH: Int): Bitmap? {
        val options = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeFile(path, options)
        options.inSampleSize = calculateInSampleSize(options, maxW, maxH)
        options.inJustDecodeBounds = false
        return BitmapFactory.decodeFile(path, options)
    }

    private fun calculateInSampleSize(options: BitmapFactory.Options, reqW: Int, reqH: Int): Int {
        val (h, w) = options.outHeight to options.outWidth
        var inSampleSize = 1
        if (h > reqH || w > reqW) {
            val halfH = h / 2
            val halfW = w / 2
            while (halfH / inSampleSize >= reqH && halfW / inSampleSize >= reqW) {
                inSampleSize *= 2
            }
        }
        return inSampleSize
    }

    private fun copyExif(srcPath: String, dstPath: String) {
        try {
            val src = ExifInterface(srcPath)
            val dst = ExifInterface(dstPath)
            val tags = arrayOf(
                ExifInterface.TAG_ORIENTATION,
                ExifInterface.TAG_DATETIME,
                ExifInterface.TAG_MAKE,
                ExifInterface.TAG_MODEL
            )
            tags.forEach { tag ->
                src.getAttribute(tag)?.let { dst.setAttribute(tag, it) }
            }
            dst.saveAttributes()
        } catch (e: Exception) { /* 部分格式不支持 EXIF，忽略 */ }
    }
}
```

### 4.3 上传流程集成

`ImageSharePresenter.kt` 的 `startUpload` 方法：

```kotlin
fun startUpload(uploadList: ArrayList<UploadInfo>) {
    GlobalScope.launch(Dispatchers.IO) {
        // ★ 水印处理
        val wmConfig = WatermarkSettings().getConfig()
        if (wmConfig.enabled) {
            uploadList.forEach { info ->
                // GIF 跳过水印
                if (info.isGif) return@forEach
                val wmPath = WatermarkProcessor.apply(mActivity, info.originPath, wmConfig)
                if (wmPath != info.originPath) {
                    info.originPath = wmPath
                    info.deleteOriginFile = true
                }
            }
        }

        // 原有逻辑不变
        GlobalScope.launch(Dispatchers.Main) {
            if (uploadList.isNotEmpty() && uploadList[0].server == PicServer.S3) {
                startUploadS3(uploadList)
            } else {
                // ... 原有 UploadManager 逻辑
            }
        }
    }
}
```

### 4.4 设置页入口

**app_settings_main.xml** — 在「上传设置」分类的 `key_open_rename_time` 后新增：

```xml
<Preference
    android:key="settingWatermark"
    android:title="@string/title_watermark_setting"
    android:summary="@string/title_watermark_setting_summary" />
```

**SettingsActivity.kt** — `onCreateSetting()` 新增：

```kotlin
findPreference("settingWatermark")!!.setOnPreferenceClickListener {
    startActivity(Intent(activity, WatermarkSettingActivity::class.java))
    true
}
```

### 4.5 WatermarkSettingActivity

独立 Activity（非 Preference Fragment），支持实时预览。

```
┌─────────────────────────────────┐
│  ← 水印设置                      │
├─────────────────────────────────┤
│  [开关] 启用水印                  │
├─────────────────────────────────┤
│  ┌───────────────────────┐      │
│  │                       │      │
│  │    预览图片            │      │
│  │            @咕咚 ©    │      │
│  └───────────────────────┘      │
├─────────────────────────────────┤
│  水印文字                        │
│  [输入水印文字...]               │
├─────────────────────────────────┤
│  水印位置                        │
│  ┌───┬───┬───┐                  │
│  │🔒 │🔒 │🔒 │  ← PRO 锁       │
│  ├───┼───┼───┤                  │
│  │🔒 │🔒 │🔒 │                  │
│  ├───┼───┼───┤                  │
│  │🔒 │🔒 │ ● │  ← 免费：仅右下  │
│  └───┴───┴───┘                  │
├─────────────────────────────────┤
│  透明度                          │
│  ●────────────○ 50%             │
├─────────────────────────────────┤
│  字体大小                        │
│  [🔒小] [ 中● ] [🔒大]          │
├─────────────────────────────────┤
│  字体颜色                        │
│  [●白] [🔒黑] [🔒自定义]         │
├─────────────────────────────────┤
│  描边                            │
│  [开关]                          │
├─────────────────────────────────┤
│  图片水印                    PRO │
│  [灰色遮罩 - 升级 PRO 解锁]      │
└─────────────────────────────────┘
```

点击 PRO 锁定项的统一弹窗逻辑：

```kotlin
private fun showProTip() {
    XDialog.XBuilder(this)
        .title("PRO 功能")
        .message("升级 PRO 解锁全部水印自定义能力")
        .positive("升级 PRO") { _, _ -> PayActivity.start(this) }
        .negativeKnow()
        .show()
}
```

---

## 五、配置存储

在 `CommonSettings` 中新增，复用现有 SP 模式：

```kotlin
// CommonSettings.kt 新增
companion object {
    const val keyWmEnabled = "keyWmEnabled"
    const val keyWmText = "keyWmText"
    const val keyWmTextSize = "keyWmTextSize"       // SMALL/MEDIUM/LARGE
    const val keyWmTextColor = "keyWmTextColor"
    const val keyWmStroke = "keyWmStroke"
    const val keyWmPosition = "keyWmPosition"        // 枚举名
    const val keyWmOpacity = "keyWmOpacity"           // 10~100
    const val keyWmType = "keyWmType"                 // TEXT/IMAGE
    const val keyWmImageUri = "keyWmImageUri"
    const val keyWmImageScale = "keyWmImageScale"
}

fun getWatermarkConfig(): WatermarkConfig = WatermarkConfig(
    enabled = getBoolean(keyWmEnabled, false),
    text = getString(keyWmText, ""),
    textSize = WatermarkConfig.TextSize.valueOf(getString(keyWmTextSize, "MEDIUM")),
    textColor = getInt(keyWmTextColor, Color.WHITE),
    strokeEnabled = getBoolean(keyWmStroke, true),
    position = WatermarkConfig.Position.valueOf(getString(keyWmPosition, "BOTTOM_RIGHT")),
    opacity = getInt(keyWmOpacity, 50),
    type = WatermarkConfig.Type.valueOf(getString(keyWmType, "TEXT")),
    imageUri = getString(keyWmImageUri, ""),
    imageScale = getFloat(keyWmImageScale, 0.2f)
)
```

---

## 六、数据流

```
┌─────────────────────────────────────────────────────┐
│              WatermarkSettingActivity                │
│  用户配置 → CommonSettings (SP存储)                   │
│  PRO 检查 → 非 PRO 项灰显 + 锁                       │
└─────────────────────────────────────────────────────┘
                            ↓ 读取
┌─────────────────────────────────────────────────────┐
│          ImageSharePresenter.startUpload             │
│  getWatermarkConfig()                                │
│  → config.applyProLimit(isPro)   ← 处理层兜底        │
│  → WatermarkProcessor.apply(path, config)            │
│  → GIF 跳过                                         │
│  → 输出到 cacheDir/wm_xxx.jpg                        │
│  → UploadInfo.originPath 指向新文件                   │
└─────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────┐
│              原有压缩 + 上传流程                       │
│  PicServerUtils.compressFile() → 上传                │
│  完成后 deleteTempFile() 清理缓存                     │
└─────────────────────────────────────────────────────┘
```

---

## 七、实现步骤

| # | 步骤 | 文件 |
|---|------|------|
| 1 | 新增 `WatermarkConfig` 数据类（含 `applyProLimit`） | `arch/base/watermark/WatermarkConfig.kt` |
| 2 | 新增 `WatermarkProcessor` 绘制核心 | `arch/base/watermark/WatermarkProcessor.kt` |
| 3 | `CommonSettings` 新增配置读写 + `getWatermarkConfig()` | `app/.../settings/CommonSettings.kt` |
| 4 | 新增 strings 资源 | `app/.../res/values/strings.xml` |
| 5 | 设置页新增入口 | `app_settings_main.xml` + `SettingsActivity.kt` |
| 6 | 新增 `WatermarkSettingActivity` + layout | `app/.../activity/WatermarkSettingActivity.kt` |
| 7 | `startUpload` 集成水印处理 | `ImageSharePresenter.kt` |
| 8 | 测试 | |

---

## 八、风险

| 风险 | 应对 |
|------|------|
| 大图 OOM | `decodeSampledBitmap` 限制 4096px |
| EXIF 丢失 | `ExifInterface` 拷贝 orientation 等 |
| GIF 跳过 | `UploadInfo.isGif` 判断 |
| 批量性能 | IO 线程逐张处理 |
| 临时文件 | 复用 `deleteTempFile()` |
| PRO 绕过 | UI 层 + 处理层双重 `applyProLimit` |
