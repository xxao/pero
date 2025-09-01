#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . view import ViewEvt


class DropEvt(ViewEvt):
    """
    Defines an event which is fired if something was dropped.
    
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
    
    TYPE = EVT_DROP
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of DropEvt."""
        
        self.x_pos = None
        self.y_pos = None
        
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
            evt: pero.DropEvt
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


class DropTextEvt(ViewEvt):
    """
    Defines an event which is fired if text was dropped.
    
    Attributes:
        
        text: str
            Dropped text.
    """
    
    TYPE = EVT_DROP_TEXT
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of DropTextEvt."""
        
        self.text = None
        
        super().__init__(**kwargs)


class DropFilesEvt(ViewEvt):
    """
    Defines an event which is fired if files were dropped.
    
    Attributes:
        
        paths: (str,)
            Dropped files paths.
    """
    
    TYPE = EVT_DROP_FILES
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of DropFilesEvt."""
        
        self.paths = None
        
        super().__init__(**kwargs)
