class MainScene extends Phaser.Scene {
    constructor() {
        super("MainScene");

        this.playerCards = [];
        this.opponentHands = {};
        this.topImage = null;
        this.discardCard = null;

        this.MAX_HAND_WIDTH = 800;
        this.CARD_WIDTH = 120; // before scaling
        this.CARD_SCALE = 0.5;
    }

    preload() {
        console.log("MainScene preload");
    }

    /* =============================
       SCENE CREATE
    ============================= */
    create() {
        this.add.image(0, 0, "bg").setOrigin(0);

        this.createDrawDeck();
        this.createDiscardPile();

        // Example initial state
        this.createPlayerHand([
            "Red_0","Green_5","Blue_7","Yellow_2",
            "Red_9","Green_1","Blue_4","Yellow_6",
            "Red_3","Green_8", "Red_0","Green_5","Blue_7","Yellow_2",
            "Red_9","Green_1","Blue_4","Yellow_6",
        ]);

        this.createOpponentHand("p2", 11, "top");
        this.createOpponentHand("p3", 12, "left");
        this.createOpponentHand("p4", 21, "right");
    }

    update() {}

    /* =============================
       DRAW DECK
    ============================= */
    createDrawDeck() {
        let x = 270;
        let y = 100;

        for (let i = 0; i < 35; i++) {
            this.topImage = this.add.image(x, y, "back")
                .setScale(0.45)
                .setOrigin(0)
                .setDepth(1);
            x += 0.4;
            y -= 0.4;
        }

        this.topImage.setInteractive({ cursor: "pointer" });
        this.topImage.on("pointerdown", () => {
            console.log("Draw card clicked");
            // send { type: "draw_card" }
        });
    }

    /* =============================
       DISCARD PILE
    ============================= */
    createDiscardPile() {
        this.discardCard = this.add.image(
            this.cameras.main.centerX,
            this.cameras.main.centerY,
            "Red_5"
        )
        .setScale(0.55)
        .setDepth(2);
    }

    updateTopCard(cardKey) {
        this.discardCard.setTexture(cardKey);
    }

    /* =============================
       PLAYER HAND (DYNAMIC WIDTH)
    ============================= */
    createPlayerHand(hand) {
        this.playerCards.forEach(c => c.destroy());
        this.playerCards = [];

        const count = hand.length;
        if (count === 0) return;

        const cardVisualWidth = this.CARD_WIDTH * this.CARD_SCALE;

        // dynamic gap calculation
        let gap = cardVisualWidth * 0.6;
        const requiredWidth = gap * (count - 1);

        if (requiredWidth > this.MAX_HAND_WIDTH) {
            gap = this.MAX_HAND_WIDTH / (count - 1);
        }

        const maxAngle = Math.min(25, count * 2);
        const mid = (count - 1) / 2;

        const centerX = this.cameras.main.centerX;
        const baseY = this.cameras.main.height - 40;

        hand.forEach((card, i) => {
            const offset = i - mid;

            const x = centerX + offset * gap;
            const y = baseY + Math.abs(offset) * 10;
            const angle = mid === 0 ? 0 : offset * (maxAngle / mid);

            const img = this.add.image(x, y, card)
                .setScale(this.CARD_SCALE)
                .setOrigin(0.5, 1)
                .setAngle(angle)
                .setDepth(10 + i)
                .setInteractive({ cursor: "pointer" });

            img.on("pointerover", () => {
                img.y -= 70;
            });

            img.on("pointerout", () => {
                img.y += 70;
            });

            img.on("pointerdown", () => {
                console.log("Play card:", card);
                // send { type: "play_card", card }
            });

            this.playerCards.push(img);
        });
    }

    /* =============================
       OPPONENT HANDS (FAN STYLE)
    ============================= */
    createOpponentHand(playerId, count, position) {
        if (this.opponentHands[playerId]) {
            this.opponentHands[playerId].forEach(c => c.destroy());
        }

        this.opponentHands[playerId] = [];
        if (count === 0) return;

        let cx, cy, rotationBase, vertical = false;

        switch (position) {
            case "top":
                cx = this.cameras.main.centerX;
                cy = 0;
                rotationBase = 180;
                break;

            case "left":
                cx = 230;
                cy = this.cameras.main.centerY;
                rotationBase = -90;
                vertical = true;
                break;

            case "right":
                cx = this.cameras.main.width;
                cy = this.cameras.main.centerY;
                rotationBase = 90;
                vertical = true;
                break;
        }

        const maxSpread = 300;
        let gap = 30;
        const needed = gap * (count - 1);

        if (needed > maxSpread) {
            gap = maxSpread / (count - 1);
        }

        const maxAngle = 18;
        const mid = (count - 1) / 2;

        for (let i = 0; i < count; i++) {
            const offset = i - mid;
            let x; 
            let y;

            if(position == "top"){
                x = vertical ? cx : cx + offset * gap;
                y = vertical ? cy + offset * gap : cy - Math.abs(offset) * 3;
            }
            else if(position == "left"){
                x = vertical ? cx - Math.abs(offset) * 3 : cx + offset * gap;
                y = vertical ? cy + offset * gap : cy + Math.abs(offset) * 3;
            }
            else{
                x = vertical ? cx + Math.abs(offset) * 3: cx + offset * gap;
                y = vertical ? cy + offset * gap : cy + Math.abs(offset) * 3;
            }

            let angle = rotationBase + (mid === 0 ? 0 : offset * (maxAngle / mid));

            if(position == "top"){
                angle = -1*angle;
            }
            else if(position == "right"){
                angle = -angle;
            }

            const img = this.add.image(x, y, "back")
                .setScale(0.4)
                .setOrigin(0.5, 1)
                .setAngle(angle)
                .setDepth(5 + i);

            this.opponentHands[playerId].push(img);
        }
    }

    /* =============================
       DRAW CARD ANIMATION
    ============================= */
    animateDrawCard(cardKey, targetX, targetY) {
        const card = this.add.image(
            this.topImage.x,
            this.topImage.y,
            "back"
        )
        .setScale(0.45)
        .setOrigin(0)
        .setDepth(20);

        this.tweens.add({
            targets: card,
            x: targetX,
            y: targetY,
            duration: 400,
            ease: "Cubic.easeOut",
            onComplete: () => {
                card.setTexture(cardKey);
            }
        });
    }

    /* =============================
       BACKEND GAME UPDATE
    ============================= */
    onGameUpdate(data) {
        this.createPlayerHand(data.you.hand);
        this.updateTopCard(data.table.top_card);

        data.players.forEach(p => {
            if (!p.isYou) {
                this.createOpponentHand(p.id, p.cards, p.position);
            }
        });
    }
}
