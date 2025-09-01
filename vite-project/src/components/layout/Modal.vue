<!-- Modal.vue -->
<template>
    <Teleport to="#modal" v-if="isOpen">
        <div class="absolute inset-0" @click.self="close">
            <div class="">
                <component :is="content.component" v-bind="content.props" />
                <button @click="close">&times;</button>
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
        ...mapState("modal", {
            modals: (state) => state.modals,
        }),
        modalState() {
            return this.modals[this.name] || {};
        },
        isOpen() {
            return this.modalState.isOpen;
        },
        content() {
            return this.modalState.content || {};
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

<style></style>
