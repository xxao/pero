#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from . scale import Scale


class OrdinalScale(Scale):
    """
    This type of scale tool is used to convert discrete values of input into
    predefined discrete values of output (e.g. from category names to colors).
    
    If an unknown input value is to be converted, the next available output
    value can be automatically assigned (and remembered since then) if allowed
    by setting the 'implicit' property to True, otherwise predefined 'default'
    value is returned. Note that if implicit assignment is allowed, newly
    assigned input values are kept within the 'in_range' property, which might
    cause some memory issues because they are never released.
    
    In cases there are more input values than predefined output values, the
    available output values can be recycled by setting the 'recycle' property to
    True. Otherwise predefined 'default' value is returned. This settings makes
    most sense if implicit assignment is allowed. Note that if recycling is
    allowed the 'invert' method in this case returns the first usage of provided
    value.
    
    Properties:
        
        default: any, None or UNDEF
            Specifies the default value.
        
        implicit: bool
            Specifies whether the next available output value should be
            automatically assigned to unknown input value.
        
        recycle: bool
            Specifies whether the output values can be reused if there are no
            free values remaining.
    """
    
    default = Property(UNDEF, dynamic=False, nullable=True)
    implicit = BoolProperty(False, dynamic=False)
    recycle = BoolProperty(False, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of OrdinalScale."""
        
        super().__init__(**overrides)
        
        # init indexes
        self._in_range_idx = None
        self._out_range_idx = None
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_ordinal_scale_property_changed)
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding output value for given input value.
        
        Args:
            value: any or (any,)
                Input value to be scaled.
        
        Returns:
            any
                Scaled value.
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.scale, value))
        
        # check output
        if len(self.out_range) == 0:
            return self.default
        
        # init index map
        if self._in_range_idx is None:
            self._in_range_idx = {}
            
            for i, item in enumerate(self.in_range):
                self._in_range_idx[item] = i
        
        # get index
        idx = self._in_range_idx.get(value, None)
        
        # allow implicit value for unknowns
        if idx is None and self.implicit:
            self.in_range = list(self.in_range) + [value]
            idx = len(self.in_range) - 1
        
        # use default value
        if idx is None:
            return self.default
        
        # check max index and recycle
        if idx >= len(self.out_range):
            if self.recycle:
                idx = idx % len(self.out_range)
            else:
                return self.default
        
        # return output value
        return self.out_range[idx]
    
    
    def invert(self, value, *args, **kwargs):
        """
        Returns corresponding input value for given output value.
        
        Args:
            value: any or (any,)
                Output value to be inverted.
        
        Returns:
            any
                Inverted value.
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.invert, value))
        
        # init index map
        if self._out_range_idx is None:
            self._out_range_idx = {}
            
            for i, item in enumerate(self.out_range):
                self._out_range_idx[item] = i
        
        # get index
        idx = self._out_range_idx.get(value, None)
        
        # check index
        if idx is None or idx >= len(self.in_range):
            return None
        
        # return input value
        return self.in_range[idx]
    
    
    def _on_ordinal_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # check in_range
        if evt is None or evt.name == 'in_range':
            self._in_range_idx = None
            if self.in_range is None or self.in_range is UNDEF:
                self.in_range = ()
        
        # check out_range
        if evt is None or evt.name == 'out_range':
            self._out_range_idx = None
            if self.out_range is None or self.out_range is UNDEF:
                self.out_range = ()
