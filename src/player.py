from board import Board
import pygame
import time


def play_human(board, p, color):
    """Add a piece to the board by the human player.

    parameters:
        board: the board that will be added a piece
        p: position of the piece that will be placed, (r,c).
        color: piece color will be added, black or white, RGB value.
    return:
        board: the updated board.
    """

    if board.my_board[p[0]][p[1]] == board.states["empty"]:
        # place a piece on this position if it is empty
        if color == board.colors["black_color"]:
            # change the corresponding value of the my_board to "black"
            board.my_board[p[0]][p[1]] = board.states["black"]
        elif color == board.colors["white_color"]:
            # change the corresponding value of the my_board to "white"
            board.my_board[p[0]][p[1]] = board.states["white"]
    else:
        # remove the piece on this position if it is occupied
        board.my_board[p[0]][p[1]] = board.states["empty"]
    board.new_piece = (p[0], p[1])  # record where the new piece added
    return board


def play_ai(board, color):
    """Add a piece to the board by the computer (AI player).

    parameters:
        board: the board that will be added a piece
        color: piece color will be added, black or white, RGB value.
    return:
        board: the updated board.
    """

    s = board.options["line_numbers"]  # length of each dimension
    scores = [0] * (s * s)  # list storing the scores for each position
    if color == board.colors["black_color"]:  # find a position for black
        scores[(s + 1) * (s // 2)] = 100  # place a black at the center
    else:  # find a position for white
        scores[(s + 1) * (s // 2) - 1] = 100  # place a white left of center
    # loop over the board to calculate the score for each position
    for r in range(s):
        for c in range(s):
            if board.my_board[r][c] == 0:
                # if this position is empty, update the score using
                # the get_score function
                if scores[r * s + c] < max(get_score(board, 1, (r, c)),
                                           get_score(board, 2, (r, c))):
                    scores[r * s + c] = max(get_score(board, 1, (r, c)),
                                            get_score(board, 2, (r, c)))
            else:
                # a minor 1000000 means this position is an
                # impossible choice because it is occupied
                scores[s * r + c] = -1000000

    # figure out the position with the maximum score
    max_index = scores.index(max(scores))
    p = (int((max_index - max_index % s) / s), int(max_index % s))

    if color == board.colors["black_color"]:
        # place a black piece
        board.my_board[p[0]][p[1]] = board.states["black"]
    else:
        # place a black piece
        board.my_board[p[0]][p[1]] = board.states["white"]

    board.new_piece = (p[0], p[1])  # record where the new piece added
    return board


def get_score(board, c, p):
    """Help the play_ai to evaluate the score for each position on the board.

    parameters:
        board: current board
        c: 1 represent black; 2 represent white
        p: position that will be evaluated
    return:
        score: the score of this position
    """
    score = 0  # initialize the score to zero
    # these following list is the near positions that will be contributed
    # to the score of position(p[0], p[1]).
    try:
        mylist1 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0]][p[1] + 1],
                   board.my_board[p[0]][p[1] + 2],
                   board.my_board[p[0]][p[1] + 3],
                   board.my_board[p[0]][p[1] + 4]]
    except IndexError:
        mylist1 = [0, 0, 0, 0, 0]
    try:
        mylist2 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] + 1][p[1]],
                   board.my_board[p[0] + 2][p[1]],
                   board.my_board[p[0] + 3][p[1]],
                   board.my_board[p[0] + 4][p[1]]]
    except IndexError:
        mylist2 = [0, 0, 0, 0, 0]
    try:
        mylist3 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] + 1][p[1] + 1],
                   board.my_board[p[0] + 2][p[1] + 2],
                   board.my_board[p[0] + 3][p[1] + 3],
                   board.my_board[p[0] + 4][p[1] + 4]]
    except IndexError:
        mylist3 = [0, 0, 0, 0, 0]
    try:
        mylist4 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] - 1][p[1] + 1],
                   board.my_board[p[0] - 2][p[1] + 2],
                   board.my_board[p[0] - 3][p[1] + 3],
                   board.my_board[p[0] - 4][p[1] + 4]]
    except IndexError:
        mylist4 = [0, 0, 0, 0, 0]
    try:
        mylist5 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0]][p[1] - 1],
                   board.my_board[p[0]][p[1] - 2],
                   board.my_board[p[0]][p[1] - 3],
                   board.my_board[p[0]][p[1] - 4]]
    except IndexError:
        mylist5 = [0, 0, 0, 0, 0]
    try:
        mylist6 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] - 1][p[1]],
                   board.my_board[p[0] - 2][p[1]],
                   board.my_board[p[0] - 3][p[1]],
                   board.my_board[p[0] - 4][p[1]]]
    except IndexError:
        mylist6 = [0, 0, 0, 0, 0]
    try:
        mylist7 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] - 1][p[1] - 1],
                   board.my_board[p[0] - 2][p[1] - 2],
                   board.my_board[p[0] - 3][p[1] - 3],
                   board.my_board[p[0] - 4][p[1] - 4]]
    except IndexError:
        mylist7 = [0, 0, 0, 0, 0]
    try:
        mylist8 = [board.my_board[p[0]][p[1]],
                   board.my_board[p[0] + 1][p[1] - 1],
                   board.my_board[p[0] + 2][p[1] - 2],
                   board.my_board[p[0] + 3][p[1] - 3],
                   board.my_board[p[0] + 4][p[1] - 4]]
    except IndexError:
        mylist8 = [0, 0, 0, 0, 0]

    # evaluate this position if a black or white piece added
    score += max([evaluate(c, mylist1),
                  evaluate(c, mylist2),
                  evaluate(c, mylist3),
                  evaluate(c, mylist4),
                  evaluate(c, mylist5),
                  evaluate(c, mylist6),
                  evaluate(c, mylist7),
                  evaluate(c, mylist8)])
    return score


