# Gradients

![Registered gradients](images/gradients.svg)


## *class* Gradient(colors, stops=None, name=None)

Represents a gradient color generator defined by series of colors and their positions.

- **colors:** *(color definition,)* or *pero.Palette*  
  Sequence of color definitions. Any supported color definition can be used inside the sequence (e.g. RGB(A) tuple, hex,
  unique library name or *pero.Color*)

- **stops:** *(float,)* or *None*  
  Sequence of stop positions for each color. If set to *None*, equidistant stops are generated automatically using range
  0 to 1.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the gradient in the *pero.GRADIENTS* library.


### Properties


#### name -> *str* or *None*
Gets the gradient name or *None* if note set.

#### colors -> *(pero.Color,)*
Gets a tuple of gradient colors.

#### stops -> *(float,)*
Gets a tuple of color positions.


### Methods


#### color_at(position, name=None) -> *pero.Color*
Creates interpolated color for given position. The new color is automatically registered for later use if the name is
specified.

- **position:** *float*  
  Position of the color within defined gradient range.
 
- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in the *pero.COLORS* library.


#### normalized(start=0, end=1, name=None) -> *pero.Gradient*
Creates a new instance of current gradient normalized to specified range. The new gradient is automatically registered
for later use if the name is specified.

- **position:** *float*  
  Position of the color within defined gradient range.
 
- **name:** *str* or *None*  
  If the name is provided, it is used to register the gradient in the *pero.GRADIENTS* library.


### Static Methods


#### create(value) -> *pero.Gradient*
Creates new gradient from given value. The gradient can be specified as a sequence of color definitions, unique library
name of the gradient or palette, *pero.Palette* or *pero.Gradient*.

- **value:** *str*, *(color definition, )*, *pero.Palette* or *pero.Gradient*  
  Any supported palette definition.


#### from_name(name) -> *pero.Gradient*
Gets the gradient from library by registered name of gradient or palette (case in-sensitive).
 
- **name:** *str* or *None*  
  Registered gradient or palette name.