<script lang="js">
export default{
  name: "FFCreator",
  data(){
    return {

    };
  },
  methods:{
    main(){
      // Componente de backend para processamento das layers dos videos
      // TODO: MODULARIZAR CODIGO DO FFCREATOR PARA QUE GENERALIZE PARA QUALQUER VIDEO


      const path = require('path');
      const colors = require('colors');
      const startAndListen = require('.\\node_modules\\listen');
      const { FFCreatorCenter, FFScene, FFAudio, FFAlbum, FFText, FFImage, FFCreator } = require('.\\node_modules\\ffcreator');

      // CÓDIGO DE EXEMPLO DE UTILIZAÇÃO DO FFCREATOR e FFCreatorCenter
      const createFFTask = () => {
        const assets = path.join(__dirname, 'assets')
        const bg = path.join(assets, '02.jpeg');
        const cover = path.join(assets, '03.jpeg');
        const img1 = path.join(assets, '01.jpeg');
        const img2 = path.join(assets, '02.jpeg');
        const img3 = path.join(assets, '03.jpeg');
        const img4 = path.join(assets, '04.jpeg');
        const img5 = path.join(assets, '05.jpeg');
        const audio = path.join(assets, '03.mp3');
        const outputDir = path.join(__dirname, 'output');
        const cacheDir = path.join(__dirname, 'cache');

        // create creator instance
        const width = 576;
        const height = 1024;
        const creator = new FFCreator({
          cover,
          cacheDir,
          outputDir,
          width,
          height,
          debug: false,
          log: true,
        });

        creator.addAudio(new FFAudio({ path: audio, volume: 0.9, fadeIn: 4, fadeOut: 4, loop: true }));

        // create FFScene
        const scene1 = new FFScene();
        const scene2 = new FFScene();
        scene1.setBgColor('#3b3a98');
        scene2.setBgColor('#b33771');

        // add new album
        

        // add title
        const text1 = new FFText({ text: 'DEMO', x: width / 2, y: 150, fontSize: 40 });
        text1.setColor('#ffffff');
        text1.setBackgroundColor('#01003c');
        text1.addEffect('fadeInUp', 1, 1);
        text1.alignCenter();
        text1.setStyle({ padding: 10 });
        scene1.addChild(text1);

        const text2 = new FFText({
          text: 'DEMADADAEFAEFAF',
          x: width / 2,
          y: 250,
          fontSize: 24,
        });
        text2.setColor('#ffffff');
        text2.addEffect('fadeInUp', 1, 2);
        text2.alignCenter();
        scene1.addChild(text2);
      
        
        creator.addChild(scene1);

        // add scene2 background
        const fbg = new FFImage({ path: bg });
        fbg.setXY(width / 2, height / 2);
        scene2.addChild(fbg);
        // add logo
        /*
        const flogo1 = new FFImage({ path: logo1, x: width / 2, y: height / 2 - 150 });
        flogo1.addEffect('fadeInDown', 1, 1.2);
        scene2.addChild(flogo1); */

        scene2.setDuration(5);
        creator.addChild(scene2);
        creator.start();
        creator.openLog();

        creator.on('start', () => {
          console.log(`FFCreator start`);
        });

        creator.on('error', e => {
          console.log(`FFCreator error: ${e.error}`);
        });

        creator.on('progress', e => {
          console.log(colors.yellow(`FFCreator progress: ${(e.percent * 100) >> 0}%`));
        });

        creator.on('complete', e => {
          console.log(
            colors.magenta(`FFCreator completed: \n USEAGE: ${e.useage} \n PATH: ${e.output} `),
          );

          console.log(colors.green(`\n --- You can press the s key or the w key to restart! --- \n`));
        });

        return creator;
      };



      // module.exports = exemplo => startAndListen(() => FFCreatorCenter.addTask(createFFTask));
      // FFCreatorCenter.start() nao eh necessario ja que o centro automaticamente inicia as tarefas quando estao prontas
      FFCreatorCenter.addTask(createFFTask);
      // ;
    }
  }
}

</script>

<style>


</style>