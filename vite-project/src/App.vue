<!-- App.vue -->
<template>
    <router-view></router-view>
    <Modal name="popup" delayEnter="1000" delayExit="500" />
    <Modal name="overlay" delayEnter="500" delayExit="500" />
    <Modal name="notice" />
    <!-- <button @click="openExampleModal">Open Popup</button> -->
</template>

<script>
import Modal from "./components/layout/Modal.vue";
import { mapActions } from "vuex";

const popup = "popup";
const overlay = "overlay";

export default {
    name: "App",
    components: { Modal },
    methods: {
        ...mapActions("modal", ["openModal"]),
        openExampleModal() {
            /* this.openModal({
                name: popup,
                component: "Popup", // name of registered component
                props: { message: "Hello, this is a popup!" },
            }); */
        },
    },
    props: {},
    data() {
        return {
            _: 0,
        };
    },
    mounted() {
        // console.log("LOGADO: ", this.$store.getters.getLogado);
    },
};
</script>

<style lang="scss">
$fonte-maior: 48px;
$fonte-secao: 32px;
$fonte-paragrafo-info: 20px;
$fonte-but-grande: 24px;
</style>
