#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import ui
from objc_util import ObjCInstance
from ... events import *
from .. view import View
from . enums import *
from . canvas import UICanvas


class UIView(ui.View, View):
    """Wrapper for UI View."""
    
    
    def __init__(self):
        """Initializes a new instance of UIView."""
        
        # init base
        super(UIView, self).__init__()
        View.__init__(self)
        
        # init buffers
        self._dc_buffer = None
        self._dc_overlay = None
    
    
    def draw_control(self):
        """Draws current control graphics."""
        
        # draw on buffer
        with ui.ImageContext(self.width, self.height) as ctx:
            
            # draw control
            if self.control is not None:
                canvas = UICanvas(width=self.width, height=self.height)
                self.control.draw(canvas)
            
            # get image
            self._dc_buffer = ctx.get_image()
        
        # reset overlay
        self._dc_overlay = None
        
        # update screen
        self.set_needs_display()
    
    
    def draw_overlay(self, func=None, **kwargs):
        """
        Draws cursor rubber band overlay.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given overrides (i.e. func(canvas, **kwargs)).
        If the 'func' parameter is set to None current overlay is cleared.
        
        Args:
            func: callable or None
                Drawing function to be called to draw the overlay. If set to
                None, current overlay will be cleared.
                
            kwargs: str:any pairs
                Keyword arguments, which should be provided to the given drawing
                function.
        """
        
        # skip cleaning if empty already
        if func is None and self._dc_overlay is None:
            return
        
        # just clean
        if func is None:
            self._dc_overlay = None
            self.set_needs_display()
            return
        
        # draw on overlay
        with ui.ImageContext(self.width, self.height) as ctx:
            
            # draw overlay
            canvas = UICanvas(width=self.width, height=self.height)
            func(canvas, **kwargs)
            
            # get image
            self._dc_overlay = ctx.get_image()
        
        # update screen
        self.set_needs_display()
    
    
    def layout(self):
        """Called when view is resized."""
        
        # make size event
        size_evt = SizeEvt(
            
            native = None,
            view = self,
            control = self.control,
            
            width = self.width,
            height = self.height)
        
        # fire event
        if self.control is not None:
            self.control.fire(size_evt)
    
    
    def draw(self):
        """Draws the view."""
        
        # draw buffer
        if self._dc_buffer is not None:
            self._dc_buffer.draw(0, 0, self.width, self.height)
        
        # draw overlay
        if self._dc_overlay is not None:
            self._dc_overlay.draw(0, 0, self.width, self.height)
    
    
    def touch_began(self, touch):
        """Called when a touch event begins."""
        
        self._on_touch(touch)
    
    
    def touch_ended(self, touch):
        """Called when a touch event ends."""
    
        self._on_touch(touch)
    
    
    def touch_moved(self, touch):
        """Called when a touch event moves."""
        
        self._on_touch(touch)
    
    
    def _on_touch(self, touch):
        """Handles all touch events."""
        
        # get point
        point = Touch(
            id = touch.touch_id,
            x_pos = touch.location[0],
            y_pos = touch.location[1],
            x_prev = touch.prev_location[0],
            y_prev = touch.prev_location[1],
            force = ObjCInstance(touch).force(),
            state = UI_TOUCH_STATE[touch.phase])
        
        # init base event
        touch_evt = TouchEvt(
            
            native = touch,
            view = self,
            control = self.control,
            
            touches = [point],
            
            alt_down = False,
            cmd_down = False,
            ctrl_down = False,
            shift_down = False)
        
        # make specific event type
        if touch.phase == 'began':
            touch_evt = TouchStartEvt.from_evt(touch_evt)
        
        elif touch.phase == 'ended':
            touch_evt = TouchEndEvt.from_evt(touch_evt)
        
        elif touch.phase == 'moved':
            touch_evt = TouchMoveEvt.from_evt(touch_evt)
        
        elif touch.phase == 'cancelled':
            touch_evt = TouchCancelEvt.from_evt(touch_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(touch_evt)
