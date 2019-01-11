import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import mmap
import os
import time

FILE_DIRECTORY = 'RUN#06237.txt'


plt.ion()
plt.axis([0, 1000, 0, 1])
plt.rcParams['lines.markersize']=3
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
start = 100
while True:
    df = pd.read_csv(FILE_DIRECTORY,delimiter='\t',engine='python',skiprows=start,nrows=100,header=0,
                 names=['Timestamp','Status','Rate','Thick_1','Thick_0','Frequency'])
    df.Timestamp = pd.to_datetime(df.Timestamp)
    x = (df['Timestamp']-df['Timestamp'][0]).dt.total_seconds().tolist()
    y=df.Thick_0.tolist()
    yp = np.diff(y) / np.diff(x)
    xp = (np.array(x)[:-1] + np.array(x)[1:]) / 2
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    line = slope*np.array(x)+intercept

    slopep, interceptp, r_valuep, p_valuep, std_errp = stats.linregress(xp,yp)
    linep = slopep*xp+interceptp

    ax1.plot(x, line, 'r', label='y={:.7f}x+{:.7f}'.format(slope,intercept), color='red',linewidth=2)
    ax1.scatter(x,y,c='tab:red')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('thickness (A)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2.plot(xp, linep, 'r', label='y={:.7f}x+{:.7f}'.format(slopep,interceptp), color='blue',linewidth=2)
    ax2.scatter(xp, yp,c='tab:blue')
    ax2.set_ylabel('rate  (A/s)', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylim(0,0.002)
    ax1.legend(fontsize=12,loc='upper left')
    ax2.legend(fontsize=12,loc='lower left')
    plt.draw()
    # time.sleep(0.5)
    plt.pause(1.33)
    ax1.cla()
    ax2.cla()

    start +=10
