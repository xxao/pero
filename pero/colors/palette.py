#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from . library import Library
from . color import Color

# init library
PALETTES = Library()


class PaletteMeta(type):
    """Defines a meta class for the main Palette class."""
    
    
    def __getattr__(cls, key):
        """
        Gets registered named palette by its name.
        
        Returns:
            palette: pero.Palette
                Corresponding palette.
        """
        
        return PALETTES[key]


class Palette(object, metaclass=PaletteMeta):
    """Represents a color palette defined by series of colors."""
    
    
    def __init__(self, colors, name=None):
        """
        Initializes a new instance of Palette.
        
        Args:
            colors: (color,)
                Sequence of color definitions. Any supported color definition
                can be used inside the sequence (e.g. rgba tuple, hex, name or
                pero.Color).
            
            name: str or None
                Unique name to register.
        """
        
        # set name
        self._name = name
        
        # get colors
        self._colors = []
        for color in colors:
            if not isinstance(color, Color):
                color = Color.create(color)
            self._colors.append(color)
        
        self._colors = tuple(self._colors)
        
        # register color by name
        if name is not None:
            PALETTES.add(self)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        name = ""
        if self._name is not None:
            name = " %s" % self._name
        
        colors = [str(c) for c in self._colors]
        
        return "%s(\n\t%s)" % (name, ",\n\t".join(colors))
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    
    def __len__(self):
        """Gets number of available colors."""
        
        return len(self._colors)
    
    
    def __iter__(self):
        """Gets colors iterator."""
        
        return self._colors.__iter__()
    
    
    def __getitem__(self, value):
        """Gets color at position."""
        
        return self._colors.__getitem__(value)
    
    
    @property
    def name(self):
        """
        Gets palette name.
        
        Returns:
            str or None
                Palette name.
        """
        
        return self._name
    
    
    @property
    def colors(self):
        """
        Gets colors.
        
        Returns:
            (pero.Color,)
                Palette colors.
        """
        
        return self._colors
    
    
    def lighter(self, factor=0.2, name=None):
        """
        Creates derived palette by making current colors lighter. The factor
        specifies relative amount of white to be added, i.e. 1 results in full
        white color while 0 makes no change. The new palette is automatically
        registered for later use if the name is specified.
        
        Args:
            factor: float
                Relative amount of white to be added in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Palette
                Lighter palette.
        """
        
        colors = [c.lighter(factor) for c in self._colors]
        return Palette(colors, name)
    
    
    def darker(self, factor=0.2, name=None):
        """
        Creates derived palette by making current colors darker. The factor
        specifies relative amount of black to be added, i.e. 1 results in full
        black color while 0 makes no change. The new palette is automatically
        registered for later use if the name is specified.
        
        Args:
            factor: float
                Relative amount of black to be added in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Palette
                Darker palette.
        """
        
        colors = [c.darker(factor) for c in self._colors]
        return Palette(colors, name)
    
    
    def opaque(self, opacity=1, name=None):
        """
        Creates derived palette by setting the opacity to current colors.
        0 results in fully transparent colors while 1 means fully opaque.
        The new palette is automatically registered for later use if the name
        is specified.
        
        Args:
            opacity: float
                Opacity value in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Palette
                New palette with specified opacity.
        """
        
        colors = [c.opaque(opacity) for c in self._colors]
        return Palette(colors, name)
    
    
    def trans(self, transparency=1, name=None):
        """
        Creates derived palette by setting the transparency to current colors.
        0 results in fully opaque colors while 1 means fully transparent.
        The new palette is automatically registered for later use if the name
        is specified.
        
        Args:
            transparency: float
                Transparency value in range 0 to 1.
            
            name: str or None
                Unique name to register.
        
        Returns:
            pero.Palette
                New palette with specified transparency.
        """
        
        colors = [c.opaque(transparency) for c in self._colors]
        return Palette(colors, name)
    
    
    def reversed(self, name=None):
        """
        Creates derived palette by taking current colors in reversed order. The
        new palette is automatically registered for later use if the name is
        specified.
        
        Args:
            name: str
                Unique name to register.
        
        Returns:
            pero.Palette
                Reversed palette.
        """
        
        return Palette(reversed(self._colors), name)
    
    
    @staticmethod
    def create(value, name=None):
        """
        Creates new palette from given value. The palette can be specified as a
        sequence of color definitions, unique library name or existing
        pero.Palette to get its copy. The new palette is automatically
        registered for later use if the name is specified.
        
        Args:
            value: str, tuple or pero.Palette
                Any supported palette definition.
            
            name: str
                Unique name to register.
        
        Returns:
            pero.Palette
                Palette.
        """
        
        # clone given palette instance
        if isinstance(value, Palette):
            return Palette(value.colors, name=name)
        
        # convert from color collection
        if isinstance(value, (list, tuple)):
            return Palette(value, name=name)
        
        # convert from name
        if isinstance(value, str):
            return Palette.from_name(value)
            
        message = "Cannot create new palette from given value! -> %s" % (value,)
        raise ValueError(message)
    
    
    @staticmethod
    def from_name(name):
        """
        Gets the palette from library by its registered name (case in-sensitive).
        
        Args:
            name: str
                Registered palette name.
        
        Returns:
            pero.Palette
                Palette.
        """
        
        # get color
        if name in PALETTES:
            return PALETTES[name]
        
        # name not found
        message = "Unknown palette name specified! -> '%s'" % name
        raise ValueError(message)
    
    
    @staticmethod
    def from_palette(palette, count, name=None):
        """
        Creates new palette by picking requested number of colors from given
        color sequence, while keeping original color range. The new palette is
        automatically registered for later use if the name is specified.
        
        Args:
            palette: pero.Palette or (pero.Color,)
                Sequence of colors to choose from.
            
            count: int
                Number of colors to pick.
            
            name: str
                Unique name to register.
        
        Returns:
            pero.Palette
                Selected colors.
        """
        
        # check count
        if count > len(palette):
            message = "Given palette contains only %s colors, %d requested!" % (len(palette), count)
            raise ValueError(message)
        
        # select colors
        selection = [int(numpy.floor(i)) for i in numpy.linspace(0, len(palette)-1, num=count)]
        colors = [palette[i] for i in selection]
        
        return Palette(colors, name)
    
    
    @staticmethod
    def from_gradient(gradient, count, name=None):
        """
        Creates new palette by interpolating requested number of colors from
        given gradient. The new palette is automatically registered for later
        use if the name is specified.
        
        Args:
            gradient: pero.Gradient, pero.Palette or (color,)
                Gradient colors.
            
            count: int
                Number of colors to pick.
            
            name: str
                Unique name to register.
        
        Returns:
            pero.Palette
                Interpolated colors.
        """
        
        # import gradient
        from .gradient import Gradient
        
        # make gradient
        if not isinstance(gradient, Gradient):
            gradient = Gradient(gradient)
        
        # select colors
        stops = [x for x in numpy.linspace(0, 1, num=count)]
        colors = [gradient.color_at(x) for x in stops]
        
        return Palette(colors, name)
