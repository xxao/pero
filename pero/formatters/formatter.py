#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..properties import *


class Formatter(PropertySet):
    """
    This class mainly provides a base class for all specific formatter. It can
    be also used alone just to convert given value into a string using the
    native implementation of provided values (i.e. __str__ method).
    
    Each formatter has the 'domain' and 'precision' properties, which should be
    set automatically if formatter is used as part of an axis ticker. They can
    be used to prepare formatting according to actual data range and required
    step size.
    
    Sometimes it might be handy to remove specific part from all the labels and
    put it for example at the end of the axis title (e.g. Axis Title [10^5]).
    Such string should then be available by overriding the 'suffix' method.
    
    Properties:
        
        domain: int, float, None or UNDEF
            Specifies the maximum absolute value of current range.
        
        precision: int, float, None or UNDEF
            Specifies the minimum required precision to be kept.
    """
    
    domain = NumProperty(UNDEF, dynamic=False, nullable=True)
    precision = NumProperty(UNDEF, dynamic=False, nullable=True)
    
    
    def format(self, value):
        """
        Formats given value into a string using the native implementation of
        provided value (i.e. __str__ method).
        
        This method should be overridden in derived classes to provide specific
        formatting.
        
        Args:
            value: any
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        return str(value)
    
    
    def suffix(self):
        """
        Gets current suffix (e.g. "10^5" or "kHz").
        
        This method should be overridden in derived classes to provide specific
        logic for creating the suffix.
        
        Returns:
            str
                Labels suffix.
        """
        
        return ""
