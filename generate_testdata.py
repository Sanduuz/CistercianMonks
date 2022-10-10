#!/usr/bin/env python3

import os
import sys
import math
import random
from PIL import Image, ImageChops


def load_graphics(graphics_folder: str = "graphics") -> list:
    """
    This function loads the cistercian monk cipher
    symbols from the graphics_folder and returns
    them in a list.
    """

    graphics = []
    graphic_files = os.listdir(graphics_folder)
    graphic_files.sort()

    for graphic in graphic_files:
        graphics.append(Image.open(f"{graphics_folder}/{graphic}").convert("1"))

    return graphics


def gen_numbers(string: str) -> list:
    """
    Generate random numbers to mix up symbols.
    This is done to prevent frequency analysis
    on output.
    """

    numbers = []

    for char in string:
        num = ord(char)
        found = False
        while not found:
            random_number = random.randint(1, 9999)
            if random_number % 127 == num:
                found = True
        numbers.append(str(random_number).zfill(4))

    return numbers


def encode_message(message: str) -> None:
    """
    Input is a message with words separated in a list.
    The function saves the symbols as testdata.
    """

    symbols = load_graphics()
    numbers = gen_numbers(message)

    # "1" means black and white image

    for number in numbers:
        image = Image.new("1", (150, 200), "white")
        a, b, c, d = map(int, list(number))

        symbol_a = symbols[3*9 + a - 1] if a != 0 else symbols[-1]
        symbol_b = symbols[2*9 + b - 1] if b != 0 else symbols[-1]
        symbol_c = symbols[1*9 + c - 1] if c != 0 else symbols[-1]
        symbol_d = symbols[0*9 + d - 1] if d != 0 else symbols[-1]

        # Combine images
        symbol_part_1 = ImageChops.logical_and(symbol_a, symbol_b)
        symbol_part_2 = ImageChops.logical_and(symbol_c, symbol_d)
        symbol = ImageChops.logical_and(symbol_part_1, symbol_part_2)

        image.paste(symbol)
        image.save(f"testdata/{a}{b}{c}{d}.png")

if __name__ == "__main__":
    encode_message("testdata")
