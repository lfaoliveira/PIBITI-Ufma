<template>
    <section class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <HeaderSistema :activeIndex="5"></HeaderSistema>
        <main class="w-full">
            <OverlayAviso
                :eventoAviso="'cadastroRepetido'"
                :titulo="'Já há um usuário cadastrado com este email'"
                :subtexto="'Faça login no sistema para prosseguir'"
                :srcImg="'src/assets/alert_circle.png'"
            ></OverlayAviso>

            <OverlayAviso
                ref="avisoSucesso"
                :eventoAviso="'cadastroSucesso'"
                :titulo="'Cadastro feito com sucesso!'"
                :subtexto="'Nosso time está verificando seu CRM e enviará um email de confirmação assim que possível.'"
                :opcional="'Antes disso não será possível salvar seus diagnósticos'"
                :srcImg="'src/assets/check_circle.png'"
                :rota="'/perfil'"
            ></OverlayAviso>

            <!-- PARTE DO LOGIN -->
            <section v-if="tipo === 'login'" class="flex flex-col items-center w-full">
                <h1 class="text-[#3a0d75] text-xl sm:text-4xl m-0 text-center self-center font-light leading-normal">
                    Fazer Login
                </h1>
                <form @submit.prevent="valAcesso" class="flex flex-col gap-[2vmin] w-[clamp(280px,50vmin,500px)] mx-auto mt-[3vmin]">
                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Email</label>
                        <input
                            type="text"
                            v-model="this.email"
                            placeholder="exemplo@email.com"
                            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                        />
                    </div>
                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Senha</label>
                        <input
                            @input="checkSenha"
                            type="text"
                            v-model="this.senha"
                            placeholder=""
                            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                        />
                    </div>
                    <p v-if="this.boolErros.senha.login" class="text-red-500 text-sm">{{ this.stringErros.senha.login }}</p>
                    <a href="/esqueceuSenha" id="esqueci" class="text-blue-600 underline text-sm">Esqueci minha senha</a>
                    <p id="semLogin" class="text-sm text-gray-600">
                        Não Possui Login?
                        <a @click="trocaAcesso" class="text-blue-600 underline cursor-pointer">Cadastre-se</a>
                    </p>

                    <Button
                        type="submit"
                        :ativo="checkCampos()"
                        texto="Fazer Login"
                    ></Button>
                </form>
            </section>
            <!-- PARTE DO CADASTRO -->
            <section class="flex flex-col items-center w-full" v-if="tipo === 'cadastro'">
                <h1 class="text-[#3a0d75] text-xl sm:text-4xl m-0 text-center self-center font-light leading-normal">
                    Cadastro
                </h1>
                <form
                    @keyup.enter="$emit('submit')"
                    ref="formCadastro"
                    class="flex flex-col gap-[2vmin] w-[clamp(280px,50vmin,500px)] mx-auto mt-[3vmin]"
                    @submit.prevent="valAcesso"
                >
                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Email</label>
                        <p v-if="this.boolErros.email" class="text-red-500 text-sm">{{ this.stringErros.email }}</p>
                        <input
                            @input="checkEmail"
                            type="text"
                            v-model="this.email"
                            placeholder="exemplo@email.com"
                            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                        />
                    </div>
                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Nome Completo</label>
                        <input
                            @input="checkNome"
                            type="text"
                            v-model="this.nome"
                            placeholder=""
                            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                        />
                    </div>

                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">CRM</label>
                        <p v-if="this.boolErros.crm.uf" class="text-red-500 text-sm">{{ this.stringErros.crm.uf }}</p>
                        <p v-if="this.boolErros.crm.numero" class="text-red-500 text-sm">{{ this.stringErros.crm.numero }}</p>
                        <div class="flex gap-[1vmin]">
                            <select
                                @change="checkCRM"
                                v-model="this.uf"
                                class="w-[30%] p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                            >
                                <option value="" key="">UF</option>
                                <option
                                    v-for="item in this.ufs"
                                    :key="item"
                                    :value="item"
                                >
                                    {{ item }}
                                </option>
                            </select>

                            <input
                                @input="checkCRM"
                                type="text"
                                v-model="this.crm"
                                placeholder=""
                                class="flex-1 p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                            />
                        </div>
                    </div>

                    <div class="flex flex-col gap-[1vmin]">
                        <label class="text-[#333] text-[clamp(14px,1.8vmin,18px)]">Senha</label>
                        <input
                            @input="checkSenha"
                            type="text"
                            v-model="this.senha"
                            placeholder=""
                            class="w-full p-[clamp(8px,1.2vmin,14px)] border border-[#ddd] rounded text-[clamp(14px,1.6vmin,18px)] focus:outline-none focus:border-[#6113C6]"
                        />
                        <ul class="list-none p-0 m-0">
                            <li v-if="this.boolErros.senha.cadastro.numCaracteres" class="text-red-500 text-sm">{{ this.stringErros.senha.cadastro.numCaracteres }}</li>
                            <li v-if="this.boolErros.senha.cadastro.maiusculas" class="text-red-500 text-sm">{{ this.stringErros.senha.cadastro.maiusculas }}</li>
                        </ul>
                    </div>

                    <div class="flex items-center gap-[1vmin] my-[1vmin]">
                        <input type="checkbox" v-model="this.checks" id="checkTermos" class="w-[18px] h-[18px]" />
                        <label id="termos-label" for="checkTermos" class="text-sm text-gray-600"
                            >Concordo com os
                            <a href="/termos" id="link-termos" class="text-blue-600 bg-white p-0 hover:bg-gray-200 hover:rounded-lg hover:p-[0.25vmin]">Termos e Condições</a>
                        </label>
                    </div>

                    <p id="possuiLogin" class="text-sm text-gray-600">
                        Já Possui Login?
                        <a @click="trocaAcesso" class="text-blue-600 underline cursor-pointer">Fazer Login</a>
                    </p>

                    <Button
                        class="but-cadastro"
                        type="submit"
                        :ativo="checkCampos()"
                        texto="Cadastro"
                    ></Button>
                </form>
            </section>
        </main>
        <Rodape></Rodape>
    </section>
