#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:58:48 2018

Threshold Method

@author: fury
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
print('**********THRESHOLD METHOD**********')

def experiment(threshold, y1, y2):
    global profit, op
    hold = False
    for i in range(len(ds)-y1*240,len(ds)-y2*240-3):
        if not hold:
            if ds[i][0] > threshold * ds[i-1][0]:
                buy = ds[i+1][1]
                hold = True
        else:
            if ds[i][0] < threshold * ds[i-1][0]:
                sell = ds[i+1][0]
                profit += (sell / buy * 0.9985 - 1) * 1
                #profit *= sell / buy * 0.9985
                hold = False
                print(buy, sell, profit)
    return

ds = pd.read_csv('bitcoin.csv')
ds = np.array(ds)[:,(2,1)].tolist()
profit = 1
threshold = 1.0995
y1 = 10
y2 = 0

experiment(threshold, y1, y2)