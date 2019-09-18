#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import ui
from .enums import *
from .canvas import UICanvas


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as PNG raster image into specified file.
    
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
    
    # get line scale
    line_scale = 1
    if 'line_scale' in options:
        line_scale = options['line_scale']
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
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


def show(graphics, title=None, width=None, height=None):
    """
    Draws given graphics into Pythonista console.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        title: str or None
            Viewer frame title.
        
        width: float or None
            Viewer width in device units.
        
        height: float or None
            Viewer height in device units.
    """
    
    # check size
    if not width:
        width = VIEWER_WIDTH
    if not height:
        height = VIEWER_HEIGHT
    
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
