<template>
  <button
    class="flex items-center justify-center w-10 h-10 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105 active:scale-95"
    title="Abrir Câmera"
    @click="openCamera"
  >
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.414-1.414A1 1 0 0012.586 3H7.414a1 1 0 00-.707.293L5.293 4.707A1 1 0 014.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
    </svg>
  </button>
</template>

<script>
import { Camera, CameraResultType } from '@capacitor/camera'

export default {
  name: 'CameraVue',
  methods: {
    async openCamera () {
      try {
        if (this.$toast) {
          this.$toast.info('Abrindo a câmera...')
        }

        const image = await Camera.getPhoto({
          quality: 90,
          allowEditing: true,
          resultType: CameraResultType.DataUrl
        })

        this.$emit('picture', image.dataUrl)

        if (this.$toast) {
          this.$toast.success('Foto capturada com sucesso!')
        }
      } catch (error) {
        console.error('Erro ao abrir a câmera:', error)

        if (this.$toast) {
          this.$toast.error('Erro ao abrir a câmera')
        }
      }
    }
  }
}
</script>

<style scoped>
button:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.5);
}

@media (max-width: 640px) {
  button {
    padding: 0.75rem;
  }
}
</style>
