# Events

### <a name="Event" href="#Event">#</a> pero.Event(**kwargs)
Abstract base class for various types of events. Each derived event class has to specify its unique *TYPE* property at
least.


#### Class Properties:

- **TYPE -> str**  
Specifies the event type.


#### Methods:

- **cancel()**  
Sets current event as canceled to prevent following subscribers to be called.

- **resume()**  
Sets current event as not canceled to allow following subscribers to be called.

- **is_canceled() -> *bool***  
Returns True if the event has been canceled, False otherwise.


## Property Events

### <a name="PropertyChangedEvt" href="#PropertyChangedEvt">#</a> pero.PropertyChangedEvt(**kwargs)

**Inheritance:** [Event](event.md#Event)

Defines an event which is fired if any property of a *[pero.PropertySet](../properties/propset.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.PROPERTY_CHANGED*

#### Attributes:

- **name** -> *str*  
Gets the name of the changed property.

- **old_value** -> *any*  
Gets the original value of the changed property.

- **new_value** -> *any*  
Gets the new value of the changed property.


### <a name="PenChangedEvt" href="#PenChangedEvt">#</a> pero.PenChangedEvt(**kwargs)

**Inheritance:** [Event](event.md#Event) <- [PropertyChangedEvt](event.md#PropertyChangedEvt)

Defines an event which is fired if any pen-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.PEN_CHANGED*


### <a name="BrushChangedEvt" href="#BrushChangedEvt">#</a> pero.BrushChangedEvt(**kwargs)

**Inheritance:** [Event](event.md#Event) <- [PropertyChangedEvt](event.md#PropertyChangedEvt)

Defines an event which is fired if any brush-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.BRUSH_CHANGED*


### <a name="TextChangedEvt" href="#TextChangedEvt">#</a> pero.TextChangedEvt(**kwargs)

**Inheritance:** [Event](event.md#Event) <- [PropertyChangedEvt](event.md#PropertyChangedEvt)

Defines an event which is fired if any text-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.TEXT_CHANGED*