#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *
from .. formatters import Formatter
from . ticker import Ticker


class FixTicker(Ticker):
    """
    This type of ticker provides user-specified fixed ticks. The label
    'formatter' is by default set to pero.Formatter, but can be changed if
    needed.
    
    Properties:
        
        major_values: tuple
            Specifies the values to be used as the major ticks and labels.
        
        minor_values: tuple
            Specifies the values to be used as the minor ticks.
    """
    
    major_values = TupleProperty((), dynamic=False)
    minor_values = TupleProperty((), dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of FixTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = Formatter()
        
        # init base
        super().__init__(**overrides)
    
    
    def make_ticks(self):
        """
        Generates ticks according to current settings.
        
        Returns:
            (float,), (float,)
                Generated major and minor ticks.
        """
        
        # get range
        start, end = self.start, self.end
        if start > end:
            start, end = end, start
        
        # get ticks in current range
        major_ticks = tuple(x for x in self.major_values if start <= x <= end)
        minor_ticks = tuple(x for x in self.minor_values if start <= x <= end)
        
        return major_ticks, minor_ticks
