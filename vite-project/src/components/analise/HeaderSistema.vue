<template>
  <div></div>
</template>

<script>
export default {
  name: "HeaderSistema",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
    fnVoltar() {
      // retorna 1 página
      this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped></style>
