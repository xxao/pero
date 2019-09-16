#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..properties import UNDEF, PropertySet, SetProperty


class Tool(PropertySet):
    """Abstract base class for interactivity tools."""
    
    keys = SetProperty(UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Tool."""
        
        super(Tool, self).__init__(**overrides)
        
        # init buffers
        if self.keys == UNDEF:
            self.keys = set()
    
    
    def on_key_down(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-down event.
        
        Args:
            evt: pero.KeyDownEvt
                Event to process.
        """
        
        # remember key
        self.keys.add(evt.key)
    
    
    def on_key_up(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-up event.
        
        Args:
            evt: pero.KeyUpEvt
                Event to process.
        """
        
        # remove key
        self.keys.discard(evt.key)
    
    
    def on_mouse_enter(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-enter event.
        
        Args:
            evt: pero.MouseEnterEvt
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
        
        # clear keys
        self.keys = set()
    
    
    def on_mouse_motion(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-motion event.
        
        Args:
            evt: pero.MouseMotionEvt
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
