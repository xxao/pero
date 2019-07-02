#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


img = pero.Image(width=850, height=550)

img.fill_color = pero.colors.GhostWhite
img.fill()

rect_width = 17
rect_height = 17

label = pero.Text(text_base=pero.MIDDLE)

rect = pero.Rect(
    line_width = 1,
    line_color = pero.colors.White,
    width = rect_width,
    height = rect_height)

x = 50
y = 50

for palette in sorted(pero.PALETTES, key=lambda d: d.name):
    
    if x + rect.width * len(palette) > 900:
        x = 50
        y += round(2.5 * rect.height)
    
    title = "%s (%d)" % (palette.name, len(palette))
    label.draw(img, x=x, y=y, text=title)
    
    for color in palette.colors:
        rect.draw(img, x=x, y=y + 10, fill_color=color)
        x += rect.width - rect.line_width
    
    x += 50

img.show()
img.export('palettes.svg')
