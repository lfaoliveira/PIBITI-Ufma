<template>
  <section class="frame-pagina">
    <HeaderSistema tipo="default"></HeaderSistema>
    <main>
      <section v-if="tipo === 'login'" class="login">
        <h1>Fazer Login</h1>
        <form @submit.prevent="valAcesso">
          <div class="form-group">
            <label>Email</label>
            <input type="text" v-model="this.email" placeholder="exemplo@email.com" />
          </div>
          <div class="form-group">
            <label>Senha</label>
            <input type="text" v-model="this.senha" placeholder="" />
          </div>

          <p>
            Não Possui Login?
            <a @click="fnTermos">Fazer Cadastro</a>
          </p>

          <ButtonMedio :type="submit" :ativo="true" texto="Fazer Login"></ButtonMedio>
        </form>
      </section>

      <section v-if="tipo === 'cadastro'"></section>

      <figure class="linha"></figure>

      <section class="avulsa">
        <h1>Análise Avulsa</h1>
        <div class="div-termos-label">
          <input type="checkbox" v-model="this.checks" id="checkTermos" />
          <label id="termos-label" for="checkTermos"
            >Concordo com os
            <a href="/termos" id="link-termos">Termos e Condições</a>
          </label>
        </div>
        <ButtonMedio :ativo="true" texto="Análise Avulsa"></ButtonMedio>
      </section>
    </main>
    <Rodape></Rodape>
  </section>
</template>

<script>
import HeaderSistema from "./analise/HeaderSistema.vue";
import ButtonMedio from "./auxiliares/ButtonMedio.vue";
import Rodape from "./auxiliares/Rodape.vue";

const def = "default";
const off = "salvaroff";
const on = "salvar";
const outro = "outro";

export default {
  name: "acesso",
  components: {
    HeaderSistema,
    Rodape,
    ButtonMedio,
  },
  created() {},
  data() {
    return {
      tipo: "login",
      email: "",
      senha: "",
      checks: false,
    };
  },
  props: {},
  methods: {
    valAcesso($evt) {
      console.log(this.email, this.senha);
    },
    fnTermos() {
      this.$router.push("/termos");
    },
  },
};
</script>

<style lang="scss" scoped>
.frame-pagina {
  @include frame-pagina($gap: 60px);
  height: max-content;
}

main {
  width: 60%;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex: 1 0 0;
}
a {
  color: $terc-color;
  font-weight: 500;
  cursor: pointer;
  &:hover {
    background: none;

    color: $terc-color;
    text-decoration: underline;
  }
}

.div-termos-label {
  display: flex;
  gap: 1vmin;
  #link-termos {
    font-weight: bold;
  }
}

#checkTermos::selection {
  color: red;
}

form {
  display: flex;
  flex-direction: column;
  gap: 2vmin;
  width: 100%;
}

.login {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1vmin;

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;

    label {
      font-size: $form-fonte-titulo;
    }

    input {
      width: 100%;
      padding: 1%;
      height: 2lh;
      font-size: $form-fonte-peq;
      border: 2px solid #b3b3b3;
      border-radius: 1vmin;
      background-color: white;
      outline: none;
      transition: border-color 0.3s ease-in-out;

      &::placeholder {
        color: #757575;
      }

      &:focus {
        border-color: #444444;
      }
    }
  }
}

.linha {
  width: 2px;
  height: 100%;
  background: #9524ff;
}
</style>
