#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=500, height=330)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.LEFT)

line = pero.Line(
    line_color = pero.colors.Black,
    line_width = 5,
    line_cap = pero.BUTT,
    line_join = pero.MITER)

x1 = 30
x2 = 470
y = 30

line.draw(img, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.SOLID)
label.draw(img, x=x1, y=y+10, text="pero.SOLID")

y += 60
line.draw(img, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHED)
label.draw(img, x=x1, y=y+10, text="pero.DASHED")

y += 60
line.draw(img, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DOTTED)
label.draw(img, x=x1, y=y+10, text="pero.DOTTED")

y += 60
line.draw(img, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHDOTTED)
label.draw(img, x=x1, y=y+10, text="pero.DASHDOTTED")

y += 60
line.draw(img, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.CUSTOM, line_dash=[5, 7, 1, 2, 1, 7])
label.draw(img, x=x1, y=y+10, text="pero.CUSTOM")

img.show()
img.export('line_style.svg')
