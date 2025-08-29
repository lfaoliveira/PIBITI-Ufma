<template>
  <section class="frame-pagina">
    <HeaderSistema :activeIndex="5"></HeaderSistema>
    <main>
      <OverlayAviso
        :eventoAviso="'sucesso'"
        :titulo="'Email de recuperação enviado!'"
        :subtexto="'Caso não tenha chegado, espere até 5 minutos antes de enviar outra solicitação'"
        :srcImg="'src/assets/check_circle.png'"
      ></OverlayAviso>
      <OverlayAviso
        :eventoAviso="'falha'"
        :titulo="'Email Inválido!'"
        :subtexto="''"
        :srcImg="'src/assets/check_circle.png'"
      ></OverlayAviso>

      <h1>Recuperar Senha</h1>
      <form @submit.prevent="mudarSenha">
        <div class="form-group">
          <label>Email</label>
          <input @input="checkEmail" type="text" v-model="this.email" />
          <p v-if="this.boolErros.email" class="erro">Insira um email válido!</p>
        </div>
        <div class="form-group">
          <label>Nova Senha</label>
          <input
            @input="checkSenha"
            type="text"
            v-model="this.novaSenha"
            placeholder="Insira a nova confirmnovaSenha"
          />
          <li v-if="this.boolErros.senha.cadastro.numCaracteres" class="erro">
            A senha deve ter de 8 a 20 caracteres
          </li>
          <li v-if="this.boolErros.senha.cadastro.maiusculas" class="erro">
            A senha deve ter pelo menos 1 letra maiúscula
          </li>
        </div>
        <div class="form-group">
          <label>Confirmar Senha</label>
          <input
            @input="checkConfirmacaoSenha"
            type="text"
            v-model="this.confirmNovaSenha"
          />
          <p v-if="this.boolErros.senha.cadastro.confirm" class="erro">
            As senhas devem ser iguais!
          </p>
        </div>
        <!-- BUG AO CLICAR!!!!! -->
        <Button type="submit" :ativo="checkCampos()" texto="Enviar"></Button>
      </form>
    </main>

    <Rodape class="roda" />
  </section>
</template>

<script>
import Button from "../navigation/Button.vue";
import HeaderSistema from "../layout/HeaderSistema.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";
import Rodape from "../layout/Rodape.vue";

import axios from "axios";
import emitter from "../../eventBus";

const eventoSucesso = "sucesso";
const eventoFalha = "falha";

export default {
  name: "EsqueceuSenha",
  components: {
    HeaderSistema,
    OverlayAviso,
    Button,
    Rodape,
  },
  created() {},
  data() {
    return {
      email: "",
      novaSenha: "",
      confirmNovaSenha: "",
      erro: false,
      boolErros: {
        email: false,
        senha: {
          cadastro: {
            numCaracteres: false,
            maiusculas: false,
            confirm: false,
          },
          login: false,
        },
      },
    };
  },
  props: {
    emailUsuario: "",
  },
  methods: {
    checkCampos() {
      console.log(
        "CHECK CAMPOS: ",
        this.checkEmail() && this.checkSenha() && this.checkConfirmacaoSenha()
      );
      return (
        this.email !== "" &&
        this.checkEmail() &&
        this.checkSenha() &&
        this.checkConfirmacaoSenha()
      );
    },

    checkEmail() {
      const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
      //tira espacos
      this.email = this.email.replace(/\s/, "");
      let passou = emailRegex.test(this.email);

      if (passou && this.email === "exemplo@email.com") passou = false;
      else if (this.email === "") passou = true;
      this.boolErros.email = !passou;
      return passou;
    },
    checkSenha() {
      let passou = true;
      const regMaiusc = /[A-Z]/;

      const passou1 = this.novaSenha.length >= 8 && this.novaSenha.length <= 20;
      if (!passou1) {
        this.boolErros.senha.cadastro.numCaracteres = true;
        passou = false;
      } else {
        this.boolErros.senha.cadastro.numCaracteres = false;
      }
      const passou2 = regMaiusc.test(this.novaSenha);
      if (!passou2) {
        this.boolErros.senha.cadastro.maiusculas = true;
        passou = false;
      } else {
        this.boolErros.senha.cadastro.maiusculas = false;
      }
      return passou;
    },
    checkConfirmacaoSenha() {
      const passou = this.novaSenha == this.confirmNovaSenha;
      this.boolErros.senha.cadastro.confirm = !passou;

      return passou;
    },
  },
  // chama backend pra mandar email pro medico
  async mudarSenha() {
    const form = new FormData();
    form.append("email", this.email);
    form.append("novaSenha", this.novaSenha);
    console.log("MUDANDO SENHA");
    try {
      const res = await axios.post(this.store.getters.getUrlMudarSenha, form);
      if (res.status == 200) {
        console.log("SENHA MUDADA");
        emitter.emit(eventoSucesso);
      }
    } catch (e) {
      console.log("DEU MERDA");
      if (res.status == 400) {
        // TODO: EMITIR EVENTO DE AVISO QUE EMAIL NÃO EXISTE
        emitter.emit(eventoFalha);
      }
    }
  },
};
</script>

<style lang="scss" scoped>
.frame-pagina {
  @include frame-pagina($gap: 5vmin);
  height: 100vh;
}

h1 {
  font-weight: 600;
  width: max-content;
  margin: 0px;
  text-align: center;
}

main {
  width: fit-content;
  margin: auto;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 1vmin;
}

form {
  display: flex;
  flex-direction: column;
  gap: 3vmin;
  width: 100%;
}

.form-cadastro {
  width: 50%;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;

  label {
    font-size: $form-fonte-titulo;
    font-weight: 600;
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

.erro {
  color: red;
  margin-left: 1vmin;
}
</style>
