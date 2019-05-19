#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import ui
from .canvas import UICanvas


def export(graphics, path, width, height, **options):
    """
    Draws given graphics as PNG raster image into specified file.
    
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
    
    # get line scale
    line_scale = 1
    if 'line_scale' in options:
        line_scale = options['line_scale']
    
    # open context
    with ui.ImageContext(width*line_scale, height*line_scale) as ctx:
        
        # init canvas
        canvas = UICanvas(width=width, height=height)
        
        if 'line_scale' in options:
            canvas.line_scale = options['line_scale']
        
        if 'font_scale' in options:
            canvas.font_scale = options['font_scale']
        
        # draw graphics
        graphics.draw(canvas)
        
        # get image
        img = ctx.get_image()
        
        # save to file
        with open(path, 'wb') as f:
            f.write(img.to_png())


def show(graphics, width, height):
    """
    Draws given graphics into Pythonista console.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        width: float
            Image width in device units.
        
        height: float
            Image height in device units.
    """
    
    # open context
    with ui.ImageContext(width, height) as ctx:
        
        # init canvas
        canvas = UICanvas(width=width, height=height)
        
        # draw graphics
        graphics.draw(canvas)
        
        # get image
        img = ctx.get_image()
        
        # show image
        img.show()
