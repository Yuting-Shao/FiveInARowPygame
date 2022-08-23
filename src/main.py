import json
from board import Board
import pygame
import sys
from player import play_human, play_ai
from referee import referee
from button import Button
import time


def run_game(board):
    """Run the game in different modes according to the user's configure file.
    """

    pygame.init()  # initialize pygame
    pygame.display.set_caption("Five in a Row")  # set the title of the window

    if board.options["remember_me"] == "no" \
            and board.options["manual"] == "yes":
        # run the guest mode and placing any piece at any position mode
        run(board, board.options["restart_manual_file"])

    elif board.options["remember_me"] == "no" \
            and board.options["manual"] == "no":
        # run the guest mode and standard game mode
        run(board, board.options["restart_file"])

    elif board.options["remember_me"] == "yes" \
            and board.options["manual"] == "no" \
            and board.options["player_number"] == 2:
        # run the user mode and there are 2 human players
        file_name = input("Enter your name: ")  # let the user input name
        with open("users.json", "r") as f:
            users = json.load(f)
            if file_name in users:
                # run the game with the user's file if is an exist user
                run(board, users[file_name])
            else:
                # create and record the user's 2 human player file
                # if is a new user, then run
                users[file_name] = file_name + ".txt"
                with open("users.json", "w") as wf:
                    json.dump(users, wf)
                run(board, users[file_name])

    elif board.options["remember_me"] == "yes" \
            and board.options["manual"] == "no" \
            and board.options["player_number"] == 1:
        # run the single player mode
        file_name = input("Enter your name: ")  # let the user input name
        # user's a single player vs AI player file storing the board
        file_name1 = file_name + "1"
        file_name2 = file_name + "2"  # user's file storing the step numbers
        with open("users.json", "r") as f:
            users = json.load(f)
            if file_name1 in users:
                # exist user
                if board.options["restart_game"] == "no":
                    # exist user play a new game
                    run(board, users[file_name1])
                else:
                    # exist user play a restart game
                    run_remember_single_restart(board, users[file_name1],
                                                users[file_name2])
            else:
                # new user
                if board.options["restart_game"] == "no":
                    # new user play a new game
                    # write the user information to the user.json
                    users[file_name1] = file_name1 + ".txt"
                    users[file_name2] = board.count
                    with open("users.json", "w") as wf:
                        json.dump(users, wf)
                    # run the game
                    run(board, users[file_name1])
                else:
                    # new user can not play a restart game
                    print("restart should be no")
    else:
        print("wrong choice in the options.json")

    pygame.quit()  # quit pygame


def run(board, file_name):
    """Initialize the screen and start the game according to the mode.

    parameters:
        board: the board used for the game.
        file_name: file_name of the user.
    """

    if board.options["restart_game"] == "yes":  # restart game mode
        try:
            board.read_restart(file_name)  # read in the board
            # initialize screen
            screen = pygame.display.set_mode(
                (board.options["screen_size"], board.options["screen_size"]))
            screen.fill(board.options["board_fill_color"])
            board.draw(screen)  # draw the board and pieces

            if board.options["manual"] == "yes":  # free placement mode
                run_manual(board, screen, file_name)

            elif board.options["manual"] == "no":
                run_non_manual(board, screen, file_name)  # battle mode

            else:
                print("wrong choice in the options.json")

        except FileNotFoundError:
            # restart file can not be found
            print("restart should be no")
    elif board.options["restart_game"] == "no":  # new game mode
        # initialize screen
        screen = pygame.display.set_mode(
            (board.options["screen_size"], board.options["screen_size"]))
        screen.fill(board.options["board_fill_color"])
        board.draw(screen)  # draw the board

        if board.options["manual"] == "yes":  # free placement mode
            run_manual(board, screen, file_name)

        elif board.options["manual"] == "no":  # battle mode
            board.count = 0  # set the step number to zero
            with open("users.json", "r") as f:
                users = json.load(f)
            users[file_name[:-5] + "2"] = board.count  # store the step number
            with open("users.json", "w") as wf:
                json.dump(users, wf)
            run_non_manual(board, screen, file_name)  # run the battle mode

        else:
            print("wrong choice in the options.json")


def run_remember_single_restart(board, file_name1, count):
    """Initialize the screen and start the game when mode is
     single player vs AI player game (restart and remember_me mode)

    parameters:
        board: the board used for the game.
        file_name1: file_name of the user.
        count: the step number of this user's a single player
        vs AI player game

    """
    board.count = count  # update step number
    board.read_restart(file_name1)  # read in board restart
    # initialize screen to display
    screen = pygame.display.set_mode(
        (board.options["screen_size"], board.options["screen_size"]))
    screen.fill(board.options["board_fill_color"])
    board.draw(screen)
    # run game
    run_non_manual(board, screen, file_name1)


