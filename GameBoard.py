import tkinter
from tkinter import ttk


class Player:
    """
    constructor for player
    """

    def __init__(self, name):
        self.name = name
        self.win = 0
        self.loss = 0
        self.tie = 0


class GameBoardUi:
    """
    constructor for gameboard ui
    creates text entries in ui
    """

    def __init__(self, titile_override):
        self.root = tkinter.Tk()
        self.root.title(titile_override)
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        # self.tk_game_buttons = []
        # for column in range(len(self.board)):
        #     self.tk_game_buttons.append([])
        #     for row in range(len(self.board[column])):

        #         def on_click():
        #             ...
        #             # player = self.player_2 if self.is_server else self.player_1
        #             # self.updateGameBoard(player, row, column)

        #         button = ttk.Button(frame, text="", command=on_click)
        #         button.grid(column=column, row=row)
        #         self.tk_game_buttons[column].append(button)

        self.hostinfo_label = ttk.Label(self.frame, text="host info: ")
        self.hostinfo_label.grid(row=3)
        self.hostinfo_input = ttk.Entry(self.frame)
        self.hostinfo_input.grid(row=3, column=1, columnspan=2)
        # self.hostinfo_input.bind(
        #     "<Return>",
        #     lambda _: self.listen_for_player()
        #     if self.is_server
        #     else self.connect_to_server(),
        # )

        self.username_label = ttk.Label(self.frame, text="user name: ")
        self.username_label.grid(row=4)
        self.username_input = ttk.Entry(self.frame)
        self.username_input.grid(row=4, column=1, columnspan=2)
        # self.username_input.bind("<Return>", lambda _: self.on_entered_player_name())

    def start_loop(self):
        self.root.mainloop()


class GameBoard:
    """
    constructor for gameboard class
    """

    def __init__(
        self, player_1_name, player_2_name, is_server, game_board_ui: GameBoardUi
    ):
        self.is_server = is_server
        self.game_board_ui = game_board_ui
        self.player_1 = Player(player_1_name)
        self.player_2 = Player(player_2_name)
        self.games = 0
        self.last_player = self.player_1
        self.resetGameBoard()

    """
    update the ui corresponding to player's input
    """

    def update_game_board_ui(self, x, y, state):
        self.game_board_ui.tk_game_buttons[y][x].configure(text=state)

    """
    print the gameboard in console
    """

    def pretty_print(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == None:
                    print("_", end="")
                else:
                    print(self.board[i][j], end="")
            print()

    """
    increment the games played by 1
    """

    def updateGamesPlayed(self):
        self.games += 1

    """
    reset and clear the game board
    """

    def resetGameBoard(self):
        self.updateGamesPlayed()
        self.is_game_finished = False
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.curr_winner = None
        if not hasattr(self.game_board_ui, "tk_game_buttons"):
            return
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.update_game_board_ui(x, y, "")

    """
    input int x int y for positions, Player player for the current player
    handles where the move is placed
    return if the move was sucessful

    """

    def updateGameBoard(self, player, x, y):
        if self.board[y][x] is not None:
            return False
        self.board[y][x] = player
        self.last_player = player
        self.isWinner()
        if not self.is_game_finished:
            self.is_game_finished = self.boardIsFull()
        self.update_game_board_ui(x, y, "x" if player == self.player_1 else "o")
        return True

    """
    check if the current move results in a win, then update the stats for both players
    """

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

    """
    find out which player won the last round
    return the winning player
    """

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

    """
    checks that if no more moves can be made on the board then it is a tie
    update tie number
    return true if it is a tie
    """

    def boardIsFull(self):
        for row in self.board:
            for player in row:
                if player == None:
                    return False
        self.player_1.tie += 1
        self.player_2.tie += 1
        return True

    """
    print the stat
    """

    def printStats(self):
        print(self.get_stat())

    """
    return the stats as string for each player
    """

    def get_stat(self, player_num):
        if player_num == 1:
            return (
                f"player 1 username: {self.player_1.name}\n"
                + f"player 2 username: {self.player_2.name}\n"
                + f"last played: {self.last_player.name}\n"
                + f"number of games: {self.games}\n"
                + f"number of player1 wins: {self.player_1.win}\n"
                + f"number of player1 losses: {self.player_1.loss}\n"
                + f"number of total ties: {self.player_2.tie}\n"
            )
        else:
            return (
                f"player 1 username: {self.player_1.name}\n"
                + f"player 2 username: {self.player_2.name}\n"
                + f"last played: {self.last_player.name}\n"
                + f"number of games: {self.games}\n"
                + f"number of player2 wins: {self.player_2.win}\n"
                + f"number of player2 losses: {self.player_2.loss}\n"
                + f"number of total ties: {self.player_2.tie}\n"
            )
