const actions = {
  setLanguage({ commit }, value) {
    commit("setLanguage", value);
  },
  setLockPassword({ commit }, value) {
    commit("setLockPassword", value);
  },
  logout({commit}) {
    commit("logout");
  },
  setFullscreen({commit}) {
    commit("setFullscreen");
  }
};

export default actions;
