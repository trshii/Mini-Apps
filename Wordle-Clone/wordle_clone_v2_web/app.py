from flask import Flask, render_template, request, jsonify
from wordle_model import WordleModel, valid_words
import random

app = Flask(__name__)

target = random.choice(valid_words)
game = WordleModel(target, 6)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def handle_guess():
    data = request.json
    user_guess = data.get('guess').lower()
    verdict = game.check_guess(user_guess)

    return jsonify({
        'verdict': [v.name for v in verdict],
        'is_game_over': game.is_game_over,
        'won': game.did_player_win,
        'target': target.upper()
    })

if __name__ == '__main__':
    app.run(debug=True)

