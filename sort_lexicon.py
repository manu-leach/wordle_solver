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

def write_lexicon_to_file(lexicon_path, word_list):

    sorted_lexicon_path = lexicon_path[:len(lexicon_path) - 4]+ '_sorted.txt'
    with open(sorted_lexicon_path, 'w') as f:
        for word in word_list:
            f.write(word)
            f.write('\n')

def count_l

def main():

    lexicon_path = '100_words.txt'
    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    new_lexicon = Lexicon()
    new_lexicon.word_list = sort_by_letter_freq(new_lexicon.word_list)


    write_lexicon_to_file(lexicon_path, new_lexicon)

if __name__ == '__main__':
    main()
