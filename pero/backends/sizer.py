#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Layout
from . control import Control


class Sizer(Control):
    """
    Sizer encapsulates the pero.Layout and relays all interactive events and
    drawing mechanism down to individual cells. It allows interactive controls
    to be drawn in specific layout.
    
    Properties:
        
        graphics: pero.Layout
            Layout drawing tool.
    """
    
    graphics = Property(UNDEF, types=Layout, dynamic=False, nullable=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Sizer."""
        
        # init base
        super().__init__(**overrides)
        
        # init buffs
        self._focused = None
        
        # init layout
        if not self.graphics:
            self.graphics = Layout()
        
        # lock layout
        self.lock_property('graphics')
        
        # bind events
        self.bind(EVT_SIZE, self._on_sizer_event)
        self.bind(EVT_KEY_DOWN, self._on_sizer_event)
        self.bind(EVT_KEY_UP, self._on_sizer_event)
        self.bind(EVT_MOUSE_ENTER, self._on_sizer_event)
        self.bind(EVT_MOUSE_LEAVE, self._on_sizer_event)
        self.bind(EVT_MOUSE_MOTION, self._on_sizer_event)
        self.bind(EVT_MOUSE_SCROLL, self._on_sizer_event)
        self.bind(EVT_LEFT_DOWN, self._on_sizer_event)
        self.bind(EVT_LEFT_UP, self._on_sizer_event)
        self.bind(EVT_LEFT_DCLICK, self._on_sizer_event)
        self.bind(EVT_RIGHT_DOWN, self._on_sizer_event)
        self.bind(EVT_RIGHT_UP, self._on_sizer_event)
        self.bind(EVT_TOUCH_START, self._on_sizer_event)
        self.bind(EVT_TOUCH_END, self._on_sizer_event)
        self.bind(EVT_TOUCH_MOVE, self._on_sizer_event)
        self.bind(EVT_TOUCH_CANCEL, self._on_sizer_event)
        self.bind(EVT_TOUCH_DTAP, self._on_sizer_event)
    
    
    def get_cell(self, row, col):
        """
        Gets the cell at specified layout grid position.
        
        Args:
            row: int
                Row index of requested cell.
            
            col: int
                Column index of requested cell.
        
        Returns:
            pero.Cell or None
                Corresponding cell or None.
        """
        
        return self.graphics.get_cell(row, col)
    
    
    def get_cell_below(self, x, y):
        """
        Gets the cell for which given coordinates fall into its bounding box.
        
        Args:
            x: int or float
                X-coordinate in logical units.
            
            y: int or float
                Y-coordinate in logical units.
        
        Returns:
            pero.Cell or None
                Corresponding cell or None.
        """
        
        return self.graphics.get_cell_below(x, y)
    
    
    def add(self, graphics, row, col, **overrides):
        """
        Adds graphics to specified layout cell. Additional rows and columns are
        added if necessary with relative size of 1. See pero.Layout for more.
        
        Args:
            graphics: pero.Graphics
                Graphics to be added.
            
            row: int
                Index of the row into which the graphics should be added.
            
            col: int
                Index of the column into which the graphics should be added.
            
            overrides: (str:?)
                Additional cell properties.
        """
        
        # set parent for controls
        if isinstance(graphics, Control):
            graphics.set_parent(self)
        
        # add to layout
        self.graphics.add(graphics, row, col, **overrides)
    
    
    def add_row(self, height=1, relative=True):
        """
        Adds additional row at the end of layout with specified absolute or
        relative height.
        
        Args:
            height: int or float
                Absolute or relative height of the row.
            
            relative:
                If set to True, specified height is considered as relative
                portion of total available space after filling all fixed rows.
        """
        
        # add to layout
        self.graphics.add_row(height, relative)
    
    
    def add_col(self, width=1, relative=True):
        """
        Adds additional column at the end of layout with specified absolute or
        relative width.
        
        Args:
            width: int or float
                Absolute or relative width of the column.
            
            relative:
                If set to True, specified width is considered as relative
                portion of total available space after filling all fixed
                columns.
        """
        
        # add to layout
        self.graphics.add_col(width, relative)
    
    
    def draw_overlay(self, func=None, view=None, **kwargs):
        """Relays overlay drawing to parent."""
        
        # check parent
        if self._parent is None:
            return
        
        # get cell view shift
        view = None
        if self._focused:
            view = self._focused.content.rect
        
        # draw overlay by parent
        self._parent.draw_overlay(func, view, **kwargs)
    
    
    def _on_sizer_event(self, evt):
        """Relay events to focused control."""
        
        # process cursor event
        if hasattr(evt, 'x_pos') and hasattr(evt, 'y_pos'):
            
            # get item under cursor
            self._focused = self.graphics.get_cell_below(evt.x_pos, evt.y_pos)
            if self._focused is None:
                return
            
            # reset event position
            evt.x_pos, evt.y_pos = self._focused.to_content(evt.x_pos, evt.y_pos)
        
        # skip if no cell in focus
        if self._focused is None:
            return
        
        # reset event control
        if hasattr(evt, 'control'):
            evt.control = self._focused.graphics
        
        # raise event in focused item
        self._focused.graphics.fire(evt)
