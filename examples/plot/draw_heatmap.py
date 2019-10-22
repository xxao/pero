#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
count = 25
data = []

for x in numpy.linspace(-numpy.pi, numpy.pi, count):
    for y in numpy.linspace(-numpy.pi, numpy.pi, count):
        z = (numpy.sin(x) + numpy.sin(y))/2
        data.append((x/numpy.pi, y/numpy.pi, z))

data = numpy.array(data)
z_min = numpy.min(data[:, 2])
z_max = numpy.max(data[:, 2])

# init plot
plot = pero.plot.Plot()
plot.x_axis.title = "pi"
plot.x_axis.ticker.major_step = 0.5
plot.y_axis.title = "pi"
plot.y_axis.ticker.major_step = 0.5

# init color bar
color_bar = pero.plot.ColorBar(
    position = pero.RIGHT,
    gradient = pero.colors.YlOrBr,
    margin = 0)

# init z-axis
z_axis = pero.plot.LinAxis(
    title = "sin",
    position = pero.RIGHT,
    level = 3,
    margin = 0,
    show_line = False)

# add bar and axis
plot.add(color_bar)
plot.add(z_axis)

# map bar scale to z-axis
plot.map(color_bar, z_axis, scale='scale')

# add series
series = pero.plot.Rects(
    data = data,
    x = lambda d: d[0],
    y = lambda d: d[1],
    width = 2/(count-1),
    height = 2/(count-1),
    margin = 0,
    line_width = 0,
    fill_color = lambda d: color_bar.convert(d[2]))

plot.plot(series)

# map series z-range to z-axis
plot.map(series.tag, z_axis.tag, limits=lambda *d: (z_min, z_max))

# show plot
plot.zoom()
plot.view("Heatmap Plot", 600, 500)
