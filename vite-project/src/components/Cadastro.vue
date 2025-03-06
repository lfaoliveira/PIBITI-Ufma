<template>
  <section class="main-section">
    <header class="div-header">
      <Voltar class="seta" :onclick="fnVoltar"></Voltar>
    </header>
    <main class="content-area">
      <div class="registration-box">
        <h1 class="titulo-cad">Cadastre-se</h1>

        <form class="registration-form" @submit.prevent="cadastro">
          <div class="form-group">
            <label>Email</label>
            <input type="text" v-model="this.email" placeholder="exemplo@email.com" />
          </div>
          <ErroCadastro ref="erro1"></ErroCadastro>

          <div class="form-group">
            <label>CPF</label>
            <input type="text" v-model="this.cpf" placeholder="Digite seu CPF" />
          </div>
          <ErroCadastro ref="erro2"></ErroCadastro>

          <div class="form-group">
            <label>CRM (opcional)</label>
            <input type="text" v-model="this.crm" placeholder="Apenas oftalmologistas" />
          </div>
          <ErroCadastro ref="erro3"></ErroCadastro>

          <div class="terms">
            <input type="checkbox" v-model="this.checks" id="terms" />
            <label for="terms">Concordo com os Termos e Condições</label>
          </div>
          <ErroCadastro ref="erro4"></ErroCadastro>

          <button type="submit" class="register-button">Registrar</button>
        </form>
      </div>
      <div></div>
    </main>
    <Rodape class="rodape" margem-imagem="clamp(2px, 2vmin, 10px)"></Rodape>
  </section>
</template>

<style lang="scss" scoped>
* {
  --alt-butao: clamp(40px, 5vmin, 77px);
  --raio-butao: clamp(10px, 40%, 20px);
  font-family: "Montserrat", "Inter";
  border: 0px;
}

.main-section {
  height: fit-content;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.div-header {
  max-width: 95%;
  position: absolute;
  margin: 1vmin 0px 0px 0px;
  height: auto;
  width: clamp(90vmin, 85%, 95%);
  z-index: 1;
  display: flex;
  align-items: center;
}

.content-area {
  width: 50%;
  align-self: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.registration-box {
  padding: 4%;
  width: clamp(200px, 75%, 95%);
  margin: 2vmin;
  background: white;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.titulo-cad {
  font-size: clamp(25px, 5vmin, 48px);
  font-weight: 800;
  text-align: center;
  color: #333;
  margin-bottom: 10px;
}

.registration-form {
  margin: 2vmin;
  .form-group {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      color: #333;
    }

    input {
      width: 100%;
      padding: 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 16px;

      &:focus {
        outline: none;
        border-color: #007bff;
      }
    }
  }

  .terms {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    gap: 8px;

    input[type="checkbox"] {
      width: 18px;
      height: 18px;
      accent-color: #2c2c2c;
    }

    label {
      color: #666;
    }
  }

  .register-button {
    width: 100%;
    padding: 14px;
    background-color: var(--sec-color);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #23064a;
    }
  }
}

.rodape {
  align-self: center;
  margin-top: 2vmin;
}
</style>

<script>
import Voltar from "./icons/Voltar.vue";
import Rodape from "./Rodape.vue";
import ErroCadastro from "./erros/ErroCadastro.vue";
import { VueElement } from "vue";

export default {
  components: {
    Voltar,
    Rodape,
    ErroCadastro,
  },
  name: "cadatroComp",
  created() {},
  data() {
    return {
      email: "",
      cpf: "",
      crm: "",
      checks: false,
    };
  },
  mounted() {
    console.log("MOUNTED CADASTRO");
  },
  props: {},
  methods: {
    fnVoltar() {
      this.$router.push({ name: "home" });
    },
    handleTipoErro(str = String, referencia = VueElement, tipo = String) {
      const resposta = referencia.checkErro(tipo.toLowerCase(), str);
    },
    cadastro($evt) {
      console.log("AQUI");
      this.handleTipoErro(this.email, this.$refs.erro1, "Email");
      this.handleTipoErro(this.cpf, this.$refs.erro2, "CPF");
      this.handleTipoErro(this.crm, this.$refs.erro3, "CRM");

      const referencia = this.$refs.erro4;
      referencia.checkErro("checks", this.checks);
      console.log("FIM CADASTRO");
    },
  },
};
</script>
