# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

from random import choice, seed
from copy import deepcopy
import multiprocessing

NUMBER_OF_TURNS = 6

BLACK = 0
YELLOW = 1
GREEN = 2
seed(0)

INFINITY = 2**31

class GuessEvaluator():

    def __init__(self, board, guess_lexicon, candidate_pool):
        self.board = board
        self.guess_lexicon = guess_lexicon
        self.candidate_pool = candidate_pool
    
    def calc_expected_candidate_pool_length(self, guess):

        #print('Considering guess {}'.format(guess))

        candidate_pool_sum = 0

        for ans in self.candidate_pool.word_list:

            test_board = self.board.copy()
            test_board.set_answer(ans)

            test_candidate_pool = self.candidate_pool.copy()

            result = test_board.make_guess(guess)
            test_candidate_pool.valid_words(guess, result)

            candidate_pool_sum += len(test_candidate_pool.word_list)

        return candidate_pool_sum / len(self.candidate_pool.word_list)
    
    def calc_best_guesses(self):
        '''
        Bypasses the resource-heavy creation of a score map for general Wordle play.
        '''

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            scores = pool.map(self.calc_expected_candidate_pool_length, [guess for guess in self.guess_lexicon.word_list])

        best_score = INFINITY
        best_indices = []
        for i, score in enumerate(scores):
            if score < best_score:
                best_score = score
                best_indices = [i]
            elif score == best_score:
                best_indices.append(i)

        best_words = [self.guess_lexicon.word_list[i] for i in best_indices]
        
        return best_words


    def calc_guess_scores(self):

        word_score_map = dict()

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            scores = pool.map(self.calc_expected_candidate_pool_length, [guess for guess in self.guess_lexicon.word_list])

        for i, score in enumerate(scores):
            word_score_map[self.guess_lexicon.word_list[i]] = score

        return word_score_map

class ComputerPlayer():
    
    def __init__(self, lexicon, board, candidate_pool, start_guess=None):
        self.lexicon = lexicon
        self.board = board
        self.candidate_pool = candidate_pool
        self.start_guess = start_guess

        self.turn = 0

    def get_best_guesses_and_scores(self, score_map):

        best_score = INFINITY
        best_words = dict()

        for word, score in score_map.items():
            if score < best_score:
                best_score = score
                best_words = dict()
                best_words[word] = score
            elif score == best_score:
                best_words[word] = score

        return best_words
    
    def get_best_guess(self):
        
        best_guesses = GuessEvaluator(self.board, self.lexicon, self.candidate_pool).calc_best_guesses()

        for word in best_guesses:
            print(word)
            if word in self.candidate_pool.word_list:
                return word
            
        return best_guesses[0]

    def play_wordle(self):

        while self.turn <= NUMBER_OF_TURNS:
            self.turn += 1
            print('Turn {}'.format(self.turn))
            print('{} left in candidate pool'.format(len(self.candidate_pool.word_list)))

            if self.turn == 1 and self.start_guess != None:
                guess = self.start_guess
            else: 
                guess = self.get_best_guess()

            result = self.board.make_guess(guess)
            self.candidate_pool.valid_words(guess, result)
            self.board.print_board()

            if result == [GREEN] * 5:
                return self.turn

        print('The word was {}.'.format(self.board.answer))     
        return -1

def main():

    lexicon_path = 'lexicons/sgb_words.txt'
    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    board = WordleBoard(answer='mange')

    player = ComputerPlayer(lexicon, board, candidate_pool=lexicon.copy(), start_guess='tares')
    final_score = player.play_wordle()

    print('Scored {}'.format(final_score))
    #input('Press enter to q: ')

if __name__ == '__main__':
    main()
