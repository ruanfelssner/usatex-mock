<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header melhorado -->
    <header class="bg-white shadow-md">
      <div class="container mx-auto px-4 py-3">
        <div class="flex justify-center">
          <button
            class="transition-transform hover:scale-105 focus:outline-none"
            @click="$router.push('/')"
          >
            <img src="@/assets/LOGOUsaTex.png" alt="UsaTex Logo" class="h-12 w-auto">
          </button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="container mx-auto px-4 py-4 max-w-7xl">

      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="bg-white rounded-lg shadow-md p-4 col-span-2">
          <h3 class="text-lg font-semibold text-gray-700 mb-3 text-center">Preview</h3>

          <div class="flex justify-center mb-4">
            <div
              class="relative bg-gray-100 rounded-lg overflow-hidden max-w-sm w-full"
              id="main-background"
              :style="'background-image: url('+croppedImage+'); background-size: '+backgroundSize+'% auto; background-position: center;'"
            >
              <div class="flex items-center justify-center">
                <img
                  v-if="mockupSelected?.img"
                  :src="mockupSelected.img"
                  :alt="mockupSelected.name"
                  class="w-full h-auto object-contain"
                >
              </div>
            </div>
          </div>

          <!-- Controle de tamanho -->
          <div class="mx-auto max-w-xs">
            <label class="block text-sm font-medium text-gray-600 mb-2 text-center">
              Tamanho: {{ backgroundSize }}%
            </label>
            <input
              v-model.number="backgroundSize"
              type="range"
              min="0"
              max="150"
              step="1"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              @input="imgSize(backgroundSize)"
            >
          </div>
        </div>

        <!-- Mockups - Coluna 1 -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <h3 class="text-lg font-semibold text-gray-700 mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
            </svg>
            Mockups
          </h3>

          <select
            v-model="mockupSelected"
            class="w-full p-2 border border-gray-300 rounded-md mb-3 text-gray-700 bg-white text-sm"
          >
            <option value="" disabled>Selecione um Mockup</option>
            <option v-for="mockup in listMockups" :key="mockup.name" :value="mockup">
              {{ mockup.name }}
            </option>
          </select>

          <div class="grid grid-cols-2 gap-2 max-h-80 min-h-48 overflow-y-auto">
            <button
              v-for="(item, id) of listMockups"
              :key="'mockup-' + id"
              :class="[
                'aspect-square rounded-md overflow-hidden border-2 transition-all',
                mockupSelected?.name === item.name
                  ? 'border-blue-400'
                  : 'border-gray-200 hover:border-blue-300'
              ]"
              @click="mockupSelected = item"
            >
              <img
                :src="item.img"
                :alt="item.name"
                class="w-full h-full object-cover"
                loading="lazy"
              >
            </button>
          </div>
        </div>

        <!-- Estampas / Câmera - Coluna 3 -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <div class="flex items-center justify-between mb-3 flex-wrap">
            <h3 class="text-lg font-semibold text-gray-700 flex items-center">
              <svg
                class="w-5 h-5 mr-2"
                :class="showCamera ? 'text-purple-500' : 'text-green-500'"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  v-if="!showCamera"
                  fill-rule="evenodd"
                  d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"
                  clip-rule="evenodd"
                />
                <path
                  v-else
                  fill-rule="evenodd"
                  d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.414-1.414A1 1 0 0012.586 3H7.414a1 1 0 00-.707.293L5.293 4.707A1 1 0 014.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z"
                  clip-rule="evenodd"
                />
              </svg>
              {{ showCamera ? 'Câmera' : 'Estampas' }}
            </h3>

            <button
              v-if="camera"
              @click="showCamera = !showCamera"
              :class="[
                'px-3 py-1 rounded-md text-sm font-medium transition-all flex',
                showCamera
                  ? 'bg-purple-100 text-purple-700 hover:bg-purple-200'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              ]"
            >
              {{ showCamera ? 'Ver Estampas' : 'Usar Câmera' }}
            </button>
          </div>

          <div v-if="!showCamera">
            <select
              v-model="backgroundSelected"
              class="w-full p-2 border border-gray-300 rounded-md mb-3 text-gray-700 bg-white text-sm"
              @change="imgCropped(backgroundSelected.texture)"
            >
              <option v-for="background in backgroundList" :key="background.name" :value="background">
                {{ background.name }}
              </option>
            </select>

            <div class="grid grid-cols-2 gap-2 max-h-80 min-h-48 overflow-y-auto">
              <button
                v-for="(item, id) of backgroundList"
                :key="'bg-' + id"
                :class="[
                  'aspect-square rounded-md overflow-hidden border-2 transition-all cursor-pointer',
                  backgroundSelected?.name === item.name
                    ? 'border-green-400'
                    : 'border-gray-200 hover:border-green-300'
                ]"
                @click="imgCropped(item.texture)"
              >
                <img
                  :src="item.img"
                  :alt="item.name"
                  class="w-full h-full object-cover"
                  loading="lazy"
                >
              </button>
            </div>
          </div>

          <div v-else>
            <cropImage
              :img="ImageSelectCropped"
              :show-camera="showCamera"
              :show-camera-button="showCamera"
              @crop="imgCropped"
              @size="imgSize"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import listaImages from '@/listaImages.json'
