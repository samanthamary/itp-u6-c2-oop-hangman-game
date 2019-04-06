from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit=False, miss=False):
        if hit and miss:
            raise InvalidGuessAttempt
        self.guess = guess
        self.hit = hit
        self.miss = miss
    
    def is_hit(self):
        return self.hit == True
    
    def is_miss(self):
        return self.miss == True

class GuessWord(object):
    def __init__(self, word):
        if len(word) < 1:
            raise InvalidWordException
        self.answer = word
        self.masked = '*' * len(word)
    
    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException
        if guess.lower() in self.answer.lower():
            result = GuessAttempt(guess, hit=True)
        else:
            result = GuessAttempt(guess, miss=True)
        new_masked_word = list(self.masked)
        for idx, letter in enumerate(self.answer):
            if guess.lower() == letter.lower():
                new_masked_word[idx] = letter.lower()
        self.masked = "".join(new_masked_word)
        return result
        
            

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']  
    def __init__(self, words=WORD_LIST, number_of_guesses=5):
        self.word_list = words
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(HangmanGame.select_random_word(self.word_list))
         
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        self.previous_guesses.append(letter.lower())
        this_guess = self.word.perform_attempt(letter)
        if this_guess.is_miss():
            self.remaining_misses -= 1
        if self.is_lost():
            raise GameLostException
        if self.is_won():
            raise GameWonException
        return this_guess
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    def is_lost(self):
        return self.remaining_misses == 0 and self.word.answer != self.word.masked
    
    def is_won(self):
        return self.word.answer == self.word.masked
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
            
        
         