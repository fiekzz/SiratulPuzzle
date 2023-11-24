import pygame
import Game

class ImagePiece(pygame.sprite.Sprite):
    """A piece (subsuface) of the puzzle image."""

    def __init__(self, x, y, subsurface, objectIndex):
        super(ImagePiece, self).__init__()
        # Saves the initial position of this piece. Used later
        # to check if the puzzle is solved or not.
        self.start_pos = (x, y)
        self.x, self.y = x, y
        self.image = subsurface
        self.objectIndex: Game.ImageLocation = objectIndex

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )
