# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

import wordle_clone
import wordle_solver

def main():

    test_solutions_name = 'test_solutions'
    test_solutions = wordle_clone.Lexicon()
    test_solutions.load_from_txt('solutions/{}.txt'.format(test_solutions_name))

    lexicon_name = 'sgb_words'
    lexicon_path = 'lexicons/{}.txt'.format(lexicon_name)
    lexicon = wordle_clone.Lexicon()
    lexicon.load_from_txt(lexicon_path)

    start_guess = 'tares'

    output_filename = input('Output file: ')
    output_filepath = 'out/{}.txt'.format(output_filename)

    with open(output_filepath, mode='w', encoding='utf8') as f:
        f.write('Lexicon: {}\n'.format(lexicon_name))
        f.write('Solution set: {}'.format(test_solutions_name))

    score_list = []
    for answer in test_solutions.word_list:
        game = wordle_solver.ComputerWordleGame(answer, lexicon=lexicon, candidate_pool=lexicon.copy())
        game.single_turn(start_guess)
        score = game.play_wordle()
        score_list.append(score)

    with open(output_filepath, mode='a', encoding='utf8') as f:
        for i, score in enumerate(score_list):
            f.write('- - - - - Test {}: {} - - - - -\n'.format(i+1, test_solutions.word_list[i]))
            f.write('Score: {}\n'.format(score))

if __name__ == '__main__':
    main()