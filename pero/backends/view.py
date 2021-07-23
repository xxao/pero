#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . control import Control


class View(object):
    """Abstract base class for specific backend implementations of views."""
    
    
    def __init__(self):
        """Initializes a new instance of View."""
        
        self._control = None
    
    
    @property
    def control(self):
        """
        Gets current control.
        
        Returns:
            pero.Control or None
        """
        
        return self._control
    
    
    def set_control(self, control):
        """
        Sets current control.
        
        Args:
            control: pero.Control or None
                Specific control to be set.
        """
        
        # reset control
        if control is None:
            
            # remove parent link
            if self._control is not None:
                self._control._set_parent(None)
            
            # reset control
            self._control = None
            return
        
        # check control
        if not isinstance(control, Control):
            message = "Control must be of type 'pero.Control'! -> %s" % type(control)
            raise TypeError(message)
        
        # set control
        self._control = control
        
        # set parent
        self._control._set_parent(self)
    
    
    def set_cursor(self, cursor):
        """
        This method should be overridden to provide specific mechanism to set
        given mouse cursor.
        
        Args:
            cursor: pero.CURSOR
                Cursor type to be set. The value must be an item from the
                pero.CURSOR enum.
        """
        
        pass
    
    
    def set_tooltip(self, text):
        """
        This method should be overridden to provide specific mechanism to set
        given text as system tooltip.
        
        Args:
            text: str
                Tooltip text to be shown.
        """
        
        pass
    
    
    def refresh(self):
        """Redraws current control graphics."""
        
        self.draw_control()
    
    
    def draw_control(self):
        """
        This method should be overridden to provide specific drawing mechanism
        and canvas creation to draw current control graphics.
        """
        
        raise NotImplementedError("The 'draw_control' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_overlay(self, func=None, **kwargs):
        """
        This method should be overridden to provide specific drawing mechanism
        and canvas creation to finally call given function to draw cursor rubber
        band overlay over the current graphics.
        
        Specified function is expected to be called with a canvas as the first
        argument followed by given overrides (i.e. func(canvas, **kwargs)).
        
        Calling this method without any parameter should clear current overlay.
        
        Args:
            func: callable or None
                Drawing function to be called to draw the overlay. If set to
                None, current overlay will be cleared.
                
            kwargs: str:any pairs
                Keyword arguments, which should be provided to the given drawing
                function.
        """
        
        raise NotImplementedError("The 'draw_overlay' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def clear_overlay(self):
        """Clears current overlay."""
        
        self.draw_overlay()
