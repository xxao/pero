#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# keep version info
QT_VERSION = None
QT_NAME = None

# import PyQt5
if QT_VERSION is None:
    
    try:
        from PyQt5.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
        from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPageSize
        from PyQt5.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
        from PyQt5.QtGui import QMouseEvent, QWheelEvent, QTouchEvent
        from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QDesktopWidget
        from PyQt5.QtPrintSupport import QPrinter
        
        QT_VERSION = 5
        QT_NAME = 'PyQt5'
    
    except ImportError:
        pass

# import PySide2
if QT_VERSION is None:
    
    try:
        from PySide2.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
        from PySide2.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPageSize
        from PySide2.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
        from PySide2.QtGui import QMouseEvent, QWheelEvent, QTouchEvent
        from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QDesktopWidget
        from PySide2.QtPrintSupport import QPrinter
        
        QT_VERSION = 5
        QT_NAME = 'PySide2'
    
    except ImportError:
        pass

# import PyQt6
if QT_VERSION is None:
    
    try:
        from PyQt6.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
        from PyQt6.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPageSize
        from PyQt6.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
        from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
        from PyQt6.QtPrintSupport import QPrinter
        
        QT_VERSION = 6
        QT_NAME = 'PyQt6'
    
    except ImportError:
        pass

# import PySide6
if QT_VERSION is None:
    
    try:
        from PySide6.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
        from PySide6.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPageSize
        from PySide6.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
        from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
        from PySide6.QtPrintSupport import QPrinter
        
        QT_VERSION = 6
        QT_NAME = 'PySide6'
    
    except IOError:
        pass

# check import
if QT_VERSION is None:
    raise ImportError()

# fix version 5
if QT_VERSION == 5:
    
    # set high DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # fix QWidget
    QWidget.screen = lambda s: QDesktopWidget()
    
    # fix QMouseEvt
    QMouseEvent.position = lambda s: s.pos()
    
    # fix QWheelEvent
    QWheelEvent.position = lambda s: s.pos()
    
    # fix QTouchEvent
    QTouchEvent.points = lambda s: s.touchPoints()
    QTouchEvent.TouchPoint.position = lambda d: d.pos()
    QTouchEvent.TouchPoint.lastPosition = lambda d: d.lastPos()
    
    # fix QPrinter
    QPrinter.setPageSize = lambda s, d: s.setPaperSize(d.definitionSize(), QPrinter.Unit.Point)


# fix QApplication 'exec_' method
if not hasattr(QApplication, 'exec'):
    QApplication.exec = lambda d: d.exec_()
