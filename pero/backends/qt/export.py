#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os.path
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtPrintSupport import QPrinter
from . enums import *
from . canvas import QtCanvas
from . viewer import QtViewer


def show(graphics, title=None, width=None, height=None, **options):
    """
    Shows given graphics in the viewer app.
    
    Args:
        graphics: pero.Graphics or pero.Control
            Graphics to be shown.
        
        title: str or None
            Viewer frame title.
        
        width: float or None
            Viewer width in device units.
        
        height: float or None
            Viewer height in device units.
    """
    
    # init app
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])
    
    # init main window
    window = QtViewer()
    
    # set title
    if title is not None:
        window.set_title(title)
    
    # check size
    if not width:
        width = VIEWER_WIDTH
    if not height:
        height = VIEWER_HEIGHT
    
    # set size
    window.set_size((width, height))
    
    # set graphics
    window.set_content(graphics)
    
    # draw graphics
    window.refresh()
    
    # start app
    window.show()
    app.exec_()


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics into specified image file. The image format is
    determined from the extension of given file path. Supported extensions are
    .bmp, .gif, .jpg, .jpeg, .pdf and .png.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float or None
            Image width in device units.
        
        height: float or None
            Image height in device units.
        
        draw_scale: float
            Drawing scaling factor.
        
        line_scale: float
            Line scaling factor.
        
        font_scale: float
            Font scaling factor.
        
        quality: int
            Image quality in range between 0 and 100 with 0 meaning very poor
            and 100 excellent. This option is only available for JPEG format.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # export as raster image
    if extension in QT_RASTER_TYPES:
        export_raster(graphics, path, width, height, **options)
    
    # export as vector format
    elif extension in QT_VECTOR_TYPES:
        export_vector(graphics, path, width, height, **options)
    
    # unsupported image format
    else:
        message = "Unsupported image format! -> %s" % extension
        raise NotImplementedError(message)


def export_raster(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as raster image into specified file. The image format
    is determined from the extension of given file path. Supported extensions
    are .bmp, .gif, .jpg, .jpeg and .png.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float or None
            Image width in device units.
        
        height: float or None
            Image height in device units.
        
        draw_scale: float
            Drawing scaling factor.
        
        line_scale: float
            Line scaling factor.
        
        font_scale: float
            Font scaling factor.
        
        quality: int
            Image quality in range between 0 and 100 with 0 meaning very poor
            and 100 excellent.
    """
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # init app
    app = QApplication([])
    
    # init image
    image = QImage(width, height, QImage.Format_ARGB32)
    
    # init painter
    qp = QPainter()
    qp.begin(image)
    qp.setRenderHint(QPainter.Antialiasing)
    qp.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # init canvas
    canvas = QtCanvas(qp, width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # end drawing
    qp.end()
    
    # get image options
    quality = options.get('quality', -1)
    
    # save to file
    image.save(path, quality=quality)


def export_vector(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as vector image into specified file. The image format
    is determined from the extension of given file path. Supported extension
    is .pdf only.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float or None
            Image width in device units.
        
        height: float or None
            Image height in device units.
        
        draw_scale: float
            Drawing scaling factor.
        
        line_scale: float
            Line scaling factor.
        
        font_scale: float
            Font scaling factor.
    """
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # init app
    app = QApplication([])
    
    # init printer
    printer = QPrinter()
    printer.setPaperSize(QSizeF(width, height), QPrinter.Point)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(path)
    
    # init painter
    qp = QPainter()
    qp.begin(printer)
    qp.setRenderHint(QPainter.Antialiasing)
    qp.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # init canvas
    canvas = QtCanvas(qp, width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # end drawing
    qp.end()
