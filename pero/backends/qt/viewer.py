#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout
from ... drawing import Graphics
from .. view import Control
from . view import QtView


class QtViewer(QWidget):
    """Simple graphics viewer application."""
    
    
    def __init__(self):
        """Initializes a new instance of QtViewer."""
        
        # init base
        super().__init__()
        self.setWindowTitle("Pero")
        self.resize(750, 500)
        
        # init layout
        self._sizer = QHBoxLayout()
        self._sizer.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._sizer)
        
        # init view
        self._view = None
    
    
    def set_size(self, size):
        """
        Sets app window size.
        
        Args:
            size: (float, float)
                App window size as (width, height).
        """
        
        # set size
        self.resize(size[0], size[1])
        
        # center on screen
        geo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        geo.moveCenter(center)
        self.move(geo.topLeft())
    
    
    def set_title(self, title):
        """
        Sets app window title.
        
        Args:
            title: str
                App window title.
        """
        
        self.setWindowTitle(title or "")
    
    
    def set_content(self, content):
        """
        Sets content to draw.
        
        Args:
            content: pero.QtView, pero.Control or pero.Graphics
                A content to set.
        """
        
        # clean sizer
        if self._view is not None:
            self._sizer.removeWidget(self._view)
        
        # init view
        if isinstance(content, QtView):
            self._view = content
        
        elif isinstance(content, Control):
            self._view = QtView(self)
            self._view.set_control(content)
        
        elif isinstance(content, Graphics):
            self._view = QtView(self)
            self._view.set_control(Control(graphics=content))
        
        else:
            message = "Unknown content type! -> %s" % type(content)
            raise TypeError(message)
        
        # add to sizer
        self._sizer.addWidget(self._view, 1)
    
    
    def refresh(self):
        """Redraws graphics."""
        
        if self._view is not None:
            self._view.refresh()
