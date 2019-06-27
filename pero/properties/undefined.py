#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


class Undefined(object):
    """Defines an undefined state of a property."""
    
    
    def __str__(self):
        """Returns string representation."""
        
        return "UNDEFINED"
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return self.__str__()
    
    
    def __hash__(self):
        """Defines hash."""
        
        return hash(str(self))
    
    
    def __bool__(self):
        """Defines response for zero-check."""
        
        return False
    
    
    def __eq__(self, other):
        """Defines equality comparer."""
        
        return other is self or other == self.__str__()
    
    
    def __lt__(self, other):
        """Defines lower comparer."""
        
        return other is not self
    
    
    def __le__(self, other):
        """Defines lower or equal comparer."""
        
        return True
    
    
    def __gt__(self, other):
        """Defines greater comparer."""
        
        return False
    
    
    def __ge__(self, other):
        """Defines greater or equal comparer."""
        
        return other is self


# init as singleton
UNDEF = Undefined()
