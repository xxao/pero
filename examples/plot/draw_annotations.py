#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 100)
sin_data = numpy.sin(x_data)
cos_data = numpy.cos(x_data)
tan_data = numpy.tan(x_data)
x_data /= numpy.pi

# init plot
plot = pero.plot.Plot()
plot.x_axis.title = "pi"
plot.x_axis.zoom(-1.5, 1.5)
plot.y_axis.title = "f(x)"
plot.y_axis.zoom(-1.5, 1.5)
plot.y_axis.symmetric = False
plot.y_axis.autoscale = False
plot.legend.position = pero.N
plot.legend.orientation = pero.HORIZONTAL

# add series
sin_series = pero.plot.Scatter(x=x_data, y=sin_data, title="sin(x)", marker='o')
cos_series = pero.plot.Profile(x=x_data, y=cos_data, title="cos(x)", marker='s')
tan_series = pero.plot.Scatter(x=x_data, y=tan_data, title="tan(x)", marker='t')

plot.plot(sin_series)
plot.plot(cos_series)
plot.plot(tan_series)

# show labels
tan_series.show_labels = True
tan_series.label.visible = lambda d: abs(d[1]) > 1
tan_series.label.text = lambda d: "%.1f" % d[1]
tan_series.label.text_align = pero.LEFT
tan_series.label.text_base = pero.MIDDLE
tan_series.label.x_offset = 8
tan_series.label.y_offset = 0

# show tooltip
tooltip = lambda d: "%.2f pi\n%.2f" % tuple(d)
sin_series.tooltip.text = tooltip
cos_series.tooltip.text = tooltip
tan_series.tooltip.text = tooltip

# add unit rectangle annotation
rect = pero.Bar(
    fill_color = pero.colors.LightBlue.opaque(0.2),
    line_color = pero.colors.LightBlue,
    left = -1,
    right = 1,
    top = 1,
    bottom = -1)

plot.annotate(rect, x_props=('left', 'right'), y_props=('top', 'bottom'), z_index=.4)

# add zero lines annotations
x_zero = pero.Line(
    line_color = pero.colors.Grey,
    x1 = 0,
    x2 = 0,
    y1 = lambda x: plot.y_axis.scale.out_range[0],
    y2 = lambda x: plot.y_axis.scale.out_range[1])

plot.annotate(x_zero, x_props=('x1', 'x2'), z_index=.5)

y_zero = pero.Line(
    line_color = pero.colors.Grey,
    x1 = lambda x: plot.x_axis.scale.out_range[0],
    x2 = lambda x: plot.x_axis.scale.out_range[1],
    y1 = 0,
    y2 = 0)

plot.annotate(y_zero, y_props=('y1', 'y2'), z_index=.5)

# add arrow annotation
arrow = pero.Arrow.create(
    '<|s|>',
    x1 = -.5,
    y1 = 1,
    x2 = .5,
    y2 = -1,
    line_color = pero.colors.Black,
    fill_color = pero.colors.Black,
    line_style = pero.DASHDOTTED)

plot.annotate(arrow, x_props=('x1', 'x2'), y_props=('y1', 'y2'))

# add text annotations
left_text = pero.Textbox(
    x = -.5,
    y = 1,
    text = "-pi/2",
    text_align = pero.RIGHT,
    text_base = pero.MIDDLE,
    line_color = pero.colors.Green,
    fill_color = pero.colors.LightGreen.lighter(0.5),
    radius = 3)

plot.annotate(left_text, x_props=('x',), y_props=('y',), x_offset=-5)

right_text = pero.Textbox(
    x = .5,
    y = -1,
    text = "+pi/2",
    text_align = pero.LEFT,
    text_base = pero.MIDDLE,
    line_color = pero.colors.Red,
    fill_color = pero.colors.Red.lighter(0.5),
    radius = 3)

plot.annotate(right_text, x_props=('x',), y_props=('y',), x_offset=5)

# show plot
plot.view("Plot with Annotations")
