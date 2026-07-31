<template>
    <a
        class="inline-flex flex-row items-center justify-center w-fit gap-[1vmin] m-[0.5vmin] cursor-pointer p-0 text-white font-medium no-underline transition-all duration-300 text-[clamp(13px,1.8vmin,20px)] text-center hover:bg-[hsla(267,81%,37%,0.63)] hover:font-semibold hover:scale-110 disabled:opacity-50 disabled:cursor-default disabled:hover:scale-90"
        :href="urlPDF"
        :disabled="butDisabled"
    >
        <img
            class="w-12 aspect-square p-[0.5vmin]"
            alt="Save icon"
            src="../../assets/download.png"
        />
        <div class="flex w-fit m-auto text-white font-bold underline">
            Baixar Resultado
        </div>
    </a>
</template>

<script>
export default {
    name: "salvar",
    created() {},
    data() {
        return {};
    },
    mounted() {
        this.$el.addEventListener("click", (event) => {
            if (event.target.closest(".salvar")) {
                console.log("Salvar element clicked");
            }
        });
    },
    props: {
        modo: "off",
        urlPDF: null,
    },
    methods: {},
    computed: {
        butDisabled() {
            return this.modo == "off";
        },
    },
};
</script>
