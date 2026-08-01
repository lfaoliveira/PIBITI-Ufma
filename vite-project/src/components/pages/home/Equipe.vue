<template>
    <div class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <HeaderSistema :activeIndex="2"></HeaderSistema>

        <div
            class="grid grid-cols-1 xl:grid-cols-6 gap-[clamp(10px,2vmin,20px)] w-full px-6 h-full"
        >
            <section
                v-for="(pessoa, index) in lista_dados"
                :key="index"
                :class="[
                    index < 3
                        ? 'sm:col-span-1 lg:col-span-2'
                        : 'sm:col-span-1 lg:col-span-3',
                    'flex flex-col sm:flex-row gap-[clamp(8px,1.5vmin,16px)] justify-center w-full items-center p-1 sm:p-8',
                    pessoa.tipo,
                ]"
            >
                <div class="flex flex-col gap-3 text-center sm:text-left">
                    <h1 class="text-lg sm:text-xl font-bold">{{ pessoa.nome }}</h1>
                    <div class="shrink-0 flex justify-center sm:justify-start">
                        <img
                            class="w-48 h-56 sm:w-56 sm:h-64 lg:w-[15rem] lg:h-[15rem] object-cover"
                            :src="pessoa.img"
                            :alt="'Foto de ' + pessoa.nome"
                        />
                    </div>
                    <div class="flex flex-col gap-[1.5vmin]">
                        <h2 class="text-sm sm:text-base font-semibold">Participação:</h2>
                        <p class="text-sm sm:text-base leading-relaxed">
                            {{ pessoa.descricao }}
                        </p>
                    </div>
                </div>
            </section>
        </div>

        <section class="flex flex-col items-center gap-5 w-full px-4 sm:px-5">
            <h2 class="text-xl sm:text-2xl font-bold text-center" id="titulo-equipe">
                Equipe do NCA
            </h2>
            <div class="flex flex-col items-center gap-5 w-full max-w-6xl">
                <p
                    class="w-full text-sm sm:text-base leading-relaxed text-justify"
                    id="team-description"
                >
                    O Núcleo de Computação Aplicada (NCA) da Universidade Federal do
                    Maranhão (UFMA) desempenha um papel estratégico no desenvolvimento de
                    pesquisas e soluções tecnológicas voltadas à resolução de problemas
                    complexos da sociedade. Reunindo especialistas em Inteligência
                    Artificial, Visão Computacional, Processamento de Imagens, Ciência de
                    Dados, Engenharia de Software e Realidade Virtual, o núcleo desenvolve
                    tecnologias de ponta com aplicações em diferentes áreas, destacando-se
                    a saúde. Nesse contexto, o NCA contribui significativamente para o
                    avanço de sistemas inteligentes de apoio ao diagnóstico automatizado
                    de doenças, utilizando algoritmos de aprendizado de máquina e
                    processamento de imagens médicas para aumentar a precisão, a rapidez e
                    a confiabilidade das análises clínicas. Além de impulsionar a inovação
                    científica, o núcleo promove a formação de recursos humanos altamente
                    qualificados e fortalece a integração entre universidade, setor
                    produtivo e instituições públicas, consolidando-se como um centro de
                    excelência em pesquisa, desenvolvimento e inovação tecnológica.
                </p>
                <img
                    alt="Imagem Time do VipLab"
                    class="w-full lg:w-auto max-w-2xl h-auto object-contain"
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
                    descricao: "Professor e Orientador do projeto de pesquisa",
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
    background-color: var(--cor-paleta4);
    color: white;
    border: 1px solid var(--cor-paleta3);
}

.tipo2 {
    background: #6113c6;
    color: white;
}

@media (max-width: 640px) {
    .tipo1,
    .tipo2 {
        border-radius: 0.75rem;
    }
}
</style>
