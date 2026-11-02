#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os
import pymupdf
from . enums import *
from . canvas import MuPDFCanvas


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as PDF document into specified file.
    
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
    """
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # init document
    doc = pymupdf.open()
    page = doc.new_page(width=width, height=height)
    
    # init canvas
    canvas = MuPDFCanvas(page, snap=False)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # save to PDF file
    if extension == '.pdf':
        doc.save(path)
    
    # save to SVG
    elif extension == '.svg':
        svg_content = page.get_svg_image()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
    
    # save to raster
    elif extension in ('.png', '.jpg', '.jpeg'):
        pix = page.get_pixmap(dpi=options.get('dpi', 72))
        pix.save(path)
    
    # close document
    doc.close()
