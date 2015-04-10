# -*- coding: utf-8 -*-
"""
Turnstile data, rainy/clear comparison

Created on Thu Mar  5 16:44:34 2015

@author: Tom Enterline
"""

import numpy as np
import pandas
import datetime
import statsmodels.api as sm
from ggplot import *


def turnstile_rain():
    print ("Starting")
    dpath = '/home/tom/Desktop/turnstile_data_master_with_weather.csv'
    df = pandas.read_csv(dpath)
    df2 = df.loc[:, ['UNIT', 'DATEn', 'Hour', 'ENTRIESn_hourly',
                     'rain', 'meantempi', 'precipi']]
    grouped = df2.groupby(['UNIT', 'DATEn', 'Hour'])
    df = grouped.agg({'ENTRIESn_hourly': np.sum, 'rain': np.min,
                      'meantempi': np.min, 'precipi': np.min}).reset_index()
    x = df[['Hour']]
    y = df['ENTRIESn_hourly']
    model = sm.OLS(y, x)
    results = model.fit()
    print results.summary()
    dfp = df.loc[:, ['ENTRIESn_hourly', 'rain']]
    dfr = dfp[dfp['rain'] == 1].reset_index()
    dfc = dfp[dfp['rain'] == 0].reset_index()
    plot = ggplot(dfr, aes(x='ENTRIESn_hourly')) +\
        geom_histogram(binwidth=100) + xlim(0, 10000) + ylim(0, 10000) +\
        labs('Riders in a time period', 'Number of occurences') +\
        ggtitle('Subway ridership on rainy days')
    print plot
    plot = ggplot(dfc, aes(x='ENTRIESn_hourly')) +\
        geom_histogram(binwidth=100) + xlim(0, 10000) + ylim(0, 10000) +\
        labs('Riders in a time period', 'Number of occurences') +\
        ggtitle('Subway ridership on dry days')
    print plot

    sdfr = pandas.Series(dfr['ENTRIESn_hourly'])
    sdfc = pandas.Series(dfc['ENTRIESn_hourly'])
    df2 = pandas.DataFrame({'rain': sdfr, 'norain': sdfc})
    dfc = pandas.melt(df2)
    plot = ggplot(dfc, aes(x='value', fill='variable')) +\
        geom_histogram(binwidth=100) + xlim(0, 10000) + ylim(0, 15000) +\
        labs('Riders in a time period', 'Number of occurences') +\
        ggtitle('Subway ridership: cyan = rainy days, orange = dry days')
    print plot


turnstile_rain()
