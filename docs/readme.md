# Pero

The main motivation behind the *pero* library is to provide unified API for multiple drawing backends like
[PyQt5](https://pypi.org/project/PyQt5/), [wxPython](https://pypi.org/project/wxPython/),
[PyCairo](https://pypi.org/project/pycairo/), [PyMuPDF](https://pypi.org/project/PyMuPDF/),
[Pythonista](http://omz-software.com/pythonista/) (and possibly more), which is easy to understand and use. Beside the
common drawing capabilities, numerous pre-build glyphs are available, as well as an easy to use path, matrix
transformations etc. Depending on available backend libraries, drawings can be viewed directly or exported into various
image formats.

Ever since I discovered the wonderful [d3js](https://d3js.org>) JavaScript library, I wanted to have the same amazing
concept of dynamic properties within Python drawings. In fact, this has been the trigger to start working on the *pero*
library.


## Requirements

- [Python 3.6+](https://www.python.org)
- [Numpy](https://pypi.org/project/numpy/)
- [PIL (Pillow)](https://pypi.org/project/Pillow/)
- \[[PyQt5](https://pypi.org/project/PyQt5/)\]
- \[[wxPython](https://pypi.org/project/wxPython/)\]
- \[[PyCairo](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo)\]
- \[[PyMuPDF](https://pypi.org/project/PyMuPDF/)\]
- \[[Pythonista iOS App](http://omz-software.com/pythonista/)\]


## Installation

The *pero* library is fully implemented in Python. No additional compiler is necessary. After downloading the source
code just run the following command from the *pero* folder:

```$ python setup.py install```

or

```$ pip install .```


## Disclaimer

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.


## Modules

### [pero.drawing](drawing/readme.md)

Although the actual drawing is always done by particular backend, the main benefit of the *pero* library is its unified
drawing experience (or API), which is independent of any backend. To draw simple shapes or texts, several methods are
available for each backend's canvas implementation. For more complex drawings a path, Bezier curves and transformation
matrix can be used. Beside the main functionality, the *[pero.drawing](drawing/readme.md)* module provides a hand full
of predefined glyphs and graphics, starting from simple markers, arrows or grids and going up to more complex graphics
such as graph axes.

### [pero.colors](colors/readme.md)

One of the key element of any drawing is, of course, a color. Inside the *pero* library, colors are defined by their
RGB(A) channels using dedicated class. Additional classes are available to define and use color pallets and gradients.
Many standard colors and palettes are available and can be easily accessed by corresponding name from the
*[pero.colors](colors/readme.md)* module.

### [pero.backends](backends/readme.md)

As already mentioned, the actual drawing is done by various backends, for which the *pero* library provides consistent
API. This is achieved by specific implementations of a canvas base class, which translates the API into methods and
logic of particular backend. As of now, the *pero* library supports [PyQt5](https://pypi.org/project/PyQt5/), 
[wxPython](https://pypi.org/project/wxPython/), [PyCairo](https://pypi.org/project/pycairo/),
[PyMuPDF](https://pypi.org/project/PyMuPDF/), [Pythonista](http://omz-software.com/pythonista/) app and its own
implementation of SVG and JSON canvas.

### [pero.scales](scales/readme.md)

In prototyping or research activities, some real data often need to be mapped to screen coordinates, specific color or
simply from one dimension to another in general. This is the place where the *[pero.scales](scales/readme.md)* module
provides lots of convenient tools. Together with the dynamic nature of glyphs properties this makes creation of graphics
like plots or gauge bars much easier.

### [pero.tickers](tickers/readme.md)

For drawing graphics like plots or gauge bars it is essential to provide easy to read labels and ticks. To make this
task a bit less boring the *[pero.tickers](tickers/readme.md)* module provides several classes to help generate
reasonable values for given range and scale such as linear, logarithmic or time scale.

### [pero.formatters](formatters/readme.md)

For any graphics containing lots of text labels, the *[pero.formatters](formatters/readme.md)* module provides various
ways to conveniently format values into specific form. This can be as simple as providing templates for the
`string.format()`, custom functions or fully automatic way of formatting numbers according to specified range and
required precision.

### [pero.properties](properties/readme.md)

The core of most of the classes within the *pero* library is a specific implementation of properties and their
collections. This allows to specify properties not only by a final value but dynamically, i.e. as a function to retrieve
the final value from given data source. In addition, it allows for type checking or internal conversion from multiple
definition styles (e.g. for colors).

### [pero.events](events/readme.md)

Each time a property of *pero* graphics is changed an event is raised and can be used to act accordingly. The
*[pero.events](events/readme.md)* module, provides a general implementation of event handling mechanism and can
be used to create custom "smart" objects or interactive graphics.

### [pero.enums](enums/readme.md)

There are several constants used throughout the *pero* library to define angle units, various text properties, line and
fill properties, shortcuts to create predefined glyphs or to position objects relative to each other. These constants
are all defined in the *[pero.enums](enums/readme.md)* module.


## Basic Examples

### Using default backend

If you just want to draw an image using whatever the default backend is (for requested format), or show the image
directly (requires [wxPython](https://pypi.org/project/wxPython/) or [Pythonista](http://omz-software.com/pythonista/)),
just create an image and use it as any other *pero* canvas:

```python

import pero

# init size
width = 200
height = 200

# init image
img = pero.Image(width=width, height=height)

# draw graphics
img.line_color = "b"
img.fill_color = "w"
img.fill()
img.draw_circle(100, 100, 75)

# save to file
img.export('image.png')

# show in viewer
img.show()
```


### Using PyQt5

Inside a *QWidget* you can create a *QPainter* and encapsulate it into the *pero* canvas:

```python

import pero
from PyQt5.QtGui import QPainter

# init size
width = 200
height = 200

# init painter
qp = QPainter()
qp.begin(self)
qp.setRenderHint(QPainter.Antialiasing)

# init canvas
canvas = pero.qt.QtCanvas(qp)

# draw graphics
canvas.line_color = "b"
canvas.fill_color = "w"
canvas.fill()
canvas.draw_circle(100, 100, 75)

# end drawing
qp.end()
```


### Using wxPython

Inside a *wxApp* you can use just about any *wxDC* you want and encapsulate it into the *pero* canvas:

```python

import pero
import wx

# init size
width = 200
height = 200

# create DC
bitmap = wx.Bitmap(width, height)
dc = wx.MemoryDC()
dc.SelectObject(bitmap)

# use GCDC
if 'wxMac' not in wx.PlatformInfo:
    dc = wx.GCDC(dc)

# init canvas
canvas = pero.wx.WXCanvas(dc, width=width, height=height)

# draw graphics
canvas.line_color = "b"
canvas.fill_color = "w"
canvas.fill()
canvas.draw_circle(100, 100, 75)
```

### Using PyCairo

Depending on the final image format, choose appropriate *cairo* surface, get the drawing context and encapsulate it into
the *pero* canvas:

```python

import pero
import cairo

# init size
width = 200
height = 200

# create cairo drawing context
surface = cairo.PSSurface('image.eps', width, height)
dc = cairo.Context(surface)

# init canvas
canvas = pero.cairo.CairoCanvas(dc, width=width, height=height)

# draw graphics
canvas.line_color = "b"
canvas.fill_color = "w"
canvas.fill()
canvas.draw_circle(100, 100, 75)

# save to file
dc.show_page()
```

### Using PyMuPDF

Create a document, add new page and encapsulate it into the *pero* canvas:

```python

import pero
import fitz

# init size
width = 200
height = 200

# init document
doc = fitz.open()
page = doc.newPage(width=width, height=height)

# init canvas
canvas = pero.mupdf.MuPDFCanvas(page)

# draw graphics
canvas.line_color = "b"
canvas.fill_color = "w"
canvas.fill()
canvas.draw_circle(100, 100, 75)

# save to file
doc.save('image.pdf')
doc.close()
```

### Using SVG

The *pero* library implements its own way to draw and save SVG files Just create
a *pero* canvas:

```python

import pero

# init size
width = 200
height = 200

# init canvas
canvas = pero.svg.SVGCanvas(width=width, height=height)

# draw graphics
canvas.line_color = "b"
canvas.fill_color = "w"
canvas.fill()
canvas.draw_circle(100, 100, 75)

# save to file
with open('test.svg', 'w', encoding='utf-8') as f:
    f.write(canvas.get_xml())
```

### Using Pythonista

Initialize a new *ui.ImageContext* and create a *pero* canvas:

```python

import pero
import ui

# init size
width = 200
height = 200

# open context
with ui.ImageContext(width, height) as ctx:

    # init canvas
    canvas = pero.pythonista.UICanvas(width=width, height=height)

    # draw graphics
    canvas.line_color = "b"
    canvas.fill_color = "w"
    canvas.fill()
    canvas.draw_circle(100, 100, 75)

    # show image
    img = ctx.get_image()
    img.show()
```

### Using glyphs and dynamic properties

Similar to [d3js](https://d3js.org) JavaScript library, most of the
properties of pre-build *pero.Glyphs* objects can be specified as a function,
to which given data source is automatically provided. Together with *scales*
(and maybe the *pero.Axis)* this can be used to make simple plots easily.

```python

import pero
import numpy

# init size
width = 400
height = 300
padding = 50

# init data
x_data = numpy.linspace(-numpy.pi, numpy.pi, 50)
y_data = numpy.sin(x_data)

# init scales
x_scale = pero.LinScale(
    in_range = (min(x_data), max(x_data)),
    out_range = (padding, width-padding))

y_scale = pero.LinScale(
    in_range = (-1, 1),
    out_range = (height-padding, padding))

color_scale = pero.GradientScale(
    in_range = (-1, 1),
    out_range = pero.colors.Spectral)

# init marker
marker = pero.Circle(
    size = 8,
    x = lambda d: x_scale.scale(d[0]),
    y = lambda d: y_scale.scale(d[1]),
    line_color = lambda d: color_scale.scale(d[1]).darker(.2),
    fill_color = lambda d: color_scale.scale(d[1]))

# init image
image = pero.Image(width=width, height=height)

# fill
image.fill_color = pero.colors.White
image.fill()

# draw points
for p in zip(x_data, y_data):
    marker.draw(image, source=p)

# show image
image.show()
```