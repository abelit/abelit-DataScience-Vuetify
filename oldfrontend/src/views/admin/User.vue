<template>
  <div class="d-page-fullscreen">
    <vue-perfect-scrollbar :class="isPageFullScreen?'d-page-scroll-fullscreen ps':'ps'">
      <v-container fluid :class="isPageFullScreen?'pa-1':''">
        <v-layout row wrap>
          <!-- <v-flex xs1>
         <v-btn icon @click="toggleFullscreen" class="mx-0">
      <v-icon class="text--secondary">fullscreen</v-icon>
    </v-btn>
          </v-flex>-->
          <v-flex lg12>
            <v-card>
              <v-toolbar flat color="white">
                <v-flex xs2>
                  <v-text-field
                    flat
                    solo
                    prepend-icon="search"
                    :placeholder="$t('admin.typeSomething')"
                    v-model="search"
                    hide-details
                  ></v-text-field>
                </v-flex>
                <v-spacer></v-spacer>
                <d-refresh :pMethod="getUsers"></d-refresh>
                <d-new-user
                  ref="dnewuser"
                  :pdialog="pdialog"
                  :editedItem="editedItem"
                  :editedIndex="editedIndex"
                  @pChangeDialog="pChangeDialog"
                ></d-new-user>
                <v-btn @click="handleDownload" :loading="downloadLoading" icon>
                  <v-icon color="primary">cloud_download</v-icon>
                </v-btn>
              </v-toolbar>
              <v-divider></v-divider>
              <v-card-text class="pa-0">
                <v-data-table
                  :headers="result.headers"
                  :search="search"
                  :items="result.items"
                  :rows-per-page-items="[10,25,50,{text:'All','value':-1}]"
                  :pagination.sync="paginationSettings"
                  class="elevation-1"
                  item-key="username"
                  select-all
                  v-model="result.selected"
                  :loading="isLoading"
                  id="example"
                  value
                >
                  <template v-slot:items="props">
                    <td class="pr-0">
                      <v-checkbox primary hide-details v-model="props.selected"></v-checkbox>
                    </td>
                    <td>{{ props.item.username }}</td>
                    <td class="text-xs-left">{{ props.item.name }}</td>
                    <td class="text-xs-left">{{ props.item.email }}</td>
                    <td
                      class="text-xs-left"
                    >{{ (props.item.gender===1)?$t("auth.MALE"):$t("auth.FEMALE") }}</td>
                    <td class="text-xs-left">{{ props.item.group.name }}</td>
                    <td class="text-xs-left">{{ props.item.position.name }}</td>
                    <td class="text-xs-left">
                      <v-chip
                        outline
                        color="primary"
                        v-for="k in props.item.role"
                        :key="k.id"
                      >{{ k.name}}</v-chip>
                    </td>
                    <td class="text-xs-left">
                      <v-chip
                        :color="props.item.status===1?'primary':''"
                      >{{ (props.item.status===1)?$t("button.enabled"):$t("button.disabled") }}</v-chip>
                    </td>
                    <td class="text-xs-left">{{ props.item.created_time }}</td>

                    <td>
                      <v-icon small class="mr-2" color="primary" @click="editItem(props.item)">edit</v-icon>
                      <v-icon small color="error" @click="deleteItem(props.item)">delete</v-icon>
                    </td>
                  </template>
                  <template v-slot:no-data>
                    <span>{{$t("message.noData")}}</span>
                  </template>
                  <template v-slot:no-results>
                    <v-alert
                      :value="true"
                      color="error"
                      icon="warning"
                    >{{ $t("admin.noRecordFound") }}</v-alert>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </vue-perfect-scrollbar>
  </div>
</template>


<script>
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import DNewUser from "@/components/admin/DNewUser";
import DRefresh from "@/components/widgets/tool/DRefresh";

