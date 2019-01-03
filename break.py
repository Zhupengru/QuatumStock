#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:53:22 2018

Price Break Method

@author: fury
"""
import pandas as pd
import numpy as np

print('**********PRICE BREAK METHOD**********')

def break_experiment(up, down, delay, y1, y2):
    global mup, mdown, mprofit, mrate
    days = 1
    hold = False;
    profit = 1;
    rate = 0;
    for i in range (len(ds)-int(y1*240), len(ds)-int(y2*240)):
        ubreak = True;
        dbreak = True;
        for j in range(1, up+1):
            if ds[i] < ds[i-j]:
                ubreak = False;
                break;
        for j in range(1, down+1):
            if ds[i] > ds[i-j]:
                dbreak = False
        if not hold:
            if ubreak:
                buy = ds[i]
                hold = True
        else:
            days += 1
            if dbreak:
                sell = ds[i]
                hold  = False
                #profit += (sell / buy * 0.9985 - 1) * 1
                profit *= sell / buy * 0.9985
                hold = False
    if hold:
        sell = ds[-1]
        #profit += (sell / buy * 0.9985 - 1) * 1
        profit *= sell / buy * 0.9985
    if profit > mprofit:
        #print(up, down, profit)
        mup = up
        mdown = down
        mprofit = profit   
    if days == 0:
        days = 1
    rate = (profit - 1) * 24000 / days
    if rate > mrate:
        print(up, down, str(int(rate))+'%')
        mup = up
        mdown = down  
        mrate = rate
    return

def god_tell_me(up, down):
    ubreak = True
    dbreak = True
    for j in range(1, up+1):
        if ds[-1] < ds[-1-j]:
            ubreak = False
            break;
    for j in range(1, down+1):
        if ds[-1] > ds[-1-j]:
            dbreak = False
            break;
    if ubreak:
        print('buy!')
    elif dbreak:
        print('sell!')
    else:
        print('be easy!')
    return

ds = pd.read_csv('600775.csv')
ds = np.array(ds)[:,2].tolist()
delay = 0
y1 = 5
y2 = 0
y3 = 5
mup = 1
mdown = 1
mprofit = 1
mrate = 0

for up in range(10,501,4):
    for down in range(5,251,2):
        break_experiment(up,down,delay,y1,y2)

print (mup, mdown, mprofit)
god_tell_me(mup, mdown)
