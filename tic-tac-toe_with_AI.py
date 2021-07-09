# 'Everybody remembers this paper-and-pencil game from childhood: Tic-Tac-Toe,
# also known as Noughts and Crosses or X''s and O''s. A single mistake usually costs
# you the game, but thankfully it''s simple enough that most players discover the
# best strategy quickly. Let’s program Tic-Tac-Toe and create an AI opponent to do
# battle with!

from random import choice


class CoordinateError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class TicTacToeAI:
    game_levels = ('user', 'easy', 'medium', 'hard')

    def __init__(self, *args):
        self.active_state = True
        self.field_matrix = None
        self.current_player = None
        self.players = {}  # 0 - O, 1 - X :: level {user, easy, medium, hard}
        if len(args) > 0 and self.is_correct_restore(args[0]):
            self.restore_state(args[0])

    @property
    def next_player(self):
        return 1 - self.current_player

    @staticmethod
    def is_correct_restore(field_string):
        if len(field_string) != 9 or len([x for x in list(field_string) if x not in 'XO_ ']) != 0:
            return False
        else:
            return True

    @staticmethod
    def matrix_coord(value):  # Convert to matrix coordinates
        if not isinstance(value, int):
            if len(''.join(x for x in value if x.isalpha())) > 0:
                raise CoordinateError('You should enter numbers!')
            else:
                value = int(value) - 1
        if value < 0 or value > 2:
            raise CoordinateError('Coordinates should be from 1 to 3!')
        else:
            return value

    def print_field(self):
        line = f'{"-" * 9}\n'
        field = line
        for value in self.field_matrix:
            value = ['X' if x == 1 else 'O' if x == 0 else ' ' for x in value]
            field += f'| {" ".join(value)} |\n'
        field += line
        print(field, end='')

    def new_game(self, player_x, player_o):
        if player_x not in self.game_levels or player_o not in self.game_levels:
            raise TypeError
        print('New game started.\n')
        self.field_matrix = [[-3] * 3 for _ in range(3)]  # Create game field with starting values
        self.current_player = 1  # 'X' has first move
        self.players['0'] = player_o
        self.players['1'] = player_x
        self.game()

    def restore_state(self, field_string):
        print('Game restored.\n')
        self.current_player = 0 if field_string.count('X') - field_string.count('O') > 0 else 1
        field_list = [1 if x == 'X' else 0 if x == 'O' else -3 for x in field_string]
        self.field_matrix = [field_list[i * 3:i * 3 + 3] for i in range(3)]
        self.game()

    def field_t_matrix(self):
        return [list(x) for x in zip(*self.field_matrix)]

    def diagonals(self):
        return [[self.field_matrix[i][i] for i in range(3)], [self.field_matrix[j][2 - j] for j in range(3)]]

    def _empty_cell_finder(self, field_view=None, player=None):
        if field_view is None:
            field_view = self.field_matrix
        prewin_rows_ids = [idx for idx, value in enumerate(field_view) if sum(value) < 0]
        if player is not None:
            prewin_rows_ids = list(filter(lambda x: field_view[x].count(player) == 2, prewin_rows_ids))
        return [(row, col) for row in prewin_rows_ids
                for col, value in enumerate(field_view[row]) if value == -3]

    def prefer_moves(self, player):
        pref_moves = []
        pref_moves.extend(self._empty_cell_finder(self.field_matrix, player))  # rows
        pref_moves.extend(list(map(lambda x: (x[1], x[0]),  # columns
                                   self._empty_cell_finder(self.field_t_matrix(), player))))
        pref_moves.extend(list(map(lambda x: (x[1], abs(x[0] * 2 - x[1])),
                                   self._empty_cell_finder(self.diagonals(), player))))  # diagonals
        return pref_moves

    def status(self):  # return [game_over_flag, message_string]
        message = (False, 'Impossible')
        lines_sums = [sum(x) for y in [self.field_matrix, self.field_t_matrix(), self.diagonals()] for x in y]
        if abs(sum([x.count(1) for x in self.field_matrix]) - sum([x.count(0) for x in self.field_matrix])) <= 1:
            if 3 in lines_sums:
                message = (False, 'X wins')
            elif 0 in lines_sums:
                message = (False, 'O wins')
            elif min(lines_sums) < 0:
                message = (True, 'Game not finished')
            else:
                message = (False, 'Draw')
        return message

    def move(self, i, j):  # -> x, y: int
        message = (True, 'OK')
        try:
            i, j = self.matrix_coord(i), self.matrix_coord(j)
            if self.field_matrix[i][j] >= 0:
                message = (False, 'This cell is occupied! Choose another one!')
            else:
                self.field_matrix[i][j] = self.current_player
                self.current_player = self.next_player
                self.print_field()
        except CoordinateError as e:
            message = (False, str(e))
        finally:
            return message

    def ai(self):
        level = self.players[str(self.current_player)]
        print(f'Making move level "{level}"')
        _move = choice(self._empty_cell_finder())
        # AI medium
        if level == 'medium':
            moves_variants = self.prefer_moves(self.current_player) + self.prefer_moves(self.next_player)
            if len(moves_variants) > 0:
                _move = moves_variants[0]
        # AI hard (minimax)
        elif level == 'hard':
            _move = self.best_move()

        return _move

    def game(self):
        self.print_field()
        while self.status()[0]:
            if self.players[str(self.current_player)] == 'user':
                i, j = input('Enter the coordinates: ').split()
            else:
                i, j = self.ai()
            result = game.move(i, j)
            if not result[0]:
                print(result[1])
        print(self.status()[1], '\n')

    def play(self):
        while self.active_state:
            command = input('Input command: ').split()
            try:
                if command[0] == 'start':
                    self.new_game(command[1], command[2])
                elif command[0] == 'exit':
                    self.active_state = False
                else:
                    raise TypeError
            except (TypeError, IndexError) as e:
                print('Bad parameters!', e)

    def best_move(self):
        if len(self._empty_cell_finder()) == 9:
            return (0, 0)
        _move = None
        best_score = float('-inf')
        for i, j in self._empty_cell_finder():
            self.field_matrix[i][j] = self.current_player
            score = self.minimax(False)
            self.field_matrix[i][j] = -3
            if score > best_score:
                best_score = score
                _move = (i, j)
        return _move

    def minimax(self, is_max):
        if self.status()[1][0] == 'X':
            return 10 if self.current_player == 1 else -10
        elif self.status()[1][0] == 'O':
            return 10 if self.current_player == 0 else -10
        elif self.status()[1][0] == 'D':
            return 0

        if is_max:
            best_score = float('-inf')
            for i, j in self._empty_cell_finder():
                self.field_matrix[i][j] = self.current_player
                score = self.minimax(False)
                self.field_matrix[i][j] = -3
                best_score = max(score, best_score)
        else:
            best_score = float('inf')
            for i, j in self._empty_cell_finder():
                self.field_matrix[i][j] = self.next_player
                score = self.minimax(True)
                self.field_matrix[i][j] = -3
                best_score = min(score, best_score)

        return best_score


if __name__ == '__main__':
    game = TicTacToeAI()
    game.play()
