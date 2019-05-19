#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..properties import *


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
        
        super(Graphics, self).__init__(**overrides)
        
        # init default tag
        if self.tag is UNDEF:
            self.tag = "tag_%s" % str(id(self))
    
    
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
