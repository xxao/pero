#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Graphics, Frame
from .. glyphs import Tooltip, TextTooltip
from . tool import Tool


class Control(Graphics):
    """
    Base class for all interactive controls. The main idea is to provide
    a backend-independent interface for drawing the control graphics, overlays
    and tooltips as well as assignment of specific interactivity tools for
    mouse, keyboard and touches.
    
    Properties:
        
        graphics: pero.Graphics, None or UNDEF
            Main graphics to display within the control.
    """
    
    graphics = Property(None, types=Graphics, dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Control."""
        
        # init base
        super().__init__(**overrides)
        
        # init buffers
        self._parent = None
        self._size = (0, 0)
        
        # bind events
        self.bind(EVT_SIZE, self._on_control_size)
    
    
    def set_parent(self, parent):
        """Sets link to parent view."""
        
        # check type
        from . view import View
        if not isinstance(parent, (Control, View)):
            message = "Parent must be of type 'pero.Control' or 'pero.View'! -> %s" % type(parent)
            raise TypeError(message)
        
        # set parent
        self._parent = parent
    
    
    def set_cursor(self, cursor):
        """
        Sets given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set. The value must be an item from the
                pero.CURSOR enum.
        """
        
        # check parent
        if self._parent is None:
            return
        
        # set cursor to parent
        self._parent.set_cursor(cursor)
    
    
    def refresh(self):
        """
        Redraws current control using parent view. This makes the parent view
        responsible for initialization of a canvas and calling the 'draw' method
        to finally draw the control graphics.
        """
        
        # check parent
        if self._parent is None:
            return
        
        # refresh by parent
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
    
    
    def draw_control(self):
        """Relay control drawing to parent."""
        
        # check parent
        if self._parent is None:
            return
        
        # draw control by parent
        self._parent.draw_control()
    
    
    def draw_tooltip(self, text):
        """Relay tooltip drawing to parent."""
        
        # check parent
        if self._parent is None:
            return
        
        # draw tooltip by parent
        self._parent.draw_tooltip(text)
    
    
    def draw_overlay(self, func=None, view=None, **kwargs):
        """
        Uses parent view to initialize overlay canvas and calls given drawing
        function on it.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given arguments (i.e. func(canvas, **kwargs)).
        
        Calling this method without any parameter clears current overlay.
        
        Args:
            func: callable or None
                Drawing function to be called to draw the overlay.
            
            view: (int, int, int, int) or None
                Rectangle defined as (x, y, width, height) used to shift origin
                of drawing canvas submitted to given drawing function.
            
            kwargs: str:any pairs
                Keyword arguments, which should be provided to the given drawing
                function.
        """
        
        # check parent
        if self._parent is None:
            return
        
        # draw overlay by parent
        self._parent.draw_overlay(func, view, **kwargs)
    
    
    def clear_overlay(self):
        """Clears current overlay."""
        
        self.draw_overlay()
    
    
    def _on_control_size(self, evt):
        """Redraws current graphics when size has changed."""
        
        # get size
        self._size = (evt.width, evt.height)
        
        # draw control
        self.refresh()


class ToolControl(Control):
    """
    Main type of interactive control allowing to set specific interactivity
    tools for mouse, keyboard and touches.
    
    Properties:
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies the glyph to be used for mouse tooltip drawing. If not
            specified, a system tooltip is used instead.
        
        main_tool: pero.Tool, None or UNDEF
            Specifies the main keyboard and mouse interactivity tool. This tool
            is bound to all keyboard, mouse and touch events. Note that each
            newly assigned tool has higher priority than those currently
            assigned. Therefore, this tool should be assigned first.
        
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
        
        touch_tool: pero.Tool, None or UNDEF
            Specifies the interactivity tool used to provide specific
            functionality for touch events. This tool is bound to all keyboard
            events. Note that each newly assigned tool has higher priority than
            those currently assigned.
    """
    
    tooltip = Property(UNDEF, types=Tooltip, dynamic=False, nullable=True)
    main_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    cursor_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    left_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    right_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    touch_tool = Property(UNDEF, types=Tool, dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Control."""
        
        # init base
        super().__init__(**overrides)
        
        # init tooltip
        if self.tooltip is UNDEF:
            self.tooltip = TextTooltip()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_tool_control_property_changed)
        
        # bind tools
        self._set_tool(self.main_tool, left=True, right=True, touch=True)
        self._set_tool(self.cursor_tool)
        self._set_tool(self.left_tool, left=True)
        self._set_tool(self.right_tool, right=True)
        self._set_tool(self.touch_tool, touch=True)
    
    
    def draw_tooltip(self, canvas=None, source=UNDEF, **overrides):
        """
        Draws a tooltip either by custom glyph specified by the 'tooltip'
        property or using a system tooltip of the parent view.
        
        If the custom glyph is used all the overrides are given directly to its
        drawing method (e.g. to display specific text use text='my tooltip').
        For the system tooltip actual text is also retrieved from given
        overrides assuming the 'text' key is used.
        
        If the canvas is not provided, parent view takes care to initialize it
        if necessary and the tooltip will be drawn as overlay. Therefore, this
        method can be easily used inside overlay call as well as alone.
        
        Args:
            canvas: pero.Canvas
                Canvas to draw the graphics on.
            
            source: any
                Data source to be used for calculating callable properties of
                current tooltip glyph.
            
            overrides: str:any pairs
                Specific properties of the tooltip to be overwritten.
        """
        
        # check parent
        if self._parent is None:
            return
        
        # skip tooltip
        if self.tooltip is None:
            return
        
        # use system tooltip
        if self.tooltip is UNDEF:
            self._parent.draw_tooltip(text=overrides.get('text', ""))
            return
        
        # initialize canvas
        if canvas is None:
            self.draw_overlay(self.draw_tooltip, source=source, **overrides)
            return
        
        # get clip frame
        if self.tooltip.clip is UNDEF and 'clip' not in overrides:
            overrides['clip'] = Frame(0, 0, *self._size)
        
        # draw tooltip
        self.tooltip.draw(canvas, source=source, **overrides)
    
    
    def _set_tool(self, new_tool, old_tool=None, left=False, right=False, touch=False):
        """Registers given tool."""
        
        # unbind old tool
        if old_tool:
            self.unbind(EVT_SIZE, old_tool.on_size)
            self.unbind(EVT_KEY_DOWN, old_tool.on_key_down)
            self.unbind(EVT_KEY_UP, old_tool.on_key_up)
            self.unbind(EVT_MOUSE_ENTER, old_tool.on_mouse_enter)
            self.unbind(EVT_MOUSE_LEAVE, old_tool.on_mouse_leave)
            self.unbind(EVT_MOUSE_MOTION, old_tool.on_mouse_motion)
            self.unbind(EVT_MOUSE_SCROLL, old_tool.on_mouse_scroll)
            self.unbind(EVT_LEFT_DOWN, old_tool.on_mouse_down)
            self.unbind(EVT_LEFT_UP, old_tool.on_mouse_up)
            self.unbind(EVT_LEFT_DCLICK, old_tool.on_mouse_dclick)
            self.unbind(EVT_RIGHT_DOWN, old_tool.on_mouse_down)
            self.unbind(EVT_RIGHT_UP, old_tool.on_mouse_up)
            self.unbind(EVT_TOUCH_START, old_tool.on_touch_start)
            self.unbind(EVT_TOUCH_END, old_tool.on_touch_end)
            self.unbind(EVT_TOUCH_MOVE, old_tool.on_touch_move)
            self.unbind(EVT_TOUCH_CANCEL, old_tool.on_touch_cancel)
            self.unbind(EVT_TOUCH_DTAP, old_tool.on_touch_dtap)
        
        # check tool
        if not new_tool:
            return
        
        # bind common events
        self.bind(EVT_SIZE, new_tool.on_size)
        
        # bind key events
        self.bind(EVT_KEY_DOWN, new_tool.on_key_down)
        self.bind(EVT_KEY_UP, new_tool.on_key_up)
        
        # bind main mouse events
        self.bind(EVT_MOUSE_ENTER, new_tool.on_mouse_enter)
        self.bind(EVT_MOUSE_LEAVE, new_tool.on_mouse_leave)
        self.bind(EVT_MOUSE_MOTION, new_tool.on_mouse_motion)
        self.bind(EVT_MOUSE_SCROLL, new_tool.on_mouse_scroll)
        
        # bind left mouse events
        if left:
            self.bind(EVT_LEFT_DOWN, new_tool.on_mouse_down)
            self.bind(EVT_LEFT_UP, new_tool.on_mouse_up)
            self.bind(EVT_LEFT_DCLICK, new_tool.on_mouse_dclick)
        
        # bind right mouse events
        if right:
            self.bind(EVT_RIGHT_DOWN, new_tool.on_mouse_down)
            self.bind(EVT_RIGHT_UP, new_tool.on_mouse_up)
            self.bind(EVT_RIGHT_DCLICK, new_tool.on_mouse_dclick)
        
        # bind touch events
        if touch:
            self.bind(EVT_TOUCH_START, new_tool.on_touch_start)
            self.bind(EVT_TOUCH_END, new_tool.on_touch_end)
            self.bind(EVT_TOUCH_MOVE, new_tool.on_touch_move)
            self.bind(EVT_TOUCH_CANCEL, new_tool.on_touch_cancel)
            self.bind(EVT_TOUCH_DTAP, new_tool.on_touch_dtap)
    
    
    def _on_tool_control_property_changed(self, evt):
        """Called after any property has changed."""
        
        # main tool changed
        if evt.name == 'main_tool':
            self._set_tool(evt.new_value, evt.old_value, left=True, right=True, touch=True)
        
        # cursor tool changed
        elif evt.name == 'cursor_tool':
            self._set_tool(evt.new_value, evt.old_value)
        
        # left mouse tool changed
        elif evt.name == 'left_tool':
            self._set_tool(evt.new_value, evt.old_value, left=True)
        
        # right mouse tool changed
        elif evt.name == 'right_tool':
            self._set_tool(evt.new_value, evt.old_value, right=True)
        
        # touch tool changed
        elif evt.name == 'touch_tool':
            self._set_tool(evt.new_value, evt.old_value, touch=True)
