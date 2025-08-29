<template>
    <section class="frame-pagina">
        <HeaderSistema :activeIndex="5"></HeaderSistema>
        <main>
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

            <h1>Recuperar Senha</h1>
            <form @submit.prevent="recuperarSenha" name="FORM RECUPERAR">
                <div class="form-group">
                    <label>Email</label>
                    <input
                        @input="checkEmail"
                        type="text"
                        v-model="email"
                        placeholder="exemplo@email.com"
                    />
                    <p v-if="erro" class="erro">Insira um email válido!</p>
                </div>
                <Button type="submit" :ativo="!erro" texto="Recuperar"></Button>
            </form>
        </main>

        <Rodape />
    </section>
</template>

<script>
import Button from "../navigation/Button.vue";
import HeaderSistema from "../layout/HeaderSistema.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";
import Rodape from "../layout/Rodape.vue";

import axios from "axios";
import emitter from "../../eventBus";

const eventoSucesso = "sucesso";
const eventoFalha = "falha";

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
        };
    },
    mounted() {
        console.log("MONTADO ESQUECI");
    },
    methods: {
        checkEmail() {
            const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
            this.email = this.email.replace(/\s/, "");
            let passou = emailRegex.test(this.email);

            if (passou && this.email === "exemplo@email.com") passou = false;
            else if (this.email === "") passou = true;
            this.erro = !passou;
            return passou;
        },
        async recuperarSenha() {
            const form = new FormData();
            const urlFront = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/mudarSenha`;
            form.append("email", this.email);
            form.append("url_front", urlFront);
            console.log("ENTROU");
            try {
                console.log("TENTANDO");
                const res = await axios.post(
                    this.$store.getters.getUrlEsqueciSenha,
                    form
                );
                if (res.status == 200) {
                    emitter.emit(eventoSucesso);
                }
            } catch (error) {
                console.log("ERROR: ", error);

                emitter.emit(eventoFalha);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.frame-pagina {
    @include frame-pagina($gap: 5vmin);
    height: 100vh;
}

h1 {
    font-weight: 600;
    width: max-content;
    margin: 0px;
    text-align: center;
}

main {
    width: fit-content;
    margin: auto;
    height: 60%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 1vmin;
}

form {
    display: flex;
    flex-direction: column;
    gap: 3vmin;
    width: 100%;
}

.form-cadastro {
    width: 50%;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;

    label {
        font-size: $form-fonte-titulo;
        font-weight: 600;
    }

    input {
        width: 100%;
        padding: 1%;
        height: 2lh;
        font-size: $form-fonte-peq;
        border: 2px solid #b3b3b3;
        border-radius: 1vmin;
        background-color: white;
        outline: none;
        transition: border-color 0.3s ease-in-out;

        &::placeholder {
            color: #757575;
        }

        &:focus {
            border-color: #444444;
        }
    }
}

.erro {
    color: red;
    margin-left: 1vmin;
}
</style>
