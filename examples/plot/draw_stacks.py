#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
categories = ("one", 'two', "three", "four", "five")
y_data1 = numpy.array((5, 10, 7, 3, 4))
y_data2 = numpy.array((7, 5, 9, 1, 5))
y_data3 = numpy.array((2, 1, 3, 5, 4))

# init ordinal x-axis
x_axis = pero.plot.OrdinalAxis(
    position = pero.BOTTOM,
    margin = 0,
    labels = categories,
    label_between = True,
    level = 1)

# init plot
plot = pero.plot.Plot(x_axis=x_axis)
plot.y_axis.title = "count"

# init labels
label = pero.TextLabel(
    text = lambda d: str(d),
    text_color = pero.colors.White,
    text_base = pero.MIDDLE,
    font_size = 13,
    font_weight = pero.BOLD)

# add series
series1 = pero.plot.VBars(
    title = "Series 1",
    data = y_data1,
    x = categories,
    top = y_data1,
    x_mapper = x_axis.mapper,
    anchor = pero.CENTER,
    show_labels = True,
    label = label)

series2 = pero.plot.VBars(
    title = "Series 2",
    data = y_data2,
    x = categories,
    top = y_data2,
    y_offset = y_data1,
    x_mapper = x_axis.mapper,
    anchor = pero.CENTER,
    show_labels = True,
    label = label)

series3 = pero.plot.VBars(
    title = "Series 3",
    data = y_data3,
    x = categories,
    top = y_data3,
    y_offset = y_data1 + y_data2,
    x_mapper = x_axis.mapper,
    anchor = pero.CENTER,
    show_labels = True,
    label = label)

plot.plot(series1, x_axis=x_axis)
plot.plot(series2, x_axis=x_axis)
plot.plot(series3, x_axis=x_axis)

# show plot
plot.zoom()
plot.view("Stacked Series")
