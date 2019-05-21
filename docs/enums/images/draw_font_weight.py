#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=500, height=80)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 16,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.MIDDLE)

label.draw(img, x=30, y=40, text="pero.NORMAL", font_weight=pero.NORMAL)
label.draw(img, x=200, y=40, text="pero.LIGHT", font_weight=pero.LIGHT)
label.draw(img, x=350, y=40, text="pero.BOLD", font_weight=pero.BOLD)

img.show()
img.export('font_weight.svg')
