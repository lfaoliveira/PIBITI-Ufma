<template>
  <section class="frame-pagina">
    <HeaderSistema :activeIndex="5"></HeaderSistema>
    <main>
      <OverlayAviso
        :eventoAviso="'cadastroRepetido'"
        :titulo="'Já há um usuário cadastrado com este email'"
        :subtexto="'Faça login no sistema para prosseguir'"
        :srcImg="'src/assets/alert_circle.png'"
      ></OverlayAviso>

      <OverlayAviso
        ref="avisoSucesso"
        :eventoAviso="'cadastroSucesso'"
        :titulo="'Cadastro feito com sucesso!'"
        :subtexto="'Nosso time está verificando seu CRM e enviará um email de confirmação assim que possível.'"
        :opcional="'Antes disso não será possível salvar seus diagnósticos'"
        :srcImg="'src/assets/check_circle.png'"
      ></OverlayAviso>

      <!-- PARTE DO LOGIN -->
      <section v-if="tipo === 'login'" class="login">
        <h1>Fazer Login</h1>
        <form @submit.prevent="valAcesso">
          <div class="form-group">
            <label>Email</label>
            <input type="text" v-model="this.email" placeholder="exemplo@email.com" />
          </div>
          <div class="form-group">
            <label>Senha</label>
            <input @input="checkSenha" type="text" v-model="this.senha" placeholder="" />
          </div>
          <p v-if="this.boolErros.senha.login" class="erro">
            {{ this.stringErros.senha.login }}
          </p>
          <a href="/esqueceuSenha" id="esqueci">Esqueci minha senha</a>
          <p id="semLogin">
            Não Possui Login?
            <a @click="trocaAcesso">Cadastre-se</a>
          </p>

          <Button type="submit" :ativo="checkCampos()" texto="Fazer Login"></Button>
        </form>
      </section>
      <!-- PARTE DO CADASTRO -->
      <section class="sec-cadastro" v-if="tipo === 'cadastro'">
        <h1>Cadastro</h1>
        <form
          @keyup.enter="$emit('submit')"
          ref="formCadastro"
          class="form-cadastro"
          @submit.prevent="valAcesso"
        >
          <div class="form-group">
            <label>Email</label>
            <p v-if="this.boolErros.email" class="erro">
              {{ this.stringErros.email }}
            </p>
            <input
              @input="checkEmail"
              type="text"
              v-model="this.email"
              placeholder="exemplo@email.com"
            />
          </div>
          <div class="form-group">
            <label>Nome Completo</label>
            <input @input="checkNome" type="text" v-model="this.nome" placeholder="" />
          </div>

          <div class="form-group">
            <label>CRM</label>
            <p v-if="this.boolErros.crm.uf" class="erro">
              {{ this.stringErros.crm.uf }}
            </p>
            <p v-if="this.boolErros.crm.numero" class="erro">
              {{ this.stringErros.crm.numero }}
            </p>
            <div class="grupo-crm">
              <select @change="checkCRM" v-model="this.uf" class="select-crm">
                <option value="" key="">UF</option>
                <option v-for="item in this.ufs" :key="item" :value="item">
                  {{ item }}
                </option>
              </select>

              <input @input="checkCRM" type="text" v-model="this.crm" placeholder="" />
            </div>
          </div>

          <div class="form-group">
            <label>Senha</label>
            <input @input="checkSenha" type="text" v-model="this.senha" placeholder="" />
            <ul class="errors-senha">
              <li v-if="this.boolErros.senha.cadastro.numCaracteres" class="erro">
                {{ this.stringErros.senha.cadastro.numCaracteres }}
              </li>
              <li v-if="this.boolErros.senha.cadastro.maiusculas" class="erro">
                {{ this.stringErros.senha.cadastro.maiusculas }}
              </li>
            </ul>
          </div>

          <div class="div-termos-label">
            <input type="checkbox" v-model="this.checks" id="checkTermos" />
            <label id="termos-label" for="checkTermos"
              >Concordo com os
              <a href="/termos" id="link-termos">Termos e Condições</a>
            </label>
          </div>

          <p id="possuiLogin">
            Já Possui Login?
            <a @click="trocaAcesso">Fazer Login</a>
          </p>

          <Button
            class="but-cadastro"
            type="submit"
            :ativo="checkCampos()"
            texto="Cadastro"
          ></Button>
        </form>
      </section>
    </main>
    <Rodape></Rodape>
  </section>
</template>

<script>
import HeaderSistema from "./auxiliares/HeaderSistema.vue";
import Button from "./auxiliares/Button.vue";
import Rodape from "./auxiliares/Rodape.vue";
import OverlayAviso from "./auxiliares/OverlayAviso.vue";

import axios from "axios";
import emitter from "../eventBus";

const cadSucesso = "cadastroSucesso";
const cadRepetido = "cadastroRepetido";

