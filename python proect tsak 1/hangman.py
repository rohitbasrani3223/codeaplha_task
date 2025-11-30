import random

# --- Game Assets ---

# This list holds the ASCII art for the hangman stages.
HANGMAN_PICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# List of words for the game.
# You can easily add more words here!
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()

# --- Helper Functions ---

def get_random_word(word_list):
    """
    Returns a random string from the passed list of strings.
    """
    word_index = random.randint(0, len(word_list) - 1)
    return word_list[word_index]

def display_board(missed_letters, correct_letters, secret_word):
    """
    Displays the current state of the game: the hangman art,
    missed letters, and the partially guessed word.
    """
    # Show the hangman ASCII art based on the number of missed guesses
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    # Show the letters the player has missed
    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()
    print()

    # Create a string of underscores for the secret word
    blanks = '_' * len(secret_word)

    # Replace blanks with correctly guessed letters
    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    # Show the secret word with spaces between letters
    for letter in blanks:
        print(letter, end=' ')
    print()
    print()

def get_guess(already_guessed):
    """
    Gets a single letter guess from the player.
    Ensures the guess is a valid letter and hasn't been guessed before.
    """
    while True:
        print('Guess a letter:')
        guess = input()
        guess = guess.lower() # Make the guess lowercase
        
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif not guess.isalpha(): # Check if it's a letter
            print('Please enter a LETTER.')
        else:
            return guess

def check_win(secret_word, correct_letters):
    """
    Checks if the player has won by guessing all the letters.
    """
    found_all_letters = True
    for i in range(len(secret_word)):
        if secret_word[i] not in correct_letters:
            found_all_letters = False
            break
    return found_all_letters

# --- Main Game Logic ---

print('H A N G M A N')

# These strings will store the letters the player has guessed
missed_letters = ''
correct_letters = ''

# Get a random word for the player to guess
secret_word = get_random_word(words)
game_is_done = False

# Main game loop
while True:
    # Display the current game state
    display_board(missed_letters, correct_letters, secret_word)

    # Let the player enter a guess
    guess = get_guess(missed_letters + correct_letters)

    if guess in secret_word:
        # The player guessed correctly
        correct_letters = correct_letters + guess

        # Check if the player has won
        if check_win(secret_word, correct_letters):
            display_board(missed_letters, correct_letters, secret_word)
            print('Yes! The secret word is "' + secret_word + '"! You have won!')
            game_is_done = True
    else:
        # The player guessed incorrectly
        missed_letters = missed_letters + guess

        # Check if player has run out of guesses (lost)
        if len(missed_letters) == len(HANGMAN_PICS) - 1:
            display_board(missed_letters, correct_letters, secret_word)
            print('You have run out of guesses!\nAfter ' + str(len(missed_letters)) + ' missed guesses and ' + str(len(correct_letters)) + ' correct guesses, the word was "' + secret_word + '"')
            game_is_done = True

    # If the game is done (win or loss), ask to play again
    if game_is_done:
        print('Do you want to play again? (yes or no)')
        if not input().lower().startswith('y'):
            break # Exit the loop and end the game
        else:
            # Reset the game
            missed_letters = ''
            correct_letters = ''
            game_is_done = False
            secret_word = get_random_word(words)