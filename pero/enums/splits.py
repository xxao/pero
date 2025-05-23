#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# define engineering splits
SPLITS_ENG = {
    "y": 1e-24,
    "z": 1e-21,
    "a": 1e-18,
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "": 1e0,
    "k": 1e3,
    "M": 1e6,
    "G": 1e9,
    "T": 1e12,
    "P": 1e15,
    "E": 1e18,
    "Z": 1e21,
    "Y": 1e24}

# define bytes splits
SPLITS_BYTES = {
    "": 2**0,
    "k": 2**10,
    "M": 2**20,
    "G": 2**30,
    "T": 2**40,
    "P": 2**50,
    "E": 2**60,
    "Z": 2**70,
    "Y": 2**80}

# define time splits
SPLITS_TIME = {
    "d": 24*60*60,
    "h": 60*60,
    "m": 60,
    "s": 1,
    "ms": 1e-3,
    "us": 1e-6,
    "ns": 1e-9}
