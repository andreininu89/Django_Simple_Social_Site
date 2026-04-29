// Utility: random int
const randomInRange = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

class Star {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.reset();
  }

  reset() {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 1.5 + 0.2;

    this.x = Math.random() * this.width;
    this.y = Math.random() * this.height;

    this.vX = Math.cos(angle) * speed;
    this.vY = Math.sin(angle) * speed;

    this.alpha = Math.random() * 0.8 + 0.2;
  }

  update() {
    this.x += this.vX;
    this.y += this.vY;

    if (
      this.x < 0 || this.x > this.width ||
      this.y < 0 || this.y > this.height
    ) {
      this.reset();
    }
  }
}

class StarBackground {
  constructor(count = 200) {
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d");

    this.stars = [];
    this.count = count;

    this.resize();
    this.initStars();
    this.render = this.render.bind(this);

    window.addEventListener("resize", () => this.resize());

    document.body.appendChild(this.canvas);
    this.render();
  }

  resize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;

    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  initStars() {
    this.stars = Array.from(
      { length: this.count },
      () => new Star(this.width, this.height)
    );
  }

  render() {
    const ctx = this.ctx;

    ctx.clearRect(0, 0, this.width, this.height);

    ctx.fillStyle = "rgba(0,0,0,0.2)";
    ctx.fillRect(0, 0, this.width, this.height);

    for (const star of this.stars) {
      star.update();

      ctx.fillStyle = `rgba(255,255,255,${star.alpha})`;
      ctx.fillRect(star.x, star.y, 1, 1);
    }

    requestAnimationFrame(this.render);
  }
}

// init
new StarBackground(250);