</template>

<script>
import HeaderSistema from "../layout/HeaderSistema.vue";
import Button from "../navigation/Button.vue";
import Rodape from "../layout/Rodape.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";

import axios from "axios";
import emitter from "../../eventBus";

const cadSucesso = "cadastroSucesso";
const cadRepetido = "cadastroRepetido";

export default {
    name: "acesso",
    components: {
        HeaderSistema,
        Rodape,
        Button,
        OverlayAviso,
    },
    emits: ["abreAviso"],
    created() {},
    mounted() {
        if (this.$store.getters.getLogado) {
            this.$router.push("/perfil");
        }
    },
    data() {
        return {
            tipo: "login",
            email: "",
            senha: "",
            crm: "",
            nome: "",
            checks: false,
            uf: "",
            stringErros: {
                email: "Email Inválido",
                crm: { uf: "Insira uma UF válida!", numero: "Insira um número válido!" },
                senha: {
                    cadastro: {
                        numCaracteres: "A senha deve conter 8 a 20 caracteres",
                        maiusculas: "A senha deve ter pelo menos 1 letra maiúscula",
                    },
                    login: "Email e/ou Senha incorreto(s)!",
                },
            },
            boolErros: {
                email: false,
                crm: { uf: false, numero: false },
                senha: {
                    cadastro: {
                        numCaracteres: false,
                        maiusculas: false,
                    },
                    login: false,
                },
            },
            cadastroRepetido: false,
            ufs: [
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ],
        };
    },
    methods: {
        async valAcesso($evt) {
            if (this.tipo === "login") {
                /////LOGIN
                const form = new FormData();
                form.append("email", this.email);
                form.append("senha", this.senha);
                //SEMPRE ver se precisa de credenciais na requisicao
                let res = 0;
                try {
                    res = await axios.post(this.$store.getters.getUrlLogin, form, {
                        withCredentials: true,
                    });
                    console.log(res);
                    // sucesso login
                    if (res.status === 200) {
                        this.boolErros.senha.login = false;
                        console.log("Sucesso no LOGIN");
                        this.$store.commit("setLogado", true);
                        this.$router.push("/perfil");
                    }
                } catch (e) {
                    console.log("FALHA!");
                    this.boolErros.senha.login = true;
                }

                ///// CADASTRO
            } else if (this.tipo === "cadastro") {
                const form = new FormData();
                form.append("email", this.email);
                form.append("senha", this.senha);
                form.append("nome", this.nome);
                form.append("crm", `${this.uf}-${this.crm}`);
                // alert(this.$store.getters.getUrlCadastro);

                const res = await axios.post(this.$store.getters.getUrlCadastro, form);
                if (res.data === "JA_EXISTE") {
                    emitter.emit(cadRepetido);
                } else {
                    emitter.emit(cadSucesso);
                    this.$store.commit("setLogado", true);
                }
                console.log(`HTTP CADASTRO: ${res.data}`);
            }
        },
        checkCampos() {
            if (this.tipo === "login") {
                return this.email !== "" && this.senha !== "";
            } else {
                return (
                    this.checks &&
                    this.checkEmail() &&
                    this.checkSenha() &&
                    this.checkCRM()
                );
            }
        },
        checkEmail() {
            const emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
            //tira espacos
            this.email = this.email.replace(/\s/, "");
            let passou = emailRegex.test(this.email);

            if (passou && this.email === "exemplo@email.com") passou = false;
            else if (this.email === "") passou = true;
            this.boolErros.email = !passou;
            return passou;
        },
        checkNome() {
            if (this.nome !== "") {
                //Tudo que nao seja letra e espaco sai
                let nomeRegex = /[^\p{L}\s]/gu;
                this.nome = this.nome.replace(nomeRegex, "");
                //ajusta espaços
                nomeRegex = /[\s\n\t\r]{2,}/;
                this.nome = this.nome.replace(nomeRegex, " ");
                return true;
            }
            return false;
        },
        checkSenha() {
            let passou = true;
            const regMaiusc = /[A-Z]/;

            const passou1 = this.senha.length >= 8 && this.senha.length <= 20;
            if (!passou1) {
                this.boolErros.senha.cadastro.numCaracteres = true;
                passou = false;
            } else {
                this.boolErros.senha.cadastro.numCaracteres = false;
            }
            const passou2 = regMaiusc.test(this.senha);
            if (!passou2) {
                this.boolErros.senha.cadastro.maiusculas = true;
                passou = false;
            } else {
                this.boolErros.senha.cadastro.maiusculas = false;
            }
            return passou;
        },
        checkCRM() {
            let passou = true;
            const regNumCRM = /^\d{1,6}$/;
            this.crm = this.crm.replace(/\s/, "");
            if (this.uf === "") {
                this.boolErros.crm.uf = true;
                passou = false;
                return passou;
            } else {
                this.boolErros.crm.uf = false;
            }

            if (!regNumCRM.test(this.crm)) {
                this.boolErros.crm.numero = true;
                passou = false;
            } else {
                this.boolErros.crm.numero = false;
            }
            return passou;
        },

        trocaAcesso() {
            if (this.tipo === "cadastro") {
                this.tipo = "login";
            } else {
                this.tipo = "cadastro";
            }
        },

        handleSucess() {
            const caixa = this.$refs.caixaErro;
            caixa.style.display = "none";
            this.texto = "adadaw";
        },
    },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
