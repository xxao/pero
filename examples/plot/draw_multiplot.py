#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 100)
sin_data = numpy.sin(x_data)
cos_data = numpy.cos(x_data)
x_data /= numpy.pi

# init plots
plot1 = pero.plot.Plot(x_rangebar=None, y_rangebar=None)
plot1.x_axis.title = "pi"
plot1.y_axis.title = "f(x)"

plot2 = pero.plot.Plot(x_rangebar=None, y_rangebar=None)
plot2.x_axis.title = "pi"
plot2.y_axis.title = "f(x)"

plot3 = pero.plot.Plot(x_rangebar=None, y_rangebar=None)
plot3.x_axis.title = "pi"
plot3.y_axis.title = "f(x)"

# add series
plot1.plot(pero.plot.Profile(x=x_data, y=sin_data), title="sin(x)", color="b")
plot1.plot(pero.plot.Profile(x=x_data, y=cos_data), title="cos(x)", color="g")
plot1.zoom()

plot2.plot(pero.plot.Profile(x=x_data, y=sin_data), title="sin(x)", color="b")
plot2.zoom()

plot3.plot(pero.plot.Profile(x=x_data, y=cos_data), title="cos(x)", color="g")
plot3.zoom()

# make layout
layout = pero.Layout()
layout.add(plot1, 0, 0, col_span=2)
layout.add(plot2, 1, 0)
layout.add(plot3, 1, 1)

layout.show()
