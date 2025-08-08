<template>
  <div class="min-h-screen">
    <Model :camera="true" />
  </div>
</template>

<script>
export default {
  name: 'ClientEstampaPage',
  head () {
    return {
      title: 'UsaTex - Camera & Design',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'Capture e design suas próprias estampas - UsaTex'
        },
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1, user-scalable=no'
        }
      ]
    }
  }
}
</script>
