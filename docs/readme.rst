Pero
====

The main motivation behind the *pero* library is to provide unified API for
multiple drawing backends like `wxPython <https://pypi.org/project/wxPython/>`_,
`PyCairo <https://pypi.org/project/pycairo/>`_,
`PyMuPDF <https://pypi.org/project/PyMuPDF/>`_,
`Pythonista <http://omz-software.com/pythonista/>`_ (and
possibly more), which is easy to understand and use. Beside the common drawing
capabilities, numerous pre-build glyphs are available, as well as an easy to use
path, matrix transformations etc. Depending on available backend libraries,
drawings can be viewed directly or exported into various image formats.

Ever since I discovered the wonderful `d3js <https://d3js.org>`_ JavaScript
library, I wanted to have the same amazing concept of dynamic properties within
Python drawings. In fact, this has been the trigger to start working on the
*pero* library.


Requirements:
-------------

- Python 3.6+
- Numpy
- PIL (Pillow)
- [wxPython]
- [Cairo]
- [PyMuPDF 1.14.15+]
- [Pythonista iOS App]


Installation:
-------------

The *pero* library is fully implemented in Python. No additional compiler is
necessary. After downloading the source code just run the following command from
the *pero* folder:

$ python setup.py install

or

$ pip install .


Disclaimer:
-----------

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.


Modules
-------

- `pero.drawing <drawing/readme.rst>`_:

- `pero.colors <colors/readme.rst>`_:

- `pero.formatters <formatters/readme.rst>`_:

- `pero.scales <scales/readme.rst>`_:

- `pero.tickers <tickers/readme.rst>`_:

- `pero.backends <backends/readme.rst>`_:

- `pero.properties <properties/readme.rst>`_:

- `pero.events <events/readme.rst>`_:

- `pero.enums <enums/readme.rst>`_:


Basic Examples:
---------------

Using default backend
~~~~~~~~~~~~~~~~~~~~~

If you just want to draw an image using whatever the default backend is (for
requested format), or show the image directly (requires
`wxPython <https://pypi.org/project/wxPython/>`_ or
`Pythonista <http://omz-software.com/pythonista/>`_), just create an image and
use it as any other *pero* canvas:

.. code:: python

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


Using wxPython
~~~~~~~~~~~~~~

Inside a *wxApp* you can use just about any *wxDC* you want and encapsulate it
into the *pero* canvas:

.. code:: python

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


Using PyCairo
~~~~~~~~~~~~~

Depending on the final image format, choose appropriate *cairo* surface, get the
drawing context and encapsulate it into the *pero* canvas:

.. code:: python

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


Using PyMuPDF
~~~~~~~~~~~~~

Create a document, add new page and encapsulate it into the *pero* canvas:

.. code:: python

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


Using SVG
~~~~~~~~~

The *pero* library implements its own way to draw and save SVG files Just create
a *pero* canvas:

.. code:: python

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


Using Pythonista
~~~~~~~~~~~~~~~~

Initialize a new *ui.ImageContext* and create a *pero* canvas:

.. code:: python

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


Using glyphs and dynamic properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to `d3js <https://d3js.org>`_ JavaScript library, most of the
properties of pre-build *pero.Glyphs* objects can be specified as a function,
to which given data source is automatically provided. Together with *scales*
(and maybe the *pero.Axis)* this can be used to make simple plots easily.

.. code:: python

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

    color_scale = pero.GradientLinScale(
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
        image.draw_graphics(marker, source=p)

    # show image
    image.show()
