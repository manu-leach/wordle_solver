# -*- coding: utf-8 -*-

import wordle_clone
from math import log
import multiprocessing

class InformationCalculator():

    def __init__(self, candidate_pool):
        self.candidate_pool = candidate_pool

    def get_guess_p(self, guess, answer):
        guess_checker = wordle_clone.GuessChecker(answer)
        result = guess_checker.check_guess(guess)

        test_candidate_pool = self.candidate_pool.copy()
        test_candidate_pool.valid_words(guess, result)

        p = len(test_candidate_pool.word_list) / len(self.candidate_pool.word_list)

        return p

    def get_expected_information(self, guess):

        print('Considering {}'.format(guess))

        sum = 0
        for answer in self.candidate_pool.word_list:
            p = self.get_guess_p(guess, answer)
            sum -= p * log(p, 2)

        return sum

class ComputerPlayer():

    def __init__(self, lexicon):
        self.lexicon = lexicon

    def get_info_list_in_order_of_lexicon(self, candidate_pool):

        calculator = InformationCalculator(candidate_pool)

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            info_list = pool.map(calculator.get_expected_information, [guess for guess in self.lexicon.word_list])
            

        return info_list

    def get_best_guesses_and_info(self, candidate_pool):

        info_list = self.get_info_list_in_order_of_lexicon(candidate_pool)

        best_info = 0
        best_guesses = []
        for i, guess in enumerate(self.lexicon.word_list):
            info = info_list[i]
            if info > best_info:
                best_info = info
                best_guesses = [guess]
            elif info == best_info:
                best_guesses.append(guess)

        return best_guesses, info
    
    def get_best_guess(self, candidate_pool):

        best_guesses, _ = self.get_best_guesses_and_info(candidate_pool)

        for guess in candidate_pool.word_list:
            return guess
        
        return best_guesses[0]

class ComputerWordleGame(wordle_clone.WordleGame):

    def __init__(self, answer, lexicon, candidate_pool):
        wordle_clone.WordleGame.__init__(self, answer, lexicon)
        self.player = ComputerPlayer(lexicon)
        self.candidate_pool = candidate_pool

    def single_turn(self, guess):
        result = wordle_clone.WordleGame.single_turn(self, guess)
        self.candidate_pool.valid_words(guess, result)
        return result

    def get_guess(self):
        return self.player.get_best_guess(self.candidate_pool)
    
def main():
    
    lexicon_name = 'sgb_words'
    lexicon_path = 'lexicons/{}.txt'.format(lexicon_name)
    lexicon = wordle_clone.Lexicon()
    lexicon.load_from_txt(lexicon_path)

    start_guess = 'tares'

    game = ComputerWordleGame(answer='cigar', lexicon=lexicon, candidate_pool=lexicon.copy())
    game.single_turn(start_guess)
    game.play_wordle()

if __name__ == '__main__':
    main()
