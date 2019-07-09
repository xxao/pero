#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from .viewer import QtViewer


def export(graphics, path, width, height, **options):
    """
    Draws given graphics as raster image into specified file. The image format
    is determined from the extension of given file path.
    
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
    
    raise NotImplementedError("No export is currently implemented for Qt.")


def show(graphics, title=None, width=750, height=500):
    """
    Shows given graphics in the viewer app.
    
    Args:
        graphics: pero.Graphics
            Graphics to be shown.
        
        title: str or None
            App frame title.
        
        width: float
            App width.
        
        height: float
            App height.
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
    
    # set size
    window.set_size((width, height))
    
    # set graphics
    window.set_graphics(graphics)
    
    # draw graphics
    window.refresh()
    
    # start app
    window.show()
    app.exec_()
