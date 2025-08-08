<template>
  <div class="min-h-screen">
    <Model :camera="false" />
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  head () {
    return {
      title: 'UsaTex - Mockup Designer',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'Design mockups personalizados com estampas - UsaTex'
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
