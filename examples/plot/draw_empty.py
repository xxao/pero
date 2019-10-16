#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# init plot
plot = pero.plot.Plot()
plot.title.text = "Plot Title"
plot.x_axis.title = "x-axis"
plot.y_axis.title = "y-axis"
plot.bgr_fill_color = pero.colors.White.darker(.1)
plot.plot_fill_color = pero.colors.White

# show plot
plot.view("Empty Plot")
