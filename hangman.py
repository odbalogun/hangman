def config_loader() -> dict:
    """
    Returns the configuration file as a dictionary
    """
    import json

    with open("config.json") as config_file:
        config = json.load(config_file)
    return config

# load configuration
CONFIG = config_loader()

def close():
    """
    Exits the program
    """
    print("Exiting...")
    exit()

def get_word_from_mode(game_mode: dict) -> str:
    """
    Returns a random word from the game_mode's list of words
    """
    import random
    return random.choice(game_mode.get('words'))

def fetch_word(game_mode: dict) -> str:
    """
    Returns a random word either from the api or from the game_mode's list of words
    """
    import requests
    import os

    params = {'random': 'true', 'letters': game_mode.get('length')}
    headers = {'Authorization': os.getenv('RAPID_API_KEY')}

    try:
        # setting timeout because of inconsistent API responses
        r = requests.get(CONFIG.get('words-api'), params=params, headers=headers, timeout=5)
        # check status code and raise HTTP error if necessary
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        data = r.json()
        return data.get('word')
        # checking for ValueError to catch improperly formed JSON responses
    except (requests.exceptions.RequestException, ValueError):
        return get_word_from_mode(game_mode)

def guess_letter(guesses: str) -> str:
    import string
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) > 1:
            print("You can only guess one letter at a time \n")
        elif guess in guesses:
            print("You have already guessed this letter \n")
        elif guess not in string.ascii_lowercase:
            print("Please enter only characters \n")
        else:
            return guess


def display_word(word: str, guesses: str):
    display = ''
    for x in word:
        if x in guesses:
            display += x
        else:
            display += '_'
    print(display + "\n")

def play(word: str, max_wrong_guesses: int):
    print("Guess the word:")

    guesses = correct_guesses = ''
    while max_wrong_guesses > 0:
        # show status of word
        display_word(word, correct_guesses)
        # ask user to guess a letter
        guess = guess_letter(guesses)
        
        if guess in word:
            # if letter is correct, add to correct_guesses
            correct_guesses += guess
            print("Correct!")

            # check if all letters have been found
            if (set(word).issubset(set(correct_guesses))):
                print(f"Congratulations! You found the word {word}")
                close()
        else:
            max_wrong_guesses -= 1
            print("Wrong...")
            print(f"You have {max_wrong_guesses} guess(es) left")

            if max_wrong_guesses == 0:
                print("You lose...")
                print(f"The word is {word}")
        # add to guesses
        guesses += guess


print("Welcome to Hangman!!! \n")

username = input("What is your name? ")

while True:
    difficulty = input(
f'''
Hi, {username}! Choose your difficulty level:
    - Easy
    - Normal
    - Hard
''' 
).lower()

    # check if provided difficulty is valid
    if difficulty not in CONFIG.get('modes').keys():
        print("Invalid difficulty selected. Please select one of the available choices")
        continue

    mode = CONFIG.get('modes').get(difficulty)
    word = fetch_word(mode)
    play(word, max_wrong_guesses=mode.get('wrong_guesses'))

    check = input("Play again (Y/n)? ")
    if check.lower() == 'y':
        continue
    break

close()

