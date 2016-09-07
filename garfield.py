from abc import abstractproperty, abstractmethod

import pygame

image_cache = {}


def garfield_load_image(path):
    """Load  image quickly by using cache, copy the image if you want to edit"""
    global image_cache
    if not image_cache.__contains__(path):
        image_cache[path] = pygame.image.load(path)
    return image_cache[path]


def garfield_pick_color(image, position):
    (x, y) = position
    x = int(x)
    y = int(y)
    if x < 0 or y < 0 or x >= image.get_width() or y >= image.get_height():
        return None
    return image.get_at((x, y))


mixer_init = False


def garfield_mixer_init():
    global mixer_init
    if not mixer_init:
        pygame.mixer.init()
    mixer_init = True


def garfield_music_load(path):
    garfield_mixer_init()
    pygame.mixer.music.load(path)


def garfield_music_play(times):
    garfield_mixer_init()
    pygame.mixer.music.play(times)


def garfield_music_stop():
    garfield_mixer_init()
    pygame.mixer.music.stop()


def garfield_music_is_busy():
    garfield_mixer_init()
    return pygame.mixer.music.get_busy()


sound_cache = {}


def garfield_sound_play(path, times=0):
    global sound_cache
    if not sound_cache.__contains__(path):
        sound_cache[path] = pygame.mixer.Sound(path)
    sound_cache[path].play(times)


class Drawable:
    @abstractmethod
    def draw(self, screen=None, position=(0, 0)):
        pass


class Interactive:
    @abstractproperty
    def on_mouse_pressed(self, button, position):
        """Called when mouse is pressed. button : int(1:3); position : (int, int)"""
        return False

    @abstractmethod
    def on_mouse_released(self, button, position):
        """Called when mouse is pressed. button : int(1:3); position : (int, int)"""
        return False

    @abstractmethod
    def on_mouse_move(self, position, rel, buttons):
        """Called when mouse is moved. button : (int, int, int); position : (int, int), rel : position : (int, int)"""
        pass


class Garfield(Drawable, Interactive):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 45
        self.duration = 1000 // self.fps
        self.lastUpdateTime = 0
        self.deltaTime = 0
        self.caption = "Garfield"
        self.screen = None
        self.isContinue = True

    @abstractmethod
    def setting(self):
        """Create size, setup caption"""
        pass

    @abstractmethod
    def setup(self):
        """Called before first frame, after setting and windows is create, load your image here"""
        pass

    # library function
    def size(self, size):
        """setup size of screen, call in setting()"""
        (self.width, self.height) = size

    def window_caption(self, caption):
        """setup caption of screen, call in setting()"""
        self.caption = caption
        if self.screen is not None:
            pygame.display.set_caption(self.caption)

    def frame_rate(self, rate):
        self.fps = rate
        self.duration = 1000 // rate

    def exit(self):
        self.isContinue = False

    def __wait_for_next_frame__(self):
        current_time = pygame.time.get_ticks()
        remain_time = self.duration - current_time + self.lastUpdateTime
        if remain_time > 0:
            pygame.time.delay(remain_time)
        current_time = pygame.time.get_ticks()
        self.deltaTime = current_time - self.lastUpdateTime
        self.lastUpdateTime = current_time

    def __init_windows__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

    def __main_loop__(self):
        while self.isContinue:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_released(event.button, event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_pressed(event.button, event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.on_mouse_move(event.pos, event.rel, event.buttons)

            self.draw(self.screen, (0, 0))
            pygame.display.update()
            self.__wait_for_next_frame__()
            pass
        pygame.quit()

    def __main__(self):
        self.setting()
        self.setup()
        self.__init_windows__()
        self.__main_loop__()
        pass
