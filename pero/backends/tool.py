#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..properties import PropertySet


class Tool(PropertySet):
    """Abstract base class for interactivity tools."""
    
    
    def on_key_down(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-down event.
        
        Args:
            evt: pero.KeyDownEvt
                Event to process.
        """
        
        pass
    
    
    def on_key_up(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-up event.
        
        Args:
            evt: pero.KeyUpEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_leave(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-leave event.
        
        Args:
            evt: pero.MouseLeaveEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_motion(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-motion event.
        
        Args:
            evt: pero.MouseMotionEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_drag(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-drag event.
        
        Args:
            evt: pero.MouseDragEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_scroll(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-scroll event.
        
        Args:
            evt: pero.MouseScrollEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_down(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-button-down event.
        
        Args:
            evt: pero.LeftDownEvt or pero.RightDownEvt or pero.MiddleDownEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_up(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-button-up event.
        
        Args:
            evt: pero.LeftUpEvt or pero.RightUpEvt or pero.MiddleUpEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_dclick(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-button-double-click event.
        
        Args:
            evt: pero.LeftDClickEvt or pero.RightDClickEvt or pero.MiddleDClickEvt
                Event to process.
        """
        
        pass
