#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw

def define_lines(x: int = 75, y: int = 25) -> list:
    # Coordinates for lines. 1 Length unit for line is 50.
    center_vertical_line    = [(x, y), (x, y + 3*50)]
    top_line                = [(x, y), (x + 50, y)]
    second_top_line         = [(x, y + 50), (x + 50, y + 50)]
    tilted_down_line        = [(x, y), (x + 50, y + 50)]
    tilted_up_line          = [(x, y + 50), (x + 50, y)]
    top_vertical_line       = [(x + 50, y), (x + 50, y + 50)]

    # Other symbols can be made with combinations
    # of lines defined above + rotations.

    # Symbols without rotations
    symbols = [
        [center_vertical_line, top_line],
        [center_vertical_line, second_top_line],
        [center_vertical_line, tilted_down_line],
        [center_vertical_line, tilted_up_line],
        [center_vertical_line, top_line, tilted_up_line],
        [center_vertical_line, top_vertical_line],
        [center_vertical_line, top_line, top_vertical_line],
        [center_vertical_line, second_top_line, top_vertical_line],
        [center_vertical_line, top_line, second_top_line, top_vertical_line],
    ]

    return symbols

def draw_symbol(symbol_data: list) -> Image.Image:
    image = Image.new("1", (150, 200), "white")
    draw = ImageDraw.Draw(image)

    for line in symbol_data:
        draw.line(line, width=4)

    return image

for num in range(1, 10):
    symbols = define_lines()
    # Generate first instances of symbols without rotations
    draw_symbol(symbols[num - 1]).save(f"graphics/{str(num).zfill(4)}.png")

    # Generate horizontally rotated symbols
    draw_symbol(symbols[num - 1]).transpose(Image.Transpose.FLIP_TOP_BOTTOM).save(f"graphics/{str(num * 100).zfill(4)}.png")

    symbols = define_lines(x = 73)  # Decrement x by 2 pixels to fix offset of transposing
    # Generate vertically rotated symbols
    draw_symbol(symbols[num - 1]).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(f"graphics/{str(num * 10).zfill(4)}.png")

    # Generate vertically and horizontally rotated symbols
    draw_symbol(symbols[num - 1]).transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM).save(f"graphics/{str(num * 1000).zfill(4)}.png")

# Generate 1 blank image
Image.new("1", (150, 200), "white").save("graphics/blank.png")