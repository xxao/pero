#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . view import ViewEvt


class KeyEvt(ViewEvt):
    """
    Defines a generic event which is fired on any key-related event.
    
    Attributes:
        
        key: int
            Unicode key.
        
        char: str or None
            Character string or None if not character.
        
        pressed: bool
            Indicates the key pressed state.
        
        alt_down: bool
            Indicates Alt key state.
        
        cmd_down: bool
            Indicates Command key state.
        
        ctrl_down: bool
            Indicates Control key state.
        
        shift_down: bool
            Indicates Shift key state.
    """
    
    TYPE = EVT_KEY
    
    def __init__(self, **kwargs):
        """Initializes a new instance of KeyEvt."""
        
        self.key = None
        self.char = None
        self.pressed = None
        
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
            evt: pero.KeyEvt
                Source event from which to copy the data.
        
        Returns:
            cls instance
                New instance of requested class.
        """
        
        return cls(
            
            native = evt.native,
            view = evt.view,
            control = evt.control,
            
            key = evt.key,
            char = evt.char,
            pressed = evt.pressed,
            
            alt_down = evt.alt_down,
            cmd_down = evt.cmd_down,
            ctrl_down = evt.ctrl_down,
            shift_down = evt.shift_down)


class KeyDownEvt(KeyEvt):
    """Defines an event which is fired if a key is pressed."""
    
    TYPE = EVT_KEY_DOWN


class KeyUpEvt(KeyEvt):
    """Defines an event which is fired if a key is released."""
    
    TYPE = EVT_KEY_UP
