"""This script takes role of sorting the base table of income in timechart.
Aims to visualize a graph created from the table in better readable way.

Future implementation includes scoring table which records each score of
columns validated by which one should be show on bottom of a graph."""

import collections
import numpy as np
import pandas as pd


def sort_table(df):
    """Sort the base table to clearly see the fluctuation
        of incomes by separating static and kinetic graphs"""

    cols = df.columns.tolist()
    null_count = df.isnull().sum(axis = 0).tolist()

    """Step one:
    Decend by number of NANs in cols"""
    list(zip(cols, null_count))
    mylist = list(zip(cols, null_count))
    mylist = sorted(mylist, key=lambda i: (i[1], i[0]))
    mylist, _ = zip(*mylist)

    """Alternative step until step two and/or scoring.py completes"""
    try:
        # This route is set temporary until scoring.py is built successfully.
        try:
            import camouflage
        except:
            from models import camouflage
        df = df[list(('base', 'support', 'welfare', 'over work', 'late night', 'required', 'holiday', 'transport', 'diff', 'other'))]
    except:
        # This exception is the main route
        df = df[list(mylist)]

    """Step two:
    Rearrange order by standard deviation"""
    # null_count = df.isnull().sum(axis = 0).tolist()
    # cols = df.columns.tolist()
    # pairs = list(zip(cols, null_count))

    # mydict = collections.OrderedDict(pairs)
    # keys = ['avg', 'var', 'std']
    # avgs, vars, stds, idx = [], [], [], []
    # stat_collections = collections.defaultdict(dict)

    # for key, val in mydict.items():
    #     if key == 'base' or key == '基本給':
    #         continue
    #     elif val == 0:
    #         # dataframe version
    #         col = list(df.loc[:, key])
    #         avgs.append(int(np.average(col)))
    #         vars.append(int(np.var(col)))
    #         stds.append(int(np.std(col)))
    #         idx.append(key)
    # df = pd.DataFrame({
    #     'avg': avgs,
    #     'var': vars,
    #     'std': stds}, index = idx)

    return df