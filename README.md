# estout

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This file will become your README and also the index of your
documentation.

## Install

``` sh
pip install estout
```

## How to use

Set up an example dataset and run a few regressions to showcase the
functions in this module.

``` python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels import PanelOLS
import estout
```

``` python
np.random.seed(123)
df = pd.DataFrame(np.random.rand(9,3), 
                  columns=['y','x','z'],
                  index = pd.MultiIndex.from_product([[1,2,3],[1,2,3]], names=['firmid','time'])
                  ).assign(cons = 1)
sm1 = sm.OLS(df['y'], df[['cons','x']]).fit()
sm2 = sm.OLS(df['y'], df[['cons','x','z']]).fit().get_robustcov_results(cov_type='HAC', maxlags=2)
lmres = PanelOLS(df['y'],  df[['cons','x','z']], entity_effects=True
                 ).fit(cov_type='clustered', cluster_entity=True)
```

### Extracting statistics after fitting a model

Below, we collect just the default set of statistics from the `sm1`
object. These are given by the functions implemented in the
`statsmodels_results` module (since `sm1` was generated by the
`statsmodels` package).

``` python
estout.collect_stats(sm1)
```

    {'package': 'statsmodels',
     'ynames': ['y'],
     'xnames': ['cons', 'x'],
     'params': cons    0.507852
     x       0.345003
     dtype: float64,
     'tstats': cons    3.905440
     x       1.292246
     dtype: float64,
     'pvalues': cons    0.005858
     x       0.237293
     dtype: float64,
     'covmat':           cons         x
     cons  0.016910 -0.030531
     x    -0.030531  0.071278,
     'se': cons    0.130037
     x       0.266979
     dtype: float64,
     'nobs': 9,
     'r2': 0.19260886185799486}

Collect statistics by specifying the name of their attribute in the
results object (using the `add_stats` parameter):

``` python
estout.collect_stats(sm1, get_default_stats=False, add_stats={'xnames': 'model.exog_names',
                                                              'Adj. R2': 'rsquared_adj'})
```

    {'package': 'statsmodels',
     'xnames': ['cons', 'x'],
     'Adj. R2': 0.07726727069485129}

Add scalar statistics not available as attributes of the results object
(using the `add_literals` paramter):

``` python
estout.collect_stats(sm1, get_default_stats=False, add_literals={'Fixed Effects': 'No', 
                                                                 'Nr observations': 123})
```

    {'package': 'statsmodels', 'Fixed Effects': 'No', 'Nr observations': 123}

### Combining model results into a DataFrame

Start by collecting stats from each model and combining them in a list.

``` python
allmodels = []
for res in [sm1, sm2, lmres]:
    allmodels.append(estout.collect_stats(res))
```

``` python
estout.to_df(allmodels)
```

