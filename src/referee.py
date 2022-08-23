from board import Board
from player import play_human
import unittest


def referee(board):
    """Loop over the board to see whether anyone win after a new piece added.

    Parameters:
        board: current board
    Return:
        winner:"black" or "white" or "none"
    """

    p = board.new_piece  # the position of the new added piece
    for c in range(max(p[1] - 4, 0),
                   min(board.options["line_numbers"] - 4, p[1] + 5)):
        if (board.my_board[p[0]][c] == board.states["black"]
                and board.my_board[p[0]][c + 1] == board.states["black"]
                and board.my_board[p[0]][c + 2] == board.states["black"]
                and board.my_board[p[0]][c + 3] == board.states["black"]
                and board.my_board[p[0]][c + 4] == board.states["black"]):
            return "black"  # black piece win with 5 in row
        elif (board.my_board[p[0]][c] == board.states["white"]
              and board.my_board[p[0]][c + 1] == board.states["white"]
              and board.my_board[p[0]][c + 2] == board.states["white"]
              and board.my_board[p[0]][c + 3] == board.states["white"]
              and board.my_board[p[0]][c + 4] == board.states["white"]):
            return "white"  # white piece win with 5 in row
    for r in range(max(p[0] - 4, 0),
                   min(board.options["line_numbers"] - 4, p[0] + 5)):
        if (board.my_board[r][p[1]] == board.states["black"]
                and board.my_board[r + 1][p[1]] == board.states["black"]
                and board.my_board[r + 2][p[1]] == board.states["black"]
                and board.my_board[r + 3][p[1]] == board.states["black"]
                and board.my_board[r + 4][p[1]] == board.states["black"]):
            return "black"  # black piece win with 5 in column
        elif (board.my_board[r][p[1]] == board.states["white"]
              and board.my_board[r + 1][p[1]] == board.states["white"]
              and board.my_board[r + 2][p[1]] == board.states["white"]
              and board.my_board[r + 3][p[1]] == board.states["white"]
              and board.my_board[r + 4][p[1]] == board.states["white"]):
            return "white"  # white piece win with 5 in column
    for r in range(max(p[0] - 4, 0),
                   min(board.options["line_numbers"] - 4, p[0] + 5)):
        try:
            if (board.my_board[r][p[1] - p[0] + r] == board.states["black"]
                    and board.my_board[r + 1][p[1] - p[0] + r + 1] ==
                    board.states["black"]
                    and board.my_board[r + 2][p[1] - p[0] + r + 2] ==
                    board.states["black"]
                    and board.my_board[r + 3][p[1] - p[0] + r + 3] ==
                    board.states["black"]
                    and board.my_board[r + 4][p[1] - p[0] + r + 4] ==
                    board.states["black"]):
                return "black"  # black piece win with 5 in slash
            elif (board.my_board[r][p[1] - p[0] + r] == board.states["white"]
                  and board.my_board[r + 1][p[1] - p[0] + r + 1] ==
                  board.states["white"]
                  and board.my_board[r + 2][p[1] - p[0] + r + 2] ==
                  board.states["white"]
                  and board.my_board[r + 3][p[1] - p[0] + r + 3] ==
                  board.states["white"]
                  and board.my_board[r + 4][p[1] - p[0] + r + 4] ==
                  board.states["white"]):
                return "white"  # white piece win with 5 in slash
        except IndexError:
            pass

    for r in range(max(board.options["line_numbers"] - 4, p[0] - 4)):
        try:
            if (board.my_board[r][p[1] + p[0] - r] == board.states["black"]
                    and board.my_board[r + 1][p[1] + p[0] - r - 1] ==
                    board.states["black"]
                    and board.my_board[r + 2][p[1] + p[0] - r - 2] ==
                    board.states["black"]
                    and board.my_board[r + 3][p[1] + p[0] - r - 3] ==
                    board.states["black"]
                    and board.my_board[r + 4][p[1] + p[0] - r - 4] ==
                    board.states["black"]):
                return "black"  # black piece win with 5 in slash
            elif (board.my_board[r][p[1] + p[0] - r] == board.states["white"]
                  and board.my_board[r + 1][p[1] + p[0] - r - 1] ==
                  board.states["white"]
                  and board.my_board[r + 2][p[1] + p[0] - r - 2] ==
                  board.states["white"]
                  and board.my_board[r + 3][p[1] + p[0] - r - 3] ==
                  board.states["white"]
                  and board.my_board[r + 4][p[1] + p[0] - r - 4] ==
                  board.states["white"]):
                return "white"  # white piece win with 5 in slash
        except IndexError:
            pass

    return "none"  # not over


