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
*pero* library. Finally, it is all now available.

Until the full documentation is available, please see the *examples* folder or
the in-code documentation of classes and functions to learn more about the
*pero* library capabilities.


.. code:: python
    
    import pero
    
    img = pero.Image(width=400, height=400)
    
    img.line_cap = pero.ROUND
    img.line_join = pero.ROUND

    # fill
    img.fill_color = pero.Color.White
    img.fill()

    # body
    img.line_width = 3
    img.line_color = pero.Color.Orange.darker(.1)
    img.fill_color = pero.Color.Orange
    img.draw_circle(200, 200, 150)
    
    # shadow
    img.line_color = None
    img.fill_color = pero.Color.White.darker(.1)
    img.draw_ellipse(200, 370, 100, 20)
    
    # eyes
    img.fill_color = pero.Color.Black
    img.draw_circle(140, 170, 30)
    img.draw_circle(260, 170, 30)
    
    # eyebrows
    img.line_color = pero.Color.Black
    img.fill_color = None
    img.line_width = 7
    img.draw_arc(140, 170, 45, pero.rads(-100), pero.rads(-20))
    img.draw_arc(260, 170, 45, pero.rads(200), pero.rads(280))
    
    # mouth
    img.line_width = 10
    img.draw_arc(200, 200, 100, pero.rads(40), pero.rads(80))
    
    # highlight
    img.line_color = pero.Color.Orange.lighter(.3)
    img.draw_arc(200, 200, 135, pero.rads(220), pero.rads(260))
    
    # hat
    path = pero.Path(pero.WINDING)
    path.ellipse(200, 55, 80, 20)
    path.ellipse(200, 35, 50, 20)
    path.rect(175, 35, 50, 20)
    
    mat = pero.Matrix().rotate(pero.rads(20), 200, 200)
    path.transform(mat)
    
    img.line_color = None
    img.fill_color = pero.Color.Black
    img.draw_path(path)
    
    img.show()


Requirements:
-------------

- Python 3.6+
- Numpy
- PIL (Pillow)
- [wxPython]
- [Cairo]
- [PyMuPDF]
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

Please note that the *pero* library is still in an alpha state. Any changes in
its API may occur.


Examples:
---------


Using default backend
~~~~~~~~~~~~~~~~~~~~~

If you just want to draw an image using whatever the default backend is (for
requested format), or show the image directly (requires wxPython or Pythonista),
just create an image and use it as any other *pero* canvas:

.. code:: python
    
    # init size
    width = 200
    height = 200
    
    # init image
    image = pero.Image(width=width, height=height)
    
    # draw graphics
    image.line_color = "b"
    image.fill_color = "w"
    image.fill()
    image.draw_circle(100, 100, 75)
    
    # save to file
    image.export('image.png')


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
