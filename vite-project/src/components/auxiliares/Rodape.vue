<template>
  <footer>
    <ul class="logos">
      <a
        class="link-img"
        href="https://sigaa.ufma.br/sigaa/public/departamento/secao_extra.jsf?lc=pt_BR&id=998&extra=208953677"
        target="_blank"
      >
        <img
          src="../../assets/logo_VIP_Lab.png"
          alt="Logo footer"
          id="logo-vip"
          class="footer-logo"
        />
      </a>
      <a class="link-img" href="https://portalpadrao.ufma.br/site" target="_blank">
        <img
          src="../../assets/logo ufma.png"
          alt="Logo footer"
          id="logo-ufma"
          class="footer-logo"
        />
      </a>
      <a class="link-img" href="https://anselmopaiva.github.io/" target="_blank">
        <img
          src="../../assets/LogoNCAFundBranco2000_2021.png"
          alt="Logo footer"
          id="logo-nca"
          href="/"
          class="footer-logo"
        />
      </a>
    </ul>
    <nav class="footer-nav">
      <!-- TODO: MUDAR EMAIL DE CONTATO-->
      <a href="mailto:viplab.psno@nca.ufma.br" class="footer-link">Suporte</a>
      <a href="/termos" target="_blank" class="footer-link">Termos e Condições</a>
      <a href="/duvidas" target="_blank" class="footer-link">Sobre</a>
    </nav>
  </footer>
</template>

<style lang="scss" scoped>
footer {
  display: inline-flex;
  padding: 0px 4px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-self: flex-end;
  gap: 20px;
  width: 100%;
  padding-bottom: 1vmin;

  .logos {
    display: flex;
    padding: 1vmin 0.5vmin 0vmin 0vmin;
    justify-content: center;
    align-items: flex-start;
    gap: 10vmin;
    align-self: stretch;
    .link-img {
      width: auto;
      height: auto;
      &:hover {
        background: none;
      }
    }
    #logo-vip {
      width: 125.189px;
      aspect-ratio: 125.19/88.34;
      margin: 0;
    }
    #logo-ufma {
      width: 88.336px;
      aspect-ratio: 88.34/88.34;
      margin: 0;
    }
    #logo-nca {
      width: 113.542px;
      aspect-ratio: 113.54/88.34;
      margin: 0;
    }
  }

  .footer-nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6vmin;
    align-self: stretch;
    width: 100%;
  }

  .footer-link {
    color: #000;
    font: 700 14px Montserrat, sans-serif;
    &:hover {
      color: #000;
      background: #7f8084;
    }
  }
}
</style>

<script>
export default {
  name: "Rodape",
  data() {
    return {};
  },
  mounted() {},
  props: {
    margemImagem: { type: String, default: "20px" },
  },
  methods: {},
};
</script>
