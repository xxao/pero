#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...properties import *
from ...drawing import Band as BandGlyph
from ...drawing import MarkerProperty
from .series import Series
from . import helpers


class Band(Series):
    """
    This type of series plots raw x-sorted data as two continuous lines with
    filled area in-between. Data can be provided either directly by specifying
    the 'x', 'y1' and 'y2' properties or as a sequence of raw 'data' points
    together with 'x', 'y1' and 'y2' coordinates selectors. All the coordinates
    are expected to be in real data units.
    
    To plot data as a line the 'show_line' property must be set to True.
    Similarly, to display individual points, the 'show_points' property must be
    set to True. If set to UNDEF, and line is enabled, the points are
    automatically visible if they are separated enough, as defined by the
    'spacing' property.
    
    Any property of the 'marker' can be dynamic (including the 'marker' property
    itself), expecting the raw data point as a 'source'. By this, its color,
    fill and other properties, as well as the marker itself can be set
    independently for each data point. However, be sure that all dynamic
    properties return reasonable value for UNDEF to be used for legend. If raw
    'data' property is not specified a sequence of internal raw data is created
    as ((x,y1,y2),) coordinates.
    
    Properties:
        
        show_line: bool
            Specifies whether the profile line should be displayed.
        
        show_points: bool or UNDEF
            Specifies whether individual points should be displayed. If set to
            UNDEF, the points are displayed automatically as long as their
            distance is big enough.
        
        show_area: bool
            Specifies whether the area under profile line should be displayed.
        
        data: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the raw data points.
        
        x: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of x-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        y1: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of high y-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        y2: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of low y-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        marker: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to draw actual data points with. The
            value can be specified by any item from the pero.MARKER enum or
            as an pero.Marker instance.
        
        spacing: int, float
            Specifies the minimum x-distance between points in device units to
            enable automatic points display.
        
        line properties:
            Includes pero.LineProperties to specify the line.
        
        fill properties:
            Includes pero.FillProperties to specify the area fill.
    """
    
    show_line = BoolProperty(True, dynamic=False)
    show_points = BoolProperty(UNDEF, dynamic=False)
    show_area = BoolProperty(True, dynamic=False)
    
    data = SequenceProperty(UNDEF, dynamic=False)
    x = Property(UNDEF)
    y1 = Property(UNDEF)
    y2 = Property(UNDEF)
    
    marker = MarkerProperty('o', nullable=True)
    spacing = NumProperty(20, dynamic=False)
    
    line = Include(LineProperties, line_color=UNDEF, dynamic=False)
    fill = Include(FillProperties, fill_color=UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Band series."""
        
        super(Band, self).__init__(**overrides)
        
        # init band glyph
        self._glyph = BandGlyph()
        
        # init buffers
        self._x_data = []
        self._y1_data = []
        self._y2_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
        
        # lock properties
        self.lock_property('data')
        self.lock_property('x')
        self.lock_property('y1')
        self.lock_property('y2')
    
    
    def get_labels(self):
        """Gets series labels."""
        
        labels = self.make_labels(self._x_data, self._y1_data, self._raw_data)
        labels += self.make_labels(self._x_data, self._y2_data, self._raw_data)
        
        return labels
    
    
    def get_tooltip(self, x, y, limit):
        """Gets nearest data point tooltip."""
        
        tooltip1 = self.make_tooltip(self._x_data, self._y1_data, self._raw_data, x, y, limit)
        tooltip2 = self.make_tooltip(self._x_data, self._y2_data, self._raw_data, x, y, limit)
        
        if not tooltip1:
            return tooltip2
        
        if not tooltip2:
            return tooltip1
        
        if tooltip1.z_index >= tooltip2.z_index:
            return tooltip1
        
        return tooltip2
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """Gets current data limits using whole range or specified crops."""
        
        # check data
        if self._limits is None:
            return None
        
        # init limits
        limits = self._limits
        
        # apply crop
        if x_range:
            
            limits_by_y1 = helpers.calc_profile_limits(
                data = (self._x_data, self._y1_data),
                crop = x_range,
                extend = False,
                interpolate = True)
            
            limits_by_y2 = helpers.calc_profile_limits(
                data = (self._x_data, self._y2_data),
                crop = x_range,
                extend = False,
                interpolate = True)
            
            limits = helpers.combine_limits(limits_by_y1, limits_by_y2)
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._x_data = []
        self._y1_data = []
        self._y2_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = helpers.extract_data_size(self, 'data', 'x', 'y1', 'y2')
        
        # extract data
        self._x_data, x_raw = helpers.extract_data(self, 'x', self.data, size, self.x_mapper)
        self._y1_data, y1_raw = helpers.extract_data(self, 'y1', self.data, size, self.y_mapper)
        self._y2_data, y2_raw = helpers.extract_data(self, 'y2', self.data, size, self.y_mapper)
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data)
        else:
            self._raw_data = numpy.array([x_raw, y1_raw, y2_raw]).T
        
        # check data
        if not helpers.is_sorted(self._x_data):
            raise ValueError("X-coordinates must be sorted!")
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (self._x_data.min(), self._x_data.max()),
                (min(self._y1_data.min(), self._y2_data.min()),
                    max(self._y1_data.max(), self._y2_data.max())))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the series."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # set overrides to ignore
        ignore = {'x', 'y1', 'y2', 'line_color', 'fill_color'}
        
        # crop data
        i1, i2 = helpers.crop_indices(self._x_data, x_scale.in_range, True)
        if i1 == i2:
            return
        
        x_data = self._x_data[i1:i2]
        y1_data = self._y1_data[i1:i2]
        y2_data = self._y2_data[i1:i2]
        raw_data = self._raw_data[i1:i2]
        
        # scale coords
        x_data = x_scale.scale(x_data)
        y1_data = y_scale.scale(y1_data)
        y2_data = y_scale.scale(y2_data)
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # update glyph
            self._glyph.set_properties_from(self, source=source, overrides=overrides, ignore=ignore)
            
            # get glyph colors
            line_color = self._glyph.get_property('line_color')
            if line_color is UNDEF:
                line_color = color
            
            fill_color = self._glyph.get_property('fill_color')
            if fill_color is UNDEF:
                fill_color = color.trans(0.4)
            
            # set overrides
            glyph_overrides = overrides.copy()
            glyph_overrides['x'] = x_data
            glyph_overrides['y1'] = y1_data
            glyph_overrides['y2'] = y2_data
            glyph_overrides['line_color'] = line_color
            glyph_overrides['fill_color'] = fill_color
            
            # draw band
            self._glyph.draw(canvas, raw_data, **glyph_overrides)