import listaMockups from '@/listaMockups.json'
export default {
  name: 'IndexPage',
  props: {
    camera: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      showCamera: false, // Controla se mostra câmera ou estampas
      holdTime: 0,
      holdTimer: null,
      croppedImage: '',
      ImageSelectCropped: '',
      mockupSelected: null,
      backgroundSize: 50,
      activeList: true,
      listMockups: listaMockups.mockups,
      backgroundSelected: {
        name: 'background1',
        img: 'https://as2.ftcdn.net/v2/jpg/04/29/05/79/1000_F_429057920_h3o2Y9HJrK5RtN0QPm6gOMjCcTe1n6xK.jpg'
      },
      backgroundList: []
    }
  },
  mounted () {
    // Inicializar showCamera baseado na prop camera
    this.showCamera = this.camera

    if (listaImages.imagens.length > 0) {
      this.backgroundList = listaImages.imagens.map((item, index) => {
        return { name: 'Modelo ' + (item.replace('.jpg', '')), img: '/assets/thumb/' + item, texture: '/assets/modelos/' + item }
      })
      this.mockupSelected = this.listMockups[0]
      this.backgroundSelected = this.backgroundList[0]
      this.ImageSelectCropped = this.backgroundSelected.texture

      // Aplicar o background default automaticamente
      this.croppedImage = this.backgroundSelected.texture
    }
  },
  methods: {
    imgCropped (img) {
      this.croppedImage = img
      this.backgroundSelected = this.backgroundList.find(item => item.texture === img)
    },
    imgSize (size) {
      // Garantir que o valor seja numérico
      const numericSize = Number(size)
      if (!isNaN(numericSize)) {
        this.backgroundSize = numericSize
      }
    },
    imgCamera (img) {
      this.backgroundList.push({ name: 'Foto ' + (this.backgroundList.length + 1), img })
      this.backgroundSelected = this.backgroundList[this.backgroundList.length - 1]
      this.ImageSelectCropped = this.backgroundSelected.img
    }
  }
}
</script>
<style>
/* Slider customizado */
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
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Melhorias para o background e mockup */
#main-background {
  background-color: transparent;
}

/* Scrollbar customizado */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f7fafc;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 2px;
}

/* Transitions */
.transition-all {
  transition: all 0.2s ease;
}

/* Aspect ratio utility */
.aspect-square {
  aspect-ratio: 1 / 1;
}

/* Background utilities */
.bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.from-gray-50 {
  --tw-gradient-from: #f9fafb;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(249, 250, 251, 0));
}

.to-gray-100 {
  --tw-gradient-to: #f3f4f6;
}
</style>
