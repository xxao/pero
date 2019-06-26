#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..enums import *
from .canvas import Canvas
from .graphics import Graphics


class Image(Canvas, Graphics):
    """
    
    """
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Image."""
        
        # init buffers
        self._commands = []
        
        # init base
        super(Image, self).__init__(**overrides)
        
        # bind events
        self.bind(EVENT.PROPERTY_CHANGED, self._on_image_property_changed)
        
        # store overrides
        self._store_command('set_properties', {'properties': overrides})
    
    
    def set_viewport(self, x=None, y=None, width=None, height=None, relative=False):
        """
        Sets rectangular region currently used for drawing. This provides an
        easy way to draw complex graphics at specific position of the
        canvas without adjusting the coordinates of the graphics. It is achieved
        by changing the origin coordinates and the logical width and height of
        the canvas.
        
        Args:
            x: int or float
                X-coordinate of the top-left corner.
            
            y: int or float
                Y-coordinate of the top-left corner.
            
            width: int, float or None
                Full width of the viewport.
            
            height: int, float or None
                Full height of the viewport.
            
            relative: bool
                If set to True the new viewport is applied relative to current
                one.
        """
        
        # set to base
        super(Image, self).set_viewport(x, y, width, height, relative)
        
        # store command
        self._store_command('set_viewport', {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'relative': relative})
    
    
    def draw(self, canvas, *args, **kwargs):
        """
        Uses given canvas to draw the image.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
        """
        
        # call commands
        for name, args in self._commands:
            method = getattr(canvas, name)
            method(**args)
    
    
    def draw_arc(self, x, y, radius, start_angle, end_angle, clockwise=True):
        """
        Draws an arc of specified radius centered around given coordinates.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the arc.
            
            start_angle: int or float
                Angle of the starting point in radians.
            
            end_angle: int or float
                Angle of the starting point in radians.
            
            clockwise: bool
                Direction of drawing between start and end point.
        """
        
        # store command
        self._store_command('draw_arc', {
            'x': x,
            'y': y,
            'radius': radius,
            'start_angle': start_angle,
            'end_angle': end_angle,
            'clockwise': clockwise})
    
    
    def draw_circle(self, x, y, radius):
        """
        Draws a circle of specified radius centered around given coordinates.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the circle.
        """
        
        # store command
        self._store_command('draw_circle', {
            'x': x,
            'y': y,
            'radius': radius})
    
    
    def draw_ellipse(self, x, y, width, height):
        """
        Draws an ellipse centered around given coordinates and fitting into the
        width and height.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            width: int or float
                Full width of the ellipse.
            
            height: int or float
                Full height of the ellipse.
        """
        
        # store command
        self._store_command('draw_ellipse', {
            'x': x,
            'y': y,
            'width': width,
            'height': height})
    
    
    def draw_line(self, x1, y1, x2, y2):
        """
        Draws a line between two points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x1: int or float
                X-coordinate of the line start.
            
            y1: int or float
                Y-coordinate of the line start.
            
            x2: int or float
                X-coordinate of the line end.
            
            y2: int or float
                Y-coordinate of the line end.
        """
        
        # store command
        self._store_command('draw_line', {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2})
    
    
    def draw_lines(self, points):
        """
        Draws continuous open line using sequence of points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # store command
        self._store_command('draw_lines', {'points': points})
    
    
    def draw_path(self, path):
        """
        Draws given path using current pen and brush.
        
        This method must be overwritten by specific backend to provide native
        implementation for path drawing.
        
        Args:
            path: pero.Path
                Path to be drawn.
        """
        
        # store command
        self._store_command('draw_path', {'path': path})
    
    
    def draw_polygon(self, points):
        """
        Draws a closed polygon using sequence of points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # store command
        self._store_command('draw_polygon', {'points': points})
    
    
    def draw_rect(self, x, y, width, height, radius=None):
        """
        Draws a rectangle specified by given top left corner and size and
        optional round corners specified as a single value or individual value
        for each corners starting from top-left.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            width: int or float
                Full width of the rectangle.
            
            height: int or float
                Full height of the rectangle.
            
            radius: int, float, (int,int,int,int) or (float,float,float,float)
                Radius of curved corners.
        """
        
        # store command
        self._store_command('draw_rect', {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'radius': radius})
    
    
    def draw_text(self, text, x, y, angle=0):
        """
        Draws a text string anchored at specified point using current text
        settings.
        
        This method must be overwritten by specific backend to provide native
        implementation for text drawing.
        
        Args:
            text: str
                Text to be drawn.
            
            x: int or float
                X-coordinate of the text anchor.
            
            y: int or float
                Y-coordinate of the text anchor.
            
            angle: int or float
                Text angle in radians.
        """
        
        # store command
        self._store_command('draw_text', {
            'text': text,
            'x': x,
            'y': y,
            'angle': angle})
    
    
    def fill(self):
        """Fills current drawing region by actual fill color."""
        
        # store command
        self._store_command('fill')
    
    
    def clip(self, path):
        """
        Sets clipping path as intersection with current one.
        
        This method needs be overwritten by specific backend to provide native
        implementation for clipping.
        
        Args:
            path: pero.Path
                Path to be used for clipping.
        """
        
        # store command
        self._store_command('clip', {'path': path})
    
    
    def unclip(self):
        """
        Removes last clipping path while keeping previous if any.
        
        This method needs be overwritten by specific backend to provide native
        implementation for clipping.
        """
        
        # store command
        self._store_command('unclip')
    
    
    def group(self, id_tag=None, class_tag=None):
        """
        Opens new drawing group.
        
        This method needs be overwritten by specific backend to provide native
        implementation for objects grouping.
        
        Args:
            id_tag: str
                Unique id of the group.
            
            class_tag:
                Class of the group.
        """
        
        # store command
        self._store_command('group', {
            'id_tag': id_tag,
            'class_tag': class_tag})
    
    
    def ungroup(self):
        """
        Closes the last drawing group.
        
        This method needs be overwritten by specific backend to provide native
        implementation for objects grouping.
        """
        
        # store command
        self._store_command('ungroup')
    
    
    def export(self, path, **options):
        """
        Draws the image into specified file using the format determined
        automatically from the file extension. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Args:
            path: str
                Full path of a file to save the image into.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        from .. import backends
        backends.export(self, path, self.width, self.height, **options)
    
    
    def show(self, title=None):
        """
        Shows the image in available viewer app. Currently this is only
        available if wxPython is installed or within Pythonista app on iOS. This
        method makes sure appropriate backend canvas is created and provided to
        the 'draw' method.
        
        Args:
            title: str or None
                Viewer frame title.
        """
        
        from .. import backends
        backends.show(self, title, self.width, self.height)
    
    
    def _store_command(self, command, args=None):
        """Stores command and its parameters."""
        
        if args is None:
            args = {}
        
        self._commands.append((command, args))
    
    
    def _on_image_property_changed(self, evt):
        """Called after any property has changed."""
        
        # store command
        self._store_command('set_property', {
            'name': evt.name,
            'value': evt.new_value})
