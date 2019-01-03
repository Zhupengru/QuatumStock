#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 20:36:05 2018

MACD Method

@author: fury
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print('**********MA METHOD**********')

def experiment(filename, p, delay, y1, y2):
    ds = pd.read_csv(filename)
    #ori = np.array(ds)
    ds = np.array(ds)[:,(2,-1)].tolist()   
    
    for i in range(p):
        ds[i][1] = 0
    temp = 0
    for i in range(p):
        temp += ds[i][0]
    ds[p-1][1] = temp/p
    for i in range(p, len(ds)):
        temp += ds[i][0] - ds[i-p][0]
        ds[i][1] = temp/p
    
    profit = 1
    day = 0
    hold = False
    for i in range(len(ds)-int(y1*240), len(ds)-delay-int(y2*240)):
        if not hold:
            if ds[i][1] > ds[i-1][1]:
                buy = ds[i+delay][0]
                #bdate = ori[i][0]
                hold = True
        else:
            day += 1
            if ds[i][1] < ds[i-1][1] or ds[i][0] < 0.8 * buy:
                sell = ds[i+delay][0]
                #profit += (sell / buy * 0.9985 - 1) * 1
                profit *= sell / buy * 0.9985
                #sdate = ori[i][0]
                hold = False
                #print(bdate, sdate , buy, sell, profit)
    #print('op days:',(len(ds)-delay)/op)
    #print(filename.split('.')[0]+' in p:', p, 'profit:',profit)
    if hold:
        sell = ds[-1][0]
        #profit += (sell / buy * 0.9985 - 1) * 1
        profit *= sell / buy * 0.9985
    
    if day != 0:
        rate = (profit - 1) * 240 / day * 100
    else:
        rate = 0
    
    return [filename, p, profit, rate]

def pick_high_p(filename, p2p):
    p = 2
    profit = p2p[0][2] + p2p[1][2] +p2p[2][2] + p2p[3][2] + p2p[4][2]
    m_profit = p2p[0][2] + p2p[1][2] +p2p[2][2] + p2p[3][2] + p2p[4][2]
    for i in range(p, len(p2p)-2):
        m_profit = m_profit - p2p[i-3][2] + p2p[i+2][2]
        if m_profit > profit:
            profit = m_profit
            p = p2p[i][1]
    print(filename.split('.')[0], p, p2p[p-3][2])
    return p

def pick_high_r(filename, p2p):
    p = 2
    rate = p2p[0][3] + p2p[1][3] +p2p[2][3] + p2p[3][3] + p2p[4][3]
    m_rate = p2p[0][3] + p2p[1][3] +p2p[2][3] + p2p[3][3] + p2p[4][3]
    for i in range(p, len(p2p)-2):
        m_rate = m_rate - p2p[i-3][3] + p2p[i+2][3]
        if m_rate > rate:
            rate = m_rate
            p = p2p[i][1]
    print(filename.split('.')[0], p, p2p[p-3][2])
    return p

def god_tell_me(filename, delay, y1, y2, y3):
    p2p=[]
    p = 0
    r = 0
    for i in range(3,150):
        p2p.append(experiment(filename, i, delay, y1, y2))
    p = pick_high_p(filename, p2p)
    print(experiment(filename, p, delay, y3, 0)[2])
    r = pick_high_r(filename, p2p)
    print(experiment(filename, r, delay, y3, 0)[3])
    ds = pd.read_csv(filename)
    #ori = np.array(ds)
    ds = np.array(ds)[:,(2,-1)].tolist()
    if ds[len(ds)-1][0] > ds[len(ds)-1-p][0]:
        print(filename.split('.')[0],'buy!')
    else:
        print(filename.split('.')[0],'sell!')
    make_plot(filename,p,y3)
    
    if ds[len(ds)-1][0] > ds[len(ds)-1-r][0]:
        print(filename.split('.')[0],'buy!')
    else:
        print(filename.split('.')[0],'sell!')
    make_plot(filename,r,y3)

def make_plot(filename,p,y):
    if p > 240*y:
        y = int(p/240) + 1
    ds = pd.read_csv(filename)
    #ori = np.array(ds)
    ds = np.array(ds)[:,(2,-1)].tolist()    
    for i in range(p):
        ds[i][1] = 0
    temp = 0
    for i in range(p):
        temp += ds[i][0]
    ds[p-1][1] = temp/p
    for i in range(p, len(ds)):
        temp += ds[i][0] - ds[i-p][0]
        ds[i][1] = temp/p
    x = [i for i in range(int(y*240))]
    close = np.array(ds)[len(ds)-int(y*240):,0].reshape(-1)
    ma = np.array(ds)[len(ds)-int(y*240):,1].reshape(-1)
    plt.figure()
    plt.plot(x, ma, label = str(p), linewidth = 0.6)
    plt.plot(x, close, linewidth = 0.6, color='grey', label = filename)
    plt.plot(y*240-p-1, ds[len(ds)-p-1][0], marker = '*', color = 'red')
    plt.legend()
    plt.show()
    return
    
delay = 0
y1 = 5
y2 = 0
y3 = 5



god_tell_me('002017.csv', delay, y1, y2, y3)






#need regression test
