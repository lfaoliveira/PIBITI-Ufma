<template>
  <section class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
    <HeaderSistema :activeIndex="5"></HeaderSistema>
    <main class="flex flex-col items-center w-[clamp(280px,50vmin,500px)]">
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

      <h1 class="text-2xl font-semibold text-center my-4">Recuperar Senha</h1>
      <form @submit.prevent="mudarSenha" class="flex flex-col gap-[2vmin] w-full">
        <div class="flex flex-col gap-[1vmin]">
          <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Email</label>
          <input @input="checkEmail" type="text" v-model="this.email" class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]" />
          <p v-if="this.boolErros.email" class="text-red-500 text-sm">Insira um email válido!</p>
        </div>
        <div class="flex flex-col gap-[1vmin]">
          <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Nova Senha</label>
          <input
            @input="checkSenha"
            type="text"
            v-model="this.novaSenha"
            placeholder="Insira a nova senha"
            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
          />
          <ul class="list-none p-0 m-0">
            <li v-if="this.boolErros.senha.cadastro.numCaracteres" class="text-red-500 text-sm">A senha deve ter de 8 a 20 caracteres</li>
            <li v-if="this.boolErros.senha.cadastro.maiusculas" class="text-red-500 text-sm">A senha deve ter pelo menos 1 letra maiúscula</li>
          </ul>
        </div>
        <div class="flex flex-col gap-[1vmin]">
          <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Confirmar Senha</label>
          <input
            @input="checkConfirmacaoSenha"
            type="text"
            v-model="this.confirmNovaSenha"
            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
          />
          <p v-if="this.boolErros.senha.cadastro.confirm" class="text-red-500 text-sm">As senhas devem ser iguais!</p>
        </div>
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
/* Estilos substituídos por Tailwind */
</style>
