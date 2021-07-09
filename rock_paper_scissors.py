# If you’ve ever wanted to create games, this project will get you started!
# In this project you will code a Rock-Paper-Scissors-Lizard-Spock game, a more advanced
# version of Rock-Paper-Scissors, which can be played against the computer.

from random import choice


class Game:
    game_circle = ('rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper',
                   'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire')
    points = {'win': 100, 'draw': 50, 'lose': 0}

    def __init__(self):
        self.active_state = True
        self.user_name = None
        self.game_options = ('rock', 'paper', 'scissors')
        self.user_score = 0
        self.score_table = {}
        self.load_score_table()

    def winner_options(self, anchor_value):
        base_index = self.game_circle.index(anchor_value)
        return (self.game_circle[base_index+1:] + self.game_circle[:base_index])[:7]

    def make_move(self, user_input):
        self.computer = choice(self.game_options)
        if user_input == '!exit':
            print("Bye!")
            self.active_state = False
        elif user_input == '!rating':
            print(f'Your rating: {self.user_score}')
        elif user_input not in self.game_options:
            print('Invalid input')
        elif user_input == self.computer:
            print(f'There is a draw {user_input}')
            self.user_score += self.points['draw']
        elif self.computer in self.winner_options(user_input):
            print(f'Sorry, but the computer chose {self.computer}')
        elif self.computer not in self.winner_options(user_input):
            print(f'Well done. The computer chose {self.computer} and failed')
            self.user_score += self.points['win']

    def load_score_table(self):
        with open('rating.txt') as f:
            for line in f:
                score = line.split()
                self.score_table[score[0]] = int(score[1])

    def choose_level(self):
        options = tuple(input().split(','))
        if len(options) > 2 and all([x in self.game_circle for x in options]):
            self.game_options = options
        print("Okay, let's start")

    def play_game(self):
        self.user_name = input('Enter your name: ')
        print(f'Hello, {self.user_name}')
        self.choose_level()
        self.user_score = self.score_table[self.user_name] \
            if self.user_name in self.score_table.keys() else 0

        while self.active_state:
            self.make_move(input())


if __name__ == '__main__':
    new_game = Game()
    new_game.play_game()
