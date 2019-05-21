#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=450, height=80)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 16,
    font_name = pero.UNDEF,
    text_base = pero.MIDDLE)

label.draw(img, x=30, y=40, text="pero.SERIF", font_family=pero.SERIF)
label.draw(img, x=160, y=40, text="pero.SANS", font_family=pero.SANS)
label.draw(img, x=300, y=40, text="pero.MONO", font_family=pero.MONO)

img.show()
img.export('font_family.svg')
