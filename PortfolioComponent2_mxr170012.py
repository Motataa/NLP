# Portfolio Component 2: Word Guessing Game
# Motalib Rahim (mxr170012)

import sys # for sys parameter
import nltk # for preprocessing text data
import random # for random modules
from nltk.corpus import stopwords # to prevent common words
from nltk.tokenize import word_tokenize # tokenize sentence
from nltk.stem import WordNetLemmatizer # to return the base form of a word

# reads in the file in sys arg
def read_file(filename):
    with open(filename, 'r') as f:
        raw_text = f.read()
    return raw_text

# lexical diversity of tokenized raw_text
def calculate_lexical(raw_text):
    tokens = word_tokenize(raw_text.lower()) # tokenize lower case raw text
    # only raw text are tokenized with length over 5
    tokens = [token for token in tokens if token.isalpha() and token not in stopwords.words('english') and len(token) > 5]
    # lexical diversity calculation no. of unique tokens by total number of tokens
    lexical = len(set(tokens)) / len(tokens)
    return (lexical)


# function that preprocess raw_text
# function that preprocess raw_text
def preprocess_raw_text(raw_text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(raw_text.lower())
    tokens = [token for token in tokens if
              token.isalpha() and token not in stopwords.words('english') and len(token) > 5]
    lemmas = set(lemmatizer.lemmatize(token) for token in tokens)
    pos_tagged = nltk.pos_tag(list(lemmas))  # pos tag on unique lemmas
    print(pos_tagged[:20])  # prints the first 20
    nouns = [lemma for lemma, pos in pos_tagged if pos.startswith('N')]  # list of lemmas only nouns

    print(f"No. of tokens: {len(tokens)}")
    print(f"No. of nouns: {len(nouns)}")
    return tokens, nouns

# dictionary for items in list of tokens and nouns
def common_noun(nouns, tokens):
    # sort dictionary by count
    noun_counts = {}
    for noun in nouns:
        count = tokens.count(noun)
        noun_counts[noun] = count
    sorted_nouns = sorted(noun_counts.items(), key=lambda x: x[1], reverse=True)
    common_nouns = [noun for noun, count in sorted_nouns[:50]]
    print(f"Top 50 nouns: {common_nouns}")
    return common_nouns

#guessing game function
def guessing_game(words):
    total_score = 5 # game starts with 5 points or when '!' is inputted
    while total_score >= 0: # game ends score below 0
        word = random.choice(words) # chooses one of the 50 words list
        top_words = list(word)
        print("Word Guessing Game!")
        guessed = ['_'] * len(word) # underscore for each letter of the word
        letter_guessed = set()
        while '_' in guessed and total_score >= 0:
            print(''.join(guessed))
            letter = input("Guess a letter: ")
            if letter == '!': # end game when user inputs ! as a letter
                print("Game over, final score:", total_score)
                return
            if letter in top_words: # letter exists in the word
                if letter not in letter_guessed:
                    print("Right!")
                    for i in range(len(top_words)):
                        if top_words[i] == letter:
                            guessed[i] = letter
                    total_score += 1 # add a point to the total score
                    letter_guessed.add(letter)
                else: print('You already guessed the letter!')
            else:
                print("Sorry, guess again") # if letter doesnt exist
                total_score -= 1 # negative scoring
            print(f"Total score for guessed word: {total_score}") # total score
        total_score += len(top_words)
        print("Sorry, game over!") # once the whole word is completed
        return


if __name__ == '__main__':
    if len(sys.argv) < 2: # checks for the file in a sys arg
        print("Error: Check if the file is valid.")  # when file doesn't exist
        sys.exit()
    filename = sys.argv[1]
    raw_text = read_file(filename)
    lexical = calculate_lexical(raw_text)
    print(f"Lexical diversity: {lexical:.2f}") # prints lexical diversity in 2 decimal
    tokens, nouns = preprocess_raw_text(raw_text)
    top_nouns = common_noun(nouns, tokens)
    guessing_game(top_nouns)