Text Enums
==========

pero.FONT_FAMILY
----------------
Used to specify a font family, rather then exact font to use.

.. image:: images/font_family.svg

- **pero.SERIF**: Default serif font will be used (e.g. Times).
- **pero.SANS**: Default sans-serif font will be used (e.g. Arial or Helvetica).
- **pero.MONO**: Default monospaced font will be used (e.g. Courier).


pero.FONT_STYLE
---------------
Used to specify a font style to use.

.. image:: images/font_style.svg

- **pero.NORMAL**: Normal font style variant will be used.
- **pero.ITALIC**: Italic font style variant will be used.


pero.FONT_WEIGHT
----------------
Used to specify a font weight to use. Note that not all values are supported by all backends and the closest value might
be used instead (e.g. pero.HEAVY falls to pero.BOLD).

.. image:: images/font_weight.svg

- **pero.NORMAL**: Normal font weight variant will be used.
- **pero.LIGHT**: Light font weight variant will be used.
- **pero.BOLD**: Bold font weight variant will be used.
- **pero.BLACK**: Black font weight variant will be used.
- **pero.HEAVY**: Heavy font weight variant will be used.
- **pero.SEMIBOLD**: Semi-bold font weight variant will be used.
- **pero.MEDIUM**: Medium font weight variant will be used.
- **pero.ULTRALIGHT**: Ultra-light font weight variant will be used.
- **pero.THIN**: Thin font weight variant will be used.


pero.TEXT_ALIGN
---------------
Used to specify a text horizontal alignment.

.. image:: images/text_align.svg

- **pero.LEFT**: Uses the text left side as anchor.
- **pero.CENTER**: Uses the text center as anchor.
- **pero.RIGHT**: Uses the text right side as anchor.


pero.TEXT_BASELINE
------------------
Used to specify a text vertical alignment.

.. image:: images/text_base.svg

- **pero.TOP**: Uses the text top side as anchor.
- **pero.MIDDLE**: Uses the text center as anchor.
- **pero.BOTTOM**: Uses the text bottom side as anchor.


pero.TEXT_ROTATION
------------------
Used to define a way to align text labels around a circle according to their angle.

.. image:: images/text_rotation.svg

- **pero.NONE**: Labels are drawn horizontally, aligned to the circle.
- **pero.FOLLOW**: Labels are drawn the way their left or right side follows the circle.
- **pero.NATURAL**: Labels are drawn the way their top or bottom side follows the circle.
- **pero.FACEOUT**: Labels are drawn the way their bottom side follows the circle.
- **pero.FACEIN**: Labels are drawn the way their top side follows the circle.
