<!-- App.vue -->
<template>
    <router-view></router-view>
    <Modal />
</template>

<script>
import Modal from "./components/layout/Modal.vue";

export default {
    name: "App",
    components: { Modal },
    methods: {},
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
