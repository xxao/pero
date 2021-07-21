#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from . scale import Scale


class LevelScale(Scale):
    """
    This type of scale tool is used to convert continuous input values into a
    predefined categorical threshold-based output. The input range should
    contain thresholds for each predefined level (maximum value allowed). The
    output range defines the final values representing particular level
    (e.g. color, name etc.).
    
    Properties:
        
        in_range: (float,)
            Specifies the maximum threshold for each level.
        
        out_range: (any,)
            Specifies the output levels values.
    """
    
    in_range = TupleProperty((), intypes=(int, float), dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LevelScale."""
        
        super().__init__(**overrides)
        
        # init index
        self._levels_idx = None
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_levels_scale_property_changed)
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding output level for given input value.
        
        Args:
            value: float or (float,)
                Input value to be converted into level.
        
        Returns:
            any
                Corresponding level.
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.scale, value))
        
        # get index of the same or nearest bigger
        idx = 0
        hi = min(len(self.in_range), len(self.out_range))
        
        while idx < hi:
            mid = (idx + hi) // 2
            if self.in_range[mid] >= value:
                hi = mid
            else:
                idx = mid + 1
        
        # out of range
        if idx >= len(self.out_range):
            return None
        
        # get level
        return self.out_range[idx]
    
    
    def invert(self, value, *args, **kwargs):
        """
        Returns maximum threshold value for given level.
        
        Args:
            value: any or (any,)
                Level value.
        
        Returns:
            float
                Maximum threshold of the level.
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.invert, value))
        
        # init index map
        if self._levels_idx is None:
            self._levels_idx = {}
            
            for i, item in enumerate(self.out_range):
                self._levels_idx[item] = i
        
        # get index
        idx = self._levels_idx.get(value, None)
        
        # check index
        if idx is None or idx >= len(self.in_range):
            return None
        
        # inside
        return self.in_range[idx]
    
    
    def _on_levels_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # check in_range
        if evt is None or evt.name in 'in_range':
            if self.in_range is None or self.in_range is UNDEF:
                self.in_range = ()
        
        # check out_range
        if evt is None or evt.name == 'out_range':
            self._levels_idx = None
            if self.out_range is None or self.out_range is UNDEF:
                self.out_range = ()
