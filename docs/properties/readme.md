# Properties

### <a id="Event" href="#Property">#</a> pero.Property(default=pero.UNDEF, types=(), dynamic=True, nullable=False)

Defines a generic property used in all [pero.PropertySet](#PropertySet) classes. The main purpose is to provide
reasonable default value and possibility to allow certain types or values only. Specific derived implementations can be
created to provide custom value checking and parsing by overwriting the *parse* and *clone* methods. If allowed by the
*dynamic* attribute the actual value can be a function or method, which is expected to give the final value from
provided data source. This allows properties to be dynamic and provide specific values based on actual data.

- **default:** *any*  
  Default value used to initialize the property.

- **types:** *(type,)*  
  Specifies the allowed types for values. If empty, specific type is not required for values.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.

#### Properties:

- **name** -> *str* or *None*  
  Gets property name.

- **default** -> *any*  
  Gets the default value.

- **types** -> *(type,)*  
  Gets allowed types.


- **dynamic** -> *bool*  
  Gets the value indicating whether the property can be dynamic (True).


- **nullable** -> *bool*  
  Gets the value indicating whether the property can be set to None (True).

#### Methods:

- **parse(value)** -> *any*  
  Validates and converts given value into final requested type or keeps callable (if allowed). The base implementation
  only ensures the allowed type but some of the more specific properties have their own implementations.


- **clone(\*\*kwargs)** -> *[pero.Property](#Property)*  
  Creates a clone of current property. Note that any custom property, which defines its own attributes should overwrite
  this method and provide its own attributes as keyword arguments to this base method.


### <a id="Event" href="#PropertySet">#</a> pero.PropertySet(**overrides)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler)

Abstract base class for all property-having classes.

#### Methods:

- **has_property(name)** -> *bool*  
  Returns True if specified property exists, False otherwise.

    - **name:** *str*  
    Name of the property to check.

- **get_property(name, source=UNDEF, overrides=None, native=False)** -> *any*  
  Gets the value of specified property. If specified property is available within *overrides* the value in *overrides*
  is used instead of current one. If allowed and the value is callable but still not of the requested type, given
  *source* is is provided as the argument for calling it and returned value is finally used.

    In some specific cases it might be useful to retrieve the callable function itself, i.e. without applying it onto
    given source. This can be achieved by setting the *native* argument to True.

    - **name:** *str*  
      Name of the property to check.
    
    - **source:** *any*  
      Data source to be used for retrieving the final value of callable property.
    
    - **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current value.
    
    - **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **get_child_overrides(child_name, overrides)** -> *dict*  
  Extracts the overrides for existing child property set. A property is considered as a child if it starts with given
  *child_name* followed by '_' and if it is not a direct property of current property set. E.g. if current set has a
  property 'marker', its line properties can be specified directly as 'marker_line_color'. However, this mechanism
  assumes the child property to be also derived from pero.PropertySet and it must be initialized already.

    - **child_name:** *str*  
      Name of the property to check.
    
    - **overrides:** *dict* or *None*  
      Overrides to extract the child from.

- **set_property(name, value, raise_error=True)**  
    Sets given value for a property specified by given name.
    
    In some cases it might be useful to initialize also some properties of a child property set directly along the current
    one. Therefore, if the property name is not found within current property set its name is split by '_' and it tries to
    search for a property matching the left side of the split. If such property is found in current property set, then the
    right part of the split is used to set the child property. E.g. if current set has a property 'marker', its line
    properties can be set directly as 'marker_line_color'. However, this mechanism assumes the child property to be also
    derived from pero.PropertySet and it must be initialized already.
    
    - **name:** *str*  
      Name of the property to be set.
    
    - **value:** *any*  
      Property value to be set.
    
    - **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be set.

- **set_properties(properties, raise_error=True)**  
    Sets multiple properties in a batch using name:value dictionary.

    In some cases it might be useful to initialize also some properties of a child property set directly along the current
    one. Therefore, if the property name is not found within current property set its name is split by '_' and it tries to
    search for a property matching the left side of the split. If such property is found in current property set, then the
    right part of the split is used to set the child property. E.g. if current set has a property 'marker', its line
    properties can be set directly as 'marker_line_color'. However, this mechanism assumes the child property to be also
    derived from pero.PropertySet and it must be initialized already.
    
    - **properties:** *{str:any}*  
      Properties names and values to be set.
    
    - **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be set.

- **set_properties_from(prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, native=False)**  
    Sets values of all shared properties (i.e. having the same name) from given property set to current property set.
    
    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed and
    the value is callable but still not of the requested type, given *source* is provided as argument for calling it and
    returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source. This
    can be achieved by setting the *native* argument to True.
    
    - **prop_set:** *[pero.PropertySet](readme.md#PropertySet)*  
      Property set from which to retrieve the properties.
    
    - **src_prefix:** *str*  
      Prefix used for shared properties in the source set. Shared properties without this prefix will be skipped.
    
    - **dst_prefix:** *str*  
      Prefix used for shared properties in the destination set. Shared properties without this prefix will be skipped.
    
    - **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
    - **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values.
    
    - **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **set_properties_to(prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, native=False)**  
    Sets values of all shared properties (i.e. having the same name) from current property set to given property set.

    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed and
    the value is callable but still not of the requested type, given *source* is provided as argument for calling it and
    returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source. This
    can be achieved by setting the *native* argument to True.
    
    - **prop_set:** *[pero.PropertySet](readme.md#PropertySet)*  
      Property set to which to the properties should be set.
    
    - **src_prefix:** *str*  
      Prefix used for shared properties in the source set. Shared properties without this prefix will be skipped.
    
    - **dst_prefix:** *str*  
      Prefix used for shared properties in the destination set. Shared properties without this prefix will be skipped.
    
    - **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
    - **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values.
    
    - **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **lock_property(name, lock=True, raise_error=True)**  
  Locks or unlocks specified property to disable or re-enable further changes. This is typically used for properties,
  which must be provided upon a class initialization and must stay intact after that.
    
    - **name:** *str*  
      Name of the property to be set.
    
    - **lock:** *bool*  
      Specifies whether the property should be locked (True) or unlocked (False).
    
    - **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be locked.

- **hold_property(name, hold=True, raise_error=True)**  
  Holds or releases specified property, which means its current value stays unchanged if the new value to be set is
  undefined (pero.UNDEF). This is used for several properties of the [pero.Canvas](../drawing/canvas.md) so that the
  values are never set to undefined state.
    
    - **name:** *str*  
      Name of the property to be set.
    
    - **lock:** *bool*  
      Specifies whether the property should be locked (True) or unlocked (False).
    
    - **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be held.

- **is_property_locked(name)** -> *bool*  
  Returns True if specified property is locked, False otherwise.
    
    - **name:** *str*  
      Name of the property to check.

- **is_property_held(name)** -> *bool*  
  Returns True if specified property is held, False otherwise.
    
    - **name:** *str*  
      Name of the property to check.

- **clone(name, source=UNDEF, overrides=None, native=False)** -> *any*  
  Creates a shallow copy of current instance. A new [pero.PropertySet](#PropertySet) is created with all the properties
  cloned, however, the actual values of the properties are just copied, not cloned.
    
    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed and
    the value is callable but still not of the requested type, given 'source' is provided as argument for calling it and
    returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source. This
    can be achieved by setting the *native* argument to True.
    
    - **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
    - **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values.
    
    - **native:** *bool*  
      If set to True callable properties are set directly without calling them with the source as argument.
  
#### Class Methods:

- **properties()** -> *([pero.Property](#Property),)*  
  Gets all available properties of the class.


### <a id="Event" href="#Include">#</a> pero.Include(prop_set, prefix="", dynamic=None, nullable=None, exclude=None, **overrides)

This class is used as a tool to include all available [pero.Properties](#Property) of another
[pero.PropertySet](#PropertySet). The properties can be included with optional *prefix*, which is added then to the name
of each included property, and custom defaults provided as *overrides*. In addition the *dynamic* and *nullable* flags
can also be changed for all the included property.

- **prop_set:** *[pero.PropertySet](#PropertySet)*  
  Property set class from which to include all the properties.
            
- **prefix:** *str*  
  Optional prefix to be added to the names of all included properties.
            
- **dynamic:** *bool* or *None*  
  If set to True or False the value overwrites the original value of the all included properties.
            
- **nullable:** *bool* or *None*  
  If set to True or False the value overwrites the original value of the all included properties.
            
- **exclude:** *(str,)*  
  Names of the properties to ignore. Original names without the prefix must be used.
            
- **overrides:** *{str:any}*  
  Overwrites for default values of specific properties. Original names without the prefix must be used.