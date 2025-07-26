#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . enums import *
from . sketch import ShowSketch, ExportSketch


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
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # init sketch
    sketch = ShowSketch(graphics, title, width, height, **options)
    
    # show sketch
    sketch.run_sketch()


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
    
    # init sketch
    sketch = ExportSketch(graphics, path, width, height, **options)
    
    # draw and save to file
    sketch.run_sketch()
