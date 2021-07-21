#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. properties import *


class Converter(PropertySet):
    """
    Converter is a simple scale-like tool to convert from one value to another
    by custom forward and reverse functions.
    
    Properties:
        
        forward: callable
            Specifies the function to be used for forward conversion. The
            function is expected to have just one argument for the input value
            and should return converted output.
        
        reverse: callable
            Specifies the function to be used for reverse conversion. The
            function is expected to have just one argument for the input value
            and should return reversed output.
    """
    
    forward = FuncProperty(UNDEF)
    reverse = FuncProperty(UNDEF)
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding converted value for given input value.
        
        Args:
            value: any or (any,)
                Input value to be scaled.
        
        Returns:
            any
                Converted value.
        """
        
        # no function defined
        if self.forward is UNDEF:
            return None
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.forward, value))
        
        # convert
        return self.forward(value)
    
    
    def invert(self, value, *args, **kwargs):
        """
        Returns corresponding reversed value for given output value.
        
        Args:
            value: any or (any,)
                Output value to be inverted.
        
        Returns:
            any
                Reversed value.
        """

        # no function defined
        if self.reverse is UNDEF:
            return None
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.reverse, value))
        
        # convert
        return self.reverse(value)
