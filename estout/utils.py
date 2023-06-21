# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_utils.ipynb.

# %% ../nbs/01_utils.ipynb 3
from __future__ import annotations
from pathlib import Path
import os
import platform
from subprocess import PIPE, Popen, run, SubprocessError
import functools
from typing import Dict, List, Tuple 
import pandas as pd 

# %% auto 0
__all__ = ['rgetattr', 'rsetattr', 'default_formats', 'get_stars', 'model_groups', 'tex_table_env', 'make_pdf_from_tex',
           'open_pdf_file']

# %% ../nbs/01_utils.ipynb 4
def rgetattr(obj, attr, *args):
    """Recursive getattr (for nested attributes)."""
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

# %% ../nbs/01_utils.ipynb 5
def rsetattr(obj, attr, val):
    """Recursive setattr (for nested attributes)."""
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# %% ../nbs/01_utils.ipynb 6
def default_formats() -> dict:
    """Default output formats for some very common statistics."""
    return  {'params':'{:.2f}', 
            'tstats':'{:.2f}', 
            'pvalues': '{:.3f}',
            'se':'{:.2f}', 
            'r2':'{:.3f}',
            'nobs':'{:.0f}'
            }

# %% ../nbs/01_utils.ipynb 8
def get_stars(pvalues: pd.Series, # this is compared to key of 'stars' parameter to determine how many stars should be added
            stars: dict = {.1:'*',.05:'**',.01:'***'} # todo: default values to the left are star symbols that are not rendered correctly in markdown
            ) -> pd.Series:
    """For each pvalue, check the lowest key in 'stars' for which the pvalue is smaller than that key, and return the corresponding nr of stars."""

    param_names = list(pvalues.index)

    #Sort 'stars' by key (in reverse order)
    ks = list(stars.keys())
    ks.sort(reverse=True)
    stars = {k: stars[k] for k in ks}

    out = pd.Series('', index=param_names)
    for param in param_names:    
        for alpha in stars:
            if pvalues[param] < alpha:
                out[param] = stars[alpha]
                
    return out

# %% ../nbs/01_utils.ipynb 11
def model_groups(column_group_names: Dict[str, List[int]], # keys are group titles, values are lists of column indices included in each group
                add_clines: bool=True # if True, adds lines below group names
                ) -> str:
    """Returns LaTex code needed to add at the top of the table in order to give names to groups of columns in the table."""
    
    group_names = ''
    group_lines = ''
    for key,value in column_group_names.items():
        if type(key) != str:
            raise TypeError('Each key in column_group_names must be a string')
        if type(value) != list:
            raise TypeError("Each value in column_group_names dict must be a list")
        if len(value) != 2:
            raise TypeError("Each value in column_group_names dict must contain two integers")
        
        value = sorted(value)
        group_names += '& \multicolumn{%i}{c}{%s} ' %(value[1]-value[0]+1,key)
        if add_clines:
            group_lines += '\cline{%s-%s} ' %(str(value[0]+1),str(value[1]+1))

    return group_names + ' \\\\ \n' + group_lines + ' \n'

# %% ../nbs/01_utils.ipynb 13
def tex_table_env(nr_columns: int, # number of columns in the table
                    env: str='tabularx' # latex tabular environment specification. either 'tabularx' or 'tabular*'
                    ) -> Tuple[str,str]:
    """Creates LaTex code to add at the top of the table to create the correct tabular environment."""

    if env=='tabularx':
        header = '\\begin{tabularx}{\\textwidth}{@{}l *{%i}{>{\centering\\arraybackslash}X}@{}}' %nr_columns 
        footer = '\\end{tabularx}'
    elif env=='tabular*':
        header = '\\begin{tabular*}{\\textwidth}{@{\extracolsep{\\fill}}l*{%i}{c}}' %nr_columns
        footer = '\\end{tabular*}'
    else:
        raise NotImplemented(f"LaTex tabular environment {env} has not yet been implemented in tex_table_env()")
    return header,footer 

# %% ../nbs/01_utils.ipynb 16
def make_pdf_from_tex(tex_file_path: Path|str):
    if isinstance(tex_file_path,str):
        tex_file_path = Path(tex_file_path)
    os.chdir(tex_file_path.parent)   
    process = Popen(['pdflatex',tex_file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False)
    output, errors = process.communicate()
    if process.returncode == 0:
        print("PDF creation successful!")
    else:
        print("PDF creation failed. Errors:", errors.decode('utf-8'))
    return Path(str.replace(str(tex_file_path), '.tex', '.pdf'))

# %% ../nbs/01_utils.ipynb 17
def open_pdf_file(file_path):
    try:
        if platform.system() == "Windows": run(['start', file_path])
        else: run(['open', file_path])
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except SubprocessError:
        print(f"Error opening PDF file: {file_path}")
