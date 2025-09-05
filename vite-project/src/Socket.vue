<template>
    <h1>EXEMPLO ANALISE</h1>
    <div class="outline-red-50 outline-2 w-4 h-4"></div>
</template>

<script>
export default {
    name: "Socket",
    created() {},
    data() {
        return {};
    },
    props: {},
    methods: {
        async enviaFlask() {
            const url = this.$store.getters.getUrlBackend;
            const res = await fetch(`${String(url)}/submit_form`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ texto: "texto", video: "video" }),
            });
            const { uuid } = await res.json();
            const ws = new WebSocket(`${this.$store.getters.getUrlBackend}/ws`);
            ws.onopen = () => ws.send(uuid);
            ws.onmessage = (evt) => console.log("WS got:", evt.data);
        },
    },
};
</script>

<style lang="scss" scoped></style>
