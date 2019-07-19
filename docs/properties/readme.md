# Properties

The core of most of the classes within the pero library is a specific implementation of properties and their
collections. This allows to specify properties not only by a final value but dynamically, i.e. as a function to retrieve
the final value from given data source. In addition, it allows for type checking or internal conversion from multiple
definition styles (e.g. for colors).


## Main Classes

- [pero.Property](#Property)
- [pero.PropertySet](#PropertySet)
- [pero.Include](#Include)

## Basic Properties

- [pero.BoolProperty](#BoolProperty)
- [pero.EnumProperty](#EnumProperty)
- [pero.FuncProperty](#FuncProperty)
- [pero.StringProperty](#StringProperty)
- [pero.DictProperty](#DictProperty)

## Numeric Properties

- [pero.NumProperty](#NumProperty)
- [pero.FloatProperty](#FloatProperty)
- [pero.IntProperty](#IntProperty)
- [pero.RangeProperty](#RangeProperty)
- [pero.QuadProperty](#QuadProperty)

## Collection Properties

- [pero.IterProperty](#IterProperty)
- [pero.ListProperty](#ListProperty)
- [pero.SequenceProperty](#SequenceProperty)
- [pero.SetProperty](#SetProperty)
- [pero.TupleProperty](#TupleProperty)

## Special Properties

- [pero.ColorProperty](#ColorProperty)
- [pero.PaletteProperty](#PaletteProperty)
- [pero.GradientProperty](#GradientProperty)
- [pero.DashProperty](#DashProperty)
- [pero.MarkerProperty](#MarkerProperty)
- [pero.HeadProperty](#HeadProperty)
- [pero.FrameProperty](#FrameProperty)

## Property Mixes

- [pero.AngleProperties](#AngleProperties)
- [pero.ColorProperties](#ColorProperties)
- [pero.LineProperties](#LineProperties)
- [pero.FillProperties](#FillProperties)
- [pero.TextProperties](#TextProperties)


### <a id="Property" href="#Property">#</a> pero.Property(default=pero.UNDEF, types=(), dynamic=True, nullable=False)

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


### <a id="PropertySet" href="#PropertySet">#</a> pero.PropertySet(**overrides)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler)

This class provides an abstract base for all property-having classes.

Since the *[pero.PropertySet](#PropertySet)* is derived from *[pero.EvtHandler](../events/readme.md#EvtHandler)* it
behaves like an event manager itself. By default this is used to fire the
[pero.PropertyChangedEvt](../events/readme.md#PropertyChangedEvt) event every time a property value is changed. This
event can be bound using the *bind* method together with
[pero.EVENT.PROPERTY_CHANGED](../events/readme.md#PropertyChangedEvt) type.

```python
import pero

# init property monitor
def monitor(evt):
    print("%s: %s -> %s", (evt.name, evt.old_value, evt.new_value))

# define set
class MyPropertySet(pero.PropertySet):
    
    name = pero.StringProperty(pero.UNDEF)
    x = pero.NumProperty(0)
    y = pero.NumProperty(0)

# instantiate with overrides
my_set = MyPropertySet(name="Glyph")

# set monitor for property changes
my_set.bind(pero.EVT_PROPERTY_CHANGED, monitor)

# set dynamic properties
my_set.x = lambda d: d[0]
my_set.y = lambda d: d[1]

# get property
name = my_set.name
name = my_set.get_property('name')

# get dynamic properties
point = (10, 20)
x = my_set.get_property('x', point)
y = my_set.get_property('y', point)
```

#### Methods:

- **has_property(name)** -> *bool*  
  Returns True if specified property exists, False otherwise.

  -   **name:** *str*  
      Name of the property to check.

- **get_property(name, source=UNDEF, overrides=None, native=False)** -> *any*  
  Gets the value of specified property. If specified property is available within *overrides* the value in *overrides*
  is used instead of current one. If allowed and the value is callable but still not of the requested type, given
  *source* is is provided as the argument for calling it and returned value is finally used.

    In some specific cases it might be useful to retrieve the callable function itself, i.e. without applying it onto
    given source. This can be achieved by setting the *native* argument to True.

  -   **name:** *str*  
      Name of the property to check.
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable property.
    
  -   **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current value.
    
  -   **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **get_child_overrides(child_name, overrides)** -> *{str:any}*  
  Extracts the overrides for existing child property set. A property is considered as a child if it starts with given
  *child_name* followed by '_' and if it is not a direct property of current property set. E.g. if current set has a
  property 'marker', its line properties can be specified directly as 'marker_line_color'. However, this mechanism
  assumes the child property to be also derived from pero.PropertySet and it must be initialized already.

  -   **child_name:** *str*  
      Name of the property to check.
    
  -   **overrides:** *dict* or *None*  
      Overrides to extract the child from.

- **set_property(name, value, raise_error=True)**  
    Sets given value for a property specified by given name.
    
    In some cases it might be useful to initialize also some properties of a child property set directly along the
    current one. Therefore, if the property name is not found within current property set its name is split by '_' and
    it tries to search for a property matching the left side of the split. If such property is found in current property
    set, then the right part of the split is used to set the child property. E.g. if current set has a property
    'marker', its line properties can be set directly as 'marker_line_color'. However, this mechanism assumes the child
    property to be also derived from pero.PropertySet and it must be initialized already.
    
  -   **name:** *str*  
      Name of the property to be set.
    
  -   **value:** *any*  
      Property value to be set.
    
  -   **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be set.

- **set_properties(properties, raise_error=True)**  
    Sets multiple properties in a batch using name:value dictionary.

    In some cases it might be useful to initialize also some properties of a child property set directly along the
    current one. Therefore, if the property name is not found within current property set its name is split by '_' and
    it tries to search for a property matching the left side of the split. If such property is found in current property
    set, then the right part of the split is used to set the child property. E.g. if current set has a property
    'marker', its line properties can be set directly as 'marker_line_color'. However, this mechanism assumes the child
    property to be also derived from pero.PropertySet and it must be initialized already.
    
  -   **properties:** *{str:any}*  
      Properties names and values to be set.
    
  -   **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be set.

- **set_properties_from(prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, native=False)**  
    Sets values of all shared properties (i.e. having the same name) from given property set to current property set.
    
    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed
    and the value is callable but still not of the requested type, given *source* is provided as argument for calling it
    and returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source.
    This can be achieved by setting the *native* argument to True.
    
  -   **prop_set:** *[pero.PropertySet](#PropertySet)*  
      Property set from which to retrieve the properties.
    
  -   **src_prefix:** *str*  
      Prefix used for shared properties in the source set. Shared properties without this prefix will be skipped.
    
  -   **dst_prefix:** *str*  
      Prefix used for shared properties in the destination set. Shared properties without this prefix will be skipped.
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
  -   **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values.
    
  -   **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **set_properties_to(prop_set, src_prefix="", dst_prefix="", source=UNDEF, overrides=None, native=False)**  
    Sets values of all shared properties (i.e. having the same name) from current property set to given property set.

    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed
    and the value is callable but still not of the requested type, given *source* is provided as argument for calling it
    and returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source.
    This can be achieved by setting the *native* argument to True.
    
  -   **prop_set:** *[pero.PropertySet](#PropertySet)*  
      Property set to which to the properties should be set.
    
  -   **src_prefix:** *str*  
      Prefix used for shared properties in the source set. Shared properties without this prefix will be skipped.
    
  -   **dst_prefix:** *str*  
      Prefix used for shared properties in the destination set. Shared properties without this prefix will be skipped.
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
  -   **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values 
    
  -   **native:** *bool*  
      If set to True callable properties are returned directly without calling them with the source as argument.

- **lock_property(name, lock=True, raise_error=True)**  
  Locks or unlocks specified property to disable or re-enable further changes. This is typically used for properties,
  which must be provided upon a class initialization and must stay intact after that.
    
  -   **name:** *str*  
      Name of the property to be set.
    
  -   **lock:** *bool*  
      Specifies whether the property should be locked (True) or unlocked (False) 
    
  -   **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be locked.

- **hold_property(name, hold=True, raise_error=True)**  
  Holds or releases specified property, which means its current value stays unchanged if the new value to be set is
  undefined (pero.UNDEF). This is used for several properties of the [pero.Canvas](../drawing/canvas.md#Canvas) so that
  the values are never set to undefined state.
    
  -   **name:** *str*  
      Name of the property to be set.
    
  -   **lock:** *bool*  
      Specifies whether the property should be locked (True) or unlocked (False).
    
  -   **raise_error:** *bool*  
      If set to True, an error is raised if unknown property is about to be held.

- **is_property_locked(name)** -> *bool*  
  Returns True if specified property is locked, False otherwise.
    
  -   **name:** *str*  
      Name of the property to check.

- **is_property_held(name)** -> *bool*  
  Returns True if specified property is held, False otherwise.
    
  -   **name:** *str*  
      Name of the property to check.

- **clone(name, source=UNDEF, overrides=None, native=False)** -> *any*  
  Creates a shallow copy of current instance. A new [pero.PropertySet](#PropertySet) is created with all the properties
  cloned, however, the actual values of the properties are just copied, not cloned.
    
    If any property is available within *overrides* the value in *overrides* is used instead of current one. If allowed
    and the value is callable but still not of the requested type, given 'source' is provided as argument for calling it
    and returned value is finally used.
    
    In some cases it might be useful to retrieve the callable function itself, without applying it onto given source.
    This can be achieved by setting the *native* argument to True 
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
  -   **overrides:** *dict* or *None*  
      Highest priority properties to be used instead of current values.
    
  -   **native:** *bool*  
      If set to True callable properties are set directly without calling them with the source as argument.
  
#### Class Methods:

- **properties()** -> *([pero.Property](#Property),)*  
  Gets all available properties of the class.


### <a id="Include" href="#Include">#</a> pero.Include(prop_set, prefix="", dynamic=None, nullable=None, exclude=None, **overrides)

This class is used as a tool to include all available [pero.Properties](#Property) of another
[pero.PropertySet](#PropertySet). The properties can be included with optional *prefix*, which is added then to the name
of each included property, and custom defaults provided as *overrides*. In addition the *dynamic* and *nullable* flags
can also be changed for all the included property 

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


```python
import pero

class MyPropertySet(pero.PropertySet):
    
    # this registers all properties of pero.LineProperties prefixed by 'horizontal_'
    # e.g. horizontal_line_width = 2
    horizontal_pen = pero.Include(pero.LineProperties, prefix="horizontal_", line_width=2)
    
    # this again registers all properties of pero.LineProperties now prefixed by 'vertical_'
    # e.g. vertical_line_width = 2
    vertical_pen = pero.Include(pero.LineProperties, prefix="vertical_", line_width=1)
```

## Basic Properties

### <a id="BoolProperty" href="#BoolProperty">#</a> pero.BoolProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing booleans only.

- **default:** *bool*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="EnumProperty" href="#EnumProperty">#</a> pero.EnumProperty(default=UNDEF, enum=(), **kwargs)

**Inheritance:** [Property](#Property)

Defines a generic property allowing predefined set of values only.

- **default:** *any*  
  Default value used to initialize the property.

- **enum:** *(any,)*  
  Collection of allowed values.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="FuncProperty" href="#FuncProperty">#</a> pero.FuncProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing functions and methods only.

- **default:** *callable*  
  Default value used to initialize the property.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="StringProperty" href="#StringProperty">#</a> pero.StringProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing strings only.

- **default:** *str*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="DictProperty" href="#DictProperty">#</a> pero.DictProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing dicts only.

- **default:** *{any:any}*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


## Numeric Properties

### <a id="NumProperty" href="#NumProperty">#</a> pero.NumProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a numeric property allowing floats and integers only.

- **default:** *int* or *float*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="FloatProperty" href="#FloatProperty">#</a> pero.FloatProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing floats only.

- **default:** *float*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="IntProperty" href="#IntProperty">#</a> pero.IntProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property allowing floats only.

- **default:** *int*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="RangeProperty" href="#RangeProperty">#</a> pero.RangeProperty(default=UNDEF, minimum=None, maximum=None, minimum_incl=True, maximum_incl=True, **kwargs)

**Inheritance:** [Property](#Property)

Defines a generic property allowing numbers within specific range only.

- **default:** *(int, int)* or *(float, float)*  
  Default value used to initialize the property.

- **minimum:** *int*, *float* or *None*  
  Minimum allowed value.

- **maximum:** *int*, *float* or *None*  
  Maximum allowed value.

- **minimum_incl:** *bool*  
  Specifies whether the minimum value should be included (True) or excluded (False) from allowed range.

- **maximum_incl:** *bool*  
  Specifies whether the maximum value should be included (True) or excluded (False) from allowed range.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="QuadProperty" href="#QuadProperty">#</a> pero.QuadProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property used for quad-sided connected values like margin, padding etc. The value must be provided as a single
number or as a list or tuple of numbers defining individual values for top, right, bottom and left side. If only a
single value is provided, it is used for all the sides. If two values are provided, the first value is set to top and
bottom and the second value is set to left and right.

- **default:** *int*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


## Collection Properties

### <a id="IterProperty" href="#IterProperty">#</a> pero.IterProperty(default=UNDEF, intypes=(), **kwargs)

**Inheritance:** [Property](#Property)

Defines a generic property allowing collections with specified types of inner elements.

- **default:** *(any,)*  
  Default value used to initialize the property.

- **intypes:** *(type,)*  
  Allowed types for collection elements. If empty, specific inner type is not required for inner elements.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="ListProperty" href="#ListProperty">#</a> pero.ListProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property) <- [IterProperty](#IterProperty)

Defines a property allowing lists only.

- **default:** *\[any,\]*  
  Default value used to initialize the property.

- **intypes:** *(type,)*  
  Allowed types for collection elements. If empty, specific inner type is not required for inner elements.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="SequenceProperty" href="#SequenceProperty">#</a> pero.SequenceProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property) <- [IterProperty](#IterProperty)

Defines a property allowing lists, tuples and numpy.ndarray only.

- **default:** *(any,)*  
  Default value used to initialize the property.

- **intypes:** *(type,)*  
  Allowed types for collection elements. If empty, specific inner type is not required for inner elements.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="SetProperty" href="#SetProperty">#</a> pero.SetProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property) <- [IterProperty](#IterProperty)

Defines a property allowing sets only.

- **default:** *(any,)*  
  Default value used to initialize the property.

- **intypes:** *(type,)*  
  Allowed types for collection elements. If empty, specific inner type is not required for inner elements.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="TupleProperty" href="#TupleProperty">#</a> pero.TupleProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property) <- [IterProperty](#IterProperty)

Defines a property allowing tuples only.

- **default:** *(any,)*  
  Default value used to initialize the property.

- **intypes:** *(type,)*  
  Allowed types for collection elements. If empty, specific inner type is not required for inner elements.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


## Special Properties

### <a id="ColorProperty" href="#ColorProperty">#</a> pero.ColorProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property, which simplifies a color definition by automatically creating a [pero.Color](../colors/readme.md#Color)
instance from various input options or registered name. See [color definition](../colors/readme.md#Color) for more info.

- **default:** *[color definition](../colors/readme.md#Color)*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="PaletteProperty" href="#PaletteProperty">#</a> pero.PaletteProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property, which simplifies a color palette definition by automatically creating a
[pero.Palette](../colors/readme.md#Palette) instance from various input options or registered palette name. See
[palette definition](../colors/readme.md#Palette) for more info.

- **default:** *[palette definition](../colors/readme.md#Palette)*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="GradientProperty" href="#GradientProperty">#</a> pero.GradientProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a property, which simplifies a color gradient definition by automatically creating a
[pero.Gradient](../colors/readme.md#Gradient) instance from various input options or registered gradient name. See
[gradient definition](../colors/readme.md#Gradient) for more info.

- **default:** *[gradient definition](../colors/readme.md#Gradient)*  
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="DashProperty" href="#DashProperty">#</a> pero.DashProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a line dash property. The value must be provided as a list or tuple of numbers defining the length of lines and
spaces in-between.

- **default:** *(int,)* or *(float,)*   
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.

### <a id="MarkerProperty" href="#MarkerProperty">#</a> pero.MarkerProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a marker property, which simplifies a marker definition by converting specific symbols into an instance of
corresponding *[pero.Marker](../drawing/marker.md#Marker)* glyph. Available symbols are defined by the
[pero.MARKER](../enums/readme.md#MARKER) enum.

- **default:** *str* or *[pero.Marker](../drawing/marker.md#Marker)*   
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


### <a id="HeadProperty" href="#HeadProperty">#</a> pero.HeadProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a head property, which simplifies a head definition by converting specific symbols into an instance of
corresponding *[pero.Head](../drawing/arrow.md#Head)* glyph. Available symbols are defined by the
[pero.HEAD](../enums/readme.md#HEAD) enum.

- **default:** *str* or *[pero.Head](../drawing/arrow.md#Head)*   
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.

### <a id="FrameProperty" href="#FrameProperty">#</a> pero.FrameProperty(default=UNDEF, **kwargs)

**Inheritance:** [Property](#Property)

Defines a frame property. The value must be provided as a [pero.Frame](../drawing/frame.md#Frame) or as a tuple or list
of four numbers for left x, top y, width and height.

- **default:** *(int, int, int, int)* or *[pero.Frame](../drawing/frame.md#Frame)*   
  Default value used to initialize the property.

- **dynamic:** *bool*  
  Specifies whether the property can be defined as dynamic i.e. the actual value of the property is a function, which is
  expected to give the final value from provided data source. Assigned function must provide expected value type.

- **nullable:** *bool*  
  Specifies whether the property value can be set to None.


## Property Mixes

### <a id="AngleProperties" href="#AngleProperties">#</a> pero.AngleProperties(**kwargs)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler) <- [PropertySet](#PropertySet)

Collection of properties defining an angle value with its units.

#### Properties

- **angle:** *int* or *float*   
  Specifies the angle value.

- **angle_units:** *str*   
  Specifies the angle units as any item from the [pero.ANGLE](../enums/readme.md#ANGLE) enum.

#### Static Methods

- **get_angle(prop_set, prefix="", units=ANGLE.RAD, source=UNDEF, overrides=None)** -> *float*   
  Retrieves current angle value from given [pero.PropertySet](#PropertySet) directly converted to requested units.
        
  -   **prop_set:** *[pero.PropertySet](#PropertySet)*  
      Property set from which to retrieve the angle.
    
  -   **prefix:** *str*  
      Prefix applied to all angle properties.
    
  -   **units:** *str*  
      Requested units of the angle as any item from the [pero.ANGLE](../enums/readme.md#ANGLE) enum.
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
  -   **overrides:** *{str:any}* or *None*  
      Highest priority properties to be used instead of current values.

### <a id="ColorProperties" href="#ColorProperties">#</a> pero.ColorProperties(**kwargs)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler) <- [PropertySet](#PropertySet)

Collection of properties defining a color.

#### Properties

- **color:** *[color definition](../colors/readme.md#Color)**   
  Specifies the color as an RGB or RGBA tuple, hex code, name or [pero.Color](../colors/readme.md#Color). If the color
  is set to *None*, transparent color is set instead.

- **alpha:** *int*   
  Specifies the color alpha channel as a value between 0 and 255, where 0 means fully transparent and 255 fully opaque.
  If this value is set, it will overwrite the alpha channel in the final color.

#### Static Methods

- **get_color(prop_set, prefix="", source=UNDEF, overrides=None)** -> *[pero.Color](../colors/readme.md#Color)*   
  Retrieves current color value from given [pero.PropertySet](#PropertySet) with the alpha property automatically
  applied.
        
  -   **prop_set:** *[pero.PropertySet](#PropertySet)*  
      Property set from which to retrieve the color.
    
  -   **prefix:** *str*  
      Prefix applied to all color properties.
    
  -   **source:** *any*  
      Data source to be used for retrieving the final value of callable properties.
    
  -   **overrides:** *{str:any}* or *None*  
      Highest priority properties to be used instead of current values.

### <a id="LineProperties" href="#LineProperties">#</a> pero.LineProperties(**kwargs)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler) <- [PropertySet](#PropertySet)

Collection of properties defining a line or pen style.

#### Properties

- **line_color:** *[color definition](../colors/readme.md#Color)*  
  Specifies the line color as an RGB or RGBA tuple, hex code, name or [pero.Color](../colors/readme.md#Color).

- **line_alpha:** *int*  
  Specifies the line color alpha channel as a value between 0 and 255, where 0 is fully transparent and 255 fully
  opaque. If this value is set, it will overwrite the alpha channel in the final line color.
        
- **line_width:** *int* or *float*  
  Specifies the line width.
        
- **line_style:** *str*  
  Specifies the line drawing style as any item from the [pero.LINE_STYLE](../enums/readme.md#LINE_STYLE) enum.
        
- **line_dash:** *(float,)*  
  Specifies the line dash style as a collection of numbers defining the lengths of lines and spaces in-between.
  Specified value is used if the 'line_style' property is set to *pero.LINE_STYLE.CUSTOM*.
        
- **line_cap:** *str*  
  Specifies the line ends shape as any item from the [pero.LINE_CAP](../enums/readme.md#LINE_CAP) enum.
        
- **line_join:** *str*  
  Specifies the line corners shape as any item from the [pero.LINE_JOIN](../enums/readme.md#LINE_JOIN) enum.

### <a id="FillProperties" href="#FillProperties">#</a> pero.FillProperties(**kwargs)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler) <- [PropertySet](#PropertySet)

Collection of properties defining a fill or brush style.

#### Properties

- **fill_color:** *[color definition](../colors/readme.md#Color)*  
  Specifies the fill color as an RGB or RGBA tuple, hex code, name or [pero.Color](../colors/readme.md#Color).

- **fill_alpha:** *int*  
  Specifies the fill color alpha channel as a value between 0 and 255, where 0 is fully transparent and 255 fully
  opaque. If this value is set, it will overwrite the alpha channel in the final fill color.
        
- **fill_style:** *str*  
  Specifies the fill style as any item from the [pero.FILL_STYLE](../enums/readme.md#FILL_STYLE) enum.

### <a id="TextProperties" href="#TextProperties">#</a> pero.TextProperties(**kwargs)

**Inheritance:** [EvtHandler](../events/readme.md#EvtHandler) <- [PropertySet](#PropertySet)

Collection of properties defining a text style.

#### Properties

- **font_size:** *int*  
  Specifies the font size or None to reset to default size.
        
- **font_name:** *str*  
  Specifies an existing font name or None to reset to default family.
        
- **font_family:** *str*  
  Specifies the font family as any item from the [pero.FONT_FAMILY](../enums/readme.md#FONT_FAMILY) enum or None to
  reset to default family.

- **font_style:** *str*  
  Specifies the font style as any item from the [pero.FONT_STYLE](../enums/readme.md#FONT_STYLE) enum or None to reset
  to default style.

- **font_weight:** *str*  
  Specifies the font weight as any item from the [pero.FONT_WEIGHT](../enums/readme.md#FONT_WEIGHT) enum or None to
  reset to default weight.
        
- **text_align:** *str*  
  Specifies the text alignment as any item from the [pero.TEXT_ALIGN](../enums/readme.md#TEXT_ALIGN) enum or None to
  reset to default alignment.
        
- **text_base:** *str*  
  Specifies the text baseline as any item from the [pero.TEXT_BASELINE](../enums/readme.md#TEXT_BASELINE) enum or None
  to reset to default baseline.
        
- **text_color:** *[color definition](../colors/readme.md#Color)*  
  Specifies the text foreground color as an RGB or RGBA tuple, hex code, name or [pero.Color](../colors/readme.md#Color).
        
- **text_alpha:** *int*  
  Specifies the text foreground alpha channel as a value between 0 and 255, where 0 is fully transparent and 255 fully
  opaque. If this value is set, it will overwrite the alpha channel of the final text color.
        
- **text_bgr_color:** *[color definition](../colors/readme.md#Color)*  
  Specifies the text background color as an RGB or RGBA tuple, hex code, name or [pero.Color](../colors/readme.md#Color).
        
- **text_bgr_alpha: *int*  
  Specifies the text background alpha channel as a value between 0 and 255, where 0 is fully transparent and 255 fully
  opaque. If this value is set, it will overwrite the alpha channel of the final text background color.
        
- **text_split:** *bool*  
  Specifies whether the text should be first split into individual lines. This requires corresponding 'text_splitter'
  property to be set.
        
- **text_splitter:** *str*  
  Specifies the character(s) to be used for splitting a text into individual lines.
        
- **text_spacing:** *float*  
  Specifies additional space to be inserted between text lines as multiplier of line height.