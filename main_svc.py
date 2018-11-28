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

# Define the input 2D array for linear SVC
# No. of rows corrrespond to no. of data sets (kept variable)
# No. of columns is the important parameters (hard coded)
input_arr = np.zeros([len(prefix)*(index.size**3),20])

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
#                          READING OUTPUTS                             #
#**********************************************************************#

# File prefixes
to_folder = './t_output_files/'

# Lists for storing input parameters
# Each element in the list is a list where the function output is dumped
c = []
t = []
psiposmax = []

for pref in prefix:
    for i in index:
        for j in index:
            for k in index:
                filename = to_folder + pref + "e" + str(i) + "d" + str(j) + "gc" + str(k) + "_out.csv"
                print("Reading file:"+filename)
                df,time,psiposmax_val = output_reader.read_output_file(filename)


#**********************************************************************#
#                         SAMPLE SVC BLOCK                             #
#**********************************************************************#

X = np.array([[5.1,3.5,1.4,0.2],[4.9,3,1.4,0.2],[4.7,3.2,1.3,0.2],[4.6,3.1,1.5,0.2],[5,3.6,1.4,0.2],[5.4,3.9,1.7,0.4],[4.6,3.4,1.4,0.3]])
Y = np.array([1,0,1,0,1,1,1])
clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(X, Y)
#print(clf.coef_)
print(clf.predict([[5.1,2,0,0.7]]))
                
                c.append(df)
                t.append(time)
                psiposmax.append(psiposmax_val)
