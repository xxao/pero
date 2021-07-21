#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import inspect
from .. events import EvtHandler
from . undefined import UNDEF
from . prop import Property

# define property names splitter
PROP_SPLITTER = '_'

# init properties cache
_PROPERTIES_CACHE = {}


class Include(object):
    """
    This class is used as a tool to include all available properties of another
    property set. The properties can be included with optional prefix, which is
    added then to the name of each included property, and custom defaults
    provided as overrides. In addition the 'dynamic' and 'nullable' flags can
    also be changed for all the included property.
    """
    
    
    def __init__(self, prop_set, prefix="", dynamic=None, nullable=None, exclude=None, **overrides):
        """
        Initializes a new instance of Include.
        
        Args:
            prop_set: pero.PropertySet class
                Property set class from which to include all the properties.
            
            prefix: str
                Optional prefix to be added to the names of all included
                properties. If prefix does not end with '_' it is added
                automatically. Such pattern is required to retrieve child
                properties etc.
            
            dynamic: bool or None
                If set to True or False the value overwrites the original value
                of the all included properties.
            
            nullable: bool or None
                If set to True or False the value overwrites the original value
                of the all included properties.
            
            exclude: (str,)
                Names of the properties to ignore. Original names without the
                prefix must be used.
            
            overrides: str:any pairs
                Overwrites for default values of specific properties. Original
                names without the prefix must be used.
        """
        
        # check type
        if not issubclass(prop_set, PropertySet):
            message = "Properties must be subclass of pero.PropertySet! -> %s" % type(prop_set)
            raise TypeError(message)
        
        # check prefix
        if prefix and prefix[-1] != PROP_SPLITTER:
            prefix = prefix + PROP_SPLITTER
        
        # set values
        self._property_set = prop_set
        self._prefix = prefix
        self._dynamic = dynamic
        self._nullable = nullable
        self._exclude = set(exclude) if exclude else set()
        self._overrides = overrides
    
    
    def make_properties(self):
        """
        Creates clones of all properties to be included and adjusts each name
        by provided prefix.
        
        Returns:
            (pero.Property,)
                List of initialized properties.
        """
        
        properties = []
        
        # clone properties
        for prop in self._property_set.properties():
            
            # skip if excluded
            if prop.name in self._exclude:
                continue
            
            # get name
            name = prop.name
            if self._prefix:
                name = self._prefix + name
            
            # get default
            default = prop.default
            if prop.name in self._overrides:
                default = self._overrides[prop.name]
            
            # get dynamic
            dynamic = prop.dynamic
            if self._dynamic is not None:
                dynamic = self._dynamic
            
            # get nullable
            nullable = prop.nullable
            if self._nullable is not None:
                nullable = self._nullable
            
            # add cloned property
            properties.append(prop.clone(
                name = name,
                default = default,
                dynamic = dynamic,
                nullable = nullable))
        
        return properties


class PropertySetMeta(type):
    """Defines a meta class for pero.PropertySet classes."""
    
    
    def __new__(cls, cls_name, bases, cls_dict):
        """Creates a new parent class."""
        
        # finalize properties
        for name, item in tuple(cls_dict.items()):
            
            # set property name
            if isinstance(item, Property):
                item._name = name
            
            # insert properties from Includes
            elif isinstance(item, Include):
                
                # remove include itself
                del cls_dict[name]
                
                # insert contained properties
                for prop in item.make_properties():
                    if prop.name in cls_dict:
                        message = "Property with the name '%s' is already present!" % prop.name
                        raise KeyError(message)
                    cls_dict[prop.name] = prop
        
        # init new class
        return type.__new__(cls, cls_name, bases, cls_dict)


