<template>
    <main
        class="shadow-[0px_0px_0px_0.05rem_rgb(0,0,0)] mx-auto w-[clamp(90vmin,90%,100%)] h-[22rem] md:h-[25rem] lg:h-[30rem] mt-[5vmin] relative text-white mb-[2%] self-center"
    >
        <!-- @loadedmetadata="getLoadedVideo" -->
        <video
            class="video-js vjs-custom-skin"
            preload="auto"
            :src="this.videoSource"
            :muted="muted"
            :autoplay="autoplay"
            :controls="controls"
            :loop="loop"
            ref="videoplayer"
        />
        <img ref="imgGraf" />
    </main>
</template>

<style scoped>
/* Video.js custom overrides - mantidos porque afetam o player globalmente */
.video-js .vjs-control-bar {
    background: linear-gradient(
        180deg,
        rgba(95, 95, 95, 0.66) 0%,
        rgba(33, 33, 33, 0.85) 39%,
        rgba(17, 0, 0, 1) 97%
    );
}

.video-js .vjs-play-control {
    background-color: #fff;
    color: #6113c6;
    border-radius: 100%;
    display: flex;
    aspect-ratio: 21/15;
}

.video-js .vjs-mute-control {
    color: #fff;
    margin-left: 1vmin;
}

.video-js .vjs-control-bar {
    display: flex;
}

.video-js[tabindex="-1"] {
    height: 100%;
    width: 100%;
}
</style>

<script>
import videojs from "video.js"
import "video.js/dist/video-js.css"

export default {
    name: "Player_de_Video",
    // TODO: INSERIR LOGICA DE ADAPTAR TAMANHO DO WRAPPER COM BASE NO ASPECT-RATIO DO VIDEO
    props: {
        videoSource: { type: String, required: true, default: "" },
        mimeVideo: { type: String, required: true, default: "" },
        controls: { type: Boolean, default: true },
        loop: { type: Boolean, default: true },
        autoplay: { type: Boolean, default: false },
        muted: { type: Boolean, default: true },
        preload: { type: String, default: "false" },
    },
    components: {},
    data() {
        return {}
    },
    async mounted() {
        console.log("MONTADO VIDEOPLAYER:")
        console.log("MIME: VIDEOPLAYER: ", this.mimeVideo)
        try {
            const sources = [{ src: this.videoSource, type: `${this.mimeVideo}` }]
            this.setupPlayer(sources)
        } catch (error) {
            console.log(error)
        }
    },

    methods: {
        setupPlayer(sources) {
            //Funcao que faz setup inicial do videoplayer usando dados do VideoPlayer.vue
            this.player = videojs(this.$refs.videoplayer, {
                sources: sources,
            })
        },

        onVoltar() {
            this.$router.push("/")
        },
    },
    beforeDestroy() {
        if (this.player) {
            this.player.dispose()
        }
    },
    computed: {
        stylePausa() {
            /*FUNCAO que estiliza play e pause  */
            // so funiona porque nao acessa DOM diretamente. ver docs
            if (this.playing) {
                return {
                    padding: `0%`,
                    width: `clamp(1vmin, 22px + 3px, 100%)`,
                }
            } else {
                return {
                    padding: `12%`,
                    width: `clamp(1vmin, 25px, 100%)`,
                }
            }
        },
    },
}
</script>
