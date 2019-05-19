#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .library import Library

# init library
COLORS = Library()


class ColorMeta(type):
    """Defines a meta class for the main Color class."""
    
    
    def __getattr__(cls, key):
        """
        Gets registered named color by its name.
        
        Returns:
            color: pero.Color
                Corresponding color.
        """
        
        return COLORS[key]


class Color(object, metaclass=ColorMeta):
    """
    Represents a color defined by red, green, blue and alpha channels. All the
    channels are defined as integers between 0 to 255.
    """
    
    
    def __init__(self, red, green, blue, alpha=255., name=None):
        """
        Initializes a new instance of Color.
        
        Args:
            red: int
                Red channel as a value in range 0 to 255.
            
            green: int
                Green channel as a value in range 0 to 255.
            
            blue: int
                Blue channel as a value in range 0 to 255.
            
            alpha: int
                Alpha channel as a value in range 0 to 255.
            
            name: str or None
                Unique name to register.
        """
        
        super(Color, self).__init__()
        
        # check values
        for c in (red, green, blue, alpha):
            if not isinstance(c, (int, float)) or c < 0 or c > 255:
                message = "Color channel must be a number between 0 and 255! -> (%s, %s, %s, %s)" % (red, green, blue, alpha)
                raise ValueError(message)
        
        # set values
        self._red = int(0.5 + red)
        self._green = int(0.5 + green)
        self._blue = int(0.5 + blue)
        self._alpha = int(0.5 + alpha)
        self._name = name
        
        # register color by name
        if name is not None:
            COLORS.add(self)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        name = ""
        if self._name is not None:
            name = " %s" % self._name
        
        return "(%s,%s,%s,%s)%s" % (self._red, self._green, self._blue, self._alpha, name)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    
    def __eq__(self, other):
        """Equal operator."""
        
        if self is other:
            return True
        
        if isinstance(other, Color):
            return (self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
                and self.alpha == other.alpha)
        
        if isinstance(other, (list, tuple)):
            
            if len(other) == 3:
                return (self.red == other[0]
                    and self.green == other[1]
                    and self.blue == other[2]
                    and self.alpha == 255)
            
            if len(other) == 4:
                return (self.red == other[0]
                    and self.green == other[1]
                    and self.blue == other[2]
                    and self.alpha == other[3])
        
        return False
    
    
    def __ne__(self, other):
        """Not equal operator."""
        
        return not self.__eq__(other)
    
    
    @property
    def name(self):
        """
        Gets color name.
        
        Returns:
            str or None
                Color name.
        """
        
        return self._name
    
    
    @property
    def red(self):
        """
        Gets red channel as a value in range 0 to 255.
        
        Returns:
            int
                Red channel value.
        """
        
        return self._red
    
    
    @property
    def green(self):
        """
        Gets green channel as a value in range 0 to 255.
        
        Returns:
            int
                Green channel value.
        """
        
        return self._green
    
    
    @property
    def blue(self):
        """
        Gets blue channel as a value in range 0 to 255.
        
        Returns:
            int
                Blue channel value.
        """
        
        return self._blue
    
    
    @property
    def alpha(self):
        """
        Gets alpha channel as a value in range 0 to 255 where 0 means fully
        transparent and 255 fully opaque.
        
        Returns:
            int
                Alpha channel value.
        """
        
        return self._alpha
    
    
    @property
    def rgba(self):
        """
        Gets RGBA channels tuple where each channel is defined as integer in
        range 0 to 255.
        
        Returns:
            (int, int, int, int)
                Values of RGBA channels.
        """
        
        return self._red, self._green, self._blue, self._alpha
    
    
    @property
    def rgb(self):
        """
        Gets RGB channels tuple where each channel is defined as integer in
        range 0 to 255.
        
        Returns:
            (int, int, int)
                Values of RGB channels.
        """
        
        return self._red, self._green, self._blue
    
    
    @property
    def rgba_r(self):
        """
        Gets RGBA channels tuple where each channel is defined as float in
        range 0 to 1.
        
        Returns:
            (float, float, float, float)
                Values of RGBA channels.
        """
        
        return self._red/255., self._green/255., self._blue/255., self._alpha/255.
    
    
    @property
    def rgb_r(self):
        """
        Gets RGB channels tuple where each channel is defined as float in
        range 0 to 1.
        
        Returns:
            (float, float, float)
                Values of RGB channels.
        """
        
        return self._red/255., self._green/255., self._blue/255.
    
    
    @property
    def hex(self):
        """
        Gets RGBA channels as hex string prefixed by '#'.
        
        Returns:
            str
                Hex string of #RGBA channels.
        """
        
        return "#%02x%02x%02x%02x" % (self._red, self._green, self._blue, self._alpha)
    
    
    def lighter(self, factor=0.2, name=None):
        """
        Creates derived color by making current color lighter. The factor
        specifies relative amount of white to be added, i.e. 1 results in full
        white color while 0 makes no change. The new color is automatically
        registered for later use if the name is specified.
        
        Args:
            factor: float
                Amount of lightening to be applied in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                Lighter color.
        """
        
        # check value
        if factor < 0 or factor > 1:
            message = "Lightening factor must be in range 0 to 1! -> '%s'" % factor
            raise ValueError(message)
        
        # make color
        r = self._red + (255 - self._red) * factor
        g = self._green + (255 - self._green) * factor
        b = self._blue + (255 - self._blue) * factor
        
        return Color(r, g, b, self._alpha, name)
    
    
    def darker(self, factor=0.2, name=None):
        """
        Creates derived color by making current color darker. The factor
        specifies relative amount of black to be added, i.e. 1 results in full
        black color while 0 makes no change. The new color is automatically
        registered for later use if the name is specified.
        
        Args:
            factor: float
                Amount of darkening to be applied in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                Darker color.
        """
        
        # check value
        if factor < 0 or factor > 1:
            message = "Darkening factor must be in range 0 to 1! -> '%s'" % factor
            raise ValueError(message)
        
        # make color
        r = self._red * (1. - factor)
        g = self._green * (1. - factor)
        b = self._blue * (1. - factor)
        
        return Color(r, g, b, self._alpha, name)
    
    
    def opaque(self, opacity=1, name=None):
        """
        Creates derived color by setting the opacity. 0 results in fully
        transparent color while 1 means fully opaque. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            opacity: float
                Opacity value in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                New color with specified opacity.
        """
        
        # check value
        if opacity < 0 or opacity > 1:
            message = "Opacity must be in range 0 to 1! -> '%s'" % opacity
            raise ValueError(message)
        
        # make color
        alpha = opacity * 255
        
        return Color(self._red, self._green, self._blue, alpha, name)
    
    
    def trans(self, transparency=1, name=None):
        """
        Creates derived color by setting the transparency. 0 results in fully
        opaque color while 1 means fully transparent. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            transparency: float
                Transparency value in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                New color with specified transparency.
        """
        
        # check value
        if transparency < 0 or transparency > 1:
            message = "Transparency must be in range 0 to 1! -> '%s'" % transparency
            raise ValueError(message)
        
        # make color
        alpha = 255 - transparency * 255
        
        return Color(self._red, self._green, self._blue, alpha, name)
    
    
    @staticmethod
    def create(value):
        """
        Initializes new color from given value. The color can be specified as an
        RGB or RGBA tuple, hex code, name or pero.Color.
        
        Args:
            value: str, (int,) or pero.Color
                Any supported color definition.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        # clone given color instance
        if isinstance(value, Color):
            return Color(value.red, value.green, value.blue, value.alpha)
        
        # convert from channels
        if isinstance(value, (list, tuple)):
            if len(value) == 3:
                return Color(value[0], value[1], value[2])
            if len(value) == 4:
                return Color(value[0], value[1], value[2], value[3])
        
        # convert from string
        if isinstance(value, str):
            
            # convert from hex
            if value[0] == '#':
                return Color.from_hex(value)
            
            # use registered name
            return Color.from_name(value)
        
        # unable to parse
        message = "Cannot create new color from given value! -> %s" % (value,)
        raise ValueError(message)
    
    
    @staticmethod
    def from_name(name):
        """
        Initializes a color from registered name.
        
        Args:
            name: str
                Registered color name.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        # get color
        if name in COLORS:
            return COLORS[name]
        
        # name not found
        message = "Unknown color name specified! -> '%s'" % name
        raise ValueError(message)
    
    
    @staticmethod
    def from_hex(color, name=None):
        """
        Initializes a color from hex value. The value can be provided either as
        RGB or RGBA channels where all channels are defined by one or two
        digits/characters. The value can be prefixed by '#'. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            color: str
                Hex color representation.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        # strip prefix
        value = color.lstrip('#')
        
        # parse channels
        if len(value) == 3 or len(value) == 4:
            channels = list(int(value[i]+value[i], 16) for i in range(0, len(value)))
        
        elif len(value) == 6 or len(value) == 8:
            channels = list(int(value[i:i+2], 16) for i in range(0, len(value), 2))
        
        else:
            message = "Unrecognized hex color value! -> %s" % color
            raise ValueError(message)
        
        return Color(*channels, name=name)
    
    
    @staticmethod
    def from_int(color, alpha_first=False, alpha_relative=False, name=None):
        """
        Initializes a color from integer value. Additional arguments can be used
        to specify position and range of the alpha channel. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            color: int
                Integer representation.
            
            alpha_first: bool
                Set to True if alpha channel is specified first.
            
            alpha_relative: bool
                Set to True if alpha channel is specified in %/100.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        if alpha_first:
            a = ((color >> 24) & 0xFF)
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
        else:
            r = ((color >> 24) & 0xFF)
            g = (color >> 16) & 0xFF
            b = (color >> 8) & 0xFF
            a = color & 0xFF
        
        if alpha_relative:
            a = int(a / 255.)
        
        return Color(r,g,b,a, name)
    
    
    @staticmethod
    def interpolate(color1, color2, x, name=None):
        """
        Initializes new color by interpolating relative position between two
        colors. The new color is automatically registered for later use if the
        name is specified.
        
        Args:
            color1: str, (int,) or pero.Color
                First color.
            
            color2: str, (int,) or pero.Color
                Second color.
            
            x: float
                Relative position in %/100.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                Interpolated color.
        """
        
        # check types
        if not isinstance(color1, Color):
            color1 = Color.create(color1)
        
        if not isinstance(color2, Color):
            color2 = Color.create(color2)
        
        # interpolate channels
        x = float(x)
        red = color1.red + x*(color2.red-color1.red)
        green = color1.green + x*(color2.green-color1.green)
        blue = color1.blue + x*(color2.blue-color1.blue)
        alpha = color1.alpha + x*(color2.alpha-color1.alpha)
        
        # crop channels
        red = max(0., min(255., red))
        green = max(0., min(255., green))
        blue = max(0., min(255., blue))
        alpha = max(0., min(255., alpha))
        
        # make color
        return Color(red, green, blue, alpha, name)
