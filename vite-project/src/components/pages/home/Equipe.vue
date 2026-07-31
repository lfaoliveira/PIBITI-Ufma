<template>
    <div class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <HeaderSistema :activeIndex="2"></HeaderSistema>

        <!-- TODO: BOTAR FOTOS DO POVO E PARTICIPAÇÃO -->

        <section
            v-for="(pessoa, index) in lista_dados"
            :key="index"
            :class="
                `flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` +
                ` ` +
                pessoa.tipo
            "
        >
            <div class="div-img">
                <img
                    class="w-[20rem] h-[22rem] object-cover"
                    :src="pessoa.img"
                    :alt="'Foto de ' + pessoa.nome"
                />
            </div>
            <div class="textos">
                <h1 class="nome">{{ pessoa.nome }}</h1>
                <h1 class="participacao">Participação:</h1>
                <p class="desc">{{ pessoa.descricao }}</p>
            </div>
        </section>

        <section class="flex flex-col items-center gap-5 w-full px-5">
            <h2 class="section-title" id="titulo-equipe">Equipe do NCA</h2>
            <div class="flex flex-col md:flex-row items-center gap-5 w-full">
                <p class="texto-secoes" id="team-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer
                    fringilla mi a lorem tincidunt imperdiet. Duis ac nisl pellentesque,
                    posuere dui eu, iaculis lectus. Curabitur vehicula nibh urna Morbi
                    vulputate magna id magna tempus volutpat. Duis metus elit, egestas id
                    lorem at, dictum sollicitudin nunc. Nunc a bibendum leo. Fusce
                    efficitur nibh a pretium feugiat. In at facilisis ante. Nullam id
                    velit sed dolor mattis fringilla. Aliquam id interdum lorem
                </p>
                <img
                    alt="Imagem Time do VipLab"
                    class="team-image"
                    src="../../../assets/Foto-NCA.png"
                />
            </div>
        </section>

        <Rodape></Rodape>
    </div>
    <!-- fim frame-pagina -->
</template>

<script>
import Rodape from "../../layout/Rodape.vue"
import HeaderSistema from "../../layout/HeaderSistema.vue"

export default {
    name: "autores",
    components: {
        HeaderSistema,
        Rodape,
    },
    created() {},
    data() {
        return {
            lista_dados: [
                {
                    nome: "Luis Felipe Araujo de Oliveira",
                    descricao: "Desenvolvedor Frontend e Backend da Aplicação",
                    tipo: "tipo2",
                    img: "src/assets/equipe/luis_felipe.png",
                },
                {
                    nome: "Prof. João Dalysson",
                    descricao: "Professor e Orientador do projeto de ppesquisa",
                    tipo: "tipo1",
                    img: "src/assets/equipe/dallyson.png",
                },
                {
                    nome: "Prof. Luis Rivero",
                    descricao: "Professor e UX Designer",
                    tipo: "tipo2",
                    img: "src/assets/equipe/luis_rivero.png",
                },
                {
                    nome: "Polyana Bezerra",
                    descricao:
                        "Pesquisadora principal na criação do método de diagnóstico automático da Paralisia",
                    tipo: "tipo1",
                    img: "src/assets/equipe/polyana.png",
                },
                {
                    nome: "Dr. Jorge",
                    descricao: "Médico pesquisador e Co-autor no projeto de pesquisa",
                    tipo: "tipo2",
                    img: "src/assets/equipe/jorge.png",
                },
            ],
        }
    },
    props: {},
    methods: {},
    mounted() {},
}
</script>

<style lang="scss" scoped>
.tipo1 {
    background-color: white;
    color: black;
}

.tipo2 {
    background: #6113c6;
    color: white;
}
</style>
