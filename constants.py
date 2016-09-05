import pygame


class Constant:
    BG_COLOR = pygame.Color(38, 100, 100, 255)

    BUBBLE_FRAME_COUNT = 21
    BUBBLE_BLUE = 0
    BUBBLE_VIOLET = 1
    BUBBLE_GREEN = 2
    BUBBLE_LIGHT_BLUE = 3
    BUBBLE_RED = 4
    BUBBLE_YELLOW = 5

    DATA_FOLDER = "assets/"
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

    uniqueInt = 0

    @staticmethod
    def get_unique_int():
        Constant.uniqueInt += 1
        return Constant.uniqueInt
