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

    def __init__(self, answer):
        self.guesses = []
        self.results = []
        self.answer = answer

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

        copy_board = WordleBoard(self.answer)
        copy_board.guesses = deepcopy(self.guesses)
        copy_board.results = self.results.copy()

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

class GuessEvaluator():

    def __init__(self, board, candidate_pool):
        self.best_candidate_pool_sum = INFINITY
        self.best_words = []

        self.board = board
        self.candidate_pool = candidate_pool

    def get_best_guess(self):

        for word in self.best_words:
            if word in self.candidate_pool.word_list:
                return word
        
        return self.best_words[0]

    def get_expected_candidate_pool_length(self):
        
        if self.best_candidate_pool_sum == INFINITY:
            return INFINITY
        else:
            return self.best_candidate_pool_sum / len(self.candidate_pool.word_list)
    
    def evaluate_guess(self, guess, breakout=True):

        candidate_pool_sum = 0

        for ans in self.candidate_pool.word_list:

            test_board = self.board.copy()
            test_board.set_answer(ans)

            test_candidate_pool = self.candidate_pool.copy()

            result = test_board.make_guess(guess)
            test_candidate_pool.valid_words(guess, result)

            candidate_pool_sum += len(test_candidate_pool.word_list)

            if breakout and candidate_pool_sum > self.best_candidate_pool_sum:
                return False
            
        if candidate_pool_sum == self.best_candidate_pool_sum:
            self.best_words.append(guess)
        elif candidate_pool_sum < self.best_candidate_pool_sum:
            self.best_candidate_pool_sum = candidate_pool_sum
            self.best_words = [guess]

        return True
    
def best_guess(lexicon, board, candidate_pool, lex_to_test=False):

    information = INFINITY
    best_words = []

    if not lex_to_test:
        lex_to_test = lexicon.copy()

    if len(candidate_pool.word_list) == 1:
        return candidate_pool.word_list[0]
    
    guess_evaluator = GuessEvaluator(board, candidate_pool)

    for j, word in enumerate(lex_to_test.word_list):

        if not j % 100:
            print('Considering guess {}/{}: {}'.format(j, len(lex_to_test.word_list), word))

        guess_evaluator.evaluate_guess(word, breakout=True)

    return guess_evaluator.get_best_guess()

def play_wordle(lexicon_path, first_guess, answer):

    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    candidate_pool = lexicon.copy()

    board = WordleBoard(answer)

    result = board.make_guess(first_guess)
    candidate_pool.valid_words(first_guess, result)
    board.print_board()

    for turn in range(1,6):
        print('Turn {}'.format(turn + 1))
        print('{} left in candidate pool'.format(len(candidate_pool.word_list)))

        guess = best_guess(lexicon, board, candidate_pool)
        result = board.make_guess(guess)
        candidate_pool.valid_words(guess, result)
        board.print_board()

        if result == [GREEN] * 5:
            return turn + 1

    print('The word was {}'.format(board.answer))
    return -1

def main():

    best_start_guess = 'mango'
    lexicon_path = 'lexicons/valid-wordle-words.txt'
    play_wordle(lexicon_path, best_start_guess, 'mangy')

    #print(best_first_guess(lexicon_path))
    #input('Press enter to q: ')

if __name__ == '__main__':
    main()
