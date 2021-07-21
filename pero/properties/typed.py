#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from . undefined import UNDEF
from . prop import Property


class EnumProperty(Property):
    """Defines a generic property allowing predefined set of values only."""
    
    
    def __init__(self, default=UNDEF, enum=(), **kwargs):
        """
        Initializes a new instance of EnumProperty.
        
        Args:
            enum: pero.Enum or (any,)
                Allowed values.
        """
        
        self._enum = set(enum)
        
        kwargs['default'] = default
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check allowed values
        if value in self._enum:
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # cannot convert value
        enums = "|".join(str(x) for x in self._enum)
        message = "Value of '%s' property must be in (%s)! -> %s" % (self.name, enums, value)
        raise TypeError(message)
    
    
    def clone(self, **kwargs):
        """Creates a clone of current property."""
        
        return super().clone(enum=self._enum, **kwargs)


class RangeProperty(Property):
    """Defines a generic property allowing values within specific range only."""
    
    
    def __init__(self, default=UNDEF, minimum=None, maximum=None, minimum_incl=True, maximum_incl=True, **kwargs):
        """
        Initializes a new instance of RangeProperty.
        
        Args:
            minimum: int, float or None
                Minimum allowed value.
            
            maximum: int, float or None
                Maximum allowed value.
            
            minimum_incl: bool
                Specifies whether the minimum value should be included (True)
                or excluded (False) from allowed range.
            
            maximum_incl: bool
                Specifies whether the maximum value should be included (True)
                or excluded (False) from allowed range.
        """
        
        self._minimum = minimum
        self._maximum = maximum
        self._minimum_incl = minimum_incl
        self._maximum_incl = maximum_incl
        
        kwargs['default'] = default
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # check minimum
        if self._minimum is not None:
            
            if not self._minimum_incl and value <= self._minimum:
                message = "Value of '%s' property must be greater than %s! -> %s" % (self.name, self._minimum, value)
                raise ValueError(message)
            
            elif value < self._minimum:
                message = "Value of '%s' property must be greater or equal to %s! -> %s" % (self.name, self._minimum, value)
                raise ValueError(message)
        
        # check maximum
        if self._maximum is not None:
            
            if not self._maximum_incl and value >= self._maximum:
                message = "Value of '%s' property must be smaller than %s! -> %s" % (self.name, self._maximum, value)
                raise ValueError(message)
            
            elif value > self._maximum:
                message = "Value of '%s' property must be smaller or equal to %s! -> %s" % (self.name, self._maximum, value)
                raise ValueError(message)
        
        return value
    
    
    def clone(self, **kwargs):
        """Creates a clone of current property."""
        
        return super().clone(
            minimum = self._minimum,
            maximum = self._maximum,
            minimum_incl = self._minimum_incl,
            maximum_incl = self._maximum_incl,
            **kwargs)


class FuncProperty(Property):
    """Defines a callable property."""
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # allow functions
        if callable(value):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # cannot convert value
        message = "Value of '%s' property must be callable! -> %s" % (self.name, type(value))
        raise TypeError(message)


class BoolProperty(Property):
    """Defines a boolean property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of BoolProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (bool,)
        
        super().__init__(**kwargs)


class IntProperty(Property):
    """Defines an integer property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of IntProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (int,)
        
        super().__init__(**kwargs)


class FloatProperty(Property):
    """Defines a float property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of FloatProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (float,)
        
        super().__init__(**kwargs)


class NumProperty(Property):
    """Defines a numeric property for float and int."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of NumProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (int, float)
        
        super().__init__(**kwargs)


class StringProperty(Property):
    """Defines a string property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of StringProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (str,)
        
        super().__init__(**kwargs)


class IterProperty(Property):
    """Defines a collection property with specified types of inner elements."""
    
    
    def __init__(self, default=UNDEF, intypes=(), **kwargs):
        """
        Initializes a new instance of IterProperty.
        
        Args:
            intypes: (Type,)
                Allowed types for collection elements. If empty, specific inner
                type is not required for inner elements.
        """
        
        # set allowed inner types
        self._intypes = intypes
        
        if isinstance(intypes, list):
            self._intypes = tuple(intypes)
        
        elif not isinstance(intypes, tuple):
            self._intypes = (intypes,)
        
        # init property
        kwargs['default'] = default
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # skip inner type checking
        if not self._intypes:
            return value
        
        # check inner types
        for elm in value:
            if not isinstance(elm, self._intypes):
                intypes = "|".join(x.__name__ for x in self._intypes)
                message = "All elements of the '%s' property must be of type (%s)! -> %s" % (self.name, intypes, type(elm))
                raise TypeError(message)
        
        return value
    
    
    def clone(self, **kwargs):
        """Creates a clone of current property."""
        
        return super().clone(intypes=self._intypes, **kwargs)


class SequenceProperty(IterProperty):
    """Defines a sequence property allowing list, tuple and numpy.ndarray."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of ListProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (list, tuple, numpy.ndarray)
        
        super().__init__(**kwargs)


class ListProperty(IterProperty):
    """Defines a list property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of ListProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (list,)
        
        super().__init__(**kwargs)


class TupleProperty(IterProperty):
    """Defines a tuple property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of TupleProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (tuple,)
        
        super().__init__(**kwargs)


class SetProperty(IterProperty):
    """Defines a set property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of SetProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (set,)
        
        super().__init__(**kwargs)


class DictProperty(Property):
    """Defines a dictionary property."""
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of DictProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (dict,)
        
        super().__init__(**kwargs)


class QuadProperty(Property):
    """
    Defines a property used for quad-sided connected values like margins,
    paddings etc. The value must be provided as a single number or as a list or
    tuple of numbers defining individual values for top, right, bottom and left
    side. If only a single value is provided, it is used for all the sides. If
    two values are provided, the first value is set to top and bottom and the
    second value is set to left and right.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of QuadProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (int, float, tuple, list)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # single value
        if isinstance(value, (int, float)):
            return value, value, value, value
        
        # check type
        if isinstance(value, (list,tuple)) and all(isinstance(x, (int, float)) for x in value):
            
            if len(value) == 1:
                return value[0], value[0], value[0], value[0]
            
            elif len(value) == 2:
                return value[0], value[1], value[0], value[1]
            
            elif len(value) == 4:
                return tuple(value)
        
        # parse main
        value = super().parse(value)
        
        # allow None or UNDEF
        if value is None or value is UNDEF:
            return value
        
        # allow functions
        if callable(value):
            return value
        
        # wrong value
        message = "Value of '%s' property must be a number or list or tuple of 2 or 4 numbers! -> %s" % (self.name, value)
        raise TypeError(message)
