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
        <button :type="type" v-if="ativo == false" class="botao-acao classeInativo" disabled>
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


// .button-container {
//     @include container-botoes;
//     .button {
//         @include botao-acao($escala: 1.05, $height: $alt-botao);
//         font-weight: $peso-fonte-butao;
//         font-size: $fonte-but-medio;
//         color: white;
//     }
// }
</style>
