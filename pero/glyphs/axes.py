#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from . glyph import Glyph


class Axis(Glyph):
    """
    Abstract base class for various types of axes. They serve as a drawing glyph
    only and do not implement any logic to generate ticks and labels. Everything
    is expected to be supplied in its final form already.
    
    Properties:
        
        show_line: bool or callable
            Specifies whether the major axis line should be displayed.
        
        show_labels: bool or callable
            Specifies whether the labels should be displayed.
        
        show_major_ticks: bool or callable
            Specifies whether the major ticks should be displayed.
        
        show_minor_ticks: bool or callable
            Specifies whether the minor ticks should be displayed.
        
        x: int, float or callable
            Specifies the x-coordinate of the origin.
        
        y: int, float or callable
            Specifies the y-coordinate of the origin.
        
        line properties:
            Includes pero.LineProperties to specify the main line.
        
        labels: (str,), callable, None or UNDEF
            Specifies the major ticks labels.
        
        label_between: bool
            Specifies whether labels should be in-between the major ticks (True)
            or stick to them (False). If set to True, number of ticks should be
            one item bigger compared to the labels, otherwise the last label
            will not be shown.
        
        label_offset: int, float or callable
            Specifies the shift of the labels from the main line.
        
        label_flip: bool or callable
            Specifies whether the labels should be displayed on default side of
            the axis according to other properties (False) or flipped to the
            other side (True).
        
        label_text properties:
            Includes pero.TextProperties to specify the labels text
            properties. Some of them (e.g. alignment, angle, baseline) are
            typically set automatically according to other axis properties.
        
        major_ticks: (float,), callable, None or UNDEF
            Specifies the coordinates of the major ticks.
        
        major_tick_size: int, float or callable
            Specifies the length of the major ticks.
        
        major_tick_offset: int, float or callable
            Specifies the shift of the major ticks from the main line.
        
        major_tick_flip: bool or callable
            Specifies whether the major ticks should be displayed on default
            side of the axis according to other properties (False) or flipped to
            the other side (True).
        
        major_tick_line properties:
            Includes pero.LineProperties to specify the major ticks line.
        
        minor_ticks: (float,), callable, None or UNDEF
            Specifies the coordinates of the minor ticks.
        
        minor_tick_size: int, float or callable
            Specifies the length of the minor ticks.
        
        minor_tick_offset: int, float or callable
            Specifies the shift of the minor ticks from the main line.
        
        minor_tick_flip: bool or callable
            Specifies whether the minor ticks should be displayed on default
            side of the axis according to other properties (False) or flipped to
            the other side (True).
        
        minor_tick_line properties:
            Includes pero.LineProperties to specify the minor ticks line.
    """
    
    show_line = BoolProperty(True)
    show_labels = BoolProperty(True)
    show_major_ticks = BoolProperty(True)
    show_minor_ticks = BoolProperty(True)
    
    x = NumProperty(0)
    y = NumProperty(0)
    
    line = Include(LineProperties, line_color="#000")
    
    labels = TupleProperty(None, nullable=True, intypes=(str,))
    label_text = Include(TextProperties, prefix="label", font_size=11, text_align=UNDEF, text_base=UNDEF)
    label_between = BoolProperty(False)
    label_offset = NumProperty(10)
    label_flip = BoolProperty(False)
    
    major_ticks = TupleProperty(None, nullable=True, intypes=(int, float))
    major_tick_line = Include(LineProperties, prefix="major_tick", line_color="#000")
    major_tick_size = NumProperty(5)
    major_tick_offset = NumProperty(0)
    major_tick_flip = BoolProperty(False)
    
    minor_ticks = TupleProperty(None, nullable=True, intypes=(int, float))
    minor_tick_line = Include(LineProperties, prefix="minor_tick", line_color="#000")
    minor_tick_size = NumProperty(3)
    minor_tick_offset = NumProperty(0)
    minor_tick_flip = BoolProperty(False)


