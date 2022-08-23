import pygame
import time
import numpy as np
import unittest


class Board:
    """Board class is used to create a board object. Black or white pieces
    can be placed on the cross points of the board.

    attributes:
        my_board, states, colors, options, unit_size, new_piece, count.

    methods:
        draw, draw_board, draw_pieces, write_restart, read_restart.
    """

    def __init__(self, states, colors, options):
        """Constructor.

        Parameters:
            states: a dict mapping states to integers.
            colors: a dict mapping colors to list of RGB values.
            options: a dict containing the properties of the board.
        """

        # a dict mapping state of one position on the board to integers,
        # 0 represents empty, 1 represents black piece,
        # 2 represents white piece.
        self.states = states

        # a dict mapping black and white colors to their RGB values.
        self.colors = colors

        # a dict read from the options.json file containing the
        # properties of the board.
        self.options = options

        # unit size between two lines on the board.
        self.unit_size = (self.options["screen_size"] /
                          (self.options["line_numbers"] + 1))

        # a two-dimensional array represents the states of all
        # positions on the board using 0,1,2.
        self.my_board = [[]] * self.options["line_numbers"]
        for i in range(self.options["line_numbers"]):
            self.my_board[i] = ([self.states["empty"]] *
                                self.options["line_numbers"])

        # the position where the last piece placed
        self.new_piece = (-1, -1)

        # step numbers
        self.count = 0

    def draw(self, screen):
        """Draw the board and pieces on the screen.

        Parameters:
            screen: the screen created by pygame.
        Return:
            none.
        """

        self.draw_board(screen)  # draw board lines
        self.draw_pieces(screen)  # draw pieces
        pygame.display.flip()  # update display of the screen

    def draw_board(self, screen):
        """Draw the board lines on the screen using the
        pygame.draw.line method.

        Parameters:
            screen: the screen created by pygame.
        Return:
            none.
        """

        for i in range(self.options["line_numbers"]):
            # draw one horizontal line
            pygame.draw.line(screen, self.options["board_line_color"],
                             [self.unit_size, (i + 1) * self.unit_size],
                             [self.options["screen_size"] - self.unit_size,
                              (i + 1) * self.unit_size], 1)

            # draw one vertical line
            pygame.draw.line(screen, self.options["board_line_color"],
                             [(i + 1) * self.unit_size, self.unit_size],
                             [(i + 1) * self.unit_size,
                              self.options["screen_size"] - self.unit_size], 1)

    def draw_pieces(self, screen):
        """Draw the pieces on the screen using the
        pygame.draw.circle method.

        Parameters:
            screen: the screen created by pygame.
        Return:
            none.
        """

        # using two for loops to loop the whole cross points on the board
        for r in range(self.options["line_numbers"]):
            for c in range(self.options["line_numbers"]):
                if self.my_board[r][c] == self.states["black"]:
                    # if the my_board value of this position is 1 (black),
                    # draw a black circle to represent a black piece
                    pygame.draw.circle(screen, self.colors["black_color"],
                                       [self.unit_size * (c + 1),
                                        self.unit_size * (r + 1)],
                                       self.options["piece_size"], 0)

                elif self.my_board[r][c] == self.states["white"]:
                    # if the my_board value of this position is 2 (white),
                    # draw a white circle to represent a white piece
                    pygame.draw.circle(screen, self.colors["white_color"],
                                       [self.unit_size * (c + 1),
                                        self.unit_size * (r + 1)],
                                       self.options["piece_size"], 0)

    def write_restart(self, file_name):
        """Write the board on the screen to a file.

        reference: https://www.geeksforgeeks.org/numpy-savetxt/
        Parameters:
            file_name: name of the restart file
        Return:
            none
        """

        # convert the my_board to a numpy array
        board_array = np.array(self.my_board)
        # save board_array to a file
        np.savetxt(file_name, board_array, delimiter=", ", fmt="%d")

    def read_restart(self, file_name):
        """Read the board from a file.

        reference: https://www.geeksforgeeks.org/numpy-loadtxt-in-python/
        Parameters:
            file_name: name of the restart file
        Return:
            none
        """

        # load the my_board from the file
        self.my_board = list(np.loadtxt(file_name, delimiter=", ",
                                        dtype=float, ).astype(int))


