#!/usr/bin/env python3

import os
import sys
import math
import random
import datetime
from PIL import Image, ImageChops, ImageStat

MOD = 512

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
            if random_number % MOD == num:
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

    msg_length = len(" ".join(message))

    # Calculate image dimensions (Approximate a square)
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

    return image


def divide_image(image: Image.Image) -> list:
    """
    This function divides given image into 4 segments.
    This is done to separate 1000, 100, 10 and 1 digits
    from the symbol. When the image is separated into
    4 segments, we only have to try 40 (4*10) different
    symbol parts instead of 9999 combinations.

    The function returns a list of the 4 segments.
    """

    # + 1 once again for offsets

    # Top left segment
    image_tl = image.crop((0, 0, 75 + 1, 100))

    # Top right segment
    image_tr = image.crop((75 + 1, 0, 150, 100))

    # Bottom left segment
    image_bl = image.crop((0, 100, 75 + 1, 200))

    # Bottom right segment
    image_br = image.crop((75 + 1, 100, 150, 200))

    return [image_tl, image_tr, image_bl, image_br]


def compare_images(image1: Image.Image, image2: Image.Image) -> bool:
    """
    This function compares 2 given images and returns
    a bool based on whether the images match or not.
    """

    difference = ImageChops.difference(image1, image2)
    image_stat = ImageStat.Stat(difference)

    if image_stat.extrema[0] == (0, 0):
        return True

    return False


def parse_symbol(message_symbol: Image.Image) -> int:
    """ This function decodes given symbol. """

    numeral = 0

    # [top left, top right, bottom left, bottom right]
    message_symbol_parts = divide_image(message_symbol)

    # Divide symbols into subcategories
    symbols_tr = symbols[:9]
    symbols_tl = symbols[9:2*9]
    symbols_br = symbols[2*9:3*9]
    symbols_bl = symbols[3*9:4*9]

    for index, symbol in enumerate(symbols_tr):
        symbol_tr = divide_image(symbol)[1]
        if compare_images(message_symbol_parts[1], symbol_tr):
            numeral += index + 1
            break

    for index, symbol in enumerate(symbols_tl):
        symbol_tl = divide_image(symbol)[0]
        if compare_images(message_symbol_parts[0], symbol_tl):
            numeral += 10 * (index + 1)
            break

    for index, symbol in enumerate(symbols_br):
        symbol_br = divide_image(symbol)[3]
        if compare_images(message_symbol_parts[3], symbol_br):
            numeral += 100 * (index + 1)
            break

    for index, symbol in enumerate(symbols_bl):
        symbol_bl = divide_image(symbol)[2]
        if compare_images(message_symbol_parts[2], symbol_bl):
            numeral += 1000 * (index + 1)
            break

    return numeral


def decode_numeral(numeral: int) -> str:
    """
    This function takes in a numeral and changes
    it back to its corresponding character according
    to the ASCII table.
    """

    return chr(numeral % MOD)


def get_symbols_from_image(image: Image.Image) -> list:
    """
    This function parses multiple symbols
    from single file and returns a list
    of those symbols.
    """

    image_width, image_height = image.size
    num_of_symbols_x = image_width // 150
    num_of_symbols_y = image_height // 200
    symbol_width = 150
    symbol_height = 200

    symbols = []

    # Rectangle that will be cropped over each symbol at a time
    # [Left, Top, Right, Bottom]
    crop_rect = [0, 0, symbol_width, symbol_height]

    for _ in range(num_of_symbols_y):
        for _ in range(num_of_symbols_x):
            symbol = image.crop(tuple(crop_rect))
            symbols.append(symbol)

            # Add offsets in x level
            crop_rect[0] += symbol_width
            crop_rect[2] += symbol_height

        # Reset x level offsets
        crop_rect[0], crop_rect[2] = 0, symbol_width

        # Add y level offsets
        crop_rect[1] += symbol_height
        crop_rect[3] += symbol_height

    return symbols


if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit(f"Usage: {sys.argv[0]} <(E)ncode/(D)ecode> <Message/Cipher_file>")

    option = sys.argv[1].upper()
    data = sys.argv[2:]

    # Load graphics
    print("[*] Loading graphics...")
    symbols = load_graphics()

    if option == "E":
        image = encode_message(data)
        location = f"output/message_{datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')}.png"
        image.save(location)
        print(f"[+] Encoded message saved - {location}")
        choice = input("[?] Show image now? (y/N): ").upper()
        if choice == "Y":
            image.show()
        elif choice == "N" or choice == "":
            exit()
        else:
            exit(f"Invalid choice - {choice}")

    elif option == "D":
        for file in data:
            if os.path.isfile(file):
                image = Image.open(file)
                print(f"[*] Parsing symbols from file... - {file}")
                message_symbols = get_symbols_from_image(image)
                message = []
                print(f"[*] Decoding symbols...")
                for symbol in message_symbols:
                    message.append(decode_numeral(parse_symbol(symbol)))
                print(f"[+] Decoded message: {''.join(message)}")
            else:
                print(f"[!] No such file - {file}")

    else:
        exit(f"Invalid option {option}")
