import pygame
from random import choice
from tkinter import messagebox
import Game
import style
import sys
import numpy as n
from singleton import singleton

class Piece:
    def __init__(self, image_piece, index):
        self.image_piece, self.index = image_piece, index

class FixedList:
    fixed_list = [[0, 1, 2, 3],
                 [4,  5, 6, 7],
                 [8, 9, 10, 11],
                 [12, 13, 14, -1]]


class Puzzle:
    """The puzzle object."""

    def __init__(self, x, y, image_pieces, image_path, image_text: str, imageLocation: list):
        self.x, self.y, self.image_pieces, self.image_path, self.image_text = x, y, image_pieces, image_path, image_text
        self.imageLocation = imageLocation

        self.piecesList: list(Piece) = []
        print("-----------------------------")

    @property
    def rect(self):
        """Returns a rect representing the board."""
        rect = pygame.Rect(self.x, self.y, 0, 0)
        for s in self.image_pieces:
            rect.union_ip(s.rect)
        return rect

    def update(self, event):
        """Processes user's input."""
        if event.type != pygame.KEYDOWN:
            return
        elif event.key == pygame.K_UP:
            self.move('up')
        elif event.key == pygame.K_RIGHT:
            self.move('right')
        elif event.key == pygame.K_DOWN:
            self.move('down')
        elif event.key == pygame.K_LEFT:
            self.move('left')
        elif event.key == pygame.K_ESCAPE:
            if confirm_quit():
                game = Game.GameSingleton()
                game.started = False


    def swap_up(self, row, col):
        if row > 0:
            self.imageLocation[row][col], self.imageLocation[row - 1][col] = self.imageLocation[row - 1][col], self.imageLocation[row][col]

    def swap_down(self, row, col):
        if row < len(self.imageLocation) - 1:
            # print(f"Row={row}")
            self.imageLocation[row][col], self.imageLocation[row + 1][col] = self.imageLocation[row + 1][col], self.imageLocation[row][col]

    def swap_right(self, row, col):
        if col < len(self.imageLocation[0]) - 1:
            self.imageLocation[row][col], self.imageLocation[row][col + 1] = self.imageLocation[row][col + 1], self.imageLocation[row][col]

    def swap_left(self, row, col):
        if col > 0:
            self.imageLocation[row][col], self.imageLocation[row][col - 1] = self.imageLocation[row][col - 1], self.imageLocation[row][col]

    def move(self, direction):
        """Move an image piece in the given direction. Possible directions
           are 'up', 'right', 'down' or 'left'."""
        board_rect = self.rect
        x_spacing, y_spacing = (board_rect.width // 4, board_rect.height // 4)

        # print(board_rect.width // 4, board_rect.height // 4)

        x, y = {
            'up':    (0, -y_spacing),
            'right': (x_spacing, 0),
            'down':  (0, y_spacing),
            'left':  (-x_spacing, 0)
        }[direction]

        # Helper function to check if a rect is valid (inside the puzzle)
        is_valid = board_rect.colliderect
        # The current state of the puzzle
        current_pos = set((s.x, s.y) for s in self.image_pieces)
        # current_location = set(())
        # Searchs sequentially for the only peice that can be moved
        # to the given direction
        for piece in self.image_pieces:
            new_x, new_y = piece.x + x, piece.y + y
            # Checks if the position is empty and is valid (inside the puzzle).
            if ((new_x, new_y) not in current_pos and is_valid(new_x, new_y, piece.width, piece.height)):
                # If everything is ok, then moves the image piece
                piece.x, piece.y = new_x, new_y

        must_break = False

        for i, row in enumerate(self.imageLocation):
            for j, element in enumerate(row):
                if element.index == -1:
                    if direction == 'up':
                        self.swap_down(i, j)
                    elif direction == 'down':
                        self.swap_up(i, j)
                    elif direction == 'right':
                        self.swap_left(i, j)
                    elif direction == 'left':
                        self.swap_right(i, j)
                    must_break = True
                    break

            if must_break:
                break

        print("----------------------------- ^^^ FIXED")
        # print(type(self.fixed_location))
        for row in FixedList.fixed_list:
            for element in row:
                print(element, end=' ')
            print()
        print("----------------------------- ^^^ IMAGELOCATION")

        currentArr = []

        for row in self.imageLocation:
            arr = []
            for element in row:
                print(element.index, end=' ')
                arr.append(element.index)
            print()
            currentArr.append(arr)

        result = compare(currentArr, FixedList.fixed_list)

        # narr1 = n.array([self.imageLocation])
        # narr2 = n.array([FixedList.fixed_list])
        #
        # result = (narr1 == narr2).all()

        print(result)
        if result:
            if confirm_finished():
                game = Game.GameSingleton()
                game.isBreak = True
                # pygame.quit()
                # sys.exit()


    def shuffle(self, moves=100):
        """Shuffles the board applying random moves."""
        for _ in range(moves):
            m = choice(('up', 'right', 'down', 'left'))
            self.move(m)

        # Makes sure the blank space is at the bottom-right corner
        # self.move('left'), self.move('left'), self.move('left')
        # self.move('up'), self.move('up'), self.move('up')

    def draw(self, surface):
        """Draw the image pieces on the surface."""
        for subsurf in self.image_pieces:
            surface.blit(subsurf.image, (subsurf.x, subsurf.y))
        # Draws a white border around the image
        brect = self.rect
        inflated_brect = brect.inflate(int(brect.width * 0.05), int(brect.height * 0.05))
        pygame.draw.rect(surface, (255, 255, 255), inflated_brect, 3)
        navigate_path = "assets/images/ArrowGame.png"
        navigate_image = pygame.image.load(navigate_path).convert_alpha()
        scaled_down = pygame.transform.scale(navigate_image, (200, 150))
        surface.blit(scaled_down, (20, 600))
        navigate_font = pygame.font.Font(style.font_path, 30)
        navigateText = navigate_font.render("Navigate puzzle", True, style.white_color)
        navigate_rect = navigateText.get_rect()
        navigate_rect.center = (320, 675)
        surface.blit(navigateText, navigate_rect)

        puzzle_image = pygame.image.load(self.image_path).convert_alpha()
        scaled_down = pygame.transform.scale(puzzle_image, (200, 200))
        surface.blit(scaled_down, (600, 90))

        container_width = 200
        container_height = 500
        current_line = []
        lines = []
        imageTextFont = pygame.font.Font(style.font_path, 16)

        words = self.image_text.split()
        for word in words:
            test_line = " ".join(current_line + [word])
            text_width, text_height = imageTextFont.size(test_line)

            if text_width <= container_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        lines.append(" ".join(current_line))
        total_text_height = len(lines) * text_height
        y = (container_height - total_text_height) // 2
        W = 1400
        H = 200

        for line in lines:
            imageTextText = imageTextFont.render(line, True, style.white_color)
            imageTextRect = imageTextText.get_rect()
            imageTextRect.midtop = (W // 2, y + H)
            surface.blit(imageTextText, imageTextRect)
            y += text_height

def confirm_quit():
    result = messagebox.askokcancel("Quit Game", "Are you sure you want to quit game?")
    return result

def confirm_finished():
    result = messagebox.showinfo("Game finished", "Congratulations! You have finished the game")
    return result

def compare(a, b): return a == b