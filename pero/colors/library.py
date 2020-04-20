#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


class Library(object):
    """
    Represents a named library of available items used to provide library of
    predefined colors, palettes and gradients. Each added item is registered
    using its original name as well as the lowercase version. 
    """
    
    
    def __init__(self):
        """Initializes a new instance of Library."""
        
        self._items = {}
        self._names = {}


    def __len__(self):
        """Gets number of available colors."""
    
        return len(self._items)


    def __contains__(self, key):
        """Checks whether item exists."""
        
        return key in self._names
    
    
    def __getattr__(self, key):
        """Gets registered item by its name."""
        
        if key in self._names:
            return self._items[self._names[key]]
        
        raise AttributeError(key)
    
    
    def __getitem__(self, key):
        """Gets registered item by its name."""
        
        if key in self._names:
            return self._items[self._names[key]]
        
        raise KeyError(key)
    
    
    def __iter__(self):
        """Gets items iterator."""
        
        return self._items.values().__iter__()
    
    
    def add(self, item):
        """Adds new item."""
        
        self._items[item.name] = item
        self._names[item.name] = item.name
        self._names[item.name.lower()] = item.name
