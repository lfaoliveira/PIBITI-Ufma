<!-- Modal.vue -->
<template>
    <Teleport to="#modal" v-if="isOpen">
        <div class="absolute inset-0" @click.self="close">
            <div class="">
                <component :is="content.component" v-bind="content.props" />
                <!-- <button @click="close">&times;</button> -->
            </div>
        </div>
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
