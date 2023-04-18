# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:48:28 2023

@author: manul
"""

import wordle_solver

def gen_test_data():

    test_solutions_name = 'first_50_solutions'
    test_solutions = wordle_solver.Lexicon()
    test_solutions.load_from_txt('solutions/{}.txt'.format(test_solutions_name))

    lexicon_name = 'sgb_words'
    lexicon = wordle_solver.Lexicon()
    lexicon.load_from_txt('lexicons/{}.txt'.format(lexicon_name))

    best_start_guess = 'tares' # DEPENDENT ON LEXICON

    output_path = 'out/' + input('Output path: ') + '.txt'

    with open(output_path, mode='w', encoding='utf8') as f:
        f.write('Solution test set: {}\n'.format(test_solutions_name))
        f.write('Lexicon: {}\n'.format(lexicon_name))
    
    for i, answer in enumerate(test_solutions.word_list):
        board = wordle_solver.WordleBoard(answer)
        player = wordle_solver.ComputerPlayer(lexicon.copy(), board, candidate_pool=lexicon.copy(), start_guess=best_start_guess)
        score = player.play_wordle()

        with open(output_path, mode='w', encoding='utf8') as f:
            f.write('- - - - - Answer {}: {} - - - - -\n'.format(i+1, answer))
            f.write('Score: {}\n'.format(score))
            player.board.print_board()



def main():

    gen_test_data()


if __name__ == '__main__':
    main()