<style type="text/css">
</style>
<table id="T_878c1" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_878c1_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_878c1_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_878c1_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_878c1_level0_row0" class="row_heading level0 row0" rowspan="2">cons</th>
      <th id="T_878c1_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_878c1_row0_col0" class="data row0 col0" >0.51***</td>
      <td id="T_878c1_row0_col1" class="data row0 col1" >0.70***</td>
      <td id="T_878c1_row0_col2" class="data row0 col2" >0.73***</td>
    </tr>
    <tr>
      <th id="T_878c1_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_878c1_row1_col0" class="data row1 col0" >(3.91)</td>
      <td id="T_878c1_row1_col1" class="data row1 col1" >(21.48)</td>
      <td id="T_878c1_row1_col2" class="data row1 col2" >(167.36)</td>
    </tr>
    <tr>
      <th id="T_878c1_level0_row2" class="row_heading level0 row2" rowspan="2">x</th>
      <th id="T_878c1_level1_row2" class="row_heading level1 row2" >params</th>
      <td id="T_878c1_row2_col0" class="data row2 col0" >0.35</td>
      <td id="T_878c1_row2_col1" class="data row2 col1" >0.57**</td>
      <td id="T_878c1_row2_col2" class="data row2 col2" >0.64*</td>
    </tr>
    <tr>
      <th id="T_878c1_level1_row3" class="row_heading level1 row3" >tstats</th>
      <td id="T_878c1_row3_col0" class="data row3 col0" >(1.29)</td>
      <td id="T_878c1_row3_col1" class="data row3 col1" >(2.85)</td>
      <td id="T_878c1_row3_col2" class="data row3 col2" >(2.26)</td>
    </tr>
    <tr>
      <th id="T_878c1_level0_row4" class="row_heading level0 row4" rowspan="2">z</th>
      <th id="T_878c1_level1_row4" class="row_heading level1 row4" >params</th>
      <td id="T_878c1_row4_col0" class="data row4 col0" ></td>
      <td id="T_878c1_row4_col1" class="data row4 col1" >-0.64**</td>
      <td id="T_878c1_row4_col2" class="data row4 col2" >-0.77**</td>
    </tr>
    <tr>
      <th id="T_878c1_level1_row5" class="row_heading level1 row5" >tstats</th>
      <td id="T_878c1_row5_col0" class="data row5 col0" ></td>
      <td id="T_878c1_row5_col1" class="data row5 col1" >(-3.55)</td>
      <td id="T_878c1_row5_col2" class="data row5 col2" >(-2.91)</td>
    </tr>
    <tr>
      <th id="T_878c1_level0_row6" class="row_heading level0 row6" >r2</th>
      <th id="T_878c1_level1_row6" class="row_heading level1 row6" ></th>
      <td id="T_878c1_row6_col0" class="data row6 col0" >0.193</td>
      <td id="T_878c1_row6_col1" class="data row6 col1" >0.487</td>
      <td id="T_878c1_row6_col2" class="data row6 col2" >0.352</td>
    </tr>
    <tr>
      <th id="T_878c1_level0_row7" class="row_heading level0 row7" >nobs</th>
      <th id="T_878c1_level1_row7" class="row_heading level1 row7" ></th>
      <td id="T_878c1_row7_col0" class="data row7 col0" >9</td>
      <td id="T_878c1_row7_col1" class="data row7 col1" >9</td>
      <td id="T_878c1_row7_col2" class="data row7 col2" >9</td>
    </tr>
  </tbody>
</table>

We can choose to report only a subset of the regressors.

``` python
estout.to_df(allmodels, which_xvars=['x','z'])
```

<style type="text/css">
</style>
<table id="T_14722" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_14722_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_14722_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_14722_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_14722_level0_row0" class="row_heading level0 row0" rowspan="2">x</th>
      <th id="T_14722_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_14722_row0_col0" class="data row0 col0" >0.35</td>
      <td id="T_14722_row0_col1" class="data row0 col1" >0.57**</td>
      <td id="T_14722_row0_col2" class="data row0 col2" >0.64*</td>
    </tr>
    <tr>
      <th id="T_14722_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_14722_row1_col0" class="data row1 col0" >(1.29)</td>
      <td id="T_14722_row1_col1" class="data row1 col1" >(2.85)</td>
      <td id="T_14722_row1_col2" class="data row1 col2" >(2.26)</td>
    </tr>
    <tr>
      <th id="T_14722_level0_row2" class="row_heading level0 row2" rowspan="2">z</th>
      <th id="T_14722_level1_row2" class="row_heading level1 row2" >params</th>
      <td id="T_14722_row2_col0" class="data row2 col0" ></td>
      <td id="T_14722_row2_col1" class="data row2 col1" >-0.64**</td>
      <td id="T_14722_row2_col2" class="data row2 col2" >-0.77**</td>
    </tr>
    <tr>
      <th id="T_14722_level1_row3" class="row_heading level1 row3" >tstats</th>
      <td id="T_14722_row3_col0" class="data row3 col0" ></td>
      <td id="T_14722_row3_col1" class="data row3 col1" >(-3.55)</td>
      <td id="T_14722_row3_col2" class="data row3 col2" >(-2.91)</td>
    </tr>
    <tr>
      <th id="T_14722_level0_row4" class="row_heading level0 row4" >r2</th>
      <th id="T_14722_level1_row4" class="row_heading level1 row4" ></th>
      <td id="T_14722_row4_col0" class="data row4 col0" >0.193</td>
      <td id="T_14722_row4_col1" class="data row4 col1" >0.487</td>
      <td id="T_14722_row4_col2" class="data row4 col2" >0.352</td>
    </tr>
    <tr>
      <th id="T_14722_level0_row5" class="row_heading level0 row5" >nobs</th>
      <th id="T_14722_level1_row5" class="row_heading level1 row5" ></th>
      <td id="T_14722_row5_col0" class="data row5 col0" >9</td>
      <td id="T_14722_row5_col1" class="data row5 col1" >9</td>
      <td id="T_14722_row5_col2" class="data row5 col2" >9</td>
    </tr>
  </tbody>
