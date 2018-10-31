import os
import sys
import numpy as np 
import scipy as sp 
from pdb import set_trace as keyboard

def read_input_file(filename):
  
  # Code to read the MOOSE input (<filename.i>) file
  # All outputs are either lists or list of lists
  
  f = open(filename, 'r')
  
  mat_prop = []
  crack_hwidths = []
  crack_vars = []
  crack_funs = []
  i = 0
  
  reading_lines = True

  while reading_lines:
    
    # Read line by line, stripping the whitespace
    line = f.readline().strip()
    i += 1
    #**********************************************************************#
    #                      READING MATERIAL PROPERTIES                     #
    #**********************************************************************#
    
    if '[Materials]' in line:
        print("Line %d:Reading material properties"%(i))
        read_materials = True
        flag_d = False
        while read_materials:
            line = f.readline().strip()
            i += 1
            # Finding gc
            if 'gc' in line:
                mat_prop.append(line)
            # Finding Young's modulus
            elif 'youngs_modulus' in line:
                mat_prop.append(line)
            # Finding YoPoisson ratio
            elif 'poissons_ratio' in line:
                mat_prop.append(line)
            # Finding density
            elif 'prop_names = density' in line:
                flag_d = True
                continue
            elif flag_d:
                mat_prop.append("density"+ line.strip("prop"))
                flag_d = False
            # Checking end of materials block
            elif '[]' in line:
                read_materials = False
                print("Line %d:Done reading material properties"%(i))     

    #**********************************************************************#
    #                      READING CRACK FUNCTIONS                         #
    #**********************************************************************#                
                           
    if '[Functions]' in line:
        print("Line %d:Reading crack properties"%(i))
        read_function = True
        while read_function:
            line = f.readline().strip()
            i += 1
            # Checking end of functions block
            if '[]' in line:
                read_function = False
                print("Line %d:Done reading crack properties"%(i))
            # Finding half-width parameters
            # Strips the ' s at the star and end and stores it in the relevant list
            elif 'vals' in line:
                crack_hwidths = ((line.strip("vals = ")).strip("'")).split(" ")
            # Finding corresponding parameters values
            elif 'vars' in line:
                crack_vars = ((line.strip("vars = ")).strip("'")).split(" ")
            # Extracting all crack functions
            elif 'value' in line:
                temp = line.replace("value = 'min(","")
                crack_funs.append(temp.replace(",1)'",""))
                
    #**********************************************************************#
    #                      READING BOUNDARY CONDITIONS                     #
    #**********************************************************************#
    
    if '[BCs]' in line:
        BC = []
        BC_index = 0
        print("Line %d:Reading BCs"%(i))
        read_BC = True
        while read_BC:
            line = f.readline().strip()
            i += 1
            # Checking for end of BCs block
            if '[]' in line:
                read_BC = False
                print("Line %d:Done reading BCs"%(i))
            
            # Executed at the start of one BC sub-block
            elif '[./' in line:
                continue
            
            # Executed at the end of one BC sub-block. 
            # Increments index for list of BCs
            elif '[../]' in line:
                BC_index += 1
                
                # Removes extra ", " at the end of the last element in BC
                BC[-1] = BC[-1][:-2]
            
            # Executed between "[./ ........ [../]"
            else:
                # Determines if the line has to be added to the same list element of appended to the list
                # Depending on whether we are operating in the same BC sub-block or have moved on to the next block respectively
                if BC == [] or len(BC) == BC_index:
                    BC.append(line + ", ")
                else:
                    BC[BC_index] += line + ", "
                
                
    #**********************************************************************#
    #                         CHECKING END OF FILE                         #
    #**********************************************************************#
                            
    elif '[Outputs]' in line:
      reading_lines = False
      print("Line %d:End of file"%(i))

  return mat_prop,crack_hwidths,crack_vars,crack_funs,BC

#**********************************************************************#
#                     EXTRACTING NUMERICAL VALUES                      #
#                        OF MATERIAL PROPERTIES                        #
#**********************************************************************#
    
def extract_mat_properties(mat_prop):
    for string in mat_prop:
        if 'gc' in string:
            gc = 0.
            for t in string.split():
                try:
                    gc = float(t)
                except ValueError:
                    pass
                    
        elif 'youngs_modulus' in string:
            E = 0.
            for t in string.split():
                try:
                    E = float(t)
                except ValueError:
                    pass
                    
        elif 'poissons_ratio' in string:
            nu = 0.
            for t in string.split():
                try:
                    nu = float(t)
                except ValueError:
                    pass
        
        elif 'density_values' in string:
            rho = 0.
            for t in string.split():
                try:
                    rho = float(t)
                except ValueError:
                    pass
                    
    return gc,E,nu,rho
    
