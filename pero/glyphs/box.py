#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Graphics, Path
from . glyph import Glyph


class Box(Glyph):
    """
    Defines a generic graphics box. This glyph allows to draw a graphics
    within a box with predefined position, size and alignment. If width and
    heights are not provided, the box automatically fills all available space
    and shifts canvas origin according to desired content alignment.
    
    Together with pero.Control, this can be used to create simple interactive
    elements like buttons etc.
    
    Properties:
        
        graphics: pero.Graphics
            Specifies the box content to draw.
        
        h_align: str or callable
            Horizontal alignment of the box content as any item from the
            pero.POSITION_LRC enum.
        
        v_align: str or callable
            Vertical alignment of the box content as any item from the
            pero.POSITION_TBC enum.
        
        clip: bool
            Specifies whether the box content overflow should be clipped.
        
        anchor: pero.POSITION_COMPASS or callable
            Specifies the anchor position as any item from the
            pero.POSITION_COMPASS enum.
        
        x: int, float or callable
            Specifies the x-coordinate of the box anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the box anchor.
        
        width: int, float, callable or UNDEF
            Specifies the box width. If not defined, the value is taken
            automatically from given canvas.
        
        height: int, float, callable or UNDEF
            Specifies the box height. If not defined, the value is taken
            automatically from given canvas.
        
        radius: int, float, (int,), (float,), callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        padding: int, float, (int,), (float,), callable or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top.
        
        margin:  int, float, (int,), (float,), callable or UNDEF
            Specifies the outer space as a single value or values for individual
            sides starting from top.
        
        line properties:
            Includes pero.LineProperties to specify the box outline.
        
        fill properties:
            Includes pero.FillProperties to specify the box fill.
    """
    
    graphics = Property(UNDEF, types=(Graphics,), dynamic=False)
    h_align = EnumProperty(POS_LEFT, enum=POSITION_LRC)
    v_align = EnumProperty(POS_TOP, enum=POSITION_TBC)
    clip = BoolProperty(True)
    
    anchor = EnumProperty(POS_NW, enum=POSITION_COMPASS)
    x = NumProperty(0)
    y = NumProperty(0)
    width = NumProperty(UNDEF)
    height = NumProperty(UNDEF)
    
    radius = QuadProperty(0)
    padding = QuadProperty(5)
    margin = QuadProperty(0)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        anchor = self.get_property('anchor', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        radius = self.get_property('radius', source, overrides)
        padding = self.get_property('padding', source, overrides)
        margin = self.get_property('margin', source, overrides)
        graphics = self.get_property('graphics', source, overrides)
        h_align = self.get_property('h_align', source, overrides)
        v_align = self.get_property('v_align', source, overrides)
        clip = self.get_property('clip', source, overrides)
        
        # init box
        box_x = x
        box_y = y
        box_w = width
        box_h = height
        padding = padding or (0, 0, 0, 0)
        margin = margin or (0, 0, 0, 0)
        
        # get width from canvas and adjust by anchor
        if box_w is UNDEF:
            box_w = canvas.viewport.width
            if anchor in (POS_NW, POS_W, POS_SW):
                box_w -= x + margin[1] + margin[3]
            elif anchor in (POS_NE, POS_E, POS_SE):
                box_w = x - margin[1] - margin[3]
            elif anchor in (POS_N, POS_C, POS_S):
                box_w -= margin[1] + margin[3]
        
        # get height from canvas and adjust by anchor
        if box_h is UNDEF:
            box_h = canvas.viewport.height
            if anchor in (POS_NW, POS_N, POS_NE):
                box_h -= y + margin[0] + margin[2]
            elif anchor in (POS_SW, POS_S, POS_SE):
                box_h = y - margin[0] - margin[2]
            elif anchor in (POS_W, POS_C, POS_E):
                box_h -= margin[0] + margin[2]
        
        # adjust box origin by anchor
        if anchor == POS_N:
            box_x -= 0.5 * box_w
        elif anchor == POS_NE:
            box_x -= box_w
        elif anchor == POS_E:
            box_x -= box_w
            box_y -= 0.5 * box_h
        elif anchor == POS_SE:
            box_x -= box_w
            box_y -= box_h
        elif anchor == POS_S:
            box_x -= 0.5 * box_w
            box_y -= box_h
        elif anchor == POS_SW:
            box_y -= box_h
        elif anchor == POS_W:
            box_y -= 0.5 * box_h
        elif anchor == POS_C:
            box_x -= 0.5 * box_w
            box_y -= 0.5 * box_h
        
        # adjust box origin by margin
        if anchor in (POS_NW, POS_W, POS_SW):
            box_x += margin[3]
        elif anchor in (POS_NE, POS_E, POS_SE):
            box_x -= margin[1]
        elif anchor in (POS_N, POS_C, POS_S):
            box_x = margin[3]
        
        if anchor in (POS_NW, POS_N, POS_NE):
            box_y += margin[0]
        if anchor in (POS_SW, POS_S, POS_SE):
            box_y -= margin[2]
        elif anchor in (POS_W, POS_C, POS_E):
            box_y = margin[0]
        
        # adjust content frame by padding
        con_x = box_x + padding[3]
        con_y = box_y + padding[0]
        con_w = box_w - padding[1] - padding[3]
        con_h = box_h - padding[0] - padding[2]
        
        # start drawing group
        canvas.group()
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw box
        canvas.draw_rect(box_x, box_y, box_w, box_h, radius)
        
        # set clipping
        if clip:
            canvas.clip(Path().rect(con_x, con_y, con_w, con_h))
        
        # draw graphics
        if graphics:
            
            # adjust content frame by alignment
            if h_align == POS_CENTER:
                con_x += 0.5 * con_w
            elif h_align == POS_RIGHT:
                con_x += con_w
            
            if v_align == POS_CENTER:
                con_y += 0.5 * con_h
            elif v_align == POS_BOTTOM:
                con_y += con_h
            
            # get overrides
            overrides = self.get_child_overrides('graphics', overrides)
            
            # draw graphics
            with canvas.view(con_x, con_y, con_w, con_h, relative=True):
                graphics.draw(canvas, source=source, **overrides)
        
        # revert clipping
        if clip:
            canvas.unclip()
        
        # end drawing group
        canvas.ungroup()
