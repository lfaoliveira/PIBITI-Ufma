<template>
  <section class="main-section">
    <header class="div-header">
      <Voltar class="seta" :onclick="fnVoltar"></Voltar>
    </header>
    <main class="content-area">
      <div class="registration-box">
        <h1>Cadastre-se</h1>

        <form class="registration-form">
          <div class="form-group">
            <label>Email</label>
            <input type="email" placeholder="exemplo@email.com" />
          </div>

          <div class="form-group">
            <label>CPF</label>
            <input type="text" placeholder="Digite seu CPF" />
          </div>

          <div class="form-group">
            <label>CRM (opcional)</label>
            <input type="text" placeholder="Apenas oftalmologistas" />
          </div>

          <div class="terms">
            <input type="checkbox" id="terms" />
            <label for="terms">Concordo com os Termos e Condições</label>
          </div>

          <button type="submit" class="register-button">Registrar</button>
        </form>
      </div>
    </main>
    <Rodape class="rodape" margem-imagem="clamp(2px, 1vmin, 10px)"></Rodape>
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
  height: 99vh;
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
  width: 75%;
  margin: 2vmin auto 0vmin auto;
  background-color: #ebd3ff;
  align-self: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.registration-box {
  margin-top: 2vmin;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 50%;

  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
  }
}

.registration-form {
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
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #23064a;
    }
  }

  .rodape {
    gap: -1px;
  }
}
</style>

<script>
import Voltar from "./icons/Voltar.vue";
import Rodape from "./Rodape.vue";

export default {
  components: {
    Voltar,
    Rodape,
  },
  name: "cadatroComp",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
    fnVoltar() {
      this.$router.push({ name: "home" });
    },
  },
};
</script>

<style lang="scss" scoped></style>
