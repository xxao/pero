#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. colors import Color
from . typed import *
from . special import *
from . undefined import UNDEF
from . propset import PropertySet, Include, PROP_SPLITTER


class AngleProperties(PropertySet):
    """
    Collection of properties defining an angle value with its units.
    
    Properties:
        
        angle: int, float, callable, None or UNDEF
            Specifies the angle value.
        
        angle_units: pero.ANGLE, callable or UNDEF
            Specifies the angle units as any item from the pero.ANGLE enum.
    """
    
    angle = NumProperty(0, nullable=True)
    angle_units = EnumProperty(ANGLE_RAD, enum=ANGLE)
    
    
    @staticmethod
    def get_angle(prop_set, prefix="", units=ANGLE_RAD, source=UNDEF, overrides=None):
        """
        Gets current angle value directly converted to requested units.
        
        Args:
            prop_set: pero.PropertySet
                Property set from which to retrieve the angle.
            
            prefix: str
                Prefix applied to all angle properties.
            
            units: str
                Requested units of the angle as any item from the pero.ANGLE
                enum.
            
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current values.
        
        Returns:
            float or UNDEF
                Angle value in requested units or UNDEF if value or units are
                not defined.
        """
        
        # check type
        if not isinstance(prop_set, PropertySet):
            message = "Property set must be of type pero.PropertySet! -> %s" % type(prop_set)
            raise TypeError(message)
        
        # check prefix
        if prefix and prefix[-1] != PROP_SPLITTER:
            prefix = prefix + PROP_SPLITTER
        
        # get properties
        angle = prop_set.get_property(prefix+'angle', source, overrides)
        angle_units = prop_set.get_property(prefix+'angle_units', source, overrides)
        
        # check if None
        if angle is None or angle_units is None:
            return 0
        
        # check if defined
        if angle is UNDEF or angle_units is UNDEF:
            return UNDEF
        
        # check units
        if units == angle_units:
            return angle
        
        elif units == ANGLE_RAD:
            return math.radians(angle)
        
        elif units == ANGLE_DEG:
            return math.degrees(angle)


class ColorProperties(PropertySet):
    """
    Collection of properties defining a color.
    
    Properties:
        
        color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the color as an RGB or RGBA tuple, hex code, name or
            pero.Color. If the color is set to None, transparent color is
            set instead.
        
        alpha: int, callable, None or UNDEF
            Specifies the color alpha channel as a value between 0 and 255,
            where 0 means fully transparent and 255 fully opaque. If this value
            is set, it will overwrite the alpha channel in the final color.
    """
    
    color = ColorProperty(UNDEF, nullable=True)
    alpha = RangeProperty(UNDEF, minimum=0, maximum=255, nullable=True)
    
    
    @staticmethod
    def get_color(prop_set, prefix="", source=UNDEF, overrides=None):
        """
        Gets current color property value with the alpha property applied.
        
        Args:
            prop_set: pero.PropertySet
                Property set from which to retrieve the properties.
            
            prefix: str
                Prefix applied to color properties.
            
            source: any
                Data source to be used for retrieving the final value of
                callable properties.
            
            overrides: dict or None
                Highest priority properties to be used instead of current values.
        
        Returns:
            pero.Color or UNDEF
                Color value with applied alpha or UNDEF if color not defined.
        """
        
        # check type
        if not isinstance(prop_set, PropertySet):
            message = "Property set must be of type pero.PropertySet! -> %s" % type(prop_set)
            raise TypeError(message)
        
        # check prefix
        if prefix and prefix[-1] != PROP_SPLITTER:
            prefix = prefix + PROP_SPLITTER
        
        # get properties
        color = prop_set.get_property(prefix+'color', source, overrides)
        alpha = prop_set.get_property(prefix+'alpha', source, overrides)
        
        # make transparent from None
        if color is None:
            return Color.Transparent
        
        # check if defined
        if color is UNDEF or alpha is UNDEF or alpha is None:
            return color
        
        # apply alpha
        if color.alpha != alpha:
            color = color.opaque(alpha/255.)
        
        return color


