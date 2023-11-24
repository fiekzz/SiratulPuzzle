import sys

import pygame
import style
from tkinter import *
from tkinter import messagebox

root = Tk()
root.withdraw()

class ItemLevel:
    def __init__(self, image, text):
        self.image, self.text = image, text

class LevelSelector:
    """The level selector scene."""

    # Initialize images
    IMAGES = [
        "assets/images/puzzles/Aqsa.png",
        "assets/images/puzzles/Kurma.png",
        "assets/images/puzzles/Nabawi.png",
        "assets/images/puzzles/Quran.png",
        "assets/images/puzzles/Uhud.png",
    ]

    ITEM_LIST: list[ItemLevel] = [
        ItemLevel("assets/images/puzzles/Aqsa.png", "Masjidil Aqsa, also known as Al-Aqsa Mosque, is situated in the Old City of Jerusalem, Palestine. It is the third holiest site in Islam, following Mecca and Medina. The mosque encompasses the Dome of the Rock, an iconic golden-domed structure, and is surrounded by a vast courtyard. Masjidil Aqsa holds special significance as it is believed to be the place where Prophet Muhammad (peace be upon him) ascended to the heavens during the Night Journey."),
        ItemLevel("assets/images/puzzles/Kurma.png", "Dates, or kurma, are sweet fruits from the date palm tree. With a rich flavor and chewy texture, they serve as a natural sweetener packed with fiber, vitamins, and minerals. Popular in Middle Eastern cuisine, dates are not only delicious but also hold cultural significance, particularly during religious observances like Ramadan. Besides their taste, dates offer health benefits, supporting digestion and heart health."),
        ItemLevel("assets/images/puzzles/Nabawi.png", "Masjid Nabawi in Medina, Saudi Arabia, is the second holiest mosque in Islam. Built by Prophet Muhammad, it houses his tomb under the iconic green dome. Renowned for its historical significance, the mosque's serene atmosphere and architectural beauty draw millions of visitors, providing a sacred space for spiritual reflection and prayer."),
        ItemLevel("assets/images/puzzles/Quran.png", "The Quran is the holy book of Islam, comprising divine revelations received by Prophet Muhammad over 23 years. With 114 chapters, it serves as a guide for faith, morality, and daily life. Written in eloquent Arabic, the Quran is considered the literal word of God, emphasizing monotheism, compassion, and ethical conduct. It holds a central place in Islamic worship, providing spiritual guidance for millions of believers worldwide."),
        ItemLevel("assets/images/puzzles/Uhud.png", "Uhud, a mountain near Medina, Saudi Arabia, gained historical prominence due to the Battle of Uhud in 625 CE. Fought between the Muslims led by Prophet Muhammad and the Quraysh tribe, the battle had strategic implications despite initial successes. Uhud remains a symbol of resilience and is visited by pilgrims, serving as a reminder of the challenges faced by the early Muslim community."),
    ]

    # Select level constructor
    def __init__(self, on_select):
        self.on_select = on_select  # Callback to start the game
        # Start with level index 0
        self._level = 0
        # Load images into game image
        self._images = []
        for item in self.ITEM_LIST:
            self._images.append(load_puzzle_image(item.image, image_size=(250, 250)))
        # self._select = pygame.image.load("select.png").convert_alpha()

    def prev(self):
        """Slide to the previous image."""
        if self._level > 0:
            self._level -= 1

    def next(self):
        """Slide to the next image."""
        if self._level < len(self._images) - 1:
            self._level += 1

    def _current_puzzle(self):
        """Returns the image for the current level."""
        return self._images[self._level]

    def _prev_puzzle(self):
        """Returns the image for the previous level (if exists)."""
        if self._level > 0:
            return self._images[self._level - 1]

    def _next_puzzle(self):
        """Returns the image for the next level (if exists)."""
        if self._level < len(self._images) - 1:
            return self._images[self._level + 1]

    # Update the user input arrow down, left, right, return
    def update(self, event):
        if event.type != pygame.KEYDOWN:
            return
        elif event.key == pygame.K_LEFT:
            self.prev()
        elif event.key == pygame.K_RIGHT:
            self.next()
        elif event.key == pygame.K_RETURN:
            # self.on_select(self.IMAGES[self._level])
            self.on_select(self.ITEM_LIST[self._level].image, self.ITEM_LIST[self._level].text)
        elif event.key == pygame.K_ESCAPE:
            if confirm_quit():
                pygame.quit()
                sys.exit()

    def draw(self, surface):
        pos = ((20, 200), (375, 250), (730, 200))
        levels = (self._prev_puzzle(),
                  self._current_puzzle(),
                  self._next_puzzle())
        # Draws the images at the predefined positions
        for level, p in zip(levels, pos):
            if level is not None:
                surface.blit(level, p)
        # Draws a white border around the current image and the `select puzzle` image
        # pygame.draw.rect(surface, (255, 255, 255), (80, 94, 240, 240), 3)
        pygame.draw.rect(surface, (255, 255, 255), (360, 235, 280, 280), 1, border_radius=30)
        # surface.blit(self._select, (423.5, 40))
        # TITLE TEXT
        # text = style.fontTitle.render("Welcome to SiratulPuzzle!", True, white_color)
        text = style.fontTitle.render("Welcome to SiratulPuzzle!", True, style.white_color)
        text_rect = text.get_rect()
        text_rect.center = (500, 100)
        surface.blit(text, text_rect)
        # Arrow picture
        arrowFont = pygame.font.Font(style.font_path, 30)
        arrowText = arrowFont.render("[<-] left   [->] right    [Enter] to choose   [ESC] exit game", True, style.white_color)
        arrow_rect = arrowText.get_rect()
        arrow_rect.center = (500, 600)
        surface.blit(arrowText, arrow_rect)

def load_puzzle_image(path, image_size):
    surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(surface, image_size)

def load_puzzle_text(text):
    return

def confirm_quit():
    result = messagebox.askokcancel("Quit Game", "Are you sure you want to quit game?")
    return result