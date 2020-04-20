#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


class Enum(object):
    """
    Defines a generic enum type, where values are provided as key:value pairs.
    The key can be used to access the value like from dict (e.g. enum[key]) or
    as property (e.g. enum.key). Each value must be unique.
    
    Note that unlike the normal dict, the Enum __contains__ method is not
    checking for keys but for values.
    """
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of Enum."""
        
        # get named values
        self._map = kwargs
        
        # get all values
        values = list(kwargs.values())
        self._values = set(values)
        
        # check values
        if len(values) != len(self._values):
            message = "Enum values are not unique! -> %s" % ", ".join(str(v) for v in values)
            raise AttributeError(message)
    
    
    def __contains__(self, value):
        """Checks whether value exists."""
        
        return value in self._values
    
    
    def __getattr__(self, name):
        """Gets value by its name."""
        
        if name in self._map:
            return self._map[name]
        
        raise AttributeError(name)
    
    
    def __getitem__(self, name):
        """Gets value by its name."""
        
        if name in self._map:
            return self._map[name]
        
        raise KeyError(name)
    
    
    def __iter__(self):
        """Gets values iterator."""
        
        return self._values.__iter__()
