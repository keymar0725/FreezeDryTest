#!/usr/bin/env python3
import csv
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import os.path
import datetime
from matplotlib import rcParams

### Init ###
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Meiryo"]
out_dir = "out/"
os.makedirs(out_dir, exist_ok=True)

#######
# Argument
import_file = sys.argv[1]       # csv file
plt_pitch = int(sys.argv[2])    # plot pitch
temp_lim1 = int(sys.argv[3])    # temp minimum
temp_lim2 = int(sys.argv[4])    # temp maximum
pa_lim1 = int(sys.argv[5])      # vaccum minimum
pa_lim2 = int(sys.argv[6])      # vaccum maximum

if plt_pitch!=1 and plt_pitch%60!=0:
    sys.exit("Error!:Plot Pitch")

dictionary = {3600:"1hour",
              1800:"30min",
              60:"1min",
              1:"1sec",
              }

plt_name = dictionary[plt_pitch]

# Input for Zip
pitches = [3600, 1800, 60, 1]
x_names = ["[h]", "[0.5h]", "[m]", "[s]"]

# Debug
print("Input File: {0}".format(os.path.basename(import_file)))
print("Plot Picth: {0}".format(plt_pitch))
print("Plot Name: {0}".format(plt_name))

# csv_file_name
out_name = os.path.basename(import_file).rstrip('.csv')
print("Output Name: {0}".format(out_name))

######

col_name = range(1,10,1)
df = pd.read_csv(import_file,
                  names = col_name,
                  encoding="shift-jis",
                  delimiter=",",
                  dtype="object")

###filter DataFrame
header_num = int(df.iloc[0,1])
_df = df[header_num:]
_df = _df.drop([1,2], axis=1)
_df = _df.dropna(how='all', axis=1)
_df = _df.dropna(how='any')
for i in range(3,6):
    _df = _df[_df[i]!="BURNOUT"]

_df = _df[1:].astype(float)   # convert float

for i in range(3,6):
    _df = _df[_df[i]<=100]   # 100℃以下

row, col = _df.shape
for j in range(5,7):
    for i in range(0,row):
        _df.iloc[i,j] = 10**(_df.iloc[i,j] - 3)

for i in range(8,10):
    _df = _df[_df[i]<=200]   # 200Pa以下

###


# List plot points
ch1 = []
ch2 = []
ch3 = []
ch4 = []
ch5 = []
ch6 = []
ch7 = []

row, col = _df.shape
ch_temp = [ch1, ch2, ch3, ch4, ch5]
ch_names_temp = ["品温1","品温2","品温3","CT温度","乾燥窯温度"]
col_temp = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
ch_vd = [ch6, ch7]
ch_names_vd = ["乾燥窯真空度","CT真空度"]
col_vd = ['#8c564b', '#e377c2']

# Plot from ch1 to 5
for ch, j in zip(ch_temp, range(5)):
    for i in range(0, row, plt_pitch):
        a = _df.iloc[i,j]
        ch.append(a)

# Plot ch6, ch7
for ch, j in zip(ch_vd, range(5,7)):
    for i in range(0, row, plt_pitch):
        a = _df.iloc[i,j]
        ch.append(a)

# Graph Setup
fig = plt.figure(figsize=(12, 7), dpi=300)
ax1 = fig.add_subplot()
ax2 = ax1.twinx()
ax1.set_title('FD Test: {}'.format(out_name),fontsize=18)
ax1.set_xlabel('Time [min]')
ax1.set_ylabel('Temparature [℃]')
ax2.set_ylabel('Vacuum Degree [Pa]')
ax1.set_xlim([0,len(ch1)])
ax1.set_xticks(np.arange(0,len(ch1),step=240))
ax1.set_ylim([temp_lim1, temp_lim2])
ax2.set_ylim([pa_lim1, pa_lim2])
ax1.grid(which = "major", axis = "y", color = "gray", alpha = 0.5, linestyle = ":", linewidth = 0.5)


for ch, names, col in zip(ch_temp, ch_names_temp, col_temp):
    ax1.plot(ch, label = names, color = col)
    
for ch, names, col in zip(ch_vd, ch_names_vd, col_vd):
    ax2.plot(ch, label = names, color = col)

# Date Input
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y%m%d')

ax1.legend(bbox_to_anchor=(1.08, 1), loc='upper left', borderaxespad=0, fontsize=8)
ax2.legend(bbox_to_anchor=(1.08, 0.83), loc='upper left', borderaxespad=0, fontsize=8)
fig.show()
fig.savefig(out_dir + "{0}_{1}_{2}".format(out_name, plt_name,d)+".jpg",bbox_inches='tight')