#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ... enums import *
from . canvas import JsonCanvas


def export(graphics, path, width=None, height=None, **options):
    """
    Saves given graphics as JSON dump into specified file.
    
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
    
    # init canvas
    canvas = JsonCanvas(width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # save to file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(canvas.get_json())
