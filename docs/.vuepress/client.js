import { defineClientConfig } from '@vuepress/client'
import { watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'

const logoMap = {
  '/inbox/': 'https://gudong.s3.bitiful.net/icon/inbox_ic_launcher.png',
  '/light/': 'https://cdn.jsdelivr.net/gh/maoruibin/assets@master/2024/09/17/20240917112408747.png',
  '/cang/': 'https://gudong.s3.bitiful.net/icon/cang_launcher_icon.png?no-wait=on',
  '/rssplus/': 'https://gudong.s3.bitiful.net/icon/rss_ic_launcher.png',
  '/picplus/': 'https://gudong.s3.bitiful.net/icon/pic_ic_launcher.png',
}

const defaultLogo = 'https://gudong.s3.bitiful.net/asset/avatar.jpg'

function updateLogo(path) {
  // SSR 阶段没有 document,直接跳过,等客户端 hydration 后再执行
  if (typeof document === 'undefined') return

  const matched = Object.keys(logoMap).find((prefix) => path.startsWith(prefix))
  const logoUrl = matched ? logoMap[matched] : defaultLogo

  const img = document.querySelector('img.logo') || document.querySelector('.navbar-brand img')
  if (img) {
    img.src = logoUrl
  }
}

// ===== 访问统计 beacon（2026-11-03 收编进 gudong-api 统一 PV/UV 体系）=====
// 文档站无账号体系：localStorage 匿名 deviceId（格式与 inBoxWeb 一致，便于后端区分来源）。
// 每次路由变化（含首次进入）报一次 = +1 PV；同设备同天只记一次 UV（后端去重）。
// 走 /app/config 的 web 轻量分支，后端不查支付配置；失败静默，绝不影响页面。
const BEACON_API = 'https://api.gudong.site/app/config'
const BEACON_APPID = '1028' // 应用文档站（Apps 表专用 appid，勿复用）
const DEVICE_ID_KEY = 'gd_appdoc_device_id'

function getOrCreateDeviceId() {
  try {
    let deviceId = localStorage.getItem(DEVICE_ID_KEY)
    if (!deviceId) {
      deviceId = 'web_' + Date.now() + '_' + Math.random().toString(36).slice(2, 11)
      localStorage.setItem(DEVICE_ID_KEY, deviceId)
    }
    return deviceId
  } catch (_) {
    return 'web_anonymous'
  }
}

function reportVisit() {
  if (typeof window === 'undefined' || typeof fetch === 'undefined') return
  try {
    fetch(BEACON_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        appid: BEACON_APPID,
        from: 'web',
        deviceId: getOrCreateDeviceId(),
        email: '',
        requestVersion: '',
      }),
      keepalive: true,
    }).catch(() => {})
  } catch (_) { /* 统计失败不影响页面 */ }
}

export default defineClientConfig({
  setup() {
    const route = useRoute()

    watch(
      () => route.path,
      async (path) => {
        await nextTick()
        updateLogo(path)
        reportVisit()
      },
      { immediate: true }
    )
  },
})
