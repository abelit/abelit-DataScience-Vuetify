<template>
  <v-menu
    :close-on-content-click="false"
    bottom
    min-width="300"
    max-width="300"
    nudge-bottom="10"
    offset-y
    transition="slide-y-transition"
    
  >
    <template v-slot:activator="{ on }">
      <div v-on="on">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn dark icon v-on="on" class="setting-fab">
              <v-icon>camera</v-icon>
            </v-btn>
          </template>
          <span>{{$t("tooltip.THEME_PICKER")}}</span>
        </v-tooltip>
      </div>
    </template>

    <v-card>
      <v-container grid-list-xl>
        <v-layout wrap>
          <v-flex xs12>
            <div class="text-xs-center body-2 text-uppercase sidebar-filter">{{ $t("theme.NAVBAR_THEME") }}</div>

            <v-layout justify-center>
              <v-avatar
                v-for="c in toolbarColors"
                :key="c"
                :class="[c === toolbarColor?'color-tb-active color-tb-' + c:'color-tb-'+c]"
                size="23"
                @click="setToolbarColor(c)"
              />
            </v-layout>
            <v-divider class="mt-3"/>
          </v-flex>

          <v-flex xs12>
            <div class="text-xs-center body-2 text-uppercase sidebar-filter">{{ $t("theme.BUTTON_THEME") }}</div>

            <v-layout justify-center>
              <v-avatar
                v-for="c in buttonColors"
                :key="c"
                :class="[c === buttonColor?'color-btn-active color-btn-' + c:'color-btn-'+c]"
                size="23"
                @click="setSidebarButtonColor(c)"
              />
            </v-layout>
            <v-divider class="mt-3"/>
          </v-flex>

          <v-flex xs12>
            <div class="text-xs-center body-2 text-uppercase sidebar-filter">{{ $t("theme.SIDEBAR_THEME") }}</div>
          </v-flex>
          <v-flex v-for="img in images" :key="img" xs3>
            <v-img
              :class="[image === img ? 'image-active' : '']"
              :src="img"
              height="120"
              @click.native="setSidebarImageNew(img)"
            />
          </v-flex>
          <v-flex v-for="c in colors" :key="c" xs3>
            <v-img
              :class="[c === color?'image-active color-' + c:'color-'+c]"
              height="120"
              @click.native="setSidebarColorNew(c)"
            />
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-menu>
</template>

<script>
// Utilities
import { mapState, mapActions } from "vuex";
export default {
  data: () => ({
    colors: ["deep-purple", "orange", "grey", "cyan"],
    buttonColors: [
      "deep-purple",
      "green",
      "cyan",
      "orange",
      "red",
      "grey"
    ],
    toolbarColors: [
      "deep-purple",
      "green",
      "cyan",
      "orange",
      "red",
      "grey"
    ],
    images: [
      "/static/images/theme/sidebar/sidebar003.jpg",
      "/static/images/theme/sidebar/sidebar002.jpg",
      "/static/images/theme/sidebar/sidebar005.jpg",
      "/static/images/theme/sidebar/sidebar007.jpg"
    ]
  }),

  computed: {
    ...mapState(["color", "image", "buttonColor", "toolbarColor"])
  },

  methods: {
    ...mapActions([
      "setSidebarImage",
      "setSidebarButtonColor",
      "setSidebarColor",
      "setToolbarColor"
    ]),
    setSidebarImageNew(val) {
      this.setSidebarColor("");
      this.setSidebarImage(val);
    },
    setSidebarColorNew(val) {
      this.setSidebarImage("");
      this.setSidebarColor(val);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/assets/styles/index.scss";
.v-avatar,
.v-responsive {
  cursor: pointer;
}
</style>


<style lang="stylus">
  .setting-fab 
    top:50%!important; 
    right:0;
    border-radius:0  
</style>