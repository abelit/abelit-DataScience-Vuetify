<template>
  <v-container fluid fill-height>
    <v-row align="center" justify="center">
      <div class="mr-3 hidden-sm-and-down">
        <v-img :src="require('@/assets/images/error/404.svg')"></v-img>
      </div>
      <div class="text-md-center">
        <h1>404</h1>
        <h2 class="my-3 headline">Sorry, page not found</h2>
        <div>
          <v-btn color="primary" @click="goHome">
            <v-icon>mdi-keyboard-return</v-icon>
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </div>
      </div>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    goHome() {
      this.$router.push({ path: "/" });
    }
  }
};
</script>
<style scoped lang="css">
h1 {
  font-size: 150px;
  line-height: 150px;
  font-weight: 700;
  color: #252932;
  text-shadow: rgba(61, 61, 61, 0.3) 1px 1px, rgba(61, 61, 61, 0.2) 2px 2px,
    rgba(61, 61, 61, 0.3) 3px 3px;
}
</style>
