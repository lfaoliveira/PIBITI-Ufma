<template>
    <a
        class="flex items-center justify-end gap-3 w-full text-white text-xs sm:text-sm font-medium py-2 px-3 rounded-lg hover:bg-white/10 transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
        :href="urlPDF"
        :disabled="butDisabled"
    >
        <span>Baixar Resultado</span>
        <img class="w-5 h-5" alt="Save icon" src="../../assets/download.png" />
    </a>
</template>

<script>
export default {
    name: "salvar",
    created() {},
    data() {
        return {}
    },
    mounted() {
        this.$el.addEventListener("click", (event) => {
            if (event.target.closest(".salvar")) {
                console.log("Salvar element clicked")
            }
        })
    },
    props: {
        modo: "off",
        urlPDF: null,
    },
    methods: {},
    computed: {
        butDisabled() {
            return this.modo == "off"
        },
    },
}
</script>
