# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_utils.ipynb.

# %% auto 0
__all__ = ['rgetattr', 'rsetattr']

# %% ../nbs/01_utils.ipynb 4
import functools
from typing import Dict 
import pandas as pd 
import numpy as np

# %% ../nbs/01_utils.ipynb 5
def rgetattr(obj, attr, *args):
    """Recursive getattr (for nested attributes)."""
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

# %% ../nbs/01_utils.ipynb 6
def rsetattr(obj, attr, val):
    """Recursive setattr (for nested attributes)."""
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)