</table>

Report other statistics under the parameter values.

``` python
estout.to_df(allmodels, stats_body=['params','se','pvalues'], which_xvars=['x'])
```

<style type="text/css">
</style>
<table id="T_086e9" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_086e9_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_086e9_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_086e9_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_086e9_level0_row0" class="row_heading level0 row0" rowspan="3">x</th>
      <th id="T_086e9_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_086e9_row0_col0" class="data row0 col0" >0.35</td>
      <td id="T_086e9_row0_col1" class="data row0 col1" >0.57**</td>
      <td id="T_086e9_row0_col2" class="data row0 col2" >0.64*</td>
    </tr>
    <tr>
      <th id="T_086e9_level1_row1" class="row_heading level1 row1" >se</th>
      <td id="T_086e9_row1_col0" class="data row1 col0" >(0.27)</td>
      <td id="T_086e9_row1_col1" class="data row1 col1" >(0.20)</td>
      <td id="T_086e9_row1_col2" class="data row1 col2" >(0.28)</td>
    </tr>
    <tr>
      <th id="T_086e9_level1_row2" class="row_heading level1 row2" >pvalues</th>
      <td id="T_086e9_row2_col0" class="data row2 col0" >(0.237)</td>
      <td id="T_086e9_row2_col1" class="data row2 col1" >(0.029)</td>
      <td id="T_086e9_row2_col2" class="data row2 col2" >(0.086)</td>
    </tr>
    <tr>
      <th id="T_086e9_level0_row3" class="row_heading level0 row3" >r2</th>
      <th id="T_086e9_level1_row3" class="row_heading level1 row3" ></th>
      <td id="T_086e9_row3_col0" class="data row3 col0" >0.193</td>
      <td id="T_086e9_row3_col1" class="data row3 col1" >0.487</td>
      <td id="T_086e9_row3_col2" class="data row3 col2" >0.352</td>
    </tr>
    <tr>
      <th id="T_086e9_level0_row4" class="row_heading level0 row4" >nobs</th>
      <th id="T_086e9_level1_row4" class="row_heading level1 row4" ></th>
      <td id="T_086e9_row4_col0" class="data row4 col0" >9</td>
      <td id="T_086e9_row4_col1" class="data row4 col1" >9</td>
      <td id="T_086e9_row4_col2" class="data row4 col2" >9</td>
    </tr>
  </tbody>
</table>

Change the statistics reported at the bottom of the table

``` python
estout.to_df(allmodels, stats_bottom=['r2'],  which_xvars=['x'])
```

<style type="text/css">
</style>
<table id="T_5c951" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_5c951_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_5c951_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_5c951_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_5c951_level0_row0" class="row_heading level0 row0" rowspan="2">x</th>
      <th id="T_5c951_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_5c951_row0_col0" class="data row0 col0" >0.35</td>
      <td id="T_5c951_row0_col1" class="data row0 col1" >0.57**</td>
      <td id="T_5c951_row0_col2" class="data row0 col2" >0.64*</td>
    </tr>
    <tr>
      <th id="T_5c951_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_5c951_row1_col0" class="data row1 col0" >(1.29)</td>
      <td id="T_5c951_row1_col1" class="data row1 col1" >(2.85)</td>
      <td id="T_5c951_row1_col2" class="data row1 col2" >(2.26)</td>
    </tr>
    <tr>
      <th id="T_5c951_level0_row2" class="row_heading level0 row2" >r2</th>
      <th id="T_5c951_level1_row2" class="row_heading level1 row2" ></th>
      <td id="T_5c951_row2_col0" class="data row2 col0" >0.193</td>
      <td id="T_5c951_row2_col1" class="data row2 col1" >0.487</td>
      <td id="T_5c951_row2_col2" class="data row2 col2" >0.352</td>
    </tr>
  </tbody>
</table>

Change the formatting for any of the statistics reported.

