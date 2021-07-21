#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import UNDEF, PropertySet, SetProperty


class Tool(PropertySet):
    """Abstract base class for interactivity tools."""
    
    keys = SetProperty(UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Tool."""
        
        super().__init__(**overrides)
        
        # init buffers
        if self.keys == UNDEF:
            self.keys = set()
    
    
    def on_size(self, evt):
        """
        This method should be overridden to provide specific handling
        of window size-change event.
        
        Args:
            evt: pero.SizeEvt
                Event to process.
        """
        
        pass
    
    
    def on_key_down(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-down event.
        
        Args:
            evt: pero.KeyDownEvt
                Event to process.
        """
        
        self.add_key(evt.key)
    
    
    def on_key_up(self, evt):
        """
        This method should be overridden to provide specific handling
        of key-up event.
        
        Args:
            evt: pero.KeyUpEvt
                Event to process.
        """
        
        self.remove_key(evt.key)
    
    
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
        
        self.clear_keys()
    
    
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
            evt: pero.LeftDownEvt, pero.RightDownEvt or pero.MiddleDownEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_up(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-button-up event.
        
        Args:
            evt: pero.LeftUpEvt, pero.RightUpEvt or pero.MiddleUpEvt
                Event to process.
        """
        
        pass
    
    
    def on_mouse_dclick(self, evt):
        """
        This method should be overridden to provide specific handling
        of mouse-button-double-click event.
        
        Args:
            evt: pero.LeftDClickEvt, pero.RightDClickEvt or pero.MiddleDClickEvt
                Event to process.
        """
        
        pass
    
    
    def on_touch_start(self, evt):
        """
        This method should be overridden to provide specific handling
        of touch-start event.
        
        Args:
            evt: pero.TouchStartEvt
                Event to process.
        """
        
        pass
    
    
    def on_touch_end(self, evt):
        """
        This method should be overridden to provide specific handling
        of touch-end event.
        
        Args:
            evt: pero.TouchEndEvt
                Event to process.
        """
        
        pass
    
    
    def on_touch_move(self, evt):
        """
        This method should be overridden to provide specific handling
        of touch-move event.
        
        Args:
            evt: pero.TouchMoveEvt
                Event to process.
        """
        
        pass
    
    
    def on_touch_cancel(self, evt):
        """
        This method should be overridden to provide specific handling
        of touch-cancel event.
        
        Args:
            evt: pero.TouchCancelEvt
                Event to process.
        """
        
        pass
    
    
    def add_key(self, key):
        """
        Remembers given key.
        
        Args:
            key: pero.KEY
                A key to remember as any value from the pero.KEY enum.
        """
        
        self.keys.add(key)
    
    
    def remove_key(self, key):
        """
        Removes given key.
        
        Args:
            key: pero.KEY
                A key to remove as any value from the pero.KEY enum.
        """
        
        self.keys.discard(key)
    
    
    def clear_keys(self):
        """Removes all keys."""
    
        self.keys.clear()
