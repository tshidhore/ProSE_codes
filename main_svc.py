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
ti_folder = './t_input_files/'

# Lists for storing input parameters
# Prefix1 and prefix2 shortened as p1,p2
# Each element in the list is a list where the function output is dumped

# Indices for e, d, gc
index = np.arange(1,4)
temp = []

# Define the input 2D array for linear SVC
# No. of rows corrrespond to no. of data sets (kept variable)
# No. of columns is the important parameters (hard coded)
input_arr = np.zeros([len(prefix)*(index.size**3),20])
X = []
Y = []

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
                
                temp.append(n_cracks)

#**********************************************************************#
#                       INPUTS TO INTEGERS                            #
#**********************************************************************#  
# Author: Akshay Biniwale
                if gc == 0.001:
                    gc_t = 0
                elif gc == 0.2:
                    gc_t = 1
                else:
                    gc_t = 2
                if E == 0.0005:
                    E_t = 0
                elif E == 0.05:
                    E_t = 1
                else:
                    E_t = 2
                if rho == 0.8:
                    rho_t = 0
                elif rho == 1.4:
                    rho_t = 1
                else:
                    rho_t = 2
                if crack_angle_deg == 0:
                    crack_angle_deg_t = 0
                else:
                    crack_angle_deg_t = 1
                arr_in = [gc_t,E_t,rho_t,n_cracks,crack_angle_deg_t]
                X.append(arr_in)
                           
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
#                c,t,psiposmax,cdot,psidot,sigmaxx,sigmayy = output_reader.read_output_file(filename)
                c,t,psiposmax,cdot,psidot = output_reader.read_output_file(filename)

#**********************************************************************#
#                       OUTPUTS TO INTEGERS                            #
#**********************************************************************#  
# Author: Akshay Biniwale
                if cdot[len(cdot)-1] > 0 and psidot[len(psidot)-1] > 0:
                    prop = 1
                else:
                    prop = 2
#                if abs(sigmaxx[len(sigmaxx)-1]) > abs(sigmayy[len(sigmayy)-1]):
#                    mode = 10
#                else:
#                    mode = 20
#                arr_out = prop+mode
#                Y.append(arr_out)
                Y.append(prop)
                
#**********************************************************************#
#                         SAMPLE SVC BLOCK                             #
#**********************************************************************#

X1 = np.array(X)
Y1 = np.array(Y)
clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(X1, Y1)
#print(clf.coef_)
pred = clf.predict([[1,1,1,1,1]])
print(pred)

if str(pred[0])[0] == 1:
    print('does not propogate')
else:
    print('propogates')
#if str(pred[0])[1] == 1:
#    print('mode 1')
#else:
#    print('mode 2')
    
                