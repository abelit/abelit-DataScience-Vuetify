<template>
  <div class="login-container container-fluid">
    <v-card class="mx-auto" style="max-width: 500px; margin-top:5%;" color="#eaeaeaa1">
      <v-toolbar color="#01074ccf !important" cards dark flat>
        <v-icon size="36" color="#efefef">account_box</v-icon>
        <v-card-title
          class="title font-weight-regular"
          style="margin: 0 auto;"
        >{{$t('admin.USER_ADD')}}</v-card-title>
      </v-toolbar>
      <v-form ref="form" v-model="form" class="pa-3 pt-4">
        <v-text-field
          v-model="username"
          box
          color="deep-purple"
          :label="$t('auth.USERNAME')"
          type="username"
          v-validate="'required|alpha_num|max:20|min:6'"
          :error-messages="errors.collect('username')+usernameMessage"
          data-vv-name="username"
          required
          class="df-input"
          @focus="checkUsername"
          @blur="checkUsername"
        ></v-text-field>
        <v-text-field
          v-model="name"
          box
          color="deep-purple"
          :label="$t('auth.NAME')"
          type="name"
          v-validate="'required|max:20|min:2'"
          :error-messages="errors.collect('name')"
          data-vv-name="name"
          required
          class="df-input"
        ></v-text-field>

        <v-text-field
          v-model="email"
          box
          color="deep-purple"
          :label="$t('auth.EMAIL')"
          type="email"
          v-validate="'required|email'"
          :error-messages="errors.collect('email') + emailMessage"
          data-vv-name="email"
          required
          class="df-input"
          @focus="checkEmail"
          @blur="checkEmail"
        ></v-text-field>

        <v-text-field
          v-model="password"
          box
          color="deep-purple"
          counter="18"
          :label="$t('auth.PASSWORD')"
          style="min-height: 96px; "
          :append-icon="passwordShow ? 'visibility_off' : 'visibility'"
          :type="passwordShow ? 'text' : 'password'"
          @click:append="passwordShow = !passwordShow"
          v-validate="'required|max:18|min:8'"
          :error-messages="errors.collect('password')"
          data-vv-name="password"
          ref="password"
          required
        ></v-text-field>
        <v-layout wrap align-center>
          <!-- <v-flex xs12 sm6 d-flex> -->
          <v-select
            v-model="selected_department"
            v-validate="'required'"
            :error-messages="errors.collect('department')"
            :items="departments"
            item-text="name"
            item-value="id"
            box
            :label="$t('auth.DEPARTMENT')"
            class="df-select"
            data-vv-name="department"
            required
          ></v-select>
          <!-- </v-flex> -->

          <!-- <v-flex xs12 sm6 d-flex> -->
          <v-select
            v-model="selected_position"
            v-validate="'required'"
            :error-messages="errors.collect('position')"
            :items="positions"
            item-text="name"
            item-value="id"
            box
            :label="$t('auth.POSITION')"
            class="df-select"
            data-vv-name="position"
            required
          ></v-select>
          <!-- </v-flex> -->

          <v-select
            v-model="picked_gender"
            v-validate="'required'"
            :error-messages="errors.collect('gender')"
            :items="genders"
            item-text="name"
            item-value="id"
            box
            :label="$t('auth.GENDER')"
            class="df-select"
            data-vv-name="gender"
            required
          ></v-select>
        </v-layout>
        <v-checkbox
          v-model="status"
          value="1"
          :label="$t('button.ENABLE')"
          data-vv-name="status"
          type="checkbox"
        ></v-checkbox>
      </v-form>
      <v-divider></v-divider>

      <v-card-actions>
        <v-btn
          flat
          class="title font-weight-regular"
          @click="$refs.forauth.reset()"
        >{{$t('button.CLOSE')}}</v-btn>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-btn
          :disabled="!form"
          class="title font-weight-regular"
          color="#01074ccf"
          depressed
          @click="submit"
        ><span  style="color: #efefef">{{$t('button.ADD')}}</span></v-btn>
      </v-card-actions>
      <div class="loading-overlay" v-if="isButtonLoading">
        <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
        <span>{{loadingMessage}}</span>
      </div>

      <div class="loading-overlay" v-if="message">
        <span v-bind:class="[isActive?'activeClass':'errorClass']">{{message}}</span>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    passwordShow: false,
    username: undefined,
    name: undefined,
    email: undefined,
    form: false,
    isButtonLoading: false,
    loadingMessage: "",
    message: undefined,
    usernameMessage: "",
    emailMessage: "",
    password: undefined,
    selected_department: undefined,
    selected_position: undefined,
    picked_gender: undefined,
    departments: [],
    genders: [],
    positions: [],
    status: 0,
    isActive: false
  }),
  methods: {
    // 等待完成表单输入验证后，然后显示登陆加载动画，这里在需要使用async与await关键字
    async submit() {
      await this.$validator.validateAll();

      if (this.$validator.errors.all().length === 0) {
        this.isButtonLoading = true;
        this.loadingMessage = this.$t("message.LOADING");
        setTimeout(() => {
          this.isButtonLoading = false;
          this.$axios
            .post("/admin/user/add", {
              username: this.username,
              name: this.name,
              email: this.email,
              password: this.password,
              selected_department: this.selected_department,
              selected_position: this.selected_position,
              picked_gender: this.picked_gender,
              status: this.status
            })
            .then(() => {
              this.isActive = true;
              this.message = this.$t("message.SUCCESS_ADD");
              setTimeout(() => {
                this.message = "";
              }, 2000);
            })
            .catch(() => {
              this.isActive = false;
              this.message = this.$t("message.ERROR_ADD");
              setTimeout(() => {
                this.message = "";
              }, 2000);
            });
        }, 2000);
      }
    },
    getDepartment() {
      this.$axios
        .get("/api/group")
        .then(res => {
          // console.log(res.data)
          for (var i = 0; i < res.data.length; i++) {
            this.departments.push({
              id: res.data[i].id,
              name: res.data[i].name
            });
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    getPosition() {
      this.$axios
        .get("/api/position")
        .then(res => {
          // console.log(res.data)
          for (var i = 0; i < res.data.length; i++) {
            this.positions.push({
              id: res.data[i].id,
              name: res.data[i].name
            });
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    checkUsername() {
      this.$axios
        .get("/api/checkusername", {
          params: {
            username: this.username
          }
        })
        .then(() => {
          this.usernameMessage = "";
        })
        .catch(() => {
          this.usernameMessage = this.$t("api.USERNAME_EXIST");
        });
    },
    checkEmail() {
      this.$axios
        .get("/api/checkemail", {
          params: {
            email: this.email
          }
        })
        .then(() => {
          this.emailMessage = "";
        })
        .catch(() => {
          this.emailMessage = this.$t("api.EMAIL_EXIST");
        });
    },
    clear() {
      this.name = "";
      this.email = "";
      this.select = null;
      this.checkbox = null;
      this.$validator.reset();
    },
    getGender() {
      let male = this.$t("auth.MALE");
      let female = this.$t("auth.FEMALE");
      this.genders = [
        {
          id: 0,
          name: male
        },
        {
          id: 1,
          name: female
        }
      ];
    }
  },
  mounted() {
    this.getDepartment();
    this.getPosition();
    this.getGender();
  }
};
</script>

<style lang="css" scoped>
.login-container {
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: 100% 100%;
  -moz-background-size: 100% 100%;
}
.df-icon {
  position: relative;
  padding: 10px;
  background: #01074ccf;
  min-width: 50px;
  text-align: center;
  margin-bottom: auto;
  margin-left: 5px;
}

.df-input {
  padding: 10px;
}
.df-select {
  width: 20px;
}
.df-radio {
  margin-top: 0px;
  padding-top: 0px;
}
.activeClass {
  color: green;
  font-size: 18px;
}
.errorClass {
  color: red;
  font-size: 18px;
}
</style>