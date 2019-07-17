# Events

### <a id="Event"></a> pero.Event(**kwargs)
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


## Events

- [pero.PropertyChangedEvt](#PropertyChangedEvt)
- [pero.PenChangedEvt](#PenChangedEvt)
- [pero.BrushChangedEvt](#BrushChangedEvt)
- [pero.TextChangedEvt](#TextChangedEvt)
- [pero.ViewEvt](#ViewEvt)
- [pero.KeyEvt](#KeyEvt)
- [pero.KeyDownEvt](#KeyDownEvt)
- [pero.KeyUpEvt](#KeyUpEvt)


## Property Events

### <a id="PropertyChangedEvt"></a> pero.PropertyChangedEvt(**kwargs)

**Inheritance:** [Event](#Event)

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


### <a id="PenChangedEvt"></a> pero.PenChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any pen-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.PEN_CHANGED*


### <a id="BrushChangedEvt"></a> pero.BrushChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any brush-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.BRUSH_CHANGED*


### <a id="TextChangedEvt"></a> pero.TextChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any text-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.TEXT_CHANGED*



## View Events

### <a id="ViewEvt"></a> pero.ViewEvt(**kwargs)

**Inheritance:** [Event](#Event)

Abstract base class for various types of *[pero.View](../backends/view.md)* events.

#### Class Properties:

- **TYPE** -> *pero.VIEW*

#### Attributes:

- **native** -> *any*  
Native event fired by the view.

- **view** -> *[pero.View](../backends/view.md)*  
The view, which fires the event.

- **graphics** -> *[pero.Graphics](../drawing/graphics.md)*  
The view main graphics object.


### <a id="SizeEvt"></a> pero.SizeEvt(**kwargs)
**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt)

Defines an event which is fired if *[pero.View](../backends/view.md)* size was changed.

#### Class Properties:

- **TYPE** -> *pero.SIZE*

#### Attributes:

- **width** -> *int*  
New width of the view.

- **height** -> *int*  
  New height of the view.


### <a id="KeyEvt"></a> pero.KeyEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt)

Defines a generic event which is fired on any key-related event of *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.KEY*

#### Attributes:

- **key** -> *int*  
Key code.

- **char** -> *str*  
Character string or None if not character.

- **pressed** -> *bool*  
Indicates the key pressed state.

- **alt_down** -> *bool*  
Indicates Alt key state.

- **cmd_down** -> *bool*  
Indicates Command key state.

- **ctrl_down** -> *bool*  
Indicates Control key state.

- **shift_down** -> *bool*  
Indicates Shift key state.


### <a id="KeyDownEvt"></a> pero.KeyDownEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [KeyEvt](#KeyEvt)

Defines an event which is fired if a key is pressed inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.KEY_DOWN*


### <a id="KeyUpEvt"></a> pero.KeyUpEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [KeyEvt](#KeyEvt)

Defines an event which is fired if a key is released inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.KEY_UP*
