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

    def valid_words(self, guess, result):

        to_remove = set()

        for word in self.word_list:
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
            self.word_list.remove(word)

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

    for word in lexicon.word_list:
        current_information = 0

        for ans in candidate_pool.word_list:
            print('testing "{}" with answer "{}"'.format(word, ans))
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

def play_wordle(lexicon_path):

    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    candidate_pool = lexicon.copy()

    board = WordleBoard()
    board.set_answer(candidate_pool.rnd())

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

    lexicon_path = '100_words_sorted.txt'
    play_wordle(lexicon_path)
    input('Press enter to q: ')
    
if __name__ == '__main__':
    main()
