# Events


### pero.Event(**kwargs)
Abstract base class for various types of events. Each derived event class has to specify its unique *TYPE* property at
least.


#### Class Properties:

##### TYPE -> str
Specifies the event type.


#### Methods:

##### cancel()
Sets current event as canceled to prevent following subscribers to be called.

##### resume()
Sets current event as not canceled to allow following subscribers to be called.

##### is_canceled() -> *bool*
Returns True if the event has been canceled, False otherwise.


## Property Events


### PropertyChangedEvt(**kwargs)
Defines an event which is fired if any property of a *[pero.PropertySet](../properties/propset.md)* was changed.

TYPE = pero.PROPERTY_CHANGED

#### Attributes:

##### name -> *str*
Gets the name of the changed property.

##### old_value -> *any*
Gets the original value of the changed property.

##### new_value -> *any*
Gets the new value of the changed property.


### PenChangedEvt(**kwargs)
    Inheritance: [pero.PropertyChangedEvt](../events/event.md)

Defines an event which is fired if any pen-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

TYPE = pero.PEN_CHANGED


### BrushChangedEvt(**kwargs)
    Inheritance: [pero.PropertyChangedEvt](../events/event.md)

Defines an event which is fired if any brush-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

TYPE = pero.BRUSH_CHANGED


### TextChangedEvt(**kwargs)
    Inheritance: [pero.PropertyChangedEvt](../events/event.md)

Defines an event which is fired if any text-related property of *[pro.Canvas](../drawing/canvas.md)* was changed.

TYPE = pero.TEXT_CHANGED


## View Events


### ViewEvt(**kwargs)
    Inheritance: [pero.Event](../events/event.md)

Abstract base class for various types of *[pero.View](../backends/view.md)* events.

#### Attributes:

##### native -> *any*
Native event fired by the view.

##### view -> *[pero.View](../backends/view.md)*
The view, which fires the event.

##### graphics -> *[pero.Graphics](../drawing/graphics.md)*
The view main graphics object.


### SizeEvt(**kwargs)
    Inheritance: [pero.ViewEvt](../events/event.md)

Defines an event which is fired if *[pero.View](../backends/view.md)* size was changed.

TYPE = pero.SIZE

#### Attributes:

##### width -> *int*
New width of the view.

##### height -> *int*
New height of the view.


### KeyEvt(**kwargs)
    Inheritance: [pero.ViewEvt](../events/event.md)

Defines a generic event which is fired on any key-related event of *[pero.View](../backends/view.md)*.

TYPE = pero.KEY

#### Attributes:

##### key -> *int*
Key code.

##### char -> *str*
Character string or None if not character.

##### pressed -> *bool*
Indicates the key pressed state.

##### alt_down -> *bool*
Indicates Alt key state.

##### cmd_down -> *bool*
Indicates Command key state.

##### ctrl_down -> *bool*
Indicates Control key state.

##### shift_down -> *bool*
Indicates Shift key state.


### KeyDownEvt(**kwargs)
    Inheritance: [pero.KeyEvt](../events/event.md)

Defines an event which is fired if a key is pressed inside *[pero.View](../backends/view.md)*.

TYPE = pero.KEY_DOWN


### KeyUpEvt(**kwargs)
    Inheritance: [pero.KeyEvt](../events/event.md)

Defines an event which is fired if a key is released inside *[pero.View](../backends/view.md)*.

TYPE = pero.KEY_UP


### MouseEvt(**kwargs)
    Inheritance: [pero.ViewEvt](../events/event.md)

Defines a generic event which is fired on any mouse-related event of *[pero.View](../backends/view.md)*.

TYPE = pero.MOUSE

#### Attributes:

##### x_pos -> *float*
Cursor x-coordinate in device units.

##### y_pos -> *float*
Cursor y-coordinate in device units.

##### x_rot -> *float*
Mouse wheel rotation in x-direction.

##### y_rot -> *float*
Mouse wheel rotation in y-direction.

##### left_down -> *bool*
Indicates left mouse button key state.

##### middle_down -> *bool*
Indicates middle mouse button key state.

##### right_down -> *bool*
Indicates right mouse button key state.

##### alt_down -> *bool*
Indicates Alt key state.

##### cmd_down -> *bool*
Indicates Command key state.

##### ctrl_down -> *bool*
Indicates Control key state.

##### shift_down -> *bool*
Indicates Shift key state.


### MouseEnterEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if mouse enters the *[pero.View](../backends/view.md)*.

TYPE = pero.MOUSE_ENTER


### MouseLeaveEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if mouse left the *[pero.View](../backends/view.md)*.

TYPE = pero.MOUSE_LEAVE


### MouseMotionEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if mouse moves inside *[pero.View](../backends/view.md)*.

TYPE = pero.MOUSE_MOTION


### MouseScrollEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if mouse wheel rotates inside *[pero.View](../backends/view.md)*.

TYPE = pero.MOUSE_SCROLL


### LeftDownEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if left-mouse button is pressed inside *[pero.View](../backends/view.md)*.

TYPE = pero.LEFT_DOWN


### LeftUpEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if left-mouse button is released inside *[pero.View](../backends/view.md)*.

TYPE = pero.LEFT_UP


### LeftDClickEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if left-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

TYPE = pero.LEFT_DCLICK


### MiddleDownEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if middle-mouse button is pressed inside *[pero.View](../backends/view.md)*.

TYPE = pero.MIDDLE_DOWN


### MiddleUpEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if middle-mouse button is released inside *[pero.View](../backends/view.md)*.

TYPE = pero.MIDDLE_UP


### MiddleDClickEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if middle-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

TYPE = pero.MIDDLE_DCLICK


### RightDownEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if right-mouse button is pressed inside *[pero.View](../backends/view.md)*.

TYPE = pero.RIGHT_DOWN


### RightUpEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if right-mouse button is released inside *[pero.View](../backends/view.md)*.

TYPE = pero.RIGHT_UP


### RightDClickEvt(**kwargs)
    Inheritance: [pero.MouseEvt](../events/event.md)

Defines an event which is fired if right-mouse button is double-clicked inside *[pero.View](../backends/view.md)*.

TYPE = pero.RIGHT_DCLICK