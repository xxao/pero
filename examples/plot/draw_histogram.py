#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
data = numpy.random.normal(size=1000)
hist1, bins1 = pero.plot.calc_histogram(data, 50, cumulative=False)
hist2, bins2 = pero.plot.calc_histogram(data, 50, cumulative=True)

# normalize cumulative
hist2 = hist2 * hist1.max() / hist2.max()

# init plot
plot = pero.plot.Plot(
    x_axis_title = 'random',
    y_axis_title = 'count')

# add bars
series = pero.plot.Bars(
    top = hist1,
    left = bins1[:-1],
    right = bins1[1:],
    bottom = 0,
    anchor = pero.TOP,
    margin = (0.05, 0, 0, 0))

plot.plot(series)

# add step line
series = pero.plot.Profile(
    x = bins1[1:],
    y = hist1,
    line_width = 3,
    steps = pero.BEFORE)

plot.plot(series)

# add cumulative
series = pero.plot.Profile(
    x = bins2[1:],
    y = hist2,
    line_width = 2)

plot.plot(series)

# show plot
plot.zoom()
plot.view("Histogram")
