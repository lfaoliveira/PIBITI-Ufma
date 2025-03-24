<template>
  <section class="frame-pagina">
    <HeaderSistema tipo="default"></HeaderSistema>
    <main>
      <section v-if="tipo === 'login'" class="login">
        <h1>Fazer Login</h1>
        <form @submit.prevent="valAcesso">
          <div class="form-group">
            <label>Email</label>
            <input
              @input="checkEmail"
              type="text"
              v-model="this.email"
              placeholder="exemplo@email.com"
            />
          </div>
          <div class="form-group">
            <label>Senha</label>
            <input @input="checkSenha" type="text" v-model="this.senha" placeholder="" />
          </div>

          <p id="semLogin">
            Não Possui Login?
            <a @click="trocaAcesso">Fazer Cadastro</a>
          </p>

          <ButtonGrande type="submit" :ativo="true" texto="Fazer Login"></ButtonGrande>
        </form>
      </section>

      <section class="sec-cadastro" v-if="tipo === 'cadastro'">
        <h1>Cadastro (Apenas Médicos)</h1>
        <form class="form-cadastro" @submit.prevent="valAcesso">
          <div class="form-group">
            <label>Email</label>
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
            <div class="grupo-crm">
              <select v-model="this.uf" class="select-crm">
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
            :ativo="true"
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
          :ativo="true"
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
      console.log(this.email, this.crm);
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
    checkEmail($evt) {
      console.log($evt);
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
  }
}

#possuiLogin,
#semLogin {
  font-weight: bold;
  a {
    font-weight: 600;
  }
}
</style>
