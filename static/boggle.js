class Boggle {
  constructor(board, secs = 60) {
    this.secs = secs;
    this.showTimer();

    this.score = 0;
    this.guesses = new Set();
    this.board = board;

    //.bind(this) ensures 'this' context is preserved when calling tick
    this.timer = setInterval(this.tick.bind(this), 1000);

    $('.add-guess').on('submit', this.handleGuess.bind(this));
  }
  showGuess(guess) {
    $('.guesses').append($('<li>', { text: guess }));
  }

  showScore() {
    $('.score').text(this.score);
  }

  showTimer() {
    $('.timer').text(this.secs);
  }

  showResponse(msg) {
    $('.response').text(msg)
  }

  async tick() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs <= 0) {
      clearInterval(this.timer);
      //   await this.scoreGame();
    }
  }

  async handleGuess(e) {
    e.preventDefault();
    const $guess = $('.guess');
    let guess = $guess.val();

    if (this.guesses.has(guess)) {
      this.showResponse(`Already found "${guess}"`);
      return;
    }

    const res = await axios.get('/check-guess', { params: { guess } });

    if (res.data.result === "not-word") {
      this.showResponse(`${guess} is not a valid word!`)
    } else if (res.data.result === 'not-on-board') {
      this.showResponse(`${guess} is not on the board.`);
    } else {
      this.showGuess(guess);
      this.score += guess.length;
      this.showScore();
      this.guesses.add(guess)
      console.log(this.guesses)
      this.showResponse(`Added '${guess}'`)
    }
  }

  async showScore
}
