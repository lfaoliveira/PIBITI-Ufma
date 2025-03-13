<template>
  <nav class="navbar">
    <ul class="nav-list">
      <li class="nav-item" v-for="(item, index) in menuItems" :key="index">
        <a :class="{ active: activeIndex === index }" @click="setActive(index)">
          {{ item }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      menuItems: ["Sistema", "Método", "Autores", "Dúvidas?"],
      activeIndex: 0,
    };
  },
  methods: {
    setActive(index) {
      this.activeIndex = index;
    },
  },
};
</script>

<style scoped>
.navbar {
  width: 100%;
  z-index: 1;
  background-color: #12071c;
  padding: 15px;
}

.nav-list {
  display: flex;
  list-style: none;
  justify-content: flex-start;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.nav-item a {
  color: white;
  font-size: 18px;
  font-weight: normal;
  text-decoration: none;
  transition: font-weight 0.3s;
}

.nav-item a.active {
  font-weight: bold;
}
</style>
