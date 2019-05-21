#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

width = 400
height = 400
padding = 30
margin = 10

size = (height - 2*padding - 3*margin) / 4
x = padding
y = padding

x_data = [1,2,3,4,5,6,7,8,9,10]
y_data = [5,2,7,3,9,2,8,6,1,10]

x_scale = pero.LinScale()
x_scale.in_range = (x_data[0], x_data[-1])
x_scale.out_range = (padding, width-padding)

y_scale = pero.LinScale()
y_scale.in_range = (-1, 11)
y_scale.out_range = (y+size-padding, y)

img = pero.Image(width=width, height=height)
img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.LEFT)

glyph = pero.Profile(
    show_line = True,
    show_points = True,
    show_area = True,
    line_color = pero.colors.Blue,
    fill_color = pero.colors.Blue.lighter(0.7),
    marker_size = 8,
    marker_line_color = pero.colors.White,
    marker_fill_color = pero.colors.Blue)

glyph.draw(img, steps=pero.NONE, x=x_scale.scale(x_data), y=y_scale.scale(y_data), base=y_scale.scale(0))
label.draw(img, x=x, y=y+50, text="pero.NONE")

y += size + margin
y_scale.out_range = (y+size-padding, y)

glyph.draw(img, steps=pero.BEFORE, x=x_scale.scale(x_data), y=y_scale.scale(y_data), base=y_scale.scale(0))
label.draw(img, x=x, y=y+50, text="pero.BEFORE")

y += size + margin
y_scale.out_range = (y+size-padding, y)

glyph.draw(img, steps=pero.AFTER, x=x_scale.scale(x_data), y=y_scale.scale(y_data), base=y_scale.scale(0))
label.draw(img, x=x, y=y+50, text="pero.AFTER")

y += size + margin
y_scale.out_range = (y+size-padding, y)

glyph.draw(img, steps=pero.MIDDLE, x=x_scale.scale(x_data), y=y_scale.scale(y_data), base=y_scale.scale(0))
label.draw(img, x=x, y=y+50, text="pero.MIDDLE")

img.show()
img.export('line_step.svg')
