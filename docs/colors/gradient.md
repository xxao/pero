# Gradients


## Registered Gradients

Registered gradient can be accessed by its name via *[pero.GRADIENTS](gradient.md)* library (e.g. `g =
pero.GRADIENTS.Blues`) or directly from the *[pero.Gradient](gradient.md)* class (e.g. `g = pero.Gradient.Blues`). All
newly created gradients with specified name are automatically registered and available.

![Registered gradients](images/gradients.svg)


## *class* Gradient(colors, stops=None, name=None)

Represents a gradient color generator defined by series of colors and their positions.

- **colors:** *([color definition](color.md),)* or *[pero.Palette](palette.md)*  
  Sequence of color definitions. Any supported color definition can be used inside the sequence (e.g. RGB(A) tuple, hex,
  unique library name or *[pero.Color](color.md)*)

- **stops:** *(float,)* or *None*  
  Sequence of stop positions for each color. If set to *None*, equidistant stops are generated automatically using range
  0 to 1.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the gradient in the *[pero.GRADIENTS](gradient.md)* library.


### Properties


#### name -> *str* or *None*
Gets the gradient name or *None* if note set.

#### colors -> *([pero.Color](color.md),)*
Gets a tuple of gradient colors.

#### stops -> *(float,)*
Gets a tuple of color positions.


### Methods


#### color_at(position, name=None) -> *[pero.Color](color.md)*
Creates interpolated color for given position. The new color is automatically registered for later use if the name is
specified.

- **position:** *float*  
  Position of the color within defined gradient range.
 
- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in the *pero.COLORS* library.


#### normalized(start=0, end=1, name=None) -> *[pero.Gradient](gradient.md)*
Creates a new instance of current gradient normalized to specified range. The new gradient is automatically registered
for later use if the name is specified.

- **position:** *float*  
  Position of the color within defined gradient range.
 
- **name:** *str* or *None*  
  If the name is provided, it is used to register the gradient in the *[pero.GRADIENTS](gradient.md)* library.


### Static Methods


#### create(value, name=None) -> *[pero.Gradient](gradient.md)*
Creates new gradient from given value. The gradient can be specified as a sequence of color definitions, unique library
name of the gradient or palette, *[pero.Palette](palette.md)* or *[pero.Gradient](gradient.md)*. The new gradient is
automatically registered for later use if the name is specified.

- **value:** *str*, *([color definition](color.md), )*, *[pero.Palette](palette.md)* or *[pero.Gradient](gradient.md)*  
  Any supported palette definition.
 
- **name:** *str* or *None*  
  If the name is provided, it is used to register the gradient in the *[pero.GRADIENTS](gradient.md)* library.


#### from_name(name) -> *[pero.Gradient](gradient.md)*
Gets the gradient from library by registered name of gradient or palette (case in-sensitive).
 
- **name:** *str* or *None*  
  Registered gradient or palette name.