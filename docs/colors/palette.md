# Palettes

![Registered palettes](images/palettes.svg)


## *class* Palette(colors, name=None)

Represents a color palette defined by series of colors.

- **colors:** *(color definition,)*  
  Sequence of color definitions. Any supported color definition can be used inside the sequence (e.g. RGB(A) tuple, hex,
  registered name or *pero.Color*)

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *pero.PALETTES* library.


### Properties


#### name -> *str* or *None*
Gets the palette name or *None* if note set.

#### colors -> *(pero.Color,)*
Gets a tuple of palette colors.


### Methods


#### reversed(name=None) -> *pero.Palette*
Creates derived palette by taking current colors in reversed order. The new palette is automatically registered for
later use if the name is specified.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *pero.PALETTES* library.


### Static Methods


#### create(value) -> *pero.Palette*
Creates new palette from given value. The palette can be specified as a sequence of color definitions, unique library
name or existing pero.Palette to get its copy.

- **value:** *str*, *(color definition, ) or *pero.Palette*  
  Any supported palette definition.


#### from_name(name) -> *pero.Palette*
Gets the palette from library by its registered name (case in-sensitive).

- **name:** *str*  
  Registered palette name.


#### from_palette(palette, count, name=Name) -> *pero.Palette*
Creates new palette by picking requested number of colors from given color sequence, while keeping original color range.
The new palette is automatically registered for later use if the name is specified.

- **palette:** *pero.Palette*, *(color definition,)*  
  Existing palette or Sequence of colors in any supported format.

- **count:** *int*  
  Number of colors to pick.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *pero.PALETTES* library.


#### from_gradient(gradient, count, name=None) -> *pero.Palette*
Creates new palette by interpolating requested number of colors from given gradient. The new palette is automatically
registered for later use if the name is specified.

- **gradient:** *pero.Gradient*, *pero.Palette* or *(color definition,)  
  Existing gradient, palette or sequence of colors in any supported format.

- **count:** *int*  
  Number of colors to pick.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *pero.PALETTES* library.
