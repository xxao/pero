#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ...enums import *
from ...properties import *
from ...drawing import Circle, MarkerProperty
from ...backends import Tool
from ..enums import PLOT_TAG


class TooltipTool(Tool):
    """
    This tool shows detailed information about the nearest data point within
    reach limits from current cursor position.
    
    Properties:
        
        marker: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to highlight actual data point with. The
            value can be specified by any item from the pero.MARKER enum or
            as an pero.Marker instance.
        
        distance: int or float
            Specifies the maximum allowed distance between actual data point and
            cursor in device units.
    """
    
    marker = MarkerProperty(UNDEF, dynamic=False, nullable=True)
    distance = IntProperty(10, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of TooltipTool."""
        
        # init marker
        if 'marker' not in overrides:
            overrides['marker'] = Circle(
                size = 8,
                line_width = 9,
                line_color = "#f003",
                fill_color = "#f00c")
        
        # init base
        super().__init__(**overrides)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # check keys
        if self.keys:
            return
        
        # check buttons
        if evt.left_down or evt.right_down or evt.middle_down:
            return
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # cancel event
        if obj != PLOT_TAG:
            evt.control.draw_overlay()
            return
        
        # set cursor
        evt.control.set_cursor(CURSOR_ARROW)
        
        # draw tooltip
        evt.view.draw_overlay(self._draw_tooltip, evt=evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def _get_tooltip(self, evt):
        """Gets the nearest point tooltip."""
        
        tooltip = None
        
        # get plot
        plot = evt.control.graphics
        
        # get cursor coords
        x, y = evt.x_pos, evt.y_pos
        
        # process series
        for ser in sorted(plot.series, key=lambda s: s.z_index, reverse=True):
            
            # skip invisible
            if not ser.visible or not ser.show_tooltip:
                continue
            
            # get nearest tooltip
            tt = ser.get_tooltip(x, y, self.distance)
            if tt is None:
                continue
            
            # use better
            if tooltip is None or tooltip.z_index < tt.z_index:
                tooltip = tt
        
        return tooltip
    
    
    def _draw_tooltip(self, canvas, evt):
        """Draws nearest point tooltip."""
        
        # get tooltip
        tooltip = self._get_tooltip(evt)
        if not tooltip:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get plot frame
        frame = plot.get_frame(PLOT_TAG)
        
        # draw marker
        if self.marker:
            self.marker.draw(canvas, x=tooltip.x, y=tooltip.y)
        
        # draw tooltip
        tooltip.draw(canvas, clip=frame)
