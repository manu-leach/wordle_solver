# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

import wordle_solver

def main():

    test_solutions_path = 'solutions/test_solutions.txt'
    test_solutions = wordle_solver.Lexicon()
    test_solutions.load_from_txt(test_solutions_path)

    output_path = 'out/' + input('Output path: ') + '.txt'

    lexicon_path = '100_words_sorted.txt'

    with open(output_path, mode='w', encoding='utf8') as f:
        for i, solution in enumerate(test_solutions.word_list):
            f.write('- - - - - Test {}: {} - - - - -{}'.format(i, solution, '\n'))
            f.write(str(wordle_solver.play_wordle(lexicon_path)) + '\n')


if __name__ == '__main__':
    main()