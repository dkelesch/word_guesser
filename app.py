from flask import Flask, render_template, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here' # Important for session management

# --- Word List Definition ---
# You should replace this with your actual list of 56 words.
# 7 words for each length from 3 to 10.
WORDS_BY_LENGTH = {
    3: ["cat", "dog", "sun", "run", "fly", "sky", "key"],
    4: ["boat", "lamp", "fish", "tree", "book", "moon", "star"],
    5: ["apple", "grape", "dream", "house", "light", "mouse", "earth"],
    6: ["banana", "purple", "window", "guitar", "summer", "forest", "spirit"],
    7: ["chicken", "rainbow", "journey", "freedom", "library", "diamond", "example"],
    8: ["elephant", "mountain", "sunshine", "umbrella", "computer", "treasure", "solution"],
    9: ["adventure", "pineapple", "knowledge", "happiness", "butterfly", "chocolate", "wonderful"],
    10: ["strawberry", "friendship", "meditation", "technology", "connection", "celebrate", "understand"]
}

# Flatten the list and shuffle it for variety
ALL_WORDS = []
for length_category in WORDS_BY_LENGTH.values():
    ALL_WORDS.extend(length_category)
random.shuffle(ALL_WORDS) # Shuffle once at the start

# --- Helper Functions ---
def setup_new_word():
    """Sets up a new word for the game session."""
    if 'current_word_index' not in session or session['current_word_index'] >= len(ALL_WORDS) -1:
        session['current_word_index'] = 0 # Loop back or end game
        # Optional: Re-shuffle if looping
        # random.shuffle(ALL_WORDS)
    else:
        session['current_word_index'] += 1

    current_word = ALL_WORDS[session['current_word_index']]
    session['current_word'] = current_word
    session['displayed_letters'] = ['_'] * len(current_word)
    # Removed: session['revealed_indices'] = set() # This was causing the JSON error

# --- Routes ---
@app.route('/')
def index():
    if 'current_word' not in session:
        # Initialize game for the first time or if session expired
        session['current_word_index'] = -1 # So setup_new_word starts from 0
        setup_new_word()
    return render_template('index.html')

@app.route('/get_current_word_state', methods=['GET'])
def get_current_word_state():
    if 'current_word' not in session:
         # This case should ideally be handled by '/' redirecting or pre-populating
        session['current_word_index'] = -1
        setup_new_word()

    return jsonify({
        'slots': session.get('displayed_letters', []),
        'message': "Game loaded."
    })

@app.route('/next_word', methods=['POST'])
def next_word():
    setup_new_word()
    return jsonify({
        'slots': session['displayed_letters'],
        'message': "Yeni kelime hazır!"
    })

@app.route('/reveal_letter', methods=['POST'])
def reveal_letter():
    if 'current_word' not in session or not session['current_word']:
        return jsonify({'error': 'No active word'}), 400

    current_word = session['current_word']
    displayed_letters = list(session['displayed_letters']) # Make a mutable copy

    # Find indices that haven't been revealed yet (where slot is '_')
    unrevealed_letter_indices = [i for i, char_slot in enumerate(displayed_letters) if char_slot == '_']

    if not unrevealed_letter_indices:
        return jsonify({
            'slots': displayed_letters,
            'message': "All letters already revealed!"
        })

    random_index_to_reveal = random.choice(unrevealed_letter_indices)
    
    displayed_letters[random_index_to_reveal] = current_word[random_index_to_reveal]

    session['displayed_letters'] = displayed_letters # Store the updated list
    
    message = f"İpucu Harf: '{current_word[random_index_to_reveal]}'"
    if all(slot != '_' for slot in displayed_letters): # Check if all letters are revealed
        message += " - Kelime açıklandı!"

    return jsonify({
        'slots': displayed_letters,
        'message': message
    })

@app.route('/reveal_word', methods=['POST'])
def reveal_word():
    if 'current_word' not in session or not session['current_word']:
        return jsonify({'error': 'No active word'}), 400

    current_word = session['current_word']
    session['displayed_letters'] = list(current_word) # Reveal all letters
    # Removed: session['revealed_indices'] = set(range(len(current_word)))

    return jsonify({
        'slots': session['displayed_letters'],
        'message': "Kelime açıklandı!"
    })

if __name__ == '__main__':
    app.run(debug=True)