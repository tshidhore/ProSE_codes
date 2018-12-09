# Author: Tanmay C. Shidhore

# Linear SVC code
# Note: Relative paths wont work unless working directory is code directory
from os import listdir
import sys
import numpy as np 
#import scipy as sp 
from pdb import set_trace as keyboard
import input_reader
import output_reader
from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification

test_flag = False

def scale(prop_max,prop_min,prop):
    x = (prop - prop_min)/(prop_max - prop_min)
    return x
    
# Function to generate the required input, output lists needed for the SVC model
# The filenames containing the search words are excluded from the training set
# Setting labels true scales the data            
def generate_io_arr(files_i,files_o,labels,search_word="None"):
    
    # Define the input and output arrays for linear SVC
    input_arr = []
    output_arr = []
    
    # List to include files for reading as a part of the validation set 
    ifile_not_read = []
    ofile_not_read = []
    
    # Threshold values for output decision 
    cdot_thresh = 0.0001
    psidot_thresh = 0.002
    
    # Looping over each input filename
    for index,filename_i in enumerate(files_i):
        
        # Find the corresponding output file
        filename_o = files_o[index]
               
        # Excludes files containing prop+value
        # Adds it to a list for reading as a part of the validation set 
        if search_word in filename_i:
            ifile_not_read.append(filename_i)
            ofile_not_read.append(filename_o)
            print("Not reading Reading:"+filename_i)
            continue
        else:                    
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
            # to vectors with equal weights.
            
            crack_p = [1, 0]
            if n_cracks == 0:
                crack_p = [0, 1]
            
            # Default is shear load
            load = [1, 0, 0]
            
            for t in top:
                if 'uy' in t:
                    load = [0, 1, 0]    # vertical load
            for l in left:       
                if 'ux' in l:
                    load = [0, 0, 1]    # horizontal load
            if labels == False:
                arr_in = [gc,E,rho,crack_p[0],crack_p[1],load[0],load[1],load[2]]
            else:
                gc_t = scale(0.001,0.4,gc)
                E_t = scale(0.0005,5,E)
                rho_t = scale(0.8,2.0,rho)
                arr_in = [gc_t,E_t,rho_t,crack_p[0],crack_p[1],load[0],load[1],load[2]]
                
            input_arr.append(arr_in)
            
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
                    out = 4    # Crack present but does not propagate 
            
            output_arr.append(out)
            
    if search_word != "None":
        return (input_arr,output_arr,ifile_not_read,ofile_not_read)
    else:
        return (input_arr,output_arr)        
    
# Function to check the sensitivity of the SVC model to various material parameters
# 'prop' and 'val' correspond to the material property and its value
# The files containing 'prop' and 'val' will be excluded from the training set
def Test_SVC(ti_folder,to_folder,search_word,labels=False):
    #**********************************************************************#
    #                  READING INPUTS AND OUTPUTS                          #
    #**********************************************************************#
    files_i = [ti_folder + f for f in listdir(ti_folder)]
    files_o = [(f.replace(".i","_out.csv")).replace(ti_folder,to_folder) for f in files_i]
    
    input_arr,output_arr,ifile_not_read,ofile_not_read = generate_io_arr(files_i,files_o,labels,search_word)
    
    # Fitting the training data                                
    X = np.array(input_arr)
    Y = np.array(output_arr)
    clf = LinearSVC(random_state=0, tol=1e-5)
    clf.fit(X,Y)

    # Author: Tanmay C. Shidhore
    # Counter to keep track of accurate predictions
    count_acc = 0
    
    # Lists to store inputs, output and output fit for validation data
    input_arr_val = []
    output_arr_val = []
    output_arr_fit = []
    
    input_arr_val,output_arr_val = generate_io_arr(ifile_not_read,ofile_not_read,labels)
       
    # Predicts the output for validation data
    print("Predicting output data")
    output_arr_fit = clf.predict(input_arr_val)  
    # Checks if the fit and benchmark outcome match and increments the counter
    print("Comparing predicted and benchmark values")
    for i,out_predict in enumerate(output_arr_fit):
        if out_predict == output_arr_val[i]:
            count_acc += 1
            
    # Percentage accuracy of the predictions
    p_accuracy = count_acc*100/len(ifile_not_read)
    print ("The accuracy of the SVC model excluding the cases for " + search_word + " is %f" %(p_accuracy))
    return p_accuracy

