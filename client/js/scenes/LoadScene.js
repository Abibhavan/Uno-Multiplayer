class LoadScene extends Phaser.Scene {
  constructor() {
    super("LoadScene");
  }

  preload() {
    // Card back
    this.load.image("back", "/client/images/back.jpg");

    // Number cards
    const colors = ["Red", "Blue", "Yellow", "Green"];
    colors.forEach((color) => {
      for (let i = 0; i <= 9; i++) {
        this.load.image(
          `${color}_${i}`,
          `/client/images/${color}_${i}.jpg`
        );
      }
    });

    // Power cards
    const powerCards = ["Draw_2", "Reverse", "Skip"];
    colors.forEach((color) => {
      powerCards.forEach((card) => {
        this.load.image(
          `${color}_${card}`,
          `/client/images/${color}_${card}.jpg`
        );
      });
    });

    // Wild cards
    this.load.image("wild_4", "/client/images/Wild_Draw_4.jpg");
    this.load.image("wild", "/client/images/Wild_Wild.jpg");
  }

  create() {
    this.add.image(960, 540, "Red_9").setOrigin(0.5);
  }
}
