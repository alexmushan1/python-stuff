class Player:
    def __init__(self, name):
        self.name = name
        self.win = 0
        self.loss = 0
        self.tie = 0

    def __repr__(self):
        if self.name == "player2":
            return "o"
        return "x"


class GameBoard:
    def __init__(self, player_1_name, player_2_name):
        self.player_1 = Player(player_1_name)
        self.player_2 = Player(player_2_name)
        self.games = 0
        self.last_player = self.player_1
        self.resetGameBoard()
        self.updateGamesPlayed()

    def pretty_print(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == None:
                    print("_", end="")
                else:
                    print(self.board[i][j], end="")
            print()

    def updateGamesPlayed(self):
        self.games += 1

    def resetGameBoard(self):
        self.is_game_finished = False
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.curr_winner = None

    def updateGameBoard(self, player, x, y):
        self.board[y][x] = player
        self.last_player = player
        self.isWinner()
        if not self.is_game_finished:
            self.is_game_finished = self.boardIsFull()

    def isWinner(self):
        winner = self.get_winner()
        self.curr_winner = winner
        if winner is not None:
            self.is_game_finished = True
            winner.win += 1
            if winner == self.player_1:
                self.player_2.loss += 1
            else:
                self.player_1.loss += 1

    def get_winner(self):
        for col in self.board:
            first_player = None
            not_winning = False
            for player in col:
                if player == None:
                    not_winning = True
                    break
                if first_player is None:
                    first_player = player
                elif first_player != player:
                    not_winning = True
                    break
            if not not_winning:
                return first_player

        for col in range(len(self.board[0])):
            first_player = None
            not_winning = False
            for row_number in range(len(self.board)):
                player = self.board[row_number][col]
                if player == None:
                    not_winning = True
                    break
                if first_player is None:
                    first_player = player
                elif first_player != player:
                    not_winning = True
                    break
            if not not_winning:
                return first_player

        if None != self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if None != self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

    def boardIsFull(self):
        for row in self.board:
            for player in row:
                if player == None:
                    return False
        self.player_1.tie += 1
        self.player_2.tie += 1
        return True

    def printStats(self):
        print(f"player 1 username: {self.player_1.name}")
        print(f"player 2 username: {self.player_2.name}")
        print(f"last played: {self.last_player}")
        print(f"number of games: {self.games}")
        print(f"number of total wins: {self.player_1.win + self.player_2.win}")
        print(f"number of total losses: {self.player_1.loss + self.player_2.loss}")
        print(f"number of total ties: {self.player_2.tie}")
