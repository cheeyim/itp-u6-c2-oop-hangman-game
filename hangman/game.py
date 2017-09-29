from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()
            
        self.guess = guess
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit == None:
            self.hit = False
            
        return self.hit
        
    def is_miss(self):
        if self.miss == None:
            self.miss = False
            
        return self.miss


class GuessWord(object):
    def __init__(self, answer):
        
        if len(answer) == 0:
            raise InvalidWordException()
        
        self.answer = answer.lower()
        self.masked = '*' * len(answer)
        
    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException()
         
        masked_work = ''    
        for i in range(0, len(self.answer)):
            if guess.lower() == self.answer[i].lower():
                masked_work += guess.lower()
            else:
                masked_work += self.masked[i]
        self.masked = masked_work
            
        attempt = GuessAttempt(guess)
        if guess.lower() in self.answer.lower():
            attempt.hit = True
        else:
            attempt.miss = True
            
        return attempt
        

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=[], number_of_guesses=5):
        #self.list_of_words = list_of_words
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        if list_of_words != []:
            self.word = GuessWord(list_of_words[0])
        else:
            self.word = GuessWord(HangmanGame.select_random_word(HangmanGame.WORD_LIST))
    
    @classmethod
    def select_random_word(cls, list_of_words):
        
        if list_of_words == []:
            raise InvalidListOfWordsException()
            
        return random.choice(list_of_words)

    def guess(self, charToGuess):
        
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(charToGuess.lower())
        attempt = self.word.perform_attempt(charToGuess)
        if attempt.is_miss():
            self.remaining_misses -= 1
            
        if self.is_won():
            raise GameWonException()
        elif self.is_lost():
            raise GameLostException()
        
        return attempt
        
    def is_won(self):
        return self.word.answer == self.word.masked
        
    def is_finished(self):
        return self.remaining_misses == 0 or self.is_won()
        
    def is_lost(self):
        return self.remaining_misses == 0 and self.is_won() == False