<template>
    <section class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <HeaderSistema :activeIndex="5"></HeaderSistema>
        <main class="flex flex-col items-center w-[clamp(280px,50vmin,500px)]">
            <OverlayAviso
                :eventoAviso="'sucesso'"
                :titulo="'Email de recuperação enviado!'"
                :subtexto="'Caso não tenha chegado, espere até 5 minutos antes de enviar outra solicitação'"
                :srcImg="'src/assets/check_circle.png'"
            ></OverlayAviso>
            <OverlayAviso
                :eventoAviso="'falha'"
                :titulo="'Email Inválido!'"
                :subtexto="''"
                :srcImg="'src/assets/alert_circle.png'"
            ></OverlayAviso>

            <h1 class="text-2xl font-semibold text-center my-4">Recuperar Senha</h1>
            <form
                @submit.prevent="recuperarSenha"
                name="FORM RECUPERAR"
                class="flex flex-col gap-[2vmin] w-full"
            >
                <div class="flex flex-col gap-[1vmin]">
                    <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]"
                        >Email</label
                    >
                    <input
                        @input="checkEmail"
                        type="text"
                        v-model="email"
                        placeholder="exemplo@email.com"
                        class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                    />
                    <p v-if="erro" class="text-red-500 text-sm">
                        Insira um email válido!
                    </p>
                </div>
                <Button type="submit" :ativo="!erro" texto="Recuperar"></Button>
            </form>
        </main>

        <Rodape />
    </section>
</template>

<script>
import Button from "../navigation/Button.vue"
import HeaderSistema from "../layout/HeaderSistema.vue"
import OverlayAviso from "../layout/OverlayAviso.vue"
import Rodape from "../layout/Rodape.vue"

import axios from "axios"
import emitter from "../../eventBus"

const eventoSucesso = "sucesso"
const eventoFalha = "falha"

export default {
    name: "EsqueceuSenha",
    components: {
        HeaderSistema,
        OverlayAviso,
        Button,
        Rodape,
    },
    data() {
        return {
            email: "",
            erro: false,
        }
    },
    mounted() {
        console.log("MONTADO ESQUECI")
    },
    methods: {
        checkEmail() {
            const emailRegex = /^[\w]+@[\w]+\.[\w]+$/
            this.email = this.email.replace(/\s/, "")
            let passou = emailRegex.test(this.email)

            if (passou && this.email === "exemplo@email.com") passou = false
            else if (this.email === "") passou = true
            this.erro = !passou
            return passou
        },
        async recuperarSenha() {
            const form = new FormData()
            const urlFront = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/mudarSenha`
            form.append("email", this.email)
            form.append("url_front", urlFront)
            console.log("ENTROU")
            try {
                console.log("TENTANDO")
                const res = await axios.post(this.$store.getters.getUrlEsqueciSenha, form)
                if (res.status == 200) {
                    emitter.emit(eventoSucesso)
                }
            } catch (error) {
                console.log("ERROR: ", error)

                emitter.emit(eventoFalha)
            }
        },
    },
}
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