def run_manual(board, screen, file_name):
    """Run the free placement mode.

    Place a black piece at the mouse position if left click.
    Place a white piece at the mouse position if right click.
    Remove the piece at the mouse position if click and the position is
    occupied.

    parameters:
        board: current board
        screen: screen to show the board
        file_name: file name of the user
    """

    manual = True  # loop variable for the while loop
    while manual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manual = False
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # event.button == 1 means left click of mouse
                # get the position of the mouse
                p = (round((event.pos[1] - board.unit_size) /
                           board.unit_size),
                     round((event.pos[0] - board.unit_size) / board.unit_size))
                # add a black piece to p
                play_human(board, p, board.colors["black_color"])
                # draw the board and pieces
                screen.fill(board.options["board_fill_color"])
                board.draw(screen)
                board.write_restart(file_name)  # write board to restart file
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # event.button == 3 means right click of mouse
                # get the position of the mouse
                p = (round((event.pos[1] - board.unit_size) /
                           board.unit_size),
                     round((event.pos[0] - board.unit_size) /
                           board.unit_size))
                # add a white piece to p
                play_human(board, p, board.colors["white_color"])
                # draw the board and pieces
                screen.fill(board.options["board_fill_color"])
                board.draw(screen)
                board.write_restart(file_name)  # write board to restart file
    sys.exit()  # end game


def run_non_manual(board, screen, file_name):
    """Run the battle mode.

    parameters:
        board: current board.
        screen: screen to show the board.
        file_name: file_name of the user.
    """

    if board.options["player_number"] == 2:
        # 2 human players place pieces one by one
        playing = True  # loop variable for the while loop
        board.count = 0  # set the step number to zero
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # end game
                elif event.type == pygame.KEYUP:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN \
                        and event.button == 1:
                    # left clicking of mouse means placing one piece
                    # on the mouse position
                    # get the mouse position
                    p = (round((event.pos[1] - board.unit_size) /
                               board.unit_size),
                         round((event.pos[0] - board.unit_size) /
                               board.unit_size))
                    # update step number
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    board.count = users[file_name[:-5] + "2"]

                    if board.my_board[p[0]][p[1]] == board.states["empty"]:
                        # place a piece on the mouse position
                        # if it is empty
                        if board.count % 2 == 0:  # black piece turn
                            # place the black piece
                            play_human(board, p, board.colors["black_color"])
                        else:  # white piece turn
                            # place the white piece
                            play_human(board, p, board.colors["white_color"])

                        board.count += 1  # increase the step number
                        with open("users.json", "r") as f:
                            users = json.load(f)
                        users[file_name[:-5] + "2"] = board.count
                        with open("users.json", "w") as wf:
                            json.dump(users, wf)

                        screen.fill(board.options["board_fill_color"])
                        board.draw(screen)  # draw the board and pieces

                        # check if game over
                        winner = referee(board)
                        # write board to file
                        board.write_restart(file_name)

                        if winner != "none":
                            playing = False  # end the while loop
                            show_winner_and_reset_board(winner, board,
                                                        file_name, screen)
                    else:
                        # the position is not empty,
                        # tell the user to try another using
                        # a button on the screen
                        print("try again")
                        button = Button("try again", screen)
                        button.draw_button()

    elif board.options["player_number"] == 1:
        # 1 human player battle the AI
        playing = True  # loop variable for the while loop
        board.count = 0  # set the step number to zero
        if board.options["human_player"] == "black":
            # human player play black piece
            while playing:
                for event in pygame.event.get():
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    board.count = users[file_name[:-5] + "2"]
                    if board.count % 2 == 0:
                        # black piece turn (human player)
                        if event.type == pygame.QUIT:
                            sys.exit()  # end game
                        elif event.type == pygame.KEYUP:
                            pass
                        elif event.type == pygame.MOUSEBUTTONDOWN \
                                and event.button == 1:
                            # left clicking of mouse means placing one piece
                            # on the mouse position
                            # read in step number
                            # get the mouse position
                            p = (round((event.pos[1] - board.unit_size) /
                                       board.unit_size),
                                 round((event.pos[0] - board.unit_size) /
                                       board.unit_size))
                            if board.my_board[p[0]][p[1]] == \
                                    board.states["empty"]:
                                # place a piece on the mouse position
                                # if it is empty
                                board.count += 1  # increase the step number
                                with open("users.json", "r") as f:
                                    users = json.load(f)
                                users[file_name[:-5] + "2"] = board.count
                                with open("users.json", "w") as wf:
                                    json.dump(users, wf)

                                # place the black piece
                                play_human(board, p,
                                           board.colors["black_color"])
                                screen.fill(board.options["board_fill_color"])
                                board.draw(screen)  # draw the board and piece

                                # check if game over
                                winner = referee(board)
                                # write board to file
                                board.write_restart(file_name)
                                if winner != "none":
                                    playing = False  # end the while loop
                                    show_winner_and_reset_board(winner, board,
                                                                file_name,
                                                                screen)
                            else:
                                # the position is not empty,
                                # tell the user to try another using
                                # a button on the screen
                                print("try again")
                                button = Button("try again", screen)
                                button.draw_button()
                                pygame.display.flip()
                    elif board.count % 2 == 1:
                        # ai turn
                        # increase the step number
                        board.count += 1
                        with open("users.json", "r") as f:
                            users = json.load(f)
                        users[file_name[:-5] + "2"] = board.count
                        with open("users.json", "w") as wf:
                            json.dump(users, wf)

                        # place a white piece on the board
                        # by the AI
                        play_ai(board,
                                board.colors["white_color"])
                        screen.fill(
                            board.options["board_fill_color"])
                        # draw the screen and pieces
                        board.draw(screen)

                        # check if game over
                        winner = referee(board)
                        # write board to file
                        board.write_restart(file_name)
                        if winner != "none":
                            playing = False  # end the while loop
                            show_winner_and_reset_board(winner,
                                                        board,
                                                        file_name,
                                                        screen)

        elif board.options["human_player"] == "white":
            # human player playing white piece,
            while playing:
                for event in pygame.event.get():
                    # read in step number
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    board.count = users[file_name[:-5] + "2"]
                    # AI move if step number is even
                    if board.count % 2 == 0:
                        # increase the step number
                        board.count += 1
                        with open("users.json", "r") as f:
                            users = json.load(f)
                        users[file_name[:-5] + "2"] = board.count
                        with open("users.json", "w") as wf:
                            json.dump(users, wf)
                        time.sleep(1)  # hold on the display for 1s

                        # place one black piece on the board by AI
                        play_ai(board, board.colors["black_color"])
                        screen.fill(board.options["board_fill_color"])
                        board.draw(screen)  # draw the board and piece

                        # check if game over
                        winner = referee(board)
                        # write board to file
                        board.write_restart(file_name)
                        if winner != "none":
                            playing = False  # end the while loop
                            show_winner_and_reset_board(winner, board,
                                                        file_name, screen)
                    elif event.type == pygame.QUIT:
                        sys.exit()  # end game
                    elif event.type == pygame.KEYUP:
                        pass
                    elif event.type == pygame.MOUSEBUTTONDOWN \
                            and event.button == 1:
                        # human player turn; left click of mouse detected
                        # get the position of the mouse
                        p = (round((event.pos[1] - board.unit_size) /
                                   board.unit_size),
                             round((event.pos[0] - board.unit_size) /
                                   board.unit_size))

                        if board.my_board[p[0]][p[1]] == board.states["empty"]:
                            # place a piece on the mouse position
                            # if it is empty
                            board.count += 1  # increase the step number
                            with open("users.json", "r") as f:
                                users = json.load(f)
                            users[file_name[:-5] + "2"] = board.count
                            with open("users.json", "w") as wf:
                                json.dump(users, wf)

                            # place the white piece by human player
                            play_human(board, p, board.colors["white_color"])
                            screen.fill(board.options["board_fill_color"])
                            board.draw(screen)  # draw the board and pieces

                            # check if game over
                            winner = referee(board)
                            # write board to file
                            board.write_restart(file_name)

                            if winner != "none":
                                playing = False  # end the while loop
                                show_winner_and_reset_board(winner, board,
                                                            file_name, screen)
                        else:
                            # the position is not empty,
                            # tell the user to try another using
                            # a button on the screen
                            print("try again")
                            button = Button("try again", screen)
                            button.draw_button()
                            pygame.display.flip()


