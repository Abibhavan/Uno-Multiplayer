const config = {
  type: Phaser.AUTO,
  width: 1920,
  height: 1080,
  transparent: true,
  backgroundColor: "#ffffff",
  parent: "main-game",
  scale:{
    mode: Phaser.Scale.FIT,
    parent: 'main-game',
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: "arcade",
    debug: true,
  },
  dom: {
    createContainer: true,
  },
  scene: [LoadScene, MainScene],
};

const game = new Phaser.Game(config);
