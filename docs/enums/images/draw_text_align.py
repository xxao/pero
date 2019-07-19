#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=500, height=80)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 18,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.MIDDLE)

line = pero.Line(
    line_width = 2,
    line_color = pero.colors.Red)

line.draw(img, x1=30, y1=40-15, x2=30, y2=40+15)
label.draw(img, x=30, y=40, text="pero.LEFT", text_align=pero.LEFT)

line.draw(img, x1=250, y1=40-15, x2=250, y2=40+15)
label.draw(img, x=250, y=40, text="pero.CENTER", text_align=pero.CENTER)

line.draw(img, x1=470, y1=40-15, x2=470, y2=40+15)
label.draw(img, x=470, y=40, text="pero.RIGHT", text_align=pero.RIGHT)

img.show()
img.export('text_align.svg')
