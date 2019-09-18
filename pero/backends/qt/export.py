#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from .enums import *
from .viewer import QtViewer


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as raster image into specified file. The image format
    is determined from the extension of given file path.
    
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
    
    raise NotImplementedError("No export is currently implemented for Qt.")


def show(graphics, title=None, width=None, height=None):
    """
    Shows given graphics in the viewer app.
    
    Args:
        graphics: pero.Graphics
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
