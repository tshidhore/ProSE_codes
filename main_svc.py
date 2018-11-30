# Author: Tanmay C. Shidhore

# Linear SVC code
# Note: Relative paths wont work unless working directory is code directory

import os
import sys
import numpy as np 
#import scipy as sp 
from pdb import set_trace as keyboard
import input_reader
import output_reader
from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification

#**********************************************************************#
#                            READING INPUTS                            #
#**********************************************************************#

# File prefixes
prefix = ['ch','cs','cv','nch','ncs','ncv']
ncprefix = ['nch','ncs','ncv'] # Prefixes for files with no crack
ti_folder = './t_input_files/'

# Lists for storing input parameters
# Prefix1 and prefix2 shortened as p1,p2
# Each element in the list is a list where the function output is dumped

# Indices for e, d, gc
index = np.arange(1,4)

# Define the input and output array for linear SVC
# No. of rows corrrespond to no. of data sets (kept variable)
# No. of columns is the important parameters (hard coded)
#input_arr = np.zeros([len(prefix)*(index.size**3),5])
input_arr = []
output_arr = []

# Threshold values 
cdot_thresh = 0.0001
psidot_thresh = 0.002

# Counter for rows of the input array (for filling the parameters)
count=0
for pref in prefix:
    for i in index:
        for j in index:
            for k in index:
                filename = ti_folder + pref + "e" + str(i) + "d" + str(j) + "gc" + str(k) + ".i"
                print("Reading file:"+filename)
                mp,cw,cv,cf,bc,bc_funs = input_reader.read_input_file(filename)
                  
                # Output is numbers
                gc,E,nu,rho = input_reader.extract_mat_properties(mp)
                
                n_cracks,crack_c,crack_hw,crack_angle_deg = input_reader.extract_crack_params(cf,cv,cw)

                left,right,top,bottom = input_reader.BC_extract(bc,bc_funs)
                
#**********************************************************************#
#                       INPUTS TO INTEGERS                            #
#**********************************************************************#  
# Author: Akshay Biniwale
# The numeric values of the material properties are converted
# to integers for simplicity.
                if 'v' in pref:
                    load = 1    # vertical load
                elif 'h' in pref:
                    load = 2    # horizontal load
                elif 's' in pref:
                    load = 0    # shear load
#                if gc == 0.001:
#                    gc_t = 0
#                elif gc == 0.2:
#                    gc_t = 1
#                else:
#                    gc_t = 2
#                if E == 0.0005:
#                    E_t = 0
#                elif E == 0.05:
#                    E_t = 1
#                else:
#                    E_t = 2
#                if rho == 0.8:
#                    rho_t = 0
#                elif rho == 1.4:
#                    rho_t = 1
#                else:
#                    rho_t = 2
                arr_in = [gc,E,rho,n_cracks,load]
                input_arr.append(arr_in)
                           
#**********************************************************************#
#                          READING OUTPUTS                             #
#**********************************************************************#

# File prefixes
to_folder = './t_output_files/'

# Lists for storing input parameters
# Each element in the list is a list where the function output is dumped
#c = []  # time rate of change
#t = []
#psiposmax = [] # time rate of change. both are > 0

for pref in prefix:
    for i in index:
        for j in index:
            for k in index:
                filename = to_folder + pref + "e" + str(i) + "d" + str(j) + "gc" + str(k) + "_out.csv"
                print("Reading file:"+filename)
                c,t,psiposmax,cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max = output_reader.read_output_file(filename)

#**********************************************************************#
#                       OUTPUTS TO INTEGERS                            #
#**********************************************************************#  
# Author: Akshay Biniwale
                if pref in ncprefix:
                    # Conditions for nucleation
                    if cdot_max > cdot_thresh and psidot_max > psidot_thresh:
                        out = 1 # No crack - crack nucleates
                    else:
                        out = 0 # No crack - crack does not nucleate
                else:
                    # Conditions for propogation
                    if cdot_max > cdot_thresh and psidot_max > psidot_thresh:
                        if sigmayy_max > 0 and sigmayy_max > sigmaxx_max:
                            out = 2   # Crack propogates by Mode 1
                        else:
                            out = 3   # Crack propogates by Mode 2
                    else:
                        out = 4    # Crack present but does not propogate 
                
                output_arr.append(out)
                
#**********************************************************************#
#                         SAMPLE SVC BLOCK                             #
#**********************************************************************#

X = np.array(input_arr)
Y = np.array(output_arr)
clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(X, Y)

test_set = [[0.2,0.05,0.8,1,1],[0.001,5,0.8,0,2]]

pred = clf.predict(test_set)
for i in range(len(pred)):
    if pred[i] == 0:
        print('Crack does not nucleate')
    elif pred[i] == 1:
        print('Crack Nucleates')
    elif pred[i] == 2:
        print('Crack propogates by mode 1')
    elif pred[i] == 3:
        print('Crack propogates by Mode 2')
    else:
        print('Crack does not propogate')
        
                