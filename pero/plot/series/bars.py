#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...enums import *
from ...properties import *
from ...drawing import Frame
from .series import Series
from . import helpers


class Rectangles(Series):
    """
    Abstract base class for various types of rectangular data series. To specify
    the position of labels and active points used for tooltips the 'anchor'
    property must be set.
    
    Any property of the rectangle line and fill can be dynamic, expecting the
    raw data point as a 'source'. By this, the line and fill can be set
    independently for each data point. However, be sure that all dynamic
    properties return reasonable value for UNDEF to be used for legend. If raw
    'data' property is not specified a sequence of internal raw data is created
    as ((x,y),) coordinates according to the 'anchor' property.
    
    Properties:
        
        data: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the raw data points.
        
        anchor: str
            Specifies the position within rectangles to be used to display
            labels and tooltip as any item from the pero.POSITION_LRTBC enum.
        
        x_offset: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the x-offsets in data units.
        
        y_offset: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the y-offsets in data units.
        
        line properties:
            Includes pero.LineProperties to specify the outline.
        
        fill properties:
            Includes pero.FillProperties to specify the fill.
    """
    
    data = SequenceProperty(UNDEF, dynamic=False)
    anchor = EnumProperty(POS_CENTER, enum=POSITION_LRTBC, dynamic=False)
    
    x_offset = Property(UNDEF, dynamic=False)
    y_offset = Property(UNDEF, dynamic=False)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Rectangles series base."""
        
        super(Rectangles, self).__init__(**overrides)
        
        # init buffers
        self._left_data = []
        self._right_data = []
        self._top_data = []
        self._bottom_data = []
        
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
        
        # lock properties
        self.lock_property('data')
        self.lock_property('anchor')
        self.lock_property('x_offset')
        self.lock_property('y_offset')
        self.lock_property('x', raise_error=False)
        self.lock_property('y', raise_error=False)
        self.lock_property('width', raise_error=False)
        self.lock_property('height', raise_error=False)
        self.lock_property('left', raise_error=False)
        self.lock_property('right', raise_error=False)
        self.lock_property('top', raise_error=False)
        self.lock_property('bottom', raise_error=False)
    
    
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
        if x_range or y_range:
            
            limits_top_left = helpers.calc_points_limits(
                data = (self._left_data, self._top_data),
                crops = (x_range, y_range), 
                extend = False)
            
            limits_bottom_right = helpers.calc_points_limits(
                data = (self._right_data, self._bottom_data),
                crops = (x_range, y_range), 
                extend = False)
            
            limits = helpers.combine_limits(limits_top_left, limits_bottom_right)
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._left_data = []
        self._right_data = []
        self._top_data = []
        self._bottom_data = []
        
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = helpers.extract_data_size(self, 'data', 'x', 'y', 'width', 'height', 'left', 'right', 'top', 'bottom')
        
        # extract data
        self._left_data, left_raw = helpers.extract_data(self, 'left', self.data, size, self.x_mapper)
        self._right_data, right_raw = helpers.extract_data(self, 'right', self.data, size, self.x_mapper)
        self._top_data, top_raw = helpers.extract_data(self, 'top', self.data, size, self.y_mapper)
        self._bottom_data, bottom_raw = helpers.extract_data(self, 'bottom', self.data, size, self.y_mapper)
        
        self._x_data, x_raw = helpers.extract_data(self, 'x', self.data, size, self.x_mapper)
        self._y_data, y_raw = helpers.extract_data(self, 'y', self.data, size, self.y_mapper)
        width_data, width_raw = helpers.extract_data(self, 'width', self.data, size)
        height_data, height_raw = helpers.extract_data(self, 'height', self.data, size)
        
        # calc missing data
        if not self.has_property('x'):
            self._x_data = 0.5*(self._left_data + self._right_data)
            x_raw = self._x_data
        
        if not self.has_property('y'):
            self._y_data = 0.5*(self._top_data + self._bottom_data)
            y_raw = self._y_data
        
        if not self.has_property('left'):
            self._left_data = self._x_data - 0.5*width_data
            left_raw = self._left_data
        
        if not self.has_property('right'):
            self._right_data = self._x_data + 0.5*width_data
            right_raw = self._right_data
        
        if not self.has_property('top'):
            self._top_data = self._y_data + 0.5*height_data
            top_raw = self._top_data
        
        if not self.has_property('bottom'):
            self._bottom_data = self._y_data - 0.5*height_data
            bottom_raw = self._bottom_data
        
        # set anchor and raw data
        if self.anchor == POS_LEFT:
            self._x_data = self._left_data
            self._raw_data = numpy.array([left_raw, y_raw]).T
        
        elif self.anchor == POS_RIGHT:
            self._x_data = self._right_data
            self._raw_data = numpy.array([right_raw, y_raw]).T
        
        elif self.anchor == POS_TOP:
            self._y_data = self._top_data
            self._raw_data = numpy.array([x_raw, top_raw]).T
        
        elif self.anchor == POS_BOTTOM:
            self._y_data = self._bottom_data
            self._raw_data = numpy.array([x_raw, bottom_raw]).T
        
        else:
            self._raw_data = numpy.array([x_raw, y_raw]).T
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data)
        
        # apply offset
        if self.x_offset is not UNDEF:
            
            if isinstance(self.x_offset, (tuple, list)):
                self.x_offset = numpy.array(self.x_offset)
            
            self._x_data = self._x_data + self.x_offset
            self._left_data = self._left_data + self.x_offset
            self._right_data = self._right_data + self.x_offset
        
        if self.y_offset is not UNDEF:
            
            if isinstance(self.y_offset, (tuple, list)):
                self.y_offset = numpy.array(self.y_offset)
            
            self._y_data = self._y_data + self.y_offset
            self._top_data = self._top_data + self.y_offset
            self._bottom_data = self._bottom_data + self.y_offset
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (min(self._left_data.min(), self._right_data.min()),
                    max(self._left_data.max(), self._right_data.max())),
                (min(self._bottom_data.min(), self._top_data.min()),
                    max(self._bottom_data.max(), self._top_data.max())))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the series."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        frame = self.get_property('frame', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # get data
        left_data = self._left_data
        right_data = self._right_data
        top_data = self._top_data
        bottom_data = self._bottom_data
        raw_data = self._raw_data
        
        # check data
        if len(left_data) == 0:
            return
        
        # scale coords
        left_data = x_scale.scale(left_data)
        right_data = x_scale.scale(right_data)
        top_data = y_scale.scale(top_data)
        bottom_data = y_scale.scale(bottom_data)
        
        # get default colors
        default_line_color = color.darker(0.2)
        default_fill_color = color
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # draw rectangles
            for i, data in enumerate(raw_data):
                
                # get coords
                x = left_data[i]
                y = top_data[i]
                width = right_data[i] - x
                height = bottom_data[i] - y
                
                if width < 0:
                    width *= -1
                    x -= width
                
                if height < 0:
                    height *= -1
                    y -= height
                
                # apply clipping
                bbox = Frame(x, y, width, height)
                if not frame.overlaps(bbox):
                    continue
                
                # set pen and brush
                canvas.set_pen_by(self, source=data, overrides=overrides)
                canvas.set_brush_by(self, source=data, overrides=overrides)
                
                # set default colors
                if self.get_property('line_color', overrides=overrides, native=True) is UNDEF:
                    canvas.line_color = default_line_color
                
                if self.get_property('fill_color', overrides=overrides, native=True) is UNDEF:
                    canvas.fill_color = default_fill_color
                
                # draw rectangle
                canvas.draw_rect(x, y, max(2, width), max(2, height))


class Rects(Rectangles):
    """
    This type of series plots raw data as individual rectangles defined by the
    center 'x' and 'y' coordinates, 'width' and 'height'. Data can be provided
    either directly by specifying the 'x', 'y', 'width' and 'height' properties
    or as a sequence of raw 'data' points together with 'x', 'y', 'width' and
    'height' coordinates selectors. All the coordinates are expected to be in
    real data units.
    
    Properties:
        
        x: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of center x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        y: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of center y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        width: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of widths in real data units or a function to
            retrieve the widths from the raw data.
        
        height: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of heights in real data units or a function
            to retrieve the heights from the raw data.
    """
    
    x = Property(UNDEF)
    y = Property(UNDEF)
    width = Property(1)
    height = Property(1)


class Bars(Rectangles):
    """
    This type of series plots raw data as individual bars defined by the 'left',
    'right', 'top' and 'bottom' coordinates. Data can be provided either
    directly by specifying the 'left', 'right', 'top' and 'bottom' properties or
    as a sequence of raw 'data' points together with 'left', 'right', 'top' and
    'bottom' coordinates selectors. All the coordinates are expected to be in
    real data units.
    
    Properties:
        
        left: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of left x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        right: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of right x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        top: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of top y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        bottom: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of bottom y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
    """
    
    left = Property(UNDEF)
    right = Property(UNDEF)
    top = Property(UNDEF)
    bottom = Property(UNDEF)


class HBars(Rectangles):
    """
    This type of series plots raw data as individual horizontal bars defined by
    the 'y', left' and 'right' coordinates and 'height'. Data can be provided
    either directly by specifying the 'y', left', 'right' and 'height'
    properties or as a sequence of raw 'data' points together with 'y', left',
    'right' and 'height' coordinates selectors. All the coordinates are expected
    to be in real data units.
    
    Properties:
        
        y: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of center y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        left: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of left x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        right: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of right x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        height: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of heights in real data units or a function
            to retrieve the heights from the raw data.
    """
    
    y = Property(UNDEF)
    left = Property(0)
    right = Property(UNDEF)
    height = Property(.8)
    
    anchor = EnumProperty(POS_RIGHT, enum=POSITION_LRTBC, dynamic=False)
    margin = QuadProperty((.05, .05, .05, 0), dynamic=False)


class VBars(Rectangles):
    """
    This type of series plots raw data as individual vertical bars defined by
    the 'x', top' and 'bottom' coordinates and 'width'. Data can be provided
    either directly by specifying the 'x', top', 'bottom' and 'width' properties
    or as a sequence of raw 'data' points together with 'x', top', 'bottom' and
    'width' coordinates selectors. All the coordinates are expected to be in
    real data units.
    
    Properties:
        
        x: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of center x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        top: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of top y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        bottom: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of bottom y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        width: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of widths in real data units or a function to
            retrieve the widths from the raw data.
    """
    
    x = Property(UNDEF)
    top = Property(UNDEF)
    bottom = Property(0)
    width = Property(.8)
    
    anchor = EnumProperty(POS_TOP, enum=POSITION_LRTBC, dynamic=False)
    margin = QuadProperty((.05, .05, 0, .05), dynamic=False)