def evaluate(c, mylist):
    """Help the get_score function to get score of each position.

    parameters:
        c: 1 represent black and 2 represent white
        mylist: a list represent the states of the nearby positions
    return:
        score: a score evaluated according to mylist
    """

    score = 0
    if (mylist.count(c) == 4 and mylist.count(0) == 1) or \
            mylist == [0, c, c, c, 0]:
        # 4 pieces with the same color in sequence or 3 pieces with
        # the same color and two ends are empty will lead to a win,
        # so assign a high score 10000
        score = 10000
    if (mylist.count(c) == 3 and mylist.count(0) == 2) and \
            mylist != [0, c, c, c, 0]:
        # 3 pieces with the same color and 2 empty, but not 3 pieces with
        # the same color and two ends are empty, so it is good choice
        # so assign a score 1000
        score = 1000
    if mylist == [0, c, c, 0, 0] or mylist == [0, 0, c, c, 0]:
        # 2 pieces with the same color and 3 empty, it is not bad choice
        # so assign a score 100
        score = 100
    if mylist == [0, c, 0, 0, 0]:
        # 1 piece and 4 empty, assign a score 10
        score = 10
    return score


def test_play_human_ai():
    """Test play_human and play_ai functions.
    """

    # mapping states to integers
    states = {"empty": 0, "black": 1, "white": 2}
    # mapping colors to RGB values
    colors = {"black_color": [0, 0, 0], "white_color": [255, 255, 255]}
    options = dict()  # properties of the board
    options["screen_size"] = 640  # size of the board
    options["piece_size"] = 15  # size of the piece
    options["line_numbers"] = 15  # line numbers on each dimension
    options["board_line_color"] = [165, 42, 42]  # line color: brown
    options["board_fill_color"] = [144, 238, 144]  # board color: lightgreen
    board = Board(states, colors, options)
    board.my_board[7][7] = states["white"]  # place one white piece at center
    board.my_board[6][7] = states["white"]  # place white piece above center
    board.my_board[8][7] = states["white"]  # place white piece below center
    pygame.init()
    screen = pygame.display.set_mode(
        (options["screen_size"], options["screen_size"]))  # initial screen
    screen.fill(options["board_fill_color"])  # fill the screen
    board.draw(screen)  # draw the board

    print("Initialize a board with three white pieces at center.")
    time.sleep(1)  # hold on the display for 1s
    print("Place a black piece at position (5,7) to block the white pieces by \
play_human() function")
    play_human(board, (5, 7), board.colors["black_color"])
    board.draw(screen)  # draw the board
    time.sleep(1)  # hold on the display for 1s

    print("Place a white piece at a position by play_ai() function")
    play_ai(board, board.colors["white_color"])
    board.draw(screen)  # draw the board
    time.sleep(1)  # hold on the display for 1s

    print("Place a black piece at position (9,7) to block the white pieces by \
play_human() function")
    play_human(board, (9, 7), board.colors["black_color"])
    board.draw(screen)  # draw the board
    time.sleep(3)  # hold on the display for 3s
    pygame.quit()


def main():
    # test the play_human and play_ai
    print("test play_human and play_ai start:")
    test_play_human_ai()
    print("test play_human and play_ai done.")


if __name__ == "__main__":
    main()
