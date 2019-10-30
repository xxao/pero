#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import *
from .view import ViewEvt


class TouchEvt(ViewEvt):
    """
    Defines a generic event which is fired on any touch-related event.
    
    Attributes:
        
        x_pos: int or float
            Logical x-coordinate in device units.
        
        y_pos: int or float
            Logical y-coordinate in device units.
        
        alt_down: bool
            Indicates Alt key state.
        
        cmd_down: bool
            Indicates Command key state.
        
        ctrl_down: bool
            Indicates Control key state.
        
        shift_down: bool
            Indicates Shift key state.
    """
    
    TYPE = EVT_TOUCH
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of MouseEvt."""
        
        self.x_pos = None
        self.y_pos = None
        
        self.alt_down = None
        self.cmd_down = None
        self.ctrl_down = None
        self.shift_down = None
        
        super(TouchEvt, self).__init__(**kwargs)
    
    
    @classmethod
    def from_evt(cls, evt):
        """
        Initializes a new instance of given class by copying all data.
        
        Args:
            evt: pero.TouchEvt
                Source event from which to copy the data.
        
        Returns:
            cls instance
                New instance of requested class.
        """
        
        return cls(
            
            native = evt.native,
            view = evt.view,
            control = evt.control,
            
            x_pos = evt.x_pos,
            y_pos = evt.y_pos,
            
            alt_down = evt.alt_down,
            cmd_down = evt.cmd_down,
            ctrl_down = evt.ctrl_down,
            shift_down = evt.shift_down)


class TouchStartEvt(ViewEvt):
    """Defines an event which is fired if touch starts."""
    
    TYPE = EVT_TOUCH_START


class TouchEndEvt(ViewEvt):
    """Defines an event which is fired if touch ends."""
    
    TYPE = EVT_TOUCH_END


class TouchMoveEvt(ViewEvt):
    """Defines an event which is fired if touch moves."""
    
    TYPE = EVT_TOUCH_MOVE


class TouchCancelEvt(ViewEvt):
    """Defines an event which is fired if touch cancels."""
    
    TYPE = EVT_TOUCH_CANCEL
