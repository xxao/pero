#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=590, height=100)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 18,
    font_family = pero.SANS,
    font_name = pero.UNDEF)

line = pero.Line(
    line_width = 2,
    line_color = pero.colors.Red)

line.draw(img, x1=30-10, y1=50, x2=30+110, y2=50)
label.draw(img, x=30, y=50, text="pero.TOP", text_base=pero.TOP)

line.draw(img, x1=200-10, y1=50, x2=200+140, y2=50)
label.draw(img, x=200, y=50, text="pero.MIDDLE", text_base=pero.MIDDLE)

line.draw(img, x1=400-10, y1=50, x2=400+150, y2=50)
label.draw(img, x=400, y=50, text="pero.BOTTOM", text_base=pero.BOTTOM)

img.show()
img.export('text_base.svg')
