export const modal = {
  namespaced: true,
  state: () => ({
    openList: [],  // e.g. ['popup','overlay','notice']
    modals: {
      popup: { content: null },
      overlay: { content: null },
      notice: { content: null }
    }
  }),
  mutations: {
    open(state, { name, content }) {
      if (!state.openList.includes(name) && state.modals[name]) {
        state.openList.push(name);
        state.modals[name].content = content;
      }
    },
    closeOne(state, name) {
      const idx = state.openList.indexOf(name);
      if (idx !== -1) {
        state.openList.splice(idx, 1);
        state.modals[name].content = null;
      }
    },
    closeAll(state) {
      state.openList.forEach(name => {
        state.modals[name].content = null;
      });
      state.openList = [];
    }
  },
  actions: {
    openModal({ commit }, payload) {
      commit('open', payload);
    },
    closeModal({ commit }, name) {
      commit('closeOne', name);
    },
    closeAllModals({ commit }) {
      commit('closeAll');
    }
  }
};
