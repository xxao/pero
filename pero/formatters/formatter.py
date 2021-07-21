#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *


class Formatter(PropertySet):
    """
    This class mainly serves as a base class for all specific formatters. It can
    be also used alone just to convert given value into a string using the
    native implementation of provided value type (i.e. __str__ method).
    
    Each formatter has the 'domain' and 'precision' properties. They are used to
    prepare formatting according to actual data range and required precision
    (e.g. axis step size). If the formatter is used as part of an axis ticker,
    these properties are set automatically.
    
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
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats given value into a string using the native implementation of
        provided value type (i.e. __str__ method).
        
        This method should be overridden in derived classes to provide specific
        formatting mechanism.
        
        Args:
            value: any
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        return str(value)
    
    
    def suffix(self, *args, **kwargs):
        """
        Gets current suffix (e.g. "10^5" or "kHz").
        
        This method should be overridden in derived classes to provide specific
        logic for creating the suffix.
        
        Returns:
            str
                Labels suffix.
        """
        
        return ""
