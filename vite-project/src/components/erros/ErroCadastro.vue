<script>
import { ref } from "vue";

export default {
  name: "CadComp",
  created() {
    /* document.addEventListener("cadastroCerto", () => {
      console.log(this.tipo + " OK");
    }); */
  },
  data() {
    return {
      cont: 0,
      texto: "",
      tipo: null,
    };
  },
  mounted() {
    console.log("MOUNTED ERROS");
  },
  props: {},
  methods: {
    checkErro(tipo, string) {
      const dict_tipo = {
        email: this.erroEmail,
        cpf: this.erroCPF,
        crm: this.erroCRM,
        checks: this.erroChecks,
      };
      const func = dict_tipo[tipo];

      if (typeof func !== "function") {
        console.error(`Handler for type "${tipo}" is not defined`);
        return;
      }

      const retorno = func(string);
      if (retorno == "OK") {
        this.handleSucess();
        console.log("SUCESSO: ");
      } else {
        this.texto = retorno;
        const caixa = this.$refs.caixaErro;
        caixa.style.display = "unset";
        console.log("TIPO ERRO: ");
      }
    },
    handleErro(tipo) {
      console.log("ERRO AQUI");
      this.tipo = tipo;
      if (tipo === "checks") {
        this.texto = "Aceite os Termos e Condições!";
      } else {
        this.texto = retorno;
      }
    },

    erroEmail(strEmail) {
      const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
      if (strEmail === "exemplo@email.com" || !emailRegex.test(strEmail)) {
        return "Digite um email válido!";
      } else {
        return "OK";
      }
    },
    erroCPF(strCpf) {
      // Match CPF, permitindo 1 ou 0 traços
      const cpfRegex = /^[\d]{9}-?[\d]{2}$/;

      const inval = "CPF inválido!";

      // cpf so pode ter 11 ou 12 caracteres
      if (strCpf.length !== 11 || strCpf.length !== 12 || !cpfRegex.test(strCpf)) {
        return inval;
      }

      if (strCPF == "00000000000") return inval;

      for (i = 1; i <= 9; i++) {
        Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (11 - i);
      }

      Resto = (Soma * 10) % 11;

      if (Resto == 10 || Resto == 11) Resto = 0;
      if (Resto != parseInt(strCPF.substring(9, 10))) return inval;

      Soma = 0;
      for (i = 1; i <= 10; i++) {
        Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (12 - i);
      }
      Resto = (Soma * 10) % 11;
      if (Resto == 10 || Resto == 11) Resto = 0;
      if (Resto != parseInt(strCPF.substring(10, 11))) return inval;

      return "OK";
    },
    erroCRM(strCrm) {
      // TODO: CRIAR LOGICA PARA LIDAR COM CRM
      // Placeholder for CRM validation
      return "";
    },
    erroChecks(strChecks) {
      if (Boolean(strChecks) === false) {
        return "Aceite os Termos e Condições!";
      } else {
        return "OK";
      }
    },
    handleSucess() {
      const caixa = this.$refs.caixaErro;
      caixa.style.display = "none";
      this.texto = "adadaw";
    },
  },
};
</script>

<style lang="scss" scoped>
* {
  box-sizing: content-box;
}

.erro {
  width: 100%;
  height: 50px;
  background-color: white;
  color: red;
  display: none;
}
</style>

<template>
  <div
    class="erro"
    ref="caixaErro"
    @erroCadastro="handleErro"
    @cadastroCerto="handleSucess"
  >
    {{ this.texto }}
  </div>
</template>
