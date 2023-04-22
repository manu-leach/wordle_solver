# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

import wordle_clone
import wordle_solver

def main():
    
    lexicon_name = 'sgb_words'
    lexicon_path = 'lexicons/{}.txt'.format(lexicon_name)
    lexicon = wordle_clone.Lexicon()
    lexicon.load_from_txt(lexicon_path)

    test_guesses_name = 'selby_words_shared_with_sgb'
    test_guesses_path = 'lexicons/{}.txt'.format(test_guesses_name)
    test_guesses = wordle_clone.Lexicon()
    test_guesses.load_from_txt(test_guesses_path)

    dump_filepath = 'out/' + lexicon_name + '_first_guess_scores.txt'
    with open(dump_filepath, mode='w', encoding='utf8') as f:
        f.write('Lexicon: {}\n'.format(lexicon_name))

    player = wordle_solver.ComputerPlayer(test_guesses)
    info_list = player.get_info_list_in_order_of_lexicon(candidate_pool=lexicon)
    best_guesses, _ = player.get_best_guesses_and_info(info_list)
    
    print('Best guesses: {}'.format(best_guesses))

    with open(dump_filepath, mode='a', encoding='utf8') as f:
        f.write('Best guesses: {}\n'.format(best_guesses))
        f.write('- - - - - All words - - - - -\n')
        for i, info in enumerate(info_list):
            f.write('{}: {}\n'.format(test_guesses.word_list[i], info))

if __name__ == '__main__':
    main()