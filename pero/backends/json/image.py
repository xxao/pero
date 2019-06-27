#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ...drawing import Graphics
from .canvas import JsonCanvas


class Image(JsonCanvas, Graphics):
    """
    Image represents a combination of pero.JsonCanvas and pero.Graphics. This
    provides access to all the main drawing methods with a possibility to be
    later drawn into any standard canvas. In addition, two convenient methods
    are available as shortcuts to 'export' or 'show' the image using available
    default drawing backend or viewer, depending on requested format.
    """
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Image."""
        
        super(Image, self).__init__(**overrides)
    
    
    def draw(self, canvas, *args, **kwargs):
        """
        Uses given canvas to draw the image.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
        """
        
        canvas.draw_json(self.get_json())
    
    
    def export(self, path, **options):
        """
        Draws the image into specified file using the format determined
        automatically from the file extension. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Args:
            path: str
                Full path of a file to save the image into.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        from ... import backends
        backends.export(self, path, self.width, self.height, **options)
    
    
    def show(self, title=None):
        """
        Shows the image in available viewer app. Currently this is only
        available if wxPython is installed or within Pythonista app on iOS. This
        method makes sure appropriate backend canvas is created and provided to
        the 'draw' method.
        
        Args:
            title: str or None
                Viewer frame title.
        """
        
        from ... import backends
        backends.show(self, title, self.width, self.height)
    
    
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
        
        return Image().draw_json(dump)
