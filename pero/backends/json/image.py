#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ... drawing import Graphics
from . canvas import JsonCanvas


class Image(JsonCanvas, Graphics):
    """
    Image represents a combination of pero.JsonCanvas and pero.Graphics. This
    provides access to all the main drawing methods with a possibility to be
    later drawn into any standard canvas. In addition, two convenient methods
    are available as shortcuts to 'export' or 'show' the image using available
    default drawing backend or viewer, depending on requested format.
    """
    
    
    def show(self, title=None, width=None, height=None, backend=None, **options):
        """
        Shows the image in available viewer app. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the image is already part of any UI app.
        
        Args:
            title: str or None
                Viewer frame title.
            
            width: float or None
                Viewer width in device units. If set to None, current image
                width is used.
            
            height: float or None
                Viewer height in device units. If set to None, current image
                height is used.
            
            backend: pero.BACKEND
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # show image
        super().show(title, width, height, backend, **options)
    
    
    def export(self, path, width=None, height=None, backend=None, **options):
        """
        Draws the image into specified file using the format determined
        automatically from the file extension. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the image is already part of any UI app.
        
        Args:
            path: str
                Full path of a file to save the image into.
            
            width: float or None
                Image width in device units. If set to None, current image width
                is used.
            
            height: float or None
                Image height in device units. If set to None, current image
                height is used.
            
            backend: pero.BACKEND
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # export image
        super().export(path, width, height, backend, **options)
    
    
    def draw(self, canvas, *args, **kwargs):
        """
        Uses given canvas to draw the image.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
        """
        
        canvas.draw_json(self.get_json())
    
    
    @staticmethod
    def from_json(dump):
        """
        Creates a new pero.Image from given JSON dump.
        
        Args:
            dump: str or dict
                Image JSON dump.
        
        Returns:
            pero.Image
        """
        
        img = Image()
        img.draw_json(dump)
        
        return img
    
    
    @staticmethod
    def load_json(path):
        """
        Creates a new pero.Image from given JSON dump path.
        
        Args:
            path: str or dict
                Path to JSON dump.
        
        Returns:
            pero.Image
        """
        
        with open(path) as dump:
            return Image.from_json(dump.read())
