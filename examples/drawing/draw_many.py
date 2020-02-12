#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import numpy

# init size
width = 400
height = 300
padding = 50

# init data
x_data = numpy.linspace(-numpy.pi, numpy.pi, 50)
y_data = numpy.sin(x_data)

# init scales
x_scale = pero.LinScale(
    in_range = (min(x_data), max(x_data)),
    out_range = (padding, width-padding))

y_scale = pero.LinScale(
    in_range = (-1, 1),
    out_range = (height-padding, padding))

color_scale = pero.GradientScale(
    in_range = (-1, 1),
    out_range = pero.colors.Spectral)

# init marker
marker = pero.Circle(
    size = 8,
    x = lambda d: x_scale.scale(d[0]),
    y = lambda d: y_scale.scale(d[1]),
    line_color = lambda d: color_scale.scale(d[1]).darker(.2),
    fill_color = lambda d: color_scale.scale(d[1]))

# init image
image = pero.Image(width=width, height=height)

# fill
image.fill("w")

# draw points
marker.draw_many(image, zip(x_data, y_data))

# show image
image.show()
