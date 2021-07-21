#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. events import PropertyChangedEvt
from . undefined import UNDEF


class Property(object):
    """
    Defines a generic property used in all pero.PropertySet classes. The main
    purpose is to provide reasonable default value and possibility to allow
    certain types or values only. Specific derived implementations can be
    created to provide custom value checking and parsing by overwriting the
    'parse' and 'clone' methods.
    
    If allowed by the 'dynamic' attribute the actual value can be a function or
    method, which is expected to give the final value from provided data source.
    This allows properties to be dynamic and provide specific values based on
    actual data.
    
    Attributes:
        
        name: str, (read-only)
            Property name.
        
        default: any
            Default value.
        
        types: (Type,) (read-only)
            Specifies the allowed types for values. If empty, specific type is
            not required for values.
        
        dynamic: bool (read-only)
            Specifies whether the property can be defined as dynamic i.e. the
            actual value of the property is a function, which is expected to
            give the final value from provided data source. 
        
        nullable: bool (read-only)
            Specifies whether the property value can be set to None.
    """
    
    
    def __init__(self, default=UNDEF, types=(), dynamic=True, nullable=False, name=None):
        """
        Initializes a new instance of Property.
        
        Args:
            default: any
                Default value.
            
            types: (Type,)
                Specifies allowed types for values. If empty, specific type is
                not required for values.
            
            dynamic: bool
                Specifies whether the property can be defined as dynamic i.e.
                the actual value of the property is a function, which is
                expected to give the final value from provided data source.
            
            nullable: bool
                Specifies whether the property value can be set to None.
            
            name: str
                Property name.
        """
        
        self._name = name
        self._types = types
        self._dynamic = bool(dynamic)
        self._nullable = bool(nullable)
        
        # check types
        if isinstance(types, list):
            self._types = tuple(types)
        
        elif not isinstance(types, tuple):
            self._types = (types,)
        
        # set default value
        self._default = self.parse(default)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "%s(%s:%s)" % (self.__class__.__name__, self._name, self._default)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return self.__str__()
    
    
    def __get__(self, obj, objtype=None):
        """
        Depending on the context, this method returns either the property value
        or the property itself.
        
        If the 'obj' is set to an instance of pero.PropertySet, actual
        property value is returned. If such property is not yet set in the obj
        instance, the default value is returned and set to the instance as
        well.
        
        If the 'obj' is None but 'objtype' is set, the property itself is
        returned.
        """
        
        # get instance value
        if obj is not None:
            
            # check name
            name = self._name
            if not name:
                raise RuntimeError('The property name is not set!')
            
            # get known value
            if name in obj.__dict__:
                return obj.__dict__[name]
            
            # initialize by default value
            else:
                new_value = self._default
                obj.__dict__[name] = new_value
                return new_value
        
        # get property itself
        if objtype is not None:
            return self
        
        message = "Cannot get the '%s' property!" % self._name
        raise ValueError(message)
    
    
    def __set__(self, obj, value):
        """
        Depending on the context, this method parses and sets given value to
        the instance or changes the default value of the property.
        
        If the 'obj' is set to an instance of PropertySet, given value is set to
        the instance. If the value is different than the one previously set,
        the pero.EVT_PROPERTY_CHANGED event is fired with current property
        name and the old and the new values.
        
        If the 'obj' is None given value is set as default value of the property
        itself.
        """
        
        # parse value
        new_value = self.parse(value)
        
        # set instance value
        if obj is not None:
            
            # check name
            name = self._name
            if not name:
                raise RuntimeError('The property name is not set!')
            
            # check lock
            if obj.is_property_locked(name):
                message = "The property '%s' is locked and cannot be changed!" % name
                raise AttributeError(message)
            
            # check undefinable
            if value is UNDEF and obj.is_property_held(name):
                return
            
            # get old value
            if name in obj.__dict__:
                old_value = obj.__dict__[name]
            else:
                old_value = self.parse(self._default)
                obj.__dict__[name] = old_value
            
            # compare values
            if type(old_value) != type(new_value):
                replace = True
            elif isinstance(old_value, numpy.ndarray):
                replace = not numpy.array_equal(old_value, new_value)
            else:
                replace = old_value != new_value
            
            # set new value and raise changed event
            if replace:
                obj.__dict__[name] = new_value
                obj.fire(PropertyChangedEvt(name=name, old_value=old_value, new_value=new_value))
        
        # set class default
        else:
            self._default = new_value
    
    
    @property
    def name(self):
        """
        Gets property name.
        
        Returns:
            str
                Property name.
        """
        
        return self._name or self.__class__.name
    
    
    @property
    def types(self):
        """
        Gets allowed types.
        
        Returns:
            (Type,)
                Allowed types.
        """
        
        return self._types
    
    
    @property
    def dynamic(self):
        """
        Gets the value indicating whether the property can be dynamic.
        
        Returns:
            bool
                True if the property can be dynamic, False otherwise.
        """
        
        return self._dynamic
    
    
    @property
    def nullable(self):
        """
        Gets the value indicating whether the property value can be set to None.
        
        Returns:
            bool
                True if the property can be set to None, False otherwise.
        """
        
        return self._nullable
    
    
    @property
    def default(self):
        """
        Gets default value.
        
        Returns:
            any
                Default value.
        """
        
        return self._default
    
    
    @default.setter
    def default(self, value):
        """
        Sets default value.
        
        Args:
            value: any
                Default value to be set.
        """
        
        self._default = self.parse(value)
    
    
    def parse(self, value):
        """
        Validates and converts given value.
        
        Args:
            value: any
                Value to be parsed.
        
        Returns:
            any
                Parsed value.
        """
        
        # check allowed types
        if self._types and isinstance(value, self._types):
            return value
        
        # check nullable
        if not self._nullable and value is None:
            message = "Value of the '%s' property cannot be None!" % self.name
            raise ValueError(message)
        
        # check dynamic
        if not self._dynamic and callable(value):
            message = "Value of the '%s' property cannot be dynamic!" % self.name
            raise ValueError(message)
        
        # allow None, UNDEF, dynamic or untyped
        if value is None or value is UNDEF or callable(value) or not self._types:
            return value
        
        # try to convert into single defined type
        if len(self._types) == 1:
            try: return self._types[0](value)
            except: pass
        
        # cannot convert value
        types = "|".join(x.__name__ for x in self._types)
        message = "Value of the '%s' property must be of type (%s)! -> %s" % (self.name, types, type(value))
        raise TypeError(message)
    
    
    def clone(self, **kwargs):
        """
        Creates a clone of current property. Note that any custom property,
        which defines its own attributes should overwrite this method and
        provide its own attributes as keyword arguments to this base method.
        
        Args:
            kwargs: {key:value,}
                Arguments to overwrite in the clone.
        
        Returns:
            pero.Property
                Cloned property.
        """
        
        if 'name' not in kwargs:
            kwargs['name'] = self.name
        
        if 'default' not in kwargs:
            kwargs['default'] = self.default
        
        if 'types' not in kwargs:
            kwargs['types'] = self.types
        
        if 'dynamic' not in kwargs:
            kwargs['dynamic'] = self.dynamic
        
        if 'nullable' not in kwargs:
            kwargs['nullable'] = self.nullable
        
        return self.__class__(**kwargs)
