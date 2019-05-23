#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

img = pero.Image(width=200, height=200)

img.line_cap = pero.ROUND
img.line_join = pero.ROUND

# fill
img.fill_color = pero.colors.White
img.fill()

# body
img.line_width = 2
img.line_color = pero.colors.Orange.darker(.1)
img.fill_color = pero.colors.Orange
img.draw_circle(100, 100, 75)

# shadow
img.line_color = None
img.fill_color = pero.colors.White.darker(.1)
img.draw_ellipse(100, 185, 70, 10)

# eyes
img.fill_color = pero.colors.Black
img.draw_circle(70, 85, 15)
img.draw_circle(130, 85, 15)

# eye brows
img.line_color = pero.colors.Black
img.fill_color = None
img.line_width = 3
img.draw_arc(70, 85, 23, pero.rads(-100), pero.rads(-20))
img.draw_arc(130, 85, 23, pero.rads(200), pero.rads(280))

# mouth
img.line_width = 5
img.draw_arc(100, 100, 50, pero.rads(40), pero.rads(80))

# highlight
img.line_color = pero.colors.Orange.lighter(.3)
img.draw_arc(100, 100, 68, pero.rads(220), pero.rads(260))

# hat
path = pero.Path(pero.WINDING)
path.ellipse(100, 27, 40, 10)
path.ellipse(100, 17, 30, 10)
path.rect(85, 17, 30, 10)

mat = pero.Matrix().rotate(pero.rads(20), 100, 100)
path.transform(mat)

img.line_color = None
img.fill_color = pero.colors.Black
img.draw_path(path)

img.show()
img.export('image.svg')
