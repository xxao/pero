#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Frame, Path
from . glyph import Glyph
from . markers import Marker


class Legend(Glyph):
    """
    Abstract base class for various types of legend items glyphs.
    
    The pero.Legend classes can be used directly to draw legend items or as
    descriptor to create a pero.Legend instances from real data and using the
    'clone' method and a data source.
    
    Properties:
        
        bull_x: int, float or callable
            Specifies the x-coordinate of the bullet center.
        
        bull_y: int, float or callable
            Specifies the y-coordinate of the bullet center.
        
        text_x: int, float or callable
            Specifies the x-coordinate of the text anchor.
        
        text_y: int, float or callable
            Specifies the y-coordinate of the text anchor.
        
        text: str, callable, None or UNDEF
            Specifies the text to be drawn.
        
        text properties:
            Includes pero.TextProperties to specify the text properties.
    """
    
    bull_x = NumProperty(0)
    bull_y = NumProperty(0)
    
    text_x = NumProperty(0)
    text_y = NumProperty(0)
    
    text = StringProperty(UNDEF)
    font = Include(TextProperties)
    
    
    def get_bull_size(self, canvas, source=UNDEF, **overrides):
        """
        Gets bullet glyph width and height.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        
        Returns:
            (float, float)
                Object width and height.
        """
        
        raise NotImplementedError("The 'get_bull_size' method is not implemented for '%s'." % self.__class__.__name__)


