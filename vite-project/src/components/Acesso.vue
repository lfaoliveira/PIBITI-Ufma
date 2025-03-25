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
            <input @input="checkSenha" type="text" v-model="this.senha" placeholder="" />
          </div>

          <p id="semLogin">
            Não Possui Login?
            <a @click="trocaAcesso">Fazer Cadastro</a>
          </p>

          <ButtonGrande
            type="submit"
            :ativo="checkCampos()"
            texto="Fazer Login"
          ></ButtonGrande>
        </form>
      </section>

      <section class="sec-cadastro" v-if="tipo === 'cadastro'">
        <h1>Cadastro (Apenas Médicos)</h1>
        <form class="form-cadastro" @submit.prevent="valAcesso">
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

          <ButtonGrande
            class="but-cadastro"
            type="submit"
            :ativo="checkCampos()"
            texto="Cadastro"
          ></ButtonGrande>
        </form>
      </section>

      <span class="linha" />

      <section class="avulsa">
        <h1>Análise Avulsa</h1>
        <p class="aviso">
          Aviso! A Análise Avulsa não salvará nenhuma informação dos pacientes
        </p>
        <div class="div-termos-label">
          <input type="checkbox" v-model="this.checks" id="checkTermos" />
          <label id="termos-label" for="checkTermos"
            >Concordo com os
            <a href="/termos" id="link-termos">Termos e Condições</a>
          </label>
        </div>
        <ButtonGrande
          @click="fnAvulsa"
          :ativo="this.checks"
          texto="Análise Avulsa"
        ></ButtonGrande>
      </section>
    </main>
    <Rodape></Rodape>
  </section>
</template>

<script>
import HeaderSistema from "./analise/HeaderSistema.vue";
import ButtonGrande from "./auxiliares/ButtonGrande.vue";
import Rodape from "./auxiliares/Rodape.vue";

import Validator from "../scripts/valAcesso";

const def = "default";
const off = "salvaroff";
const on = "salvar";
const outro = "outro";

export default {
  name: "acesso",
  components: {
    HeaderSistema,
    Rodape,
    ButtonGrande,
  },
  created() {},
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
          login: "Senha Incorreta!",
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
    valAcesso($evt) {
      if (this.tipo === "login") {
      } else if (this.tipo === "cadastro" && this.uf !== "") {
        const res = Validator.cadastro(
          this.email,
          this.senha,
          this.nome,
          `${this.uf}-${this.crm}`
        );
      } else {
      }
    },
    checkCampos() {
      if (this.tipo === "login") {
        return this.email !== "" && this.senha !== "";
      } else {
        return (
          this.checks &&
          this.email !== "" &&
          this.senha !== "" &&
          this.uf !== "" &&
          this.crm !== ""
        );
      }
    },
    checkEmail() {
      const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
      this.email = this.email.replace(/\s/, "");
      let passou = emailRegex.test(this.email);

      if (passou && this.email === "exemplo@meail.com") passou = false;
      else if (this.email === "") passou = true;
      this.boolErros.email = !passou;
    },
    checkNome() {
      if (this.nome !== "") {
        let nomeRegex = /\d/;
        this.nome = this.nome.replace(nomeRegex, "");
        nomeRegex = /\n|\t|\r/;
        this.nome = this.nome.replace(nomeRegex, " ");
        nomeRegex = /\s{2,}/;
        this.nome = this.nome.replace(nomeRegex, " ");
      }
    },
    checkSenha() {
      const regChar = /^.{8,20}$/;
      const regMaiusc = /[A-Z]/;
      if (this.tipo === "cadastro") {
        const passou1 = regChar.test(this.senha);
        if (!passou1) {
          console.log("MUITO PEQUENO");
          this.boolErros.senha.cadastro.numCaracteres = true;
        }
        const passou2 = regMaiusc.test(this.senha);
        if (!passou2) {
          console.log("SEM MAISUCULAS");
          this.boolErros.senha.cadastro.maiusculas = true;
        }
        if (passou1 && passou2) {
          this.boolErros.senha.cadastro.numCaracteres = false;
          this.boolErros.senha.cadastro.maiusculas = false;
        }
      }
    },
    checkCRM() {
      const regNumCRM = /^\d{1,6}$/;
      this.crm = this.crm.replace(/\s/, "");
      if (this.uf === "") {
        this.boolErros.crm.uf = true;
        return;
      } else {
        this.boolErros.crm.uf = false;
      }

      if (!regNumCRM.test(this.crm)) {
        this.boolErros.crm.numero = true;
      } else {
        this.boolErros.crm.numero = false;
      }
    },
    fnTermos() {
      this.$router.push("/termos");
    },
    fnAvulsa() {
      //TODO: prompt de uplaod de video;
    },
    trocaAcesso() {
      if (this.tipo === "cadastro") {
        this.tipo = "login";
      } else {
        this.tipo = "cadastro";
      }
    },
    checkUF() {
      if (this.uf === "UF") {
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
$larg-form-cad: 100%;

.frame-pagina {
  @include frame-pagina($gap: 5vmin);
  height: 100vh;
}

h1 {
  font-weight: 600;
  width: max-content;
  margin: 0px;
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
  width: $larg-form-cad;
}
.sec-cadastro {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
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

.div-termos-label {
  display: flex;
  gap: 1vmin;
  #link-termos {
    font-weight: 500;
  }
}

input[type="checkbox"] {
  accent-color: #2c2c2c; /* Changes the check color */
}

.avulsa {
  height: 100%;
  gap: 2vmin;
  display: flex;
  flex-direction: column;
  .aviso {
    width: 43vmin;
    color: $terc-color;
    font-weight: 600;
  }
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
