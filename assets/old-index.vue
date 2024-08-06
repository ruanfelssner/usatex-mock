<template>
  <div class="container">
    <div class="row py-5 justify-content-center">
      <div class="col-auto">
        <select v-model="mockupSelected">
          <option v-for="mockup in listMockups" :key="mockup.name" :value="mockup">
            {{ mockup.name }}
          </option>
        </select>
        <select v-model="backgroundSelected" @change="croppedImage = backgroundSelected.img">
          <option v-for="background in backgroundList" :key="background.name" :value="background">
            {{ background.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="row justify-content-center mb-0">
      <div class="col-auto p-0" :style="'background-image: url('+croppedImage+')'">
        <div class="card bg-transparent border-0">
          <div class="row justify-content-center">
            <div class="col-auto overflow-hidden p-0">
              <img :src="mockupSelected?.img" alt="mockup">
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-8">
        <NuxtCropper
          ref="cropper"
          :cropper-options="{
            autoCropArea: .5,
            viewMode: 1,
            zoom: 5,
            crop: (e) => cropMove(e)
          }"
          :src="backgroundSelected.img"
        />
        <button @click="zoomAdd">
          Zoom +
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data () {
    return {
      croppedImage: null,
      mockupSelected: null,
      listMockups: [
        { name: 'alistar', img: '/assets/mockups/alistar.png' },
        { name: 'bagg', img: '/assets/mockups/bagg.png' },
        { name: 'biquini', img: '/assets/mockups/biquini.png' },
        { name: 'Bolsa', img: '/assets/mockups/Bolsa.png' },
        { name: 'cushion', img: '/assets/mockups/cushion.png' },
        { name: 'dress-mask', img: '/assets/mockups/dress-mask.png' },
        { name: 'Iphone-mask', img: '/assets/mockups/Iphone-mask.png' },
        { name: 'kaftan', img: '/assets/mockups/kaftan.png' },
        { name: 'kids-t-mask', img: '/assets/mockups/kids-t-mask.png' },
        { name: 'Legging', img: '/assets/mockups/Legging.png' },
        { name: 'leggings-mask', img: '/assets/mockups/leggings-mask.png' },
        { name: 'leggings', img: '/assets/mockups/leggings.png' },
        { name: 'mochila', img: '/assets/mockups/mochila.png' },
        { name: 'mochila02', img: '/assets/mockups/mochila02.png' },
        { name: 'parede', img: '/assets/mockups/parede.png' },
        { name: 'peep-toe', img: '/assets/mockups/peep-toe.png' },
        { name: 'Running-Shoes', img: '/assets/mockups/Running-Shoes.png' },
        { name: 'Saia', img: '/assets/mockups/Saia.png' },
        { name: 'Sandalia', img: '/assets/mockups/Sandalia.png' },
        { name: 'sapatilha', img: '/assets/mockups/sapatilha.png' },
        { name: 'sapatosalto', img: '/assets/mockups/sapatosalto.png' },
        { name: 'scarf', img: '/assets/mockups/scarf.png' },
        { name: 'scarpin', img: '/assets/mockups/scarpin.png' },
        { name: 'shirt-mask', img: '/assets/mockups/shirt-mask.png' },
        { name: 'shoes', img: '/assets/mockups/shoes.png' },
        { name: 'skid-grip', img: '/assets/mockups/skid-grip.png' },
        { name: 'slip-on', img: '/assets/mockups/slip-on.png' },
        { name: 'Sneaker', img: '/assets/mockups/Sneaker.png' },
        { name: 'sofa', img: '/assets/mockups/sofa.png' },
        { name: 'Square-Pillow', img: '/assets/mockups/Square-Pillow.png' },
        { name: 'SquarePillow', img: '/assets/mockups/SquarePillow.png' },
        { name: 'swinsuit', img: '/assets/mockups/swinsuit.png' },
        { name: 'toalha', img: '/assets/mockups/toalha.png' },
        { name: 'top-tenis', img: '/assets/mockups/top-tenis.png' },
        { name: 'trainer-mask', img: '/assets/mockups/trainer-mask.png' },
        { name: 'wallpaper-mask', img: '/assets/mockups/wallpaper-mask.png' },
        { name: 'wshoe', img: '/assets/mockups/wshoe.png' }
      ],
      backgroundSelected: {
        name: 'background1',
        img: 'https://as2.ftcdn.net/v2/jpg/04/29/05/79/1000_F_429057920_h3o2Y9HJrK5RtN0QPm6gOMjCcTe1n6xK.jpg'
      },
      backgroundList: [
        { name: 'background1', img: '/assets/backgrounds/background1.jpg' },
        { name: 'background2', img: '/assets/backgrounds/background2.jpg' },
        { name: 'background3', img: '/assets/backgrounds/background3.jpg' },
        { name: 'background4', img: '/assets/backgrounds/background4.jpg' }
      ]
    }
  },
  methods: {
    async cropMove (e) {
      const blob = await this.$refs.cropper.getCroppedBlob()
      this.croppedImage = URL.createObjectURL(blob)
    },
    zoomAdd () {
      console.log(this.$refs.cropper)
    }
  }
}
</script>
