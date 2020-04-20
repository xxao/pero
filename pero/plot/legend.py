#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import *
from ..properties import *
from ..drawing import LegendBox
from ..drawing import Legend as LegendGlyph
from .graphics import InGraphics


class Legend(InGraphics):
    """
    Legend provides a simple wrapper for the pero.LegendBox glyph to draw the
    plot legend.
    
    Properties:
        
        items: (pero.Legend,), None or UNDEF
            Specifies a collection of legend items to draw.
        
        static: bool
            Specifies whether the legend items are given by user directly (True)
            or whether they should be retrieved automatically from the plot
            (False).
        
        position: pero.POSITION_COMPASS
            Specifies the legend position within a plot as any item from the
            pero.POSITION_COMPASS enum.
        
        orientation: pero.POSITION_COMPASS
            Specifies the legend orientation as any item from the
            pero.ORIENTATION enum.
        
        margin: int, float, (int,), (float,) or UNDEF
            Specifies the space around the legend box as a single value or
            values for individual sides starting from top.
        
        padding: int, float, (int,), (float,) or UNDEF
            Specifies the inner space of the legend box as a single value or
            values for individual sides starting from top.
        
        spacing: int or float
            Specifies the additional space between legend items.
        
        radius: int, float, (int,), (float,) or UNDEF
            Specifies the corner radius of the legend box as a single value or
            values for individual corners starting from top-left.
        
        line properties:
            Includes pero.LineProperties to specify the legend box outline.
        
        fill properties:
            Includes pero.FillProperties to specify the legend box fill.
    """
    
    items = TupleProperty(UNDEF, types=(LegendGlyph,), dynamic=False, nullable=True)
    static = BoolProperty(False, dynamic=False)
    
    position = EnumProperty(POS_NE, enum=POSITION_COMPASS, dynamic=False)
    orientation = EnumProperty(ORI_VERTICAL, enum=ORIENTATION)
    margin = QuadProperty(10, dynamic=False)
    
    radius = QuadProperty(3, dynamic=False)
    padding = QuadProperty(5, dynamic=False)
    spacing = NumProperty(5, dynamic=False)
    
    line = Include(LineProperties, line_color="#ddd")
    fill = Include(FillProperties, fill_color="#fffc")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Legend."""
        
        super().__init__(**overrides)
        self._glyph = LegendBox()
    
    
    def initialize(self, canvas, plot):
        """
        This method is automatically called by parent plot to set specific
        properties and perform necessary initialization steps.
        """
        
        # check if visible
        if not self.visible:
            return
        
        # set items from plot
        if not self.static:
            
            items = []
            for series in sorted(plot.series, key=lambda s: s.z_index):
                if series.visible and series.show_legend:
                    item = series.get_legend()
                    if item and item.visible and item.text:
                        items.append(item)
            
            self.items = items
        
        # check items
        if not self.items:
            return
        
        # get position
        frame = self.frame
        position = self.position or POS_NE
        margin = self.margin or (10, 10, 10, 10)
        
        # set anchor
        self._glyph.anchor = position
        
        if position == POS_N:
            self._glyph.x = frame.cx
            self._glyph.y = frame.y1 + margin[0]
        
        elif position == POS_NE:
            self._glyph.x = frame.x2 - margin[1]
            self._glyph.y = frame.y1 + margin[0]
        
        elif position == POS_E:
            self._glyph.x = frame.x2 - margin[1]
            self._glyph.y = frame.cy
        
        elif position == POS_SE:
            self._glyph.x = frame.x2 - margin[1]
            self._glyph.y = frame.y2 - margin[2]
        
        elif position == POS_S:
            self._glyph.x = frame.cx
            self._glyph.y = frame.y2 - margin[2]
        
        elif position == POS_SW:
            self._glyph.x = frame.x1 + margin[3]
            self._glyph.y = frame.y2 - margin[2]
        
        elif position == POS_W:
            self._glyph.x = frame.x1 + margin[3]
            self._glyph.y = frame.cy
        
        elif position == POS_NW:
            self._glyph.x = frame.x1 + margin[3]
            self._glyph.y = frame.y1 + margin[0]
        
        elif position == POS_C:
            self._glyph.x = frame.cx
            self._glyph.y = frame.cy
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update glyph
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # draw legend
        self._glyph.draw(canvas, anchor=self.position)
