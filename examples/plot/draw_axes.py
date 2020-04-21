#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# init axes
left_axis = pero.plot.LogAxis(
    title = "Left Axis (log10)",
    tag = "left_axis",
    position = pero.LEFT,
    margin = 0,
    scale_in_range = (1, 1.e5),
    level = 2)

bottom_axis = pero.plot.LinAxis(
    title = "Bottom Axis (lin)",
    tag = "bottom_axis",
    position = pero.BOTTOM,
    margin = 0,
    scale_in_range = (-200, 555),
    ticker_minor_count = 5,
    level = 1)

right_axis = pero.plot.LinAxis(
    title = "Right Axis",
    tag = "right_axis",
    position = pero.RIGHT,
    margin = 0,
    ticker_formatter_hide_suffix = True,
    scale_in_range = (1, 1.e5),
    level = 2)

top_axis = pero.plot.LinAxis(
    title = "Top Axis",
    tag = "top_axis",
    position = pero.TOP,
    margin = 0,
    scale_in_range = (0.1, 1500),
    label_angle = -45,
    label_text_align = pero.LEFT,
    level = 1)

ordinal_axis = pero.plot.OrdinalAxis(
    title = "Ordinal Axis",
    tag = "ordinal_axis",
    position = pero.BOTTOM,
    margin = (20, 0, 0, 0),
    z_index = 3,
    labels = ("one", 'two', "three", "four", "five"),
    label_between = True,
    static = False,
    level = 3)

color_axis = pero.plot.LinAxis(
    title = "Color Axis",
    tag = "color_axis",
    position = pero.RIGHT,
    margin = 0,
    z_index = 3,
    scale_in_range = (0, 1),
    static = False,
    level = 3)

color_bar = pero.plot.ColorBar(
    tag = "color_bar",
    position = pero.RIGHT,
    margin = (0, 0, 0, 20),
    z_index = 2,
    gradient = pero.colors.YlOrRd)

# init grids
h_grid = pero.plot.Grid(
    scale = left_axis.scale,
    ticker = left_axis.ticker)

v_grid = pero.plot.Grid(
    scale = bottom_axis.scale,
    ticker = bottom_axis.ticker)

# init plot
plot = pero.plot.Plot(
    x_axis = bottom_axis,
    y_axis = left_axis,
    x_grid = v_grid,
    y_grid = h_grid,
    x_rangebar = None,
    y_rangebar = None)

# add additional axes
plot.add(right_axis)
plot.add(top_axis)
plot.add(ordinal_axis)
plot.add(color_axis)
plot.add(color_bar)
plot.map(color_bar, color_axis, scale='scale')

# show plot
plot.view("Multiple Axes")
