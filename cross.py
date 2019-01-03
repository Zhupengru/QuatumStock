#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 10:28:23 2018

Golden-Cross Method

@author: fury
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print('**********CROSS METHOD**********')

def cross_experiment(short, med, delay, y1, y2):
    #short = 20
    #med  =60
    global mp, mshort, mmed
    
    for i in range(med):
        ds[i][1] = 0
        ds[i][2] = 0
        
    temp = 0
    for i in range(short):
        temp += ds[i][0]
    ds[short-1][1] = temp/short
    for i in range(short, len(ds)):
        temp += ds[i][0] - ds[i-short][0]
        ds[i][1] = temp/short
        
    temp = 0
    for i in range(med):
        temp += ds[i][0]
    ds[med-1][2] = temp/med
    for i in range(med, len(ds)):
        temp += ds[i][0] - ds[i-med][0]
        ds[i][2] = temp/med
        
    profit = 1
    op = 1
    hold = False
    for i in range(len(ds)-int(240*y1), len(ds)-delay-int(240*y2)):
        if not hold:
            if ds[i][1] > ds[i][2]:
                buy = ds[i+delay][0]
                #bdate = ori[i][0]
                hold = True
        else:
            if ds[i][1] < ds[i][2] or ds[i][0] < 0.8 * buy:
                sell = ds[i+delay][0]
                #profit += (sell / buy * 0.9985 - 1) * 1
                profit *= sell / buy * 0.9985
                #sdate = ori[i][0]
                op+=1
                hold = False
                #print(bdate, sdate , buy, sell, profit)
    #print('op days:',(len(ds)-delay)/op)
    #print(filename.split('.')[0]+' in p:', p, 'profit:',profit)
    if hold:
        sell = ds[-1][0]
        #profit += (sell / buy * 0.9985 - 1) * 1
        profit *= sell / buy * 0.9985
    
    if profit > mp:
        mp = profit
        mshort = short
        mmed = med
        print (short, med, profit)
    return profit, short, med

def make_plot(short, med, y3):
    if med > 240*y3:
        y3 = int(med/240) + 1
    for i in range(med):
        ds[i][1] = 0
        ds[i][2] = 0
        
    temp = 0
    for i in range(short):
        temp += ds[i][0]
    ds[short-1][1] = temp/short
    for i in range(short, len(ds)):
        temp += ds[i][0] - ds[i-short][0]
        ds[i][1] = temp/short
        
    temp = 0
    for i in range(med):
        temp += ds[i][0]
    ds[med-1][2] = temp/med
    for i in range(med, len(ds)):
        temp += ds[i][0] - ds[i-med][0]
        ds[i][2] = temp/med
    
    x = [i for i in range(int(y3*240))]
    close = np.array(ds)[len(ds)-int(y3*240):,0].reshape(-1)
    s =     np.array(ds)[len(ds)-int(y3*240):,1].reshape(-1)
    m =     np.array(ds)[len(ds)-int(y3*240):,2].reshape(-1)
    plt.figure()
    plt.plot(x, close, color = 'grey', linewidth = 0.6)
    plt.plot(x, m, label = 'm = '+str(med), linewidth = 0.6)
    plt.plot(x, s, label = 's = '+str(short), linewidth = 0.6)
    plt.legend()
    plt.show()
  

ds = pd.read_csv('bitcoin.csv')
#ori = np.array(ds)
ds = np.array(ds)[:,(2,-1,1)].tolist()
mp = 1
mshort = 1
mmed = 2

delay = 0
y1 = 8
y2 = 0
y3 = 8
#short = 1 med = 46

profit = []
for short in range(1,501):
    for med in range(short+10, 1001):
        profit.append(cross_experiment(short, med, delay, y1, y2)[0])

print()
print(mp, mshort, mmed)
print(cross_experiment(mshort, mmed, delay, y3, 0)[0])
make_plot(mshort, mmed, y3)
if ds[len(ds)-1][1] > ds[len(ds)-1][2]:
    print('buy!')
else:
    print('sell!')        
