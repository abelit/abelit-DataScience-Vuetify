import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

// import bootstrap
import "bootstrap/dist/css/bootstrap.css";
import "jquery/dist/jquery.js";
import "bootstrap/dist/js/bootstrap.js";

// import "./plugins/vuetify"; 可以使用以下三行代码代替
// import Vuetify from 'vuetify';
// Vue.use(Vuetify);
// import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

// import Echarts
import echarts from "echarts";
Vue.prototype.$echarts = echarts;

// import axios for ajax application
import axios from "axios";
axios.defaults.baseURL = "http://localhost:5000";
Vue.prototype.$axios = axios;

// 以下是另外两个Vue UI前端框架
// import element framwork and ui component
// import Element UI
// import ElementUI from "element-ui";
// Vue.use(ElementUI);
// import "element-ui/lib/theme-chalk/index.css";
// import Vue Material UI frontend framwork
// import VueMaterial from "vue-material";
// import "vue-material/dist/vue-material.min.css";
// import "vue-material/dist/theme/default.css";
// Vue.use(VueMaterial);

// import fonts
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";

// import vue-i18n for location application
import VueI18n from "vue-i18n";
Vue.use(VueI18n);

// Configure vue-i18n
const i18n = new VueI18n({
  // 启动程序时从本地读取localStorage读取语言，如果没有找不到，则设置为"zh_CN"
  locale: localStorage.getItem("language") || "zh_CN",
  messages: {
    // 中文语言包
    zh_CN: require("./common/lang/zh"),
    // 英文语言包
    en_US: require("./common/lang/en")
  }
});

// import and add vee-validate
import VeeValidate from "vee-validate";
import zh from "vee-validate/dist/locale/zh_CN";
import en from "vee-validate/dist/locale/en";
Vue.use(VeeValidate, {
  i18n,
  i18nRootKey: "validation",
  dictionary: {
    en_US: en,
    zh_CN: zh
  }
});

// 设置浏览器头部标题
import { setTitle } from '@/utils' 


Vue.config.productionTip = false;

/* 请求拦截器 */
axios.interceptors.request.use(
  function (config) {
    // 每次请求时会从localStorage中获取token
    let token = localStorage.getItem("token");

    if (token) {
      token = "bearer" + " " + token.replace(/'|"/g, "");
      // 把token加入到默认请求参数中
      config.headers.common["Authorization"] = token;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// axios响应拦截器，401状态时跳转登录页并清除token
axios.interceptors.response.use(
  response => {
    // console.log("拦截器1");
    // getRoutes();
    return response;
  },
  error => {
    // console.log("拦截器2");
    // console.log(error.response);
    if (error.response) {
      if (error.response.status === 401) {
        // store.commit("delToken");
        // router.push("/user/login");
        // return
        if (localStorage.getItem("token")) {
          let rtoken = JSON.parse(localStorage.getItem("token")).refresh_token;
          axios
            .post(
              "/refresh", {}, {
                headers: {
                  Authorization: "Bearer " + rtoken
                }
              }
            )
            .then(res => {
              store.commit("setToken", {
                access_token: res.data.access_token,
                refresh_token: rtoken
              });
            })
            .catch(error => {
              store.commit("delToken");
              router.push("/user/login");
              console.log(error);
            });
        } else {
          store.commit("delToken");
          router.push("/user/login");
        }
      }
    }
    return Promise.reject(error.response);
  }
);

router.beforeEach(async (to, from, next) => {
  // console.log('beforeEach ...');
  // console.log(to);
  // console.log(from);
  NProgress.start();
  if (store.state.isLock && to.path !== '/lock') {
    next({
      path: '/lock'
    })
  } else {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (localStorage.getItem("token")) {
       const browserHeaderTitle = to.name
      store.commit('SET_BROWSERHEADERTITLE', {
        browserHeaderTitle: browserHeaderTitle
      })
      next();
    } else {
      next({
        path: "/user/login",
        query: {
          url: to.fullPath
        }
      });
    }
  } else {
    next();
  }
  // 动态路由
  if (localStorage.getItem("token")) {
    if (localStorage.getItem("routeList")) {
      let routeList = JSON.parse(localStorage.getItem("routeList"));
      console.log(routeList);
      localStorage.removeItem("routeList");
      // 使用router.onReady解决刷新时新增的动态路由无法生效
      router.onReady(() => {
        genRoutes(routeList);
      });
      next();
    } else {
      next();
    }
  } else {
    router.addRoutes([{
      path: "*",
      name: "404",
      component: () => import("@/views/error/NotFound")
    }]);
  }
}
});

router.afterEach(() => {
  setTimeout(() => {
    const browserHeaderTitle = store.state.browserHeaderTitle
    setTitle(browserHeaderTitle)
  }, 0);
  NProgress.done();
})

function genRoutes(routeList) {
  // 生成路由对象，使用 vue-cli开发时导入组件推荐使用import导入模块
  let routes = [];
  for (let i = 0; i < routeList.length; i++) {
    routes.push({
      path: routeList[i].path,
      name: routeList[i].name,
      component: () => import("@/components/demo/" + routeList[i].component)
    });
  }

  routes.push({
    path: "*",
    name: "404",
    component: () => import("@/views/error/NotFound")
  });

  // 把动态路由写入实列路由表
  // for (var rt in routes) {
  //   router.options.routes.push(routes[rt]);
  // }
  // add dynamic routes 添加动态路由
  router.addRoutes(routes);
  console.log(router.options.routes);
  localStorage.setItem("routeList", JSON.stringify(routeList));
}

// "#app"挂在的是public/index.html里面id=app
// create Vue instance
new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount("#app");