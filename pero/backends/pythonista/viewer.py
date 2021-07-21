#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import ui
from ... drawing import Graphics
from .. view import Control
from . view import UIView


class UIViewer(ui.View):
    """Simple graphics viewer application."""
    
    
    def __init__(self, **kwargs):
        """Initializes a new instance of UIViewer."""
        
        # init base
        super().__init__(**kwargs)
        self.name = "Pero"
        
        # init view
        self._view = None
    
    
    def set_size(self, size):
        """
        Sets app window size.
        
        Args:
            size: (float, float)
                App window size as (width, height).
        """
        
        self.width = size[0]
        self.height = size[1]
    
    
    def set_title(self, title):
        """
        Sets app window title.
        
        Args:
            title: str
                App window title.
        """
        
        self.name = title or ""
    
    
    def set_content(self, content):
        """
        Sets content to draw.
        
        Args:
            content: pero.UIView, pero.Control or pero.Graphics
                A content to set.
        """
        
        # clean sizer
        if self._view is not None:
            self.remove_subview(self._view)
        
        # init view
        if isinstance(content, UIView):
            self._view = content
        
        elif isinstance(content, Control):
            self._view = UIView()
            self._view.set_control(content)
        
        elif isinstance(content, Graphics):
            self._view = UIView()
            self._view.set_control(Control(graphics=content))
        
        else:
            message = "Unknown content type! -> %s" % type(content)
            raise TypeError(message)
        
        # add to sizer
        self.add_subview(self._view)
        
        # set layout
        self._view.flex = "WH"
    
    
    def layout(self):
        """Called when view is resized."""
        
        # set size to child
        if self._view is not None:
            self._view.frame = (0, 0, self.width, self.height)
    
    
    def refresh(self):
        """Redraws graphics."""
        
        if self._view is not None:
            self._view.refresh()
