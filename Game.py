import pygame
import LevelSelector
from Puzzle import Puzzle
import ImagePiece
from singleton import singleton
from weakref import WeakValueDictionary
import sys

listLocation = []

@singleton
class GameSingleton:
    """The game class."""

    _instances = WeakValueDictionary()

    def __init__(self, width, height, game_rect=(0, 0, 328, 328)):
        # Set the display screen dimensions
        self.width, self.height = width, height
        self.game_rect = game_rect
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Screen title
        pygame.display.set_caption("SiratulPuzzle")
        # Creates the level selector
        self.level_selector = LevelSelector.LevelSelector(on_select=self.start)
        # Marks the game as running, but level was not selected yet
        self.running = True
        self.started = False
        self.isBreak = False

    def start(self, image_path, image_text):
        """Starts the game, loads and shuffles the image."""
        self.puzzle = make_puzzle(image_path, self.game_rect, image_text)
        self.puzzle.shuffle(moves=150)
        self.started = True


    def update(self):
        """Processes input events and updates the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type != pygame.KEYDOWN:
                continue
            # Pass the control to the level selector if game is not started
            if not self.started:
                self.level_selector.update(event)
            else:
                self.puzzle.update(event)

    def draw(self):
        """Draws either the level selector or the game puzzle."""
        surface = self.screen
        if not self.started:
            self.level_selector.draw(surface)
        else:
            self.puzzle.draw(surface)

    def game_loop(self):
        """Performs the game loop: process input, update screen etc."""
        clock = pygame.time.Clock()
        while self.running:
            elapsed = clock.tick(30)
            self.screen.fill((0, 0, 0))
            self.update()
            self.draw()
            pygame.display.update()
            if self.isBreak:
                break
        pygame.quit()
        # del GameSingleton
        sys.exit()

def make_puzzle(image_path, board_rect, image_text):
    """Creates the game puzzle"""
    width = 500
    height = 500
    x = 70
    y = 100
    puzzle_image = LevelSelector.load_puzzle_image(image_path, image_size=(width, height))
    image_pieces = list(make_subsurfaces(puzzle_image, offset=(x, y)))
    # Create the puzzle, leaving out the last piece of the image.
    return Puzzle(x, y, image_pieces[:-1], image_path, image_text, listLocation)

def make_subsurfaces(surface, offset=(0, 0)):
    """Cuts the image in small pieces of the same size."""
    width, height = surface.get_size()
    assert width % 4 + height % 4 == 0, ("image's dimention is not div by 4: {}".format(surface.get_size()))

    offx, offy = offset

    constList: list[list[ImageLocation]] = []

    index = 0

    for y in range(0, height, height//4):
        locationList = []
        for x in range(0, width, width // 4):
            subsurface = surface.subsurface(x, y, width//4, height//4)
            # print(f"[x={x} y={y}]", end=' ')
            if(index == 15):
                objectLocation = ImageLocation(-1)
            else:
                objectLocation = ImageLocation(index)

            index += 1
            locationList.append(objectLocation)
            yield ImagePiece.ImagePiece(offx + x, offy + y, subsurface, objectLocation)

        constList.append(locationList)

    global listLocation
    listLocation = constList


class ImageLocation:
    def __init__(self, index):
        self.index = index