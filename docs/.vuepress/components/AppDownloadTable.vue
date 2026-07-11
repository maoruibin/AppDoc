<template>
  <div v-if="loading" class="app-download-loading">加载中…</div>
  <table v-else class="app-download-table">
    <thead>
      <tr>
        <th style="width:36px"></th>
        <th>应用</th>
        <th>简介</th>
        <th style="width:90px">下载</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="app in visibleApps" :key="app.package">
        <td>
          <img
            :src="resolveIcon(app.icon)"
            width="28"
            :alt="app.name"
            @error="onIconError"
          />
        </td>
        <td>
          <a :href="app.doc">{{ app.name }}</a>
        </td>
        <td>{{ app.desc }}</td>
        <td>
          <a :href="app.download" class="download-link">下载主页</a>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'AppDownloadTable',
  data() {
    return {
      apps: [],
      loading: true,
    }
  },
  computed: {
    visibleApps() {
      return this.apps
        .filter((a) => a.visible)
        .sort((a, b) => (a.sort || 999) - (b.sort || 999))
    },
  },
  async mounted() {
    try {
      const base = (typeof window !== 'undefined' && window.__VUEPRESS_BASE__) || '/'
      const res = await fetch((base || '/') + 'apps.json')
      this.apps = await res.json()
    } catch (e) {
      console.error('[AppDownloadTable] 加载 apps.json 失败', e)
    } finally {
      this.loading = false
    }
  },
  methods: {
    resolveIcon(icon) {
      if (!icon) return ''
      if (icon.startsWith('/')) {
        const base = (typeof window !== 'undefined' && window.__VUEPRESS_BASE__) || '/'
        return (base || '/') + icon.replace(/^\//, '')
      }
      return icon
    },
    onIconError(e) {
      e.target.style.display = 'none'
    },
  },
}
</script>

<style scoped>
.app-download-table {
  width: 100%;
  border-collapse: collapse;
}
.app-download-table th,
.app-download-table td {
  padding: 10px 8px;
  border-bottom: 1px solid var(--border-color, #eaecef);
  text-align: left;
  vertical-align: middle;
}
.app-download-table img {
  vertical-align: middle;
  border-radius: 6px;
}
.download-link {
  white-space: nowrap;
}
.app-download-loading {
  padding: 20px;
  color: #999;
}
</style>