#**********************************************************************#
#                     EXTRACTING NUMERICAL VALUES                      #
#                         OF CRACK PARAMETERS                          #
#**********************************************************************#
    
def extract_crack_params(cf,cv,cw):
    
    # lists for crack angle, crack half-width
    # and damage fraction at crack centre
    
    crack_angle_deg = []
    crack_hw = []
    crack_c = []
    
    # Separate each individual crack function
    # Demarcated based on the ) for the previous function and + after that
    # assuming that such a ')+' combination wont occur anywhere except at the
    # end of a crack equation
    
    CFs = cf[0].replace(")+",") ")
    CFs = CFs.split(" ")
    
    # Number of separate equations = no. of cracks
    n_cracks = len(CFs)
    
    for crack in CFs:
        
        # Demarcate the c_centre value from the exp
        crack = crack.replace("*exp"," exp")
        # Demarcate the 'if' parts
        crack = crack.replace("*if"," if")
        
        # Extract c at centre, crack half width and crack angle
        f = crack_c_extract(crack)
        g = crack_hw_extract(crack,cv,cw)
        h = crack_angle_extract(crack)
        
        # Append it to the appropriate lists
        crack_c.append(f)
        crack_hw.append(g)
        crack_angle_deg.append(h)
    
    return n_cracks,crack_c,crack_hw,crack_angle_deg

def BC_extract(bc):
    left = []
    right = []
    top = []
    bottom = []
    
    # Iterate over each extracted sub-block
    for BC_kind in bc:
        
        # Split various attributes using '.'
        BC_kind = BC_kind.split(", ")
        
        # Identify the splice which contains the "boundary" keyword
        for i,x in enumerate(BC_kind):
            if "boundary" in x:
                index = i        
        # Store the relevant information in BC_kind in the corresponding list
        # 2nd argument to extract_BC_info() ensures that everythong in BC_kind except "boundary = ..." is passed     
        if "left" in BC_kind[index] or "0" in BC_kind[index]:
            extract_BC_info(left,[p for j,p in enumerate(BC_kind) if j != index])
        elif "bottom" in BC_kind[index] or "1" in BC_kind[index]:
            extract_BC_info(bottom,[p for j,p in enumerate(BC_kind) if j != index])
        elif "right" in BC_kind[index] or "2" in BC_kind[index]:
            extract_BC_info(right,[p for j,p in enumerate(BC_kind) if j != index])
        elif "top" in BC_kind[index] or "3" in BC_kind[index]:
            extract_BC_info(top,[p for j,p in enumerate(BC_kind) if j != index])
    
    # Append "Free" if no BCs found for a particular side        
    if left == []:
        left.append("Free")
    elif right == []:
        right.append("Free")
    elif top == []:
        top.append("Free")
    elif bottom == []:
        bottom.append("Free")

    return left,right,top,bottom

# Function to append the information in BC_kind to the list for a specific side
def extract_BC_info(side,u):
    
    for x in u:
        side.append(x)

# Function to extract the c value at crack centre    
def crack_c_extract(i):
    # Equations of cracks with c_value of 1 assumed to
    # start with the 'exp' string directly
    if i[0] == 'e':
        return 1.00
    # If value is not 1, then the numerical value is the first
    # element after splitting tyhe string based on " "
    else:
        t = i.split(" ")
        return float(t[0])

# Function to extract the crack half-width         
def crack_hw_extract(i,cv,cw):
    
    # Determines which splice of the crack equation
    # (after its split based on spaces) contains the half
    # -width parameter.
    
    # Cracks with c_value of 1 have the exp(..) as the 0th eelement
    if i[0] == 'e':
        index = 0
    
    # Cracks with a c_value other than 1 have the exp(..) as the 1st element
    else:
        index = 1
        
    # Split the equation based on spaces
    t = i.split(" ")
    
    # Seacrh the specific parameter used for the particular crack
    # from the half-width parameters extracted previously
    
    for j,x in enumerate(cv):
        if x == t[index][-2]:
            
            # return the numerical value (stored in cw) corresponding to the half-width parameter found
            return cw[j]

def crack_angle_extract(i):
    
    if i[0] == 'e':
        index = 0
    else:
        index = 1
    
    t = i.split(" ")
    if 'abs(y-tan' in t[index]:
        y = ((t[index].replace("abs(y-tan("," ")).replace("*pi"," pi")).split(" ")
        return float(y[1])
                
    elif 'abs(x' in t[index]:
        return 90.00
    else:
        return 0.00
        
        
           
mp,cw,cv,cf,bc = read_input_file("samplefile.i")  

# Output is numbers
gc,E,nu,rho = extract_mat_properties(mp)

n_cracks,crack_c,crack_hw,crack_angle_deg = extract_crack_params(cf,cv,cw)

left,right,top,bottom = BC_extract(bc)