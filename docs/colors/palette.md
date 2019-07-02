# Palettes


## Registered Palettes

Registered palette can be accessed by its name via *[pero.PALETTES](palette.md)* library (e.g. `p =
pero.PALETTES.Blues`) or directly from the *[pero.Palette](palette.md)* class (e.g. `p = pero.Palette.Blues`). All newly created
palettes with specified name are automatically registered and available. The default palettes can also be accessed
directly from the *pero.colors* module (e.g. `p = pero.colors.Blues`).

![Registered palettes](images/palettes.svg)


## pero.Palette(colors, name=None)

Represents a color palette defined by series of colors.

- **colors:** *([color definition](color.md),)*  
  Sequence of color definitions. Any supported color definition can be used inside the sequence (e.g. RGB(A) tuple, hex,
  registered name or *[pero.Color](color.md)*)

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *[pero.PALETTES](palette.md)* library.


### Properties


#### name -> *str* or *None*
Gets the palette name or *None* if note set.

#### colors -> *([pero.Color](color.md),)*
Gets a tuple of palette colors.


### Methods


#### reversed(name=None) -> *[pero.Palette](palette.md)*
Creates derived palette by taking current colors in reversed order. The new palette is automatically registered for
later use if the name is specified.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *[pero.PALETTES](palette.md)* library.


### Static Methods


#### create(value, name=None) -> *[pero.Palette](palette.md)*
Creates new palette from given value. The palette can be specified as a sequence of color definitions, unique library
name or existing pero.Palette to get its copy. The new palette is automatically registered for later use if the name is
specified.

- **value:** *str*, *([color definition](color.md), )* or *[pero.Palette](palette.md)*  
  Any supported palette definition.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *[pero.PALETTES](palette.md)* library.


#### from_name(name) -> *[pero.Palette](palette.md)*
Gets the palette from library by its registered name (case in-sensitive).

- **name:** *str*  
  Registered palette name.


#### from_palette(palette, count, name=Name) -> *[pero.Palette](palette.md)*
Creates new palette by picking requested number of colors from given color sequence, while keeping original color range.
The new palette is automatically registered for later use if the name is specified.

- **palette:** *[pero.Palette](palette.md)*, *([color definition](color.md),)*  
  Existing palette or Sequence of colors in any supported format.

- **count:** *int*  
  Number of colors to pick.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *[pero.PALETTES](palette.md)* library.


#### from_gradient(gradient, count, name=None) -> *[pero.Palette](palette.md)*
Creates new palette by interpolating requested number of colors from given gradient. The new palette is automatically
registered for later use if the name is specified.

- **gradient:** *[pero.Gradient](gradient.md)*, *[pero.Palette](palette.md)* or *([color definition](color.md),)  
  Existing gradient, palette or sequence of colors in any supported format.

- **count:** *int*  
  Number of colors to pick.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the palette in the *[pero.PALETTES](palette.md)* library.