def test_board_without_piece():
    """Test function to draw a board without piece.

    A board without piece will display on the screen for 3s.
    """

    # mapping states to integers
    states = {"empty": 0, "black": 1, "white": 2}
    # mapping colors to RGB values
    colors = {"black_color": [0, 0, 0], "white_color": [255, 255, 255]}
    options = dict()  # properties of the board
    options["screen_size"] = 640  # size of the board
    options["line_numbers"] = 15  # line numbers on each dimension
    options["board_line_color"] = [165, 42, 42]  # line color: brown
    options["board_fill_color"] = [144, 238, 144]  # board color: lightgreen
    board = Board(states, colors, options)
    pygame.init()
    screen = pygame.display.set_mode(
        (options["screen_size"], options["screen_size"]))  # initial screen
    screen.fill(options["board_fill_color"])  # fill the screen
    board.draw(screen)  # test for drawing a board without pieces
    print("A board without pieces was drawn. It will be closed after 3s.")
    time.sleep(3)  # hold on the display for 3s
    pygame.quit()


def test_board_with_piece():
    """Test function to draw a board with piece.

    A board with one black piece at center and four white pieces around it
    will display on the screen for 3s.
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
    board.my_board[7][7] = states["black"]  # place one black piece at center
    board.my_board[6][7] = states["white"]  # place white piece above black
    board.my_board[8][7] = states["white"]  # place white piece below black
    board.my_board[7][6] = states["white"]  # place white piece left black
    board.my_board[7][8] = states["white"]  # place white piece right black
    pygame.init()
    screen = pygame.display.set_mode(
        (options["screen_size"], options["screen_size"]))  # initial screen
    screen.fill(options["board_fill_color"])  # fill the screen
    board.draw(screen)  # test for drawing a board without pieces
    print("A board with one black piece at center and four white pieces \
around it was draw. It will be closed after 3s.")
    time.sleep(3)  # hold on the display for 3s
    pygame.quit()


class TestRestart(unittest.TestCase):
    """Test write_restart and read_restart.
    """

    def test_write_read_restart(self):
        """A board with one black piece at center and four white pieces around
        it will be saved to a file using write_restart function, then read the
        board from that file using read_restart function.
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
        board.my_board[7][7] = states["black"]  # place black piece at center
        board.my_board[6][7] = states["white"]  # place white piece above black
        board.my_board[8][7] = states["white"]  # place white piece below black
        board.my_board[7][6] = states["white"]  # place white piece left black
        board.my_board[7][8] = states["white"]  # place white piece right black

        # flat the 2D lists to 1D
        # sources: https://miguendes.me/python-flatten-list
        before_restart = [item
                          for sublist in board.my_board for item in sublist]
        # write the board to the file test_restart.txt
        board.write_restart("test_restart.txt")

        # recreate the board
        board = Board(states, colors, options)
        # read the board from the file test_restart.txt
        board.read_restart("test_restart.txt")
        # flat the 2D lists to 1D
        after_restart = [item
                         for sublist in board.my_board for item in sublist]
        actual = (after_restart == before_restart)
        expected = True
        self.assertEqual(actual, expected)


def main():
    # test the class Board

    # test 1: draw a board without pieces
    print("test Board class start:")
    print("test 1 / 2: draw a board without pieces")
    test_board_without_piece()
    print("test 1 / 2 pass")
    print("-" * 80)

    # test 2: draw a board with pieces
    print("test 2 / 2: draw a board with pieces")
    test_board_with_piece()
    print("test 2 / 2 pass")
    print("test Board class done.")

    # test 3: test the write_restart and read_restart
    unittest.main()


if __name__ == "__main__":
    main()
