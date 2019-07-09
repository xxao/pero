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
        
        # init buffers
        self._cursor = CURSOR.ARROW
    
    
    def paintEvent(self, evt):
        """Redraws the view."""
        
        self._on_paint(evt)
    
    
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
        
        # get qt cursor
        qt_cursor = cursor
        if qt_cursor in QT_CURSORS:
            qt_cursor = QT_CURSORS[qt_cursor]
        
        # set cursor
        self.setCursor(qt_cursor)
        
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
        
        # update screen
        self.repaint()
    
    
    def draw_system_tooltip(self, text):
        """
        Shows given text as a system tooltip.
        
        Args:
            text: str
                Tooltip text to be shown.
        """
        
        self.setToolTip(text)
    
    
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
        
        pass
    
    
    def _on_paint(self, evt):
        """Repaints current graphics."""
        
        # init painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # init canvas
        canvas = QtCanvas(qp)
        
        # draw
        self.draw(canvas)
        
        # end drawing
        qp.end()
