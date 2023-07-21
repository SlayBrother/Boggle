from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.debug = True

toolbar = DebugToolbarExtension

boggle_game = Boggle()

RESPONSES = []

@app.route('/')
def home_link():
    return render_template('home.html')

@app.route('/boggle')
def play_boggle():

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    # # if 'board' not in session:
    # #     session['board'] =  boggle_game.make_board()
    
    # # board = session['board']

    # user_input = ''

    # if request.method == 'POST':
    #     user_input = request.form.get('user_input')

    #     if user_input:    
    #         if 'user_inputs' not in session:
    #             session['user_inputs'] = []
    #         session['user_inputs'].append(user_input)

    # print(f"User Input: {user_input}")

    return render_template('boggle.html', board=board, highscore = highscore, nplays=nplays)


@app.route("/check-word")
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result': response})
                
    
@app.route("/post-score", methods=["POST"])
def post_score():

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['plays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)


    # for entry in words:
    #     if word == entry:
    #         for i in range(0, (word)):
    #             if (word[i] =< 2):
    #                 return "Valid word"