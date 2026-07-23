import random
import nltk
from enum import Enum, auto
from collections.abc import Sequence
from nltk.corpus import words
nltk.download('words')


valid_words = [w.lower() for w in words.words() if len(w) == 5]

class Verdict(Enum):
    CORRECT = auto()
    PARTIAL = auto()
    WRONG = auto()

assets = {
    Verdict.CORRECT: '🟩',
    Verdict.PARTIAL: '🟨',
    Verdict.WRONG: '⬜'
}
    
class WordleModel:
    def __init__(self, target_word: str, attempts: int):
        self._target = target_word
        self._attempts = attempts
        self._is_game_over = False
        self._did_player_win = False

    @property
    def target(self):
        return self._target
    
    @property
    def is_game_over(self):
        return self._is_game_over
    
    @property
    def did_player_win(self):
        return self._did_player_win
    
    @property
    def attempts(self):
        return self._attempts
    
    def check_guess(self, guess: str) -> Sequence[Verdict]:
        verdict_out = [Verdict.WRONG] * 5
        target_pool = list(self._target)
        guess_chars = list(guess)

        for i in range(5):
            if guess_chars[i] == target_pool[i]:
                verdict_out[i] = Verdict.CORRECT
                target_pool[i] = None
                guess_chars[i] = None

        for i in range(5):
            if guess_chars[i] is not None:
                if guess_chars[i] in target_pool:
                    verdict_out[i] = Verdict.PARTIAL
                    target_pool.remove(guess_chars[i])

        self.use_attempt()
        
        if all(v == Verdict.CORRECT for v in verdict_out):
            self.game_over()
            self.game_win()
        
        elif self.attempts <= 0:
            self.game_over()

        return verdict_out
    
    def game_over(self):
        self._is_game_over = True

    def game_win(self):
        self._did_player_win = True
    
    def use_attempt(self):
        self._attempts -= 1
    
class WordleView:
    def ask_for_guess(self) -> str:
        guess = str(input('Enter a 5-letter word: \n')).lower()
        while len(guess) != 5:
            guess = str(input('Enter a 5-letter word: \n')).lower()
        return guess
    
    def print_feedback(self, verdict: Sequence[Verdict]):
        feedback_out = ''
        for ch in verdict:
            feedback_out += assets[ch]
        print(feedback_out)
        if all(v == Verdict.CORRECT for v in verdict):
            print('Correct!')   

    def print_lose_message(self, target: str):
        print(f"You lost! The word was: {target}")

class WordleController:
    def __init__(self, model: WordleModel, view: WordleView):
        self.model = model
        self.view = view

    def start(self):
        model = self.model
        view = self.view

        while not model.is_game_over:
            print(f"\nAttempts remaining: {self.model.attempts}")
            guess = view.ask_for_guess()
            verdict = model.check_guess(guess)
            view.print_feedback(verdict)

        if not model.did_player_win:
            view.print_lose_message(model.target)

if __name__ == '__main__':
    target_word = random.choice(valid_words)
    attempt_count = 6
    model = WordleModel('abbey', attempt_count)
    view = WordleView()
    controller = WordleController(model, view)

    controller.start()