``` python
estout.to_df(allmodels, add_formats={'params':'{:.3}','r2':'{:.2f}'}, which_xvars=['x'])
```

<style type="text/css">
</style>
<table id="T_a67a8" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_a67a8_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_a67a8_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_a67a8_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a67a8_level0_row0" class="row_heading level0 row0" rowspan="2">x</th>
      <th id="T_a67a8_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_a67a8_row0_col0" class="data row0 col0" >0.345</td>
      <td id="T_a67a8_row0_col1" class="data row0 col1" >0.571**</td>
      <td id="T_a67a8_row0_col2" class="data row0 col2" >0.643*</td>
    </tr>
    <tr>
      <th id="T_a67a8_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_a67a8_row1_col0" class="data row1 col0" >(1.29)</td>
      <td id="T_a67a8_row1_col1" class="data row1 col1" >(2.85)</td>
      <td id="T_a67a8_row1_col2" class="data row1 col2" >(2.26)</td>
    </tr>
    <tr>
      <th id="T_a67a8_level0_row2" class="row_heading level0 row2" >r2</th>
      <th id="T_a67a8_level1_row2" class="row_heading level1 row2" ></th>
      <td id="T_a67a8_row2_col0" class="data row2 col0" >0.19</td>
      <td id="T_a67a8_row2_col1" class="data row2 col1" >0.49</td>
      <td id="T_a67a8_row2_col2" class="data row2 col2" >0.35</td>
    </tr>
    <tr>
      <th id="T_a67a8_level0_row3" class="row_heading level0 row3" >nobs</th>
      <th id="T_a67a8_level1_row3" class="row_heading level1 row3" ></th>
      <td id="T_a67a8_row3_col0" class="data row3 col0" >9</td>
      <td id="T_a67a8_row3_col1" class="data row3 col1" >9</td>
      <td id="T_a67a8_row3_col2" class="data row3 col2" >9</td>
    </tr>
  </tbody>
</table>

Replace regressor (or bottom stats) names with labels.

``` python
estout.to_df(allmodels, labels={'cons':'Intercept', 'nobs':'Observations'}, which_xvars=['cons'])
```

<style type="text/css">
</style>
<table id="T_dcf93" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_dcf93_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_dcf93_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_dcf93_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_dcf93_level0_row0" class="row_heading level0 row0" rowspan="2">Intercept</th>
      <th id="T_dcf93_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_dcf93_row0_col0" class="data row0 col0" >0.51***</td>
      <td id="T_dcf93_row0_col1" class="data row0 col1" >0.70***</td>
      <td id="T_dcf93_row0_col2" class="data row0 col2" >0.73***</td>
    </tr>
    <tr>
      <th id="T_dcf93_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_dcf93_row1_col0" class="data row1 col0" >(3.91)</td>
      <td id="T_dcf93_row1_col1" class="data row1 col1" >(21.48)</td>
      <td id="T_dcf93_row1_col2" class="data row1 col2" >(167.36)</td>
    </tr>
    <tr>
      <th id="T_dcf93_level0_row2" class="row_heading level0 row2" >r2</th>
      <th id="T_dcf93_level1_row2" class="row_heading level1 row2" ></th>
      <td id="T_dcf93_row2_col0" class="data row2 col0" >0.193</td>
      <td id="T_dcf93_row2_col1" class="data row2 col1" >0.487</td>
      <td id="T_dcf93_row2_col2" class="data row2 col2" >0.352</td>
    </tr>
    <tr>
      <th id="T_dcf93_level0_row3" class="row_heading level0 row3" >Observations</th>
      <th id="T_dcf93_level1_row3" class="row_heading level1 row3" ></th>
      <td id="T_dcf93_row3_col0" class="data row3 col0" >9</td>
      <td id="T_dcf93_row3_col1" class="data row3 col1" >9</td>
      <td id="T_dcf93_row3_col2" class="data row3 col2" >9</td>
    </tr>
  </tbody>
</table>

