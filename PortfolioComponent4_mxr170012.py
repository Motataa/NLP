# Portfolio Assignment 4: Ngrams
# Motalib Rahim - mxr170012
# Dr. Karen Mazidi

import nltk  # natural language tool kit
# nltk.download('punkt') # divides text into list of sentences
from collections import Counter  # for count
from nltk.tokenize import word_tokenize  # split text
import pickle  # to store and acess data
import math  # calculation


# to read file as arg
def read(fname):
    file = open(fname, "r")
    text_in = file.readlines()

    text_in = list(map(lambda x: x.strip(), text_in))  # to prevent newline and read text

    tokens = nltk.tokenize.word_tokenize(' '.join(text_in))  # tokenize text

    bigram_list = list(nltk.ngrams(tokens, 2))  # bigram list
    unigram_list = list(nltk.ngrams(tokens, 1))  # unigram list

    bigram_dict = {b: bigram_list.count(b) for b in set(bigram_list)}  # bigram dictionary
    unigram_dict = {t: tokens.count(t) for t in set(tokens)}  # unigram dictionary
    return unigram_dict, bigram_dict  # return both dictionary


if __name__ == '__main__':
    # call 3 times for every lang and pickle
    english_unigram_dict, english_bigram_dict = read('LangId.train.English')
    italian_unigram_dict, italian_bigram_dict = read('LangId.train.Italian')
    french_unigram_dict, french_bigram_dict = read('LangId.train.French')

    with open('english_unigram_dict.pickle', 'wb') as file_in:
        pickle.dump(english_unigram_dict, file_in)

    with open('english_bigram_dict.pickle', 'wb') as file_in:
        pickle.dump(english_bigram_dict, file_in)

    with open('italian_unigram_dict.pickle', 'wb') as file_in:
        pickle.dump(italian_unigram_dict, file_in)

    with open('italian_bigram_dict.pickle', 'wb') as file_in:
        pickle.dump(italian_bigram_dict, file_in)

    with open('french_unigram_dict.pickle', 'wb') as file_in:
        pickle.dump(french_unigram_dict, file_in)

    with open('french_bigram_dict.pickle', 'wb') as file_in:
        pickle.dump(french_bigram_dict, file_in)

    # load the pickled dict for each language / unpickle

    with open('english_unigram_dict.pickle', 'rb') as file:
        english_unigram_dict = pickle.load(file)

    with open('english_bigram_dict.pickle', 'rb') as file:
        english_bigram_dict = pickle.load(file)

    with open('french_unigram_dict.pickle', 'rb') as file:
        french_unigram_dict = pickle.load(file)

    with open('french_bigram_dict.pickle', 'rb') as file:
        french_bigram_dict = pickle.load(file)

    with open('italian_unigram_dict.pickle', 'rb') as file:
        italian_unigram_dict = pickle.load(file)

    with open('italian_bigram_dict.pickle', 'rb') as file:
        italian_unigram_dict = pickle.load(file)

    with open('LangId.test', 'r') as test_file:

        # calculate probability w laplace smoothing
        def compute_prob(text_in, unigram_dict, bigram_dict, N, V):

            p_laplace = 1

            for bigram_list in test_file:
                n = bigram_dict[bigram_list] if bigram_list in bigram_dict else 0
                n_gt = bigram_dict[bigram_list] if bigram_list in bigram_dict else 1 / N
                x = unigram_dict[bigram_list[0]] if bigram_list[0] in unigram_dict else 0
                if x == 0:
                    p_gt = p_gt * (1 / N)
                else:
                    p_gt = p_gt * (n_gt / x)
                p_laplace = p_laplace * ((n + 1) / (x + V))

            print("Laplace smoothing probability is %.5f" % p_laplace)