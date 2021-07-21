#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import ui
from .. control import Control
from . enums import *
from . canvas import UICanvas
from . viewer import UIViewer


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
        
        style: str
            Presentation style of the ui.View. Recognized values are:
            fullscreen, sheet, popover and panel. If any touch events are
            expected to work, the fullscreen should be used.
    """
    
    # show as image in console
    if not isinstance(graphics, Control):
        export(graphics, width=width, height=height, **options)
        return
    
    # get style
    style = "fullscreen"
    if 'style' in options:
        style = options['style']
    
    # init main window
    window = UIViewer()
    
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
    window.present(style)


def export(graphics, path=None, width=None, height=None, **options):
    """
    Draws given graphics as raster image into specified file or into Pythonista
    console.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str or None
            Full path of a file to save the image into. If set to None the image
            is displayed in the Pythonista console.
        
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
        
        if 'draw_scale' in options:
            canvas.draw_scale = options['draw_scale']
        
        if 'line_scale' in options:
            canvas.line_scale = options['line_scale']
        
        if 'font_scale' in options:
            canvas.font_scale = options['font_scale']
        
        # draw graphics
        graphics.draw(canvas)
        
        # get image
        img = ctx.get_image()
        
        # save to file
        if path:
            with open(path, 'wb') as f:
                f.write(img.to_png())
        
        # show image
        else:
            img.show()
