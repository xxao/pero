#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..enums import *
from ..properties import *
from ..drawing import Graphics, Tooltip, TextTooltip
from .tool import Tool


class Control(PropertySet):
    """
    Base class for all interactive controls. The main idea is to provide
    a backend-independent interface for drawing the control graphics, overlays
    and tooltips as well as assignment of specific interactivity tools for mouse
    and keyboard.
    
    Properties:
        
        graphics: pero.Graphics, None or UNDEF
            Main graphics to display within the control.
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies the glyph to be used for mouse tooltip drawing. If not
            specified, a system tooltip is used instead.
        
        main_tool: pero.Tool, None or UNDEF
            Specifies the main keyboard and mouse interactivity tool. This tool
            is bound to all keyboard and mouse events. Note that each newly
            assigned tool has higher priority than those currently assigned.
            Therefore this tool should be assigned first.
        
        cursor_tool: pero.Tool, None or UNDEF
            Specifies the interactivity tool used to provide specific
            functionality for mouse cursor (i.e. no button is pressed). This
            tool is bound to all keyboard and mouse events except mouse buttons
            events. Note that each newly assigned tool has higher priority than
            those currently assigned.
        
        left_tool: pero.Tool, None or UNDEF
            Specifies the interactivity tool used to provide specific
            functionality for left mouse button. This tool is bound to all
            keyboard and mouse events including the left mouse button events.
            Note that each newly assigned tool has higher priority than those
            currently assigned.
        
        right_tool: pero.Tool, None or UNDEF
            Specifies the interactivity tool used to provide specific
            functionality for right mouse button. This tool is bound to all
            keyboard and mouse events including the right mouse button events.
            Note that each newly assigned tool has higher priority than those
            currently assigned.
    """
    
    graphics = Property(None, types=Graphics, dynamic=False, nullable=True)
    tooltip = Property(UNDEF, types=Tooltip, dynamic=False, nullable=True)
    
    main_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    cursor_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    left_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    right_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Control."""
        
        # init base
        super(Control, self).__init__(**overrides)
        
        # init buffers
        self._parent = None
        self._cursor = CURSOR.ARROW
        
        # init tooltip
        if self.tooltip is UNDEF:
            self.tooltip = TextTooltip()
        
        # bind events
        self.bind(EVENT.SIZE, self._on_control_size)
        self.bind(EVENT.PROPERTY_CHANGED, self._on_control_property_changed)
    
    
    def set_cursor(self, cursor):
        """
        Sets given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set. The value must be an item from the
                pero.CURSOR enum.
        """
        
        # check cursor
        if self._cursor == cursor:
            return
        
        # remember cursor
        self._cursor = cursor
        
        # set to view
        if self._parent is not None:
            self._parent.set_cursor(cursor)
    
    
    def export(self, path, width=None, height=None, **options):
        """
        Draws current graphics into specified image file using the format
        determined automatically from the file extension. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Args:
            path: str
                Full path of a file to save the image into.
            
            width: float or None
                Image width in device units.
            
            height: float or None
                Image height in device units.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        if self.graphics is not None and self.graphics is not UNDEF:
            self.graphics.export(path, width, height, **options)
    
    
    def show(self, title=None, width=None, height=None):
        """
        Shows given graphics in available viewer app. This method makes sure
        appropriate backend canvas is created and provided to the 'draw' method.
        
        Args:
            title: str or None
                Viewer frame title.
            
            width: float or None
                Image width in device units.
            
            height: float or None
                Image height in device units.
        """
        
        from .export import show
        show(self, title, width, height)
    
    
    def refresh(self):
        """
        Redraws current control using parent view. This makes the parent view
        responsible for initialization of a canvas and calling the 'draw' method
        to finally draw the control graphics.
        """
        
        if self._parent is not None:
            self._parent.draw_control()
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """
        Uses given canvas to draw the graphics.
        
        Args:
            canvas: pero.Canvas or None
                Specific canvas to draw the graphics on.
            
            source: any
                Data source to be used for calculating callable properties of
                current graphics.
            
            overrides: str:any pairs
                Specific properties of current graphics to be overwritten.
        """
        
        if self.graphics is not None and self.graphics is not UNDEF:
            self.graphics.draw(canvas, source=source, **overrides)
    
    
    def draw_tooltip(self, canvas, source=UNDEF, **overrides):
        """
        Draws a tooltip either by custom glyph specified by the 'tooltip'
        property or using a system tooltip of the parent view.
        
        If the custom glyph is used all the overrides are given directly to its
        drawing method (e.g. to display specific text use text='my tooltip').
        For the system tooltip actual text is also retrieved from given
        overrides assuming the 'text' key is used.
        
        Args:
            canvas: pero.Canvas
                Canvas to draw the graphics on.
            
            source: any
                Data source to be used for calculating callable properties of
                current tooltip glyph.
            
            overrides: str:any pairs
                Specific properties of the tooltip to be overwritten.
        """
        
        # skip tooltip
        if self.tooltip is None:
            return
        
        # use custom tooltip
        if self.tooltip is not UNDEF:
            self.tooltip.draw(canvas, source=source, **overrides)
            return
        
        # extract text
        text = overrides.get('text', "")
        
        # use system tooltip
        if self._parent is not None:
            self._parent.draw_tooltip(text)
    
    
    def draw_overlay(self, func=None, **kwargs):
        """
        Uses parent view to initialize overlay canvas and calls given drawing
        function on it.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given arguments (i.e. func(canvas, **kwargs)).
        
        Calling this method without any parameter clears current overlay.
        
        Args:
            func: callable or None
                Drawing function to be called to draw the overlay.
            
            kwargs: str:any pairs
                Keyword arguments, which should be provided to the given drawing
                function.
        """
        
        if self._parent:
            self._parent.draw_overlay(func, **kwargs)
    
    
    def _set_parent(self, parent):
        """Sets link to parent view."""
        
        self._parent = parent
    
    
    def _set_tool(self, new_tool, old_tool=None, left=False, right=False):
        """Registers given tool."""
        
        # unbind old tool
        if old_tool:
            self.unbind(EVENT.KEY_DOWN, old_tool.on_key_down)
            self.unbind(EVENT.KEY_UP, old_tool.on_key_up)
            self.unbind(EVENT.MOUSE_ENTER, old_tool.on_mouse_enter)
            self.unbind(EVENT.MOUSE_LEAVE, old_tool.on_mouse_leave)
            self.unbind(EVENT.MOUSE_MOTION, old_tool.on_mouse_motion)
            self.unbind(EVENT.MOUSE_SCROLL, old_tool.on_mouse_scroll)
            self.unbind(EVENT.LEFT_DOWN, old_tool.on_mouse_down)
            self.unbind(EVENT.LEFT_UP, old_tool.on_mouse_up)
            self.unbind(EVENT.LEFT_DCLICK, old_tool.on_mouse_dclick)
            self.unbind(EVENT.RIGHT_DOWN, old_tool.on_mouse_down)
            self.unbind(EVENT.RIGHT_UP, old_tool.on_mouse_up)
        
        # check tool
        if not new_tool:
            return
        
        # bind key events
        self.bind(EVENT.KEY_DOWN, new_tool.on_key_down)
        self.bind(EVENT.KEY_UP, new_tool.on_key_up)
        
        # bind main mouse events
        self.bind(EVENT.MOUSE_ENTER, new_tool.on_mouse_enter)
        self.bind(EVENT.MOUSE_LEAVE, new_tool.on_mouse_leave)
        self.bind(EVENT.MOUSE_MOTION, new_tool.on_mouse_motion)
        self.bind(EVENT.MOUSE_SCROLL, new_tool.on_mouse_scroll)
        
        # bind left mouse events
        if left:
            self.bind(EVENT.LEFT_DOWN, new_tool.on_mouse_down)
            self.bind(EVENT.LEFT_UP, new_tool.on_mouse_up)
            self.bind(EVENT.LEFT_DCLICK, new_tool.on_mouse_dclick)
        
        # bind right mouse events
        if right:
            self.bind(EVENT.RIGHT_DOWN, new_tool.on_mouse_down)
            self.bind(EVENT.RIGHT_UP, new_tool.on_mouse_up)
            self.bind(EVENT.RIGHT_DCLICK, new_tool.on_mouse_dclick)
    
    
    def _on_control_size(self, evt):
        """Redraws current graphics when size has changed."""
        
        if self._parent is not None:
            self._parent.draw_control()
    
    
    def _on_control_property_changed(self, evt):
        """Called after any property has changed."""
        
        # main tool changed
        if evt.name == 'main_tool':
            self._set_tool(evt.new_value, evt.old_value, True, True)
        
        # cursor tool changed
        elif evt.name == 'cursor_tool':
            self._set_tool(evt.new_value, evt.old_value, False, False)
        
        # left mouse tool changed
        elif evt.name == 'left_tool':
            self._set_tool(evt.new_value, evt.old_value, True, False)
        
        # right mouse tool changed
        elif evt.name == 'right_tool':
            self._set_tool(evt.new_value, evt.old_value, False, True)
