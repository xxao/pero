#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import sys
from ..enums import *
from ..properties import *
from ..drawing import Graphics, Tooltip
from .tool import Tool


class View(PropertySet):
    """
    Abstract base class for interactive views.
    
    Properties:
        
        graphics: pero.Graphics, None or UNDEF
            Main graphics to display within the view.
        
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
    
    
    def __init__(self):
        """Initializes a new instance of View."""
        
        super(View, self).__init__()
        
        # init tooltip glyph
        if self.tooltip is UNDEF:
            self.tooltip = Tooltip()
        
        # bind events
        self.bind(EVENT.PROPERTY_CHANGED, self._on_view_property_changed)
    
    
    def set_cursor(self, cursor):
        """
        This method should be overridden to provide specific mechanism to set
        given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set. The value must be an item from the
                pero.CURSOR enum.
        """
        
        raise NotImplementedError("The 'set_cursor' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def refresh(self, **overrides):
        """
        Refreshes current view by calling the draw method.
        
        Args:
            overrides: str:any pairs
                Specific properties of current graphics to be overwritten.
        """
        
        self.draw(**overrides)
    
    
    def draw(self, canvas=None, **overrides):
        """
        This method should be overridden to provide specific drawing mechanism
        and canvas creation to finally draw current graphics.
        
        The overrides values should be directly forwarded into current graphics
        drawing method.
        
        Args:
            canvas: pero.Canvas or None
                Specific canvas to draw the graphics on.
            
            overrides: str:any pairs
                Specific properties of current graphics to be overwritten.
        """
        
        raise NotImplementedError("The 'draw' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_tooltip(self, canvas, **overrides):
        """
        Draws a tooltip either by custom glyph specified by the 'tooltip'
        property or using a system method.
        
        If the custom glyph is used all the overrides are given directly to its
        drawing method (e.g. to display specific text use text='my tooltip').
        For the system tooltip actual text is also retrieved from given
        overrides assuming the 'text' key is used.
        
        Args:
            canvas: pero.Canvas
                Canvas to draw the graphics on.
            
            overrides: str:any pairs
                Specific properties of the tooltip to be overwritten.
        """
        
        # skip tooltip
        if self.tooltip is None:
            return
        
        # use custom tooltip
        if self.tooltip is not UNDEF:
            self.tooltip.draw(canvas, **overrides)
            return
        
        # extract text
        text = overrides.get('text', "")
        
        # use system tooltip
        if text:
            self.draw_system_tooltip(text)
    
    
    def draw_system_tooltip(self, text):
        """
        This method should be overridden to show given text using a system
        tooltip.
        
        Args:
            text: str
                Tooltip text to be shown.
        """
        
        raise NotImplementedError("The 'draw_system_tooltip' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_overlay(self, func=None, **overrides):
        """
        This method should be overridden to provide specific drawing mechanism
        and canvas creation to finally call given function to draw cursor rubber
        band overlay over the current graphics.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given overrides (i.e. func(canvas, **overrides)).
        
        It is expected that current overlay is just cleared if this method is
        called without any parameter.
        
        Args:
            func: callable or None
                Method to be called to draw the overlay.
                
            overrides: str:any pairs
                Specific properties of the drawing method to be overwritten.
        """
        
        raise NotImplementedError("The 'draw_overlay' method is not implemented for '%s'." % self.__class__.__name__)
    
    
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
    
    
    def _on_view_property_changed(self, evt):
        """Called after any property has changed."""
        
        # main tool changed
        if evt.name == 'main_tool':
            self._set_tool(evt.new_value, evt.old_value, True, True)
        
        # cursor tool changed
        if evt.name == 'cursor_tool':
            self._set_tool(evt.new_value, evt.old_value, False, False)
        
        # left mouse tool changed
        elif evt.name == 'left_tool':
            self._set_tool(evt.new_value, evt.old_value, True, False)
        
        # right mouse tool changed
        elif evt.name == 'right_tool':
            self._set_tool(evt.new_value, evt.old_value, False, True)
