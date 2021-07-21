#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from . event import Event


class PropertyChangedEvt(Event):
    """
    Defines an event which is fired if any property of a pero.PropertySet
    was changed.
    
    Attributes:
        
        name: str
            Name of the changed property.
        
        old_value: any
            Original value.
        
        new_value: any
            New value.
    """
    
    TYPE = EVT_PROPERTY_CHANGED
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of PropertyChangedEvt."""
        
        self.name = None
        self.old_value = None
        self.new_value = None
        
        super().__init__(**kwargs)
    
    
    @classmethod
    def from_evt(cls, evt):
        """
        Initializes a new instance of given class by copying all current data.
        
        Args:
            evt: pero.PropertyChangedEvt
                Source event from which to copy the data.
        
        Returns:
            cls instance
                New instance of requested class.
        """
        
        return cls(
            name = evt.name,
            old_value = evt.old_value,
            new_value = evt.new_value)
