#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import re
import json
from .. enums import *
from . matrix import Matrix
from . frame import Frame

# define constants
_CIRCLE_FORCE = (4./3.)*numpy.tan(numpy.pi/(2*4))
_SVG_COMMANDS = set('MmZzLlHhVvCcSsQqTtAa')
_SVG_COMMANDS_RE = re.compile("([MmZzLlHhVvCcSsQqTtAa])")
_SVG_COORDS_RE = re.compile("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")
_ANGLE_LIMIT = 0.0001


class Path(object):
    """
    Represents a complex graphical path as a sequence of standard commands. All
    of the drawing methods returns self so that they can be chained.
    """
    
    
    def __init__(self, fill_rule=EVENODD):
        """
        Initializes a new instance of Path.
        
        Args:
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum. 
        """
        
        self._paths = [[]]
        self._subpath = self._paths[-1]
        self._cursor = (0, 0)
        
        self._bbox = None
        self._commands = None
        self._anchors = None
        self._handles = None
        self._start_angle = None
        self._end_angle = None
        
        self._fill_rule = fill_rule
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "\n".join(str(x) for x in self.commands())
    
    
    @property
    def fill_rule(self):
        """
        Gets current fill rule as a value from pero.FILL_RULE enum.
        
        Returns:
            str
                Fill rule.
        """
        
        return self._fill_rule
    
    
    @fill_rule.setter
    def fill_rule(self, value):
        """
        Sets current fill rule as a value from pero.FILL_RULE enum.
        
        Args:
            value: pero.FILL_RULE
                Fill rule.
        """
        
        self._fill_rule = value
    
    
    @property
    def cursor(self):
        """
        Gets current cursor position.
        
        Returns:
            (float, float)
                Current cursor coordinates.
        """
        
        return self._cursor
    
    
    def commands(self):
        """
        Gets a sequence of all commands from all sub-paths.
        
        Returns:
            ((str, float,),)
                Sequence of commands as (pero.PATH, *values)
        """
        
        # get commands
        if self._commands is None:
            self._commands = tuple(tuple(c) for p in self._paths for c in p)
        
        return self._commands
    
    
    def anchors(self):
        """
        Gets all anchors.
        
        Returns:
            ((float, float),)
                Path anchors.
        """
        
        # get anchors
        if self._anchors is None:
            
            anchors = []
            
            # parse path
            for subpath in self._paths:
                
                # parse subpath
                origin = None
                for command in subpath:
                    
                    # get data
                    key = command[0]
                    values = command[1:]
                    
                    # close
                    if key == PATH_CLOSE:
                        continue
                    
                    # move to
                    if key == PATH_MOVE:
                        origin = values
                        continue
                    
                    # add origin
                    if origin:
                        anchors.append(origin)
                        origin = None
                    
                    # line to
                    if key == PATH_LINE:
                        anchors.append(values)
                    
                    # curve to
                    elif key == PATH_CURVE:
                        anchors.append(values[4:6])
            
            self._anchors = tuple(anchors)
        
        return self._anchors
    
    
    def handles(self):
        """
        Gets all control handles.
        
        Returns:
            ((float, float, float, float),)
                Path handles as (x, y, cx, cy).
        """
        
        # get handles
        if self._handles is None:
            
            handles = []
            
            # parse path
            for subpath in self._paths:
                
                # parse subpath
                cursor = None
                for command in subpath:
                    
                    # get data
                    key = command[0]
                    values = command[1:]
                    
                    # move to
                    if key == PATH_MOVE:
                        cursor = values
                    
                    # line to
                    elif key == PATH_LINE:
                        cursor = values
                    
                    # curve to
                    elif key == PATH_CURVE:
                        handles.append(cursor+values[0:2])
                        handles.append(values[4:6]+values[2:4])
                        cursor = values[4:6]
            
            self._handles = tuple(handles)
        
        return self._handles
    
    
    def start(self):
        """
        Gets the start point of the first sub-path.
        
        Returns:
            (float, float)
                Path start coordinates.
        """
        
        # return cursor if not path
        if not self._paths:
            return self.cursor
        
        # get first sub-path
        path = self._paths[0]
        if not path:
            return self.cursor
        
        # get start
        for command in path:
            
            # get data
            key = command[0]
            values = command[1:]
            
            # move to
            if key == PATH_MOVE:
                return values
        
        return self.cursor
    
    
    def end(self):
        """
        Gets the end point of the last sub-path.
        
        Returns:
            (float, float)
                Path end coordinates.
        """
        
        # return cursor if not path
        if not self._paths:
            return self.cursor
        
        # get first sub-path
        path = self._paths[-1]
        if not path:
            return self.cursor
        
        # get end
        for command in reversed(path):
            
            # get data
            key = command[0]
            values = command[1:]
            
            # line to
            if key == PATH_LINE:
                return values
            
            # curve to
            elif key == PATH_CURVE:
                return values[4:6]
        
        return self.cursor
    
    
    def center(self):
        """
        Gets current bounding box center.
        
        Returns:
            (float, float)
                Path center coordinates.
        """
        
        # return cursor if not path
        if not self._paths:
            return self.cursor
        
        # get center
        return self.bbox().center
    
    
    def start_angle(self):
        """
        Gets the angle of the path at the start point of the first sub-path
        in radians.
        
        Returns:
            float or None
                Start angle in radians.
        """
        
        # get angle
        if self._start_angle is None:
            
            # get first sub-path
            path = self._paths[0]
            if not path:
                return None
            
            # init points
            origin = None
            control = None
            
            # get angle
            for command in path:
                
                # get data
                key = command[0]
                values = command[1:]
                
                # move to
                if key == PATH_MOVE:
                    origin = values
                
                # line to
                elif key == PATH_LINE:
                    control = values
                
                # curve to
                elif key == PATH_CURVE:
                    control = values[:2]
                
                # calc angle
                if origin and control:
                    self._start_angle = numpy.arctan2(control[1] - origin[1], control[0] - origin[0])
                    break
        
        return self._start_angle
    
    
    def end_angle(self):
        """
        Gets the angle of the path at the end point of the last sub-path
        in radians.
        
        Returns:
            float or None
                End angle in radians.
        """
        
        # get angle
        if self._end_angle is None:
            
            # get last sub-path
            path = self._paths[-1]
            if not path:
                return None
            
            # init points
            origin = None
            control = None
            
            # get angle
            for command in reversed(path):
                
                # get data
                key = command[0]
                values = command[1:]
                
                # move to
                if key == PATH_MOVE:
                    origin = values
                
                # line to
                elif key == PATH_LINE:
                    if control:
                        origin = values
                    else:
                        control = values
                
                # curve to
                elif key == PATH_CURVE:
                    if control:
                        origin = values[4:6]
                    else:
                        origin = values[2:4]
                        control = values[4:6]
                
                # calc angle
                if origin and control:
                    self._end_angle = numpy.arctan2(control[1] - origin[1], control[0] - origin[0])
                    break
        
        return self._end_angle
    
    
    def bbox(self):
        """
        Calculates current path bounding box.
        
        Returns:
            pero.Frame or None
                Path bounding box or None if path doesn't contain any command.
        """
        
        # calc box
        if self._bbox is None:
            
            # init origin
            x1 = 0
            y1 = 0
            
            # add commands
            for command in self.commands():
                
                # get data
                key = command[0]
                values = command[1:]
                
                # close
                if key == PATH_CLOSE:
                    continue
                
                # move to
                if key == PATH_MOVE:
                    x1, y1 = values
                    continue
                
                # init frame
                if self._bbox is None:
                    self._bbox = Frame(x1, y1)
                
                # line to
                if key == PATH_LINE:
                    self._bbox.extend(x1, y1)
                    x1, y1 = values
                    self._bbox.extend(x1, y1)
                
                # curve to
                elif key == PATH_CURVE:
                    cx1, cy1, cx2, cy2, x2, y2 = values
                    bbox = Path.curve_bbox(x1, y1, cx1, cy1, cx2, cy2, x2, y2)
                    self._bbox.extend(*bbox.rect)
                    x1, y1 = x2, y2
        
        return self._bbox.clone()
    
    
    def json(self):
        """
        Gets current path as JSON dump.
        
        Returns:
            str
                JSON dump.
        """
        
        return json.dumps({
            "fill_rule": self.fill_rule,
            "commands": self.commands()})
    
    
    def svg(self, indent="", rounding=None):
        """
        Gets current path as SVG commands.
        
        Args:
            indent: str
                XML indentation.
            
            rounding: int or None
                Rounding applied to all coordinates.
        
        Returns:
            str
                SVG commands
        """
        
        full_svg = []
        for path in self._paths:
            
            path_svg = []
            for commands in path:
                key = commands[0]
                
                values = commands[1:]
                if rounding is not None:
                    values = (round(x, rounding) for x in values)
                
                command = " ".join(str(x) for x in values) if values else ""
                path_svg.append(key+command)
            
            full_svg.append(" ".join(path_svg))
        
        indent = "\n" + indent
        
        return indent + indent.join(full_svg)
    
    
    def dirty(self):
        """Resets internal cached values."""
        
        self._bbox = None
        self._commands = None
        self._anchors = None
        self._handles = None
        self._start_angle = None
        self._end_angle = None
    
    
    def close(self):
        """
        Adds a line segment from current point to the beginning of the current
        sub-path. A new sub-path will be initialized.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # check if sub-path exists
        if not self._subpath:
            return self
        
        # close current sub-path
        self._subpath.append([PATH_CLOSE])
        
        # move cursor
        self._cursor = self._subpath[0][1:3]
        
        # init new sub-path
        self._subpath = []
        self._paths.append(self._subpath)
        
        # make dirty
        self.dirty()
        
        return self
    
    
    def move_to(self, x, y, relative=False):
        """
        Begins a new sub-path by moving current point to given coordinates.
        
        Args:
            x: int or float
                X-coordinate of the point to move to.
            
            y: int or float
                Y-coordinate of the point to move to.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # move cursor
        self._cursor = (x, y)
        
        # init new sub-path
        if self._subpath:
            self._subpath = []
            self._paths.append(self._subpath)
        
        return self
    
    
    def line_to(self, x=None, y=None, relative=False):
        """
        Adds a straight line from the current point to given coordinates.
        
        Args:
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # check coords
        if x is None and y is None:
            return
        
        # init sub-path if necessary
        if not self._subpath:
            self._subpath.append([PATH_MOVE, self._cursor[0], self._cursor[1]])
        
        # get absolute coordinates
        if relative:
            if x is not None:
                x += self._cursor[0]
            if y is not None:
                y += self._cursor[1]
        
        # vertical line
        if x is None:
            x = self._cursor[0]
        
        # horizontal line
        if y is None:
            y = self._cursor[1]
        
        # add line
        self._subpath.append([PATH_LINE, x, y])
        
        # move cursor
        self._cursor = (x, y)
        
        # make dirty
        self.dirty()
        
        return self
    
    
    def ray_to(self, angle, length):
        """
        Adds a straight line from the current point by given angle and length.
        
        Args:
            angle: int or float
                Line angle in radians.
            
            length: int or float
                Line length.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get previous end point
        x1, y1 = self._cursor
        
        # calc end point
        x2 = x1 + length * numpy.cos(angle)
        y2 = y1 + length * numpy.sin(angle)
        
        # add line
        self.line_to(x2, y2)
        
        return self
    
    
    def curve_to(self, cx1, cy1, cx2, cy2, x, y, relative=False):
        """
        Adds a cubic Bezier curve from the current point using control points
        and end point.
        
        Args:
            cx1: int or float
                X-coordinate of the start control point.
            
            cy1: int or float
                Y-coordinate of the start control point.
            
            cx2: int or float
                X-coordinate of the end control point.
            
            cy2: int or float
                Y-coordinate of the end control point.
            
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # init sub-path if necessary
        if not self._subpath:
            self._subpath.append([PATH_MOVE, self._cursor[0], self._cursor[1]])
        
        # get absolute coordinates
        if relative:
            cx1 += self._cursor[0]
            cy1 += self._cursor[1]
            cx2 += self._cursor[0]
            cy2 += self._cursor[1]
            x += self._cursor[0]
            y += self._cursor[1]
        
        # add curve
        self._subpath.append([PATH_CURVE, cx1, cy1, cx2, cy2, x, y])
        
        # move cursor
        self._cursor = (x, y)
        
        # make dirty
        self.dirty()
        
        return self
    
    
    def curve_s_to(self, cx2, cy2, x, y, relative=False):
        """
        Adds a smooth cubic Bezier curve from the current point, using
        reflection of the previous control point and given end point and control
        point.
        
        Args:
            cx2: int or float
                X-coordinate of the end control point.
            
            cy2: int or float
                Y-coordinate of the end control point.
            
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            cx2 += self._cursor[0]
            cy2 += self._cursor[1]
            x += self._cursor[0]
            y += self._cursor[1]
        
        # get previous control point
        cx1, cy1 = self._cursor
        if self._subpath and self._subpath[-1][0] == PATH_CURVE:
            cx1, cy1 = self._subpath[-1][3:5]
            cx1 += 2*(self._cursor[0] - cx1)
            cy1 += 2*(self._cursor[1] - cy1)
        
        # add curve
        self.curve_to(cx1, cy1, cx2, cy2, x, y)
        
        return self
    
    
    def quad_to(self, cx, cy, x, y, relative=False):
        """
        Adds a quadratic Bezier curve from the current point using control and
        end point.
        
        Args:
            cx: int or float
                X-coordinate of the control point.
            
            cy: int or float
                Y-coordinate of the control point.
            
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
            cx += self._cursor[0]
            cy += self._cursor[1]
        
        # get control points
        cx1 = cx - (cx - self._cursor[0])/3.
        cy1 = cy - (cy - self._cursor[1])/3.
        
        cx2 = cx - (cx - x)/3.
        cy2 = cy - (cy - y)/3.
        
        # add curve
        self.curve_to(cx1, cy1, cx2, cy2, x, y)
        
        return self
    
    
    def quad_s_to(self, x, y, relative=False):
        """
        Adds a smooth quadratic Bezier curve from the current point, using
        reflection of the previous control point and given end point.
        
        Args:
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # get previous control point
        cx1, cy1 = self._cursor
        if self._subpath and self._subpath[-1][0] == PATH_CURVE:
            cx1, cy1 = self._subpath[-1][3:5]
            cx1 += 2*(self._cursor[0] - cx1)
            cy1 += 2*(self._cursor[1] - cy1)
        
        # get previous end point
        x1, y1 = self._cursor
        
        # get quad control point
        cx = .5*(3*cx1 - x1)
        cy = .5*(3*cy1 - y1)
        
        # get end control point
        cx2 = cx - (cx-x)/3.
        cy2 = cy - (cy-y)/3.
        
        # add curve
        self.curve_to(cx1, cy1, cx2, cy2, x, y)
        
        return self
    
    
    def bow_to(self, x, y, radius, large=False, clockwise=True, relative=False):
        """
        Adds a circular arc from the current point, using given radius and end
        point coordinates. One of the four existing solutions is chosen
        according to the 'large' and 'clockwise' parameters.
        
        If the radius is too small for specified end points the theoretical
        minimum is used, which equals half of the end points distance.
        
        Args:
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            radius: int or float
                Radius of the arc.
            
            large: bool
                Specifies which of the possible arcs will be drawn according
                to its length.
            
            clockwise: bool
                Specifies which of the possible arcs will be drawn according to
                drawing direction. If set to True the clockwise arc is drawn,
                otherwise the anti-clockwise.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # get start point
        x1, y1 = self._cursor
        
        # get points distance and angle
        dist = 0.5 * numpy.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        angle = numpy.arctan2(y - y1, x - x1)
        
        # check min radius
        radius = max(radius, dist)
        
        # calc sin/cos
        sin = numpy.sin(angle)
        cos = numpy.cos(angle)
        
        # get origins
        c = numpy.sqrt(radius ** 2 - dist ** 2)
        c1x = x1 + dist * cos - c * sin
        c1y = y1 + dist * sin + c * cos
        c2x = x1 + dist * cos + c * sin
        c2y = y1 + dist * sin - c * cos
        
        # set circles
        if angle >= 0:
            small = c1x, c1y
            big = c2x, c2y
        else:
            big = c2x, c2y
            small = c1x, c1y
        
        # apply direction
        if not clockwise:
            small, big = big, small
        
        # select final circle
        cx, cy = big if large else small
        
        # get end angle
        end_angle = numpy.arctan2(y - cy, x - cx)
        
        # add arc
        self.arc_around(cx, cy, end_angle, clockwise=clockwise)
        
        return self
    
    
    def arc_to(self, cx, cy, x, y, radius=None, relative=False, finalize=False, limit=True):
        """
        Adds a circular arc from the current point, using given radius and
        control and end point coordinates. This is achieved by adding additional
        points (as needed) between the endpoints to reach smoothly the desired
        arc radius.
        
        The initial strait segment between start point and the first new point
        is added automatically. By default the final strait segment is omitted
        and the path ends at the last newly added point. This behavior can be
        changed by setting the 'finalize' to True.
        
        If the radius is too big for given points the final curve creates
        characteristic flipping effect with sharp corners. This behavior can be
        avoided by setting the 'limit' to True to limit the radius to maximum
        value to get smooth curve. The same value is also used automatically
        if radius is not specified.
        
        Args:
            cx: int or float
                X-coordinate of the control point.
            
            cy: int or float
                Y-coordinate of the control point.
            
            x: int or float
                X-coordinate of the end point.
            
            y: int or float
                Y-coordinate of the end point.
            
            radius: int or float
                Radius of the arc.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
            
            finalize: bool
                If set to True the final strait segment to the end point is
                added automatically.
            
            limit: bool
                If set to True the maximum allowed radius is used to avoid the
                curve flipping effect.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
            cx += self._cursor[0]
            cy += self._cursor[1]
        
        # get start point
        x1, y1 = self._cursor
        
        # check control point
        if (x1 == cx and y1 == cy) or (x == cx and y == cy) or radius == 0:
            if finalize: self.line_to(x, y)
            else: self.line_to(cx, cy)
            return self
        
        # check same point
        if x1 == x and y1 == y:
            if finalize: self.line_to(x, y)
            return self
        
        # check points in line
        if abs((cy - y1) * (x - x1) - (cx - x1) * (y - y1)) < 1e-5:
            if finalize: self.line_to(x, y)
            else: self.line_to(cx, cy)
            return self
        
        # get total angle
        angle = numpy.arctan2(cy-y1, cx-x1) - numpy.arctan2(cy-y, cx-x)
        
        # get distances
        x1c = numpy.sqrt((cx - x1)**2 + (cy - y1)**2)
        x2c = numpy.sqrt((cx - x)**2 + (cy - y)**2)
        
        # get limits
        min_dist = min(x1c, x2c)
        max_radius = min_dist * abs(numpy.tan(0.5*angle))
        
        # use max radius if not set
        if radius is not None:
            dist = radius / abs(numpy.tan(0.5*angle))
        else:
            dist = min_dist
            radius = max_radius
        
        # check limits
        if limit and (dist > x1c or dist > x2c):
            dist = min_dist
            radius = max_radius
        
        # get arc endpoints
        ax1 = cx - (cx - x1) * dist / x1c
        ay1 = cy - (cy - y1) * dist / x1c
        ax2 = cx - (cx - x) * dist / x2c
        ay2 = cy - (cy - y) * dist / x2c
        
        # get arc origin
        dx = cx * 2 - ax1 - ax2
        dy = cy * 2 - ay1 - ay2
        ac = numpy.sqrt(dx**2 + dy**2)
        oc = numpy.sqrt(radius**2 + dist**2)
        
        ox = cx - dx * oc / ac
        oy = cy - dy * oc / ac
        
        # get end angle
        end_angle = numpy.arctan2(ay2-oy, ax2-ox)
        
        # get arc direction
        clockwise = True
        if -numpy.pi < angle < 0 or numpy.pi < angle:
            clockwise = False
        
        # add initial line
        if x1 != ax1 or y1 != ay1:
            self.line_to(ax1, ay1)
        
        # add arc
        self.arc_around(ox, oy, end_angle, clockwise=clockwise)
        
        # add final line
        if finalize and (x != ax2 or y != ay2):
            self.line_to(x, y)
        
        return self
    
    
    def arc_around(self, x, y, end_angle, clockwise=True, relative=False):
        """
        Adds a circular arc from the current point around given center
        coordinates up to specified end angle.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            end_angle: float
                End angle in radians.
            
            clockwise: bool
                Specifies the direction of drawing. If set to True, the arc
                will be drawn in the clockwise direction.
            
            relative: bool
                If set to True given coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # init constants
        pi2 = numpy.pi * 2
        pi05 = numpy.pi * 0.5
        
        # get start point
        x1, y1 = self._cursor
        
        # get radius
        radius = numpy.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        
        # get angles
        start_angle = numpy.arctan2(y1 - y, x1 - x) % pi2
        end_angle = end_angle % pi2
        total_angle = numpy.abs(end_angle - start_angle) % pi2
        
        if start_angle > end_angle:
            total_angle = pi2 - total_angle
        
        # change direction
        direction = 1
        if not clockwise:
            total_angle = pi2 - total_angle
            direction = -1
        
        # init start
        a1 = start_angle
        
        # create segments
        while total_angle > _ANGLE_LIMIT:
            # calc segment angle
            a2 = a1 + direction * min(total_angle, pi05)
            angle = (a2 - a1)
            
            # calc force
            force = radius * (4. / 3.) * numpy.tan(numpy.pi / (2 * pi2 / angle))
            
            # calc coordinates
            x2 = x + radius * numpy.cos(a2)
            y2 = y + radius * numpy.sin(a2)
            cx1 = x1 + force * numpy.cos(a1 + pi05)
            cy1 = y1 + force * numpy.sin(a1 + pi05)
            cx2 = x2 + force * numpy.cos(a2 - pi05)
            cy2 = y2 + force * numpy.sin(a2 - pi05)
            
            # add curve
            self.curve_to(cx1, cy1, cx2, cy2, x2, y2)
            
            # update values
            total_angle -= numpy.abs(angle)
            a1 = a2
            x1 = x2
            y1 = y2
        
        return self
    
    
    def arc(self, x, y, radius, start_angle, end_angle, clockwise=True):
        """
        Adds an arc as a new sub-path of given radius centered around given
        coordinates.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the arc.
            
            start_angle: float
                Start angle in radians.
            
            end_angle: float
                End angle in radians.
            
            clockwise: bool
                Specifies the direction of drawing. If set to True, the arc
                will be drawn in the clockwise direction.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # move to start
        x1 = x + radius * numpy.cos(start_angle)
        y1 = y + radius * numpy.sin(start_angle)
        self.move_to(x1, y1)
        
        # add arc
        self.arc_around(x, y, end_angle, clockwise)
        
        return self
    
    
    def circle(self, x, y, radius, relative=False):
        """
        Adds a circle as a new closed sub-path of given radius centered around
        given coordinates. Current cursor point stays at the circle center.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the circle.
            
            relative: bool
                If set to True center coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # calc control handle length
        force = radius * _CIRCLE_FORCE
        
        # create circle
        self.move_to(x, y-radius)
        self.curve_to(x+force, y-radius, x+radius, y-force, x+radius, y)
        self.curve_to(x+radius, y+force, x+force, y+radius, x, y+radius)
        self.curve_to(x-force, y+radius, x-radius, y+force, x-radius, y)
        self.curve_to(x-radius, y-force, x-force, y-radius, x, y-radius)
        self.close()
        
        # move cursor to center
        self._cursor = (x, y)
        
        return self
    
    
    def ellipse(self, x, y, width, height, relative=False):
        """
        Adds an ellipse as a new closed sub-path of given size centered around
        given coordinates. Current cursor point stays at the ellipse center.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            width: int or float
                Full width of the ellipse.
            
            height: int or float
                Full height of the ellipse.
            
            relative: bool
                If set to True center coordinates are considered as relative to
                current point.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # create ellipse
        path = Path().circle(0, 0, 0.5*height)
        scale = float(width) / height
        matrix = Matrix().scale(scale, 1).translate(x, y)
        path.transform(matrix)
        
        # add to current path
        self.path(path)
        
        # move cursor to center
        self._cursor = (x, y)
        
        return self
    
    
    def rect(self, x, y, width, height, radius=0, relative=False):
        """
        Adds a rectangle as a new closed sub-path of given size and the top-left
        origin coordinates. Current cursor point stays at the top left corner.
        
        Args:
            x: int or float
                X-coordinate of the top left corner.
            
            y: int or float
                Y-coordinate of the top left corner.
            
            width: int or float
                Full rectangle width.
            
            height: int or float
                Full rectangle height.
            
            radius: int or float or collection of four int/float
                Radius of the corners as a single value or separate value for
                each corner individually, starting top-left.
            
            relative: bool
                If set to True origin coordinates are considered as relative to
                current point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # get absolute coordinates
        if relative:
            x += self._cursor[0]
            y += self._cursor[1]
        
        # create standard rectangle
        if not radius:
            
            self.move_to(x, y)
            self.line_to(width, 0, relative=True)
            self.line_to(0, height, relative=True)
            self.line_to(-width, 0, relative=True)
            self.close()
            
            return self
        
        # use separate radii
        if isinstance(radius, (list, tuple)):
            r1, r2, r3, r4 = radius
        else:
            r1, r2, r3, r4 = radius, radius, radius, radius
        
        # calc control handle length
        f1 = r1 * _CIRCLE_FORCE
        f2 = r2 * _CIRCLE_FORCE
        f3 = r3 * _CIRCLE_FORCE
        f4 = r4 * _CIRCLE_FORCE
        
        self.move_to(x+width-r2, y)
        self.curve_to(f2, 0, r2, r2-f2, r2, r2, relative=True)
        self.line_to(0, height-r2-r3, relative=True)
        self.curve_to(0, f3, -r3+f3, r3, -r3, r3, relative=True)
        self.line_to(-width+r3+r4, 0, relative=True)
        self.curve_to(-f4, 0, -r4, -r4+f4, -r4, -r4, relative=True)
        self.line_to(0, -height+r4+r1, relative=True)
        self.curve_to(0, -f1, r1-f1, -r1, r1, -r1, relative=True)
        self.close()
        
        # move cursor to origin
        self._cursor = (x, y)
        
        return self
    
    
    def polygon(self, points, relative=False):
        """
        Adds a polygon as a new closed sub-path defined by given points.
        
        Args:
            points: list of (float, float)
                Collection of x,y coordinates of the points.
            
            relative: bool
                If set to True all coordinates are considered as relative to
                previous point.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # move to start
        x, y = points[0]
        self.move_to(x, y, relative=relative)
        
        # add points
        for point in points[1:]:
            self.line_to(point[0], point[1], relative=relative)
        
        # close polygon
        self.close()
        
        return self
    
    
    def path(self, path):
        """
        Adds a given path as a new closed sub-path.
        
        Args:
            path: pero.Path
                Path to be added.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # add commands
        for command in path.commands():
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                self.close()
            
            # move to
            elif key == PATH_MOVE:
                self.move_to(*values)
            
            # line to
            elif key == PATH_LINE:
                self.line_to(*values)
            
            # curve to
            elif key == PATH_CURVE:
                self.curve_to(*values)
        
        return self
    
    
    def transform(self, matrix):
        """
        Transforms each command by transformation matrix.
        
        Args:
            matrix: pero.Matrix
                Transformation matrix to apply.
        
        Returns:
            pero.Path
                Returns self so that the commands can be chained.
        """
        
        # transform commands
        for subpath in self._paths:
            for command in subpath:
                
                # get data
                key = command[0]
                values = command[1:]
                
                # move to
                if key == PATH_MOVE:
                    command[1:3] = matrix.transform(values[0], values[1])
                
                # line to
                elif key == PATH_LINE:
                    command[1:3] = matrix.transform(values[0], values[1])
                
                # curve to
                elif key == PATH_CURVE:
                    command[1:3] = matrix.transform(values[0], values[1])
                    command[3:5] = matrix.transform(values[2], values[3])
                    command[5:7] = matrix.transform(values[4], values[5])
        
        # transform cursor
        self._cursor = tuple(matrix.transform(self._cursor[0], self._cursor[1]))
        
        # make dirty
        self.dirty()
        
        return self
    
    
    def transformed(self, matrix, fill_rule=None):
        """
        Creates a clone of current path and applies the transformation.
        
        Args:
            matrix: pero.Matrix
                Transformation matrix to apply.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum. If set to None, current path value is used.
        
        Returns:
            pero.Path
                Transformed path as a new instance.
        """
        
        return self.clone(fill_rule).transform(matrix)
    
    
    def split(self):
        """
        Splits current path into individual sub-paths.
        
        Returns:
            (pero.Path,)
                Individual paths.
        """
        
        # just one path
        if len(self._paths) == 1:
            return self.clone()
        
        # split paths
        return tuple(Path.from_commands(x) for x in self._paths if x)
    
    
    def symbol(self, fill_rule=None):
        """
        Creates a clone of current path centered at 0,0 and rescaled to fit into
        1 x 1 square.
        
        Args:
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum. If set to None, current path value is used.
        
        Returns:
            pero.Path
                Symbol path.
        """
        
        # get current bounding box
        bbox = self.bbox()
        
        # init matrix
        matrix = Matrix()
        
        # center around zero
        matrix.translate(-bbox.cx, -bbox.cy)
        
        # scale to 1 x 1
        scale = 1. / max(bbox.width, bbox.height)
        matrix.scale(scale, scale)
        
        # apply to path
        return self.clone(fill_rule).transform(matrix)
    
    
    def clone(self, fill_rule=None):
        """
        Creates a clone of current path.
        
        Args:
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum. If set to None, current path value is used.
        
        Returns:
            pero.Path
                Direct clone of current path.
        """
        
        # get fill rule
        if fill_rule is None:
            fill_rule = self._fill_rule
        
        # clone commands
        path = Path.from_commands(self.commands(), fill_rule)
        
        # set cursor
        path._cursor = self._cursor
        
        return path
    
    
    @staticmethod
    def curve_bbox(x1, y1, cx1, cy1, cx2, cy2, x2, y2):
        """
        Gets bounding box of Bezier curve.
        
        Args:
            x1: int or float
                X-coordinate of the start point.
            
            y1: int or float
                Y-coordinate of the start point.
            
            cx1: int or float
                X-coordinate of the start control point.
            
            cy1: int or float
                Y-coordinate of the start control point.
            
            cx2: int or float
                X-coordinate of the end control point.
            
            cy2: int or float
                Y-coordinate of the end control point.
            
            x2: int or float
                X-coordinate of the end point.
            
            y2: int or float
                Y-coordinate of the end point.
        
        Returns:
            tuple of int or float
                Curve bounding box as top-left x, y, width and height.
        """
        
        # init box
        bbox = Frame(x1, y1)
        bbox.extend(x2, y2)
        
        # init points
        p1 = (x1, y1)
        c1 = (cx1, cy1)
        c2 = (cx2, cy2)
        p2 = (x2, y2)
        
        for i in range(2):
            
            def f(t):
                return numpy.power(1 - t, 3) * p1[i] \
                    + 3 * numpy.power(1 - t, 2) * t * c1[i] \
                    + 3 * (1 - t) * numpy.power(t, 2) * c2[i] \
                    + numpy.power(t, 3) * p2[i]
            
            b = 6 * p1[i] - 12 * c1[i] + 6 * c2[i]
            a = -3 * p1[i] + 9 * c1[i] - 9 * c2[i] + 3 * p2[i]
            c = 3 * c1[i] - 3 * p1[i]
            
            if a == 0:
                
                if b == 0:
                    continue
                
                t = -c / b
                if 0 < t < 1:
                    if i == 0:
                        bbox.extend(x=f(t))
                    elif i == 1:
                        bbox.extend(y=f(t))
                
                continue
            
            b2ac = numpy.power(b, 2) - 4 * c * a
            if b2ac < 0:
                continue
            
            t1 = (-b + numpy.sqrt(b2ac)) / (2 * a)
            if 0 < t1 < 1:
                if i == 0:
                    bbox.extend(x=f(t1))
                elif i == 1:
                    bbox.extend(y=f(t1))
            
            t2 = (-b - numpy.sqrt(b2ac)) / (2 * a)
            if 0 < t2 < 1:
                if i == 0:
                    bbox.extend(x=f(t2))
                elif i == 1:
                    bbox.extend(y=f(t2))
            
        return bbox
    
    
    @staticmethod
    def from_commands(commands, fill_rule=EVENODD):
        """
        Creates a new path from given commands.
        
        Args:
            commands: ((pero.PATH, float,),)
                Sequence of commands as (key, *values), where key must be a
                value from the pero.PATH enum.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum.
        
        Returns:
            pero.Path
                Path created from given commands.
        """
        
        # init path
        path = Path(fill_rule)
        
        # add commands
        for command in commands:
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                path.close()
            
            # move to
            elif key == PATH_MOVE:
                path.move_to(*values)
            
            # line to
            elif key == PATH_LINE:
                path.line_to(*values)
            
            # curve to
            elif key == PATH_CURVE:
                path.curve_to(*values)
        
        return path
    
    
    @staticmethod
    def from_json(dump):
        """
        Creates a new path from given JSON dump.
        
        Args:
            dump: str
                JSON string representing the path.
        
        Returns:
            pero.Path
                Path created from given JSON dump.
        """
        
        # load json
        if not isinstance(dump, dict):
            dump = json.loads(dump)
        
        # init path
        path = Path(fill_rule=dump.get("fill_rule", EVENODD))
        
        # add commands
        for command in dump.get("commands", []):
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                path.close()
            
            # move to
            elif key == PATH_MOVE:
                path.move_to(*values)
            
            # line to
            elif key == PATH_LINE:
                path.line_to(*values)
            
            # curve to
            elif key == PATH_CURVE:
                path.curve_to(*values)
        
        return path
    
    
    @staticmethod
    def from_svg(svg, fill_rule=EVENODD):
        """
        Creates a new path by parsing given SVG path definition.
        
        Args:
            svg: str
                SVG commands.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum.
        
        Returns:
            pero.Path
                Path created from given SVG commands.
        """
        
        # init path
        path = Path(fill_rule)
        
        # parse commands
        command = None
        for x in _SVG_COMMANDS_RE.split(svg):
            
            # close
            if x == 'Z' or x == 'z':
                path.close()
                continue
            
            # get command
            if x in _SVG_COMMANDS:
                command = x
                continue
            
            # get coords
            coords = tuple(map(float, _SVG_COORDS_RE.findall(x)))
            if not coords:
                continue
            
            # move to
            if command == 'M':
                path.move_to(*coords)
            elif command == 'm':
                path.move_to(*coords, relative=True)
            
            # line to
            elif command == 'L':
                path.line_to(*coords)
            elif command == 'l':
                path.line_to(*coords, relative=True)
            
            # horizontal line to
            elif command == 'H':
                path.line_to(x=coords[0])
            elif command == 'h':
                path.line_to(x=coords[0], relative=True)
            
            # vertical line to
            elif command == 'V':
                path.line_to(y=coords[0])
            elif command == 'v':
                path.line_to(y=coords[0], relative=True)
            
            # curve to
            elif command == 'C':
                path.curve_to(*coords)
            elif command == 'c':
                path.curve_to(*coords, relative=True)
            
            # smooth curve to
            elif command == 'S':
                path.curve_s_to(*coords)
            elif command == 's':
                path.curve_s_to(*coords, relative=True)
            
            # quad to
            elif command == 'Q':
                path.quad_to(*coords)
            elif command == 'q':
                path.quad_to(*coords, relative=True)
            
            # smooth quad to
            elif command == 'T':
                path.quad_s_to(*coords)
            elif command == 't':
                path.quad_s_to(*coords, relative=True)
            
            # unknown
            else:
                raise ValueError("Unsupported path command! -> %s" % command)
        
        return path
    
    
    @staticmethod
    def from_bezier(curve, fill_rule=EVENODD):
        """
        Creates a new path from given Bezier curve.
        
        Args:
            curve: pero.Bezier
                Bezier curve.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum.
        
        Returns:
            pero.Path
                Path created from given Bezier.
        """
        
        # get curve coords
        coords = curve.coords
        
        # make path
        path = Path(fill_rule)
        path.move_to(coords[0], coords[1])
        path.curve_to(*coords[2:])
        
        return path
    
    
    @staticmethod
    def make_star(rays, x=0, y=0, outer_radius=.5, inner_radius=.25, fill_rule=EVENODD):
        """
        Creates a closed star-like path.
        
        Args:
            rays: int
                Number of rays.
            
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            outer_radius: int or float
                Outer radius of the rays.
            
            inner_radius: int or float
                Inner radius of the rays.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum.
        
        Returns:
            pero.Path
                A new star-like path.
        """
        
        # calc vertices
        sides = rays * 2
        theta = (2*numpy.pi/sides * numpy.arange(sides + 1)) - numpy.pi / 2.0
        
        r = numpy.full(sides + 1, outer_radius, dtype=float)
        r[1::2] = inner_radius
        
        vertices = numpy.stack((r*numpy.cos(theta), r*numpy.sin(theta)), axis=1)
        vertices += numpy.array((x, y))
        
        # make path
        return Path(fill_rule).polygon(vertices[:-1])
    
    
    @staticmethod
    def make_ngon(sides, x=0, y=0, radius=.5, fill_rule=EVENODD):
        """
        Creates a closed regular polygon path.
        
        Args:
            sides: int
                Number of sides/vertices.
            
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the polygon.
            
            fill_rule: pero.FILL_RULE
                Specifies the fill rule to be used for drawing as a value from
                pero.FILL_RULE enum.
        
        Returns:
            pero.Path
                A new regular polygon path.
        """
        
        # calc vertices
        theta = (2*numpy.pi/sides * numpy.arange(sides + 1)) - numpy.pi / 2.0
        r = numpy.full(sides + 1, radius, dtype=float)
        
        vertices = numpy.stack((r*numpy.cos(theta), r*numpy.sin(theta)), axis=1)
        vertices += numpy.array((x, y))
        
        # make path
        return Path(fill_rule).polygon(vertices[:-1])
