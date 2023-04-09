# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:05:19 2023

@author: manul
"""
from wordle_solver import load_lexicon_to_list

def sort_repeats_to_bottom(lexicon):

    go_to_bottom = []

    for word in lexicon:
        for letter in word:
            if word.count(letter) > 1:
                go_to_bottom.append(word)
                break

    for word in go_to_bottom:
        lexicon.remove(word)
        lexicon.append(word)

    return lexicon

def write_lexicon_to_file(lexicon_path, lexicon):

    sorted_lexicon_path = lexicon_path[:len(lexicon_path) - 4]+ '_sorted.txt'
    with open(sorted_lexicon_path, 'w') as f:
        for word in lexicon:
            f.write(word)
            f.write('\n')

def main():

    lexicon_path = '100_words.txt'
    lexicon = load_lexicon_to_list(lexicon_path)

    new_lexicon = sort_repeats_to_bottom(lexicon.copy())

    write_lexicon_to_file(lexicon_path, new_lexicon)

if __name__ == '__main__':
    main()
