#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=500, height=250)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 12,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

img.line_color = pero.colors.Blue
img.fill_color = pero.colors.Blue.lighter(.7)

x = 70
y = 30
size = 20

# test asterisk
marker = pero.Asterisk(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'*'\npero.Asterisk")

x += 120

# test cross
marker = pero.Cross(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'x'\npero.Cross")

x += 120

# test plus
marker = pero.Plus(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'+'\npero.Plus")

x += 120

# test circle
marker = pero.Circle(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'o'\npero.Circle")

x = 70
y += 120

# test diamond
marker = pero.Diamond(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'d'\npero.Diamond")

x += 120

# test triangle
marker = pero.Triangle(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'t'\npero.Triangle")

x += 120

# test square
marker = pero.Square(size=size)
marker.draw(img, x=x, y=y)
label.draw(img, x=x, y=y+30, text="'s'\npero.Square")

img.show()
img.export('markers.svg')
