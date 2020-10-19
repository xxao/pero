#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. import colors
from ..enums import *
from ..properties import *
from ..drawing import Graphics, Frame, Shape, Circle
from ..scales import OrdinalScale
from .enums import *
from . import utils

# define constants
_REGIONS = ('a', 'b', 'ab', 'c', 'ac', 'bc', 'abc')
_CIRCLES = ('circle_a', 'circle_b', 'circle_c')


class Venn(Graphics):
    """
    
    Properties:
        
        mode: pero.VENN or callable
            Specifies whether circles and overlaps should be proportional to
            their area as any item from the pero.venn.VENN enum.
                pero.venn.VENN.NONE - non-proportional
                pero.venn.VENN.SEMI - circles are proportional but overlaps not
                pero.venn.VENN.FULL - circles and overlaps try to be proportional
        
        x: int or float
            Specifies the x-coordinate of the top-left corner
        
        y: int or float
            Specifies the y-coordinate of the top-left corner
        
        width: int, float or UNDEF
            Specifies the full diagram width. If set to UNDEF the full area of
            given canvas is used.
        
        height: int, float or UNDEF
            Specifies the full diagram height. If set to UNDEF the full area of
            given canvas is used.
        
        padding: int, float or tuple
            Specifies the inner space of the diagram as a single value or values
            for individual sides starting from top.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the diagram outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the diagram fill.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for diagram regions.
    """
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(10, dynamic=False)
    
    bgr_line = Include(LineProperties, prefix="bgr", dynamic=False, line_width=0)
    bgr_fill = Include(FillProperties, prefix="bgr", dynamic=False, fill_color="#fff")
    
    mode = EnumProperty(VENN_MODE_SEMI, enum=VENN_MODE, dynamic=False, nullable=True)
    palette = PaletteProperty(colors.Pastel1, dynamic=False, nullable=True)
    
    a = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    b = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    ab = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    c = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    ac = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    bc = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    abc = Property(UNDEF, types=(Shape,), dynamic=False, nullable=False)
    
    circle_a = Property(UNDEF, types=(Circle,), dynamic=False, nullable=False)
    circle_b = Property(UNDEF, types=(Circle,), dynamic=False, nullable=False)
    circle_c = Property(UNDEF, types=(Circle,), dynamic=False, nullable=False)
    
    
    def __init__(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """Initializes a new instance of Venn diagram."""
        
        # init main graphics
        for key in _REGIONS:
            if key not in overrides:
                overrides[key] = Shape(tag=key, z_index=REGION_Z, line_width=0)
        
        for key in ('circle_a', 'circle_b', 'circle_c'):
            if key not in overrides:
                overrides[key] = Circle(tag=key, z_index=CIRCLE_Z, fill_style=TRANS)
        
        # init base
        super().__init__(**overrides)
        
        # init buffs
        self._data = (a, b, ab, c, ac, bc, abc)
        self._graphics = {k: self.get_property(k) for k in _REGIONS + _CIRCLES}
        self._frame = Frame(0, 0, 1, 1)
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_venn_property_changed)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the diagram."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        mode = self.get_property('mode', source, overrides)
        palette = self.get_property('palette', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # init frame
        self._frame = Frame(padding[3], padding[0], width - (padding[1]+padding[3]), height - (padding[0]+padding[2]))
        
        # refuse to draw if "negative" size
        if self._frame.reversed:
            return
        
        # calculate venn
        coords, radii = utils.calc_venn(*self._data, mode=mode)
        coords, radii = utils.fit_into(coords, radii, *self._frame.rect)
        regions = utils.make_regions(coords, radii)
        
        # init colors
        color_scale = OrdinalScale(in_range=_REGIONS, out_range=palette)
        
        # draw main bgr
        canvas.set_pen_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.draw_rect(x, y, width, height)
        
        # sort objects by z-index
        objects = sorted(self._graphics.values(), key=lambda o: o.z_index)
        
        # draw objects
        for obj in objects:
            
            # get overrides
            obj_overrides = self.get_child_overrides(obj.tag, overrides)
            
            # update region overrides
            if obj.tag in _REGIONS:
                obj_overrides['path'] = regions[obj.tag].path()
                if obj.fill_color is UNDEF:
                    obj_overrides['fill_color'] = color_scale.scale(obj.tag)
            
            # update circles overrides
            if obj.tag in _CIRCLES:
                obj_overrides['x'] = coords[_CIRCLES.index(obj.tag)][0]
                obj_overrides['y'] = coords[_CIRCLES.index(obj.tag)][1]
                obj_overrides['size'] = 2*radii[_CIRCLES.index(obj.tag)]
                obj_overrides['visible'] = radii[_CIRCLES.index(obj.tag)] > 0
            
            # draw object
            obj.draw(canvas, **obj_overrides)
    
    
    def _on_venn_property_changed(self, evt):
        """Called after any property has changed."""
        
        pass
