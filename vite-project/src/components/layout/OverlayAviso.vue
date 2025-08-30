<template>
    <section v-if="aberto" class="overlay">
        <div class="alerta">
            <img :src="srcImg" />
            <ul class="textos">
                <h1>{{ titulo }}</h1>
                <h1>{{ subtexto }}</h1>
                <h1 v-if="opcional !== ''" id="opcional">{{ opcional }}</h1>
            </ul>
        </div>
        <div class="div-but">
            <Button @click="closeOverlay" :texto="'OK'" :ativo="true"></Button>
        </div>
    </section>
</template>

<script>
import Button from "../navigation/Button.vue";
import emitter from "../../eventBus.js";

export default {
    name: "overlay",
    components: {
        Button,
    },
    created() {
        // Listen for the 'cadastroRepetido' event
        emitter.on(this.eventoAviso, this.openOverlay);
    },
    mounted() {
        console.log("MONTADO AVISo");
    },
    beforeUnmount() {
        // Clean up the event listener
        emitter.off(this.eventoAviso, this.openOverlay);
    },
    data() {
        return {
            aberto: null,
        };
    },
    props: {
        eventoAviso: "", //
        titulo: "",
        subtexto: "",
        opcional: "",
        srcImg: { type: String, default: "", required: true },
        rota: null,
    },
    methods: {
        openOverlay() {
            this.aberto = true;
        },
        closeOverlay() {
            this.aberto = false;
            if (this.rota != null) {
                console.log("ROTA: ", this.rota);
                this.$router.push(this.rota);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.overlay {
    @include overlay;
    background: white;

    gap: 5vmin;

    img {
        margin-left: 5vmin;
        width: 10vmin;
        height: 10vmin;
    }

    .alerta {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        gap: 2vmin;

        .textos {
            display: flex;
            width: fit-content;
            flex-direction: column;
            align-items: flex-start;
            gap: 5vmin;
            align-self: stretch;
        }
        #opcional {
            color: #792359;
        }
    }
    .div-but {
        width: 22vmin;
    }
}
</style>
