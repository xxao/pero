#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import weakref


class Proxy(object):
    """
    This class encapsulates given callback function to enable weak references
    to instance methods as well as functions.
    """
    
    
    def __init__(self, callback):
        """
        Initializes a new instance of Proxy.
        
        Args:
            callback: callable
                Callback function or method to be encapsulated.
        """
        
        # instance methods
        if hasattr(callback, '__self__'):
            self.obj = weakref.ref(callback.__self__)
            self.func = weakref.ref(callback.__func__)
        
        # direct function
        else:
            self.obj = None
            self.func = weakref.ref(callback)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "Proxy(%s)" % self.callback
    
    
    def __call__(self, *args, **kwargs):
        """Calls defined callback."""
        
        self.callback(*args, **kwargs)
    
    
    def __eq__(self, other):
        """Compares two proxies for equality."""
        
        if not isinstance(other, Proxy):
            other = Proxy(other)
        
        if self.obj is other.obj:
            return self.func is other.func
        
        if self.obj is None or other.obj is None:
            return False
        
        return self.obj() is other.obj() and self.func() is other.func()
    
    
    def __ne__(self, other):
        """Compares two proxies for non-equality."""
        
        return not self.__eq__(other)
    
    
    @property
    def callback(self):
        """Gets the callback."""
        
        # direct function
        if self.obj is None:
            return self.func()
        
        # instance method
        obj = self.obj()
        if obj is not None:
            return getattr(obj, self.func().__name__)
