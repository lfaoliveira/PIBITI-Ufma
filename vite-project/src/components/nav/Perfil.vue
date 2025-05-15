<template>
  <main class="frame-pagina">
    <HeaderSistema :activeIndex="6"></HeaderSistema>
    <OverlayAviso
      :eventoAviso="'semLogin'"
      :titulo="'Sua sessão expirou'"
      :subtexto="'Faça Login novamente para acessar seus dados '"
      :srcImg="'src/assets/alert_circle.png'"
      :rota="'/acesso'"
    ></OverlayAviso>
    <section class="info">
      <img src="../../assets/generic_avatar.png" id="foto" />
      <div class="nome-crm">
        <p>Dr. {{ this.nomeMedico }}</p>
        <p>{{ this.crm }}</p>
      </div>
    </section>

    <section class="secao-tabela">
      <h1 v-if="temDiags">Análises Realizadas</h1>
      <h1 v-if="!temDiags">Não há diagnósticos</h1>
      <table v-if="temDiags">
        <thead>
          <tr class="header-row">
            <th class="cel-header" scope="col" v-for="string in header">{{ string }}</th>
          </tr>
        </thead>
        <tr v-for="(obj, index) in entradas">
          <td class="cel-dado" v-for="(valor, key) in obj">
            <template v-if="key === 'pdf'">
              <a @click="baixarRelatorio" :href="valor">Baixar</a>
            </template>
            <template v-else>
              {{ valor }}
            </template>
          </td>
          <td class="cel-acao">
            <button @click="fnEditar" class="but-acao" id="editar">
              <img src="../../assets/mdi_pencil-outline.png" />
            </button>

            <button @click="fnDeletar" class="but-acao" id="deletar">
              <img src="../../assets/mdi_trash.png" />
            </button>
          </td>
        </tr>
      </table>
      <div class="container-paginas">
        <nav class="paginas">
          <button @click="fnAtras" class="but-avancar">
            <img class="icone-avancar" src="../../assets/left_duo.png" />
          </button>

          <span class="numero-pagina">
            <p>{{ this.pagAtual }}</p>
            <p>de</p>
            <p>{{ this.maxPags }}</p>
          </span>

          <button @click="fnFrente" class="but-avancar">
            <img class="icone-avancar" src="../../assets/right_duo.png" />
          </button>
        </nav>
      </div>
    </section>
    <Rodape id="rodape"></Rodape>
  </main>
</template>

<script>
import HeaderSistema from "../auxiliares/HeaderSistema.vue";
import OverlayAviso from "../auxiliares/OverlayAviso.vue";
import Rodape from "../auxiliares/Rodape.vue";
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
      console.log("ERRO AO PEGAR PERFIL!");
    }
    this.entradas = this.ajustarEntradasTabela(res2.data.lista);
    this.nomeMedico = res2.data.nomeMedico;
    this.crm = res2.data.crm;
    console.log("ENTRADAS: ", this.entradas);
    this.maxPags = Math.ceil(this.entradas.length / this.maxItens_Pag);
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
      //pegar mais dados do BD
    },
    fnFrente() {
      //pegar mais dados do BD
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
  computed: {},
  data() {
    return {
      nomeMedico: "Médico",
      crm: "MA-12345",
      temDiags: true,
      pagAtual: 1,
      maxPags: "-", //esse aqui se pega do BD
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
.frame-pagina {
  @include frame-pagina($gap: 5vmin);
  height: 100vh;
  align-items: center;
}
.info {
  display: flex;
  gap: 3vmin;
  padding: 1vmin;
  align-self: stretch;
  align-items: center;

  height: max-content;
  #foto {
    aspect-ratio: 1/1;
    width: 12vmin;
    height: auto;
  }
  .nome-crm {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-direction: column;
    background: $sec-color;
    border-radius: 3vmin;
    width: clamp(20ch, 350px, 40ch);
    padding: 0.65lh 0.5lh;
    gap: 1vmin;

    color: white;
  }
}

.secao-tabela {
  display: flex;
  flex-flow: column;
  align-items: center;
  margin: 0px 20vmin;
  gap: 4vmin;
  table {
    width: 100%;
    border-collapse: collapse;
    border-bottom: 1px solid rgba(213, 213, 213, 0.5);
    border-right: 1px solid rgba(213, 213, 213, 0.5);
  }
  thead {
    border-top: 1px solid rgba(213, 213, 213, 0.5);
    border-left: 1px solid rgba(213, 213, 213, 0.5);
    background: #7133ab;
    color: white;
  }

  td,
  th {
    width: 500px;
    border-top: 1px solid rgba(213, 213, 213, 0.5);
    border-left: 1px solid rgba(213, 213, 213, 0.5);
    margin: none;
    a {
      &:hover {
        background: none;
        text-decoration: underline;
      }
    }
  }
  th {
    text-align: start;
  }
  .cel-acao {
    .but-acao {
      aspect-ratio: 1/1;
      width: 4.5vmin;
      background: none;
      cursor: pointer;
      &:hover,
      &:focus {
        background: #e4e4e4;
        border-radius: 3vmin;
      }
    }
    #editar {
      margin-right: 1vmin;
    }
  }
}

.container-paginas {
  display: flex;
  .paginas {
    display: flex;
    gap: 1vmin;
    align-items: center;

    .but-avancar {
      display: flex;
      align-items: center;
      padding: 0px;
      background: none;
      cursor: pointer;
      .icone-avancar {
        padding: 0px;
        aspect-ratio: 1/1;
        width: 4ch;
      }
    }

    .numero-pagina {
      p {
        font-weight: 600;
      }

      color: #525252;
      display: flex;
      align-items: center;
      height: min-content;
      gap: 0.5ch;
      width: max-content;
    }
  }
}
</style>
