# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

from random import choice, seed
from copy import deepcopy

ALPHABET = 'abcdefghijklmnopqrstuvxywz'
BLACK = 0
YELLOW = 1
GREEN = 2
seed(0)

INFINITY = 2**31

class WordleBoard:

    def __init__(self):
        self.guesses = []
        self.results = []

        self.answer = ''
        self.candidate_pool = []

    def recalc_candidate_pool(self, guess, result):

        to_remove = set()

        for word in self.candidate_pool:
            unaccounted_word = list(word)

            for i, letter in enumerate(guess):
                if result[i] == GREEN:
                    if letter != word[i]:
                        to_remove.add(word)
                        #print('{} does not match green {}'.format(word, letter))
                        break
                    else:
                        unaccounted_word.remove(letter)

            # Nicer way to do to avoid lookup. TODO
            if word in to_remove:
                continue

            for i, letter in enumerate(guess):
                if result[i] == YELLOW:
                    if letter in unaccounted_word:
                        unaccounted_word.remove(letter)
                    else:
                        to_remove.add(word)
                        #print('{} does not match yellow {}'.format(word, letter))
                        break
                elif result[i] == BLACK:
                    if letter in unaccounted_word:
                        to_remove.add(word)
                        #print('{} does not match black {}'.format(word, letter))
                        break

        for word in to_remove:
            self.candidate_pool.remove(word)

        #print(to_remove)
        #print(self.candidate_pool)

    def check_guess(self, guess):

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
        self.recalc_candidate_pool(guess, result)

    def make_guess(self, guess):
        self.guesses.append(guess)
        self.check_guess(guess)

    def random_answer(self):
        self.answer = choice(self.candidate_pool)
        print(self.answer)

    def copy(self):

        copy_board = WordleBoard()
        copy_board.guesses = deepcopy(self.guesses)
        copy_board.results = deepcopy(self.results)
        copy_board.answer = self.answer
        copy_board.candidate_pool = deepcopy(self.candidate_pool)

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

def load_lexicon_to_list(lexicon_path):

    with open(lexicon_path, mode='r', encoding='utf8') as f:
        lex_list = f.readlines()

    for i, word in enumerate(lex_list):
        lex_list[i] = word.rstrip('\n')

    return lex_list

def calc_best_guess(lexicon, board):

    information = INFINITY
    best_word = None

    if len(board.candidate_pool) == 1:
        return board.candidate_pool[0]

    for word in lexicon:
        current_information = 0
        for ans in board.candidate_pool:
            print('testing "{}" with answer "{}"'.format(word, ans))
            test_board = board.copy()
            test_board.make_guess(word)
            current_information += len(test_board.candidate_pool)

            if current_information >= information:
                break

        if current_information < information:
            information = current_information
            best_word = word

    return best_word

def main():

    lexicon_path = 'sgb_words_sorted.txt'

    board = WordleBoard()
    lexicon = load_lexicon_to_list(lexicon_path)
    board.candidate_pool = lexicon.copy()
    board.random_answer()

    for turn in range(6):
        print('Turn {}'.format(turn + 1))

        board.make_guess(calc_best_guess(lexicon, board))
        #board.make_guess(input('Enter word: '))
        board.print_board()

        if board.results[turn] == [GREEN] * 5:
            print('YOU WIN')
            break

    else:
        print('YOU LOSE')

    print('The word was {}'.format(board.answer))
    input('Press ENTER to close: ')

if __name__ == '__main__':
    main()
