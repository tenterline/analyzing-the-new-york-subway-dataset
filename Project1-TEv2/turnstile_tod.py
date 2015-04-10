# -*- coding: utf-8 -*-
"""
Turnstile data regression, based on time of day.

Created on Sat Feb 21 21:00:49 2015

@author: Tom Enterline
"""

import numpy as np
import pandas
from ggplot import *
# import datetime
from scipy import stats


def turnstile_tod():
    print ("Starting")
    df = pandas.read_csv('/home/tom/Desktop/turnstile_grouped.csv')
    df['4hour'] = (df['Hour'] // 4) * 4
    grouped4 = df.groupby(['4hour'])
    agg4 = grouped4.agg({'ENTRIESn_hourly': np.sum}).reset_index()
    print agg4
    x = agg4['4hour']
    y = agg4['ENTRIESn_hourly']
    results = stats.linregress(x, y)
    print 'Regression r2 =', results[2]
    print 'All regression results:', results
    title = 'Total subway ridership by time-of-day, grouped in 4 hour buckets'
    plot = ggplot(agg4, aes(x='4hour', y='ENTRIESn_hourly')) + \
        geom_point() + geom_line() + \
        xlim(-1, 21) +\
        labs('Time of day when period started (0 = midnight)',
             'Total riders in 4-hour time period') +\
        ggtitle(title)
    print plot
    print "Done."

turnstile_tod()
