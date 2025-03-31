<template>
  <HeaderSistema :logado="true" :activeIndex="6"></HeaderSistema>
</template>

<script>
import HeaderSistema from "../auxiliares/HeaderSistema.vue";

export default {
  name: "Test",
  components: {
    HeaderSistema,
  },
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style lang="scss" scoped></style>
