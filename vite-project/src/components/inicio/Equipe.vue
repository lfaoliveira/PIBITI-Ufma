<template>
  <div id="divisor" class="secao">
    <img
      src="../../assets/logo_VIP_Lab.png"
      alt="Logo VIpLab"
      class="img-logos"
      id="logo-vip"
    />
    <img
      src="../../assets/logo ufma.png"
      alt="Logo UFMA"
      class="img-logos"
      id="logo-ufma"
    />
    <img
      src="../../assets/LogoNCAFundBranco2000_2021.png"
      alt="Logo VIpLab"
      class="img-logos"
      :id="this.idNCA"
    />
  </div>
  <section class="team secao">
    <h2 class="section-title" id="titulo-equipe">Equipe</h2>
    <div class="team-content">
      <p class="texto-secoes" id="team-description">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
        lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
        lectus. Curabitur vehicula nibh urna Morbi vulputate magna id magna tempus
        volutpat. Duis metus elit, egestas id lorem at, dictum sollicitudin nunc. Nunc a
        bibendum leo. Fusce efficitur nibh a pretium feugiat. In at facilisis ante. Nullam
        id velit sed dolor mattis fringilla. Aliquam id interdum lorem
      </p>
      <img
        alt="Imagem Time do VipLab"
        class="team-image"
        src="../../assets/foto time.png"
      />
    </div>
  </section>
</template>

<script>
export default {
  name: "Test",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style lang="scss" scoped></style>
