# Enums

There are several constants used throughout the *pero* library to define
angle units, various text properties, line and fill properties,
shortcuts to create predefined glyphs or to position objects relative to
each other.


## Drawing Enums

### <a id="ANGLE" href="#ANGLE">#</a> pero.ANGLE

Used to specify angle units.

- **pero.ANGLE_DEG**: Angle defined in degrees.
- **pero.ANGLE_RAD**: Angle defined in radians.


### <a id="LINE_CAP" href="#LINE_CAP">#</a> pero.LINE_CAP

Used to specify a shape to be used at line ends.

![Line Cap](images/line_cap.svg)

- **pero.LINE_CAP_BUTT**: A line cuts directly after endpoint.
- **pero.LINE_CAP_SQUARE**: A line continues beyond endpoint for half its width.
- **pero.LINE_CAP_ROUND**: A line continues beyond endpoint by half circle to
  form round endpoints.


### <a id="LINE_JOIN" href="#LINE_JOIN">#</a> pero.LINE_JOIN

Used to specify a line join style.

![Line Join](images/line_join.svg)

- **pero.LINE_JOIN_BEVEL**: A line join is cutout at the distance of half line width.
- **pero.LINE_JOIN_MITER**: Extends a line join to follow the angle of segments.
- **pero.LINE_JOIN_ROUND**: A line join is filled by circle to form round join.


### <a id="LINE_STYLE" href="#LINE_STYLE">#</a> pero.LINE_STYLE

Used to specify a line style.

![Line Style](images/line_style.svg)

- **pero.LINE_STYLE_SOLID**: A line is drawn as a solid line.
- **pero.LINE_STYLE_DOTTED**: A line is drawn as a series of dots and spaces.
- **pero.LINE_STYLE_DASHED**: A line is drawn as a series of dashes and spaces.
- **pero.LINE_STYLE_DASHDOTTED**: A line is drawn as a series of dashes, dots and spaces.
- **pero.LINE_STYLE_CUSTOM**: A line is drawn according to definition given by 'line_dash'.


### <a id="FILL_STYLE" href="#FILL_STYLE">#</a> pero.FILL_STYLE

Used to specify a filling style.

- **pero.FILL_STYLE_SOLID**: Uses current fill color to draw fills.
- **pero.FILL_STYLE_TRANS**: Uses transparent color to draw fills.


### <a id="FILL_RULE" href="#FILL_RULE">#</a> pero.FILL_RULE
Used to specify a path filling rule.

![Fill Rule](images/fill_rule.svg)

- **pero.FILL_RULE_EVENODD**: Fills an area according to inside/outside state.
- **pero.FILL_RULE_WINDING**: Fills a whole enclosed area.


### <a id="LINE_STEP" href="#LINE_STEP">#</a> pero.LINE_STEP

Used to specify a profile line steps style.

![Line Step](images/line_step.svg)

- **pero.LINE_STEP_NONE**: Data points are connected directly by strait line.
- **pero.LINE_STEP_BEFORE**: A horizontal line starts before data points.
- **pero.LINE_STEP_AFTER**: A horizontal line starts after data points.
- **pero.LINE_STEP_MIDDLE**: A horizontal line crosses data points.


## Text Enums

### <a id="FONT_FAMILY" href="#FONT_FAMILY">#</a> pero.FONT_FAMILY

Used to specify a font family, rather then exact font to use.

![Font Family](images/font_family.svg)

- **pero.FONT_FAMILY_SERIF**: Default serif font will be used (e.g. Times).
- **pero.FONT_FAMILY_SANS**: Default sans-serif font will be used (e.g. Arial or Helvetica).
- **pero.FONT_FAMILY_MONO**: Default monospaced font will be used (e.g. Courier).


### <a id="FONT_STYLE" href="#FONT_STYLE">#</a> pero.FONT_STYLE

Used to specify a font style to use.

![Font Style](images/font_style.svg)

- **pero.FONT_STYLE_NORMAL**: Normal font style variant will be used.
- **pero.FONT_STYLE_ITALIC**: Italic font style variant will be used.


### <a id="FONT_WEIGHT" href="#FONT_WEIGHT">#</a> pero.FONT_WEIGHT

Used to specify a font weight to use. Note that not all values are supported by all backends and the closest value might
be used instead (e.g. pero.HEAVY falls to pero.BOLD).

![Font Weight](images/font_weight.svg)

