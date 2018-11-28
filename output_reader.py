# Author: Tanmay C. Shidhore

# Header file to read the MOOSE output (<filename.csv>) file
# All outputs are returned as numpy arrays
# Note: Relative paths wont work unless working directory is code directory

import os
import sys
import numpy as np 
import scipy as sp 
from pdb import set_trace as keyboard
import pandas as pd

# Switch for the test block
test_flag = False

def read_output_file(filename):
    
    # Reads csv file <filename>
    # Input name should contain extension
    f = pd.read_csv(filename)
    
    # Block extracting the required outputs
    c = f.c.values
    t = f.time.values
    psiposmax = f.psiposmax.values
    
    return c,t,psiposmax
  
#**********************************************************************#
#                         Test Block                                   #
#**********************************************************************#

if test_flag:
    folder = './test/'
    filename = folder + 'ncve1d1gc1_out.csv'
    c1,t1,psiposmax1 = read_output_file(filename)