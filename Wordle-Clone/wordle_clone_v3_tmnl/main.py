import random
import nltk
import os
from enum import Enum, auto
from collections.abc import Sequence

if not os.path.exists('valid_words.txt'):
    from nltk.corpus import words, brown
    nltk.download('words')
    nltk.download('brown')

    common_words = set(w.lower() for w in brown.words())
    valid_words = {w.lower() for w in words.words() if len(w) == 5}
    refined_valid_words = [w for w in valid_words if w in common_words]

    with open('valid_words.txt', 'w') as f:
        for word in refined_valid_words:
            f.write(f"{word}\n")
else:
    with open('valid_words.txt', 'r') as f:
        refined_valid_words = [line.strip() for line in f]

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Verdict(Enum):
    CORRECT = auto()
    PARTIAL = auto()
    WRONG = auto()

assets = {
    Verdict.CORRECT: '🟩',
    Verdict.PARTIAL: '🟨',
    Verdict.WRONG: '⬜'
}

GREEN = '\033[92m'
YELLOW = '\033[93m'
GRAY = '\033[90m'
RESET = '\033[0m'

color_map = {
    Verdict.CORRECT: GREEN,
    Verdict.PARTIAL: YELLOW,
    Verdict.WRONG: GRAY
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
        while True:
            guess = str(input('Enter a valid 5-letter word: \n')).lower()
            if len(guess) == 5 and guess in refined_valid_words:
                break
        return guess
    
    def print_feedback(self, guess: str, verdict: Sequence[Verdict]):

        colored_output = ""
        
        for char, v in zip(guess.upper(), verdict):
            color = color_map[v]
            colored_output += f"{color} {char} {RESET}"
            
        print(f"\n{colored_output}")

        emoji_output = " ".join(assets[v] for v in verdict)
        print(f"{emoji_output}\n")

        if all(v == Verdict.CORRECT for v in verdict):
            print('Correct!')   

    def print_lose_message(self, target: str):
        print(f"You lost! The word was: {target.upper()}")

class WordleController:
    def __init__(self, model: WordleModel, view: WordleView):
        self.model = model
        self.view = view

    def start(self):
        clear_terminal()
        model = self.model
        view = self.view

        while not model.is_game_over:
            print(f"\nAttempts remaining: {self.model.attempts}")
            guess = view.ask_for_guess()
            verdict = model.check_guess(guess)
            view.print_feedback(guess, verdict)

        if not model.did_player_win:
            view.print_lose_message(model.target)

if __name__ == '__main__':
    target_word = random.choice(list(refined_valid_words))
    attempt_count = 6
    model = WordleModel(target_word, attempt_count)
    view = WordleView()
    controller = WordleController(model, view)

    controller.start()