<template>
  <main class="frame-pagina">
    <HeaderSistema :activeIndex="6"></HeaderSistema>
    <section class="info">
      <img />
      <div class="nome-crm">
        <p></p>
        <p></p>
      </div>
    </section>

    <section class="secao-tabela">
      <h1>Análises Realizadas</h1>
      <table>
        <th v-for="(string, index) in header">
        <td class="cel-header">{{ string }}</td>
        </th>
        <tr v-for="(obj, index) in entradas">
          <td class="cel-dado"></td>
          <td class="cel-acao"></td>
        </tr>
      </table>
      <div class="container-paginas">
        <nav class="paginas">
          <button class="icone-avancar">
            <img class="icone-avancar" />
          </button>

          <span class="numero-pagina">
            <p>{{}} de</p>
            <p>{{}}</p>
          </span>

          <button class="icone-avancar">
            <img class="icone-avancar" />
          </button>
        </nav>
      </div>
    </section>
    <Rodape></Rodape>
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
  props: {
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
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.frame-pagina {
  @include frame-pagina($gap: 5vmin);
  height: 100vh;
}
</style>
