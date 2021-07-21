#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import sys
import os.path
from PIL import ImageFont
from .. enums import *


class FontManager(object):
    """
    Font manager holds information about all supported fonts currently
    available. This is mainly used to speed up text size calculations and font
    handling for canvas like SVG, where no specific text size calculation is
    available. For now, only the TrueType or OpenType fonts are supported.
    """
    
    def __init__(self):
        """Initializes a new instance of FontManager."""
        
        self._fonts = {}
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        buff = "["
        for font in self.fonts:
            buff += "\n%s" % font
        buff += "\n]"
        
        return buff
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return self.__str__()
    
    
    @property
    def families(self):
        """
        Gets all available font families names.
        
        Returns:
            (str,)
                Tuple of font families names.
        """
        
        return tuple(sorted(self._fonts.keys()))
    
    
    @property
    def fonts(self):
        """
        Gets all available fonts sorted by name.
        
        Returns:
            (pero.Font,)
                Tuple of fonts
        """
        
        fonts = (self._fonts[name] for name in sorted(self._fonts.keys()))
        return tuple(v for f in fonts for v in f)
    
    
    def get_font(self, family, style=None, weight=None):
        """
        Gets specified font from library.
        
        Args:
            family: str
                Family name of the font.
            
            style: pero.FONT_STYLE or None
                Specifies requested style of the font as any item from the
                pero.FONT_STYLE enum or None if not important.
            
            weight: pero.FONT_WEIGHT or None
                Specifies requested weight of the font as any item from the
                pero.FONT_WEIGHT enum or None if not important.
        
        Returns:
            pero.Font or None
                Requested font or None if not found.
        """
        
        # get fonts
        fonts = self._fonts.get(family, None)
        if fonts is None:
            return None
        
        # check style
        fonts = [f for f in fonts if (not style or f.style == style)]
        
        # check specific weight
        for font in fonts:
            if not weight or font.weight == weight:
                return font
        
        # check light weight loosely
        if weight in FONT_WEIGHTS_LIGHT:
            for font in fonts:
                if font.weight in FONT_WEIGHTS_LIGHT:
                    return font
        
        # check bold weight loosely
        if weight in FONT_WEIGHTS_BOLD:
            for font in fonts:
                if font.weight in FONT_WEIGHTS_BOLD:
                    return font
        
        return None
    
    
    def load_fonts(self, path):
        """
        Loads all supported fonts from specified folder.
        
        Args:
            path: str
                Absolute path to the fonts folder.
        """
        
        for file_name in os.listdir(path):
            self.load_font(os.path.join(path, file_name))
    
    
    def load_font(self, path, name=None):
        """
        Loads specified font file.
        
        Args:
            path: str
                Absolute path to the font definition file.
            
            name: str or None
                Specific (system) font name. Family name is used if not
                provided.
        """
        
        # get filename and extension
        dir_name, file_name = os.path.split(path)
        base_name, extension = os.path.splitext(file_name)
        
        # load TrueType or OpenType font
        font = None
        if extension.lower() in ('.ttf', '.otf', '.ttc'):
            font = Font.from_ttf(path, name)
        
        # check font
        if font is None:
            return
        
        # add to library
        if font.family not in self._fonts:
            self._fonts[font.family] = [font]
        else:
            self._fonts[font.family].append(font)
    
    
    def load(self):
        """Loads all supported fonts from known system locations."""
        
        # load MSWin fonts
        if sys.platform == 'win32':
            
            paths = [
                r"c:\Windows\Fonts"]
            
            for path in paths:
                if os.path.exists(path):
                    self.load_fonts(path)
        
        # load macOS fonts
        elif sys.platform == 'darwin':
            
            paths = [
                r"/Library/Fonts/",
                r"/Network/Library/Fonts/",
                r"/System/Library/Fonts/"]
            
            home = os.environ.get('HOME')
            if home is not None:
                path = os.path.join(home, 'Library', 'Fonts')
                paths.append(path)
            
            for path in paths:
                if os.path.exists(path):
                    self.load_fonts(path)
        
        # load iOS fonts
        elif sys.platform == 'ios':
            
            from objc_util import ObjCClass
            ui_font = ObjCClass('UIFont')
            
            for family in ui_font.familyNames():
                names = ui_font.fontNamesForFamilyName_(family)
                for name in names:
                    font = ImageFont.truetype(str(name), 10)
                    if font is not None:
                        self.load_font(font.path, str(name))


