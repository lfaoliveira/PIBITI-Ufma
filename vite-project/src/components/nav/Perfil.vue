<template>
  <main class="frame-pagina">
    <HeaderSistema :activeIndex="6"></HeaderSistema>
    <section class="info">
      <img src="../../assets/generic_avatar.png" id="foto" />
      <div class="nome-crm">
        <p>Dr. {{ this.nomeMedico }}</p>
        <p>{{ this.crm }}</p>
      </div>
    </section>

    <section class="secao-tabela">
      <h1>Análises Realizadas</h1>
      <table v-if="temDiags">
        <thead>
          <tr class="header-row">
            <th class="cel-header" scope="col" v-for="string in header">{{ string }}</th>
          </tr>
        </thead>
        <tr v-for="(obj, index) in entradas">
          <td class="cel-dado" v-for="(valor, key) in obj">
            <template v-if="key === 'linkRelatorio'">
              <a :href="valor">Baixar</a>
            </template>
            <template v-else>
              {{ valor }}
            </template>
          </td>
          <td class="cel-acao">
            <button class="but-acao">
              <img src="" />
            </button>

            <button class="but-acao">
              <img src="" />
            </button>
          </td>
        </tr>
      </table>
      <div class="container-paginas">
        <nav class="paginas">
          <button class="but-avancar">
            <img class="icone-avancar" src="../../assets/left_duo.png" />
          </button>

          <span class="numero-pagina">
            <p>{{ this.pagAtual }}</p>
            <p>de</p>
            <p>{{ this.maxPags }}</p>
          </span>

          <button class="but-avancar">
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
import Rodape from "../auxiliares/Rodape.vue";

export default {
  name: "Perfil_comp",
  components: {
    HeaderSistema,
    Rodape,
  },
  created() {},
  data() {
    return {
      nomeMedico: "Fulano de Siclano",
      crm: "MA-666666",
      temDiags: true,
      pagAtual: 1,
      maxPags: "-", //esse aqui se pega do BD
      header: [
        "Paciente",
        "Diagnóstico",
        "Diagnóstico Automatizado",
        "Descrição",
        "Data de Diagnóstico",
        "Última Modificação",
        "Relatório",
        "Ações",
      ],
      entradas: [
        {
          nomePaciente: "adawda",
          diagMedico: "adawda",
          diagAutom: "adawda",
          desc: "adawda",
          dataDiag: "adawda",
          ultimaModif: "adawda",
          linkRelatorio: "adawda",
        },
        {
          nomePaciente: "wewewewe",
          diagMedico: "wewewewe",
          diagAutom: "wewewewe",
          desc: "wewewewe",
          dataDiag: "wewewewe",
          ultimaModif: "wewewewe",
          linkRelatorio: "wewewewe",
        },
      ],
    };
  },
  props: {},
  methods: {},
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
      color: #676666;
      display: flex;
      align-items: center;
      height: min-content;
      gap: 0.5ch;
      width: max-content;
    }
  }
}
</style>
