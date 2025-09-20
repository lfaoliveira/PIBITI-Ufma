<template>
    <main class="flex flex-col items-center gap-[5vmin] h-screen">
        <HeaderSistema :activeIndex="6"></HeaderSistema>
        <OverlayAviso
            :eventoAviso="'semLogin'"
            :titulo="'Sua sessão expirou'"
            :subtexto="'Faça Login novamente para acessar seus dados '"
            :srcImg="'src/assets/alert_circle.png'"
            :rota="'/acesso'"
        ></OverlayAviso>

        <!-- Converted .info section to Tailwind classes -->
        <section class="flex gap-[3vmin] p-[1vmin] self-stretch items-center h-max">
            <img
                src="../../assets/generic_avatar.png"
                class="aspect-square w-[12vmin] h-auto"
            />
            <div
                class="flex items-start justify-center flex-col bg-purple-700 rounded-[3vmin] w-[clamp(20ch,350px,40ch)] px-[0.5lh] py-[0.65lh] gap-[1vmin] text-white"
            >
                <p>Dr. {{ this.nomeMedico }}</p>
                <p>{{ this.crm }}</p>
            </div>
        </section>

        <!-- Converted .secao-tabela section to Tailwind classes -->
        <section class="w-[95%] flex flex-col items-center mx-[20vmin] gap-[4vmin]">
            <h1 v-if="temDiags" class="text-2xl font-semibold">Análises Realizadas</h1>
            <h1 v-if="!temDiags" class="text-2xl font-semibold">Não há diagnósticos</h1>

            <table
                v-if="temDiags"
                class="w-full !border-b !border-r !border-l border-gray-300/50"
            >
                <thead
                    class=" !border-t !border-l border-gray-300/50 bg-purple-700 text-white"
                >
                    <tr>
                        <th
                            class="w-[500px] !border-t !border-l border-gray-300/50 text-left p-2"
                            scope="col"
                            v-for="string in header"
                        >
                            {{ string }}
                        </th>
                    </tr>
                </thead>
                <tbody class="border">
                    <tr
                        v-for="(obj, index) in paginatedEntradas"
                        class="!border-t border-gray-300/50"
                    >
                        <td
                            class="w-[500px] !border-t !border-l border-gray-300/50 p-2"
                            v-for="(valor, key) in obj"
                        >
                            <template v-if="key === 'pdf'">
                                <a
                                    @click="baixarRelatorio"
                                    :href="valor"
                                    class="hover:underline hover:bg-transparent"
                                    >Baixar</a
                                >   
                            </template>
                            <template v-else>
                                {{ valor }}
                            </template>
                        </td>
                        <td class="w-[500px] !border-t !border-l border-gray-300/50 p-2">
                            <button
                                @click="fnEditar"
                                class="aspect-square w-[4.5vmin] bg-transparent cursor-pointer hover:bg-gray-200 hover:rounded-[3vmin] focus:bg-gray-200 focus:rounded-[3vmin] mr-[1vmin]"
                            >
                                <img src="../../assets/mdi_pencil-outline.png" />
                            </button>

                            <button
                                @click="fnDeletar"
                                class="aspect-square w-[4.5vmin] bg-transparent cursor-pointer hover:bg-gray-200 hover:rounded-[3vmin] focus:bg-gray-200 focus:rounded-[3vmin]"
                            >
                                <img src="../../assets/mdi_trash.png" />
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Enhanced pagination controls with page numbers and better navigation -->
            <div class="flex" v-if="temDiags && totalPages > 1">
                <nav class="flex gap-[1vmin] items-center">
                    <!-- First page button -->
                    <button
                        @click="goToFirstPage"
                        :disabled="pagAtual === 1"
                        class="flex items-center p-2 bg-transparent cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 rounded"
                    >
                        <span class="text-sm">««</span>
                    </button>

                    <!-- Previous page button -->
                    <button
                        @click="fnAtras"
                        :disabled="pagAtual === 1"
                        class="flex items-center p-0 bg-transparent cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <img
                            class="p-0 aspect-square w-[4ch]"
                            src="../../assets/left_duo.png"
                        />
                    </button>

                    <!-- Page numbers -->
                    <div class="flex gap-1 mx-2">
                        <button
                            v-for="page in visiblePages"
                            :key="page"
                            @click="goToPage(page)"
                            :class="[
                                'px-3 py-1 text-sm rounded transition-colors',
                                page === pagAtual 
                                    ? 'bg-purple-700 text-white font-semibold' 
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            ]"
                        >
                            {{ page }}
                        </button>
                    </div>

                    <!-- Current page info -->
                    <!-- <span class="text-gray-600 flex items-center h-min gap-[0.5ch] w-max mx-2">
                        <p class="font-semibold">{{ this.pagAtual }}</p>
                        <p class="font-semibold">de</p>
                        <p class="font-semibold">{{ totalPages }}</p>
                    </span> -->

                    <!-- Next page button -->
                    <button
                        @click="fnFrente"
                        :disabled="pagAtual === totalPages"
                        class="flex items-center p-0 bg-transparent cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <img
                            class="p-0 aspect-square w-[4ch]"
                            src="../../assets/right_duo.png"
                        />
                    </button>

                    <!-- Last page button -->
                    <button
                        @click="goToLastPage"
                        :disabled="pagAtual === totalPages"
                        class="flex items-center p-2 bg-transparent cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 rounded"
                    >
                        <span class="text-sm">»»</span>
                    </button>
                </nav>
            </div>

            <!-- Items per page selector -->
            <div class="flex items-center gap-2" v-if="temDiags">
                <label class="text-sm text-gray-600">Itens por página:</label>
                <select 
                    v-model="itemsPerPage" 
                    @change="changeItemsPerPage"
                    class="px-2 py-1 border border-gray-300 rounded text-sm"
                >
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                </select>
                <span class="text-sm text-gray-600">
                    Mostrando {{ startItem }} - {{ endItem }} de {{ totalItems }} itens
                </span>
            </div>
        </section>

        <Rodape class="mt-auto"></Rodape>
    </main>
