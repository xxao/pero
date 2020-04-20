#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import time
from ..backends import Control
from ..enums import *
from ..properties import *
from .tools import *
from .plot import Plot


class PlotControl(Control):
    """
    Abstract base class for plot views providing several convenient methods to
    apply zoom to specific axis, enable zoom undos and sets default
    interactivity tools.
    
    Properties:
        
        zoom_undo: int
            Specifies the number of zoom undoes to be stored.
        
        zoom_wait: float
            Specifies the minimum time in seconds between zoom events to save
            the new range for undo. The is mainly intended to ignore scrolling
            steps.
    """
    
    graphics = Property(None, types=Plot, dynamic=False, nullable=True)
    
    zoom_undo = IntProperty(256, dynamic=False, nullable=False)
    zoom_wait = FloatProperty(0.5, dynamic=False, nullable=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of PlotControl."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._zoom_ranges = []
        self._zoom_time = 0
        
        # save current zoom
        self.save_zoom()
        
        # bind events
        self.bind(EVT_ZOOM, self.on_zoom)
        self.bind(EVT_PROPERTY_CHANGED, self._on_plotcontrol_property_changed)
        
        # init main tool
        if self.main_tool is UNDEF:
            self.main_tool = NavigatorTool()
        
        # init cursor tool
        if self.cursor_tool is UNDEF:
            self.cursor_tool = TooltipTool()
        
        # init left tool
        if self.left_tool is UNDEF:
            self.left_tool = ZoomTool()
        
        # init right tool
        if self.right_tool is UNDEF:
            self.right_tool = MeasureTool()
    
    
    def on_zoom(self, evt):
        """Handles zoom event."""
        
        # save current zoom
        self.save_zoom()
        
        # redraw plot
        self.refresh()
    
    
    def zoom(self, axis_tag=None, minimum=None, maximum=None, save=True):
        """
        Sets given range to specific plot axis.
        
        If 'axis_tag' is set to None, given range will be applied to all axes.
        This make only sense if minimum and maximum are both set to None, so all
        the axes will be set to cover full range of connected data series.
        
        If minimum or maximum is set to None, the value will be set by maximum
        or minimum value to cover full range of connected data series.
        
        Note that this method does not fire the pero.EVENT.ZOOM event
        automatically. It must be done manually if required.
        
        Args:
            axis_tag: str or None
                Unique tag of the axis to be zoomed.
            
            minimum: float or None
                Minimum value to be set.
            
            maximum: float or None
                Maximum value to be set.
            
            save: bool
                If set to True the new zoom state is saved.
        """
        
        # check plot
        if not self.graphics:
            return
        
        # set zoom
        self.graphics.zoom(axis_tag, minimum, maximum)
        
        # save current zoom
        if save:
            self.save_zoom()
    
    
    def zoom_back(self):
        """
        Applies previous plot axes ranges.
        
        Note that this method does not fire the pero.EVENT.ZOOM event
        automatically. It must be done manually if required.
        """
        
        # check plot
        if not self.graphics:
            return
        
        # check zooms
        if not self._zoom_ranges:
            return
        
        # remove latest (current) if not last
        if len(self._zoom_ranges) > 1:
            del self._zoom_ranges[-1]
        
        # set ranges
        for tag, in_range in self._zoom_ranges[-1].items():
            axis = self.graphics.get_obj(tag)
            if axis is not None:
                axis.scale.in_range = in_range
    
    
    def save_zoom(self):
        """Remembers current axes ranges."""
        
        # check plot
        if not self.graphics:
            return
        
        # get current ranges
        ranges = {}
        for axis in self.graphics.axes:
            ranges[axis.tag] = axis.scale.in_range
        
        # check last zoom
        if self._zoom_ranges:
            
            # check same ranges
            if self._zoom_ranges[-1] == ranges:
                return
            
            # remove last if too recent (probably scrolling)
            if (time.time() - self._zoom_time) < self.zoom_wait:
                del self._zoom_ranges[-1]
        
        # save current ranges
        self._zoom_ranges.append(ranges)
        if len(self._zoom_ranges) > self.zoom_undo:
            del self._zoom_ranges[0]
        
        # save time stamp
        self._zoom_time = time.time()
    
    
    def _on_plotcontrol_property_changed(self, evt):
        """Called after any property has changed."""
        
        # plot changed
        if evt.name == 'graphics':
            
            # reset zoom memory
            self._zoom_ranges = []
            self._zoom_time = 0
            
            # save current zoom
            if self.graphics:
                self.save_zoom()
