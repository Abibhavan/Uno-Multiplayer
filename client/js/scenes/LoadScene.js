class LoadScene extends Phaser.Scene {
  constructor() {
    super("LoadScene");
  }

  preload() {
    console.log("preloading");
    
    const { width, height } = this.cameras.main;

    // ---------- 0. Load "back" first ----------
    this.load.image("back", "/client/images/back.jpg");
    this.load.image("bg", "/client/images/bg.jpg");

    // Once the back image is loaded, start loading animation
    this.load.once("complete", () => {
      this.startLoadingAnimation();
      this.startAssetLoading();
    });

    this.load.start(); // force loading "back"
  }

  startLoadingAnimation() {
    this.add.image(0, 0, 'bg').setOrigin(0)
    const { width, height } = this.cameras.main;

    // ---------- 1. Loading text ----------
    this.loadingText = this.add
      .text(width / 2, height / 2 + 100, "Loading...", {
        font: "40px Arial",
        fill: "#ffffff",
      })
      .setOrigin(0.5);

    // ---------- 2. Loading percentage ----------
    this.percentText = this.add
      .text(width / 2, height / 2 + 150, "0%", {
        font: "28px Arial",
        fill: "#ffffff",
      })
      .setOrigin(0.5);

    // ---------- 3. Card fan animation ----------
    this.cards = [];
    const cardCount = 7;
    const spacing = 30;

    for (let i = 0; i < cardCount; i++) {
      let card = this.add.image(
        width / 2 + (i - Math.floor(cardCount / 2)) * spacing,
        height / 2 - 100,
        "back"
      );
      card.setOrigin(0.5);
      card.setScale(0.25);
      card.angle = -15 + i * 5; // fan effect
      this.cards.push(card);
    }

    this.tweens.add({
      targets: this.cards,
      y: `+=15`,
      duration: 600,
      yoyo: true,
      repeat: -1,
      ease: "Sine.easeInOut",
      delay: this.cards.map((c, i) => i * 100),
    });
  }

  startAssetLoading() {
    // ---------- 4. Load card assets ----------
    const colors = ["Red", "Blue", "Yellow", "Green"];
    colors.forEach((color) => {
      for (let i = 0; i <= 9; i++) {
        this.load.image(`${color}_${i}`, `/client/images/${color}_${i}.jpg`);
      }
    });

    const powerCards = ["Draw_2", "Reverse", "Skip"];
    colors.forEach((color) => {
      powerCards.forEach((card) => {
        this.load.image(`${color}_${card}`, `/client/images/${color}_${card}.jpg`);
      });
    });

    this.load.image("wild_4", "/client/images/Wild_Draw_4.jpg");
    this.load.image("wild", "/client/images/Wild_Wild.jpg");

    // ---------- 5. Update loading progress ----------
    this.load.on("progress", (value) => {
      this.percentText.setText(parseInt(value * 100) + "%");
    });
    console.log("Doing preload");
    
    this.load.on("complete", () => {
      console.log("Starting mainscene");
      this.time.delayedCall(2000, () => {
        
        this.scene.start("MainScene");
      });
    });

    this.load.start(); // start loading remaining assets
  }
}
