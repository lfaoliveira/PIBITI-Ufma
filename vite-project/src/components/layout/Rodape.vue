<template>
    <footer
        class="inline-flex flex-col justify-center items-center self-end w-full gap-5 pb-[1vmin] mb-40"
    >
        <ul
            class="flex justify-center items-start gap-[10vmin] self-stretch p-[1vmin_0.5vmin_0_0]"
        >
            <a
                class="w-auto h-auto hover:bg-transparent"
                href="https://sigaa.ufma.br/sigaa/public/departamento/secao_extra.jsf?lc=pt_BR&id=998&extra=208953677"
                target="_blank"
            >
                <img
                    src="../../assets/logo_VIP_Lab.png"
                    alt="Logo footer"
                    id="logo-vip"
                    class="w-[125.189px] aspect-[125.19/88.34] m-0"
                />
            </a>
            <a
                class="w-auto h-auto hover:bg-transparent"
                href="https://portalpadrao.ufma.br/site"
                target="_blank"
            >
                <img
                    src="../../assets/logo ufma.png"
                    alt="Logo footer"
                    id="logo-ufma"
                    class="w-[88.336px] aspect-square m-0"
                />
            </a>
            <a
                class="w-auto h-auto hover:bg-transparent"
                href="https://anselmopaiva.github.io/"
                target="_blank"
            >
                <img
                    src="../../assets/LogoNCAFundBranco2000_2021.png"
                    alt="Logo footer"
                    id="logo-nca"
                    class="w-[113.542px] aspect-[113.54/88.34] m-0"
                />
            </a>
        </ul>
        <nav class="flex justify-center items-center gap-[6vmin] self-stretch w-full">
            <a
                href="mailto:viplab.psno@nca.ufma.br"
                class="text-black font-bold text-sm font-montserrat no-underline hover:bg-[#7f8084] hover:text-black"
                >Suporte</a
            >
            <a
                href="/termos"
                target="_blank"
                class="text-black font-bold text-sm font-montserrat no-underline hover:bg-[#7f8084] hover:text-black"
                >Termos e Condições</a
            >
            <a
                href="/duvidas"
                target="_blank"
                class="text-black font-bold text-sm font-montserrat no-underline hover:bg-[#7f8084] hover:text-black"
                >Sobre</a
            >
        </nav>
    </footer>
</template>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>

<script>
export default {
    name: "Rodape",
    data() {
        return {}
    },
    mounted() {},
    props: {
        margemImagem: { type: String, default: "20px" },
    },
    methods: {},
}
</script>
