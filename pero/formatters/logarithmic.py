#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from ..properties import *
from .formatter import Formatter


class LogFormatter(Formatter):
    """
    This formatter tool uses a logarithm of specified base to format given
    values. For log10 the scientific notation (e.g. 2e6) can be enabled by
    setting the 'sci_notation' property to True. For other logarithms labels can
    be formatted using exponent (e.g. 2^3) by setting the 'exp_notation' property
    to True. Negative values are formatted as positive while keeping the '-' sign
    in the final label.
    
    Properties:
        
        base: int, float
            Specifies the logarithm base to be used.
        
        sci_notation: bool
            Specifies whether the scientific notation (e.g. 2e6) is enabled.
            This only applies if the 'base' is set to 10.
        
        exp_notation: bool
            Specifies whether the exponent notation (e.g. 2^3) should be used.
    """
    
    base = NumProperty(10, dynamic=False)
    sci_notation = BoolProperty(True, dynamic=False)
    exp_notation = BoolProperty(True, dynamic=False)
    
    
    def format(self, value):
        """
        Formats a given value using logarithmic formatting.
        
        Args:
            value: float
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        # check for 0
        if value == 0.0:
            return "0"
        
        # get sign and make vale positive
        sign = -1 if value < 0 else 1
        value = abs(value)
        
        # calc log
        base = self.base if self.base else 10
        log = math.log(value) / math.log(base)
        exp = math.floor(log)
        
        # use scientific notation
        if base == 10 and self.sci_notation:
            return "{:.0e}".format(sign*value)
        
        # use exponent notation
        if self.exp_notation:
            return "{:.0f}^{:.0f}".format(sign*base, exp)
        
        # make template
        if exp < 0:
            template = "{:0.%df}" % abs(exp)
        else:
            template = "{:.0f}"
        
        # apply template
        return template.format(sign*math.pow(base, exp))
