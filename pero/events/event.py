#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


class Event(object):
    """
    Abstract base class for various types of events. Each derived event class
    has to specify its unique TYPE property at least.
    """
    
    TYPE = None
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of Event."""
        
        self._canceled = False
        
        # set given arguments
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                raise AttributeError("Attribute not found! --> %s" % name)
    
    
    def cancel(self):
        """
        Sets current event as canceled to prevent following subscribers to be
        called.
        """
        
        self._canceled = True
    
    
    def resume(self):
        """
        Sets current event as not canceled to allow following subscribers to be
        called.
        """
        
        self._canceled = False
    
    
    def is_canceled(self):
        """
        Gets the value indicating if the event has been canceled.
        
        Returns:
            bool
                Canceled flag.
        """
        
        return self._canceled
