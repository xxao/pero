#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . library import Library

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
    
    
    def __init__(self, *args, name=None):
        """
        Initializes a new instance of Color.
        
        Args:
            args: (int, int, int), (int, int, int, int) or str
                The RGB(A) channels can be provided as 3 or 4 integers for
                individual channels, tuple of 3 or 4 integers or hex string with
                leading '#'.
            
            name: str or None
                Unique name to register.
        """
        
        # init channels
        channels = None
        red, green, blue, alpha = (0, 0, 0, 255)
        
        # convert from channels
        if len(args) == 3 or len(args) == 4:
            channels = args
        
        # convert from single value
        elif len(args) == 1:
            
            # get value
            value = args[0]
            
            # get channels
            if isinstance(value, (list, tuple)):
                channels = value
            
            # convert from hex
            elif isinstance(value, str):
                
                # strip prefix
                value = value.lstrip('#')
                
                # parse channels
                if len(value) == 3 or len(value) == 4:
                    channels = list(int(value[i]+value[i], 16) for i in range(0, len(value)))
                
                elif len(value) == 6 or len(value) == 8:
                    channels = list(int(value[i:i+2], 16) for i in range(0, len(value), 2))
        
        # check channels
        if channels is None or len(channels) < 3 or len(channels) > 4:
            message = "Unrecognized color definition! -> %s" % (args,)
            raise ValueError(message)
        
        # get channels
        if len(channels) == 3:
            red, green, blue = channels
        
        elif len(channels) == 4:
            red, green, blue, alpha = channels
        
        # check channels
        for c in (red, green, blue, alpha):
            if not isinstance(c, (int, float)) or c < 0 or c > 255:
                message = "Color channels must be a number between 0 and 255! -> (%s, %s, %s, %s)" % (red, green, blue, alpha)
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
        range 0 to 255. This might me useful to implement backends not
        supporting color transparency.
        
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
                Relative amount of white to be added in range 0 to 1.
            
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
        
        return Color(r, g, b, self._alpha, name=name)
    
    
    def darker(self, factor=0.2, name=None):
        """
        Creates derived color by making current color darker. The factor
        specifies relative amount of black to be added, i.e. 1 results in full
        black color while 0 makes no change. The new color is automatically
        registered for later use if the name is specified.
        
        Args:
            factor: float
                Relative amount of black to be added in range 0 to 1.
            
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
        
        return Color(r, g, b, self._alpha, name=name)
    
    
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
        
        return Color(self._red, self._green, self._blue, alpha, name=name)
    
    
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
        
        return Color(self._red, self._green, self._blue, alpha, name=name)
    
    
    @staticmethod
    def create(value, name=None):
        """
        Creates new color from given value. The color can be specified as an
        RGB or RGBA tuple of integers, hex code, unique library name or existing
        pero.Color to get its copy. The new color is automatically registered
        for later use if the name is specified.
        
        Args:
            value: str, (int, int, int), (int, int, int, int) or pero.Color
                Any supported color definition.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        # clone given color instance
        if isinstance(value, Color):
            return Color(value.rgba, name=name)
        
        # convert from channels
        if isinstance(value, (list, tuple)):
            return Color(value, name=name)
        
        # convert from string
        if isinstance(value, str):
            
            # convert from hex
            if value[0] == '#':
                return Color(value, name=name)
            
            # use registered name
            return Color.from_name(value)
        
        # unable to parse
        message = "Cannot create new color from given value! -> %s" % (value,)
        raise ValueError(message)
    
    
    @staticmethod
    def from_name(name):
        """
        Gets the color from library by its registered name (case in-sensitive).
        
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
    def from_int(value, alpha_first=False, alpha_relative=False, name=None):
        """
        Creates a color from integer value. Additional arguments can be used
        to specify position and range of the alpha channel. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            value: int
                Integer representation.
            
            alpha_first: bool
                If set to True the alpha channel is expected to be the at the first channel.
            
            alpha_relative: bool
                If set to True the alpha channel is expected to be specified in range from 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                RGBA color.
        """
        
        if alpha_first:
            a = ((value >> 24) & 0xFF)
            r = (value >> 16) & 0xFF
            g = (value >> 8) & 0xFF
            b = value & 0xFF
        else:
            r = ((value >> 24) & 0xFF)
            g = (value >> 16) & 0xFF
            b = (value >> 8) & 0xFF
            a = value & 0xFF
        
        if alpha_relative:
            a = int(a / 255.)
        
        return Color(r, g, b, a, name=name)
    
    
    @staticmethod
    def interpolate(color1, color2, x, name=None):
        """
        Creates new color by interpolating relative position between two
        colors. The new color is automatically registered for later use if the
        name is specified.
        
        Args:
            color1: str, (int, int, int), (int, int, int, int) or pero.Color
                First color.
            
            color2: str, (int, int, int), (int, int, int, int) or pero.Color
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
        return Color(red, green, blue, alpha, name=name)
