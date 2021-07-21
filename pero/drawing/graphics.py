#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *


class Graphics(PropertySet):
    """
    Abstract base class for all graphical objects.
    
    Properties:
        
        tag: str, callable, None or UNDEF
            Specifies the unique tag of the object. If not provided on a class
            initialization it is set automatically using object id. The value is
            often used as id when drawn to SVG or as object identifier in
            complex graphics like charts.
        
        visible: bool, callable
            Specifies whether the object should be drawn or skipped.
        
        z_index: int, float or UNDEF
            Specifies the object z-index. The value may be used to provide
            specific order for objects drawing in complex graphics like charts.
            Bigger the value is, more on top the graphics should be drawn. Any
            specific use of this must be implemented by a user to draw graphics
            in desired order.
    """
    
    tag = StringProperty(UNDEF, nullable=True)
    visible = BoolProperty(True)
    z_index = NumProperty(UNDEF)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Graphics."""
        
        super().__init__(**overrides)
        
        # init default tag
        if self.tag is UNDEF:
            self.tag = "tag_%s" % str(id(self))
    
    
    def show(self, title=None, width=None, height=None, backend=None, **options):
        """
        Shows current graphics in available viewer app. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the graphics is already part of any UI app.
        
        Args:
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
        
        # try get size
        if width is None and self.has_property('width'):
            width = self.get_property('width')
        if height is None and self.has_property('height'):
            height = self.get_property('height')
        
        from .. import backends
        backends.show(self, title, width, height, backend, **options)
    
    
    def export(self, path, width=None, height=None, backend=None, **options):
        """
        Draws current graphics into specified image file using the format
        determined automatically from the file extension. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the graphics is already part of any UI app.
        
        Args:
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
        
        # try get size
        if width is None and self.has_property('width'):
            width = self.get_property('width')
        if height is None and self.has_property('height'):
            height = self.get_property('height')
        
        from .. import backends
        backends.export(self, path, width, height, backend, **options)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """
        Uses given canvas to draw the graphics.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        """
        
        raise NotImplementedError("The 'draw' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_many(self, canvas, source, **overrides):
        """
        Uses given canvas to draw the graphics for each item in given source.
        In fact this is just a convenient shortcut to call the 'draw' method in
        a loop.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
            
            source: (any,)
                Collection of data source items to be used for calculating
                callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        """
        
        # check source
        if source is None or source is UNDEF:
            return
        
        # draw items
        for item in source:
            self.draw(canvas, item, **overrides)
    
    
    def is_visible(self, source=UNDEF, overrides=None):
        """
        Returns True if current graphics is visible.
        
        Args:
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: dict
                Specific properties to be overwritten.
        
        Returns:
            bool
                Returns True if current graphics is visible.
        """
        
        return self.get_property('visible', source, overrides)
