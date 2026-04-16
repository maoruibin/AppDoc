import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'
import { webpackBundler } from '@vuepress/bundler-webpack'
import taskLists from 'markdown-it-task-lists'

export default defineUserConfig({
  lang: 'zh-CN',
  title: '咕咚',
  description: '软件使用说明文档',
  head: [
    ['link', { rel: 'icon', href: '/img/favicon-32.png' }]
  ],
  markdown: {
    extendsMarkdown: (md) => {
      md.use(taskLists)
    }
  },
  theme: defaultTheme({
    logo: '/img/gudong-doc-logo.svg',
    navbar: [
      { text: '首页', link: '/' },
      { text: '知识卡片', link: 'https://card.gudong.site/' },
      { text: '下载地址', link: '/inbox/download' },
      {
        text: '作品集合',
        children: [
          { text: 'inBox 笔记', link: '/inbox/' },
          { text: '仓咚咚', link: '/cang/' },
          { text: '点亮', link: '/light/' },
          { text: '咕咚订阅', link: '/rssplus/' },
          { text: '咕咚云图', link: '/picplus/' }
        ]
      },
      {
        text: '更多',
        children: [
          { text: '联系我们', link: '/inbox/contact' },
          { text: '购买 PRO', link: '/inbox/pay' },
          { text: '我的博客', link: 'https://blog.gudong.site/' }
        ]
      }
    ],
    sidebar: {
      '/inbox/': [
        { text: '你好', collapsible: false, children: [
          { text: '常见问题', link: '/inbox/qa', children: [] },
          { text: '使用指南', link: '/inbox/guide', children: [] },
          { text: '更新日志', link: '/inbox/changelog', children: [] },
          { text: '开发计划', link: '/inbox/dev_plan', children: [] },
          { text: '购买 PRO', link: '/inbox/pay', children: [] },
          { text: '捐赠', link: '/inbox/donate', children: [] }
        ]},
        { text: '数据', collapsible: false, children: [
          { text: '数据备份', link: '/inbox/data_backup', children: [] },
          { text: '数据存储与同步', link: '/inbox/data_storage_guide', children: [] },
          { text: '图片选择', link: '/inbox/image_select', children: [] },
          { text: '历史记录', link: '/inbox/history', children: [] }
        ]},
  
        { text: '功能', collapsible: false, children: [
          { text: 'Markdown', link: '/inbox/markdown', children: [] },
          { text: '快速操作', link: '/inbox/quick', children: [] },
          { text: '标签', link: '/inbox/tag', children: [] },
          { text: '盒子', link: '/inbox/box', children: [] },
          { text: '时间笔记', link: '/inbox/time_note', children: [] },
          { text: '热力图', link: '/inbox/heatmap', children: [] },
          { text: '链接', link: '/inbox/link', children: [] },
          { text: '图片服务', link: '/inbox/image_server', children: [] }
        ]},
        { text: '开放', collapsible: false, children: [
          { text: 'Kimi 接入', link: '/inbox/ai_kimi', children: [] },
          { text: 'DeepSeek', link: '/inbox/deepseek', children: [] },
          { text: 'Web S3 教程', link: '/inbox/lesson-web-s3', children: [] },
          { text: 'S3 存储配置问题排查指南', link: '/inbox/s3-issue', children: [] },
          { text: 'Memos', link: '/inbox/memos', children: [] },
          { text: '思源', link: '/inbox/siyuan', children: [] },
          { text: 'API', link: '/inbox/api', children: [] },
          
          { text: 'Scheme', link: '/inbox/scheme', children: [] }
        ]},
        { text: '教程', collapsible: false, children: [
          { text: 'Web S3 教程', link: '/inbox/lesson-web-s3', children: [] },
          { text: '导出到 Obsidian', link: '/inbox/export_obsidian', children: [] },
          { text: '导出到思源', link: '/inbox/export_siyuan', children: [] },
          { text: '数据恢复', link: '/inbox/data_recovery', children: [] },
          { text: '导入数据', link: '/inbox/lesson-import', children: [] },
          { text: '时间笔记教程', link: '/inbox/lesson-timenote', children: [] },
          { text: 'WebDAV 教程', link: '/inbox/lesson-webdav', children: [] },
          { text: '数据推送', link: '/inbox/data_push', children: [] }
        ]},
        { text: '关于', collapsible: false, children: [
          { text: '缘起', link: '/inbox/reason', children: [] },
          { text: '下载地址', link: '/inbox/download', children: [] },
          { text: '更新日志', link: '/inbox/changelog', children: [] },
          { text: '联系我们', link: '/inbox/contact', children: [] }
        ]},
        { text: '服务协议', collapsible: false, children: [
          { text: '服务协议', link: '/inbox/agreement', children: [] },
          { text: '隐私政策', link: '/inbox/private', children: [] }
        ]}
      ],
      '/cang/': [
        { text: '你好', collapsible: false, children: [
          { text: '常见问题', link: '/cang/qa', children: [] },
          { text: '使用指南', link: '/cang/guide', children: [] },
          { text: '更新日志', link: '/cang/changelog', children: [] }
        ]},
        { text: '使用场景', collapsible: false, children: [
          { text: '使用场景', link: '/cang/usage_scenarios', children: [] },
          { text: '专业版', link: '/cang/pro_version', children: [] }
        ]},
        { text: '数据', collapsible: false, children: [
          { text: '数据安全', link: '/cang/data_security', children: [] }
        ]},
        { text: '服务协议', collapsible: false, children: [
          { text: '服务协议', link: '/cang/agreement', children: [] },
          { text: '隐私政策', link: '/cang/privacy', children: [] }
        ]}
      ],
      '/light/': [
        { text: '你好', collapsible: false, children: [
          { text: '介绍', link: '/light/', children: [] },
          { text: '常见问题', link: '/light/qa', children: [] },
          { text: '愿望清单', link: '/light/wish', children: [] }
        ]},
        { text: '打卡', collapsible: false, children: [
          { text: '打卡记录', link: '/light/note', children: [] },
          { text: '开放接口', link: '/light/api', children: [] }
        ]},
        { text: '数据', collapsible: false, children: [
          { text: '数据备份', link: '/light/data_backup', children: [] },
          { text: '数据恢复', link: '/light/data_recovery', children: [] },
          { text: 'WebDAV 云盘', link: '/light/data_webdav', children: [] }
        ]},
        { text: '教程', collapsible: false, children: [
          { text: 'WebDAV 教程', link: '/light/lesson-webdav', children: [] }
        ]},
        { text: '服务协议', collapsible: false, children: [
          { text: '隐私政策', link: '/light/private', children: [] },
          { text: '用户协议', link: '/light/agreement', children: [] }
        ]},
        { text: '关于', collapsible: false, children: [
          { text: '为什么', link: '/light/why', children: [] },
          { text: '更新日志', link: '/light/changelog', children: [] },
          { text: '联系我们', link: '/light/contact', children: [] }
        ]}
      ],
      '/rssplus/': [
        { text: '你好', collapsible: false, children: [
          { text: '常见问题', link: '/rssplus/qa', children: [] }
        ]},
        { text: '服务协议', collapsible: false, children: [
          { text: '服务协议', link: '/rssplus/agreement', children: [] },
          { text: '隐私政策', link: '/rssplus/private', children: [] }
        ]},
        { text: '关于', collapsible: false, children: [
          { text: '什么是 RSS', link: '/rssplus/whatrss', children: [] },
          { text: '更新日志', link: '/rssplus/changelog', children: [] }
        ]}
      ],
      '/picplus/': [
        { text: '你好', collapsible: false, children: [
          { text: '介绍', link: '/picplus/', children: [] },
          { text: '常见问题', link: '/picplus/qa', children: [] },
          { text: '更新日志', link: '/picplus/changelog', children: [] }
        ]},
        { text: '教程', collapsible: false, children: [
          { text: 'WebDAV 教程', link: '/picplus/lesson_webdav', children: [] },
          { text: 'GitHub 教程', link: '/picplus/lesson_github', children: [] },
          { text: '七牛云教程', link: '/picplus/lesson_qiniu', children: [] },
          { text: '腾讯云教程', link: '/picplus/lesson_tenxun', children: [] },
          { text: 'Lsky 教程', link: '/picplus/lesson-lsky', children: [] }
        ]},
        { text: '使用', collapsible: false, children: [
          { text: 'WebDAV 使用', link: '/picplus/webdav', children: [] },
          { text: '推荐配置', link: '/picplus/recommend', children: [] },
          { text: '使用方式', link: '/picplus/way', children: [] }
        ]},
        { text: '服务协议', collapsible: false, children: [
          { text: '隐私政策', link: '/picplus/private', children: [] },
          { text: '服务协议', link: '/picplus/agreement', children: [] }
        ]},
        { text: '关于', collapsible: false, children: [
          { text: '为什么', link: '/picplus/why', children: [] },
          { text: '关于', link: '/picplus/about', children: [] }
        ]}
      ]
    }
  }),
  bundler: webpackBundler({
    chainWebpack: (config) => {
      ['scss', 'sass'].forEach((ruleName) => {
        const rule = config.module.rule(ruleName)
        if (rule) {
          const use = rule.use('sass-loader')
          if (use) {
            use.tap((opts) => {
              opts = opts || {}
              opts.sassOptions = Object.assign({}, opts.sassOptions, {
                silenceDeprecations: ['legacy-js-api']
              })
              return opts
            })
          }
        }
      })
    }
  })
})
