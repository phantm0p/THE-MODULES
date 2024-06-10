# BOT/game/tictactoe/tictactoe_logic.py

class TicTacToe:
    def __init__(self, player_x, player_o):
        self.board = [' ' for _ in range(9)]
        self.players = {'X': player_x, 'O': player_o}
        self.current_turn = 'X'
        self.current_winner = None
        self.notification_message_id = None
        self.game_message_id = None

    def make_move(self, square, player):
        if self.board[square] == ' ':
            self.board[square] = player
            if self.check_winner(square, player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, square, player):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == player for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == player for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == player for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == player for s in diagonal2]):
                return True
        return False

    def switch_turn(self):
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    def empty_squares(self):
        return ' ' in self.board
