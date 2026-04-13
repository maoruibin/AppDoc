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

const defaultLogo = '/img/gudong-doc-logo.svg'

function updateLogo(path) {
  const matched = Object.keys(logoMap).find((prefix) => path.startsWith(prefix))
  const logoUrl = matched ? logoMap[matched] : defaultLogo

  const img = document.querySelector('img.logo') || document.querySelector('.navbar-brand img')
  if (img) {
    img.src = logoUrl
  }
}

export default defineClientConfig({
  setup() {
    const route = useRoute()

    watch(
      () => route.path,
      async (path) => {
        await nextTick()
        updateLogo(path)
      },
      { immediate: true }
    )
  },
})
