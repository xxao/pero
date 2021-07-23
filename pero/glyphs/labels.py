#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Frame, FrameProperty
from . glyph import Glyph


class Label(Glyph):
    """
    Abstract base class for various types of label items glyphs.
    
    The pero.Label classes can be used directly to draw labels or as descriptor
    to create a pero.Label instances from real data and using the 'clone'
    method and a data source.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        x_offset: int, float or callable
            Specifies the x-axis shift from the label anchor.
        
        y_offset: int, float or callable
            Specifies the y-axis shift from the label anchor.
    """
    
    x = NumProperty(UNDEF)
    y = NumProperty(UNDEF)
    
    x_offset = NumProperty(UNDEF)
    y_offset = NumProperty(UNDEF)
    
    
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
        
        raise NotImplementedError("The 'get_bbox' method is not implemented for '%s'." % self.__class__.__name__)


class TextLabel(Label):
    """
    Defines a simple text label glyph.
    
    Properties:
        
        text: str, callable, None or UNDEF
            Specifies the text to be drawn.
        
        text properties:
            Includes pero.TextProperties to specify the text properties.
        
        angle properties:
            Includes pero.AngleProperties to specify the text angle.
    """
    
    text = StringProperty(UNDEF)
    font = Include(TextProperties, text_align=TEXT_ALIGN_CENTER, text_base=TEXT_BASE_BOTTOM)
    angle = Include(AngleProperties)
    
    
    def get_bbox(self, canvas, source=UNDEF, **overrides):
        """Gets glyph bounding box."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return None
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        x_offset = self.get_property('x_offset', source, overrides)
        y_offset = self.get_property('y_offset', source, overrides)
        text = self.get_property('text', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # check text
        if not text:
            return None
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # apply offset
        x += x_offset or 0
        y += y_offset or 0
        
        # get bounding box
        return canvas.get_text_bbox(text, x, y, angle)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw label."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        x_offset = self.get_property('x_offset', source, overrides)
        y_offset = self.get_property('y_offset', source, overrides)
        text = self.get_property('text', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # check text
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # check offset
        x_offset = x_offset or 0
        y_offset = y_offset or 0
        
        # draw text
        canvas.draw_text(text, x+x_offset, y+y_offset, angle)


class LabelBox(Glyph):
    """
    Labels box provides a simple tool to draw all given labels at once in
    the order defined by their 'z_index' property. This can be useful in case of
    drawing plot labels as one consistent layer or group.
    
    If the 'clip' frame is provided, all the labels having the anchor
    coordinates outside the frame are ignored and not drawn. In addition, labels
    for which the bounding box falls partially outside the the clipping frame,
    are automatically shifted to ensure their full visibility.
    
    By default the container makes sure the labels do not overlap each other
    using their bounding box. If two labels are overlapping, the one with higher
    'z_index' is finally drawn. To ignore label overlaps the 'overlap' property
    must be set to False.
    
    Properties:
        
        items: (pero.Label,), callable, None or UNDEF
            Specifies a collection of label items to draw.
        
        overlap: bool or callable
            Specifies whether the labels can overlap (True) or should be skipped
            automatically if there is not enough free space (False).
        
        spacing: int, float or callable
            Specifies the minimum free space between adjacent labels.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the available drawing frame, which is used to hide
            invisible labels or shift partially visible labels.
        
        padding: int, float, (int,), (float,) callable or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top. This is used in addition to the 'clip' to
            shift partially visible labels.
    """
    
    items = TupleProperty(UNDEF, types=(Label,))
    
    overlap = BoolProperty(False)
    spacing = NumProperty(4)
    
    clip = FrameProperty(UNDEF)
    padding = QuadProperty(5)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw labels."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        
        # get labels as ((label, x, y, x_offset, y_offset),)
        labels = self._get_items(canvas, source, overrides)
        if not labels:
            return
        
        # sort to ensure the most important is drawn on top (as last)
        labels.sort(key=lambda d: d[0].z_index or 0)
        
        # start drawing group
        canvas.group(tag, "labels")
        
        # draw labels
        for label in labels:
            label[0].draw(canvas,
                x = label[1],
                y = label[2],
                x_offset = label[3],
                y_offset = label[4])
        
        # end drawing group
        canvas.ungroup()
    
    
    def _get_items(self, canvas, source, overrides):
        """Gets final list of labels to be drawn."""
        
        # get properties
        items = self.get_property('items', source, overrides)
        overlap = self.get_property('overlap', source, overrides)
        spacing = self.get_property('spacing', source, overrides)
        clip = self.get_property('clip', source, overrides)
        padding = self.get_property('padding', source, overrides)
        
        # check items
        if not items:
            return []
        
        # prepare labels as ((label, x, y, x_offset, y_offset),)
        labels = []
        for label in items:
            x_offset = label.get_property('x_offset') or 0
            y_offset = label.get_property('y_offset') or 0
            labels.append([label, label.x, label.y, x_offset, y_offset])
        
        # allow overlaps and do not clip
        if overlap and not clip:
            return labels
        
        # init padded clip
        padded = clip
        if padding:
            padded = clip.clone()
            padded.shrink(*padding)
        
        # apply clipping and prevent overlaps
        final = []
        area = []
        
        for label in sorted(labels, key=lambda d: d[0].z_index or 0, reverse=True):
            
            # check if outside clip
            if clip and not clip.contains(label[0].x, label[0].y):
                continue
            
            # get bbox
            bbox = label[0].get_bbox(canvas, x=label[1], y=label[2], x_offset=label[3], y_offset=label[4])
            if bbox is None:
                continue
            
            # apply clipping
            if padded:
                
                # calc shift
                x_shift = 0
                y_shift = 0
                
                if bbox.x1 < padded.x1:
                    x_shift = padded.x1 - bbox.x1
                elif bbox.x2 > padded.x2:
                    x_shift = padded.x2 - bbox.x2
                
                if bbox.y1 < padded.y1:
                    y_shift = padded.y1 - bbox.y1
                elif bbox.y2 > padded.y2:
                    y_shift = padded.y2 - bbox.y2
                
                # apply shift
                if x_shift or y_shift:
                    label[3] += x_shift
                    label[4] += y_shift
                    bbox.offset(x_shift, y_shift)
            
            # check overlaps
            if not overlap:
                
                # apply spacing
                if spacing:
                    x, y, width, height = bbox.rect
                    bbox = Frame(x-0.5*spacing, y-0.5*spacing, width+spacing, height+spacing)
                
                # check overlaps
                if any(bbox.overlaps(x) for x in area):
                    continue
            
            # store label
            final.append(label)
            area.append(bbox)
        
        return final
