#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter

from ...events import *
from ..view import View
from .enums import *
from .canvas import QtCanvas


class QtView(QWidget, View, metaclass=type('QWidgetMeta', (type(QWidget), type(View)), {})):
    """Wrapper for QWidget View."""
    
    
    def __init__(self, parent=None):
        """Initializes a new instance of QtView."""
        
        # init base
        super(QtView, self).__init__(parent)
        View.__init__(self)
        self.setMouseTracking(True)
        
        # set window events
        self.paintEvent = self._on_paint
        self.resizeEvent = self._on_size
        
        self.keyPressEvent = self._on_key_down
        self.keyReleaseEvent = self._on_key_up
        
        self.mouseMoveEvent = self._on_mouse_move
        self.wheelEvent = self._on_mouse_wheel

        self.enterEvent = self._on_mouse_enter
        self.leaveEvent = self._on_mouse_leave
        
        self.mousePressEvent = self._on_mouse_down
        self.mouseReleaseEvent = self._on_mouse_up
        self.mouseDoubleClickEvent = self._on_mouse_dclick
    
    
    def set_cursor(self, cursor):
        """
        Sets given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set as any item from the pero.CURSOR enum.
        """
        
        # get qt cursor
        qt_cursor = cursor
        if qt_cursor in QT_CURSORS:
            qt_cursor = QT_CURSORS[qt_cursor]
        
        # set cursor
        self.setCursor(qt_cursor)
    
    
    def set_tooltip(self, text):
        """
        Sets given text as a system tooltip.
        
        Args:
            text: str
                Tooltip text to be shown.
        """
        
        self.setToolTip(text)
    
    
    def draw_control(self, canvas=None):
        """
        Draws current control graphics into specified or newly created canvas.
        
        Args:
            canvas: pero.Canvas or None
                Specific canvas to draw the control on. If se to None, this
                method is responsible to initialize one.
        """
        
        # check control
        if self.control is None:
            return
        
        # draw to given canvas
        if canvas is not None:
            self.control.draw(canvas)
            return
        
        # update screen
        self.repaint()
    
    
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
        
        pass
    
    
    def _init_view_event(self, evt):
        """Initialize view event."""
        
        # init base event
        view_evt = ViewEvt(
            
            native = evt,
            view = self,
            control = self.control)
        
        return view_evt
    
    
    def _init_key_event(self, evt):
        """Initialize key event."""
        
        # init base event
        key_evt = KeyEvt(
            
            native = evt,
            view = self,
            control = self.control,
            
            key = evt.key(),
            char = evt.text(),
            
            alt_down = bool(evt.modifiers() & Qt.AltModifier),
            cmd_down = bool(evt.modifiers() & Qt.ControlModifier),
            ctrl_down = bool(evt.modifiers() & Qt.ControlModifier),
            shift_down = bool(evt.modifiers() & Qt.ShiftModifier))
        
        return key_evt
    
    
    def _init_mouse_event(self, evt):
        """Initialize mouse event."""
        
        # init base event
        mouse_evt = MouseEvt(
            
            native = evt,
            view = self,
            control = self.control,
            
            x_pos = evt.x(),
            y_pos = evt.y(),
            
            left_down = bool(evt.buttons() & Qt.LeftButton),
            middle_down = bool(evt.buttons() & Qt.MiddleButton),
            right_down = bool(evt.buttons() & Qt.RightButton),
            
            alt_down = bool(evt.modifiers() & Qt.AltModifier),
            cmd_down = bool(evt.modifiers() & Qt.ControlModifier),
            ctrl_down = bool(evt.modifiers() & Qt.ControlModifier),
            shift_down = bool(evt.modifiers() & Qt.ShiftModifier))
        
        return mouse_evt
    
    
    def _on_paint(self, evt):
        """Repaints current graphics."""
        
        # init painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # init canvas
        canvas = QtCanvas(qp)
        
        # draw control
        self.draw_control(canvas)
        
        # end drawing
        qp.end()
    
    
    def _on_size(self, evt):
        """Repaints current graphics when size has changed."""
        
        # get window size
        size = evt.size()
        width = max(1, size.width())
        height = max(1, size.height())
        
        # draw control
        self.draw_control()
        
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
    
    
    def _on_key_down(self, evt):
        """Handles key down event."""
        
        # init base event
        key_evt = self._init_key_event(evt)
        
        # make specific event type
        key_evt = KeyDownEvt.from_evt(key_evt)
        key_evt.pressed = True
        
        # fire event
        if self.control is not None:
            self.control.fire(key_evt)
    
    
    def _on_key_up(self, evt):
        """Handles key up event."""
        
        # init base event
        key_evt = self._init_key_event(evt)
        
        # make specific event type
        key_evt = KeyUpEvt.from_evt(key_evt)
        key_evt.pressed = False
        
        # fire event
        if self.control is not None:
            self.control.fire(key_evt)
    
    
    def _on_mouse_move(self, evt):
        """Handles mouse move event."""
        
        # init base event
        mouse_evt = self._init_mouse_event(evt)
        
        # make specific event type
        mouse_evt = MouseMotionEvt.from_evt(mouse_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(mouse_evt)
    
    
    def _on_mouse_wheel(self, evt):
        """Handles mouse wheel event."""
        
        # get rotation
        rotation = evt.angleDelta()
        
        # skip if no rotation
        if rotation.x() == 0 and rotation.y() == 0:
            return
        
        # init base event
        mouse_evt = self._init_mouse_event(evt)
        
        # make specific event type
        mouse_evt = MouseScrollEvt.from_evt(mouse_evt)
        mouse_evt.x_rot = rotation.x()
        mouse_evt.y_rot = rotation.y()
        
        # fire event
        if self.control is not None:
            self.control.fire(mouse_evt)
    
    
    def _on_mouse_enter(self, evt):
        """Handles mouse enter event."""
        
        # init base event
        view_evt = self._init_view_event(evt)
        
        # make specific event type
        view_evt = MouseEnterEvt.from_evt(view_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(view_evt)
    
    
    def _on_mouse_leave(self, evt):
        """Handles mouse leave event."""
        
        # init base event
        view_evt = self._init_view_event(evt)
        
        # make specific event type
        view_evt = MouseLeaveEvt.from_evt(view_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(view_evt)
    
    
    def _on_mouse_down(self, evt):
        """Handles mouse button down event."""
        
        # init base event
        mouse_evt = self._init_mouse_event(evt)
        
        # make specific event type
        if evt.button() == Qt.LeftButton:
            mouse_evt = LeftDownEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.MiddleButton:
            mouse_evt = MiddleDownEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.RightButton:
            mouse_evt = RightDownEvt.from_evt(mouse_evt)
        
        # set focus
        self.setFocus(Qt.MouseFocusReason)
        
        # fire event
        if self.control is not None:
            self.control.fire(mouse_evt)
    
    
    def _on_mouse_up(self, evt):
        """Handles mouse button up event."""
        
        # init base event
        mouse_evt = self._init_mouse_event(evt)
        
        # make specific event type
        if evt.button() == Qt.LeftButton:
            mouse_evt = LeftUpEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.MiddleButton:
            mouse_evt = MiddleUpEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.RightButton:
            mouse_evt = RightUpEvt.from_evt(mouse_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(mouse_evt)
    
    
    def _on_mouse_dclick(self, evt):
        """Handles mouse button double-click event."""
        
        # init base event
        mouse_evt = self._init_mouse_event(evt)
        
        # make specific event type
        if evt.button() == Qt.LeftButton:
            mouse_evt = LeftDClickEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.MiddleButton:
            mouse_evt = MiddleDClickEvt.from_evt(mouse_evt)
        
        elif evt.button() == Qt.RightButton:
            mouse_evt = RightDClickEvt.from_evt(mouse_evt)
        
        # fire event
        if self.control is not None:
            self.control.fire(mouse_evt)