def show_winner_and_reset_board(winner, board, file_name, screen):
    """Show the winner and reset the board to empty.

    parameters:
        winner: winner of the game.
        board: current board.
        file_name: file_name of the user.
        screen: screen to show the button.
    """

    print(f"{winner} win!")
    # show who is the winner on the screen
    button = Button(winner + " win", screen)
    button.draw_button()
    pygame.display.flip()
    board.count = 0  # reset the step number
    with open("users.json", "r") as f:
        users = json.load(f)
    users[file_name[:-5] + "2"] = board.count
    with open("users.json", "w") as wf:
        json.dump(users, wf)
    # reset the board and write to file
    for i in range(board.options["line_numbers"]):
        board.my_board[i] = ([board.states["empty"]] *
                             board.options["line_numbers"])
        board.write_restart(file_name)
    game_exit()  # exit game


def game_exit():
    """Helper function to exit the game.
    """

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                pass


def main():
    # read in the options from the options.json file
    with open("options.json", "r") as f:
        options = json.load(f)

    # mapping states to integers
    states = {"empty": 0, "black": 1, "white": 2}

    # mapping colors to RGB values
    colors = {"black_color": [0, 0, 0], "white_color": [255, 255, 255]}

    # create the board for the game
    board = Board(states, colors, options)

    # launch the game five in a row
    run_game(board)


if __name__ == "__main__":
    main()
