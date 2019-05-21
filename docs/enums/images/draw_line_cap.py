#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=450, height=100)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

pather = pero.Pather(
    line_width = 15,
    line_cap = pero.BUTT,
    fill_color = None,
    anchor_size = 6,
    anchor_fill_color = pero.colors.Red,
    cursor = None)

path = pero.Path().line_to(80, 0)

x = 30
y = 40

mat = pero.Matrix().translate(x, y)
pather.draw(img, path=path.transformed(mat), line_cap=pero.BUTT)
label.draw(img, x=x+40, y=y+15, text="pero.BUTT")

x += 150
mat = pero.Matrix().translate(x, y)
pather.draw(img, path=path.transformed(mat), line_cap=pero.ROUND)
label.draw(img, x=x+40, y=y+15, text="pero.ROUND")

x += 150
mat = pero.Matrix().translate(x, y)
pather.draw(img, path=path.transformed(mat), line_cap=pero.SQUARE)
label.draw(img, x=x+40, y=y+15, text="pero.SQUARE")

img.show()
img.export('line_cap.svg')
