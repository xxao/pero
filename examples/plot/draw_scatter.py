#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
count = 50
x_data = numpy.linspace(-5, 5, count)
y_data_1 = numpy.random.normal(0, 1., count)
y_data_2 = numpy.random.normal(0, 5., count)

size_data = 10 + 30 * numpy.random.random(2 * count)
size_scale = pero.OrdinalScale(out_range=size_data, implicit=True)
size = lambda d: size_scale.scale(d[0])

# init plot
plot = pero.plot.Plot()
plot.x_axis.title = "x-value"
plot.y_axis.title = "random"
plot.legend.position = pero.NE
plot.legend.orientation = pero.VERTICAL

# add series
series1 = pero.plot.Circles(x=x_data, y=y_data_1, marker_size=size, marker_fill_alpha=150, title="normal 1")
series2 = pero.plot.Diamonds(x=x_data, y=y_data_2, marker_size=size, marker_fill_alpha=150, title="normal 5")

plot.plot(series1)
plot.plot(series2)

# show plot
plot.zoom()
plot.view("Scatter Series")