class Font(object):
    """This class holds some basic information about available font."""
    
    
    def __init__(self, path, name, family, style, weight):
        """Initializes a new instance of Font."""
        
        self._path = path
        self._name = name
        self._family = family
        self._style = style
        self._weight = weight
        
        self._cache = {}
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "%s (%s | %s | %s) [%s]" % (self._family, self._name, self._style, self._weight, self._path)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    
    @property
    def path(self):
        """
        Gets absolute path to the font file.
        
        Returns:
            str
                Absolute path to font file.
        """
        
        return self._path
    
    
    @property
    def name(self):
        """
        Gets the font name.
        
        Returns:
            str
                Font name.
        """
        
        return self._name
    
    
    @property
    def family(self):
        """
        Gets the font family name.
        
        Returns:
            str
                Font family name.
        """
        
        return self._family
    
    
    @property
    def style(self):
        """
        Gets the font style.
        
        Returns:
            pero.FONT_STYLE
                Font style.
        """
        
        return self._style
    
    
    @property
    def weight(self):
        """
        Gets the font weight.
        
        Returns:
            pero.FONT_WEIGHT
                Font weight.
        """
        
        return self._weight
    
    
    def get_font(self, size):
        """
        Gets initialized PIL font.
        
        Args:
            size: int
                Font size.
        
        Returns:
            PIL.ImageFont
                Initialized font with specified size.
        """
        
        if size not in self._cache:
            self._cache[size] = ImageFont.truetype(self._path, size)
        
        return self._cache[size]
    
    
    def get_size(self, text, size):
        """
        Gets text size for given text.
        
        Args:
            text: str
                Text for which the size should be calculated.
            
            size: int
                Font size to be used.
        
        Returns:
            (float, float)
                Text size as width and height.
        """
        
        return self.get_font(size).getsize(text)
    
    
    def get_descent(self, size):
        """
        Gets font descent for given font size.
        
        Args:
            size: int
                Font size to be used.
        
        Returns:
            float
                Font descent.
        """
        
        font = self.get_font(size)
        
        m = font.getsize("M")[1]
        mj = font.getsize("Mj")[1]
        
        return mj - m
    
    
    @staticmethod
    def from_ttf(path, name=None):
        """
        Creates a new instance of Font.
        
        Args:
            path: str
                Absolute path to a font definition file.
            
            name: str
                Specific (system) name of the font variant.
        
        Returns:
            pero.Font or None
                Font information or None if not supported.
        """
        
        try:
            font = ImageFont.truetype(path, 10)
            
            font_family, font_type = font.getname()
            font_name = name or font_family
            font_style = FONT_STYLE_NORMAL
            font_weight = FONT_WEIGHT_NORMAL
            
            # get style
            if 'Italic' in font_type:
                font_style = FONT_STYLE_ITALIC
            
            elif 'Oblique' in font_type:
                font_style = FONT_STYLE_ITALIC
            
            # get weight
            if 'Regular' in font_type:
                font_weight = FONT_WEIGHT_NORMAL
            
            elif 'Bold' in font_type:
                font_weight = FONT_WEIGHT_BOLD
            
            elif 'Light' in font_type:
                font_weight = FONT_WEIGHT_LIGHT
            
            elif 'Black' in font_type:
                font_weight = FONT_WEIGHT_BLACK
            
            elif 'Heavy' in font_type:
                font_weight = FONT_WEIGHT_HEAVY
            
            elif 'Semibold' in font_type:
                font_weight = FONT_WEIGHT_SEMIBOLD
            
            elif 'Medium' in font_type:
                font_weight = FONT_WEIGHT_MEDIUM
            
            elif 'Ultralight' in font_type:
                font_weight = FONT_WEIGHT_ULTRALIGHT
            
            elif 'Thin' in font_type:
                font_weight = FONT_WEIGHT_THIN
            
            # make font
            return Font(path, font_name, font_family, font_style, font_weight)
        
        except:
            return None


# initializes available fonts
FONTS = FontManager()
FONTS.load()
