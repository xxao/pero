#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import wx
from ... events import *
from .. view import View
from . enums import *
from . canvas import WXCanvas


class WXView(wx.Window, View, metaclass=type('WXViewMeta', (type(wx.Window), type(View)), {})):
    """Wrapper for wxPython View."""
    
    
    def __init__(self, parent, id=-1, size=wx.DefaultSize, style=wx.WANTS_CHARS):
        """Initializes a new instance of WXView."""
        
        # init base
        wx.Window.__init__(self, parent, id, size=size, style=style)
        View.__init__(self)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        # init buffers
        self._dc_buffer = wx.Bitmap(*self.GetClientSize())
        self._dc_overlay = wx.Overlay()
        self._dc_overlay_empty = True
        self._use_buffer = wx.Platform == '__WXMSW__'
        
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
    
    
    def set_cursor(self, cursor):
        """
        Sets given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set as any item from the pero.CURSOR enum.
        """
        
        # get wx cursor
        wx_cursor = cursor
        
        if wx_cursor in WX_CURSORS:
            wx_cursor = WX_CURSORS[wx_cursor]
        
        if not isinstance(wx_cursor, wx.Cursor):
            wx_cursor = wx.Cursor(wx_cursor)
        
        # set cursor
        self.SetCursor(wx_cursor)
    
    
    def set_tooltip(self, text):
        """
        Sets given text as a system tooltip.
        
        Args:
            text: str
                Tooltip text to be set.
        """
        
        self.SetToolTip(text)
    
    
    def draw_control(self):
        """Draws current control graphics."""
        
        # check control
        if self.control is None:
            return
        
        # draw into buffer
        if self._use_buffer:
            
            # init DC
            dc = wx.MemoryDC()
            dc.SelectObject(self._dc_buffer)
            
            # init canvas
            canvas = self._make_canvas(dc)
            
            # draw control
            self.control.draw(canvas)
            
            # reset overlay
            if not self._dc_overlay_empty:
                self._dc_overlay.Reset()
            
            # delete DC
            dc.SelectObject(wx.NullBitmap)
            del dc
        
        # update screen
        self.Refresh(eraseBackground=False)
        self.Update()
    
    
    def draw_overlay(self, func=None, **kwargs):
        """
        Draws cursor rubber band overlay.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given overrides (i.e. func(canvas, **kwargs)).
        If the 'func' parameter is set to None current overlay is cleared.
        
        Args:
            func: callable or None
                Drawing function to be called to draw the overlay. If set to
                None, current overlay will be cleared.
                
            kwargs: str:any pairs
                Keyword arguments, which should be provided to the given drawing
                function.
        """
        
        # check control
        if self.control is None:
            return
        
        # do not clean if empty
        if func is None and self._dc_overlay_empty:
            return
        
        # clear current tooltip
        self.SetToolTip("")
        
        # make overlay DC
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self._dc_overlay, dc)
        odc.Clear()
        
        # draw overlay
        if func is not None:
            canvas = self._make_canvas(dc)
            func(canvas, **kwargs)
            self._dc_overlay_empty = False
        
        # delete DC
        del odc
    
    
    def _on_paint(self, evt):
        """Repaints current graphics."""
        
        # draw buffer on screen
        if self._use_buffer:
            wx.BufferedPaintDC(self, self._dc_buffer)
        
        # draw directly
        else:
            dc = wx.PaintDC(self)
            canvas = self._make_canvas(dc)
            self.control.draw(canvas)
            self._dc_overlay.Reset()
    
    
    def _on_size(self, evt):
        """Repaints current graphics when size has changed."""
        
        # get window size
        width, height = self.GetClientSize()
        width = max(1, width)
        height = max(1, height)
        
        # init new buffer
        if self._use_buffer:
            self._dc_buffer = wx.Bitmap(width, height)
        
        # make size event
        size_evt = SizeEvt(
            
            native = evt,
            view = self,
            control = self.control,
            
            width = width,
            height = height)
        
        # fire event
        if self.control is not None:
            self.control.fire(size_evt)
    
    
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
            control = self.control,
            
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
        if self.control is not None:
            self.control.fire(key_evt)
    
    
    def _on_mouse(self, evt):
        """Handles all mouse events."""
        
        # get position
        x, y = evt.GetPosition()
        
        # get wheel rotation
        if evt.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL:
            x_rot = evt.GetWheelRotation()
            y_rot = 0
        else:
            x_rot = 0
            y_rot = evt.GetWheelRotation()
        
        # init base event
        mouse_evt = MouseEvt(
            
            native = evt,
            view = self,
            control = self.control,
            
            x_pos = x,
            y_pos = y,
            
            x_rot = x_rot,
            y_rot = y_rot,
            
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
        if self.control is not None:
            self.control.fire(mouse_evt)
    
    
    def _make_canvas(self, dc):
        """Makes canvas using given DC."""
        
        # use GCDC
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)
        
        # make canvas
        return WXCanvas(dc)
