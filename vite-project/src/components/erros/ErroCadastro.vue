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
        return null;
      }

      const arrayRet = func(string);
      const texto = arrayRet[0];
      const valor = arrayRet[1];

      if (valor == null) {
        this.texto = texto;
        const caixa = this.$refs.caixaErro;
        caixa.style.display = "unset";
      } else {
        this.handleSucess();
        alert(`VALOR: ${valor}`);
        console.log("SUCESSO: ", tipo);
        return valor;
      }
    },

    erroEmail(strEmail) {
      const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
      if (strEmail === "exemplo@email.com" || !emailRegex.test(strEmail)) {
        return ["Digite um email válido!", null];
      } else {
        return ["OK", strEmail];
      }
    },
    erroCPF(strCpf) {
      // Match CPF, permitindo traço, ponto e espaco na string
      const cpfRegex = /^(\d\s*){9}[-|\.]?\d{2}\s*$/g;

      const inval = "CPF inválido!";

      // Remove pontos e tracos
      strCpf = strCpf.replace(/\.|-|\s/g, "");

      console.log("INICIO CHECAGEM CPF");

      // cpf so pode ter 11 caracteres, depis do tratamento
      if (strCpf.length !== 11 || !cpfRegex.test(strCpf)) {
        console.log("CPF INVALIDO");
        return [inval, null];
      }

      //nao retirar!
      if (strCpf == "00000000000") return [inval, null];
      let Soma = 0;
      for (let i = 1; i <= 9; i++) {
        Soma = Soma + parseInt(strCpf.substring(i - 1, i)) * (11 - i);
      }

      let Resto = (Soma * 10) % 11;

      if (Resto == 10 || Resto == 11) Resto = 0;
      if (Resto != parseInt(strCpf.substring(9, 10))) return [inval, null];
      console.log("PRIMEIRO CHECK OK");

      Soma = 0;
      for (let i = 1; i <= 10; i++) {
        Soma = Soma + parseInt(strCpf.substring(i - 1, i)) * (12 - i);
      }
      Resto = (Soma * 10) % 11;
      if (Resto == 10 || Resto == 11) Resto = 0;
      if (Resto != parseInt(strCpf.substring(10, 11))) return [inval, null];
      console.log("SEGUNDO CHECK OK");
      return ["OK", strCpf];
    },
    erroCRM(strCrm) {
      // TODO: CRIAR LOGICA PARA LIDAR COM CRM
      // Placeholder for CRM validation
      return "";
    },
    erroChecks(strChecks) {
      const boolCheck = Boolean(strChecks);
      if (boolCheck === false) {
        return ["Aceite os Termos e Condições!", null];
      } else {
        return ["OK", boolCheck];
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
