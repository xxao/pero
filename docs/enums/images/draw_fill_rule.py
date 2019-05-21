#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=330, height=180)

img.fill_color = pero.colors.GhostWhite
img.fill()

img.fill_color = pero.colors.LightBlue
img.line_color = pero.colors.Black
img.line_width = 1

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

path = pero.Path().move_to(0, -50).line_to(40, 50).line_to(-55, -10).line_to(55, -10).line_to(-40, 50).close()
mat = pero.Matrix()

mat.translate(90, 70)
img.draw_path(path.transformed(mat, pero.EVEN_ODD))
label.draw(img, x=90, y=70+60, text="pero.EVEN_ODD")

mat.translate(150, 0)
img.draw_path(path.transformed(mat, pero.WINDING))
label.draw(img, x=240, y=70+60, text="pero.WINDING")

img.show()
img.export('fill_rule.svg')
