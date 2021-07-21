#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . view import ViewEvt


class MouseEvt(ViewEvt):
    """
    Defines a generic event which is fired on any mouse-related event.
    
    Attributes:
        
        x_pos: int or float
            Logical x-coordinate in device units.
        
        y_pos: int or float
            Logical y-coordinate in device units.
        
        x_rot: int
            Mouse wheel rotation in x direction.
        
        y_rot: int
            Mouse wheel rotation in y direction.
        
        left_down: bool
            Indicates left mouse button state.
        
        middle_down: bool
            Indicates middle mouse button state.
        
        right_down: bool
            Indicates right mouse button state.
        
        alt_down: bool
            Indicates Alt key state.
        
        cmd_down: bool
            Indicates Command key state.
        
        ctrl_down: bool
            Indicates Control key state.
        
        shift_down: bool
            Indicates Shift key state.
    """
    
    TYPE = EVT_MOUSE
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of MouseEvt."""
        
        self.x_pos = None
        self.y_pos = None
        
        self.x_rot = None
        self.y_rot = None
        
        self.left_down = None
        self.middle_down = None
        self.right_down = None
        
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
            evt: pero.MouseEvt
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
            
            x_rot = evt.x_rot,
            y_rot = evt.y_rot,
            
            left_down = evt.left_down,
            middle_down = evt.middle_down,
            right_down = evt.right_down,
            
            alt_down = evt.alt_down,
            cmd_down = evt.cmd_down,
            ctrl_down = evt.ctrl_down,
            shift_down = evt.shift_down)


class MouseEnterEvt(ViewEvt):
    """Defines an event which is fired if mouse enters window."""
    
    TYPE = EVT_MOUSE_ENTER


class MouseLeaveEvt(ViewEvt):
    """Defines an event which is fired if mouse leaves window."""
    
    TYPE = EVT_MOUSE_LEAVE


class MouseMotionEvt(MouseEvt):
    """Defines an event which is fired if mouse moves."""
    
    TYPE = EVT_MOUSE_MOTION


class MouseScrollEvt(MouseEvt):
    """Defines an event which is fired if mouse wheel rotates."""
    
    TYPE = EVT_MOUSE_SCROLL


class LeftDownEvt(MouseEvt):
    """Defines an event which is fired if left-mouse button is pressed."""
    
    TYPE = EVT_LEFT_DOWN


class LeftUpEvt(MouseEvt):
    """Defines an event which is fired if left-mouse button is released."""
    
    TYPE = EVT_LEFT_UP


class LeftDClickEvt(MouseEvt):
    """Defines an event which is fired if left-mouse button is double-clicked."""
    
    TYPE = EVT_LEFT_DCLICK


class MiddleDownEvt(MouseEvt):
    """Defines an event which is fired if middle-mouse button is pressed."""
    
    TYPE = EVT_MIDDLE_DOWN


class MiddleUpEvt(MouseEvt):
    """Defines an event which is fired if middle-mouse button is released."""
    
    TYPE = EVT_MIDDLE_UP


class MiddleDClickEvt(MouseEvt):
    """Defines an event which is fired if middle-mouse button is double-clicked."""
    
    TYPE = EVT_MIDDLE_DCLICK


class RightDownEvt(MouseEvt):
    """Defines an event which is fired if right-mouse button is pressed."""
    
    TYPE = EVT_RIGHT_DOWN


class RightUpEvt(MouseEvt):
    """Defines an event which is fired if right-mouse button is released."""
    
    TYPE = EVT_RIGHT_UP


class RightDClickEvt(MouseEvt):
    """Defines an event which is fired if right-mouse button is double-clicked."""
    
    TYPE = EVT_RIGHT_DCLICK
