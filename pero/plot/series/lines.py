#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...enums import *
from ...properties import *
from ...drawing import Frame, HeadProperty
from .series import Series
from . import helpers


class Lines(Series):
    """
    This type of series plots raw data as individual strait lines with optional
    head on each side. Data can be provided either directly by specifying
    the 'x1', 'y1', 'x2' and 'y2' properties or as a sequence of raw 'data'
    points together with 'x1', 'y1', 'x2' and 'y2' coordinates selectors. All
    the coordinates are expected to be in real data units.
    
    Any property of the line, 'start_head' or 'end_head' can be dynamic
    (including the 'start_head' and 'end_head' property itself), expecting the
    raw data point as a 'source'. By this, their color, fill and other
    properties, as well as the heads itself can be set independently for each
    data line. However, be sure that all dynamic properties return reasonable
    value for UNDEF to be used for legend. If raw 'data' property is not
    specified a sequence of internal raw data is created as ((x1,y1,x2,y2),)
    coordinates.
    
    Properties:
        
        data: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the raw data points.
        
        x1: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of start x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        y1: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence start of y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        x2: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of end x-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        y2: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence end of y-coordinates in real data units or
            a function to retrieve the coordinates from the raw data.
        
        start_head: pero.Head, pero.HEAD, callable, None or UNDEF
            Specifies the head glyph to be drawn at the beginning or the line.
            The value can be specified by any item from the pero.HEAD enum or
            as an pero.Head instance.
        
        end_head: pero.Head, pero.HEAD, callable, None or UNDEF
            Specifies the head glyph to be drawn at the end or the line. The
            value can be specified by any item from the pero.HEAD enum or as
            an pero.Head instance.
        
        anchor: pero.POSITION_SEM
            Specifies the position within lines to be used to display
            labels and tooltip as any item from the pero.POSITION_SEM enum.
        
        line properties:
            Includes pero.LineProperties to specify the line.
    """
    
    data = Property(UNDEF, dynamic=False)
    x1 = Property(UNDEF)
    y1 = Property(UNDEF)
    x2 = Property(UNDEF)
    y2 = Property(UNDEF)
    
    start_head = HeadProperty(UNDEF, nullable=True)
    end_head = HeadProperty(UNDEF, nullable=True)
    anchor = EnumProperty(POS_MIDDLE, enum=POSITION_SEM, dynamic=False)
    
    line = Include(LineProperties)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Lines series base."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._x1_data = []
        self._x2_data = []
        self._y1_data = []
        self._y2_data = []
        
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
        
        # lock properties
        self.lock_property('data')
        self.lock_property('x1')
        self.lock_property('x2')
        self.lock_property('y1')
        self.lock_property('y2')
        self.lock_property('anchor')
    
    
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
            
            limits_start = helpers.calc_points_limits(
                data = (self._x1_data, self._y1_data),
                crops = (x_range, y_range), 
                extend = False)
            
            limits_end = helpers.calc_points_limits(
                data = (self._x2_data, self._y2_data),
                crops = (x_range, y_range), 
                extend = False)
            
            limits = helpers.combine_limits(limits_start, limits_end)
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._x1_data = []
        self._x2_data = []
        self._y1_data = []
        self._y2_data = []
        
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = helpers.extract_data_size(self, 'data', 'x1', 'x2', 'y1', 'y2')
        
        # extract data
        self._x1_data, x1_raw = helpers.extract_data(self, 'x1', self.data, size, self.x_mapper)
        self._x2_data, x2_raw = helpers.extract_data(self, 'x2', self.data, size, self.x_mapper)
        self._y1_data, y1_raw = helpers.extract_data(self, 'y1', self.data, size, self.y_mapper)
        self._y2_data, y2_raw = helpers.extract_data(self, 'y2', self.data, size, self.y_mapper)
        
        # set anchor
        if self.anchor == POS_START:
            self._x_data = self._x1_data
            self._y_data = self._y1_data
        
        elif self.anchor == POS_END:
            self._x_data = self._x2_data
            self._y_data = self._y2_data
        
        else:
            self._x_data = .5*(self._x1_data + self._x2_data)
            self._y_data = .5*(self._y1_data + self._y2_data)
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data)
        else:
            self._raw_data = numpy.array([x1_raw, y1_raw, x2_raw, y2_raw]).T
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (min(self._x1_data.min(), self._x2_data.min()),
                    max(self._x1_data.max(), self._x2_data.max())),
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
        frame = self.get_property('frame', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # get heads overrides
        start_head_overrides = self.get_child_overrides('start_head', overrides)
        start_head_overrides_fin = start_head_overrides.copy()
        
        end_head_overrides = self.get_child_overrides('end_head', overrides)
        end_head_overrides_fin = end_head_overrides.copy()
        
        # get data
        x1_data = self._x1_data
        x2_data = self._x2_data
        y1_data = self._y1_data
        y2_data = self._y2_data
        raw_data = self._raw_data
        
        # check data
        if len(x1_data) == 0:
            return
        
        # scale coords
        x1_data = x_scale.scale(x1_data)
        x2_data = x_scale.scale(x2_data)
        y1_data = y_scale.scale(y1_data)
        y2_data = y_scale.scale(y2_data)
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # draw lines
            for i, data in enumerate(raw_data):
                
                # get coords
                x1 = x1_data[i]
                x2 = x2_data[i]
                y1 = y1_data[i]
                y2 = y2_data[i]
                
                # apply clipping
                bbox = Frame(x1, y1, x2-x1, y2-y1)
                if not frame.overlaps(bbox):
                    continue
                
                # set pen and brush
                canvas.line_color = color
                canvas.fill_color = None
                canvas.set_pen_by(self, source=data, overrides=overrides)
                
                # draw line
                canvas.draw_line(x1, y1, x2, y2)
                
                # draw start head
                head = self.get_property('start_head', data, overrides)
                if head:
                    
                    # get head colors
                    line_color = head.get_property('line_color', overrides=start_head_overrides, native=True)
                    if line_color is UNDEF:
                        line_color = color
                    
                    fill_color = head.get_property('fill_color', overrides=start_head_overrides, native=True)
                    if fill_color is UNDEF:
                        fill_color = color
                    
                    # set overrides
                    start_head_overrides_fin['x'] = x1
                    start_head_overrides_fin['y'] = y1
                    start_head_overrides_fin['angle'] = numpy.arctan2(y2-y1, x2-x1)+numpy.pi
                    start_head_overrides_fin['angle_units'] = ANGLE_RAD
                    start_head_overrides_fin['line_color'] = line_color
                    start_head_overrides_fin['fill_color'] = fill_color
                    
                    # draw head
                    head.draw(canvas, data, **start_head_overrides_fin)
                
                # draw end head
                head = self.get_property('end_head', data, overrides)
                if head:
                    
                    # get head colors
                    line_color = head.get_property('line_color', overrides=end_head_overrides, native=True)
                    if line_color is UNDEF:
                        line_color = color
                    
                    fill_color = head.get_property('fill_color', overrides=end_head_overrides, native=True)
                    if fill_color is UNDEF:
                        fill_color = color
                    
                    # set overrides
                    end_head_overrides_fin['x'] = x2
                    end_head_overrides_fin['y'] = y2
                    end_head_overrides_fin['angle'] = numpy.arctan2(y2-y1, x2-x1)
                    end_head_overrides_fin['angle_units'] = ANGLE_RAD
                    end_head_overrides_fin['line_color'] = line_color
                    end_head_overrides_fin['fill_color'] = fill_color
                    
                    # draw head
                    head.draw(canvas, data, **end_head_overrides_fin)
