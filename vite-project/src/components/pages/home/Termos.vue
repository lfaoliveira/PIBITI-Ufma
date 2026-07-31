<template>
    <div class="flex flex-col items-center gap-[2vmin] max-[500px]:gap-[1vmin] h-max">
        <HeaderSistema tipo="outro" />
        <h1 class="text-center">Termos e Condições</h1>
        <main class="border border-black w-[90%] self-center flex flex-col justify-start items-center overflow-auto h-[50vmin]">
            <h1>Título dos Termos e Condições</h1>
            <ol class="flex flex-col w-full px-[4vmin] items-start list-decimal">
                <li class="flex flex-col justify-center items-center" v-for="(obj, index) in termos">
                    <h2>{{ `${index + 1}. ${obj.titulo}` }}</h2>
                    <p>{{ obj.p }}</p>
                </li>
            </ol>
        </main>
    </div>
</template>

<script>
import HeaderSistema from "../../layout/HeaderSistema.vue";

export default {
    name: "termosComp",
    components: {
        HeaderSistema,
    },
    created() {},
    data() {
        return {
            termos: [
                { titulo: "a", p: "a1" },
                { titulo: "b", p: "a2" },
                { titulo: "c", p: "a3" },
                { titulo: "d", p: "a4" },
                { titulo: "e", p: "a5" },
                { titulo: "a", p: "a1" },
                { titulo: "b", p: "a2" },
                { titulo: "c", p: "a3" },
                { titulo: "d", p: "a4" },
                { titulo: "e", p: "a5" },
            ],
        };
    },
    props: {},
    methods: {
        fnVoltar() {
            this.$router.push({ name: "cad" });
        },
    },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
