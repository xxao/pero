#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=350, height=180)

img.fill_color = pero.colors.GhostWhite
img.fill()

img.fill_color = pero.colors.Blue.lighter(0.7)
img.line_color = pero.colors.Blue
img.line_width = 1

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

path = pero.Path.from_svg("M90 10 L137 155 L14 65 L163 65 L43 155 Z")
mat = pero.Matrix()

img.draw_path(path.transformed(mat, pero.EVENODD))
label.draw(img, x=90, y=160, text="pero.EVENODD")

mat.translate(170, 0)
img.draw_path(path.transformed(mat, pero.WINDING))
label.draw(img, x=260, y=160, text="pero.WINDING")

img.show()
img.export('fill_rule.svg')
