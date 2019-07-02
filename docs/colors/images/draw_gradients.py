#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


img = pero.Image(width=800, height=830)

img.fill_color = pero.colors.GhostWhite
img.fill()

steps = 128
padding = 20
spacer = 5
indent = 80

width, height = img.viewport.wh
length = width - indent - 2 * padding
thickness = (height - 2 * padding) / len(pero.GRADIENTS) - spacer
y = padding

label = pero.Text(
    text_align = pero.RIGHT,
    text_base = pero.MIDDLE)

glyph = pero.ColorBar(
    orientation = pero.HORIZONTAL,
    x = padding + indent,
    length = length,
    thickness = thickness,
    line_color = pero.colors.Grey,
    steps = steps)

for gradient in sorted(pero.GRADIENTS, key=lambda d: d.name):
    
    label.draw(img, x=padding + indent - 10, y=y + 0.5 * thickness, text=gradient.name)
    glyph.draw(img, y=y, gradient=gradient)
    
    y += spacer + thickness

img.show()
img.export('gradients.svg')
