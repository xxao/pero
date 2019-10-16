#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..properties import *
from ..drawing import Glyph
from ..scales import Scale
from .graphics import InGraphics


class Annotation(InGraphics):
    """
    Annotation provides a simple wrapper to draw any given glyph by applying
    specified x and/or y scaling to selected properties. This class is typically
    used to draw plot annotations by providing coordinates and additional
    properties in data units. Scaling into device units is done automatically.
    
    All the glyph properties should be specified directly to the given 'glyph'.
    Those specified by 'x_props' or 'y_props' are eventually overridden by their
    re-scaled values.
    
    Optional 'x_offset' and/or 'y_offset' in device units can be set e.g. to
    avoid overlapping of the annotation with plotted data.
    
    Properties:
        
        glyph: pero.Glyph
            Specifies the glyph to draw as annotation.
        
        x_props: (str,)
            Specifies the x-coordinate properties which should be re-scaled into
            final device units.
        
        x_scale: pero.Scale
            Specifies the scale to convert x-properties from real data units
            into final device units.
        
        x_offset: int or float
            Specifies the additional shift in device units to be applied to all
            x-properties.
        
        y_props: (str,)
            Specifies the y-coordinate properties which should be re-scaled into
            final device units.
        
        y_scale: pero.Scale
            Specifies the scale to convert y-properties from real data units
            into final device units.
        
        y_offset: int or float
            Specifies the additional shift in device units to be applied to all
            y-properties.
    """
    
    glyph = Property(UNDEF, types=(Glyph,), dynamic=False)
    
    x_props = TupleProperty(UNDEF, intypes=(str,), dynamic=False)
    x_scale = Property(UNDEF, types=(Scale,), dynamic=False)
    x_offset = NumProperty(0, dynamic=False)
    
    y_props = TupleProperty(UNDEF, intypes=(str,), dynamic=False)
    y_scale = Property(UNDEF, types=(Scale,), dynamic=False)
    y_offset = NumProperty(0, dynamic=False)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the annotation."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        x_props = self.get_property('x_props', source, overrides)
        y_props = self.get_property('y_props', source, overrides)
        x_offset = self.get_property('x_offset', source, overrides)
        y_offset = self.get_property('y_offset', source, overrides)
        glyph = self.get_property('glyph', source, overrides)
        
        # init glyph overrides
        glyph_overrides = self.get_child_overrides('glyph', overrides)
        
        # scale properties
        if x_props and x_scale:
            for prop_name in x_props:
                prop_value = glyph.get_property(prop_name, source, glyph_overrides)
                prop_value = x_scale.scale(prop_value) + x_offset
                glyph_overrides[prop_name] = prop_value
        
        if y_props and y_scale:
            for prop_name in y_props:
                prop_value = glyph.get_property(prop_name, source, glyph_overrides)
                prop_value = y_scale.scale(prop_value) + y_offset
                glyph_overrides[prop_name] = prop_value
        
        # draw glyph
        glyph.draw(canvas, source=UNDEF, **glyph_overrides)