</template>

<script>
import HeaderSistema from "../layout/HeaderSistema.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";
import Rodape from "../layout/Rodape.vue";
import emitter from "../../eventBus";
import axios from "axios";

export default {
    name: "Perfil_comp",
    components: {
        HeaderSistema,
        Rodape,
        OverlayAviso,
    },
    created() {},
    async mounted() {
        console.log("MONTADO PERFIL");
        if (!this.$store.getters.getLogado) {
            emitter.emit("semLogin");
        }
        let res2;
        try {
            res2 = await axios.get(this.$store.getters.getPerfil, {
                params: { pagAtual: this.pagAtual },
                withCredentials: true,
            });
        } catch (e) {
            if (e.response.status == 401) {
                this.ajustarEntradasTabela([]);
            }
            console.log("ERRO AO PEGAR PERFIL!");
        }
        this.entradas = this.ajustarEntradasTabela(res2.data.lista);
        this.nomeMedico = res2.data.nomeMedico;
        this.crm = res2.data.crm;
        this.maxItens_Pag = parseInt(res2.data.maxItensPag);
        console.log("ENTRADAS: ", this.entradas);
        console.log("LENGTH: ", this.entradas.length);
        this.maxPags = Math.ceil(parseInt(this.entradas.length) / this.maxItens_Pag);
    },
    methods: {
        baixarRelatorio(evt) {
            console.log(evt.target.href);
        },
        fnEditar() {
            //codigo de acao
        },
        fnDeletar() {
            //codigo de acao
        },
        fnAtras() {
            if (this.pagAtual > 1) {
                this.pagAtual--;
            }
        },
        fnFrente() {
            if (this.pagAtual < this.totalPages) {
                this.pagAtual++;
            }
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.pagAtual = page;
            }
        },
        goToFirstPage() {
            this.pagAtual = 1;
        },
        goToLastPage() {
            this.pagAtual = this.totalPages;
        },
        changeItemsPerPage() {
            this.pagAtual = 1; // Reset to first page when changing items per page
        },
        ajustarEntradasTabela(list) {
            let key;
            let copy = Array();
            let novoObj;

            for (let i = 0; i < list.length; ++i) {
                let obj = list[i];
                novoObj = new Object();
                Object.entries(obj).forEach((pair) => {
                    key = pair[0];
                    //se header tem
                    if (Object.hasOwn(this.header, key)) {
                        if (pair[1] == "") pair[1] = "-";
                        if (key === "dataDiag" || key === "ultimaModif") {
                            // OBS: Date RECEBE TEMPO EM ms, logo multplica tempo UNIX em mil
                            pair[1] = new Date(pair[1] * 1000).toLocaleString("pt-BR", {
                                day: "2-digit",
                                month: "2-digit",
                                year: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                            });
                        } else if (key === "diagnosticoMedico" || key === "diagAutom") {
                            let valor = String(pair[1]).split("+");
                            const esq = valor[0];
                            const dir = valor[1];
                            if (esq == "false" && dir == "false") {
                                pair[1] = "Saudável";
                            } else if (esq == "true" && dir === "true") {
                                pair[1] = "Paralisia em Ambos Olhos";
                            } else {
                                if (esq == "true") {
                                    pair[1] = "Paralisia no Olho Esquerdo";
                                } else {
                                    pair[1] = "Paralisia no Olho Direito";
                                }
                            }
                        }

                        novoObj[key] = pair[1];
                    }
                });
                // Reorder novoObj based on header keys
                const orderedObj = {};
                Object.keys(this.header).forEach((key) => {
                    if (novoObj.hasOwnProperty(key)) {
                        orderedObj[key] = novoObj[key];
                    }
                });
                novoObj = orderedObj;
                copy.push(novoObj);
            }
            //ordena com base na data de diagnostico
            return copy.sort((a, b) => {
                return Date.parse(a.dataDiag) - Date.parse(b.dataDiag);
            });
        },
    },
    computed: {
        totalItems() {
            return this.entradas.length;
        },
        totalPages() {
            return Math.ceil(this.totalItems / this.itemsPerPage);
        },
        paginatedEntradas() {
            const start = (this.pagAtual - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.entradas.slice(start, end);
        },
        visiblePages() {
            const pages = [];
            const maxVisible = 5;
            let start = Math.max(1, this.pagAtual - Math.floor(maxVisible / 2));
            let end = Math.min(this.totalPages, start + maxVisible - 1);
            
            // Adjust start if we're near the end
            if (end - start + 1 < maxVisible) {
                start = Math.max(1, end - maxVisible + 1);
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
        startItem() {
            return this.totalItems === 0 ? 0 : (this.pagAtual - 1) * this.itemsPerPage + 1;
        },
        endItem() {
            return Math.min(this.pagAtual * this.itemsPerPage, this.totalItems);
        }
    },
    data() {
        return {
            nomeMedico: "Médico",
            crm: "MA-12345",
            temDiags: true,
            pagAtual: 1,
            itemsPerPage: 10, // Default items per page
            maxPags: "1", // Keep for backward compatibility
            header: {
                nomePaciente: "Paciente",
                diagnosticoMedico: "Diagnóstico Médico",
                diagAutom: "Diagnóstico Automatizado",
                desc: "Descrição",
                dataDiag: "Data de Diagnóstico",
                ultimaModif: "Última Modificação",
                pdf: "Relatório",
                acoes: "Ações",
            },
            entradas: [
                {
                    nomePaciente: "-",
                    diagMedico: "-",
                    diagAutom: "-",
                    desc: "-",
                    dataDiag: "-",
                    ultimaModif: "-",
                    pdf: "-",
                },
                {
                    nomePaciente: "-",
                    diagMedico: "-",
                    diagAutom: "-",
                    desc: "-",
                    dataDiag: "-",
                    ultimaModif: "-",
                    pdf: "-",
                },
            ],
        };
    },
    props: {},
};
</script>

<style lang="scss" scoped>
// .frame-pagina {
//     @include frame-pagina($gap: 5vmin);
//     height: 100vh;
//     align-items: center;
// }


// .info {
//   display: flex;
//   gap: 3vmin;
//   padding: 1vmin;
//   align-self: stretch;
//   align-items: center;

//   height: max-content;
//   #foto {
//     aspect-ratio: 1/1;
//     width: 12vmin;
//     height: auto;
//   }
//   .nome-crm {
//     display: flex;
//     align-items: flex-start;
//     justify-content: center;
//     flex-direction: column;
//     background: $sec-color;
//     border-radius: 3vmin;
//     width: clamp(20ch, 350px, 40ch);
//     padding: 0.65lh 0.5lh;
//     gap: 1vmin;

//     color: white;
//   }
// }

// .secao-tabela {
//   display: flex;
//   flex-flow: column;
//   align-items: center;
//   margin: 0px 20vmin;
//   gap: 4vmin;
//   table {
//     width: 100%;
//     border-collapse: collapse;
//     border-bottom: 1px solid rgba(213, 213, 213, 0.5);
//     border-right: 1px solid rgba(213, 213, 213, 0.5);
//   }
//   thead {
//     border-top: 1px solid rgba(213, 213, 213, 0.5);
//     border-left: 1px solid rgba(213, 213, 213, 0.5);
//     background: #7133ab;
//     color: white;
//   }

//   td,
//   th {
//     width: 500px;
//     border-top: 1px solid rgba(213, 213, 213, 0.5);
//     border-left: 1px solid rgba(213, 213, 213, 0.5);
//     margin: none;
//     a {
//       &:hover {
//         background: none;
//         text-decoration: underline;
//       }
//     }
//   }
//   th {
//     text-align: start;
//   }
//   .cel-acao {
//     .but-acao {
//       aspect-ratio: 1/1;
//       width: 4.5vmin;
//       background: none;
//       cursor: pointer;
//       &:hover,
//       &:focus {
//         background: #e4e4e4;
//         border-radius: 3vmin;
//       }
//     }
//     #editar {
//       margin-right: 1vmin;
//     }
//   }
// }

// .container-paginas {
//   display: flex;
//   .paginas {
//     display: flex;
//     gap: 1vmin;
//     align-items: center;

//     .but-avancar {
//       display: flex;
//       align-items: center;
//       padding: 0px;
//       background: none;
//       cursor: pointer;
//       .icone-avancar {
//         padding: 0px;
//         aspect-ratio: 1/1;
//         width: 4ch;
//       }
//     }

//     .numero-pagina {
//       p {
//         font-weight: 600;
//       }

//       color: #525252;
//       display: flex;
//       align-items: center;
//       height: min-content;
//       gap: 0.5ch;
//       width: max-content;
//     }
//   }
// }
</style>
