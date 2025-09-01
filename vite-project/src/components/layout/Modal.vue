<!-- Modal.vue -->
<template>
    <Teleport to="#modal" v-if="isOpen">
        <div class="modal-overlay" @click.self="close">
            <div class="modal-content">
                <component :is="content.component" v-bind="content.props" />
                <button @click="close">Close</button>
            </div>
        </div>
    </Teleport>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
    props: {
        name: { type: String, required: true },
    },
    computed: {
        ...mapState("modal", {
            modalState: (state) => state.modals[this.name],
        }),
        isOpen() {
            return this.modalState?.isOpen;
        },
        content() {
            return this.modalState?.content || {};
        },
    },
    methods: {
        ...mapActions("modal", ["closeModal"]),
        close() {
            this.closeModal(this.name);
        },
    },
};
</script>

<style>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
}
</style>
