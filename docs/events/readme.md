# Events

To be truly unified API, the *pero* library implements its own events mechanism. This mechanism is typically used to
inform any class derived from *[pero.PropertySet](../properties/readme.md#PropertySet)* if a property has changed, or to unify
the key and mouse events raised by *[pero.View](../backends/readme.md#View)*.


### <a id="Event" href="#Event">#</a> pero.Event(**kwargs)

The *[pero.Event](#Event)* is an abstract base class, from which various types of events are derived. Each derived class
must define its unique *TYPE* property, which can be used to bind specific event to a callback.

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


### <a id="EvtHandler" href="#EvtHandler">#</a> pero.EvtHandler()

This class represents an event raising base class, to which specific callbacks can be attached to be called when
appropriate *[pero.Event](#Event)* is fired. When specific event is fired, **bound callbacks are called in reversed
order**, so the last added callback will be called first. Calling of registered callbacks continues until all are called
or until one of them cancels the event by calling the *cancel* method.


#### Methods:

- **bind(evt_type, callback, \*\*kwargs)**  
  Registers given callback for specific event. Additional keyword arguments can be specified to be always provided when
  the event is fired. These arguments will be used as defaults but they can be overridden by the same argument provided
  directly to the *fire* method.

    - **evt_type:** *str* or *[pero.Event](#Event)*  
    Specific event type to which the callback should be attached.

    - **callback:** *callable*  
    Callback to be called when event is fired.

    - **kwargs:** *{str: any}*  
    Specific keyword arguments.


- **unbind(evt_type, callback, \*\*kwargs)**  
  Removes given callback if registered for specified event. If additional keyword arguments are provided, they must
  match exactly all the arguments provided when the callback was attached. If not provided, just the callback must
  match.

    - **evt_type:** *str* or *[pero.Event](#Event)*  
    Specific event type to which the callback was attached.

    - **callback:** *callable*  
    Callback to be removed.

    - **kwargs:** *{str: any}*  
    Specific keyword arguments.


- **fire(evt, callback, \*\*kwargs)**  
  Fires given event by calling all registered callbacks with given params. When a specific event is fired, bound
  callbacks are called in reversed order, so the last added callback will be called first. Calling of registered
  callbacks continues until all are called or until one of them cancels the event by calling *cancel* method.

    - **evt:** *str* or *[pero.Event](#Event)*  
    Event instance which should be processed.

    - **kwargs:** *{str: any}*  
    Specific keyword arguments.


## Events

- [pero.PropertyChangedEvt](#PropertyChangedEvt)
- [pero.PenChangedEvt](#PenChangedEvt)
- [pero.BrushChangedEvt](#BrushChangedEvt)
- [pero.TextChangedEvt](#TextChangedEvt)
- [pero.ViewEvt](#ViewEvt)
- [pero.KeyEvt](#KeyEvt)
- [pero.KeyDownEvt](#KeyDownEvt)
- [pero.KeyUpEvt](#KeyUpEvt)
- [pero.MouseEvt](#MouseEvt)
- [pero.MouseEnterEvt](#MouseEnterEvt)
- [pero.MouseLeaveEvt](#MouseLeaveEvt)
- [pero.MouseMotionEvt](#MouseMotionEvt)
- [pero.MouseScrollEvt](#MouseScrollEvt)
- [pero.LeftDownEvt](#LeftDownEvt)
- [pero.LeftUpEvt](#LeftUpEvt)
- [pero.LeftDClickEvt](#LeftDClickEvt)
- [pero.MiddleDownEvt](#MiddleDownEvt)
- [pero.MiddleUpEvt](#MiddleUpEvt)
- [pero.MiddleDClickEvt](#MiddleDClickEvt)
- [pero.RightDownEvt](#RightDownEvt)
- [pero.RightUpEvt](#RightUpEvt)
- [pero.RightDClickEvt](#RightDClickEvt)


### <a id="PropertyChangedEvt" href="#PropertyChangedEvt">#</a> pero.PropertyChangedEvt(**kwargs)

**Inheritance:** [Event](#Event)

Defines an event which is fired if any property of a *[pero.PropertySet](../properties/readme.md#PropertySet)* was changed.

#### Class Properties:

- **TYPE** -> *pero.PROPERTY_CHANGED*

#### Attributes:

- **name** -> *str*  
Gets the name of the changed property.

- **old_value** -> *any*  
Gets the original value of the changed property.

- **new_value** -> *any*  
Gets the new value of the changed property.


### <a id="PenChangedEvt" href="#PenChangedEvt">#</a> pero.PenChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any pen-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.PEN_CHANGED*


### <a id="BrushChangedEvt" href="#BrushChangedEvt">#</a> pero.BrushChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any brush-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.BRUSH_CHANGED*


### <a id="TextChangedEvt" href="#TextChangedEvt">#</a> pero.TextChangedEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [PropertyChangedEvt](#PropertyChangedEvt)

Defines an event which is fired if any text-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

#### Class Properties:

- **TYPE** -> *pero.TEXT_CHANGED*



### <a id="ViewEvt" href="#ViewEvt">#</a> pero.ViewEvt(**kwargs)

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


### <a id="SizeEvt" href="#SizeEvt">#</a> pero.SizeEvt(**kwargs)
**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt)

Defines an event which is fired if *[pero.View](../backends/view.md)* size was changed.

#### Class Properties:

- **TYPE** -> *pero.SIZE*

#### Attributes:

- **width** -> *int*  
New width of the view.

- **height** -> *int*  
  New height of the view.


### <a id="KeyEvt" href="#KeyEvt">#</a> pero.KeyEvt(**kwargs)

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


### <a id="KeyDownEvt" href="#KeyDownEvt">#</a> pero.KeyDownEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [KeyEvt](#KeyEvt)

Defines an event which is fired if a key is pressed inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.KEY_DOWN*


### <a id="KeyUpEvt" href="#KeyUpEvt">#</a> pero.KeyUpEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [KeyEvt](#KeyEvt)

Defines an event which is fired if a key is released inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.KEY_UP*


### <a id="MouseEvt" href="#MouseEvt">#</a> pero.MouseEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt)

Defines a generic event which is fired on any mouse-related event of *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MOUSE*

#### Attributes:

- **x_pos** -> *float*  
Cursor x-coordinate in device units.

- **y_pos** -> *float*  
Cursor y-coordinate in device units.

- **x_rot** -> *float*  
Mouse wheel rotation in x-direction.

- **y_rot** -> *float*  
Mouse wheel rotation in y-direction.

- **left_down** -> *bool*  
Indicates left mouse button key state.

- **middle_down** -> *bool*  
Indicates middle mouse button key state.

- **right_down** -> *bool*  
Indicates right mouse button key state.

- **alt_down** -> *bool*  
Indicates Alt key state.

- **cmd_down** -> *bool*  
Indicates Command key state.

- **ctrl_down** -> *bool*  
Indicates Control key state.

- **shift_down** -> *bool*  
Indicates Shift key state.

### <a id="MouseEnterEvt" href="#MouseEnterEvt">#</a> MouseEnterEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if mouse enters the *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MOUSE_ENTER*

### <a id="MouseLeaveEvt" href="#MouseLeaveEvt">#</a> pero.MouseLeaveEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if mouse left the *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MOUSE_LEAVE*


### <a id="MouseMotionEvt" href="#MouseMotionEvt">#</a> pero.MouseMotionEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if mouse moves inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MOUSE_MOTION*


### <a id="MouseScrollEvt" href="#MouseScrollEvt">#</a> pero.MouseScrollEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if mouse wheel rotates inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MOUSE_SCROLL*


### <a id="LeftDownEvt" href="#LeftDownEvt">#</a> pero.LeftDownEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if left-mouse button is pressed inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.LEFT_DOWN*


### <a id="LeftUpEvt" href="#LeftUpEvt">#</a> pero.LeftUpEvt(**kwargs)
**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if left-mouse button is released inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.LEFT_UP*


### <a id="LeftDClickEvt" href="#LeftDClickEvt">#</a> pero.LeftDClickEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if left-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.LEFT_DCLICK*


### <a id="MiddleDownEvt" href="#MiddleDownEvt">#</a> pero.MiddleDownEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if middle-mouse button is pressed inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MIDDLE_DOWN*


### <a id="MiddleUpEvt" href="#MiddleUpEvt">#</a> pero.MiddleUpEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if middle-mouse button is released inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MIDDLE_UP*


### <a id="MiddleDClickEvt" href="#MiddleDClickEvt">#</a> pero.MiddleDClickEvt(**kwargs)
**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if middle-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.MIDDLE_DCLICK*


### <a id="RightDownEvt" href="#RightDownEvt">#</a> pero.RightDownEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if right-mouse button is pressed inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.RIGHT_DOWN*


### <a id="RightUpEvt" href="#RightUpEvt">#</a> pero.RightUpEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if right-mouse button is released inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.RIGHT_UP*


### <a id="RightDClickEvt" href="#RightDClickEvt">#</a> pero.RightDClickEvt(**kwargs)

**Inheritance:** [Event](#Event) <- [ViewEvt](#ViewEvt) <- [MouseEvt](#MouseEvt)

Defines an event which is fired if right-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

#### Class Properties:

- **TYPE** -> *pero.RIGHT_DCLICK*