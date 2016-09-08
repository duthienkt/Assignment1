import pygame


class Constant:
    BG_COLOR = pygame.Color(38, 100, 100, 255)
    COLOR_BLUE = pygame.Color(0, 0, 255, 255)
    COLOR_RED = pygame.Color(255, 0, 0, 255)
    COLOR_WHILE = pygame.Color(255, 255, 255, 255)
    BUBBLE_FRAME_COUNT = 21
    BUBBLE_BLUE = 0
    BUBBLE_VIOLET = 1
    BUBBLE_GREEN = 2
    BUBBLE_LIGHT_BLUE = 3
    BUBBLE_RED = 4
    BUBBLE_YELLOW = 5

    DATA_FOLDER = "assets/"
    PATH_LOGO = DATA_FOLDER + "LOGO.png"
    PATH_ST_GR = DATA_FOLDER + "startbackground.png"
    PATH_BUBBLE = ["bub_blue.png", "bub_violet.png", "bub_green.png", "bub_light_blue.png", "bub_red.png",
                   "bub_yellow.png"]

    BUBBLE_EXP_FRAME_COUNT = 7
    BUBBLE_EXP_BLUE = 0
    BUBBLE_EXP_VIOLET = 1
    BUBBLE_EXP_GREEN = 2
    BUBBLE_EXP_LIGHT_BLUE = 3
    BUBBLE_EXP_RED = 4
    BUBBLE_EXP_YELLOW = 5
    PATH_BUBBLE_EXP = ["be_blue.png", "be_violet.png", "be_green.png", "be_light_blue.png", "be_red.png",
                       "be_yellow.png"]
    PATH_NORMAL_CURSOR = DATA_FOLDER + "ncursor.png"
    NORMAL_CURSOR_FRAME_COUNT = 5
    PATH_ARROW_CURSOR = DATA_FOLDER + "arrow.png"
    ARROW_CURSOR_FRAME_COUNT = 4

    BUTTON_PLAY = 0
    BUTTON_EXIT = 1
    BUTTON_POWER = 2
    BUTTON_OVER = 3
    PATH_BUTTON_UP = ["play1.png", "exit1.png", "turnoff.png", "defeat.png"]
    PATH_BUTTON_DOWN = ["play2.png", "exit2.png", "turnoff1.png", "defeat2.png"]

    PATH_BACKGROUND_SOUND = [DATA_FOLDER + "AX.ogg", DATA_FOLDER + "background.ogg",
                             DATA_FOLDER + "tt.ogg",
                             ]

    PATH_PLAY_IMAGE = ["1.png", "2.png", "3.png", "4.png"]

    # List axis of box in the background
    AXIS_BOX = ((153, 455),
                (264, 455),
                (383, 455),
                (498, 455),
                (617, 455),
                (97, 487),
                (207, 487),
                (319, 487),
                (438, 487),
                (569, 487),
                (691, 487),
                (148, 533),
                (267, 533),
                (387, 535),
                (503, 535),
                (622, 535))

    uniqueInt = 0

    @staticmethod
    def get_unique_int():
        Constant.uniqueInt += 1
        return Constant.uniqueInt
