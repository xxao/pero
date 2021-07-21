#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . view import ViewEvt


class Touch(object):
    """
    Represents a single touch point.
    
    Attributes:
        
        id: any
            Unique identifier of current touch.
        
        x_pos: int or float
            Logical x-coordinate in device units.
        
        y_pos: int or float
            Logical y-coordinate in device units.
        
        x_prev: int, float or None
            Previous logical x-coordinate in device units.
        
        y_prev: int, float or None
            Previous logical y-coordinate in device units.
        
        force: float
            Touch pressure as a value between 0 and 1.
        
        state: pero.TOUCH
            Specifies current state of the touch as any value from the
            pero.TOUCH enum.
    """
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of Touch."""
        
        self.id = None
        
        self.x_pos = None
        self.y_pos = None
        
        self.x_prev = None
        self.y_prev = None
        
        self.force = None
        self.state = None
        
        # set given arguments
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                raise AttributeError("Attribute not found! --> %s" % name)


class TouchEvt(ViewEvt):
    """
    Defines a generic event which is fired on any touch-related event.
    
    Attributes:
        
        touches: (pero.Touch,)
            Collection of individual touches.
        
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
        
        self.touches = None
        
        self.alt_down = None
        self.cmd_down = None
        self.ctrl_down = None
        self.shift_down = None
        
        super().__init__(**kwargs)
    
    
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
            
            touches = evt.touches,
            
            alt_down = evt.alt_down,
            cmd_down = evt.cmd_down,
            ctrl_down = evt.ctrl_down,
            shift_down = evt.shift_down)


class TouchStartEvt(TouchEvt):
    """Defines an event which is fired if touch starts."""
    
    TYPE = EVT_TOUCH_START


class TouchEndEvt(TouchEvt):
    """Defines an event which is fired if touch ends."""
    
    TYPE = EVT_TOUCH_END


class TouchMoveEvt(TouchEvt):
    """Defines an event which is fired if touch moves."""
    
    TYPE = EVT_TOUCH_MOVE


class TouchCancelEvt(TouchEvt):
    """Defines an event which is fired if touch cancels."""
    
    TYPE = EVT_TOUCH_CANCEL
