#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# init axes
left_axis = pero.plot.LogAxis(title="Left Axis (log10)", position=pero.LEFT, margin=0, tag="left_axis")
left_axis.scale.in_range = (1, 1.e5)
left_axis.level = 2

bottom_axis = pero.plot.LinAxis(title="Bottom Axis (lin)", position=pero.BOTTOM, margin=0, tag="bottom_axis")
bottom_axis.scale.in_range = (-200, 555)
bottom_axis.ticker.minor_count = 5
bottom_axis.level = 1

right_axis = pero.plot.LinAxis(title="Right Axis", position=pero.RIGHT, margin=0, tag="right_axis")
right_axis.ticker.formatter.hide_suffix = True
right_axis.scale.in_range = (1, 1.e5)
right_axis.level = 2

top_axis = pero.plot.LinAxis(title="Top Axis", position=pero.TOP, margin=0, tag="top_axis")
top_axis.scale.in_range = (0.1, 1500)
top_axis.label_angle = -45
top_axis.label_text_align = pero.LEFT
top_axis.level = 1

ordinal_axis = pero.plot.OrdinalAxis(title="Ordinal Axis", position=pero.BOTTOM, margin=(20, 0, 0, 0), tag="ordinal_axis", z_index=3)
ordinal_axis.labels = ("one", 'two', "three", "four", "five")
ordinal_axis.label_between = True
ordinal_axis.static = False
ordinal_axis.level = 3

color_axis = pero.plot.LinAxis(title="Color Axis", position=pero.RIGHT, margin=0, tag="color_axis", z_index=3)
color_axis.scale.in_range = (0, 1)
color_axis.static = False
color_axis.level = 3

color_bar = pero.plot.ColorBar(position=pero.RIGHT, margin=(0, 0, 0, 20), tag="color_bar", z_index=2)
color_bar.gradient = pero.colors.YlOrRd

# init grids
h_grid = pero.plot.Grid()
h_grid.scale = left_axis.scale
h_grid.ticker = left_axis.ticker

v_grid = pero.plot.Grid()
v_grid.scale = bottom_axis.scale
v_grid.ticker = bottom_axis.ticker

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
