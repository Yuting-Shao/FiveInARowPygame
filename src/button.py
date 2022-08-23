import pygame
import time


class Button:
    """Button class is used to generate a button on screen.

    reference: [Book] Eric Matthes, Python Crash Course - A Hands-On,
    Project-Based Introduction to Programming, Chapter 14.1.1
    attributes:
        screen, screen_rect, font, rect, text_image, text_image_rect.

    methods:
        draw_button.
    """

    def __init__(self, text, screen):
        """Constructor

        Parameters:
            text: text shown in the button.
            screen: screen to show the button.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.SysFont(None, 24)
        self.rect = pygame.Rect(0, 0, 200, 100)  # rectangle shape button
        self.rect.center = self.screen_rect.center
        self.text_image = self.font.render(text, True, [0, 0, 0],
                                           [255, 255, 255])  # text and color
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw the button.
        """

        self.screen.fill([255, 255, 255], self.rect)  # white background
        self.screen.blit(self.text_image, self.text_image_rect)
        pygame.display.flip()  # update the display


def test_button():
    """Test button class.

    A button with the text 'Hello world!' in it will be shown.
    """

    options = dict()  # properties of the board
    options["screen_size"] = 640  # size of the board
    pygame.init()
    screen = pygame.display.set_mode(
        (options["screen_size"], options["screen_size"]))  # initial screen
    button = Button("Hello world!", screen)
    print("Draw a Hello world! button on the screen. Will disappear in 3s.")
    button.draw_button()
    time.sleep(3)  # hold on the display for 3s
    pygame.quit()


def main():
    # test button class
    print("Test button start:")
    test_button()
    print("Test button done.")


if __name__ == "__main__":
    main()
