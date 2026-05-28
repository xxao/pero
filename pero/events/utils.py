#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .mouse import *


def is_mouse_click_evt(evt, history, latency=0.3):
    """
    Checks if given event is mouse click.
    
    Args:
        evt: pero.Event
            Event to be checked.
        
        history: (pero.Event, )
            List of previous events.
        
        latency: float
            Maximum time in seconds between mouse down and up events.
    
    Returns:
        bool
             True if given event is mouse click, False otherwise.
    """
    
    # check type
    if not isinstance(evt, (LeftUpEvt, MiddleUpEvt, RightUpEvt)):
        return False
    
    # check history
    if not history:
        return False
    
    # get previous event
    last = history[-1]
    
    # check last event
    if not isinstance(last, (LeftDownEvt, MiddleDownEvt, RightDownEvt)):
        return False
    
    # check position
    if evt.x_raw != last.x_raw or evt.y_raw != last.y_raw:
        return False
    
    # check same button
    if isinstance(evt, LeftUpEvt) != isinstance(last, LeftDownEvt):
        return False
    if isinstance(evt, MiddleUpEvt) != isinstance(last, MiddleDownEvt):
        return False
    if isinstance(evt, RightUpEvt) != isinstance(last, RightDownEvt):
        return False
    
    # check time
    if evt.time - last.time > latency:
        return False
    
    return True