Since the output of
[`to_df`](https://ionmihai.github.io/estout/core.html#to_df) is a
pd.DataFrame, it is easy to add more information at the bottom of the
table without having to re-run
[`collect_stats`](https://ionmihai.github.io/estout/core.html#collect_stats).

``` python
df = estout.to_df(allmodels)
df.loc['Fixed effects',:] = ['No','No','Entity']
df
```

<style type="text/css">
</style>
<table id="T_870de" data-quarto-disable-processing="true">
  <thead>
    <tr>
      <th class="blank" >&nbsp;</th>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_870de_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_870de_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_870de_level0_col2" class="col_heading level0 col2" >2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_870de_level0_row0" class="row_heading level0 row0" rowspan="2">cons</th>
      <th id="T_870de_level1_row0" class="row_heading level1 row0" >params</th>
      <td id="T_870de_row0_col0" class="data row0 col0" >0.51***</td>
      <td id="T_870de_row0_col1" class="data row0 col1" >0.70***</td>
      <td id="T_870de_row0_col2" class="data row0 col2" >0.73***</td>
    </tr>
    <tr>
      <th id="T_870de_level1_row1" class="row_heading level1 row1" >tstats</th>
      <td id="T_870de_row1_col0" class="data row1 col0" >(3.91)</td>
      <td id="T_870de_row1_col1" class="data row1 col1" >(21.48)</td>
      <td id="T_870de_row1_col2" class="data row1 col2" >(167.36)</td>
    </tr>
    <tr>
      <th id="T_870de_level0_row2" class="row_heading level0 row2" rowspan="2">x</th>
      <th id="T_870de_level1_row2" class="row_heading level1 row2" >params</th>
      <td id="T_870de_row2_col0" class="data row2 col0" >0.35</td>
      <td id="T_870de_row2_col1" class="data row2 col1" >0.57**</td>
      <td id="T_870de_row2_col2" class="data row2 col2" >0.64*</td>
    </tr>
    <tr>
      <th id="T_870de_level1_row3" class="row_heading level1 row3" >tstats</th>
      <td id="T_870de_row3_col0" class="data row3 col0" >(1.29)</td>
      <td id="T_870de_row3_col1" class="data row3 col1" >(2.85)</td>
      <td id="T_870de_row3_col2" class="data row3 col2" >(2.26)</td>
    </tr>
    <tr>
      <th id="T_870de_level0_row4" class="row_heading level0 row4" rowspan="2">z</th>
      <th id="T_870de_level1_row4" class="row_heading level1 row4" >params</th>
      <td id="T_870de_row4_col0" class="data row4 col0" ></td>
      <td id="T_870de_row4_col1" class="data row4 col1" >-0.64**</td>
      <td id="T_870de_row4_col2" class="data row4 col2" >-0.77**</td>
    </tr>
    <tr>
      <th id="T_870de_level1_row5" class="row_heading level1 row5" >tstats</th>
      <td id="T_870de_row5_col0" class="data row5 col0" ></td>
      <td id="T_870de_row5_col1" class="data row5 col1" >(-3.55)</td>
      <td id="T_870de_row5_col2" class="data row5 col2" >(-2.91)</td>
    </tr>
    <tr>
      <th id="T_870de_level0_row6" class="row_heading level0 row6" >r2</th>
      <th id="T_870de_level1_row6" class="row_heading level1 row6" ></th>
      <td id="T_870de_row6_col0" class="data row6 col0" >0.193</td>
      <td id="T_870de_row6_col1" class="data row6 col1" >0.487</td>
      <td id="T_870de_row6_col2" class="data row6 col2" >0.352</td>
    </tr>
    <tr>
      <th id="T_870de_level0_row7" class="row_heading level0 row7" >nobs</th>
      <th id="T_870de_level1_row7" class="row_heading level1 row7" ></th>
      <td id="T_870de_row7_col0" class="data row7 col0" >9</td>
      <td id="T_870de_row7_col1" class="data row7 col1" >9</td>
      <td id="T_870de_row7_col2" class="data row7 col2" >9</td>
    </tr>
    <tr>
      <th id="T_870de_level0_row8" class="row_heading level0 row8" >Fixed effects</th>
      <th id="T_870de_level1_row8" class="row_heading level1 row8" ></th>
      <td id="T_870de_row8_col0" class="data row8 col0" >No</td>
      <td id="T_870de_row8_col1" class="data row8 col1" >No</td>
      <td id="T_870de_row8_col2" class="data row8 col2" >Entity</td>
    </tr>
  </tbody>
</table>
