# Author: Tanmay C. Shidhore

# Header file to read the MOOSE input (<filename.i>) file
# All outputs are either lists or list of lists

import os
import sys
import numpy as np 
#import scipy as sp 
from pdb import set_trace as keyboard
import input_reader

#**********************************************************************#
#                            READING INPUTS                            #
#**********************************************************************#

# File prefixes
prefix1 = ['che','cse','cve']
prefix2 = ['nche','ncse','ncve']

# Lists for storing input parameters
# Prefix1 and prefix2 shortened as p1,p2
# Each element in the list is a list where the function output is dumped
p1_mp = []
p1_cracks = []
p1_BC = []

p2_mp = []
p2_cracks = []
p2_BC = []
 

# Indices for e, d, gc
index = np.arange(1,4)

for pref in prefix1:
    for i in index:
        for j in index:
            for k in index:
                filename = pref + str(i) + "d" + str(j) + "gc" + str(k) + ".i"
                print("Reading file:"+filename)
                mp,cw,cv,cf,bc,bc_funs = input_reader.read_input_file(filename)
                  
                # Output is numbers
                p1_mp.append([input_reader.extract_mat_properties(mp)])

                p1_cracks.append([input_reader.extract_crack_params(cf,cv,cw)])

                p1_BC.append([input_reader.BC_extract(bc,bc_funs)]) 
            
for pref in prefix2:
    for i in index:
        for j in index:
            for k in index:
                filename = pref + str(i) + "d" + str(j) + "gc" + str(k) + ".i"
                print("Reading file:"+filename)
                mp,cw,cv,cf,bc,bc_funs = input_reader.read_input_file(filename)
                  
                # Output is numbers
                p2_mp.append([input_reader.extract_mat_properties(mp)])

                p2_cracks.append([input_reader.extract_crack_params(cf,cv,cw)])

                p2_BC.append([input_reader.BC_extract(bc,bc_funs)])
