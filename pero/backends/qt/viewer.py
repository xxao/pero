#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout

from .view import QtView


class QtViewer(QWidget):
    """Simple graphics viewer application."""
    
    
    def __init__(self):
        """Initializes a new instance of QtViewer."""
        
        # init base
        super(QtViewer, self).__init__()
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
    
    
    def set_graphics(self, graphics):
        """
        Sets graphics to draw.
        
        Args:
            graphics: pero.QtView or pero.Graphics
        """
        
        # init view
        if isinstance(graphics, QtView):
            self._view = graphics
        else:
            self._view = QtView(self)
            self._view.graphics = graphics
        
        # clean sizer
        if self._view is not None:
            self._sizer.removeWidget(self._view)
        
        # add to sizer
        self._sizer.addWidget(self._view, 1)
    
    
    def refresh(self):
        """Redraws graphics."""
        
        if self._view is not None:
            self._view.refresh()
