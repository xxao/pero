#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=350, height=80)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 16,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.MIDDLE)

label.draw(img, x=30, y=40, text="pero.NORMAL", font_style=pero.NORMAL)
label.draw(img, x=200, y=40, text="pero.ITALIC", font_style=pero.ITALIC)

img.show()
img.export('font_style.svg')
