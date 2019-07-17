# pero.EvtHandler()

This class represents an event raising base class, to which specific callbacks can be attached to be called when
appropriate *[pero.Event](event.md)* is fired. When a specific event is fired, bound callbacks are called in reversed
order, so the last added callback will be called first. Calling of registered callbacks continues until all are called
or until one of them cancels the event by calling the *cancel* method.


## Methods


### bind(evt_type, callback, **kwargs)
Registers given callback for specific event. Additional keyword arguments can be specified to be always provided when
the event is fired. These arguments will be used as defaults but they can be overridden by the same argument provided
directly to the *fire* method.

- **evt_type:** *str* or *[pero.Event](event.md)*  
  Specific event type to which the callback should be attached.

- **callback:** *callable*  
  Callback to be called when event is fired.

- **kwargs:** *{str, any}*  
  Specific keyword arguments.


### unbind(evt_type, callback, **kwargs)
Removes given callback if registered for specified event. If additional keyword arguments are provided, they must match
exactly all the arguments provided when the callback was attached. If not provided, just the callback must match.

- **evt_type:** *str* or *[pero.Event](event.md)*  
  Specific event type to which the callback was attached.

- **callback:** *callable*  
  Callback to be removed.

- **kwargs:** *{str, any}*  
  Specific keyword arguments.


### fire(evt, callback, **kwargs)
Fires given event by calling all registered callbacks with given params. When a specific event is fired, bound callbacks
are called in reversed order, so the last added callback will be called first. Calling of registered callbacks continues
until all are called or until one of them cancels the event by calling *cancel* method.

- **evt:** *str* or *[pero.Event](event.md)*  
  Event instance which should be processed.

- **kwargs:** *{str, any}*  
  Specific keyword arguments.
