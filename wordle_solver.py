# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

from random import choice, seed
from copy import deepcopy

BLACK = 0
YELLOW = 1
GREEN = 2
seed(0)

INFINITY = 2**31

class WordleBoard:

    def __init__(self):
        self.guesses = []
        self.results = []
        self.answer = 'aaaaa'

    def make_guess(self, guess):
        self.guesses.append(guess)

        result = [BLACK] * 5
        unnaccounted_guess = [None] * 5
        unnaccounted_answer = []

        for i, letter in enumerate(guess):
            if letter == self.answer[i]:
                result[i] = GREEN
            else:
                unnaccounted_guess[i] = letter
                unnaccounted_answer.append(self.answer[i])

        for i, letter in enumerate(unnaccounted_guess):
            if letter in unnaccounted_answer:
                result[i] = YELLOW
                unnaccounted_answer.remove(letter)

        self.results.append(result)

        return result

    def set_answer(self, answer):
        self.answer = answer

    def copy(self):

        copy_board = WordleBoard()
        copy_board.guesses = deepcopy(self.guesses)
        copy_board.results = self.results.copy()
        copy_board.set_answer(self.answer)

        return copy_board

    def print_board(self):

        for i, word in enumerate(self.guesses):
            print('({},{}) ({},{}) ({},{}) ({},{}), ({},{})'.format(word[0],
                                                            self.results[i][0],
                                                            word[1],
                                                            self.results[i][1],
                                                            word[2],
                                                            self.results[i][2],
                                                            word[3],
                                                            self.results[i][3],
                                                            word[4],
                                                            self.results[i][4]))

class Lexicon:

    def __init__(self):
        self.word_list = []

    def load_from_txt(self, lex_path):

        with open(lex_path, mode='r', encoding='utf8') as f:
            temp_list = f.readlines()

        for i, line in enumerate(temp_list):
            temp_list[i] = line.rstrip('\n')

        self.word_list = temp_list

    def word_match_guess(self, word, guess, result):
        '''
        Based on guess and a result, checks if word could be the answer
        '''

        unaccounted_letters = []

        for i, letter in enumerate(word):
            if result[i] == GREEN:
                if letter != guess[i]:
                    return False
            else:
                unaccounted_letters += letter,

        for i, letter in enumerate(guess):
            if result[i] == YELLOW:
                if letter in unaccounted_letters:
                    unaccounted_letters.remove(letter)
                else:
                    return False

            if result[i] == BLACK:
                if letter in unaccounted_letters:
                    return False

        return True

    def valid_words(self, guess, result):

        to_remove = [word for word in self.word_list if not self.word_match_guess(word, guess, result)]

        for word in to_remove:
            self.word_list.remove(word)

        #self.word_list = [word for word in self.word_list if word not in to_remove]

    def rnd(self):

        return choice(self.word_list)

    def copy(self):
        copy_lexicon = Lexicon()
        copy_lexicon.word_list = self.word_list.copy()
        return copy_lexicon

def best_guess(lexicon, board, candidate_pool):

    information = INFINITY
    best_word = None

    if len(candidate_pool.word_list) == 1:
        return candidate_pool.word_list[0]

    for j, word in enumerate(lexicon.word_list):

        print('Considering guess {}/{}: {}'.format(j, len(lexicon.word_list),
                                                   word))
        current_information = 0

        for i, ans in enumerate(candidate_pool.word_list):

            if not i % 100:
                print('Answer {}/{}'.format(i, len(candidate_pool.word_list)))

            test_board = board.copy()
            test_board.set_answer(ans)

            test_candidate_pool = candidate_pool.copy()

            result = test_board.make_guess(word)
            test_candidate_pool.valid_words(word, result)

            current_information += len(test_candidate_pool.word_list)

            if current_information >= information:
                break

        if current_information < information:
            information = current_information
            best_word = word

    return best_word

def play_wordle(lexicon_path,answer=False):

    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    candidate_pool = lexicon.copy()

    board = WordleBoard()
    if not answer:
        board.set_answer(candidate_pool.rnd())
    else:
        board.set_answer(answer)

    for turn in range(6):
        print('Turn {}'.format(turn + 1))

        guess = best_guess(lexicon, board, candidate_pool)
        result = board.make_guess(guess)
        candidate_pool.valid_words(guess, result)
        board.print_board()

        if result == [GREEN] * 5:
            return turn + 1

    print('The word was {}'.format(board.answer))
    return -1

def main():

    lexicon_path = '500_words_sorted.txt'
    play_wordle(lexicon_path)
    #input('Press enter to q: ')

if __name__ == '__main__':
    main()
