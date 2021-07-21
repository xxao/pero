#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import fitz
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
    """
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # init document
    doc = fitz.open()
    page = doc.newPage(width=width, height=height)
    
    # init canvas
    canvas = MuPDFCanvas(page)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # save to file
    doc.save(path)
    doc.close()
