#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . values import *
from . enum import Enum

# define backends
BACKEND_JSON = JSON
BACKEND_SVG = SVG
BACKEND_QT = QT
BACKEND_WX = WX
BACKEND_CAIRO = CAIRO
BACKEND_MUPDF = MUPDF
BACKEND_PYTHONISTA = PYTHONISTA

BACKEND = Enum(
    JSON = BACKEND_JSON,
    SVG = BACKEND_SVG,
    QT = BACKEND_QT,
    WX = BACKEND_WX,
    CAIRO = BACKEND_CAIRO,
    MUPDF = BACKEND_MUPDF,
    PYTHONISTA = BACKEND_PYTHONISTA)

# define image formats supported by JSON backend
EXPORT_JSON = {
    '.json'}

# define image formats supported by SVG backend
EXPORT_SVG = {
    '.svg'}

# define image formats supported by QT backend
EXPORT_QT = {
    '.bmp',
    '.gif',
    '.jpg',
    '.jpeg',
    '.pdf',
    '.png'}

# define image formats supported by WX backend
EXPORT_WX = {
    '.bmp',
    '.cur',
    '.ico',
    '.jpg',
    '.jpeg',
    '.pcx',
    '.png',
    '.pnm',
    '.tif',
    '.tiff',
    '.xpm'}

# define formats supported by Cairo backend
EXPORT_CAIRO = {
    '.bmp',
    '.eps',
    '.gif',
    '.jpg',
    '.jpeg',
    '.pdf',
    '.png',
    '.svg',
    '.tif',
    '.tiff'}

# define image formats supported by MuPDF backend
EXPORT_MUPDF = {
    '.pdf'}

# define image formats supported by Pythonista backend
EXPORT_PYTHONISTA = {
    '.png'}

# define available formats
EXPORT_FORMATS = {
    BACKEND_JSON: EXPORT_JSON,
    BACKEND_SVG: EXPORT_SVG,
    BACKEND_QT: EXPORT_QT,
    BACKEND_WX: EXPORT_WX,
    BACKEND_CAIRO: EXPORT_CAIRO,
    BACKEND_MUPDF: EXPORT_MUPDF,
    BACKEND_PYTHONISTA: EXPORT_PYTHONISTA}

# define export backend priorities
EXPORT_PRIORITY = [
    BACKEND_JSON,
    BACKEND_SVG,
    BACKEND_QT,
    BACKEND_WX,
    BACKEND_CAIRO,
    BACKEND_MUPDF,
    BACKEND_PYTHONISTA]

# define viewer backend priorities
VIEWER_PRIORITY = [
    BACKEND_QT,
    BACKEND_WX,
    BACKEND_PYTHONISTA]

# define default export size
EXPORT_WIDTH = 750
EXPORT_HEIGHT = 500

VIEWER_WIDTH = 750
VIEWER_HEIGHT = 500
