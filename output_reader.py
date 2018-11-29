# Author: Tanmay C. Shidhore

# Header file to read the MOOSE output (<filename.csv>) file
# All outputs are returned as numpy arrays
# Note: Relative paths wont work unless working directory is code directory

# Author: Akshay Dandekar
# Stresses output
# Functions stress_state, stress_rotation and derivative defined

import os
import sys
import numpy as np 
from numpy import diff
import scipy as sp 
from pdb import set_trace as keyboard
import pandas as pd

# Switch for the test block
test_flag = True

def stress_state(stressxxmax,stressxxmin,stressxymax,stressxymin,stressyymax,stressyymin):
    stressxx = np.zeros(stressxxmax.shape)
    stressxy = np.zeros(stressxymax.shape)
    stressyy = np.zeros(stressyymax.shape)
    for i in range(len(stressxx)):
        if abs(stressxxmin[i])>stressxxmax[i]:
            stressxx[i] = stressxxmin[i]
        else:
            stressxx[i] = stressxxmax[i]
        if abs(stressyymin[i])>stressyymax[i]:
            stressyy[i] = stressyymin[i]
        else:
            stressyy[i] = stressyymax[i]
        if abs(stressxymin[i])>stressxymax[i]:
            stressxy[i] = stressxymin[i]
        else:
            stressxy[i] = stressxymax[i]
    return stressxx,stressxy,stressyy

def stress_rotation(stressxx,stressxy,stressyy):
    theta = np.pi/6
    sigmaxx = np.zeros(stressxx.shape)
    sigmaxy = np.zeros(stressxy.shape)
    sigmayy = np.zeros(stressyy.shape)
    for i in range(len(sigmaxx)):
        sigmaxx[i] = (stressxx[i]+stressyy[i])/2 + (stressxx[i]-stressyy[i])*np.cos(2*theta)/2 + stressxy[i]*np.sin(2*theta)
        sigmayy[i] = (stressxx[i]+stressyy[i])/2 - (stressxx[i]-stressyy[i])*np.cos(2*theta)/2 - stressxy[i]*np.sin(2*theta)
    return sigmaxx,sigmayy

def derivative(y,t):
    dt = t[1]-t[0]
    dydt = diff(y)/dt
    return dydt
    
def read_output_file(filename):
    
    # Reads csv file <filename>
    # Input name should contain extension
    f = pd.read_csv(filename)
    
    # Block extracting the required outputs
    c = f.c.values
    t = f.time.values
    psiposmax = f.psiposmax.values
    
    #   Stresses added to output on 11-28-2018 by Akshay Dandekar
    stressxxmax = f.stressxxmax.values
    stressxxmin = f.stressxxmin.values
    stressxymax = f.stressxymax.values
    stressxymin = f.stressxymin.values
    stressyymax = f.stressyymax.values
    stressyymin = f.stressyymin.values
    
    stressxx,stressxy,stressyy = stress_state(stressxxmax,stressxxmin,stressxymax,stressxymin,stressyymax,stressyymin)
    sigmaxx,sigmayy = stress_rotation(stressxx,stressxy,stressyy)
    
    cdot = derivative(c,t)
    psidot = derivative(psiposmax,t)
    
    return c,t,psiposmax,cdot,psidot
  
#**********************************************************************#
#                         Test Block                                   #
#**********************************************************************#

if test_flag:
    folder = './test/'
    filename = folder + 'ncve1d1gc1_out.csv'
    c1,t1,psiposmax1,cdot1,psidot1 = read_output_file(filename)