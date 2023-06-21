# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['collect_stats', 'to_df', 'to_tex']

# %% ../nbs/00_core.ipynb 4
from typing import List
import importlib
import numpy as np
import pandas as pd

import statsmodels.api as sm
from linearmodels import PanelOLS

from .utils import *

# %% ../nbs/00_core.ipynb 7
def collect_stats(res, # results object to extract stats from
                  package: str=None, # name of package that generated 'res' object
                  get_default_stats = True, # if True, returns all stats implemented by the f'{package}_results' module
                  add_stats: dict=None, # keys are stats to extract in addition to the default ones, values are attributes of 'res'
                  add_literals: dict=None, # additional info to be added to output dict as literal strings
                  ) -> dict:
    """Collects stats from 'res' object. stats in 'add_stats' can override default stats()"""

    if res.__module__.startswith('linearmodels'): package = 'linearmodels'
    if res.__module__.startswith('statsmodels'): package = 'statsmodels'

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

# %% ../nbs/00_core.ipynb 13
def to_df(res_list: List[dict], # list of outputs from `collect_stats()`
          which_xvars: list=None, # if None, report all xvars
          stats_body: list=['params', 'tstats'], # each element of 'res_list' needs to have these stats as keys; values must be pd.Series
          stats_bottom: list=['r2', 'nobs'], # each element of 'res_list' needs to have these stats as keys; values must be scalars
          labels: dict=None,
          add_formats: dict=None  
          ) -> pd.DataFrame: 
    """Combines results from multiple `collect_stats()` outputs into a single pd.DataFrame"""  
    
    formats = default_formats()
    if add_formats is not None: formats.update(add_formats)
    
    columns = []
    for i,res in enumerate(res_list):
        newcol = pd.concat([res[x] for x in stats_body], axis=1, ignore_index=True).set_axis(stats_body, axis=1)
        for x in stats_body:
            newcol[x] = newcol[x].map(formats[x].format)
            if x == 'params':
                newcol[x] += get_stars(res['pvalues'])
            else:
                newcol[x] = '(' + newcol[x] + ')'
        newcol = newcol.stack(level=0) #set_index('coeff_names')
        columns.append(newcol)

    out = pd.concat(columns, axis = 1)
    if which_xvars is None: out = out.loc[which_xvars].copy()
    
    for i,res in enumerate(res_list):
        for x in stats_bottom:
            out.loc[x,i] = formats[x].format(res[x]) if x in formats else res[x]

    if labels is not None:
        for var in set(out.droplevel(1).index):
            if var in labels: out = out.rename(index={var:labels[var]}, level=0)            

    return out.astype('string').fillna('')

# %% ../nbs/00_core.ipynb 15
def to_tex(get_pdf=True, open_pdf=False):
    pass