class StraitAxis(Axis):
    """
    Strait axis is a standard type of axis used for Cartesian plots. By default
    the axis is drawn as a horizontal line with ticks and labels facing down. To
    create a vertical or angled axis either the 'position' or 'angle' property
    must be specified and the whole axis is rotated around the origin given by
    'x' and 'y' properties.
    
    According to the 'relative' property, the axis ticks are expected to be
    provided as relative values (True) (as a distance from axis origin) or as
    absolute values (False) (as a distance from device zero).
    
    Properties:
        
        show_title: bool or callable
            Specifies whether the title should be displayed.
        
        angle properties:
            Includes pero.AngleProperties to specify the angle.
        
        length: int, float or callable
            Specifies the main axis line length.
        
        offset: int, float or callable
            Specifies the main axis line shift from the origin. (This shift is
            not applied to the ticks.)
        
        position: pero.POSITION_LRTB or callable
            Specifies the axis base orientation and labels and titles position
            as any item from the pero.POSITION_LRTB enum.
        
        relative: bool or callable
            Specifier whether the ticks values are given as a shift from the
            axis origin (True) or as absolute values (False).
        
        label_overlap: bool or callable
            Specifies whether the labels can overlap (True) each other or should
            be removed automatically (False).
        
        label_angle properties:
            Includes pero.AngleProperties to specify the labels angle.
        
        title: str, callable, None or UNDEF
            Specifies the title to show.
        
        title_position: pero.POSITION_SEM or callable
            Specifies the title position relative to the axis origin as any item
            from the pero.POSITION_SEM enum.
        
        title_offset: int, float or callable
            Specifies the shift of the title from the main axis line.
        
        title_flip: bool or callable
            Specifies whether the title should be displayed on default side
            of the axis according to other properties (False) or flipped to the
            other side (True).
        
        title_text properties:
            Includes pero.TextProperties to specify the title text
            properties. Some of them (e.g. alignment, angle, baseline) are
            typically set automatically according to other axis properties.
        
        title_angle properties:
            Includes pero.AngleProperties to specify the title angle. By
            default the angle is set automatically according to other axis
            properties.
    """
    
    show_title = BoolProperty(True)
    
    position = EnumProperty(POS_BOTTOM, enum=POSITION_LRTB)
    relative = BoolProperty(False)
    
    angle = Include(AngleProperties)
    length = NumProperty(UNDEF)
    offset = NumProperty(0)
    
    title = StringProperty(None, nullable=True)
    title_position = EnumProperty(POS_MIDDLE, enum=POSITION_SEM)
    title_offset = NumProperty(25)
    title_flip = BoolProperty(False)
    title_text = Include(TextProperties, prefix="title", font_weight=FONT_WEIGHT_BOLD, font_size=12, text_align=UNDEF, text_base=UNDEF)
    title_angle = Include(AngleProperties, prefix="title", angle=UNDEF)
    
    label_angle = Include(AngleProperties, prefix="label")
    label_overlap = BoolProperty(False)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the axis."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        show_title = self.get_property('show_title', source, overrides)
        show_labels = self.get_property('show_labels', source, overrides)
        show_major_ticks = self.get_property('show_major_ticks', source, overrides)
        show_minor_ticks = self.get_property('show_minor_ticks', source, overrides)
        
        # start drawing group
        canvas.group(tag, "axis")
        
        # draw minor ticks
        if show_minor_ticks:
            canvas.group(None, "minor_ticks")
            self._draw_minor_ticks(canvas, source, overrides)
            canvas.ungroup()
        
        # draw major ticks
        if show_major_ticks:
            canvas.group(None, "major_ticks")
            self._draw_major_ticks(canvas, source, overrides)
            canvas.ungroup()
        
        # draw labels
        if show_labels:
            canvas.group(None, "labels")
            self._draw_labels(canvas, source, overrides)
            canvas.ungroup()
        
        # draw title
        if show_title:
            self._draw_title(canvas, source, overrides)
        
        # draw main line
        if show_line:
            self._draw_line(canvas, source, overrides)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_major_ticks(self, canvas, source, overrides):
        """Draws axis major ticks."""
        
        # get properties
        ticks = self.get_property('major_ticks', source, overrides)
        size = self.get_property('major_tick_size', source, overrides)
        offset = self.get_property('major_tick_offset', source, overrides)
        flip = self.get_property('major_tick_flip', source, overrides)
        
        # set pen
        canvas.set_pen_by(self, prefix='major_tick_', source=source, overrides=overrides)
        
        # draw ticks
        self._draw_ticks(canvas, source, overrides, ticks, size, offset, flip)
    
    
    def _draw_minor_ticks(self, canvas, source, overrides):
        """Draws axis minor ticks."""
        
        # get properties
        flip = self.get_property('minor_tick_flip', source, overrides)
        ticks = self.get_property('minor_ticks', source, overrides)
        size = self.get_property('minor_tick_size', source, overrides)
        offset = self.get_property('minor_tick_offset', source, overrides)
        
        # set pen
        canvas.set_pen_by(self, prefix='minor_tick_', source=source, overrides=overrides)
        
        # draw ticks
        self._draw_ticks(canvas, source, overrides, ticks, size, offset, flip)
    
    
    def _draw_ticks(self, canvas, source, overrides, ticks, tick_size, tick_offset, tick_flip):
        """Draws axis ticks."""
        
        # check data
        if not ticks:
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        position = self.get_property('position', source, overrides)
        relative = self.get_property('relative', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # apply position
        if position in POSITION_LR:
            angle += 0.5*math.pi
        
        if position in POSITION_TR:
            tick_size *= -1
            tick_offset *= -1
        
        # apply flipping
        if tick_flip:
            tick_size *= -1
            tick_offset *= -1
        
        # make ticks relative
        offset = 0
        if not relative:
            offset -= y if position in POSITION_LR else x
        
        # calc sin and cos
        sin = round(math.sin(angle), 5)
        cos = round(math.cos(angle), 5)
        
        # draw ticks
        for tick in ticks:
            
            x1 = x + (tick+offset) * cos - tick_offset * sin
            y1 = y + (tick+offset) * sin + tick_offset * cos
            x2 = x + (tick+offset) * cos - (tick_offset+tick_size) * sin
            y2 = y + (tick+offset) * sin + (tick_offset+tick_size) * cos
            
            canvas.draw_line(x1=x1, y1=y1, x2=x2, y2=y2)
    
    
    def _draw_labels(self, canvas, source, overrides):
        """Draws axis labels."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        position = self.get_property('position', source, overrides)
        relative = self.get_property('relative', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        labels = self.get_property('labels', source, overrides)
        label_between = self.get_property('label_between', source, overrides)
        label_offset = self.get_property('label_offset', source, overrides)
        label_angle = AngleProperties.get_angle(self, 'label_', ANGLE_RAD, source, overrides)
        label_flip = self.get_property('label_flip', source, overrides)
        label_overlap = self.get_property('label_overlap', source, overrides)
        ticks = self.get_property('major_ticks', source, overrides)
        
        # check data
        if not labels:
            return
        
        # set font
        canvas.set_text_by(self, prefix="label", source=source, overrides=overrides)
        
        # apply position
        if position in POSITION_LR:
            angle += 0.5*math.pi
        
        if position in POSITION_TR:
            label_offset *= -1
        
        # apply flipping
        if label_flip:
            label_offset *= -1
        
        # make ticks relative
        offset = 0
        if not relative:
            offset -= y if position in POSITION_LR else x
        
        # set ticks in-between
        if label_between:
            ticks = numpy.array(ticks)
            ticks = .5*(ticks[:-1] + ticks[1:])
        
        # calc sin and cos
        sin = round(math.sin(angle), 5)
        cos = round(math.cos(angle), 5)
        
        # get final orientation
        is_horizontal = sin == 0
        is_vertical = cos == 0
        is_left = cos < 0
        is_bottom = sin > 0
        is_flipped = bool(label_flip) != bool(position in POSITION_TR)
        
        # set alignment
        if canvas.text_align is UNDEF:
            
            if is_horizontal:
                canvas.text_align = TEXT_ALIGN_CENTER
            elif is_bottom:
                canvas.text_align = TEXT_ALIGN_LEFT if is_flipped else TEXT_ALIGN_RIGHT
            else:
                canvas.text_align = TEXT_ALIGN_RIGHT if is_flipped else TEXT_ALIGN_LEFT
        
        # set baseline
        if canvas.text_base is UNDEF:
            
            if is_vertical:
                canvas.text_base = TEXT_BASE_MIDDLE
            elif is_left:
                canvas.text_base = TEXT_BASE_TOP if is_flipped else TEXT_BASE_BOTTOM
            else:
                canvas.text_base = TEXT_BASE_BOTTOM if is_flipped else TEXT_BASE_TOP
        
        # draw labels
        area = []
        for i in range(min(len(labels), len(ticks))):
            
            # get values
            label = labels[i]
            pos = ticks[i]
            
            # check label
            if not label:
                continue
            
            # calc anchor
            x1 = x + (pos+offset) * cos - label_offset * sin
            y1 = y + (pos+offset) * sin + label_offset * cos
            
            # get bbox
            bbox = canvas.get_text_bbox(label, x1, y1, label_angle)
            
            # check overlaps
            if not label_overlap and any(bbox.overlaps(box) for box in area):
                continue
            
            # draw label
            canvas.draw_text(label, x=x1, y=y1, angle=label_angle)
            area.append(bbox)
    
    
    def _draw_title(self, canvas, source, overrides):
        """Draws axis title."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        offset = self.get_property('offset', source, overrides)
        position = self.get_property('position', source, overrides)
        length = self.get_property('length', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        title = self.get_property('title', source, overrides)
        title_position = self.get_property('title_position', source, overrides)
        title_offset = self.get_property('title_offset', source, overrides)
        title_angle = AngleProperties.get_angle(self, 'title_', ANGLE_RAD, source, overrides)
        title_flip = self.get_property('title_flip', source, overrides)
        
        # check data
        if not title:
            return
        
        # set font
        canvas.set_text_by(self, prefix="title", source=source, overrides=overrides)
        
        # apply position
        if position in POSITION_LR:
            angle += 0.5*math.pi
        
        if position in POSITION_TR:
            title_offset *= -1
        
        # apply flipping
        if title_flip:
            title_offset *= -1
        
        # calc sin and cos
        sin = round(math.sin(angle), 5)
        cos = round(math.cos(angle), 5)
        
        # get final orientation
        is_vertical = cos == 0
        is_left = cos < 0
        is_flipped = bool(title_flip) != bool(position in POSITION_TR)
        
        # get y-offset
        y_offset = title_offset
        
        # get x-offset
        x_offset = offset
        if title_position == POS_MIDDLE:
            x_offset += .5 * length
        elif title_position == POS_END:
            x_offset += length
        
        # calc anchor
        x = x + x_offset * cos - y_offset * sin
        y = y + x_offset * sin + y_offset * cos
        
        # set alignment
        if canvas.text_align is UNDEF:
            
            if title_position == POS_MIDDLE:
                canvas.text_align = TEXT_ALIGN_CENTER
            
            elif title_position == POS_START and is_vertical:
                canvas.text_align = TEXT_ALIGN_LEFT if is_flipped else TEXT_ALIGN_RIGHT
            
            elif title_position == POS_START:
                canvas.text_align = TEXT_ALIGN_RIGHT if is_left else TEXT_ALIGN_LEFT
            
            elif title_position == POS_END and is_vertical:
                canvas.text_align = TEXT_ALIGN_RIGHT if is_flipped else TEXT_ALIGN_LEFT
            
            elif title_position == POS_END:
                canvas.text_align = TEXT_ALIGN_LEFT if is_left else TEXT_ALIGN_RIGHT
        
        # set baseline
        if canvas.text_base is UNDEF:
            
            if is_vertical:
                canvas.text_base = TEXT_BASE_BOTTOM
            elif is_left:
                canvas.text_base = TEXT_BASE_TOP if is_flipped else TEXT_BASE_BOTTOM
            else:
                canvas.text_base = TEXT_BASE_BOTTOM if is_flipped else TEXT_BASE_TOP
        
        # get angle
        if title_angle is UNDEF:
            
            if is_vertical:
                title_angle = angle if is_flipped else -angle
            else:
                title_angle = angle-math.pi if is_left else angle
        
        # draw title
        canvas.draw_text(title, x=x, y=y, angle=title_angle)
    
    
    def _draw_line(self, canvas, source, overrides):
        """Draws axis line."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        position = self.get_property('position', source, overrides)
        offset = self.get_property('offset', source, overrides)
        length = self.get_property('length', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # set pen
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # apply position
        if position in POSITION_LR:
            angle -= 0.5*math.pi
            length *= -1
            offset *= -1
        
        # calc sin and cos
        sin = round(math.sin(angle), 5)
        cos = round(math.cos(angle), 5)
        
        # calc coords
        x1 = x + offset * cos
        y1 = y + offset * sin
        x2 = x + (length+offset) * cos
        y2 = y + (length+offset) * sin
        
        # draw line
        canvas.draw_line(x1=x1, y1=y1, x2=x2, y2=y2)


class RadialAxis(Axis):
    """
    Radial axis is a standard type of axis used for polar plots. By default
    the axis is drawn as a circle or arc line with ticks and labels facing out.
    
    The ticks are expected to be provided as absolute angle values in the units
    specified by the 'units' property.
    
    Properties:
        
        radius: int, float or callable
            Specifies the axis radius.
        
        units: str or callable
            Specifies the angle units for the ticks as any item from the
            pero.ANGLE enum.
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
        
        clockwise: bool or callable
            Specifies the drawing direction. If set to True the axis is drawn
            clockwise, otherwise anti-clockwise.
        
        label_rotation: pero.TEXT_ROTATION or callable
            Specifies the label rotation style as any item from the
            pero.TEXT_ROTATION enum.
    """
    
    radius = NumProperty(100)
    units = EnumProperty(ANGLE_RAD, enum=ANGLE)
    start_angle = Include(AngleProperties, prefix="start")
    end_angle = Include(AngleProperties, prefix="end")
    clockwise = BoolProperty(True)
    
    label_rotation = EnumProperty(TEXT_ROT_FOLLOW, enum=TEXT_ROTATION)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the axis."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        show_labels = self.get_property('show_labels', source, overrides)
        show_major_ticks = self.get_property('show_major_ticks', source, overrides)
        show_minor_ticks = self.get_property('show_minor_ticks', source, overrides)
        
        # start drawing group
        canvas.group(tag, "axis")
        
        # draw minor ticks
        if show_minor_ticks:
            canvas.group(None, "minor_ticks")
            self._draw_minor_ticks(canvas, source, overrides)
            canvas.ungroup()
        
        # draw major ticks
        if show_major_ticks:
            canvas.group(None, "major_ticks")
            self._draw_major_ticks(canvas, source, overrides)
            canvas.ungroup()
        
        # draw labels
        if show_labels:
            canvas.group(None, "labels")
            self._draw_labels(canvas, source, overrides)
            canvas.ungroup()
        
        # draw main line
        if show_line:
            self._draw_line(canvas, source, overrides)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_major_ticks(self, canvas, source, overrides):
        """Draws axis major ticks."""
        
        # get properties
        ticks = self.get_property('major_ticks', source, overrides)
        size = self.get_property('major_tick_size', source, overrides)
        offset = self.get_property('major_tick_offset', source, overrides)
        flip = self.get_property('major_tick_flip', source, overrides)
        
        # set pen
        canvas.set_pen_by(self, prefix='major_tick_', source=source, overrides=overrides)
        
        # draw ticks
        self._draw_ticks(canvas, source, overrides, ticks, size, offset, flip)
    
    
    def _draw_minor_ticks(self, canvas, source, overrides):
        """Draws axis minor ticks."""
        
        # get properties
        ticks = self.get_property('minor_ticks', source, overrides)
        size = self.get_property('minor_tick_size', source, overrides)
        offset = self.get_property('minor_tick_offset', source, overrides)
        flip = self.get_property('minor_tick_flip', source, overrides)
        
        # set pen
        canvas.set_pen_by(self, prefix='minor_tick_', source=source, overrides=overrides)
        
        # draw ticks
        self._draw_ticks(canvas, source, overrides, ticks, size, offset, flip)
    
    
    def _draw_ticks(self, canvas, source, overrides, ticks, tick_size, tick_offset, tick_flip):
        """Draws axis ticks."""
        
        # check data
        if not ticks:
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        radius = self.get_property('radius', source, overrides)
        units = self.get_property('units', source, overrides)
        
        # convert angles
        if units == ANGLE_DEG:
            ticks = tuple(map(math.radians, ticks))
        
        # get radii
        if tick_flip:
            inner_radius = radius - tick_offset - tick_size
            outer_radius = inner_radius + tick_size
        else:
            inner_radius = radius + tick_offset
            outer_radius = inner_radius + tick_size
        
        # draw ticks
        for angle in ticks:
            
            cos = math.cos(angle)
            sin = math.sin(angle)
            
            x1 = x + inner_radius * cos
            y1 = y + inner_radius * sin
            x2 = x + outer_radius * cos
            y2 = y + outer_radius * sin
            
            canvas.draw_line(x1, y1, x2, y2)
    
    
    def _draw_labels(self, canvas, source, overrides):
        """Draws axis labels."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        radius = self.get_property('radius', source, overrides)
        
        flip = self.get_property('label_flip', source, overrides)
        labels = self.get_property('labels', source, overrides)
        label_between = self.get_property('label_between', source, overrides)
        label_offset = self.get_property('label_offset', source, overrides)
        label_rotation = self.get_property('label_rotation', source, overrides)
        ticks = self.get_property('major_ticks', source, overrides)
        units = self.get_property('units', source, overrides)
        
        # check data
        if not labels:
            return
        
        # set font
        canvas.set_text_by(self, prefix="label", source=source, overrides=overrides)
        
        # set ticks in-between
        if label_between:
            ticks = numpy.array(ticks)
            ticks = .5*(ticks[:-1] + ticks[1:])
        
        # convert angles
        if units == ANGLE_DEG:
            ticks = tuple(map(math.radians, ticks))
        
        # get position
        position = POS_INSIDE if flip else POS_OUTSIDE
        
        # get radius
        radius += -label_offset if flip else label_offset
        
        # draw labels
        for i in range(min(len(labels), len(ticks))):
            
            # get values
            label = labels[i]
            angle = ticks[i]
            
            # check label
            if not label:
                continue
            
            # draw label
            canvas.draw_text_polar(label, x, y, radius, angle, position, label_rotation)
    
    
    def _draw_line(self, canvas, source, overrides):
        """Draws axis line."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        radius = self.get_property('radius', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        start_angle = AngleProperties.get_angle(self, 'start_', ANGLE_RAD, source, overrides)
        end_angle = AngleProperties.get_angle(self, 'end_', ANGLE_RAD, source, overrides)
        
        # set pen
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # clear fill color
        canvas.fill_color = None
        
        # draw full circle
        if abs(start_angle - end_angle) >= 2*math.pi:
            canvas.draw_circle(x, y, radius)
        
        # draw arc
        else:
            canvas.draw_arc(x, y, radius, start_angle, end_angle, clockwise)
