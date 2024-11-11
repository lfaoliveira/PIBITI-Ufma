<template>
  <footer class="footer">
    <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/938d419ab519c103a1e0833b1a20709f879d21b943df87ce5a6ad7be4a35e7b8?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Logo footer" class="footer-logo" />
    <nav class="footer-nav">
      <a href="#" class="footer-link">Avisos Legais</a>
      <a href="mailto:contato@email.ufma.br" class="footer-link">Contato: contato@email.ufma.br</a>
      <a href="#" class="footer-link">Sobre</a>
    </nav>
  </footer>
</template>

<script>
export default {
  name: "Rodape",
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped>
.footer {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-logo {
  width: 100px;
  height: auto;
  margin-bottom: 20px;
}

.footer-nav {
  display: flex;
  justify-content: space-around;
  width: 100%;
  max-width: 600px;
}

.footer-link {
  color: #000;
  font: 700 14px Montserrat, sans-serif;
}

</style>