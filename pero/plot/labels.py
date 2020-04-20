#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..properties import *
from ..drawing import Label, LabelBox
from .graphics import InGraphics


class Labels(InGraphics):
    """
    Labels container provides a simple tool to draw all given labels at once in
    the order defined by their 'z_index' property.
    
    By default the container makes sure the labels do not overlap each other
    using their bounding box. If two labels are overlapping, the one with higher
    'z_index' is finally drawn. To ignore label overlaps the 'overlap' property
    must be set to False.
    
    All the labels having the anchor coordinates outside the frame are ignored
    and not drawn. In addition, labels for which the bounding box falls
    partially outside the the clipping frame, are automatically shifted to
    ensure their full visibility.
    
    Properties:
        
        items: (pero.Label,), None or UNDEF
            Specifies a collection of labels to draw.
        
        overlap: bool
            Specifies whether the labels can overlap each other (True) or should
            be skipped  automatically if there is not enough space available
            (False).
        
        spacing: int, float
            Specifies the minimum additional space between adjacent labels.
        
        padding: int, float, (int,), (float,) or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top. This is used in addition to the 'clip' to
            shift partially visible labels.
    """
    
    items = ListProperty(UNDEF, types=(Label,), dynamic=False)
    
    overlap = BoolProperty(False, dynamic=False)
    spacing = NumProperty(4, dynamic=False)
    padding = QuadProperty(5, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Grid."""
        
        super().__init__(**overrides)
        self._glyph = LabelBox()
    
    
    def initialize(self, canvas, plot):
        """
        This method is automatically called by parent plot to set specific
        properties and perform necessary initialization steps.
        """
        
        # check if visible
        if not self.visible:
            return
        
        # set items from plot
        items = []
        for series in plot.series:
            if series.visible and series.show_labels:
                items += series.get_labels()
        
        self.items = items
        
        
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        
        # update glyph
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # draw labels
        self._glyph.draw(canvas, clip=frame)
