export const modal = {
  namespaced: true,
  state: () => ({
    openList: [],  // e.g. ['popup','overlay','notice']
    modals: {
      popup: { content: null, isOpen: false },
      overlay: { content: null, isOpen: false },
      notice: { content: null, isOpen: false }
    }
  }),
  mutations: {
    open(state, { name, content }) {
      if (!state.openList.includes(name) && state.modals[name]) {
        state.openList.push(name);
        state.modals[name].content = content;
        state.modals[name].isOpen = true; // Set isOpen to true
      }
    },
    close(state, name) {
      const idx = state.openList.indexOf(name);
      if (idx !== -1) {
        state.openList.splice(idx, 1);
        state.modals[name].content = null;
        state.modals[name].isOpen = false; // Set isOpen to true
      }
    },
    closeAll(state) {
      state.openList.forEach(name => {
        state.modals[name].content = null;
        state.modals[name].isOpen = false; // Set isOpen to true

      });
      state.openList = [];
    }
  },
  actions: {
    openModal({ commit }, payload) {
      commit('open', payload);
    },
    closeModal({ commit }, name) {
      commit('close', name);
    },
    closeAllModals({ commit }) {
      commit('closeAll');
    }
  }
};
