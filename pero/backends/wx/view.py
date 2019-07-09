#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from ...events import *
from ..view import View
from .enums import *
from .canvas import WXCanvas


class WXView(wx.Window, View, metaclass=type('WXViewMeta', (type(wx.Window), type(View)), {})):
    """Wrapper for wxPython View."""
    
    
    def __init__(self, parent, id=-1, size=wx.DefaultSize, style=wx.WANTS_CHARS):
        """Initializes a new instance of WXView."""
        
        # init base
        wx.Window.__init__(self, parent, id, size=size, style=style)
        View.__init__(self)
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        # init buffers
        self._dc_buffer = None
        self._dc_overlay = wx.Overlay()
        self._dc_overlay_empty = True
        self._dc_size = None
        self._use_buffer = wx.Platform == '__WXMSW__'
        self._cursor = CURSOR.ARROW
        
        # set window events
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_SIZE, self._on_size)
        
        self.Bind(wx.EVT_KEY_DOWN, self._on_key)
        self.Bind(wx.EVT_KEY_UP, self._on_key)
        
        self.Bind(wx.EVT_MOTION, self._on_mouse)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse)
        
        self.Bind(wx.EVT_LEFT_DOWN, self._on_mouse)
        self.Bind(wx.EVT_LEFT_UP, self._on_mouse)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_mouse)
        
        self.Bind(wx.EVT_MIDDLE_DOWN, self._on_mouse)
        self.Bind(wx.EVT_MIDDLE_UP, self._on_mouse)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self._on_mouse)
        
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_mouse)
        self.Bind(wx.EVT_RIGHT_UP, self._on_mouse)
        self.Bind(wx.EVT_RIGHT_DCLICK, self._on_mouse)
        
        # init buffer
        self._on_size(None)
    
    
    def set_cursor(self, cursor):
        """
        Sets given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set as any item from the pero.CURSOR enum.
        """
        
        # check current
        if self._cursor == cursor:
            return
        
        # get wx cursor
        wx_cursor = cursor
        
        if wx_cursor in WX_CURSORS:
            wx_cursor = WX_CURSORS[wx_cursor]
        
        if not isinstance(wx_cursor, wx.Cursor):
            wx_cursor = wx.Cursor(wx_cursor)
        
        # set cursor
        self.SetCursor(wx_cursor)
        
        # remember cursor
        self._cursor = cursor
    
    
    def draw(self, canvas=None, **overrides):
        """
        Draws current graphics into specified or newly created canvas.
        
        Args:
            canvas: pero.Canvas or None
                Specific canvas to draw the graphics on.
            
            overrides: str:any pairs
                Specific properties of current graphics to be overwritten.
        """
        
        # check graphics
        if not self.graphics:
            return
        
        # draw to given canvas
        if canvas is not None:
            self.graphics.draw(canvas, **overrides)
            return
        
        # draw into buffer
        if self._use_buffer:
            
            # init DC
            dc = wx.MemoryDC()
            dc.SelectObject(self._dc_buffer)
            
            # init canvas
            canvas = self._make_canvas(dc)
            
            # draw graphics
            self.graphics.draw(canvas, **overrides)
            del dc
            
            # reset overlay
            self._dc_overlay.Reset()
        
        # update screen
        self.Refresh(eraseBackground=False)
        self.Update()
    
    
    def draw_system_tooltip(self, text):
        """
        Shows given text as a system tooltip.
        
        Args:
            text: str
                Tooltip text to be shown.
        """
        
        self.SetToolTip(text)
    
    
    def draw_overlay(self, func=None, **overrides):
        """
        Draws cursor rubber band overlay.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given overrides (i.e. func(canvas, **overrides)).
        If the 'func' parameter is set to None current overlay is cleared.
        
        Args:
            func: callable or None
                Method to be called to draw the overlay or None to clear
                current.
                
            overrides: str:any pairs
                Specific properties of the drawing method to be overwritten.
        """
        
        # do not clean if empty
        if func is None and self._dc_overlay_empty:
            return
        
        # clear current tooltip
        self.SetToolTip("")
        
        # disable overlay on Mac until it is working
        # if wx.Platform == "__WXMAC__":
        #     return
        
        # make and clear overlay DC
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self._dc_overlay, dc)
        odc.Clear()
        
        # check function
        if func is None:
            del odc
            return
        
        # make canvas
        canvas = self._make_canvas(dc)
        
        # draw overlay
        func(canvas, **overrides)
        self._dc_overlay_empty = False
        
        # delete overlay DC
        del odc
    
    
    def _on_paint(self, evt):
        """Repaints current graphics."""
        
        # draw buffer on screen
        if self._use_buffer:
            dc = wx.BufferedPaintDC(self, self._dc_buffer)
        
        # draw directly
        else:
            dc = wx.PaintDC(self)
            canvas = self._make_canvas(dc)
            self.draw(canvas)
            self._dc_overlay.Reset()
    
    
    def _on_size(self, evt):
        """Repaints current graphics when size has changed."""
        
        # get window size
        width, height = self.GetClientSize()
        width = max(1, width)
        height = max(1, height)
        
        # remember current size
        self._dc_size = (width, height)
        
        # make new off-screen bitmap
        self._dc_buffer = wx.Bitmap(width, height)
        
        # draw graphics
        self.draw()
        
        # make size event
        size_evt = SizeEvt(
            
            native = evt,
            view = self,
            graphics = self.graphics,
            
            width = width,
            height = height)
        
        # fire event
        self.fire(size_evt)
    
    
    def _on_key(self, evt):
        """Handles all key events."""
        
        # get Unicode key
        key = evt.GetUnicodeKey()
        if key != wx.WXK_NONE:
            char = chr(key)
        else:
            key = evt.GetKeyCode()
            char = None
        
        # convert to known key
        if key in WX_KEYS:
            key = WX_KEYS[key]
        
        # init base event
        key_evt = KeyEvt(
            
            native = evt,
            view = self,
            graphics = self.graphics,
            
            key = key,
            char = char,
            
            alt_down = evt.AltDown(),
            cmd_down = evt.CmdDown(),
            ctrl_down = evt.ControlDown(),
            shift_down = evt.ShiftDown())
        
        # get event type
        evt_type = evt.GetEventType()
        
        # make specific event type
        if evt_type == wx.wxEVT_KEY_DOWN:
            key_evt = KeyDownEvt.from_evt(key_evt)
        
        elif evt_type == wx.wxEVT_KEY_UP:
            key_evt = KeyUpEvt.from_evt(key_evt)
        
        # fire event
        self.fire(key_evt)
    
    
    def _on_mouse(self, evt):
        """Handles all mouse events."""
        
        # get position
        x, y = evt.GetPosition()
        
        # init base event
        mouse_evt = MouseEvt(
            
            native = evt,
            view = self,
            graphics = self.graphics,
            
            x_pos = x,
            y_pos = y,
            
            x_rot = evt.GetWheelRotation(),
            
            left_down = evt.LeftIsDown(),
            middle_down = evt.MiddleIsDown(),
            right_down = evt.RightIsDown(),
            
            alt_down = evt.AltDown(),
            cmd_down = evt.CmdDown(),
            ctrl_down = evt.ControlDown(),
            shift_down = evt.ShiftDown())
        
        # get event type
        evt_type = evt.GetEventType()
        
        # make specific event type
        if evt_type == wx.wxEVT_MOTION:
            mouse_evt = MouseMotionEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_MOUSEWHEEL:
            mouse_evt = MouseScrollEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_LEAVE_WINDOW:
            mouse_evt = MouseLeaveEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_LEFT_DOWN:
            mouse_evt = LeftDownEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_LEFT_UP:
            mouse_evt = LeftUpEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_LEFT_DCLICK:
            mouse_evt = LeftDClickEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_MIDDLE_DOWN:
            mouse_evt = MiddleDownEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_MIDDLE_UP:
            mouse_evt = MiddleUpEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_MIDDLE_DCLICK:
            mouse_evt = MiddleDClickEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_RIGHT_DOWN:
            mouse_evt = RightDownEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_RIGHT_UP:
            mouse_evt = RightUpEvt.from_evt(mouse_evt)
        
        elif evt_type == wx.wxEVT_RIGHT_DCLICK:
            mouse_evt = RightDClickEvt.from_evt(mouse_evt)
        
        # set focus
        if self.FindFocus() is not self and \
            evt_type in (wx.wxEVT_LEFT_DOWN, wx.wxEVT_LEFT_DCLICK,
                wx.wxEVT_MIDDLE_DOWN, wx.wxEVT_MIDDLE_DCLICK,
                wx.wxEVT_RIGHT_DOWN, wx.wxEVT_RIGHT_DCLICK):
            
            self.SetFocus()
            try: wx.Yield()
            except: pass
        
        # fire event
        self.fire(mouse_evt)
    
    
    def _make_canvas(self, dc):
        """Makes canvas using given DC."""
        
        # use GCDC
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)
        
        # make canvas
        return WXCanvas(dc)
