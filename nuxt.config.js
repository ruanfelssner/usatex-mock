export default {
  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Usatex',
    htmlAttrs: {
      lang: 'pt-BR'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/vue-cropper.js', ssr: false }
  ],

  ssr: false,

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    '@nuxtjs/fontawesome'
  ],
  modules: [
    '@nuxtjs/toast',
    'bootstrap-vue/nuxt',
    '@nuxtjs/pwa'
  ],
  fontawesome: {
    async: true,
    icons: {
      solid: ['faCamera', 'faRotateRight', 'faRotateLeft', 'faMagnifyingGlassPlus', 'faMagnifyingGlassMinus']
    }
  },

  toast: {
    position: 'bottom-center',
    duration: 2000
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    vendor: [
      'vue-cropperjs'
    ]
  },
  pwa: {
    manifest: {
      name: 'USATEX',
      short_name: 'Usatex',
      description: 'Gerenciador de Mockups e Estampas',
      lang: 'pt-BR'
    },
    meta: {
      theme_color: '#ffffff' // Cor do tema do seu PWA
    }
  }
}