class PropertySet(EvtHandler, metaclass=PropertySetMeta):
    """
    Abstract base class for all property-having classes.
    
    This class also serves as an event handler, which means it can fire events
    using the 'fire' method and specific listeners can be attached to it. By
    default only the pero.EVT_PROPERTY_CHANGED is fired every time a
    property is changed.
    """
    
    
    def __init__(self, **overrides):
        """
        Initializes a new instance of PropertySet.
        
        Args:
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        super().__init__()
        
        # get available properties
        self._properties = {p.name: p for p in self.properties()}
        self._locked = set()
        self._held = set()
        
        # set given properties
        self.set_properties(overrides, True)
    
    
    def __call__(self, **overrides):
        """
        Updates specified properties.
        
        Args:
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # set given properties
        self.set_properties(overrides, True)
    
    
    def has_property(self, name):
        """
        Checks whether specified property exists.
        
        Args:
            name: str
                Name of the property.
        
        Returns:
            bool
                True if the property exists, False otherwise.
        """
        
        return name in self._properties
    
    
    def get_property(self, name, source=UNDEF, overrides=None, native=False):
        """
        Gets the value of specified property.
        
        If specified property is available within 'overrides' the value in
        'overrides' is used instead of current one. If allowed and the value is
        callable but still not of the requested type, given 'source' is provided
        as the argument for calling it and returned value is finally used.
        
        In some cases it might be useful to retrieve the callable function
        itself, without applying it onto given source. This can be achieved by
        setting the 'native' argument to True.
        
        Args:
            name: str
                Name of the property to be retrieved.
            
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current value.
            
            native: bool
                If set to True callable properties are returned directly
                without calling and using the source.
        
        Returns:
            any
                Property value.
        """
        
        # get property
        prop = self._properties[name]
        
        # use native value
        if native:
            if overrides and name in overrides:
                return overrides[name]
            
            return getattr(self, name)
        
        # use overrides
        if overrides and name in overrides:
            value = prop.parse(overrides[name])
        
        # get property value
        else:
            value = getattr(self, name)
        
        # requested type
        if isinstance(value, prop.types):
            return value
        
        # dynamic property
        if callable(value):
            value = value(source)
        
        # parse value
        return prop.parse(value)
    
    
    def get_own_overrides(self, overrides):
        """
        Extracts the overrides for direct properties of current property set.
        
        Args:
            overrides: dict or None
                Overrides to extract the properties from.
        
        Returns:
            dict
                Extracted self overrides as {name: value}.
        """
        
        # check overrides
        if overrides is None:
            return {}
        
        # init own overrides
        own_overrides = {}
        
        # get own overrides
        for name in overrides:
            if name in self._properties:
                own_overrides[name] = overrides[name]
        
        return own_overrides
    
    
    def get_child_overrides(self, child_name, overrides):
        """
        Extracts the overrides for child property set. A property is considered
        as child-related if it starts with specified 'child_name' followed by
        '_' and it is not a direct property of current property set.
        
        Args:
            child_name: str
                Name of the child property set.
            
            overrides: dict or None
                Overrides to extract the properties from.
        
        Returns:
            dict
                Extracted child overrides as {name: value}.
        """
        
        # check overrides
        if overrides is None:
            return {}
        
        # get prefix
        prefix = child_name + PROP_SPLITTER
        
        # init child overrides
        child_overrides = {}
        
        # get child overrides
        for name in overrides:
            
            # skip current
            if name in self._properties:
                continue
            
            # skip without prefix
            if not name.startswith(prefix) or name == prefix:
                continue
            
            # add override
            new_name = name.split(prefix, 1)[1] 
            child_overrides[new_name] = overrides[name]
        
        return child_overrides
    
    
    def set_property(self, name, value, raise_error=True):
        """
        Sets given value for specified property.
        
        In some cases it might be useful to initialize also some properties of
        a child property set directly along the current one. Therefore, if the
        property name is not found within current property set its name is split
        by '_' and it tries to search for a property matching the left
        side of the split. If such property is found in current property set,
        then the right part of the split is used to set the child property. E.g.
        if current set has a property 'marker', its line properties can be set
        directly as 'marker_line_color'. However, this mechanism assumes the
        child property to be also derived from pero.PropertySet and it must be
        initialized already.
        
        Args:
            name: str
                Name of the property to be set.
            
            value: any
                Property value to be set.
            
            raise_error: bool
                If set to True, an error is raised if unknown property is about
                to be set.
        """
        
        # set known property
        if name in self._properties:
            setattr(self, name, value)
            return
        
        # try child properties
        else:
            
            idx = name.find(PROP_SPLITTER)
            while idx > 0:
                
                parent = name[:idx]
                if parent in self._properties:
                    prop = getattr(self, parent)
                    if isinstance(prop, PropertySet):
                        prop.set_property(name[idx+1:], value, raise_error)
                        return
                
                idx = name.find(PROP_SPLITTER, idx+1)
        
        # raise error for unknown property
        if raise_error:
            message = "%s has no property '%s'!" % (self.__class__.__name__, name)
            raise AttributeError(message)
    
    
    def set_properties(self, properties, raise_error=True):
        """
        Sets multiple properties in a batch using name:value dictionary.
        
        In some cases it might be useful to initialize also some properties of
        a child property set directly along the current one. Therefore, if the
        property name is not found within current property set its name is split
        by '_' and it tries to search for a property matching the left
        side of the split. If such property is found in current property set,
        then the right part of the split is used to set the child property. E.g.
        if current set has a property 'marker', its line properties can be set
        directly as 'marker_line_color'. However, this mechanism assumes the
        child property to be also derived from pero.PropertySet and it must be
        initialized already.
        
        Args:
            properties: dict
                Properties names and values to be set.
            
            raise_error: bool
                If set to True, an error is raised if unknown property is about
                to be set.
        """
        
        for name, value in sorted(properties.items()):
            self.set_property(name, value, raise_error)
    
    
    def set_properties_from(self, prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, ignore=None, native=False):
        """
        Sets values of all shared properties from given property set to current
        property set.
        
        If any property is available within 'overrides' the value in
        'overrides' is used instead of current one. If allowed and the value is
        callable but still not of the requested type, given 'source' is provided
        as argument for calling it and returned value is finally used.
        
        In some cases it might be useful to retrieve the callable function
        itself, without applying it onto given source. This can be achieved by
        setting the 'native' argument to True.
        
        Args:
            prop_set: pero.PropertySet
                Property set from which to retrieve the properties.
            
            src_prefix: str
                Prefix used for shared properties in the source set. Shared
                properties without this prefix will be skipped.
            
            dst_prefix: str
                Prefix used for shared properties in the destination set. Shared
                properties without this prefix will be skipped.
            
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current values.
                The names should include the 'src_prefix'.
            
            ignore: (str,)
                Collection of properties to be ignored. The names should include
                the 'src_prefix'.
            
            native: bool
                If set to True callable properties from the source are used
                directly without calling.
        """
        
        # check prefixes
        if src_prefix and src_prefix[-1] != PROP_SPLITTER:
            src_prefix = src_prefix + PROP_SPLITTER
        
        if dst_prefix and dst_prefix[-1] != PROP_SPLITTER:
            dst_prefix = dst_prefix + PROP_SPLITTER
        
        # process source properties
        for prop in prop_set.properties():
            
            # get source name without prefix
            name = prop.name
            if src_prefix and name.startswith(src_prefix):
                name = name[len(src_prefix):]
            elif src_prefix:
                continue
            
            # finalize names
            src_name = prop.name
            dst_name = dst_prefix + name
            
            # skip properties
            if ignore and src_name in ignore:
                continue
            
            # set shared properties
            if dst_name in self._properties:
                value = prop_set.get_property(src_name, source, overrides, native)
                setattr(self, dst_name, value)
    
    
    def set_properties_to(self, prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, ignore=None, native=False):
        """
        Sets values of all shared properties from current property set to given
        property set.
        
        If any property is available within 'overrides' the value in
        'overrides' is used instead of current one. If allowed and the value is
        callable but still not of the requested type, given 'source' is provided
        as argument for calling it and returned value is finally used.
        
        In some cases it might be useful to retrieve the callable function
        itself, without applying it onto given source. This can be achieved by
        setting the 'native' argument to True.
        
        Args:
            prop_set: pero.PropertySet
                Property set to which set the properties.
            
            src_prefix: str
                Prefix used for shared properties in the source set. Shared
                properties without this prefix will be skipped.
            
            dst_prefix: str
                Prefix used for shared properties in the destination set. Shared
                properties without this prefix will be skipped.
            
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current values.
                The names should include the 'src_prefix'.
            
            ignore: (str,)
                Collection of properties to be ignored. The names should include
                the 'src_prefix'.
            
            native: bool
                If set to True callable properties from the source are used
                directly without calling.
        """
        
        # check prefixes
        if src_prefix and src_prefix[-1] != PROP_SPLITTER:
            src_prefix = src_prefix + PROP_SPLITTER
        
        if dst_prefix and dst_prefix[-1] != PROP_SPLITTER:
            dst_prefix = dst_prefix + PROP_SPLITTER
        
        # process current properties
        for prop in self.properties():
            
            # get current name without prefix
            name = prop.name
            if src_prefix and name.startswith(src_prefix):
                name = name[len(src_prefix):]
            elif src_prefix:
                continue
            
            # finalize names
            src_name = prop.name
            dst_name = dst_prefix + name
            
            # skip properties
            if ignore and src_name in ignore:
                continue
            
            # set shared properties
            if dst_name in prop_set._properties:
                value = self.get_property(src_name, source, overrides, native)
                setattr(prop_set, dst_name, value)
    
    
    def lock_property(self, name, lock=True, raise_error=True):
        """
        Locks or unlocks specified property to disable or enable any further
        changes.
        
        Args:
            name: str
                Name of the property to be locked/unlocked.
            
            lock: bool
                Specifies whether the property should be locked (True) or
                unlocked (False).
            
            raise_error: bool
                If set to True, an error is raised if unknown property is about
                to be locked/unlocked.
        """
        
        # lock/unlock property
        if name in self._properties:
            
            if lock:
                self._locked.add(name)
            else:
                self._locked.discard(name)
            
            return
        
        # raise error for unknown property
        if raise_error:
            message = "%s has no property '%s'!" % (self.__class__.__name__, name)
            raise AttributeError(message)
    
    
    def hold_property(self, name, hold=True, raise_error=True):
        """
        Holds or releases specified property to keep its previous value if the
        new value is undefined (pero.UNDEF).
        
        Args:
            name: str
                Name of the property to be held/released.
            
            hold: bool
                Specifies whether the property should be held (True) or
                released (False).
            
            raise_error: bool
                If set to True, an error is raised if unknown property is about
                to be held/released.
        """
        
        # hold/release property
        if name in self._properties:
            
            if hold:
                self._held.add(name)
            else:
                self._held.discard(name)
            
            return
        
        # raise error for unknown property
        if raise_error:
            message = "%s has no property '%s'!" % (self.__class__.__name__, name)
            raise AttributeError(message)
    
    
    def is_property_locked(self, name):
        """
        Checks whether specified property is locked.
        
        Args:
            name: str
                Name of the property.
        
        Returns:
            bool
                True if the property is locked, False otherwise.
        """
        
        return name in self._locked
    
    
    def is_property_held(self, name):
        """
        Checks whether specified property is held.
        
        Args:
            name: str
                Name of the property.
        
        Returns:
            bool
                True if the property is held, False otherwise.
        """
        
        return name in self._held
    
    
    def clone(self, source=UNDEF, overrides=None, native=False):
        """
        Creates a shallow copy of current instance. A new pero.PropertySet
        is created with all the properties cloned, however, the actual values
        of the properties are just copied but not cloned.
        
        If any property is available within 'overrides' the value in
        'overrides' is used instead of current one. If allowed and the value is
        callable but still not of the requested type, given 'source' is provided
        as argument for calling it and returned value is finally used. This is
        very useful for defining a 'template' with some properties as functions
        and create a cloned instance with final values. A nice example could be
        labels for scatter plot.
        
        In some cases it might be useful to retrieve the callable function
        itself, without applying it onto given source. This can be achieved by
        setting the 'native' argument to True.
        
        Args:
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current values.
            
            native: bool
                If set to True callable properties are returned directly
                without calling.
        
        Returns:
            pero.PropertySet
                Cloned property set.
        """
        
        # init clone instance
        clone = self.__class__()
        
        # get properties
        for name in self._properties:
            value = self.get_property(name, source, overrides, native)
            setattr(clone, name, value)
        
        # keep locks
        clone._locked = set(self._locked)
        
        # keep holds
        clone._held = set(self._held)
        
        return clone
    
    
    @classmethod
    def properties(cls):
        """
        Gets all available properties of the class.
        
        Returns:
            (pero.Property,)
                Available properties.
        """
        
        key = cls
        
        # use cache
        if key in _PROPERTIES_CACHE:
            return _PROPERTIES_CACHE[key]
        
        # collect properties
        properties = []
        for item in inspect.getmembers(key):
            if isinstance(item[1], Property):
                properties.append(item[1])
        
        # update cache
        _PROPERTIES_CACHE[key] = tuple(properties)
        
        return properties
