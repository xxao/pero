#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . event import Event


class ViewEvt(Event):
    """
    Abstract base class for various types of view events.
    
    Attributes:
        
        native: any
            Native event fired by the view.
            
        view: pero.View
            The view, which fires the event.
            
        control: pero.Control
            The control which fired the event.
    """
    
    TYPE = EVT_VIEW
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of ViewEvt."""
        
        self.native = None
        self.view = None
        self.control = None
        
        super().__init__(**kwargs)
    
    
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
            control = evt.control)


class SizeEvt(ViewEvt):
    """
    Defines an event which is fired if view size was changed.
    
    Attributes:
        
        width: int or float
            New width of the view.
        
        height: int or float
            New height of the view.
    """
    
    TYPE = EVT_SIZE
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of SizeEvt."""
        
        self.width = None
        self.height = None
        
        super().__init__(**kwargs)


class ZoomEvt(ViewEvt):
    """Defines an event which is fired if axes ranges were changed."""
    
    TYPE = EVT_ZOOM
