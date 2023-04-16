# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

import wordle_solver

def main():
    
    lexicon_name = 'sgb_words'
    lexicon = wordle_solver.Lexicon()
    lexicon.load_from_txt('lexicons/'+ lexicon_name + '.txt')

    first_guesses_to_test = wordle_solver.Lexicon()
    first_guesses_to_test.load_from_txt('lexicons/selby_words_shared_with_sgb.txt')

    board = wordle_solver.WordleBoard('aaaaa') # Answer will do nothing here
    guesser = wordle_solver.GuessEvaluator(board, guess_lexicon=first_guesses_to_test, candidate_pool=lexicon)
    player = wordle_solver.ComputerPlayer(lexicon, board, candidate_pool=lexicon)

    score_map = guesser.calc_guess_scores()
    best_words_with_score = player.get_best_guesses_and_scores(score_map)

    dump_filepath = 'out/' + lexicon_name + '_first_guess_scores.txt'
    with open(dump_filepath, mode='w', encoding='utf8') as f:
        f.write('- - - - - BEST WORDS - - - - - \n')
        for word, score in best_words_with_score.items():
            f.write('{}: {} \n'.format(word, score))

        f.write('- - - - - ALL WORDS - - - - - \n')
        for word, score in score_map.items():
            f.write('{}: {} \n'.format(word,score))

if __name__ == '__main__':
    main()