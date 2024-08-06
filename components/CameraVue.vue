<template>
  <button class="btn btn-primary" @click="openCamera">
    <font-awesome-icon :icon=" ['fa','camera']" size="lg" class="fa-lg" />
  </button>
</template>
<script>
import { Camera, CameraResultType } from '@capacitor/camera'
export default {
  methods: {
    async openCamera () {
      this.$toast.info('Abrindo a camera')
      try {
        const image = await Camera.getPhoto({
          quality: 90,
          allowEditing: true,
          resultType: CameraResultType.DataUrl
        })
        this.$emit('picture', image.dataUrl)
      } catch (e) {
        this.$toast.error('Erro ao abrir a camera')
        this.$toast.error(e)
      }
    }
  }
}
</script>
