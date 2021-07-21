#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. colors import Color, Palette, Gradient
from . undefined import UNDEF
from . prop import Property


class ColorProperty(Property):
    """
    Defines a color property, which simplifies a color definition by
    automatically creating a pero.Color instance from various input options
    such as an RGB(A) channels (0-255 each), hex string (including leading '#'
    sign) or registered name.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of ColorProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Color, str, tuple, list)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check color
        if isinstance(value, Color):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert to color
        return Color.create(value)


class PaletteProperty(Property):
    """
    Defines a color palette property, which simplifies a palette definition by
    automatically creating a pero.Palette instance from various input options
    such as a list of supported pero.Color definitions or registered palette
    name.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of PaletteProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Palette, str, tuple, list)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check palette
        if isinstance(value, Palette):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert to palette
        return Palette.create(value)


class GradientProperty(Property):
    """
    Defines a color gradient property, which simplifies a gradient definition by
    automatically creating a pero.Gradient instance from various input
    options such as a list of supported pero.Color definitions, pero.Palette
    or registered palette or gradient name.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of GradientProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Gradient, Palette, str, tuple, list)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check gradient
        if isinstance(value, Gradient):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # convert to gradient
        return Gradient.create(value)


class DashProperty(Property):
    """
    Defines a line dash property. The value must be provided as a list or tuple
    of numbers defining the length of lines and spaces in-between.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of DashProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (tuple, list)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check type
        if isinstance(value, (list,tuple)) and all(isinstance(x, (int, float)) for x in value):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # wrong value
        message = "Value of '%s' property must be a list or a tuple of numbers! -> %s" % (self.name, value)
        raise TypeError(message)
