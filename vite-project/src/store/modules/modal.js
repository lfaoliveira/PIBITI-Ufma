// store/modules/modal.js
export const modal = {
  namespaced: true,
  state: () => ({
    isOpen: false,
    content: null,
  }),
  mutations: {
    open(state, content) {
      state.isOpen = true;
      state.content = content;
    },
    close(state) {
      state.isOpen = false;
      state.content = null;
    },
  },
  actions: {
    openModal({ commit }, content) {
      commit('open', content);
    },
    closeModal({ commit }) {
      commit('close');
    },
  },
};
