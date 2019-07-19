#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=600, height=450)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 14,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_align = pero.CENTER,
    text_base = pero.MIDDLE)

circle = pero.Circle(
    size = 100,
    line_width = 2,
    line_color = pero.colors.Red,
    fill_color = None)

rotations = {
    pero.NONE: 'NONE',
    pero.FOLLOW: 'FOLLOW',
    pero.NATURAL: 'NATURAL',
    pero.FACEOUT: 'FACEOUT',
    pero.FACEIN: 'FACEIN'}

x = 0
y = 50 + 0.5*circle.size

for i, rotation in enumerate(rotations):
    
    if i == 3:
        x = 0
        y += 220
    
    x += 50 + 0.5*circle.size
    
    circle.draw(img, x=x, y=y)
    
    text = "pero.%s" % rotations[rotation]
    label.draw(img, text=text, x=x, y=y+0.5*circle.size+50)
    
    img.font_size = 12
    for angle in range(0, 360, 45):
        text = "%d" % angle
        img.draw_text_polar(text, x, y, 0.55*circle.size, pero.rads(angle), rotation=rotation, position=pero.OUTSIDE)
    
    x += 100

img.show()
img.export('text_rotation.svg')