def Sample_SVC(ti_folder,to_folder,vi_folder,vo_folder,labels=False):
    
    search_word = "None"
    labels=False
    #**********************************************************************#
    #              READING TRAINING INPUTS AND OUTPUTS                     #
    #**********************************************************************#
    t_files_i = [ti_folder + f for f in listdir(ti_folder)]
    t_files_o = [(f.replace(".i","_out.csv")).replace(ti_folder,to_folder) for f in t_files_i]
    
    #**********************************************************************#
    #              READING VALIDATION INPUTS AND OUTPUTS                   #
    #**********************************************************************#
    v_files_i = [vi_folder + f for f in listdir(vi_folder)]
    v_files_o = [(f.replace(".i","_out.csv")).replace(vi_folder,vo_folder) for f in v_files_i]
    
    input_arr,output_arr = generate_io_arr(t_files_i,t_files_o,labels,search_word)
    
    # Fitting the training data                                
    X = np.array(input_arr)
    Y = np.array(output_arr)
    clf = LinearSVC(random_state=0, tol=1e-5)
    clf.fit(X,Y)

    # Author: Tanmay C. Shidhore
    # Counter to keep track of accurate predictions
    count_acc = 0
    
    # Lists to store inputs, output and output fit for validation data
    input_arr_val = []
    output_arr_val = []
    output_arr_fit = []
    
    input_arr_val,output_arr_val = generate_io_arr(v_files_i,v_files_o,labels)
       
    # Predicts the output for validation data
    print("Predicting output data")
    output_arr_fit = clf.predict(input_arr_val)  
    # Checks if the fit and benchmark outcome match and increments the counter
    print("Comparing predicted and benchmark values")
    for i,out_predict in enumerate(output_arr_fit):
        if out_predict == output_arr_val[i]:
            count_acc += 1
            
    # Percentage accuracy of the predictions
    p_accuracy = count_acc*100/len(v_files_i)
    print ("The accuracy of the SVC prediction is %f" %(p_accuracy))
    return p_accuracy                                             
                                                                                          
                                                                                                                                                                                    
# Test for sensitivity to extrapolated values
ti_folder = "./t_input_files/"
to_folder = "./t_output_files/"
vi_folder = "./v_input_files/"
vo_folder = "./v_output_files/"
                                                    
p1 = Test_SVC(ti_folder,to_folder,"e1")
p2 = Test_SVC(ti_folder,to_folder,"gc1")
p3 = Test_SVC(ti_folder,to_folder,"d1")
p4 = Test_SVC(ti_folder,to_folder,"e3")
p5 = Test_SVC(ti_folder,to_folder,"gc3")
p6 = Test_SVC(ti_folder,to_folder,"d3")

# Test for missing interpolated values
p7 = Test_SVC(ti_folder,to_folder,"e2")
p8 = Test_SVC(ti_folder,to_folder,"gc2")
p9 = Test_SVC(ti_folder,to_folder,"d2")

# Raw material properties linearly scaled down to 0,1
p1l = Test_SVC(ti_folder,to_folder,"e1",True)
p2l = Test_SVC(ti_folder,to_folder,"gc1",True)
p3l = Test_SVC(ti_folder,to_folder,"d1",True)
p4l = Test_SVC(ti_folder,to_folder,"e3",True)
p5l = Test_SVC(ti_folder,to_folder,"gc3",True)
p6l = Test_SVC(ti_folder,to_folder,"d3",True)

# Test for missing interpolated values
p7l = Test_SVC(ti_folder,to_folder,"e2",True)
p8l = Test_SVC(ti_folder,to_folder,"gc2",True)
p9l = Test_SVC(ti_folder,to_folder,"d2",True)

# Validation data
P = Sample_SVC(ti_folder,to_folder,vi_folder,vo_folder)
Pl = Sample_SVC(ti_folder,to_folder,vi_folder,vo_folder,True)

print(p1,p1l,p2,p2l,p3,p3l,p4,p4l,p5,p5l,p6,p6l,p7,p7l,p8,p8l,p9,p9l,P,Pl) 