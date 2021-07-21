#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . proxy import Proxy
from . event import Event


class EvtHandler(object):
    """
    This class represents an event raising base class, to which specific
    callbacks can be attached to be called when appropriate event is fired.
    When a specific event is fired, bound callbacks are called in reversed
    order, so the last added callback will be called first. Calling of
    registered callbacks continues until all are called or until one of them
    cancels the event by calling the 'cancel' method.
    """
    
    
    def __init__(self):
        """Initializes a new instance of EvtHandler."""
        
        self._callbacks = {}
    
    
    def bind(self, evt_type, callback, **kwargs):
        """
        Registers given callback for specific event. Additional keyword
        arguments can be specified to be always provided when the event is
        fired. These arguments will be used as defaults but they can be
        overridden by the same argument provided directly to the 'fire' method.
        
        Args:
            evt_type: str or pero.Event
                Specific event type to which the callback should be attached.
            
            callback: callable
                Callback to be called when event is fired.
            
            kwargs: str:any pairs
                Additional keyword arguments.
        """
        
        # get event type
        evt_type = self._get_evt_type(evt_type)
        
        # register event
        if evt_type not in self._callbacks:
            self._callbacks[evt_type] = []
        
        # init proxy
        proxy = Proxy(callback)
        
        # add callback
        self._callbacks[evt_type].append((proxy, kwargs))
    
    
    def unbind(self, evt_type, callback, **kwargs):
        """
        Removes given callback if registered for specified event. If additional
        keyword arguments are provided, they must match exactly all the
        arguments provided when the callback was attached. If not provided,
        just the callback must match.
        
        Args:
            evt_type: str or pero.Event
                Specific event type to which the callback was attached.
            
            callback: callable
                Callback to be removed.
            
            kwargs: str:any pairs
                Additional keyword arguments.
        
        Returns:
            bool
                Returns True if any callback was removed, False otherwise.
        """
        
        removed = False
        
        # get event type
        evt_type = self._get_evt_type(evt_type)
        
        # get callbacks
        callbacks = self._callbacks.get(evt_type, None)
        if not callbacks:
            return removed
        
        # init proxy
        proxy = Proxy(callback)
        
        # remove matching callback
        for item in callbacks[:]:
            
            if item[0] != proxy:
                continue
            
            if kwargs and item[0] != kwargs:
                continue
            
            callbacks.remove(item)
            removed = True
        
        return removed
    
    
    def fire(self, evt, **kwargs):
        """
        Fires given event by calling all registered callbacks with given params.
        When a specific event is fired, bound callbacks are called in reversed
        order, so the last added callback will be called first. Calling of
        registered callbacks continues until all are called or until
        one of them cancels the event by calling 'cancel' method.
        
        Args:
            evt: pero.Event
                Event instance which should be processed.
            
            kwargs: str:any pairs
                Additional keyword arguments.
        """
        
        # get callbacks
        callbacks = self._callbacks.get(evt.TYPE, None)
        if not callbacks:
            return
        
        # call callbacks
        for callback, params in reversed(callbacks):
            
            # get params
            params = dict(params, **kwargs)
            
            # call callback
            callback(evt, **params)
            
            # check if canceled
            if evt.is_canceled():
                return
    
    
    def _get_evt_type(self, evt):
        """Gets event type."""
        
        if type(evt) == str:
            return evt
        
        if isinstance(evt, Event):
            return evt.TYPE
        
        if issubclass(evt, Event):
            return evt.TYPE
