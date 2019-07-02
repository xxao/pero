# pero.backends

The actual drawing is done by various backends, for which the *pero* library provides consistent API. This is achieved
by specific implementations of a canvas base class, which translates the API into methods and logic of particular
backend. As of now, the *pero* library supports [wxPython](https://pypi.org/project/wxPython/),
[PyCairo](https://pypi.org/project/pycairo/), [PyMuPDF](https://pypi.org/project/PyMuPDF/),
[Pythonista](http://omz-software.com/pythonista/) app and its own implementation of SVG and JSON canvas.

Under construction...