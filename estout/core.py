# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['collect_stats', 'to_df', 'to_tex']

# %% ../nbs/00_core.ipynb 3
import importlib
import numpy as np
import pandas as pd

import statsmodels.api as sm
from linearmodels import PanelOLS

from .utils import *

# %% ../nbs/00_core.ipynb 6
def collect_stats(res, # results object to extract stats from
                  package: str, # name of package that generated 'res' object
                  get_default_stats = True, # if True, returns all stats implemented by the f'{package}_results' module
                  add_stats: dict=None, # keys are stats to extract in addition to the default ones, values are attributes of 'res'
                  add_literals: dict=None, # additional info to be added to output dict as literal strings
                  ) -> dict:
    """Collects stats from 'res' object. stats in 'add_stats' can override defaults."""

    out = {}
    out['package'] = package
    results_module = importlib.import_module(f"estout.{package}_results")

    if get_default_stats:
        for stat in results_module.default_stats():
            out[stat] = rgetattr(results_module, stat)(res)

    if add_stats is not None:
        for stat, attr in add_stats.items():
            out[stat] = rgetattr(res, attr)

    if add_literals is not None:
        out.update(add_literals)
        
    return out

# %% ../nbs/00_core.ipynb 12
def to_df(res_list,
          which_xvars: list=None, # if None, report all xvars
          stats_body: list=['params', 'tstats'],
          stats_bottom: list=['r2', 'nobs'],
          labels: dict=None 
          ) -> pd.DataFrame: 
    

    return 

# %% ../nbs/00_core.ipynb 14
def to_tex(get_pdf=True, open_pdf=False):
    pass
