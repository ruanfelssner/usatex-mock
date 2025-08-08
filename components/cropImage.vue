<template>
  <div class="crop-container">
    <!-- Controles de tamanho -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Tamanho: {{ size }}%
      </label>
      <input
        v-model.number="size"
        type="range"
        min="0"
        max="150"
        step="1"
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
        @change="onSize"
      >
    </div>

    <!-- Controles de ação -->
    <div class="flex flex-wrap gap-2 mb-4 justify-center">
      <button
        class="flex items-center justify-center w-10 h-10 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
        title="Zoom In"
        @click="zoom(0.1)"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          <path d="M7 9a1 1 0 011-1h2a1 1 0 110 2H8a1 1 0 01-1-1z" />
          <path d="M9 7a1 1 0 10-2 0v2a1 1 0 102 0V7z" />
        </svg>
      </button>

      <button
        class="flex items-center justify-center w-10 h-10 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
        title="Zoom Out"
        @click="zoom(-0.1)"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          <path d="M7 9a1 1 0 011-1h2a1 1 0 110 2H8a1 1 0 01-1-1z" />
        </svg>
      </button>

      <button
        class="flex items-center justify-center w-10 h-10 bg-green-500 hover:bg-green-600 text-white rounded-md transition-colors"
        title="Girar à Direita"
        @click="rotate(90)"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
      </button>

      <button
        class="flex items-center justify-center w-10 h-10 bg-green-500 hover:bg-green-600 text-white rounded-md transition-colors"
        title="Girar à Esquerda"
        @click="rotate(-90)"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" style="transform: scaleX(-1)">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
      </button>

      <CameraVue
        v-if="showCameraButton"
        @picture="cameraPhoto"
      />
    </div>

    <!-- Área do cropper -->
    <div class="bg-gray-100 overflow-hidden">
      <VueCropper
        ref="cropper"
        :src="imgOrigin"
        :view-mode="3"
        :zoomable="true"
        :auto-crop="true"
        :auto-crop-area="0.6"
        :initial-aspect-ratio="1"
        :aspect-ratio="1"
        :crop-box-movable="true"
        :crop-box-resizable="true"
        :toggle-drag-mode-on-dblclick="false"
        :min-crop-box-width="50"
        :min-crop-box-height="50"
        class="w-full h-80"
        @ready="cropEvent"
        @cropend="cropEvent"
        @zoom="cropEvent"
      />
    </div>
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
      this.cropEvent()
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
.crop-container {
  width: 100%;
}

.slider {
  background: #e5e7eb;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.slider::-webkit-slider-thumb:hover {
  background: #2563eb;
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.preview {
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 50%;
  margin: 10px;
  border: 1px solid #ccc;
}

@media (max-width: 640px) {
  .flex-col {
    flex-direction: column;
  }

  .gap-4 {
    gap: 1rem;
  }

  .gap-2 {
    gap: 0.5rem;
  }
}
</style>