- **pero.FONT_WEIGHT_NORMAL**: Normal font weight variant will be used.
- **pero.FONT_WEIGHT_LIGHT**: Light font weight variant will be used.
- **pero.FONT_WEIGHT_BOLD**: Bold font weight variant will be used.
- **pero.FONT_WEIGHT_BLACK**: Black font weight variant will be used.
- **pero.FONT_WEIGHT_HEAVY**: Heavy font weight variant will be used.
- **pero.FONT_WEIGHT_SEMIBOLD**: Semi-bold font weight variant will be used.
- **pero.FONT_WEIGHT_MEDIUM**: Medium font weight variant will be used.
- **pero.FONT_WEIGHT_ULTRALIGHT**: Ultra-light font weight variant will be used.
- **pero.FONT_WEIGHT_THIN**: Thin font weight variant will be used.


### <a id="TEXT_ALIGN" href="#TEXT_ALIGN">#</a> pero.TEXT_ALIGN

Used to specify a text horizontal alignment.

![Text Align](images/text_align.svg)

- **pero.TEXT_ALIGN_LEFT**: Uses the text left side as anchor.
- **pero.TEXT_ALIGN_CENTER**: Uses the text center as anchor.
- **pero.TEXT_ALIGN_RIGHT**: Uses the text right side as anchor.


### <a id="TEXT_BASE" href="#TEXT_BASE">#</a> pero.TEXT_BASE

Used to specify a text vertical alignment.

![Text Base](images/text_base.svg)

- **pero.TEXT_BASE_TOP**: Uses the text top side as anchor.
- **pero.TEXT_BASE_MIDDLE**: Uses the text center as anchor.
- **pero.TEXT_BASE_BOTTOM**: Uses the text bottom side as anchor.


### <a id="TEXT_ROTATION" href="#TEXT_ROTATION">#</a> pero.TEXT_ROTATION

Used to define a way to align text labels around a circle according to their angle.

![Text Rotation](images/text_rotation.svg)

- **pero.TEXT_ROT_NONE**: Labels are drawn horizontally, aligned to the circle.
- **pero.TEXT_ROT_FOLLOW**: Labels are drawn the way their left or right side follows the circle.
- **pero.TEXT_ROT_NATURAL**: Labels are drawn the way their top or bottom side follows the circle.
- **pero.TEXT_ROT_FACEOUT**: Labels are drawn the way their bottom side follows the circle.
- **pero.TEXT_ROT_FACEIN**: Labels are drawn the way their top side follows the circle.


## Glyphs Enums

### <a id="MARKER" href="#MARKER">#</a> pero.MARKER

