#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. colors import Gradient, Transparent
from . interpols import *
from . scale import Scale


class GradientScale(Scale):
    """
    This type of scale tool is used to convert continuous numerical input values
    into color gradient. This is typically used to convert real data units
    defined by 'in_range' property into a color gradient e.g. to plot data
    series. This type of scale does not provide the 'invert' method.
    
    The conversion is done in two steps: normalizing given value within the
    input range and converting the normalized value within the output gradient.
    To provide a specific way of input range normalization, appropriate
    'normalizer' must be specified. There are already some predefined gradient
    scales for convenient use like GradientLinScale, GradientLogScale and
    GradientPowScale.
    
    The output colors should be provided either as a list of colors or palette
    into the 'out_range', from which the gradient is created automatically.
    
    Properties:
        
        in_range: (float, float)
            Specifies the start and end value of the input range.
        
        out_range: pero.Gradient, pero.Palette, (color,), str
            Specifies the output gradient as a sequence of supported pero.Color
            definitions, pero.Palette, pero.Gradient or registered palette or
            gradient name.
        
        normalizer: pero.Interpol
            Specifies the normalization interpolator.
    """
    
    in_range = TupleProperty((), intypes=(int, float), dynamic=False)
    out_range = GradientProperty(UNDEF, dynamic=False)
    
    normalizer = Property(UNDEF, types=(Interpol,), dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of GradientScale."""
        
        # init interpolator
        if 'normalizer' not in overrides:
            overrides['normalizer'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # init gradient
        self._gradient = None
        self._update_gradient()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_gradient_scale_property_changed)
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding output color for given input value.
        
        Args:
            value: float or (float,)
                Input value to be scaled.
        
        Returns:
            pero.Color
                Output color.
        """
        
        # apply array scaling
        if isinstance(value, (numpy.ndarray, list, tuple)):
            return tuple(map(self.scale, value))
        
        # normalize value
        norm = self.normalizer.normalize(value, self.in_range[0], self.in_range[1])
        
        # convert normalized value into color
        return self._gradient.color_at(norm)
    
    
    def _update_gradient(self):
        """Updates gradient by current out_range."""
        
        if self.out_range is UNDEF:
            self._gradient = Gradient((Transparent, Transparent))
        
        else:
            self._gradient = self.out_range.normalized(0, 1)
    
    
    def _on_gradient_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # update gradient
        if evt is None or evt.name == 'out_range':
            self._update_gradient()


class GradientLinScale(GradientScale):
    """Gradient scale with linear transformation."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of GradientLinScale."""
        
        # init normalizer
        overrides['normalizer'] = LinInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock normalizer
        self.lock_property('normalizer')


class GradientLogScale(GradientScale):
    """Gradient scale with logarithmic transformation."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of GradientLogScale."""
        
        # init normalizer
        overrides['normalizer'] = LogInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock normalizer
        self.lock_property('normalizer')


class GradientPowScale(GradientScale):
    """
    Gradient scale with exponential transformation.
    
    Properties:
        
        power: int or float
            Specifies the exponent to be used.
    """
    
    power = FloatProperty(1, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of GradientPowScale."""
        
        # init normalizer
        overrides['normalizer'] = PowInterpol()
        
        # init base
        super().__init__(**overrides)
        
        # lock normalizer
        self.lock_property('normalizer')
        
        # set power
        self.normalizer.power = self.power
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_pow_scale_property_changed)
    
    
    def _on_pow_scale_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # check power
        if evt is None or evt.name == 'power':
            self.normalizer.power = self.power
