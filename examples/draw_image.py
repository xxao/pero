#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=400, height=400)

img.line_cap = pero.ROUND
img.line_join = pero.ROUND

# fill
img.fill_color = pero.colors.White
img.fill()

# body
img.line_width = 3
img.line_color = pero.colors.Orange.darker(.1)
img.fill_color = pero.colors.Orange
img.draw_circle(200, 200, 150)

# shadow
img.line_color = None
img.fill_color = pero.colors.White.darker(.1)
img.draw_ellipse(200, 370, 100, 20)

# eyes
img.fill_color = pero.colors.Black
img.draw_circle(140, 170, 30)
img.draw_circle(260, 170, 30)

# eye brows
img.line_color = pero.colors.Black
img.fill_color = None
img.line_width = 7
img.draw_arc(140, 170, 45, pero.rads(-100), pero.rads(-20))
img.draw_arc(260, 170, 45, pero.rads(200), pero.rads(280))

# mouth
img.line_width = 10
img.draw_arc(200, 200, 100, pero.rads(40), pero.rads(80))

# highlight
img.line_color = pero.colors.Orange.lighter(.3)
img.draw_arc(200, 200, 135, pero.rads(220), pero.rads(260))

# hat
path = pero.Path(pero.WINDING)
path.ellipse(200, 55, 80, 20)
path.ellipse(200, 35, 50, 20)
path.rect(175, 35, 50, 20)

mat = pero.Matrix().rotate(pero.rads(20), 200, 200)
path.transform(mat)

img.line_color = None
img.fill_color = pero.colors.Black
img.draw_path(path)

img.show()
