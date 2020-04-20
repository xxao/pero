#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...enums import *
from ...properties import *
from ...drawing import Profile as ProfileGlyph
from ...drawing import MarkerProperty
from .series import Series
from . import helpers


class Profile(Series):
    """
    This type of series plots raw x-sorted data as continuous line. Data can be
    provided either directly by specifying the 'x' and 'y' properties or as a
    sequence of raw 'data' points together with 'x' and 'y' coordinates
    selectors. All the coordinates as well as the 'base' are expected to be in
    real data units.
    
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
    as ((x,y),) coordinates.
    
    Optionally the area under the curve can also be displayed if the 'show_area'
    property is set to True. In such case the line is additionally drawn as a
    filled polygon either by connecting first and last points directly or using
    strait line defined by the 'base' property.
    
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
        
        y: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of y-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        base: int, float, None or UNDEF
            Specifies the area base value in real data units.
        
        steps: pero.LINE_STEP
            Specifies the way stepped profile should be drawn as any item from
            the pero.LINE_STEP enum.
        
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
    show_area = BoolProperty(False, dynamic=False)
    
    data = SequenceProperty(UNDEF, dynamic=False)
    x = Property(UNDEF)
    y = Property(UNDEF)
    base = NumProperty(UNDEF, dynamic=False, nullable=True)
    
    steps = EnumProperty(None, enum=LINE_STEP, nullable=True)
    marker = MarkerProperty('o', nullable=True)
    spacing = NumProperty(20, dynamic=False)
    
    line = Include(LineProperties, line_color=UNDEF, dynamic=False)
    fill = Include(FillProperties, fill_color=UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Profile series."""
        
        super().__init__(**overrides)
        
        # init profile glyph
        self._glyph = ProfileGlyph()
        
        # init buffers
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
    
    
    def get_labels(self):
        """Gets series labels."""
        
        return self.make_labels(self._x_data, self._y_data, self._raw_data)
    
    
    def get_tooltip(self, x, y, limit):
        """Gets nearest data point tooltip."""
        
        return self.make_tooltip(self._x_data, self._y_data, self._raw_data, x, y, limit)
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """Gets current data limits using whole range or specified crops."""
        
        # check data
        if self._limits is None:
            return None
        
        # init limits
        limits = self._limits
        
        # apply crop
        if x_range:
            
            limits = helpers.calc_profile_limits(
                data = (self._x_data, self._y_data),
                crop = x_range,
                extend = False,
                interpolate = True)
            
            if self.base not in (UNDEF, None) and limits[1] is not None:
                limits[1][0] = min(self.base, limits[1][0])
                limits[1][1] = max(self.base, limits[1][1])
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = helpers.extract_data_size(self, 'data', 'x', 'y')
        
        # extract data
        self._x_data, x_raw = helpers.extract_data(self, 'x', self.data, size, self.x_mapper)
        self._y_data, y_raw = helpers.extract_data(self, 'y', self.data, size, self.y_mapper)
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data)
        else:
            self._raw_data = numpy.array([x_raw, y_raw]).T
        
        # check data
        if not helpers.is_sorted(self._x_data):
            raise ValueError("X-coordinates must be sorted!")
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (self._x_data.min(), self._x_data.max()),
                (self._y_data.min(), self._y_data.max()))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the series."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        base = self.get_property('base', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # set overrides to ignore
        ignore = {'x', 'y', 'base', 'line_color', 'fill_color'}
        
        # crop data
        i1, i2 = helpers.crop_indices(self._x_data, x_scale.in_range, True)
        if i1 == i2:
            return
        
        x_data = self._x_data[i1:i2]
        y_data = self._y_data[i1:i2]
        raw_data = self._raw_data[i1:i2]
        
        # scale coords
        x_data = x_scale.scale(x_data)
        y_data = y_scale.scale(y_data)
        
        # scale base
        if base is not UNDEF:
            base = y_scale.scale(base)
        
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
            glyph_overrides['y'] = y_data
            glyph_overrides['base'] = base
            glyph_overrides['line_color'] = line_color
            glyph_overrides['fill_color'] = fill_color
            
            # draw profile
            self._glyph.draw(canvas, raw_data, **glyph_overrides)
