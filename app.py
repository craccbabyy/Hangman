import os
from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
from RandomWords import easy_wordlist, medium_wordlist, hard_wordlist, insane_wordlist, wrong_answer_replies, correct_answer_replies

DB_PATH = '/var/www/hangman/scores.db'

app = Flask(__name__)
app.secret_key = 'your_secret_key'
HANGMAN_PICS = [
    # 0
    """
     +---+
     |   |
         |
         |
         |
         |
         |
    =========
    """,
    # 1
    """
     +---+
     |   |
     O   |
         |
         |
         |
         |
    =========
    """,
    # 2
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
         |
    =========
    """,
    # 3
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
         |
    =========
    """,
    # 4
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
         |
    =========
    """,
    # 5
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
         |
    =========
    """, 
    # 6 
    """ 
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
         |
    =========
    """,
    # 7
    """
     +---+
     |   |
     O   |
    /|\\  |
   _/ \\  |
         |
    =========
    """,
    # 8
    """
     +---+
     |   |
     O   |
    /|\\  |
   _/ \\_ |
   R.I.P.|
    =========
    """
]

def get_word_by_difficulty(difficulty):
    if difficulty == "easy":
        return random.choice(easy_wordlist), 0, 8
    elif difficulty == "medium":
        return random.choice(medium_wordlist), 2, 6
    elif difficulty == "hard":
        return random.choice(hard_wordlist), 4, 4
    elif difficulty == "insane":
        return random.choice(insane_wordlist), 5, 3
    else:
        return random.choice(medium_wordlist), 2, 6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    difficulty = request.form['difficulty']
    word, initial_gallows, max_wrong = get_word_by_difficulty(difficulty)
    session['word'] = word.upper()
    session['guessed_letters'] = []
    session['wrong_guesses'] = 0
    session['initial_gallows'] = initial_gallows
    session['max_wrong'] = max_wrong
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'word' not in session:
        return redirect(url_for('index'))

    word = session['word']
    guessed_letters = session['guessed_letters']
    wrong_guesses = session['wrong_guesses']
    initial_gallows = session['initial_gallows']
    max_wrong = session['max_wrong']
    message = ""
    remaining_guesses = max_wrong - wrong_guesses

    if request.method == 'POST':
        guess = request.form['guess'].upper()
        if not guess.isalpha() or len(guess) != 1:
            message = "PLEASE enter a LETTER!! No Numbers or $ymbols in HANGMAN!!"
        elif guess in guessed_letters:
            message = f"You Already GUESSED '{guess}'. 🤨Try a NEW letter!"
        else:
            guessed_letters.append(guess)
            if guess not in word:
                wrong_guesses += 1
                message = f"❌{ random.choice(wrong_answer_replies) }"
            else:
                message = f"{random.choice(correct_answer_replies)} '{guess}' is in the WORD!"

        session['guessed_letters'] = guessed_letters
        session['wrong_guesses'] = wrong_guesses

    word_display = " ".join([letter if letter in guessed_letters else "_" for letter in word])

    #DISPLAY LOGIC got moved down a bit

    # ✅ WIN
    if all(letter in guessed_letters for letter in word):
        gallows_phase = min(initial_gallows + wrong_guesses, len(HANGMAN_PICS) - 1)
        hangman_state = HANGMAN_PICS[gallows_phase].rstrip()

        return render_template('game.html',
            word=word,
            word_display=word,
            hangman_state=HANGMAN_PICS[gallows_phase].rstrip(),
            message="You Won! 🎉",
            game_over=True,
            guessed_letters=guessed_letters,
            gallows_phase=gallows_phase,
            revealed_word=word,
            win=True,  # 👈 tell the template this is a win
            remaining_guesses=remaining_guesses
        )

    #  ✅ LOSS — show RIP / FIRST - clamp the game-over art
    if wrong_guesses >= max_wrong: # NEED TO DO SOME THINGS BEFORE THE DISPLAY LOGIC
        gallows_phase = min(initial_gallows + wrong_guesses, len(HANGMAN_PICS) - 1)
        hangman_state = HANGMAN_PICS[gallows_phase].rstrip()
        remaining_guesses = max_wrong - wrong_guesses

        return render_template('game.html',
            remaining_guesses=remaining_guesses,
            word=word,
            word_display=word_display,
            hangman_state=hangman_state,
            message="❌Game Over!❌",
            game_over=True,
            guessed_letters=guessed_letters,
            gallows_phase=gallows_phase,
            revealed_word=word
        )
    # NORMAL PLAY (ONLY show UP TO phase 7!!)
    gallows_phase = min(initial_gallows + wrong_guesses, 7) # this is where we fixed
    hangman_state = HANGMAN_PICS[gallows_phase].rstrip()

    return render_template('game.html',
        word_display=word_display,
        hangman_state=hangman_state,
        message=message,
        guessed_letters=guessed_letters,
        game_over=False,
        gallows_phase=gallows_phase,
        remaining_guesses=remaining_guesses
    )

@app.route('/enter-name', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form['name']
        save_score(name)
        session.clear()
        return redirect(url_for('highscores'))
    return render_template('enter_name.html')

def save_score(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (name TEXT, wins INTEGER)''')
    c.execute('SELECT wins FROM scores WHERE name = ?', (name,))
    result = c.fetchone()
    if result:
        c.execute('UPDATE scores SET wins = wins + 1 WHERE name = ?', (name,))
    else:
        c.execute('INSERT INTO scores (name, wins) VALUES (?, 1)', (name,))
    conn.commit()
    conn.close()

@app.route('/highscores')
def highscores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, wins FROM scores ORDER BY wins DESC LIMIT 10')
    scores = c.fetchall()
    conn.close()
    return render_template('highscores.html', scores=scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

