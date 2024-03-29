# -*- coding: utf-8 -*-

from copy import deepcopy
from random import choice, seed

seed(0)

WORD_LENGTH = 5
NUMBER_OF_TURNS = 6

BLACK = 0
YELLOW = 1
GREEN = 2

class GuessChecker():

    def __init__(self, answer):
        self.answer = answer

    def get_green_indices(self, guess):
        green_indices = [i for i in range(WORD_LENGTH) if guess[i] == self.answer[i]]

        return green_indices

    def check_guess(self, guess):

        result = [BLACK] * 5

        unnaccounted_indices_in_guess = list(range(WORD_LENGTH))
        unnaccounted_letters_in_answer = list(self.answer)

        green_indices = self.get_green_indices(guess)
        for i in green_indices:
            unnaccounted_indices_in_guess.remove(i)
            unnaccounted_letters_in_answer.remove(self.answer[i])
            result[i] = GREEN

        for i in unnaccounted_indices_in_guess:
            letter = guess[i]
            if letter in unnaccounted_letters_in_answer:
                result[i] = YELLOW
                unnaccounted_letters_in_answer.remove(letter)
            else: # letter not in unnaccounted_letters_in_answer
                result[i] = BLACK

        return result

class WordleBoard():

    def __init__(self):
        self.guesses = []
        self.results = []

    def make_guess(self, guess, result):
        self.guesses.append(guess)
        self.results.append(result)

    def copy(self):

        copy_board = WordleBoard(self.answer)
        copy_board.guesses = self.guesses.copy
        copy_board.results = deepcopy(self.results)

        return copy_board

    def print_board(self):

        for i, word in enumerate(self.guesses):
            print('({},{}) ({},{}) ({},{}) ({},{}) ({},{})'.format(word[0],
                                                            self.results[i][0],
                                                            word[1],
                                                            self.results[i][1],
                                                            word[2],
                                                            self.results[i][2],
                                                            word[3],
                                                            self.results[i][3],
                                                            word[4],
                                                            self.results[i][4]))

class Lexicon():

    def __init__(self):
        self.word_list = []

    def load_from_txt(self, lex_path):

        temp_list = []
        with open(lex_path, mode='r', encoding='utf8') as f:
            for line in f.readlines():
                temp_list.append(line[:5])

        self.word_list = temp_list

    def word_match_guess(self, word, guess, result):
        '''
        Checks if the guess would have yielded the same result if the word was the answer
        '''

        guess_checker = GuessChecker(word)
        if result == guess_checker.check_guess(guess):
            return True

        return False

    def valid_words(self, guess, result):

        to_remove = [word for word in self.word_list if not self.word_match_guess(word, guess, result)]

        for word in to_remove:
            self.word_list.remove(word)

        # Somehow slower ???
        #self.word_list = [word for word in self.word_list if word not in to_remove]

    def rnd(self):

        return choice(self.word_list)

    def copy(self):
        copy_lexicon = Lexicon()
        copy_lexicon.word_list = self.word_list.copy()
        return copy_lexicon
    
class WordleGame():

    def __init__(self, answer, lexicon):
        self.answer = answer
        self.lexicon = lexicon
        self.board = WordleBoard()
        self.guess_checker = GuessChecker(answer)
        self.turn = 0
        
    def single_turn(self, guess):

        self.turn += 1
        print('Turn {}'.format(self.turn))

        result = self.guess_checker.check_guess(guess)

        self.board.make_guess(guess, result)
        self.board.print_board()

        return result

    def get_guess(self):
        
        return input('Make guess: ')

    def play_wordle(self):

        while self.turn < NUMBER_OF_TURNS:

            guess = self.get_guess()
            result = self.single_turn(guess)

            if result == [GREEN] * 5:
                return self.turn
        
        return -1

def main():
    
    lexicon_name = 'sgb_words'
    lexicon_path = 'lexicons/{}.txt'.format(lexicon_name)
    lexicon = Lexicon()
    lexicon.load_from_txt(lexicon_path)

    game = WordleGame(answer=lexicon.rnd(), lexicon=lexicon)
    game.play_wordle()


if __name__ == '__main__':
    main()