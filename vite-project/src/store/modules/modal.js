// store/modules/modal.js
export const modal = {
  namespaced: true,
      state: () => ({
        // track open state and content per modal
        modals: {
            popup: { isOpen: false, content: null },
            overlay: { isOpen: false, content: null },
        }
    }),
  mutations: {
        open(state, { name, content }) {
            if (state.modals[name] !== undefined) {
                state.modals[name].isOpen = true;
                state.modals[name].content = content;
            }
        },
        close(state, name) {
            if (state.modals[name] !== undefined) {
                state.modals[name].isOpen = false;
                state.modals[name].content = null;
            }
        }
    },
    actions: {
        openModal({ commit }, { name, content }) {
            commit('open', { name, content });
        },
        closeModal({ commit }, name) {
            commit('close', name);
        },
    }
};
