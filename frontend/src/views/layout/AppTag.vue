<template>
  <v-container fluid class="mt-0 ml-0 pa-0 mb-6" v-if="(typeof(isTag) == 'string' && isTag == 'true') || (typeof(isTag) != 'string' && isTag)?true:false">
    <div style="position: fixed; z-index: 1;width: 100%">
      <v-toolbar dense height="32" class="pl-1">
      <v-chip-group show-arrows class="pa-0" v-if="chip">
        <v-chip
          v-if="chip"
          class="mr-1 my-0"
          tag
          close
          to="/"
          color="orange"
          label
          outlined
          small
          @click:close="chip = false"
          @contextmenu.prevent.native="openMenu(tag,$event)"
        >Complete</v-chip>
        <v-chip
          v-if="chip"
          class="mr-1 my-0"
          tag
          close
          to="/"
          color="orange"
          label
          outlined
          small
          @click:close="chip = false"
          @contextmenu.prevent.native="openMenu(tag,$event)"
        >Complete</v-chip>
        <v-chip
          v-if="chip"
          class="mr-1 my-0"
          tag
          close
          to="/"
          color="orange"
          label
          outlined
          small
          @click:close="chip = false"
          @contextmenu.prevent.native="openMenu(tag,$event)"
        >Complete</v-chip>
      </v-chip-group>
    </v-toolbar>
    <!-- <v-divider></v-divider> -->
    <ul v-show="visible" :style="{left:left+'px',top:top+'px'}" class="contextmenu">
      <li>Refresh</li>
      <li>Close</li>
      <li>Close Others</li>
      <li>Close All</li>
    </ul>
    </div>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: function() {
    return {
      chip: true,
      visible: false,
      top: 0,
      left: 0,
      selectedTag: {},
      affixTags: []
    };
  },
  methods: {
    openMenu(tag, e) {
      const menuMinWidth = 105;
      const offsetLeft = this.$el.getBoundingClientRect().left; // container margin left
      const offsetWidth = this.$el.offsetWidth; // container width
      const maxLeft = offsetWidth - menuMinWidth; // left boundary
      const left = e.clientX - offsetLeft + 15; // 15: margin right
      if (left > maxLeft) {
        this.left = maxLeft;
      } else {
        this.left = left;
      }
      console.log(e.clientY)
      this.top = e.clientY - 50;
      this.visible = true;
      this.selectedTag = tag;
    },
    closeMenu() {
      this.visible = false;
    }
  },
  watch: {
    visible(value) {
      if (value) {
        document.body.addEventListener("click", this.closeMenu);
      } else {
        document.body.removeEventListener("click", this.closeMenu);
      }
    }
  },
  created() {
    console.log("isTag: " + this.isTag)
    console.log("isTag: " + typeof(this.isTag))
  },
  computed: {
    ...mapState(["isTag"])
  }
};
</script>

<style lang="scss">
.v-input__append-outer {
  margin: 0 0 !important;
}
.v-input__prepend-outer {
  margin: 0 0 !important;
}
.contextmenu {
  margin: 0;
  background: #fff;
  z-index: 3000;
  position: absolute;
  list-style-type: none;
  padding: 5px 0;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 400;
  color: #333;
  box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, 0.3);
  li {
    margin: 0;
    padding: 7px 16px;
    cursor: pointer;
    &:hover {
      background: #eee;
    }
  }
}
.v-toolbar__content {
  padding-left: 0px;
}
</style>