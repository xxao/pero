# pero.colors

One of the key element of any drawing is, of course, a color. Inside the *pero* library, colors are defined by their
RGB(A) channels using dedicated class. Additional classes are available to define and use color pallets and gradients.
Many standard colors and palettes are available and can be easily accessed by corresponding name from the
*pero.colors* module.


## *class* Color(red, green, blue, alpha=255, name=None)

Represents a color defined by red, green, blue and alpha channels.

- **red:** *int*  
  Red channel as a value in range 0 to 255.

- **green:** *int*  
  Green channel as a value in range 0 to 255.

- **blue:** *int*  
  Blue channel as a value in range 0 to 255.

- **alpha:** *int*  
  Alpha channel as a value in range 0 to 255.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


### Properties


#### name -> *str* or *None*
Gets the color name or *None* if note set.

#### red -> *int*
Gets red channel as a value in range 0 to 255.

#### green -> *int*
Gets green channel as a value in range 0 to 255.

#### blue -> *int*
Gets blue channel as a value in range 0 to 255.

#### alpha -> *int*
Gets alpha channel as a value in range 0 to 255 where 0 means fully transparent and 255 fully opaque.

#### rgba -> *(int, int, int, int)*
Gets RGBA channels tuple where each channel is defined as integer in range 0 to 255.

#### rgb -> *(int, int, int)*
Gets RGB channels tuple where each channel is defined as integer in range 0 to 255. This might me useful to implement
backends not supporting color transparency.

#### rgba_r -> *(float, float, float, float)*
Gets RGBA channels tuple where each channel is defined as float in range 0 to 1.

#### rgb_r -> *(float, float, float)*
Gets RGB channels tuple where each channel is defined as float in range 0 to 1.

#### hex -> *str*
Gets RGBA channels as hex string prefixed by '#'.


### Methods


#### lighter(factor=0.2, name=None) -> *pero.Color*  
Creates derived color by making current color lighter. The factor specifies relative amount of white to be added, i.e. 1
results in full white color while 0 makes no change. The new color is automatically registered for later use if the name
is specified.

- **factor:** *float*  
  Relative amount of white to be added in range 0 to 1.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


#### darker(factor=0.2, name=None) -> *pero.Color*
Creates derived color by making current color darker. The factor specifies relative amount of black to be added, i.e. 1
results in full black color while 0 makes no change. The new color is automatically registered for later use if the name
is specified.

- **factor:** *float*  
  Relative amount of black to be added in range 0 to 1.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


#### opaque(opacity=1, name=None) -> *pero.Color*
Creates derived color by setting the opacity. 0 results in fully transparent color while 1 means fully opaque. The new
color is automatically registered for later use if the name is specified.

- **opacity:** *float*  
  Opacity value in range 0 to 1, where 0 means fully transparent, 1 means fully opaque.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


#### trans(transparency=1, name=None) -> *pero.Color*
Creates derived color by setting the transparency. 0 results in fully opaque color while 1 means fully transparent. The
new color is automatically registered for later use if the name is specified.

- **transparency:** *float*  
  Transparency value in range 0 to 1, where 0 means fully opaque, 1 means fully transparent.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


### Static Methods


#### create(value) -> *pero.Color*
Creates a color from given value. The color can be specified as an RGB or RGBA tuple of integers, hex code, unique
library name or existing pero.Color to get its copy.

- **value:** *str*, *(int, int, int)*, *(int, int, int, int)* or *pero.Color*  
  Any supported color definition.


#### from_name(value) -> *pero.Color*
Gets the color from library by its registered name (case in-sensitive). 

- **value:** *str*  
  Registered color name.


#### from_hex(value, name=None) -> *pero.Color*
Creates a color from its hex value (e.g. #FFA500). The value can be provided either as RGB or RGBA channels where all
channels are defined by one or two digits/characters. The value can be prefixed by '#'. The color is automatically
registered for later use if the name is specified.

- **value:** *str*  
  Hex color representation.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


#### from_int(value, alpha_first=False, alpha_relative=False, name=None) -> *pero.Color*
Creates a color from its integer value. Additional arguments can be used to specify position and range of the alpha
channel. The new color is automatically registered for later use if the name is specified.

- **value:** *int*  
  Integer color representation.

- **alpha_first:** *bool*  
  If set to *True* the alpha channel is expected to be the at the first channel.

- **alpha_relative:** *bool*  
  If set to *True* the alpha channel is expected to be specified in range from 0 to 1.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.


#### interpolate(color1, color2, x, name=None) -> *pero.Color*
Creates new color by interpolating relative position between two given colors. The new color is automatically registered
for later use if the name is specified.

- **color1:** *pero.Color*  
  First color to interpolate from.

- **color2:** *pero.Color*  
  Second color to interpolate to.

- **x:** *float*  
  Relative position of resulting color in %/100.

- **name:** *str* or *None*  
  If the name is provided, it is used to register the color in a pero color library so it can be later accessed by
  *pero.colors.Name*.
