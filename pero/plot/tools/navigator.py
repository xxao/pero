#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import sys
from ...enums import *
from ...properties import *
from ...events import ZoomEvt
from ...backends import Tool
from ..enums import PLOT_TAG
from ..axes import Axis

# init events
_EVT_SHIFT = 'shift'
_EVT_SCALE = 'scale'
_EVT_PAN = 'pan'


class NavigatorTool(Tool):
    """
    This tool provides various ways to navigate within plot data by mouse
    scrolling or dragging or using keyboard.
    
    Properties:
        
        reverse_scroll: bool
            Specifies whether the scroll direction should be reversed.
        
        reverse_move: bool
            Specifies whether the keyboard move direction should be reversed.
        
        scroll_factor: float
            Specifies the relative scrolling step.
        
        scale_factor: float
            Specifies the relative scaling multiplier.
        
        move_factor: float
            Specifies the relative keyboard moving step.
    """
    
    reverse_scroll = BoolProperty(UNDEF, dynamic=False)
    reverse_move = BoolProperty(UNDEF, dynamic=False)
    scroll_factor = RangeProperty(UNDEF, minimum=0, maximum=1, dynamic=False)
    scale_factor = RangeProperty(UNDEF, minimum=0, maximum=1, dynamic=False)
    move_factor = RangeProperty(0.1, minimum=0, maximum=1, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of NavigatorTool."""
        
        # init scrolling
        if 'reverse_scroll' not in overrides:
            overrides['reverse_scroll'] = sys.platform == 'darwin'
        
        if 'scroll_factor' not in overrides:
            overrides['scroll_factor'] = 0.02 if sys.platform == 'darwin' else 0.05
        
        if 'scale_factor' not in overrides:
            overrides['scale_factor'] = 0.02 if sys.platform == 'darwin' else 0.05
        
        # init base
        super().__init__(**overrides)
        
        # init buffers
        self._event = None
        self._event_obj = None
        self._dragging = None
    
    
    def on_key_down(self, evt):
        """Handles key-down event."""
        
        # remember key
        self.add_key(evt.key)
        
        # escape current event
        if evt.key == KEY_ESC:
            self._escape_event(evt)
            evt.cancel()
            return
        
        # escape if active
        if self._event:
            evt.cancel()
            return
        
        # check control
        if not evt.control:
            return
        
        # shift axes
        if evt.key in (KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN):
            self._shift_axes_by_key(evt)
        
        # nothing to handle
        else:
            return
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_leave(self, evt):
        """Handles mouse-leave event."""
        
        # clear keys
        self.clear_keys()
        
        # check if active
        if not self._event:
            return
        
        # cancel current tool event
        self._escape_event(evt)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # no event set
        if not self._event:
            self._set_cursor_by_location(evt)
            return
        
        # shift axes
        if self._event == _EVT_SHIFT:
            self._shift_axes_by_dragging(evt, self._event_obj)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # pan axes
        elif self._event == _EVT_PAN and KEY_SPACE in self.keys:
            self._shift_axes_by_dragging(evt, self._event_obj)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # scale axes
        elif self._event == _EVT_SCALE:
            self._scale_axes_by_dragging(evt, self._event_obj)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_scroll(self, evt):
        """Handles mouse-scroll wheel event."""
        
        # cancel event if active
        if self._event:
            evt.cancel()
            return
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # check location
        if obj != PLOT_TAG and not isinstance(obj, Axis):
            return
        
        # check rotation
        rotation = evt.y_rot or evt.x_rot
        if not rotation:
            return
        
        # get scroll direction
        direction = -1 if rotation < 0 else 1
        if self.reverse_scroll:
            direction *= -1
        
        # scale axes from cursor position
        if evt.alt_down or evt.ctrl_down:
            self._scale_axes_by_scrolling(evt, obj, direction, True)
        
        # scale current or secondary axes
        elif evt.shift_down:
            self._scale_axes_by_scrolling(evt, obj, direction, False)
        
        # shift current or primary axes
        else:
            self._shift_axes_by_scrolling(evt, obj, direction)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_down(self, evt):
        """Handles mouse-button-down event."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # check location
        if obj != PLOT_TAG and not isinstance(obj, Axis):
            return
        
        # remember dragging origin
        self._dragging = (evt.x_pos, evt.y_pos)
        
        # start axis shift
        if isinstance(obj, Axis) and evt.left_down:
            self._event = _EVT_SHIFT
            self._event_obj = obj
        
        # start axis scale
        elif isinstance(obj, Axis) and evt.right_down:
            self._event = _EVT_SCALE
            self._event_obj = obj
        
        # pan axes
        elif KEY_SPACE in self.keys and evt.left_down:
            self._event = _EVT_PAN
            self._event_obj = PLOT_TAG
            evt.control.set_cursor(CURSOR_HAND)
        
        # no event to start
        else:
            return
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # check if active
        if not self._event:
            return
        
        # cancel event
        self._escape_event(evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_dclick(self, evt):
        """Handles mouse-button-double-click event."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # check location
        if obj != PLOT_TAG and not isinstance(obj, Axis):
            return
        
        # set full range on axes
        self._scale_axes_full(evt, obj)
        
        # stop event propagation
        evt.cancel()
    
    
    def _set_cursor_by_location(self, evt):
        """Sets cursor according to position within plot."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # set standard cursor for non-axis objects
        if not isinstance(obj, Axis):
            evt.control.set_cursor(CURSOR_ARROW)
            return
        
        # check if interactive
        if obj.static:
            evt.control.set_cursor(CURSOR_ARROW)
            return
        
        # use arrows on interactive axes
        if obj.position in (POS_LEFT, POS_RIGHT):
            evt.control.set_cursor(CURSOR_SIZENS)
        
        elif obj.position in (POS_TOP, POS_BOTTOM):
            evt.control.set_cursor(CURSOR_SIZEWE)
    
    
    def _escape_event(self, evt):
        """Cancels current tool event."""
        
        # cancel current event
        self._event = None
        self._event_obj = None
        
        # reset dragging origin
        self._dragging = None
        
        # clear overlay
        if evt.control:
            evt.control.set_cursor(CURSOR_ARROW)
            evt.control.draw_overlay()
    
    
    def _shift_axes_by_scrolling(self, evt, obj, direction):
        """Shifts axes by mouse scrolling."""
        
        # check control
        if not evt.control:
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # use selected axis
        if isinstance(obj, Axis):
            axes.append(obj)
        
        # get all primary axes
        else:
            axes = [a for a in plot.axes if a.level == 1]
        
        # remove static axes
        axes = [a for a in axes if not a.static]
        if not axes:
            return
        
        # get factor
        factor = self.scroll_factor * direction
        
        # shift axes
        for axis in axes:
            
            # skip symmetric axis
            if axis.symmetric:
                continue
            
            # get shift
            start, end = axis.scale.out_range
            shift = (start - end) * factor
            start += shift
            end += shift
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _shift_axes_by_dragging(self, evt, obj):
        """Shifts axes by mouse dragging."""
        
        # check control
        if not evt.control:
            return
        
        # check dragging
        if self._dragging is None:
            self._dragging = (evt.x_pos, evt.y_pos)
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # use selected axis
        if isinstance(obj, Axis):
            axes.append(obj)
        
        # get all axes
        elif obj == PLOT_TAG:
            axes = [a for a in plot.axes if a.level <= 2]
        
        # remove static axes
        axes = [a for a in axes if not a.static]
        if not axes:
            return
        
        # shift axes
        for axis in axes:
            
            # skip symmetric axis
            if axis.symmetric:
                continue
            
            # get cursors
            if axis.position in (POS_BOTTOM, POS_TOP):
                drag = self._dragging[0]
                cursor = evt.x_pos
            else:
                drag = self._dragging[1]
                cursor = evt.y_pos
            
            # get shift
            start, end = axis.scale.out_range
            shift = drag - cursor
            start += shift
            end += shift
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _shift_axes_by_key(self, evt):
        """Shifts axes by keys."""
        
        # check control
        if not evt.control:
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # get horizontal axes
        if evt.key in (KEY_LEFT, KEY_RIGHT):
            axes += [a for a in plot.axes if a.position in (POS_BOTTOM, POS_TOP)]
        
        # get vertical axes
        elif evt.key in (KEY_UP, KEY_DOWN):
            axes += [a for a in plot.axes if a.position in (POS_LEFT, POS_RIGHT)]
        
        # remove static axes
        axes = [a for a in axes if not a.static and a.level <= 2]
        if not axes:
            return
        
        # get direction
        direction = -1 if evt.key in (KEY_RIGHT, KEY_UP) else 1
        if self.reverse_move:
            direction *= -1
        
        # get factor
        factor = self.move_factor * direction
        
        # shift axes
        for axis in axes:
            
            # skip symmetric axes
            if axis.symmetric:
                continue
            
            # get shift
            start, end = axis.scale.out_range
            shift = (start - end) * factor
            start += shift
            end += shift
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _scale_axes_by_scrolling(self, evt, obj, direction, from_cursor):
        """Scales axes by mouse scrolling."""
        
        # check control
        if not evt.control:
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # use selected axis
        if isinstance(obj, Axis):
            axes.append(obj)
        
        # get all axes
        elif obj == PLOT_TAG and from_cursor:
            axes = [a for a in plot.axes if a.level <= 2]
        
        # get secondary axes
        else:
            axes = [a for a in plot.axes if a.level == 2]
        
        # remove static axes
        axes = [a for a in axes if not a.static]
        if not axes:
            return
        
        # get factor
        factor = - self.scale_factor * direction
        
        # scale axes
        for axis in axes:
            
            # get current range
            start, end = axis.scale.out_range
            
            # scale symmetric
            if axis.symmetric:
                end += (end - start) * factor
                start = axis.scale.scale(-axis.scale.invert(end))
            
            # scale from cursor
            elif from_cursor:
                
                # get cursor position
                if axis.position in (POS_BOTTOM, POS_TOP):
                    cursor = evt.x_pos
                else:
                    cursor = evt.y_pos
                
                # get ratio
                ratio = abs((cursor - start) / (end - start))
                
                # apply scaling
                shift = (end - start) * factor
                start -= shift * ratio
                end += shift * (1-ratio)
            
            # scale from start
            else:
                end += (start - end) * factor
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _scale_axes_by_dragging(self, evt, obj):
        """Scales axes by mouse dragging."""
        
        # check control
        if not evt.control:
            return
        
        # check dragging
        if self._dragging is None:
            self._dragging = (evt.x_pos, evt.y_pos)
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # use selected axis
        if isinstance(obj, Axis):
            axes.append(obj)
        
        # get all axes
        elif obj == PLOT_TAG:
            axes = [a for a in plot.axes]
        
        # remove static axes
        axes = [a for a in axes if not a.static]
        if not axes:
            return
        
        # scale axes
        for axis in axes:
            
            # get cursors
            if axis.position in (POS_BOTTOM, POS_TOP):
                drag = self._dragging[0]
                cursor = evt.x_pos
            else:
                drag = self._dragging[1]
                cursor = evt.y_pos
            
            # get shift
            start, end = axis.scale.out_range
            shift = drag - cursor
            end += shift
            start = -end if axis.symmetric else start
            
            # scale start also
            if axis.symmetric:
                start = axis.scale.scale(-axis.scale.invert(end))
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _scale_axes_full(self, evt, obj):
        """Scales axes to full range."""
        
        # check control
        if not evt.control:
            return
        
        # get axes
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # use selected axis
        if isinstance(obj, Axis):
            axes.append(obj)
        
        # get all axes
        elif obj == PLOT_TAG:
            axes = plot.axes
        
        # remove static axes
        axes = [a for a in axes if not a.static]
        if not axes:
            return
        
        # sort axes by level
        axes.sort(key=lambda a: a.level)
        
        # scale axes
        for axis in axes:
            start, end = plot.get_series_limits(axis.tag, exact=False)
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
