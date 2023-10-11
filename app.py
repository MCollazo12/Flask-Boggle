from flask import Flask, render_template, session, request, jsonify, redirect
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "secretkey"
toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()


@app.route("/")
def make_board():
    """
    Default route for rendering a new Boggle game board

    Generates a new board, stores it within the session, and retrieves # of guesses,
    the user's highscore, and the number of times played to render on the HTML template.
    """

    board = boggle_game.make_board()
    session["board"] = board

    guesses = session.get("guesses", 0)
    highscore = session.get("highscore", 0)
    num_plays = session.get("numplays", 0)

    return render_template(
        "index.html",
        board=board,
        guesses=guesses,
        highscore=highscore,
        num_plays=num_plays,
    )


@app.route("/check-guess")
def check_guess():
    """
    Route for checking if a guessed word is valid.
    
    Retrieves the guessed words from the input form, checks whether it is valid
    using the function 'check_valid_word' in Boggle.py, and returns a JSON 
    response with the result.
    """
    
    # Obtain the key/value guess pairs from the guess form
    guess = request.args["guess"]

    # Process the form data and return a JSON response
    board = session["board"]
    res = boggle_game.check_valid_word(board, guess)
    return jsonify({"result": res})


@app.route("/show-score", methods=["POST"])
def show_score():
    """
    Route for handling and updating the user's score.
    
    Receives the player's score as JSON data, compares it to the highscore stored 
    in the session, and updates the highscore if the new score is higher. Also keeps
    track of the number of times the user has played.
    """
    
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    session["highscore"] = max(score, highscore)
    session["num_plays"] = num_plays + 1

    return jsonify(newrecord=score > highscore)


@app.route("/get-highscore")
def get_highscore():
    """
    Route for retrieving the highscore and number of times played from the session.
    
    Returns both in a JSON response to be displayed on the page.
    """
    
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)
    return jsonify(highscore, num_plays)
