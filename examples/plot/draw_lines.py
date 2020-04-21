#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
count = 9
x1_data = numpy.linspace(-2, 2, count)
y1_data = x1_data**2
x2_data = x1_data-x1_data**3/10 + 0.3
y2_data = y1_data-x1_data**2/10 + 0.5

# init plot
plot = pero.plot.Plot(
    x_axis_title = "x-value",
    y_axis_title = "random")

# add series
series = pero.plot.Lines(
    x1 = x1_data,
    y1 = y1_data,
    x2 = x2_data,
    y2 = y2_data,
    anchor = pero.START,
    start_head = 'o',
    start_head_size = 8,
    end_head = '|>',
    end_head_size = 11,
    title = "Lines")

plot.plot(series)

# show plot
plot.zoom()
plot.view("Lines Series")
