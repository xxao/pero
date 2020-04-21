#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# init plot
plot = pero.plot.Plot(
    title_text = "Plot Title",
    x_axis_title = "x-axis",
    y_axis_title = "y-axis",
    bgr_fill_color = pero.colors.White.darker(.1),
    plot_fill_color = pero.colors.White)

# show plot
plot.view("Empty Plot")
