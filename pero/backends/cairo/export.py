#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os.path
import cairo
import PIL
import numpy
from . enums import *
from . canvas import CairoCanvas


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics into specified image file. The image format is
    determined from the extension of given file path. Supported extensions are
    .bmp, .jpg, .jpeg, .png, .pcx, .pnm, .tif, .tiff, .xpm, .ico, .cur, .svg,
    .pdf and .eps.
    
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
        
        dpi: int
            Image resolution as dots-per-inch.
        
        quality: int
            Image quality in range between 0 and 100 with 0 meaning very poor
            and 100 excellent. This option is only available for JPEG format.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # export as raster image
    if extension in CAIRO_RASTER_TYPES:
        export_raster(graphics, path, width, height, **options)
    
    # export as vector format
    elif extension in CAIRO_VECTOR_TYPES:
        export_vector(graphics, path, width, height, **options)
    
    # unsupported image format
    else:
        message = "Unsupported image format! -> %s" % extension
        raise NotImplementedError(message)


def export_raster(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as raster image into specified file. The image format
    is determined from the extension of given file path. Supported extensions
    are .bmp, .jpg, .jpeg, .png, .pcx, .tif and .tiff.
    
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
        
        dpi: int
            Image resolution as dots-per-inch.
        
        quality: int
            Image quality in range between 0 and 100 with 0 meaning very poor
            and 100 excellent. This option is only available for JPEG format.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # check format
    if extension not in CAIRO_RASTER_TYPES:
        message = "Unsupported image format! -> %s" % extension
        raise NotImplementedError(message)
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # create DC
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    dc = cairo.Context(surface)
    dc.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    
    # init canvas
    canvas = CairoCanvas(dc, width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # convert to PIL image (and convert ARGB to RGBA)
    width, height = surface.get_width(), surface.get_height()
    data = numpy.frombuffer(surface.get_data(), numpy.uint8)
    data.shape = (width, height, 4)
    tmp = numpy.copy(data[:, :, 0])
    data[:, :, 0] = data[:, :, 2]
    data[:, :, 2] = tmp
    image = PIL.Image.frombuffer("RGBA", (width, height), data, 'raw', "RGBA", 0, 1)
    
    # get image options
    params = {
        'dpi': (options.get('dpi', 72), options.get('dpi', 72)),
        'quality': options.get('quality', 95)}
    
    # save to file
    image.save(path, CAIRO_RASTER_TYPES[extension], **params)


def export_vector(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as vector image into specified file. The image format
    is determined from the extension of given file path. Supported extensions
    are .svg, .pdf and .eps.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float or None
            Image width in device units.
        
        height: float or None
            Image height in device units.
        
        line_scale: float
            Line scaling factor.
        
        font_scale: float
            Font scaling factor.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # check format
    if extension not in CAIRO_VECTOR_TYPES:
        message = "Unsupported image format! -> %s" % extension
        raise NotImplementedError(message)
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # create surface
    if extension == '.svg':
        surface = cairo.SVGSurface(path, width, height)
    
    elif extension == '.pdf':
        surface = cairo.PDFSurface(path, width, height)
    
    elif extension == '.eps':
        surface = cairo.PSSurface(path, width, height)
        surface.set_eps(True)
    
    else:
        message = "Unsupported image format! -> %s" % extension
        raise ValueError(message)
    
    # create DC
    dc = cairo.Context(surface)
    dc.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    
    # init canvas
    canvas = CairoCanvas(dc, width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # save to file
    dc.show_page()
