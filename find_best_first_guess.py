# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

from wordle_solver import WordleBoard, Lexicon, GuessEvaluator, INFINITY
import multiprocessing

def calc_for_a_single_guess(guess, board, candidate_pool):

    print('Considering {}'.format(guess))
    guess_evaluator = GuessEvaluator(board, candidate_pool)
    guess_evaluator.evaluate_guess(guess, breakout=False)
    print('{} {}'.format(guess, guess_evaluator.get_expected_candidate_pool_length()))
    return guess_evaluator.get_expected_candidate_pool_length()

def best_first_guess():

    guesses_to_test = Lexicon()
    guesses_to_test.load_from_txt('lexicons/selby_words_shared_with_sgb.txt')

    board = WordleBoard('aaaaa') # answer is irrelevant here

    lexicon = Lexicon()
    lexicon.load_from_txt('lexicons/100_words.txt')

    # https://stackoverflow.com/questions/23816546/how-many-processes-should-i-run-in-parallel

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        scores = pool.starmap(calc_for_a_single_guess, [[guess, board, lexicon] for guess in guesses_to_test.word_list])

    best_score = INFINITY
    best_words = []
    for i, score in enumerate(scores):
        if score < best_score:
            best_words = [(guesses_to_test.word_list[i], score)]
            best_score = score
        elif score == best_score:
            best_words.append((guesses_to_test.word_list[i], score))

    print(best_words)


def main():
    
    best_first_guess()

if __name__ == '__main__':
    main()