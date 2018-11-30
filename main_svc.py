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


test_flag = False
#**********************************************************************#
#                  READING INPUTS AND OUTPUTS                          #
#**********************************************************************#

# File/folder prefixes
prefix = ['ch','cs','cv','nch','ncs','ncv']
ncprefix = ['nch','ncs','ncv'] # Prefixes for files with no crack
ti_folder = './t_input_files/'
to_folder = './t_output_files/'

# Lists for storing input parameters
# Each element in the list is a list where the function output is stored

# Indices for e, d, gc
index = np.arange(1,4)

# Define the input and output array for linear SVC
# No. of rows corrrespond to no. of data sets (kept variable)
# No. of columns is the important parameters (hard coded)
input_arr = []
output_arr = []

# Threshold values 
cdot_thresh = 0.0001
psidot_thresh = 0.002

for pref in prefix:
    for i in index:
        for j in index:
            for k in index:
                filename_i = ti_folder + pref + "e" + str(i) + "d" + str(j) + "gc" + str(k) + ".i"
                print("Reading:"+filename_i)
                mp,cw,cv,cf,bc,bc_funs = input_reader.read_input_file(filename_i)
                  
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
                arr_in = [gc,E,rho,n_cracks,load]
                input_arr.append(arr_in)

                filename_o = to_folder + pref + "e" + str(i) + "d" + str(j) + "gc" + str(k) + "_out.csv"
                print("Reading:"+filename_o)
                c,t,psiposmax,cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max = output_reader.read_output_file(filename_o)

                #**********************************************************************#
                #                       OUTPUTS TO INTEGERS                            #
                #**********************************************************************#  
                # Author: Akshay Biniwale
                if n_cracks == 0:
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

if test_flag:
    """
    Limits/values of input properties-
    Gc: 0.001-0.4 kJ/m^2
    E:0.0005-5 GPa
    rho: 0.8-2.0 g/cm^3
    n_crcks: 0,1
    load: 0,1,2
    
    
    Input format:[gc,E,rho,n_cracks,load]
    """
    
    
    test_set = [[0.4,1.2,1.4,1,2]]
    
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

# Author: Tanmay C. Shidhore
#**********************************************************************#
#                      SVC MODEL VALIDATION                            #
#**********************************************************************#        
v_folder = './validation_data/'
filename_prefix = 'test'

# Indicates number of files in the vaidation folder
fileno = np.arange(1,11)

# Counter to keep track of accurate predictions
count_acc = 0

# Lists to store inputs, output and output fit
input_arr = []
output_arr = []
output_arr_fit = []

for i in fileno:
    
    filename_i = v_folder + filename_prefix + str(i) + ".i"
    
    filename_o = v_folder + filename_prefix + str(i) + ".csv"
    
    print("Reading:"+filename_i)
    mp,cw,cv,cf,bc,bc_funs = input_reader.read_input_file(filename_i)
        
    # Output is numbers
    gc,E,nu,rho = input_reader.extract_mat_properties(mp)

    n_cracks,crack_c,crack_hw,crack_angle_deg = input_reader.extract_crack_params(cf,cv,cw)

    left,right,top,bottom = input_reader.BC_extract(bc,bc_funs)
    
    if 'v' in pref:
        load = 1    # vertical load
    elif 'h' in pref:
        load = 2    # horizontal load
    elif 's' in pref:
        load = 0    # shear load
    arr_in = [gc,E,rho,n_cracks,load]
    input_arr.append(arr_in)
    
    # Fitting the validation data
    print("Fitting validation data")
    out_predict = clf.predict(input_arr)
    output_arr_fit.append(out_predict)

    print("Reading:"+filename_o)
    c,t,psiposmax,cdot_max,max_index,psidot_max,sigmaxx_max,sigmayy_max = output_reader.read_output_file(filename_o)

    if n_cracks == 0:
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
    
    # Extracting data for comparison
    print("Extracting benchmark data")
    output_arr.append(out)
    
    # Checks if the fit and benchmark outcome match and increments the counter
    if out_predict == out:
        count_acc += 1

print ("The accuracy of the SVC model is %f" %(count_acc*100/fileno.size))               