export default {
  name: "acesso",
  components: {
    HeaderSistema,
    Rodape,
    Button,
    OverlayAviso,
  },
  emits: ["abreAviso"],
  created() {},
  mounted() {},
  data() {
    return {
      tipo: "login",
      email: "",
      senha: "",
      crm: "",
      nome: "",
      checks: false,
      uf: "",
      stringErros: {
        email: "Email Inválido",
        crm: { uf: "Insira uma UF válida!", numero: "Insira um número válido!" },
        senha: {
          cadastro: {
            numCaracteres: "A senha deve conter 8 a 20 caracteres",
            maiusculas: "A senha deve ter pelo menos 1 letra maiúscula",
          },
          login: "Email e/ou Senha incorreto(s)!",
        },
      },
      boolErros: {
        email: false,
        crm: { uf: false, numero: false },
        senha: {
          cadastro: {
            numCaracteres: false,
            maiusculas: false,
          },
          login: false,
        },
      },
      cadastroRepetido: false,
      ufs: [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
      ],
    };
  },
  methods: {
    async valAcesso($evt) {
      if (this.tipo === "login") {
        /////LOGIN
        const form = new FormData();
        form.append("email", this.email);
        form.append("senha", this.senha);
        //SEMPRE ver se precisa de credenciais na requisicao
        const res = await axios.post(this.$store.getters.getUrlLogin, form, {
          withCredentials: true,
        });
        console.log(res);
        // sucesso login
        if (res.data === "OK") {
          this.boolErros.senha.login = false;
          console.log("Sucesso no LOGIN");
          this.$store.commit("setLogado", true);
          // this.$router.push("/perfil");
        } else {
          //erro no login
          this.boolErros.senha.login = true;
        }
        ///// CADASTRO
      } else if (this.tipo === "cadastro") {
        const form = new FormData();
        form.append("email", this.email);
        form.append("senha", this.senha);
        form.append("nome", this.nome);
        form.append("crm", `${this.uf}-${this.crm}`);
        // alert(this.$store.getters.getUrlCadastro);

        const res = await axios.post(this.$store.getters.getUrlCadastro, form);
        if (res.data === "JA_EXISTE") {
          emitter.emit(cadRepetido);
        } else {
          emitter.emit(cadSucesso);
          this.$store.commit("setLogado", true);
        }
        console.log(`HTTP CADASTRO: ${res.data}`);
      }
    },
    checkCampos() {
      if (this.tipo === "login") {
        return this.email !== "" && this.senha !== "";
      } else {
        return this.checks && this.checkEmail() && this.checkSenha() && this.checkCRM();
      }
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
    checkNome() {
      if (this.nome !== "") {
        //Tudo que nao seja letra e espaco sai
        let nomeRegex = /[^A-Za-z\s]/;
        this.nome = this.nome.replace(nomeRegex, "");
        //ajusta espaços
        nomeRegex = /[\s\n\t\r]{2,}/;
        this.nome = this.nome.replace(nomeRegex, " ");
        return true;
      }
      return false;
    },
    checkSenha() {
      let passou = true;
      const regMaiusc = /[A-Z]/;

      const passou1 = this.senha.length >= 8 && this.senha.length <= 20;
      if (!passou1) {
        this.boolErros.senha.cadastro.numCaracteres = true;
        passou = false;
      } else {
        this.boolErros.senha.cadastro.numCaracteres = false;
      }
      const passou2 = regMaiusc.test(this.senha);
      if (!passou2) {
        this.boolErros.senha.cadastro.maiusculas = true;
        passou = false;
      } else {
        this.boolErros.senha.cadastro.maiusculas = false;
      }
      return passou;
    },
    checkCRM() {
      let passou = true;
      const regNumCRM = /^\d{1,6}$/;
      this.crm = this.crm.replace(/\s/, "");
      if (this.uf === "") {
        this.boolErros.crm.uf = true;
        passou = false;
        return passou;
      } else {
        this.boolErros.crm.uf = false;
      }

      if (!regNumCRM.test(this.crm)) {
        this.boolErros.crm.numero = true;
        passou = false;
      } else {
        this.boolErros.crm.numero = false;
      }
      return passou;
    },

    trocaAcesso() {
      if (this.tipo === "cadastro") {
        this.tipo = "login";
      } else {
        this.tipo = "cadastro";
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
  display: flex;
  align-items: flex-start;
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

form {
  display: flex;
  flex-direction: column;
  gap: 2vmin;
  width: 100%;
}

.form-cadastro {
  width: 100%;
}
.sec-cadastro {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  gap: 5vmin;
}

.but-cadastro {
  position: relative;
  margin: 0px 2vmin;
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

.grupo-crm {
  flex-direction: row;
  display: flex;
  gap: 1vmin;
  .select-crm {
    background: white;
    border: 2px solid #b3b3b3;
    border-radius: 1vmin;
    padding: 0vmin 1.5vmin 0vmin 0.5vmin;
    &:focus,
    &:hover {
      border-color: #444444;
    }
  }
}

.login {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1vmin;
}

.linha {
  width: clamp(2px, 2px, 2px);

  height: 100%;
  background: $sec-color;
  @media (max-width: 900px) {
    padding: clamp(1px, 1px, 1px);
  }
}

input[type="checkbox"] {
  accent-color: #2c2c2c; /* Changes the check color */
}

.div-termos-label {
  display: flex;
  gap: 1vmin;
}

#possuiLogin,
#semLogin {
  font-weight: bold;
  a {
    font-weight: 600;
  }
}

.errors-senha {
  padding: 0px;
  margin-left: 1vmin;
  list-style-type: circle;
}

.erro {
  color: red;
  margin-left: 1vmin;
}
</style>
