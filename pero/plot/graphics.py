#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import *
from ..properties import *
from ..drawing import Graphics, FrameProperty


class InGraphics(Graphics):
    """
    Abstract base class for all graphical components of the plot laying inside
    the main data area.
    
    Properties:
        
        frame: pero.Frame
            Specifies the inner area of the parent plot. Typically this is
            calculated and set by the parent plot.
    """
    
    frame = FrameProperty(UNDEF, dynamic=False)
    
    
    def initialize(self, canvas, plot):
        """
        This method is automatically called by parent plot to set specific
        properties of the object and perform necessary initialization steps.
        
        This method should be overwritten by derived classed.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            plot: pero.plot.Plot
                Parent plot
        """
        
        pass


class OutGraphics(Graphics):
    """
    Abstract base class for all graphical components of the plot laying outside
    the main data area.
    
    Properties:
        
        position: str
            Specifies the object position within parent plot as any value from
            the pero.POSITION_LRTB enum.
        
        margin: int, float, tuple
            Specifies the space around the object box as a single value or
            values for individual sides starting from top.
        
        frame: pero.Frame
            Specifies the frame available for the object. Typically this is
            calculated and set by the parent plot.
    """
    
    position = EnumProperty(POS_TOP, enum=POSITION_LRTB, dynamic=False)
    margin = QuadProperty(10, dynamic=False)
    frame = FrameProperty(UNDEF, dynamic=False)
    
    
    def get_extent(self, canvas):
        """
        This method is automatically called by parent plot to get amount of
        logical space needed to draw the object.
        
        The value should only reflect the necessary space in the relevant
        direction specified by 'position' property. Typical examples are
        thickness of a range bar, height of a title text or width/height of
        an axis including ticks, labels and title. The value should not include
        specified object margin.
        
        This method should be overwritten by derived classed.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
        
        Returns:
            float
                Space needed.
        """
        
        return 0
    
    
    def initialize(self, canvas, plot):
        """
        This method is automatically called by parent plot to set specific
        properties of the object and perform necessary initialization steps.
        
        This method should be overwritten by derived classed.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            plot: pero.plot..Plot
                Parent plot
        """
        
        pass
