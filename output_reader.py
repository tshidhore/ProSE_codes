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
test_flag = False

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
    sigmayy = np.zeros(stressyy.shape)
    for i in range(len(sigmaxx)):
        sigmaxx[i] = (stressxx[i]+stressyy[i])/2 + (stressxx[i]-stressyy[i])*np.cos(2*theta)/2 + stressxy[i]*np.sin(2*theta)
        sigmayy[i] = (stressxx[i]+stressyy[i])/2 - (stressxx[i]-stressyy[i])*np.cos(2*theta)/2 - stressxy[i]*np.sin(2*theta)
    return sigmaxx,sigmayy

def derivative(y,t):
    dt = t[1]-t[0]
    dydt = diff(y)/dt
    return dydt
    
def find_max(cdot,psidot,sigmaxx,sigmayy):
    cdot_max=0
    for i,elem in enumerate(cdot[3:]):
        if abs(elem)>cdot_max:
            cdot_max = elem
            max_index = i
    psidot_max = psidot[max_index]
    sigmaxx_max = sigmaxx[max_index]
    sigmayy_max = sigmayy[max_index]
    return cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max

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
    
    # Modification by Tanmay C. Shidhore
    cdot = derivative(c,t) # Computes the derivative for values beyond the 6th time step
    psidot = derivative(psiposmax,t)
    
    cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max = find_max(cdot,psidot,sigmaxx,sigmayy)
    
    return c,t,psiposmax,cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max
  
#**********************************************************************#
#                         Test Block                                   #
#**********************************************************************#

if test_flag:
    folder = './test/'
    filename = folder + 'che3d1gc1_out.csv'
    c1,t1,psiposmax1,cdot_max1,max_index1,psidot_max1,sigmaxx_max1,sigmayy_max1 = read_output_file(filename)