# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:54:05 2023

@author: manul
"""
import wordle_solver

def main():

    lexicon = wordle_solver.Lexicon()
    lexicon.load_from_txt('100_words_sorted.txt')

    print(lexicon.word_match_guess('thing', 'their', [2,2,0,1,0]))

if __name__ == '__main__':
    main()
