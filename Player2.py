import socket

from GameBoard import GameBoard


def recieve(conn):
    return conn.recv(1000)


def send(conn, payload):
    conn.send(bytes(str(payload), encoding="ascii"))


def main():
    with socket.create_server(("", 8000)) as server:
        print("waiting for players to connect ....")
        while True:
            conn, addr = server.accept()
            player_1_name = str(recieve(conn), encoding="ascii")
            send(conn, "player2")
            game_board = GameBoard(player_1_name, "player2")
            print("gameboard created")
            game_board.pretty_print()
            print(f"your opponent is: {player_1_name}")

            def move(x, y):
                send(conn, x)
                send(conn, y)

            def wait_for_move():
                x = int(recieve(conn))
                y = int(recieve(conn))
                return x, y

            while True:
                print("waiting for other player to make a move...")
                x, y = wait_for_move()
                game_board.updateGameBoard(game_board.player_1, x, y)
                game_board.pretty_print()

                if game_board.is_game_finished:
                    if game_board.curr_winner is not None:
                        print(f"the winner is {game_board.curr_winner}")
                    else:
                        print("tie")
                    answer = str(recieve(conn), encoding="ascii")
                    if answer == "Play Again":
                        game_board.resetGameBoard()
                        print("other player wants to play again")
                        game_board.pretty_print()
                    if answer == "Fun Times":
                        game_board.printStats()
                        print("game ended")
                        return

                y = int(input("choose y(row) position for your move(from 0-2): "))
                x = int(input("choose x(col) position for your move(from 0-2): "))
                game_board.updateGameBoard(game_board.player_2, x, y)
                move(x, y)
                game_board.pretty_print()
                if game_board.is_game_finished:
                    if game_board.curr_winner is not None:
                        print(f"the winner is {game_board.curr_winner}")
                    else:
                        print("tie")
                    answer = str(recieve(conn), encoding="ascii")
                    if answer == "Play Again":
                        game_board.resetGameBoard()
                        print("other player wants to play again")
                        game_board.pretty_print()
                    if answer == "Fun Times":
                        game_board.printStats()
                        print("game ended")
                        return


if __name__ == "__main__":
    main()