class LineProperties(PropertySet):
    """
    Collection of properties defining a line or pen style.
    
    Properties:
        
        line_color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the line color as an RGB or RGBA tuple, hex code, name or
            pero.Color.
        
        line_alpha: int, callable, None or UNDEF
            Specifies the line color alpha channel as a value between 0 and 255,
            where 0 is fully transparent and 255 fully opaque. If this value is
            set, it will overwrite the alpha channel in the final line color.
        
        line_width: int, float, callable or UNDEF
            Specifies the line width.
        
        line_style: pero.LINE_STYLE, callable or UNDEF
            Specifies the line drawing style as any item from the
            pero.LINE_STYLE enum.
        
        line_dash: (float,), callable, None or UNDEF
            Specifies the line dash style as a collection of numbers defining
            the lengths of lines and spaces in-between. Specified value is used
            if the 'line_style' property is set to pero.LINE_STYLE_CUSTOM.
        
        line_cap: pero.LINE_CAP, callable or UNDEF
            Specifies the line ends shape as any item from the pero.LINE_CAP
            enum.
        
        line_join: pero.LINE_JOIN, callable or UNDEF
            Specifies the line corners shape as any item from the
            pero.LINE_JOIN enum.
    """
    
    color = Include(ColorProperties, "line_")
    line_width = NumProperty(1)
    line_dash = DashProperty(None, nullable=True)
    line_style = EnumProperty(LINE_STYLE_SOLID, enum=LINE_STYLE)
    line_cap = EnumProperty(LINE_CAP_ROUND, enum=LINE_CAP)
    line_join = EnumProperty(LINE_JOIN_ROUND, enum=LINE_JOIN)


class FillProperties(PropertySet):
    """
    Collection of properties defining a fill or brush style.
    
    Properties:
        
        fill_color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the fill color as an RGB or RGBA tuple, hex code, name or
            pero.Color.
        
        fill_alpha: int, callable, None or UNDEF
            Specifies the fill alpha channel as a value between 0 and 255, where
            0 is fully transparent and 255 fully opaque. If this value is set,
            it will overwrite the alpha channel in the final fill color.
        
        fill_style: pero.FILL_STYLE, callable or UNDEF
            Specifies the fill style as any item from the pero.FILL_STYLE
            enum.
    """
    
    color = Include(ColorProperties, "fill_")
    fill_style = EnumProperty(FILL_STYLE_SOLID, enum=FILL_STYLE)


class TextProperties(PropertySet):
    """
    Collection of properties defining a text style.
    
    Properties:
        
        font_size: int, callable, None or UNDEF
            Specifies the font size or None to reset to default size.
        
        font_name: str, callable, None or UNDEF
            Specifies an existing font name or None to reset to default family.
        
        font_family: pero.FONT_FAMILY, callable, None or UNDEF
            Specifies the font family as any item from the pero.FONT_FAMILY
            enum or None to reset to default family.
        
        font_style: pero.FONT_STYLE, callable, None or UNDEF
            Specifies the font style as any item from the pero.FONT_STYLE
            enum or None to reset to default style.
        
        font_weight: pero.FONT_WEIGHT, callable, None or UNDEF
            Specifies the font weight as any item from the pero.FONT_WEIGHT
            enum or None to reset to default weight.
        
        text_align: pero.TEXT_ALIGN, callable, None or UNDEF
            Specifies the text alignment as any item from the pero.TEXT_ALIGN
            enum or None to reset to default alignment.
        
        text_base: pero.TEXT_BASE, callable, None or UNDEF
            Specifies the text baseline as any item from the
            pero.TEXT_BASE enum or None to reset to default baseline.
        
        text_color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the text foreground color as an RGB or RGBA tuple, hex
            code, name or pero.Color.
        
        text_alpha: int, callable, None or UNDEF
            Specifies the text foreground alpha channel as a value between 0 and
            255, where 0 is fully transparent and 255 fully opaque. If this
            value is set, it will overwrite the alpha channel of the final text
            color.
        
        text_bgr_color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the text background color as an RGB or RGBA tuple, hex
            code, name or pero.Color.
        
        text_bgr_alpha: int, callable, None or UNDEF
            Specifies the text background alpha channel as a value between 0 and
            255, where 0 is fully transparent and 255 fully opaque. If this
            value is set, it will overwrite the alpha channel of the final text
            background color.
        
        text_split: bool
            Specifies whether the text should be first split into individual
            lines. This requires corresponding 'text_splitter' property to be
            set.
        
        text_splitter: str
            Specifies the character(s) to be used for splitting a text into
            individual lines.
        
        text_spacing: float
            Specifies additional space to be inserted between text lines as
            multiplier of line height.
    """
    
    font_size = IntProperty(11, nullable=True)
    font_name = StringProperty(UNDEF, nullable=True)
    font_family = EnumProperty(FONT_FAMILY_SANS, enum=FONT_FAMILY, nullable=True)
    font_style = EnumProperty(FONT_STYLE_NORMAL, enum=FONT_STYLE, nullable=True)
    font_weight = EnumProperty(FONT_WEIGHT_NORMAL, enum=FONT_WEIGHT, nullable=True)
    
    text_align = EnumProperty(TEXT_ALIGN_LEFT, enum=TEXT_ALIGN, nullable=True)
    text_base = EnumProperty(TEXT_BASE_TOP, enum=TEXT_BASE, nullable=True)
    
    for_color = Include(ColorProperties, prefix="text", color='#000')
    bgr_color = Include(ColorProperties, prefix="text_bgr", color=None)
    
    text_split = BoolProperty(True)
    text_splitter = StringProperty(LINE_SPLITTER)
    text_spacing = FloatProperty(0)
