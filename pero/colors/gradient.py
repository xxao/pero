#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .library import Library
from .color import Color
from .palette import Palette, PALETTES

# init library
GRADIENTS = Library()


class GradientMeta(type):
    """Defines a meta class for the main Gradient class."""
    
    
    def __getattr__(cls, key):
        """
        Gets registered named gradient by its name.
        
        Returns:
            pero.Gradient
                Corresponding gradient.
        """
        
        return GRADIENTS[key]


class Gradient(object, metaclass=GradientMeta):
    """
    Represents a gradient color generator defined by series of colors and their 
    positions.
    """
    
    
    def __init__(self, colors, stops=None, name=None):
        """
        Initializes a new instance of Gradient.
        
        Args:
            colors: (color,) or pero.Palette
                Sequence of color definitions. Any supported color definition
                can be used inside the sequence (e.g. rgba tuple, hex, name or
                pero.Color).
            
            stops: (float,) or None
                Sequence of stop positions for each color. If set to None,
                equidistant stops are generated automatically using range 0 to 1.
            
            name: str or None
                Unique name to register.
        """
        
        super(Gradient, self).__init__()
        
        # set name
        self._name = name
        
        # check colors
        if len(colors) == 0:
            raise AttributeError("Gradient must be defined by one color at least!")
        elif len(colors) == 1:
            colors = (colors[0], colors[0])
        
        # get colors
        self._colors = []
        
        for color in colors:
            if not isinstance(color, Color):
                color = Color.create(color)
            self._colors.append(color)
        
        self._colors = tuple(self._colors)
        
        # check stops
        if stops is not None:
            
            # check stops type
            for stop in stops:
                if not isinstance(stop, (int, float)):
                    message = "Stop positions must be numbers! -> %s" % type(stop)
                    raise TypeError(message)
            
            # check stops sorted
            if not all(stops[i] < stops[i+1] for i in range(len(stops)-1)):
                message = "Stop positions must be sorted! -> %s" % (stops,)
                raise ValueError(message)
            
            # test same size
            if len(colors) != len(stops):
                message = "Number of colors and stops must be equal!"
                raise ValueError(message)
            
            # format to float
            stops = tuple(map(float, stops))
        
        # generate stops
        else:
            stops = self._calc_stops(len(colors))
        
        self._stops = tuple(stops)
        
        # register gradient by name
        if name is not None:
            GRADIENTS.add(self)
    
    
    @property
    def name(self):
        """
        Gets gradient name.
        
        Returns:
            str or None
                Gradient name.
        """
        
        return self._name
    
    
    @property
    def colors(self):
        """
        Gets gradient colors.
        
        Returns:
            (pero.Color,)
                Gradient colors.
        """
        
        return self._colors
    
    
    @property
    def stops(self):
        """
        Gets color stops.
        
        Returns:
            (float,)
                Position of each color.
        """
        
        return self._stops
    
    
    def color_at(self, position, name=None):
        """
        Creates interpolated color for given position. The new color is
        automatically registered for later use if the name is specified.
        
        Args:
            position: float
                Position of the color within defined gradient range.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Color
                Interpolated color.
        """
        
        # check colors
        if not self._colors:
            return None
        
        # check edges
        if position <= self._stops[0]:
            return self._colors[0]
        
        if position >= self._stops[-1]:
            return self._colors[-1]
        
        # find colors around
        idx = self._locate(self._stops, position)
        left_color = self._colors[idx-1]
        right_color = self._colors[idx]
        
        # calc relative position
        left_stop = self._stops[idx-1]
        right_stop = self._stops[idx]
        position = (position - left_stop)/(right_stop - left_stop)
        
        # interpolate color
        return Color.interpolate(left_color, right_color, position, name)
    
    
    def normalized(self, start=0., end=1., name=None):
        """
        Creates a new instance of current gradient normalized to specified range.
        The new gradient is automatically registered for later use if the name
        is specified.
        
        Args:
            start: float
                Start of the normalizing range.
            
            end: float
                End of the normalizing range.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Gradient
                Normalized gradient.
        """
        
        # check colors
        if not self._colors:
            return Gradient(self._colors, name=name)
        
        # already normalized
        if self._stops[0] == start and self._stops[-1] == end:
            return Gradient(self._colors, self._stops, name)
        
        # calc normalization
        from_range = self._stops[-1] - self._stops[0]
        to_range = end - start
        
        stops = []
        for stop in self._stops:
            stop = start + to_range * float(stop - self._stops[0]) / from_range
            stops.append(stop)
        
        return Gradient(self._colors, stops, name)
    
    
    def _calc_stops(self, size):
        """Calculates equidistant stops for given number of colors."""
        
        if size == 0:
            return ()
        
        stops = []
        step = 1./(size-1)
        
        value = 0
        while value < 1:
            stops.append(value)
            value += step
        
        stops.append(1.)
        
        return stops
    
    
    def _locate(self, items, x):
        """Locates nearest higher color."""
        
        lo = 0
        hi = len(items)
        
        while lo < hi:
            mid = (lo + hi) // 2
            if items[mid] > x:
                hi = mid
            else:
                lo = mid + 1
        
        return lo
    
    
    @staticmethod
    def create(value, name=None):
        """
        Creates new gradient from given value. The gradient can be specified
        as a sequence of color definitions, palette, gradient or palette name,
        pero.Palette or pero.Gradient. The new gradient is automatically
        registered for later use if the name is specified.
        
        Args:
            value: str, (color,), pero.Palette or pero.Gradient
                Any supported gradient definition.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Gradient
                Gradient.
        """
        
        # clone given gradient instance
        if isinstance(value, Gradient):
            return Gradient(value.colors, value.stops, name=name)
        
        # convert from palette
        if isinstance(value, Palette):
            return Gradient(value, name=name)
        
        # convert from color collection
        if isinstance(value, (list, tuple)):
            return Gradient(value, name=name)
        
        # convert from name
        if isinstance(value, str):
            return Gradient.from_name(value)
        
        message = "Cannot create new gradient from given value! -> %s" % (value,)
        raise ValueError(message)
    
    
    @staticmethod
    def from_name(name):
        """
        Gets the gradient from library by registered name of gradient or palette (case in-sensitive).
        
        Args:
            name: str
                Registered gradient or palette name.
        
        Returns:
            pero.Gradient
                Gradient.
        """
        
        # try from gradients
        if name in GRADIENTS:
            return GRADIENTS[name]
        
        # try from palettes
        if name in PALETTES:
            return Gradient(PALETTES[name])
        
        # name not found
        message = "Unknown gradient or palette name specified! -> '%s'" % name
        raise ValueError(message)
