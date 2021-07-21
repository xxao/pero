#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from . interpols import *
from . scale import Scale


class ContinuousScale(Scale):
    """
    This type of scale tool is used to convert continuous numerical input values
    into continuous numerical output. This is typically used to convert real
    data units defined by 'in_range' property into device output units such as
    pixels defined by 'out_range' e.g. to draw plot axes and data series.
    
    The conversion is done in two steps: normalizing given value within the
    input range and converting the normalized value within the output range. For
    such functionality the scale contains a set of two interpolators. One is
    used for normalization 'normalizer' and the other for final conversion
    'converter'.
    
    To make a specific scale it is mostly sufficient to create an instance of
    ContinuousScale and set the 'normalizer' and/or 'converter' to provide
    specific conversion. There are already some predefined scales for convenient
    use like pero.LinScale, pero.LogScale and pero.PowScale.
    
    For the input values outside specified range the clipping can be applied by
    setting the 'clip' property to True. Otherwise such values will be
    extrapolated.
    
    To convert more data efficiently, the scale can convert not only a single
    value but whole sequence such as list or numpy.array at once. For custom
    scale be sure this functionality is supported by both interpolators.
    
    Properties:
        
        in_range: (float, float)
            Specifies the start and end value of the input range.
        
        out_range: (float, float)
            Specifies the start and end value of the output range.
        
        normalizer: pero.Interpol
            Specifies the normalization interpolator.
        
        converter: pero.Interpol
            Specifies the conversion interpolator.
        
        clip: bool
            Specifies whether the values outside current input range should be
            clipped (True) or interpolated (False).
    """
    
    in_range = TupleProperty((), intypes=(int, float), dynamic=False)
    out_range = TupleProperty((), intypes=(int, float), dynamic=False)
    
    normalizer = Property(UNDEF, types=(Interpol,), dynamic=False)
    converter = Property(UNDEF, types=(Interpol,), dynamic=False)
    clip = BoolProperty(False, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of ContinuousScale."""
        
        # init interpolators
        if 'normalizer' not in overrides:
            overrides['normalizer'] = LinInterpol()
        
        if 'converter' not in overrides:
            overrides['converter'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # init indexes
        self._in_min = 0
        self._in_max = 1
        self._out_min = 0
        self._out_max = 1
        
        # update indexes
        self._on_continuous_scale_property_changed()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_continuous_scale_property_changed)
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding output value for given input value.
        
        Args:
            value: int, float, (int,), (float,)
                Input value(s) to be scaled as a single number or a sequence of
                numbers.
        
        Returns:
            int, float or numpy.ndarray
                Scaled value(s).
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return self._scale_array(value)
        
        # clip values outside
        if self.clip:
            
            if value <= self.in_range[self._in_min]:
                return self.out_range[self._in_min]
            
            if value >= self.in_range[self._in_max]:
                return self.out_range[self._in_max]
        
        # normalize value
        norm = self.normalizer.normalize(value, self.in_range[0], self.in_range[1])
        
        # convert normalized value
        return self.converter.denormalize(norm, self.out_range[0], self.out_range[1])
    
    
    def invert(self, value, *args, **kwargs):
        """
        Returns corresponding input value for given output value.
        
        Args:
            value: int, float, (int,), (float,)
                Output value(s) to be inverted as a single number or a sequence
                of numbers.
        
        Returns:
            int, float or numpy.ndarray
                Inverted value(s).
        """
        
        # apply array inverting
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return self._invert_array(value)
        
        # clip values outside
        if self.clip:
            
            if value <= self.out_range[self._out_min]:
                return self.in_range[self._out_min]
            
            if value >= self.out_range[self._out_max]:
                return self.in_range[self._out_max]
        
        # normalize value
        norm = self.converter.normalize(value, self.out_range[0], self.out_range[1])
        
        # convert normalized value
        return self.normalizer.denormalize(norm, self.in_range[0], self.in_range[1])
    
    
    def normalize(self, value, *args, **kwargs):
        """
        Returns normalized value (in range 0 to 1) for given input value.
        
        Args:
            value: int, float, (int,), (float,)
                Input value(s) to be normalized as a single number or a sequence
                of numbers.
        
        Returns:
            int, float or numpy.ndarray
                Normalized value(s).
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return self._normalize_array(value)
        
        # clip values outside
        if self.clip:
            
            if value <= self.in_range[self._in_min]:
                return float(self._in_min)
            
            if value >= self.in_range[self._in_max]:
                return float(self._in_max)
        
        # normalize value
        return self.normalizer.normalize(value, self.in_range[0], self.in_range[1])
    
    
    def _scale_array(self, value):
        """Returns corresponding output array for given input array."""
        
        # check array
        if not isinstance(value, numpy.ndarray):
            value = numpy.array(value)
        
        # clip values
        if self.clip:
            numpy.clip(value, self.in_range[self._in_min], self.in_range[self._in_max], out=value)
        
        # normalize values
        norm = self.normalizer.normalize(value, self.in_range[0], self.in_range[1])
        
        # convert normalized values
        denorm = self.converter.denormalize(norm, self.out_range[0], self.out_range[1])
        
        return denorm
    
    
    def _invert_array(self, value):
        """Returns corresponding input array for given output array."""
        
        # check array
        if not isinstance(value, numpy.ndarray):
            value = numpy.array(value)
        
        # clip values
        if self.clip:
            numpy.clip(value, self.out_range[self._out_min], self.out_range[self._out_max], out=value)
        
        # normalize values
        norm = self.converter.normalize(value, self.out_range[0], self.out_range[1])
        
        # convert normalized values
        denorm = self.normalizer.denormalize(norm, self.in_range[0], self.in_range[1])
        
        return denorm
    
    
    def _normalize_array(self, value):
        """Returns corresponding normalized array for given input array."""
        
        # check array
        if not isinstance(value, numpy.ndarray):
            value = numpy.array(value)
        
        # normalize values
        norm = self.normalizer.normalize(value, self.in_range[0], self.in_range[1])
        
        # clip values
        if self.clip:
            numpy.clip(norm, 0., 1., out=norm)
        
        return norm
    
    
    def _on_continuous_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # check in_range
        if evt is None or evt.name in 'in_range':
            self._in_min = 0
            self._in_max = 1
            if self.in_range and self.in_range[0] > self.in_range[1]:
                self._in_min = 1
                self._in_max = 0
        
        # check out_range
        if evt is None or evt.name == 'out_range':
            self._out_min = 0
            self._out_max = 1
            if self.out_range and self.out_range[0] > self.out_range[1]:
                self._out_min = 1
                self._out_max = 0


class LinScale(ContinuousScale):
    """Continuous scale with linear transformation."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LinScale."""
        
        # init interpolators
        overrides['normalizer'] = LinInterpol()
        overrides['converter'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock interpolators
        self.lock_property('normalizer')
        self.lock_property('converter')


class LogScale(ContinuousScale):
    """Continuous scale with logarithmic transformation."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LogScale."""
        
        # init interpolators
        overrides['normalizer'] = LogInterpol()
        overrides['converter'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock interpolators
        self.lock_property('normalizer')
        self.lock_property('converter')


class PowScale(ContinuousScale):
    """
    Continuous scale with exponential transformation.
    
    Properties:
        
        power: int or float
            Specifies the exponent to be used.
    """
    
    power = FloatProperty(1, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of PowScale."""
        
        # init interpolators
        overrides['normalizer'] = PowInterpol()
        overrides['converter'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock interpolators
        self.lock_property('normalizer')
        self.lock_property('converter')
        
        # set power
        self.normalizer.power = self.power
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_pow_scale_property_changed)
    
    
    def _on_pow_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # check power
        if evt is None or evt.name == 'power':
            self.normalizer.power = self.power
