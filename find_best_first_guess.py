# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

from wordle_solver import WordleBoard, Lexicon, GuessEvaluator
import multiprocessing

def calc_for_a_single_guess(guess, board, candidate_pool):

    print('Considering {}'.format(guess))
    guess_evaluator = GuessEvaluator(board, candidate_pool)
    guess_evaluator.evaluate_guess(guess, breakout=False)
    print('{} has expected pool length {}'.format(guess, guess_evaluator.get_expected_candidate_pool_length()))

def use_threaded_maybe():

    guesses_to_test = Lexicon()
    guesses_to_test.load_from_txt('lexicons/selby_words_shared_with_sgb.txt')

    board = WordleBoard('aaaaa') # answer is irrelevant here

    lexicon = Lexicon()
    lexicon.load_from_txt('lexicons/sgb_words.txt')

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for guess in guesses_to_test.word_list:
        pool.apply_async(calc_for_a_single_guess, args=(guess, board, lexicon))

    pool.close()
    pool.join()

def best_first_guess():

    guesses_to_test = Lexicon()
    guesses_to_test.load_from_txt('lexicons/selby_words_shared_with_sgb.txt')

    board = WordleBoard('aaaaa') # answer is irrelevant here

    lexicon = Lexicon()
    lexicon.load_from_txt('lexicons/sgb_words.txt')

    guess_evaluator = GuessEvaluator(board, candidate_pool=lexicon)
    
    for i, guess in enumerate(guesses_to_test.word_list):

        print('Considering guess {}/{}: {}'.format(i+1, len(guesses_to_test.word_list), guess))
        guess_evaluator.evaluate_guess(guess, breakout=True)

    print(guess_evaluator.best_words)

def main():
    
    use_threaded_maybe()

if __name__ == '__main__':
    main()