# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_linearmodels.ipynb.

# %% auto 0
__all__ = ['ynames', 'xnames', 'params', 'tstats', 'pvalues', 'covmat', 'se', 'nobs', 'r2']

# %% ../nbs/03_linearmodels.ipynb 4
import numpy as np
import pandas as pd

# %% ../nbs/03_linearmodels.ipynb 10
def ynames(res): return res.model.dependent.vars 

# %% ../nbs/03_linearmodels.ipynb 12
def xnames(res): return res.model.exog.vars

# %% ../nbs/03_linearmodels.ipynb 14
def params(res): return res.params

# %% ../nbs/03_linearmodels.ipynb 17
def tstats(res): return res.tstats

# %% ../nbs/03_linearmodels.ipynb 19
def pvalues(res): return res.pvalues

# %% ../nbs/03_linearmodels.ipynb 21
def covmat(res): return res.cov

# %% ../nbs/03_linearmodels.ipynb 23
def se(res): return pd.Series(np.sqrt(np.diag(np.array(covmat(res)))),index=xnames(res))

# %% ../nbs/03_linearmodels.ipynb 25
def nobs(res): return res.nobs

# %% ../nbs/03_linearmodels.ipynb 27
def r2(res): return res.rsquared
