<template>
  <div class="app">
    <header class="p-3 bg-dark text-white">
      <div class="container-fluid">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-auto mb-lg-0">
            <a
              href="javascript:void(0);"
              class="w-100 d-flex align-items-center text-white text-center"
              @click="$router.push('/')"
            >
              <img src="@/assets/LOGOUsaTex.png" alt="logo" height="60" class="mx-auto">
            </a>
          </div>
        </div>
      </div>
    </header>

    <div class="container py-3">
      <div class="row justify-content-center mb-0 align-items-center mb-3">
        <div class="col-12'col-md-6 col-lg-auto boxIll" :style="'background-image: url('+croppedImage+'); background-size: '+backgroundSize+'% auto'">
          <div class="card bg-transparent border-0">
            <div class="row justify-content-center">
              <div class="col overflow-hidden p-0">
                <img :src="mockupSelected?.img" class="imgMockup" alt="mockup">
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center">
        <div class="col-4">
          <input
            id="customRange1"
            v-model="backgroundSize"
            type="range"
            class="form-range w-100 mb-3"
            step="1"
            min="0"
            max="150"
            @change="imgSize"
          >
        </div>
      </div>
      <div class="row">
        <div class="col-12 col-md-6">
          <select v-model="mockupSelected" class="form-control mb-3">
            <option value="" disabled>
              Selecione um Mockup
            </option>
            <option v-for="mockup in listMockups" :key="mockup.name" :value="mockup">
              {{ mockup.name }}
            </option>
          </select>
          <div class="boxListImgs row justify-content-center mb-2">
            <div v-for="(item, id) of listMockups" :key="'thumb'+id" class="boxImg col-auto px-0">
              <img :src="item.img" :alt="item.name" width="64" @click="mockupSelected = item">
            </div>
          </div>
        </div>
        <div v-if="!camera" class="col-12 col-md-6">
          <select v-model="backgroundSelected" class="form-control mb-3" @change="imgCropped(backgroundSelected.texture)">
            <option v-for="background in backgroundList" :key="background.name" :value="background">
              {{ background.name }}
            </option>
          </select>

          <div class="boxListImgs row justify-content-center">
            <div v-for="(item, id) of backgroundList" :key="'thumb'+id" class="boxImg col-auto px-0" @click="imgCropped(item.texture)">
              <img :src="item.img" :alt="item.name" width="64">
            </div>
          </div>
        </div>
        <div v-else class="col-12 col-md-6">
          <cropImage :img="ImageSelectCropped" :show-camera="camera" :show-camera-button="camera" @crop="imgCropped" @size="imgSize" />
        </div>
      </div>
    </div>
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
    if (listaImages.imagens.length > 0) {
      this.backgroundList = listaImages.imagens.map((item, index) => {
        return { name: 'Modelo ' + (item.replace('.jpg', '')), img: '/assets/thumb/' + item, texture: '/assets/modelos/' + item }
      })
      this.mockupSelected = this.listMockups[0]
      this.backgroundSelected = this.backgroundList[0]
      this.ImageSelectCropped = this.backgroundSelected.texture
    }
  },
  methods: {
    imgCropped (img) {
      this.croppedImage = img
      this.backgroundSelected = this.backgroundList.find(item => item.texture === img)
    },
    imgSize (size) {
      this.backgroundSize = size
    },
    imgCamera (img) {
      this.backgroundList.push({ name: 'Foto ' + (this.backgroundList.length + 1), img })
      this.backgroundSelected = this.backgroundList[this.backgroundList.length - 1]
      this.ImageSelectCropped = this.backgroundSelected.img
    }
  }
}
</script>
<style lang="scss">
.imgMockup{

  max-height:516px;
  width: 100%;
}
.boxIll{
  max-height:calc(100vh - 150px);
  max-width: 100%;
}
button svg{
  width:20px;
}
.boxListImgs{
  height:300px;
  overflow-y:scroll;
  .boxImg{
    &:hover{
      opacity:0.7;
    }
  }
}
</style>
