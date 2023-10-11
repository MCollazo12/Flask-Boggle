class Boggle {
	constructor(board, secs = 60) {
		this.secs = secs;
		this.showTimer();

		this.score = 0;
		this.guesses = new Set(); //Set stores unique guessed words
		this.board = board;

    //Set a countdown timer
		//.bind(this) ensures 'this' context is preserved when calling tick
		this.timer = setInterval(this.tick.bind(this), 1000);

    //Listens for user form submissions
		$(".add-guess").on("submit", this.handleGuess.bind(this));
	}

  //Append user's guess to guesses ul on page
	showGuess(guess) {
		$(".guesses").append($("<li>", { text: guess }));
	}

  //Display user's current score
	showScore() {
		$(".score").text(this.score);
	}

  //Displays the time remaining
	showTimer() {
		$(".timer").text(this.secs);
	}

  //Displays a response message to the user
	showResponse(msg) {
		$(".response").text(msg);
	}

  //Handle the timer tick, decrementing every second
	async tick() {
		this.secs -= 1;
		this.showTimer();

    //End game when timer reaches zero and call scoreGame
		if (this.secs == 0) {
			clearInterval(this.timer);
			await this.scoreGame();
		}
	}

  //Handle's user guess input
	async handleGuess(e) {
		e.preventDefault();
		const $guess = $(".guess");
		let guess = $guess.val();

    //Show response if user has already guessed this word
		if (this.guesses.has(guess)) {
			this.showResponse(`Already found "${guess}"`);
			return;
		}

    //Axios request will check user's guess against words on board or
    //in dict using the check_valid_word function
		const res = await axios.get("/check-guess", { params: { guess } });

    //Handle the various JSON response results
		if (res.data.result === "not-word") {
			this.showResponse(`${guess} is not a valid word!`);
		} else if (res.data.result === "not-on-board") {
			this.showResponse(`${guess} is not on the board.`);
		} else {
			this.showGuess(guess);
			this.score += guess.length;
			this.showScore();
			this.guesses.add(guess);
			console.log(this.guesses);
			this.showResponse(`Added '${guess}'`);
		}
	}

  //Handles scoring of the game using Axios requests to backend routes after counter
  //reaches zero
	async scoreGame() {
		$(".add-guess").hide();

		const score = await axios.post("/show-score", { score: this.score });

		if (score.data.newrecord) {
			this.showResponse(`New Highscore: ${score.data.newrecord}`);
		} else {
			const highScoreRes = await axios.get("/get-highscore");
			this.showResponse(
				`Your score: ${this.score} | Highscore: ${highScoreRes.data[0]} | Times Played: ${highScoreRes.data[1]}`
			);
		}
	}
}
