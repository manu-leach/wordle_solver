# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:05:19 2023

@author: manul
"""
from wordle_solver import Lexicon

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def sort_repeats_to_bottom(word_list):

    go_to_bottom = []

    for word in word_list:
        for letter in word:
            if word.count(letter) > 1:
                go_to_bottom.append(word)
                break

    for word in go_to_bottom:
        word_list.remove(word)
        word_list.append(word)

    return word_list

def write_lexicon_to_file(lexicon_path, lexicon):

    with open(lexicon_path, mode='w', encoding='utf8') as f:
        for word in lexicon.word_list:
            f.write(word)
            f.write('\n')

def find_unshared_words(lexicon1, lexicon2):

    unshared = set()

    for word in lexicon1.word_list:
        if word not in lexicon2.word_list:
            unshared.add(word)

    return unshared

def main():

    lexicon_path = 'sgb_words.txt'
    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    selby_lex = Lexicon()
    selby_lex.load_from_txt('solutions/first_50_solutions.txt')

    for word in find_unshared_words(selby_lex, lexicon):
        selby_lex.word_list.remove(word)
        print('Removing {}'.format(word))

    write_lexicon_to_file('solutions/first_50_solutions_with_sgb.txt', selby_lex)

if __name__ == '__main__':
    main()
