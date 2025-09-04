<!-- Modal.vue -->
<template>
    <Teleport to="#modal">
        <Transition
            enter-active-class="transition ease-out duration-1000"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition ease-in duration-600"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
        >
            <div v-if="isOpen" class="absolute inset-0" >
                <div class="">
                    <component :is="content.component" v-bind="content.props" />
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
    props: {
        name: { type: String, required: true },
    },
    computed: {
        ...mapState("modal", ["modals"]),
        modalState() {
            console.log("LOAD MODAL STATE: " + JSON.stringify(this.modals[this.name]));
            return this.modals[this.name] || {};
        },
        isOpen() {
            console.log("MODAL ABERTO: " + String(this.modalState.isOpen));
            return this.modalState.isOpen;
        },
        content() {
            return this.modalState.content || {};
        },
    },
    methods: {
        ...mapActions("modal", ["closeModal", "openModal", "closeAllModals"]),
        close() {
            this.closeModal(this.name);
        },
    },
};
</script>

<style></style>
