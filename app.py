
from flask import Flask, render_template, session, request, jsonify, redirect
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension



boggle_game = Boggle()
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secretkey'
toolbar = DebugToolbarExtension(app)


@app.route('/')
def make_board():
    board = boggle_game.make_board()
    session['board'] = board
    guesses = session.get('guesses', 0)
    highscore = session.get('highscore', 0)
    
    
    return render_template('base.html', board=board, guesses=guesses, highscore=highscore)


@app.route('/check-guess')
def check_guess():
    
    #Obtain the key/value guess pairs from the guess form
    guess = request.args['guess']
    
    #Process the form data and return a JSON response
    board = session['board']
    res = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': res})


@app.route('/show-score', methods=['POST'])
def show_score():
    score = request.json['score']
    highscore = session.get('highscore')
    
    session['highscore'] = max(score, highscore)
    
    return jsonify(record=score > highscore)