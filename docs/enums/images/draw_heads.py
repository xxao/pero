#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=650, height=180)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 14,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

arrow = pero.LineArrow(
    line_color = pero.colors.Blue,
    fill_color = pero.colors.Blue.lighter(.7))

x = 70
y1 = 30
y2 = 100

head = pero.LineHead(size=15, line_color=pero.colors.Blue)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2, start_head=head, end_head=head)
label.draw(img, x=x, y=y2+20, text="'|'\npero.LineHead")

x += 120

head = pero.OpenHead(size=15, line_color=pero.colors.Blue)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2, start_head=head, end_head=head)
label.draw(img, x=x, y=y2+20, text="'<' or '>'\npero.OpenHead")

x += 120

head = pero.NormalHead(size=15, line_color=pero.colors.Blue)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2, start_head=head, end_head=head)
label.draw(img, x=x, y=y2+20, text="'<|' or '|>'\npero.NormalHead")

x += 130

head = pero.VeeHead(size=15, line_color=pero.colors.Blue)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2, start_head=head, end_head=head)
label.draw(img, x=x, y=y2+20, text="'<<' or '>>'\npero.VeeHead")

x += 130

head = pero.CircleHead(size=15, line_color=pero.colors.Blue)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2, start_head=head, end_head=head)
label.draw(img, x=x, y=y2+20, text="'o'\npero.CircleHead")

img.show()
img.export('heads.svg')
