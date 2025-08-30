<!-- Modal.vue -->
<template>
    <Teleport to="#modal" v-if="isOpen">
        <div class="modal-overlay" @click.self="closeModal">
            <div class="modal-content">
                <!-- Render dynamic content passed via store -->
                <component :is="contentComponent" v-bind="contentProps" />
                <button @click="closeModal">Close</button>
            </div>
        </div>
    </Teleport>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
    computed: {
        ...mapState("modal", ["isOpen", "content"]),
        contentComponent() {
            // content can be a component or string identifier
            return this.content?.component || null;
        },
        contentProps() {
            return this.content?.props || {};
        },
    },
    methods: {
        ...mapActions("modal", ["closeModal"]),
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
