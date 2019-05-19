#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..enums import *
from .event import Event


class ViewEvt(Event):
    """
    Abstract base class for various types of view events.
    
    Attributes:
        
        native: any
            Native event fired by the view.
            
        view: pero.View
            The view, which fires the event.
            
        graphics: pero.Graphics
            The view main graphics.
    """
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of ViewEvt."""
        
        self.native = None
        self.view = None
        self.graphics = None
        
        super(ViewEvt, self).__init__(**kwargs)
    
    
    @classmethod
    def from_evt(cls, evt):
        """
        Initializes a new instance of given class by copying all data.
        
        Args:
            evt: pero.ViewEvt
                Source event from which to copy the data.
        
        Returns:
            cls instance
                New instance of requested class.
        """
        
        return cls(
            native = evt.native,
            view = evt.view,
            graphics = evt.graphics)


class PositionEvt(ViewEvt):
    """
    Abstract base class for various types of position events.
    
    Attributes:
        
        x: int or float
            Logical x-coordinate (with current line scale applied).
        
        y: int or float
            Logical y-coordinate (with current line scale applied).
        
        raw_x: int or float
            Device units x-coordinate.
        
        raw_y: int or float
            Device units y-coordinate.
    """
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of SizeEvt."""
        
        self.x = None
        self.y = None
        self.raw_x = None
        self.raw_y = None
        
        super(PositionEvt, self).__init__(**kwargs)
    
    
    @classmethod
    def from_evt(cls, evt):
        """
        Initializes a new instance of given class by copying all data.
        
        Args:
            evt: pero.PositionEvt
                Source event from which to copy the data.
        
        Returns:
            cls instance
                New instance of requested class.
        """
        
        return cls(
            native = evt.native,
            view = evt.view,
            graphics = evt.graphics,
            
            x = evt.x,
            y = evt.y,
            raw_x = evt.raw_x,
            raw_y = evt.raw_y)


class SizeEvt(ViewEvt):
    """
    Defines an event which is fired if view size was changed.
    
    Attributes:
        width: int or float
            New width of the view.
        
        height: int or float
            New height of the view.
    """
    
    TYPE = EVENT.SIZE
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of SizeEvt."""
        
        self.width = None
        self.height = None
        
        super(SizeEvt, self).__init__(**kwargs)
