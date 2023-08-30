import socket
from tkinter import ttk
import tkinter.messagebox


from gameboard import GameBoard, GameBoardUi

"""
User's manual:
    Player 2 enter host info: 127.0.0.1:8000 then wait for Player 1 to connect
    Player 1 enter the same host info: 127.0.0.1:8000 and then immediately enters its username and wait for Player 2
    Player 2 then enters its username, then player 2 will wait for player 1 to make a move
    Player 1 makes a move and player 2 will recieve the move and the board will be updated and the game will be played
"""

"""
helper method that handles recieve
"""


def recieve(conn):
    return conn.recv(1000)


"""
helper method that handles send
"""


def send(conn, payload):
    conn.send(bytes(str(payload), encoding="ascii"))


class Game:
    """
    initialize the game
    """

    def __init__(self):
        self.game_board_ui = GameBoardUi("player 2")
        self.game_board_ui.hostinfo_input.bind(
            "<Return>", lambda _: self.connect_to_server()
        )
        self.game_board_ui.username_input.bind(
            "<Return>", lambda _: self.on_entered_player_name()
        )

    """
    create a server for others to join
    """

    def connect_to_server(self):
        self.socket_server = socket.create_server(self.parse_and_wipe_host_info())
        while True:
            self.connection, _ = self.socket_server.accept()
            self.player_1_name = str(recieve(self.connection), encoding="ascii")
            break

    """
    get the name from user's input, and initialize the ui
    """

    def on_entered_player_name(self):
        player_2_name = self.game_board_ui.username_input.get()
        self.game_board_ui.username_input.delete(0, "end")
        send(self.connection, player_2_name)

        self.game_board = GameBoard(
            self.player_1_name, player_2_name, False, self.game_board_ui
        )
        self.init_board_ui()
        x, y = self.wait_for_move()
        self.game_board.updateGameBoard(self.game_board.player_1, x, y)

    """
    check for user's move on click
    """

    def generate_on_click_handler(self, column, row):
        self.turn_label = ttk.Label(self.game_board_ui.frame, text="player2's turn")
        self.turn_label.grid(row=5, column=1)

        def on_click():
            if not self.game_board.updateGameBoard(
                self.game_board.player_2, column, row
            ):
                return
            self.move(column, row)
            print(f"move: {column} {row}")
            if self.game_board.is_game_finished:
                self.on_finished()
                return
            print("waiting for other player to make a move...")
            x, y = self.wait_for_move()
            print(f"opponent moved {x} {y}")
            self.game_board.updateGameBoard(self.game_board.player_1, x, y)
            if self.game_board.is_game_finished:
                self.on_finished()
                return

        return on_click

    """
    initialize the board for tictactoe when game starts
    """

    def init_board_ui(self):
        self.game_board_ui.tk_game_buttons = []
        for row in range(len(self.game_board.board)):
            self.game_board_ui.tk_game_buttons.append([])
            for column in range(len(self.game_board.board[row])):
                button = ttk.Button(
                    self.game_board_ui.frame,
                    text="",
                    command=self.generate_on_click_handler(column, row),
                )
                button.grid(column=column, row=row)
                self.game_board_ui.tk_game_buttons[row].append(button)

    """
    this is called with game is finished,
    it will wait for player1's response to keep playing or not
    """

    def on_finished(self):
        if self.game_board.curr_winner is not None:
            print(f"the winner is {self.game_board.curr_winner}")
        else:
            print("tie")
        answer = str(recieve(self.connection), encoding="ascii")
        if answer == "Play Again":
            self.game_board.resetGameBoard()
            print("other player wants to play again")
            self.game_board.pretty_print()
            x, y = self.wait_for_move()
            self.game_board.updateGameBoard(self.game_board.player_1, x, y)
        if answer == "Fun Times":
            output_text = self.game_board.get_stat(2)
            self.stat_label = ttk.Label(self.game_board_ui.frame, text=output_text)
            self.stat_label.grid(column=3)
            print("game ended")
            return

    """
    get the host info the user entered to connect to server
    """

    def parse_and_wipe_host_info(self):
        text = self.game_board_ui.hostinfo_input.get()
        self.game_board_ui.hostinfo_input.delete(0, "end")
        host, port = text.split(":")
        print(host, port)
        return (host, int(port))

    """
    send the move positions to the other player
    """

    def move(self, x, y):
        send(self.connection, x)
        send(self.connection, y)

    """
    wait to recieve the move positions from the other player
    """

    def wait_for_move(self):
        x = int(recieve(self.connection))
        y = int(recieve(self.connection))
        return x, y

    # def try_move(self):
    #     y = int(input("choose y(row) position for your move(from 0-2): "))
    #     x = int(input("choose x(col) position for your move(from 0-2): "))
    #     if not self.game_board.updateGameBoard(self.game_board.player_1, x, y):
    #         print("invalid move")
    #         self.try_move()
    #         return
    #     self.move(x, y)

    # player_1_name = input("input your username: ")
    # player_1_name = "player1"

    def run(self):
        self.game_board_ui.start_loop()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
