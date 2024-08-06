<template>
  <div class="crop">
    <div class="row mt-3 mb-4 justify-content-center align-items-center">
      <div class="col-12 col-md-auto mb-3 mb-lg-0">
        <input
          id="customRange1"
          v-model="size"
          type="range"
          class="form-range w-100"
          step="1"
          min="0"
          max="150"
          @change="onSize"
        >
      </div>
      <div class="col-12 col-md-auto">
        <div class="w-100 d-inline-flex justify-content-between">
          <button class="btn btn-primary mr-lg-2" @click="zoom(0.2)">
            <font-awesome-icon :icon="['fas', 'magnifying-glass-plus']" size="lg" class="fa-lg" />
          </button>

          <button class="btn btn-primary mr-lg-2" @click="zoom(-0.2)">
            <font-awesome-icon :icon="['fas', 'magnifying-glass-minus']" size="lg" class="fa-lg" />
          </button>
          <button class="btn btn-primary mr-lg-2" @click="rotate(15)">
            <font-awesome-icon :icon="['fas', 'rotate-right']" size="lg" class="fa-lg" />
          </button>

          <button class="btn btn-primary mr-lg-2" @click="rotate(-15)">
            <font-awesome-icon :icon="['fas', 'rotate-left']" size="lg" class="fa-lg" />
          </button>

          <CameraVue v-if="showCameraButton" @picture="cameraPhoto" />
        </div>
      </div>
    </div>
    <VueCropper
      ref="cropper"
      :src="imgOrigin"
      :view-mode="3"
      :zoomable="true"
      :auto-crop="true"
      :auto-crop-area="true"
      :initial-aspect-ratio="(1, 0)"
      @ready="cropEvent"
      @cropend="cropEvent"
      @zoom="cropEvent"
    />
  </div>
</template>
<script>
export default {
  props: {
    img: {
      type: String,
      required: true
    },
    showCameraButton: {
      type: Boolean
    }
  },
  data () {
    return {
      imgOrigin: '',
      size: 50
    }
  },
  watch: {
    img (val) {
      this.$refs.cropper.replace(val)
      this.imgOrigin = val
    }
  },
  mounted () {
    this.$refs.cropper.replace(this.img)
    this.imgOrigin = this.img
  },
  methods: {
    cropEvent () {
      this.$emit('crop', this.$refs.cropper.getCroppedCanvas().toDataURL())
    },
    zoom (percent) {
      this.$refs.cropper.relativeZoom(percent)
    },
    rotate (deg) {
      this.$refs.cropper.rotate(deg)
      this.cropEvent()
    },
    cameraPhoto (photo) {
      this.$refs.cropper.replace(photo)
      this.imgOrigin = photo
      this.$emit('camera', photo)
    },
    onSize () {
      this.$emit('size', this.size)
    }
  }
}
</script>
<style>
.crop {
  width: 100%;
  height: 100%;
  max-height:100%;
  margin-bottom:-2px;
}
.preview {
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 50%;
  margin: 10px;
  border: 1px solid #ccc;
}
</style>