Used to specify a marker glyph type shortcut to create [pero.Marker](../drawing/marker.md#Marker).

![Markers](images/markers.svg)

- Use the "*" character for [pero.Asterisk](../drawing/marker.md#Asterisk) marker.
- Use the "o" character for [pero.Circle](../drawing/marker.md#Circle) marker.
- Use the "x" character for [pero.Cross](../drawing/marker.md#Cross) marker.
- Use the "+" character for [pero.Plus](../drawing/marker.md#Plus) marker.
- Use the "t" character for [pero.Triangle](../drawing/marker.md#Triangle) marker.
- Use the "s" character for [pero.Square](../drawing/marker.md#Square) marker.
- Use the "d" character for [pero.Diamond](../drawing/marker.md#Diamond) marker.
- Use the "p" character for [pero.Pentagon](../drawing/marker.md#Pentagon) marker.
- Use the "h" character for [pero.Hexagon](../drawing/marker.md#Hexagon) marker.


### <a id="ARROW" href="#ARROW">#</a> pero.ARROW

Used to specify an arrow glyph type shortcut to create [pero.Arrow](../drawing/arrow.md#Arrow).

![Arrows](images/arrows.svg)

- Use the "c" character for [pero.ArcArrow](../drawing/arrow.md#ArcArrow) arrow.
- Use the ")" character for [pero.BowArrow](../drawing/arrow.md#BowArrow) arrow.
- Use the "~" character for [pero.CurveArrow](../drawing/arrow.md#CurveArrow) arrow.
- Use the "-" character for [pero.LineArrow](../drawing/arrow.md#LineArrow) arrow.
- Use the "/" character for [pero.RayArrow](../drawing/arrow.md#RayArrow) arrow.
- Use the "z" character for line [pero.ConnectorArrow](../drawing/arrow.md#ConnectorArrow) arrow.
- Use the "s" character for curve [pero.ConnectorArrow](../drawing/arrow.md#ConnectorArrow) arrow.


### <a id="HEAD" href="#HEADS">#</a> pero.HEAD

Used to specify an arrow head type shortcut to create [pero.Head](../drawing/arrow.md#Head).

![Arrow Heads](images/heads.svg)

- Use the "o" character for [pero.CircleHead](../drawing/arrow.md#CircleHead) arrow head.
- Use the "\|" character for [pero.LineHead](../drawing/arrow.md#LineHead) arrow head.
- Use the "<\|" or "\|>" characters for [pero.NormalHead](../drawing/arrow.md#NormalHead) arrow head.
- Use the "<" or ">" characters for [pero.OpenHead](../drawing/arrow.md#OpenHead) arrow head.
- Use the "<<" or ">>" characters for [pero.VeeHead](../drawing/arrow.md#VeeHead) arrow head.


## Position Enums

### <a id="ORIENTATION" href="#ORIENTATION">#</a> pero.ORIENTATION

Used to specify an object orientation.

- **pero.ORI_HORIZONTAL**
- **pero.ORI_VERTICAL**


### <a id="POSITION_LR" href="#POSITION_LR">#</a> pero.POSITION_LR

Used to specify an object horizontal position.

- **pero.POS_LEFT**
- **pero.POS_RIGHT**


### <a id="POSITION_LRC" href="#POSITION_LRC">#</a> pero.POSITION_LRC

Used to specify an object horizontal position.

- **pero.POS_LEFT**
- **pero.POS_RIGHT**
- **pero.POS_CENTER**


### <a id="POSITION_TB" href="#POSITION_TB">#</a> pero.POSITION_TB

Used to specify an object vertical position.

- **pero.POS_TOP**
- **pero.POS_BOTTOM**


### <a id="POSITION_TBC" href="#POSITION_TBC">#</a> pero.POSITION_TBC

Used to specify an object vertical position.

- **pero.POS_TOP**
- **pero.POS_BOTTOM**
- **pero.POS_CENTER**


### <a id="POSITION_LRTB" href="#POSITION_LRTB">#</a> pero.POSITION_LRTB

Used to specify an object cross position.

- **pero.POS_LEFT**
- **pero.POS_RIGHT**
- **pero.POS_TOP**
- **pero.POS_BOTTOM**


### <a id="POSITION_LRTBC" href="#POSITION_LRTBC">#</a> pero.POSITION_LRTBC

Used to specify an object cross position.

- **pero.POS_LEFT**
- **pero.POS_RIGHT**
- **pero.POS_TOP**
- **pero.POS_BOTTOM**
- **pero.POS_CENTER**


### <a id="POSITION_IOC" href="#POSITION_IOC">#</a> pero.POSITION_IOC

Used to specify an object relative position.

- **pero.POS_INSIDE**
- **pero.POS_OUTSIDE**
- **pero.POS_CENTER**


### <a id="POSITION_SEM" href="#POSITION_SEM">#</a> pero.POSITION_SEM

Used to specify an object relative position.

- **pero.POS_START**
- **pero.POS_END**
- **pero.POS_MIDDLE**


### <a id="POSITION_TL" href="#POSITION_TL">#</a> pero.POSITION_TL

Used to specify an object corner position.

- **pero.POS_TOP**
- **pero.POS_LEFT**


### <a id="POSITION_TR" href="#POSITION_TR">#</a> pero.POSITION_TR

Used to specify an object corner position.

- **pero.POS_TOP**
- **pero.POS_RIGHT**


### <a id="POSITION_BL" href="#POSITION_BL">#</a> pero.POSITION_BL

Used to specify an object corner position.

- **pero.BOTTOM**
- **pero.LEFT**


### <a id="POSITION_BR" href="#POSITION_BR">#</a> pero.POSITION_BR

Used to specify an object corner position.

- **pero.POS_BOTTOM**
- **pero.POS_RIGHT**


### <a id="POSITION_COMPASS" href="#POSITION_COMPASS">#</a> pero.POSITION_COMPASS

Used to specify an object compass-like position.

- **pero.POS_N**
- **pero.POS_NW**
- **pero.POS_NE**
- **pero.POS_S**
- **pero.POS_SW**
- **pero.POS_SE**
- **pero.POS_W**
- **pero.POS_E**
- **pero.POS_C**
