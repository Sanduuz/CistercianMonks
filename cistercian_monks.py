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


def encode_message(message: list) -> Image.Image:
    """
    Input is a message with words separated in a list.
    The function returns a PIL image that can be then displayed.
    """

    print("[*] Generating random numbers...")
    numbers = gen_numbers(" ".join(message))

    msg_length = 0

    # Calculate image dimensions (Approximate a square)
    for word in message:
        msg_length += len(word)

    dimension = math.ceil(math.sqrt(msg_length))
    x, y = 150 * dimension, 200 * dimension 

    # "1" means black and white image
    image = Image.new("1", (x, y), "white")

    offset_x, offset_y = 0, 0

    for number in numbers:
        a, b, c, d = map(int, list(number))

        symbol_a = symbols[3*9 + a - 1] if a != 0 else symbols[-1]
        symbol_b = symbols[2*9 + b - 1] if b != 0 else symbols[-1]
        symbol_c = symbols[1*9 + c - 1] if c != 0 else symbols[-1]
        symbol_d = symbols[0*9 + d - 1] if d != 0 else symbols[-1]

        # Combine images
        symbol_part_1 = ImageChops.logical_and(symbol_a, symbol_b)
        symbol_part_2 = ImageChops.logical_and(symbol_c, symbol_d)
        symbol = ImageChops.logical_and(symbol_part_1, symbol_part_2)

        image.paste(symbol, (offset_x, offset_y))

        offset_x += 150
        if offset_x >= 150 * dimension:
            offset_x = 0
            offset_y += 200

    image.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit(f"Usage: {sys.argv[0]} <(E)ncode/(D)ecode> <Message/Cipher_file>")

    option = sys.argv[1].upper()
    data = sys.argv[2:]

    # Load graphics
    print("[*] Loading graphics...")
    symbols = load_graphics()

    if option == "E":
        encode_message(data)

    elif option == "D":
        exit("Not implemented yet.")
        for file in data:
            if os.path.isfile(file):
                decode_message(file)
            else:
                exit(f"[!] No such file - {data}")

    else:
        exit(f"Invalid option {option}")
