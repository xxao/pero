#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os.path
from .. enums import *


def show(graphics, title=None, width=None, height=None, backend=None, **options):
    """
    Shows given graphics in available viewer app. Currently this is only
    available if wxPython or PyQt5 is installed or within Pythonista app on iOS.
    This method makes sure appropriate backend canvas is created and provided to
    graphics 'draw' method.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        title: str or None
            Viewer frame title.
        
        width: float or None
            Viewer width in device units.
        
        height: float or None
            Viewer height in device units.
        
        backend: pero.BACKEND
            Specific backend to be used. The value must be an item from the
            pero.BACKEND enum.
        
        options: str:any pairs
            Additional parameters for specific backend.
    """
    
    # get backends
    backends = VIEWER_PRIORITY if backend is None else [backend]
    
    # get backend
    backend = None
    for module in backends:
        
        # try to import backend
        try:
            if module == BACKEND_PYTHONISTA:
                from . import pythonista as backend
            
            elif module == BACKEND_QT:
                from . import qt as backend
            
            elif module == BACKEND_WX:
                from . import wx as backend
            
            break
        
        # ignore missing library
        except ImportError:
            backend = None
            pass
    
    # no viewer available
    if backend is None:
        message = "No viewer available or missing library (e.g. wxPython, PyQt5 or Pythonista)!"
        raise ImportError(message)
    
    # show viewer
    backend.show(graphics, title, width, height, **options)


def export(graphics, path, width=None, height=None, backend=None, **options):
    """
    Draws given graphics into specified image file using the format determined
    automatically from the file extension. This method makes sure appropriate
    backend canvas is created and provided to graphics 'draw' method.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float or None
            Image width in device units.
        
        height: float or None
            Image height in device units.
        
        backend: pero.BACKEND
            Specific backend to be used. The value must be an item from the
            pero.BACKEND enum.
        
        options: str:any pairs
            Additional parameters for specific backend.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # get backends
    backends = EXPORT_PRIORITY if backend is None else [backend]
    
    # import backend
    backend = None
    for module in backends:
        
        # check if format is recognized by backend
        if extension not in EXPORT_FORMATS[module]:
            continue
        
        # try to import backend
        try:
            if module == BACKEND_CAIRO:
                from . import cairo as backend
            
            elif module == BACKEND_JSON:
                from . import json as backend
            
            elif module == BACKEND_MUPDF:
                from . import mupdf as backend
            
            elif module == BACKEND_PYTHONISTA:
                from . import pythonista as backend
            
            elif module == BACKEND_QT:
                from . import qt as backend
            
            elif module == BACKEND_SVG:
                from . import svg as backend
            
            elif module == BACKEND_WX:
                from . import wx as backend
            
            break
        
        # ignore missing library
        except ImportError:
            backend = None
            pass
    
    # unsupported format
    if backend is None:
        message = "Unsupported image format or missing library (e.g. wxPython, PyCairo, PyQt)! -> %s" % extension
        raise ImportError(message)
    
    # export image
    backend.export(graphics, path, width, height, **options)


def debug(graphics, canvas='show', title="", width=None, height=None, backend=None, **options):
    """
    Renders given graphics using simple viewer or file format. This method makes
    sure appropriate backend canvas is created and provided to graphics 'draw'
    method. In case of the image export the file is stored in current working
    directory using 'test' and appropriate format as the name.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        canvas: str
            Specifies drawing mechanism to be used. This can be either 'show',
            'wx', 'qt' or 'pythonista' to display graphics within a simple
            viewer app, or any of the supported image formats (e.g. 'png',
            'svg') to draw to 'test.?' file.
        
        title: str or None
            Viewer frame title.
        
        width: float or None
            Image or viewer width in device units.
        
        height: float or None
            Image or viewer height in device units.
        
        backend: pero.BACKEND
            Specific backend to be used. The value must be an item from the
            pero.BACKEND enum.
        
        options: key:value pairs
            Additional parameters for specific backend.
    """
    
    # render graphics in available viewer
    if canvas == 'show':
        show(graphics, title, width, height, backend, **options)
    
    # render graphics into qt viewer
    elif canvas == 'qt':
        from . import qt
        qt.show(graphics, title, width, height, **options)
    
    # render graphics into wx viewer
    elif canvas == 'wx':
        from . import wx
        wx.show(graphics, title, width, height, **options)
    
    # render graphics into Pythonista console
    elif canvas == 'pythonista':
        from . import pythonista
        pythonista.show(graphics, width, height, **options)
    
    # render graphics as image file
    else:
        filename = "test.%s" % canvas
        export(graphics, filename, width, height, backend, **options)
