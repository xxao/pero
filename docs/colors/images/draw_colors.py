#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


img = pero.Image(width=1060, height=830)

img.fill_color = pero.colors.GhostWhite
img.fill()

padding = 50
spacing = 7
size = 20
column = 160
height = img.height

label = pero.Text(
    text_align = pero.LEFT,
    text_base = pero.MIDDLE)

glyph = pero.Circle(
    line_color = pero.colors.Grey,
    line_width = 1,
    size = size)

x = padding
y = padding

for color in sorted(pero.COLORS, key=lambda d: d.name):
    glyph.draw(img, x=x, y=y, fill_color=color)
    label.draw(img, x=x + size, y=y, text=color.name)
    
    y += size + spacing
    if y > height - 0.5 * size - padding:
        y = padding
        x += column + size

img.show()
img.export('colors.svg')
