#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .canvas import SVGCanvas


def export(graphics, path, width, height, **options):
    """
    Draws given graphics as SVG vector image into specified file.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float
            Image width in device units.
        
        height: float
            Image height in device units.
        
        line_scale: float
            Line scaling factor.
        
        font_scale: float
            Font scaling factor.
    """
    
    # init canvas
    canvas = SVGCanvas(width=width, height=height)
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # save to file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(canvas.get_xml())
