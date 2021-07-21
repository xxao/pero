#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os.path
import wx
from . enums import *
from . canvas import WXCanvas
from . viewer import WXViewer


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
    
    # init app
    app = WXViewer(0)
    
    # set title
    if title is not None:
        app.set_title(title)
    
    # check size
    if not width:
        width = VIEWER_WIDTH
    if not height:
        height = VIEWER_HEIGHT
    
    # set size
    app.set_size((width, height))
    
    # set graphics
    app.set_content(graphics)
    
    # draw graphics
    app.refresh()
    
    # start app
    app.show()


def export(graphics, path, width=None, height=None, **options):
    """
    Draws given graphics as raster image into specified file. The image format
    is determined from the extension of given file path. Supported extensions
    are .bmp, .jpg, .jpeg, .png, .pcx, .pnm, .tif, .tiff, .xpm, .ico and .cur.
    
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
        
        dpi: int
            Image resolution as dots-per-inch.
        
        quality: int
            Image quality in range between 0 and 100 with 0 meaning very poor
            and 100 excellent. This option is only available for JPEG format.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # check format
    if extension not in WX_RASTER_TYPES:
        message = "Unsupported image format! -> %s" % extension
        raise NotImplementedError(message)
    
    # init simple app if necessary
    try:
        app = wx.App()
    except:
        pass
    
    # check size
    if not width:
        width = EXPORT_WIDTH
    if not height:
        height = EXPORT_HEIGHT
    
    # create DC
    bitmap = wx.Bitmap(width, height)
    dc = wx.MemoryDC()
    dc.SelectObject(bitmap)
    
    # use GCDC
    if 'wxMac' not in wx.PlatformInfo:
        dc = wx.GCDC(dc)
    
    # init canvas
    canvas = WXCanvas(dc, width=width, height=height)
    
    if 'draw_scale' in options:
        canvas.draw_scale = options['draw_scale']
    
    if 'line_scale' in options:
        canvas.line_scale = options['line_scale']
    
    if 'font_scale' in options:
        canvas.font_scale = options['font_scale']
    
    # draw graphics
    graphics.draw(canvas)
    
    # get image
    image = bitmap.ConvertToImage()
    
    # set image options
    if 'dpi' in options:
        image.SetOption(wx.IMAGE_OPTION_RESOLUTIONUNIT, str(wx.IMAGE_RESOLUTION_INCHES))
        image.SetOption(wx.IMAGE_OPTION_RESOLUTION, str(options['dpi']))
    
    if 'quality' in options:
        image.SetOption(wx.IMAGE_OPTION_QUALITY, str(options['quality']))
    else:
        image.SetOption(wx.IMAGE_OPTION_QUALITY, '95')
    
    # save to file
    image.SaveFile(path, WX_RASTER_TYPES[extension])
