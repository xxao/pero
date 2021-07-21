#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *
from . formatter import Formatter


class FuncFormatter(Formatter):
    """
    This formatter tool uses custom function to format given values.
    
    Properties:
        
        func: callable
            Specifies a function to be used for custom formatting. The function
            is expected to have just one argument for the input value and
            should return formatted string.
    """
    
    func = FuncProperty(UNDEF)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats given value using custom function.
        
        Args:
            value: any
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        return self.func(value)
