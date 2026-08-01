<template>
    <div class="flex w-full text-white">
        <button
            :type="type"
            @click="handleClick"
            v-if="ativo == true"
            class="botao-acao classeAtivo"
            enabled
        >
            {{ texto }}
        </button>
        <button :type="type" v-if="ativo == false" class="botao-acao text classeInativo" disabled>
            {{ texto }}
        </button>
    </div>
</template>

<script>
export default {
    name: "botao",
    methods: {
        handleClick() {
            this.$emit("click");
            if (this.type == "submit") {
                this.$emit("submit");
            }
        },
    },
    props: {
        ativo: true,
        texto: "",
        type: "button",
    },
    created() {},
    mounted() {
        // console.log("ATIVO PEQUNO: ", this.ativo);
    },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind - usando classes .botao-acao do style.css global */
</style>
