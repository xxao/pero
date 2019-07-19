#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=650, height=350)

img.fill_color = pero.colors.GhostWhite
img.fill()

label = pero.Text(
    font_size = 14,
    font_family = pero.SANS,
    font_name = pero.UNDEF,
    text_base = pero.TOP,
    text_align = pero.CENTER)

start_head = pero.NormalHead(
    size = 15,
    line_color = pero.colors.Blue,
    fill_color = pero.colors.Blue.lighter(0.7))

end_head = pero.NormalHead(
    size = 15,
    line_color = pero.colors.Blue,
    fill_color = pero.colors.Blue.lighter(0.7))

img.line_color = pero.colors.Blue
img.fill_color = pero.colors.Blue.lighter(.7)

x = 70
y1 = 30
y2 = 100

arrow = pero.LineArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2)
label.draw(img, x=x, y=y2+20, text="'-'\npero.LineArrow")

x += 120

arrow = pero.RayArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x=x-15, y=y1, angle=pero.rads(80), length=70)
label.draw(img, x=x, y=y2+20, text="'/'\npero.RayArrow")

x += 120

arrow = pero.ArcArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x=x, y=0.5*(y1+y2), start_angle=pero.rads(-160), end_angle=pero.rads(40), radius=40, clockwise=True)
label.draw(img, x=x, y=y2+20, text="'c'\npero.ArcArrow")

x += 130

arrow = pero.BowArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x1=x - 30, y1=y1, x2=x+30, y2=y2, radius=50, large=False, clockwise=True)
label.draw(img, x=x, y=y2+20, text="')'\npero.BowArrow")

x += 130

arrow = pero.CurveArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x1=x-25, y1=y1, x2=x+25, y2=y2)
label.draw(img, x=x, y=y2+20, text="'~'\npero.CurveArrow")

x = 100
y1 += 170
y2 += 170

arrow = pero.ConnectorArrow(start_head=start_head, end_head=end_head)
arrow.draw(img, x1=x-30, y1=y1, x2=x+30, y2=y2)
label.draw(img, x=x, y=y2+20, text="'z'\npero.ConnectorArrow")

x += 180

arrow = pero.ConnectorArrow(start_head=start_head, end_head=end_head, curve=0.85)
arrow.draw(img, x1=x-30, y1=y1, x2=x+30, y2=y2)
label.draw(img, x=x, y=y2+20, text="'s'\npero.ConnectorArrow")

img.show()
img.export('arrows.svg')
