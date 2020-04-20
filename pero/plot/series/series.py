#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...properties import *
from ...scales import Scale, ContinuousScale, LinScale
from ...drawing import Legend, MarkerLegend
from ...drawing import Label, TextLabel
from ...drawing import Tooltip, TextTooltip
from ..graphics import InGraphics
from . import helpers


class Series(InGraphics):
    """
    Abstract base class for various types of plot data series. Besides others,
    it defines the main data mappers and scales. The scales are used to convert
    coordinates from real data units into device coordinates. The mappers are
    mainly used to internally convert original categorical data into a sequence
    of continuous numbers to enable plot zooming and panning. The mappers are
    applied upon series initialization within data extraction, while the scales
    are applied upon series drawing and limits calculation.
    
    Properties:
    
        show_legend: bool
            Specifies whether the legend should be shown.
        
        show_labels: bool
            Specifies whether the labels should be shown.
        
        show_tooltip: bool
            Specifies whether the points tooltip should be shown.
        
        x_scale: pero.ContinuousScale
            Specifies the scale to be used to convert x-coordinates from real
            data units into device coordinates.
        
        y_scale: pero.ContinuousScale
            Specifies the scale to be used to convert y-coordinates from real
            data units into device coordinates.
        
        x_mapper: pero.Scale, None or UNDEF
            Specifies the additional scale to initially map categorical
            x-coordinates values into continuous range.
        
        y_mapper : pero.Scale, None or UNDEF
            Specifies the additional scale to initially map categorical
            y-coordinates values into continuous range.
        
        frame: pero.Frame, None or UNDEF
            Specifies the frame used to hide the data points outside the main
            plot area.
        
        margin: int, float or tuple
            Specifies the relative extend of the full real data ranges as a
            single value or values for individual sides starting from top as
            %/100.
        
        color: pero.Color, tuple, str
            Specifies the main series color as an RGB or RGBA tuple, hex code,
            name or pero.Color.
        
        title: str, None or UNDEF
            Specifies the title to be shown as legend.
        
        legend: pero.Legend, None or UNDEF
            Specifies the explicit value for the legend or a template to create
            it. When the actual legend is initialized, current series is
            provided as a source, therefore properties can be dynamic to
            retrieve the final value from the series.
        
        label: pero.Label, None or UNDEF
            Specifies a template to create points labels. When the actual label
            is initialized, current data point is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the point.
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies a template to create points tooltips. When the actual
            tooltip is initialized, current data point is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the point.
    """
    
    show_legend = BoolProperty(True, dynamic=False)
    show_labels = BoolProperty(UNDEF, dynamic=False)
    show_tooltip = BoolProperty(True, dynamic=False)
    
    x_scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    y_scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    
    x_mapper = Property(UNDEF, types=(Scale,), dynamic=False, nullable=True)
    y_mapper = Property(UNDEF, types=(Scale,), dynamic=False, nullable=True)
    
    margin = QuadProperty(0.05, dynamic=False)
    color = ColorProperty(UNDEF, dynamic=False)
    
    title = StringProperty(UNDEF, dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(Legend,), dynamic=False, nullable=True)
    label = Property(UNDEF, types=(Label,), dynamic=False, nullable=True)
    tooltip = Property(UNDEF, types=(Tooltip,), dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Series."""
        
        # init scales
        if 'x_scale' not in overrides:
            overrides['x_scale'] = LinScale()
        
        if 'y_scale' not in overrides:
            overrides['y_scale'] = LinScale()
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = MarkerLegend(
                text = lambda d: self.title,
                marker = 'o',
                marker_size = 8,
                marker_line_color = lambda d: self.color.darker(0.2),
                marker_fill_color = lambda d: self.color)
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: str(d),
                y_offset = -4)
        
        # init tooltip
        if 'tooltip' not in overrides:
            overrides['tooltip'] = TextTooltip(
                text = lambda d: str(d))
        
        # init base
        super().__init__(**overrides)
        
        # lock properties
        self.lock_property('x_mapper')
        self.lock_property('y_mapper')
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """
        Gets current data limits using whole range or specified crops.
        
        Args:
            x_range: (float, float) or None
                X-range limits.
            
            y_range: (float, float) or None
                Y-range limits.
            
            exact: bool
                If set to True, any additional space like margin is ignored.
        
        Returns:
            ((float,float),)
                Data limits as sequence of (min, max) for each dimension.
        """
        
        raise NotImplementedError(
            "The 'get_limits' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def get_legend(self):
        """
        Gets series legend item.
        
        Returns:
            pero.Legend or None
                Series legend item.
        """
        
        # check legend
        if not self.show_legend or not self.legend:
            return None
        
        # init legend
        legend = self.legend.clone(source=self)
        
        # set title
        if legend.text is UNDEF:
            legend.text = self.title
        
        return legend
    
    
    def get_labels(self):
        """
        Gets series labels.
        
        Returns:
            (pero.Label,)
                Series labels.
        """
        
        return []
    
    
    def get_tooltip(self, x, y, limit):
        """
        Gets nearest data point tooltip.
        
        Args:
            x: int or float
                Cursor x-coordinate in device units.
            
            y: int or float
                Cursor y-coordinate in device units.
            
            limit: int or float
                Maximum allowed distance in device units.
        
        Returns:
            tooltip: pero.Tooltip or None
                Tooltip item.
        """
        
        return None
    
    
    def make_labels(self, x_data, y_data, raw_data):
        """
        Prepares labels for given data range.
        
        Args:
            x_data: 1D numpy.ndarray
                X-coordinate data.
            
            y_data: 1D numpy.ndarray
                Y-coordinate data.
            
            raw_data: 1D numpy.ndarray
                Original data points.
        
        Returns:
            (pero.Label,)
                Labels for given data.
        """
        
        labels = []
        
        # check label
        if not self.show_labels or not self.label:
            return labels
        
        # crop data
        x_data, y_data, raw_data = helpers.crop_points(
            data = (x_data, y_data, raw_data),
            crops = (self.x_scale.in_range, self.y_scale.in_range),
            extend = False)
        
        # check data
        if len(raw_data) == 0:
            return labels
        
        # scale coords
        x_data = self.x_scale.scale(x_data)
        y_data = self.y_scale.scale(y_data)
        
        # create labels
        for i in range(len(raw_data)):
            overrides = {'x': x_data[i], 'y': y_data[i]}
            labels.append(self.label.clone(raw_data[i], overrides))
        
        return labels
    
    
    def make_tooltip(self, x_data, y_data, raw_data, x, y, limit):
        """
        Prepares nearest data point tooltip within limits from cursor position.
        
        Args:
            x_data: 1D numpy.ndarray
                X-coordinate data.
            
            y_data: 1D numpy.ndarray
                Y-coordinate data.
            
            raw_data: 1D numpy.ndarray
                Original data points.
            
            x: int or float
                Cursor x-coordinate in device units.
            
            y: int or float
                Cursor y-coordinate in device units.
            
            limit: int or float
                Maximum allowed distance in device units.
        
        Returns:
            pero.Tooltip or None
                Tooltip item.
        """
        
        # check tooltip
        if not self.show_tooltip or not self.tooltip:
            return None
        
        # calc limits
        min_x = self.x_scale.invert(x-limit)
        max_x = self.x_scale.invert(x+limit)
        min_y = self.y_scale.invert(y+limit)
        max_y = self.y_scale.invert(y-limit)
        
        # crop data
        x_data, y_data, raw_data = helpers.crop_points(
            data = (x_data, y_data, raw_data),
            crops = ((min_x, max_x), (min_y, max_y)),
            extend = False)
        
        # check data
        if len(raw_data) == 0:
            return None
        
        # scale coords
        x_data = self.x_scale.scale(x_data)
        y_data = self.y_scale.scale(y_data)
        
        # get nearest
        x_dist = x_data - x
        y_dist = y_data - y
        dist = numpy.sqrt(x_dist*x_dist + y_dist*y_dist)
        idx = numpy.argmin(dist)
        
        # check index
        if idx is None:
            return None
        
        # get overrides
        overrides = {
            'x': x_data[idx],
            'y': y_data[idx],
            'z_index': 1./dist[idx]}
        
        # make tooltip
        return self.tooltip.clone(raw_data[idx], overrides)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        raise NotImplementedError("The 'extract_data' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def finalize_limits(self, limits, exact):
        """
        Finalizes given x and y data limits by applying margins etc.
        
        Args:
            limits: ((float, float),)
                Data limits as series of (min, max) for each dimension.
            
            exact: bool
                If set to True, any additional space like margin is ignored.
        
        Returns:
            ((float, float),)
                Data limits as sequence of (min, max) for each dimension.
        """
        
        # check limits
        if limits is None:
            return None
        
        # break links
        limits = list(limits)
        for i, item in enumerate(limits):
            if item is not None:
                limits[i] = list(item)
        
        # add margin to x and y axes
        if self.margin and not exact:
            
            if limits[0] is not None:
                delta = limits[0][1] - limits[0][0]
                limits[0][0] -= delta * self.margin[3]
                limits[0][1] += delta * self.margin[1]
            
            if limits[1] is not None:
                delta = limits[1][1] - limits[1][0]
                limits[1][0] -= delta * self.margin[2]
                limits[1][1] += delta * self.margin[0]
        
        # avoid zero range
        for item in limits:
            if item is not None and item[0] == item[1]:
                item[0] -= item[0]*0.1
                item[1] += item[1]*0.1
        
        return limits