class TestReferee(unittest.TestCase):
    """Test referee functions.

    reference: https://www.digitalocean.com/community/tutorials/
    how-to-use-unittest-to-write-a-test-case-for-a-function-in-python
    """

    def test_referee_winner_none(self):
        """Test the referee function for the cases that winner is "none".
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
        # board color: lightgreen
        options["board_fill_color"] = [144, 238, 144]
        board = Board(states, colors, options)
        # no piece on the board, referee() should return "none"
        actual = referee(board)
        expected = "none"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 3 white pieces in a row, referee() should return "none"
        play_human(board, (7, 7), board.colors["white_color"])
        play_human(board, (6, 7), board.colors["white_color"])
        play_human(board, (8, 7), board.colors["white_color"])
        actual = referee(board)
        expected = "none"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 4 black pieces in a row, referee() should return "none"
        play_human(board, (7, 7), board.colors["black_color"])
        play_human(board, (6, 7), board.colors["black_color"])
        play_human(board, (8, 7), board.colors["black_color"])
        play_human(board, (9, 7), board.colors["black_color"])
        actual = referee(board)
        expected = "none"
        self.assertEqual(actual, expected)

    def test_referee_winner_black(self):
        """Test the referee function for the cases that winner is "black".
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
        # board color: lightgreen
        options["board_fill_color"] = [144, 238, 144]

        board = Board(states, colors, options)
        # 5 black pieces in a row, referee() should return "black"
        play_human(board, (5, 7), board.colors["black_color"])
        play_human(board, (6, 7), board.colors["black_color"])
        play_human(board, (7, 7), board.colors["black_color"])
        play_human(board, (8, 7), board.colors["black_color"])
        play_human(board, (9, 7), board.colors["black_color"])
        actual = referee(board)
        expected = "black"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 black pieces in a column, referee() should return "black"
        play_human(board, (7, 5), board.colors["black_color"])
        play_human(board, (7, 6), board.colors["black_color"])
        play_human(board, (7, 7), board.colors["black_color"])
        play_human(board, (7, 8), board.colors["black_color"])
        play_human(board, (7, 9), board.colors["black_color"])
        actual = referee(board)
        expected = "black"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 black pieces in a slash, referee() should return "black"
        play_human(board, (7, 7), board.colors["black_color"])
        play_human(board, (6, 6), board.colors["black_color"])
        play_human(board, (5, 5), board.colors["black_color"])
        play_human(board, (4, 4), board.colors["black_color"])
        play_human(board, (3, 3), board.colors["black_color"])
        actual = referee(board)
        expected = "black"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 black pieces in a slash, referee() should return "black"
        play_human(board, (7, 7), board.colors["black_color"])
        play_human(board, (6, 8), board.colors["black_color"])
        play_human(board, (5, 9), board.colors["black_color"])
        play_human(board, (4, 10), board.colors["black_color"])
        play_human(board, (3, 11), board.colors["black_color"])
        actual = referee(board)
        expected = "black"
        self.assertEqual(actual, expected)

    def test_referee_winner_white(self):
        """Test the referee function for the cases that winner is "white".
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
        # board color: lightgreen
        options["board_fill_color"] = [144, 238, 144]

        board = Board(states, colors, options)
        # 5 white pieces in a row, referee() should return "white"
        play_human(board, (5, 7), board.colors["white_color"])
        play_human(board, (6, 7), board.colors["white_color"])
        play_human(board, (7, 7), board.colors["white_color"])
        play_human(board, (8, 7), board.colors["white_color"])
        play_human(board, (9, 7), board.colors["white_color"])
        actual = referee(board)
        expected = "white"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 white pieces in a column, referee() should return "white"
        play_human(board, (7, 5), board.colors["white_color"])
        play_human(board, (7, 6), board.colors["white_color"])
        play_human(board, (7, 7), board.colors["white_color"])
        play_human(board, (7, 8), board.colors["white_color"])
        play_human(board, (7, 9), board.colors["white_color"])
        actual = referee(board)
        expected = "white"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 white pieces in a slash, referee() should return "white"
        play_human(board, (7, 7), board.colors["white_color"])
        play_human(board, (6, 6), board.colors["white_color"])
        play_human(board, (5, 5), board.colors["white_color"])
        play_human(board, (4, 4), board.colors["white_color"])
        play_human(board, (3, 3), board.colors["white_color"])
        actual = referee(board)
        expected = "white"
        self.assertEqual(actual, expected)

        board = Board(states, colors, options)
        # 5 white pieces in a slash, referee() should return "white"
        play_human(board, (7, 7), board.colors["white_color"])
        play_human(board, (6, 8), board.colors["white_color"])
        play_human(board, (5, 9), board.colors["white_color"])
        play_human(board, (4, 10), board.colors["white_color"])
        play_human(board, (3, 11), board.colors["white_color"])
        actual = referee(board)
        expected = "white"
        self.assertEqual(actual, expected)


def main():
    # test referee
    unittest.main()


if __name__ == "__main__":
    main()