class MarkerLegend(Legend):
    """
    Defines a simple legend item with marker bullet and line.
    
    Properties:
        
        show_marker: bool or callable
            Specifies whether the bullet marker should be displayed.
        
        show_line: bool or callable
            Specifies whether the bullet line should be displayed.
        
        marker: pero.MARKER, pero.Path, callable, None or UNDEF
            Specifies the marker to be used as bullet. The value can be
            specified by any item from the pero.MARKER enum or as pero.Path.
        
        marker_size: int, float or callable
            Specifies the bullet marker size.
        
        marker_line properties:
            Includes pero.LineProperties to specify the bullet marker line.
        
        marker_fill properties:
            Includes pero.FillProperties to specify the bullet marker fill.
        
        line_size: int, float or callable
            Specifies the bullet line length.
        
        line properties:
            Includes pero.LineProperties to specify the bullet line.
    """
    
    show_marker = BoolProperty(True)
    show_line = BoolProperty(False)
    
    marker = Property(UNDEF, types=(str, Path), nullable=True)
    marker_size = NumProperty(8)
    marker_line = Include(LineProperties, prefix='marker_', line_color=UNDEF)
    marker_fill = Include(FillProperties, prefix='marker_', fill_color=UNDEF)
    
    line_size = NumProperty(25)
    line = Include(LineProperties, line_color=UNDEF, line_width=UNDEF, line_style=UNDEF, line_dash=UNDEF)
    
    
    def get_bull_size(self, canvas, source=UNDEF, **overrides):
        """Gets bullet glyph size."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return None
        
        # get properties
        marker = self.get_property('marker', source, overrides)
        marker_size = self.get_property('marker_size', source, overrides)
        show_marker = self.get_property('show_marker', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        line_size = self.get_property('line_size', source, overrides)
        line_width = self.get_property('line_width', source, overrides)
        
        # init size
        width = 0
        height = 0
        
        # add marker
        if show_marker and marker_size and marker:
            if isinstance(marker, Path):
                bbox = marker.bbox()
                width = max(width, marker_size*bbox.width)
                height = max(height, marker_size*bbox.height)
            else:
                width = max(width, marker_size)
                height = max(height, marker_size)
        
        # add line
        if show_line and line_size:
            width = max(width, line_size)
            height = max(height, line_width or 0)
        
        return width, height
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        text = self.get_property('text', source, overrides)
        text_x = self.get_property('text_x', source, overrides)
        text_y = self.get_property('text_y', source, overrides)
        bull_x = self.get_property('bull_x', source, overrides)
        bull_y = self.get_property('bull_y', source, overrides)
        show_marker = self.get_property('show_marker', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        marker = self.get_property('marker', source, overrides)
        marker_size = self.get_property('marker_size', source, overrides)
        line_size = self.get_property('line_size', source, overrides)
        
        # start drawing group
        canvas.group(tag, "legend")
        
        # draw line
        if show_line and line_size:
            canvas.set_pen_by(self, source=source, overrides=overrides)
            x1 = bull_x - 0.5*line_size
            x2 = bull_x + 0.5*line_size
            canvas.draw_line(x1=x1, y1=bull_y, x2=x2, y2=bull_y)
        
        # draw marker
        if show_marker and marker_size and marker:
            marker_glyph = Marker.create(marker)
            marker_glyph.set_properties_from(self, src_prefix='marker_', source=source, overrides=overrides)
            marker_glyph.draw(canvas, x=bull_x, y=bull_y)
        
        # draw text
        canvas.set_text_by(self, source=source, overrides=overrides)
        canvas.draw_text(text, text_x, text_y)
        
        # end drawing group
        canvas.ungroup()


class LegendBox(Glyph):
    """
    Legend box glyph provides an easy way of drawing multiple legend items at
    given position and orientation. This can be used in case of drawing plots,
    pie charts etc.
    
    Properties:
        
        items: (pero.Legend,), callable, None or UNDEF
            Specifies a collection of legend items to draw.
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        anchor: pero.POSITION_COMPASS or callable
            Specifies the anchor position within the box as any item from the
            pero.POSITION_COMPASS enum.
        
        orientation: pero.ORIENTATION or callable
            Specifies the orientation of legend items as any item from the
            pero.ORIENTATION enum.
        
        radius: int, float, (int,), (float,) callable or UNDEF
            Specifies the background box corner radius as a single value or
            values for individual corners starting from top-left.
        
        padding: int, float, (int,), (float,) callable or UNDEF
            Specifies the inner space of the background box as a single value
            or values for individual sides starting from top.
        
        spacing: int, float or callable
            Specifies the space between individual legend items.
        
        line properties:
            Includes pero.LineProperties to specify the legend background box
            outline.
        
        fill properties:
            Includes pero.FillProperties to specify the legend background box
            fill.
    """
    
    items = TupleProperty(UNDEF, types=(Legend,), nullable=True)
    
    x = NumProperty(0)
    y = NumProperty(0)
    anchor = EnumProperty(POS_NW, enum=POSITION_COMPASS)
    orientation = EnumProperty(ORI_VERTICAL, enum=ORIENTATION)
    
    radius = QuadProperty(3)
    padding = QuadProperty(5)
    spacing = NumProperty(5)
    
    line = Include(LineProperties, line_color="#ddd")
    fill = Include(FillProperties, fill_color="#fffc")
    
    
    def get_bbox(self, canvas, source=UNDEF, **overrides):
        """
        Gets glyph bounding box.
        
        Args:
            canvas: pero.Canvas
                Canvas to be used for rendering.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        
        Returns:
            pero.Frame or None
                Object bounding box.
        """
        
        # check if visible
        if not self.is_visible(source, overrides):
            return None
        
        # get items
        items = self._get_items(canvas, source, overrides)
        if not items:
            return None
        
        # get bbox
        return self._get_bbox(source, overrides, items)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw legend box."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        padding = self.get_property('padding', source, overrides)
        radius = self.get_property('radius', source, overrides)
        
        # get items
        items = self._get_items(canvas, source, overrides)
        if not items:
            return
        
        # get bbox
        bbox = self._get_bbox(source, overrides, items)
        x = bbox.x + padding[3]
        y = bbox.y + padding[0]
        
        # start drawing group
        canvas.group(tag, "legend_box")
        
        # draw background
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        canvas.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, radius)
        
        # draw items
        for item, bull_bbox, text_bbox in items:
            item.draw(canvas,
                bull_x = x + bull_bbox[0] + 0.5*bull_bbox[2],
                bull_y = y + bull_bbox[1] + 0.5*bull_bbox[3],
                text_x = x + text_bbox[0],
                text_y = y + text_bbox[1])
        
        # end drawing group
        canvas.ungroup()
    
    
    def _get_items(self, canvas, source, overrides):
        """Gets initial boxes for all items."""
        
        # get properties
        items = self.get_property('items', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        spacing = self.get_property('spacing', source, overrides)
        
        # check spacing
        spacing = spacing or 0
        
        # init boxes
        boxes = []
        bull_max = 0
        for item in items:
            
            # check item
            if not item.visible or not item.text:
                continue
            
            # get sizes
            bull_w, bull_h = item.get_bull_size(canvas)
            canvas.set_text_by(item, source=source, overrides=overrides)
            text_w, text_h = canvas.get_text_size(item.text)
            line_w, line_h = canvas.get_line_size(item.text[0])
            
            # init bbox
            bull_bbox = [0, 0, bull_w, bull_h]
            text_bbox = [bull_w + spacing, 0, text_w, text_h]
            
            # center bullet with first line
            if bull_h < line_h:
                bull_bbox[1] += (line_h - bull_h)/2
            
            # add bbox
            boxes.append((item, bull_bbox, text_bbox))
            
            # keep max bullet width
            if bull_w > bull_max:
                bull_max = bull_w
        
        # align horizontally
        if orientation == ORI_HORIZONTAL:
            
            x_offset = 0
            for item, bull_bbox, text_bbox in boxes:
                bull_bbox[0] += x_offset
                text_bbox[0] += x_offset
                x_offset += bull_bbox[2] + text_bbox[2] + 4*spacing
        
        # align vertically
        else:
            
            y_offset = 0
            for item, bull_bbox, text_bbox in boxes:
                
                bull_bbox[1] += y_offset
                text_bbox[1] += y_offset
                y_offset += spacing + max(bull_bbox[3], text_bbox[3])
                
                diff = bull_max - bull_bbox[2]
                bull_bbox[0] += .5*diff
                text_bbox[0] += diff
        
        return boxes
    
    
    def _get_bbox(self, source, overrides, items):
        """Gets final bbox."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        anchor = self.get_property('anchor', source, overrides)
        padding = self.get_property('padding', source, overrides)
        
        # init size
        width = 0
        height = 0
        
        # get width and height of all items
        for item, bull_bbox, text_bbox in items:
            width = max(width, bull_bbox[0] + bull_bbox[2], text_bbox[0] + text_bbox[2])
            height = max(height, bull_bbox[1] + bull_bbox[3], text_bbox[1] + text_bbox[3])
        
        #  apply padding
        if padding:
            width += padding[1] + padding[3]
            height += padding[0] + padding[2]
        
        # shift anchor
        if anchor == POS_NW:
            pass
        elif anchor == POS_N:
            x -= 0.5 * width
        elif anchor == POS_NE:
            x -= width
        elif anchor == POS_E:
            x -= width
            y -= 0.5 * height
        elif anchor == POS_SE:
            x -= width
            y -= height
        elif anchor == POS_S:
            x -= 0.5 * width
            y -= height
        elif anchor == POS_SW:
            y -= height
        elif anchor == POS_W:
            y -= 0.5 * height
        elif anchor == POS_C:
            x -= 0.5 * width
            y -= 0.5 * height
        
        # make bbox
        return Frame(x, y, width, height)