export default {
  components: {
    DNewUser,
    DRefresh,
    VuePerfectScrollbar
  },
  data: () => ({
    svalue: [],
    isLoading: false,
    downloadLoading: false,
    filename: "",
    autoWidth: true,
    bookType: "xlsx",
    search: "",
    pdialog: false,
    paginationSettings: {
      rowsPerPage: 25
    },
    result: {
      selected: [],
      headers: [
        {
          text: "用户名",
          align: "left",
          value: "username"
        },
        { text: "姓名", value: "name" },
        { text: "邮箱", value: "email" },
        { text: "性别", value: "gender" },
        { text: "部门", value: "group" },
        { text: "职位", value: "position" },
        { text: "角色", value: "role" },
        { text: "状态", value: "status" },
        { text: "创建日期", value: "created_time" },
        { text: "操作", value: "action", sortable: false }
      ],
      items: []
    },
    editedIndex: -1,
    editedItem: {
      username: "",
      name: "",
      email: "",
      password: "",
      selected_department: "",
      selected_position: "",
      selected_gender: "",
      status: false,
      selected_role: ""
    },
    defaultItem: {
      username: "",
      name: "",
      email: "",
      password: "",
      selected_department: "",
      selected_position: "",
      selected_gender: "",
      status: false,
      selected_role: ""
    }
  }),

  computed: {
    isPageFullScreen() {
      return this.$store.state.isPageFullScreen;
    }
  },

  watch: {
    pdialog(val) {
      val || this.close();
      this.getUsers();
    },
    selected(val) {
      console.log(val);
    }
  },

  created() {
    this.getUsers();
  },

  methods: {
    // 从后台获取用户信息
    getUsers() {
      this.isLoading = true;
      setTimeout(() => {
        this.$axios
          .get("/admin/user/list")
          .then(res => {
            this.result.items = res.data;
          })
          .catch(error => {
            console.log(error);
          });
        this.isLoading = false;
      }, 1500);
    },
    deleteUser(item) {
      this.$axios
        .post("/admin/user/delete", {
          username: item.username
        })
        .then(() => {
          this.isActive = true;
          this.message = this.$t("message.SUCCESS_REGISTER");
          setTimeout(() => {
            this.message = "";
            // 跳转上一请求页面或主页
          }, 1000);
        })
        .catch(() => {
          this.isActive = false;
          this.message = this.$t("message.ERROR_REGISTER");
          setTimeout(() => {
            this.message = "";
          }, 1000);
        });
    },
    // 编辑条目
    editItem(item) {
      this.pdialog = true;
      this.editedIndex = this.result.items.indexOf(item);
      // this.editedItem = Object.assign({}, item);
      let genderName = this.$t("auth.MALE");
      let isStatus = false;
      if (item.gender === 0) {
        genderName = this.$t("auth.FEMALE");
      }
      if (item.status === 1) {
        isStatus = true;
      }
      this.editedItem = Object.assign({
        username: item.username,
        name: item.name,
        email: item.email,
        // password: item.password,
        selected_department: item.group,
        selected_position: item.position,
        selected_gender: { name: genderName, code: item.gender },
        status: isStatus,
        selected_role: item.role
      });
      // 调用子组件DNewUser中updateUser方法更新用户信息内容并提交保存入库
      this.$refs.dnewuser.updateUser();
    },
    // 删除条目
    deleteItem(item) {
      const index = this.result.items.indexOf(item);
      let isConfirm = confirm(this.$t("message.deleteDataTip"));
      if (isConfirm){
        this.deleteUser(item);
        this.result.items.splice(index, 1);
      }
    },

    close() {
      this.pdialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
    pChangeDialog() {
      console.log("pChangeDialog: " + this.pdialog);
      this.pdialog = false;
    },
    // 页面全屏
    toggleFullscreen() {
      this.$fullscreen.toggle(this.$el.querySelector(".d-content-fullscreen"), {
        wrap: false,
        callback: this.fullscreenChange
      });
    },
    fullscreenChange(fullscreen) {
      this.fullscreen = fullscreen;
    },
    handleDownload() {
      this.downloadLoading = true;
      import("@/assets/vendor/js/Export2Excel").then(excel => {
        let tHeader = [];
        for (var i = 0; i <= this.result.headers.length - 2; i++) {
          tHeader.push(this.result.headers[i]["text"]);
        }
        let fHeader = [];
        for (var i = 0; i <= this.result.headers.length - 2; i++) {
          fHeader.push(this.result.headers[i]["value"]);
        }
        console.log(this.result.items[0].position.name);

        let fData = [];
        let fRole = "";
        for (var i = 0; i <= this.result.items.length - 1; i++) {
          for (var j = 0; j <= this.result.items[i].role.length - 1; j++) {
            if (j === 0) {
              fRole = fRole + this.result.items[i].role[j].name;
            } else {
              fRole = fRole + "," + this.result.items[i].role[j].name;
            }
          }
          fData.push({
            username: this.result.items[i].username,
            name: this.result.items[i].name,
            email: this.result.items[i].email,
            gender:
              this.result.items[i].gender === 0
                ? this.$t("auth.FEMALE")
                : this.$t("auth.MALE"),
            position: this.result.items[i].position.name,
            group: this.result.items[i].group.name,
            status:
              this.result.items[i].status === 0
                ? this.$t("button.disable")
                : this.$t("button.enable"),
            role: fRole,
            created_time: this.result.items[i].created_time
          });
        }
        let data = this.formatJson(fHeader, fData);
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.filename,
          autoWidth: this.autoWidth,
          bookType: this.bookType
        });
        this.downloadLoading = false;
      });
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v =>
        filterVal.map(j => {
          if (j === "timestamp") {
            return parseTime(v[j]);
          } else {
            return v[j];
          }
        })
      );
    },
    handleDownloadNew() {
      $("#example").tableHTMLExport({
        // csv, txt, json, pdf
        type: "pdf",

        // file name
        filename: "sample.pdf"
      });
    }
  },
  mounted() {
  }
};
</script>


<style lang="scss" rel="stylesheet/scss" scoped>
.wrapper {
  position: relative;
  height: 400px;
  .chart-container {
    height: 100%;
    width: 100%;
  }
  .btn-map-fullscreen {
    position: absolute;
    right: 10px;
    bottom: 10px;
    width: 36px;
    height: 36px;
    padding: 0;
    font-size: 36px;
    line-height: 36px;
    text-align: center;
    outline: none;
  }
  &.fullscreen {
    display: flex;
    justify-content: center;
    align-items: center;
    .chart-container {
      height: 60%;
      width: 60%;
    }
    .btn-map-fullscreen {
      left: 10px;
      top: 10px;
      right: auto;
      bottom: auto;
    }
  }
}
.d-page-scroll-fullscreen {
  height: 100vh;
  overflow: auto;
}
.d-page-scroll {
  height: calc(100vh - 56px - 56px - 37px);
  overflow: auto;
}
</style>