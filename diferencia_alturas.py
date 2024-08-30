#############################################################################
#
#    DIFERENCIA_ALTURAS: This function take part on SMOOTH_DEM function and its  
#    aim is studying how each height is raised to get new DEM's 
#
#    Copyright (C) 2022  Daniel Pardo (UV), Spain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

## LOAD NEEDED LIBRARIES
import numpy as np
import os,glob
import rasterio as rio

###################################################################################################
#    max_min = max_min(dates, shape, nodata)   dates --> Dates to analyze 
#                                              shape --> Shape of the matrix
#                                              nodata --> Location of items without information
###################################################################################################

### FUNCTION DESCRIPTION ###
# (i) Generate variable to book some memory with numpy.zero ('dif_alturas'), this variable save 8 different matrix (0)
# (ii) For each neighbord calculate their difference between him and each item (1)
# (iii) Introduce each difference in the new variable ('dif_alturas') (2)
# (iv) Delete nodata items and calculate maximum and minimum by numpy.max and numpy.min (3)
# (v) Finally, calculate second maximum and second minimum to get more accurate DEM's (4)

### APPLY SCRIPT ###

def max_min(data,shape, nodata):
    dif_alturas = np.zeros([8, shape[0], shape[1]]) # (0)
    
    for i in range(shape[0]):  #(1)                                   #(-1,+1)
        for j in range(shape[1]):
            if j == (shape[1]-1) or i == 0:
                dif_alturas[0][i][j] = nodata
            elif data[i][j] == nodata or data[i-1][j+1] == nodata:
                dif_alturas[0][i][j] = nodata
            else: 
                dif_alturas[0][i][j] = data[i][j] - data[i-1][j+1] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(0,+1)
            for j in range(shape[1]):
                if j == (shape[1]-1):
                    dif_alturas[1][i][j] = nodata
                elif data[i][j] == nodata or data[i][j+1] == nodata:
                    dif_alturas[1][i][j] = nodata
                else: 
                    dif_alturas[1][i][j] = data[i][j] - data[i][j+1] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(+1,+1)
        for j in range(shape[1]):
            if i == (shape[0]-1) or j == (shape[1]-1):
                dif_alturas[2][i][j] = nodata
            elif data[i][j] == nodata or data[i+1][j+1] == nodata:
                dif_alturas[2][i][j] = nodata
            else: 
                dif_alturas[2][i][j] = data[i][j] - data[i+1][j+1] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(-1,0)
            for j in range(shape[1]):
                if i == 0:
                    dif_alturas[3][i][j] = nodata
                elif data[i][j] == nodata or data[i-1][j] == nodata:
                    dif_alturas[3][i][j] = nodata
                else: 
                    dif_alturas[3][i][j] = data[i][j] - data[i-1][j] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(+1,0)
        for j in range(shape[1]):
            if i == (shape[0]-1):
                dif_alturas[4][i][j] = nodata
            elif data[i][j] == nodata or data[i+1][j] == nodata:
                dif_alturas[4][i][j] = nodata
            else: 
                dif_alturas[4][i][j] = data[i][j] - data[i+1][j] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(-1,-1)
        for j in range(shape[1]):
            if i == 0 or j == 0:
                dif_alturas[5][i][j] = nodata
            elif data[i][j] == nodata or data[i-1][j-1] == nodata:
                dif_alturas[5][i][j] = nodata
            else: 
                dif_alturas[5][i][j] = data[i][j] - data[i-1][j-1] #(2)
                
    for i in range(shape[0]):  #(1)                                   #(0,-1)
        for j in range(shape[1]):
            if j == 0:
                dif_alturas[6][i][j] = nodata
            elif data[i][j] == nodata or data[i][j-1] == nodata:
                dif_alturas[6][i][j] = nodata
            else: 
                dif_alturas[6][i][j] = data[i][j] - data[i][j-1] #(2)
                
    for i in range(shape[0]):  #(1)                                  #(+1,-1)
        for j in range(shape[1]):
            if i == (shape[0]-1) or j == 0:
                dif_alturas[7][i][j] = nodata
            elif data[i][j] == nodata or data[i+1][j-1] == nodata:
                dif_alturas[7][i][j] = nodata
            else: 
                dif_alturas[7][i][j] = data[i][j] - data[i+1][j-1] #(2)
    
    # BOOK MEMORY WITH NEW VARIABLES 
    primer_max = np.zeros([shape[0], shape[1]]) 
    segundo_max = np.zeros([shape[0], shape[1]])
    primer_min = np.zeros([shape[0], shape[1]])
    segundo_min = np.zeros([shape[0], shape[1]])
        
    for i in range(shape[0]):   
        for j in range(shape[1]):
            elementos = [] # Empty variable
            for t in range(8):
                elementos.insert(t, dif_alturas[t][i][j])   
            for n in elementos[:]:
                if n == nodata:   
                    elementos.remove(nodata)
                
            if elementos == []:  #(3)
                # Introduce nodata items
                primer_max[i][j] =  primer_min[i][j] = nodata
            
            else:  #(3)
                # Introduce data items
                primer_max[i][j] = np.max(elementos)
                primer_min[i][j] = np.min(elementos)
                
    for i in range(shape[0]):  #(4)
        for j in range(shape[1]):
            elemento = [] # Empty variable
            for t in range(8):
                elemento.insert(t, dif_alturas[t][i][j])   
            for n in elemento[:]:
                if n == nodata:     # Delete nodata items
                    elemento.remove(nodata)
            for n in elemento[:]:
                if n == primer_max[i][j]:   # Delete first maximum
                    elemento.remove(primer_max[i][j])
                        
            if (np.shape(elemento)[0] < 3): 
                segundo_max[i][j] = primer_max[i][j]
            else:
                segundo_max[i][j] = np.max(elemento)
                    
    for i in range(shape[0]):  #(4)
        for j in range(shape[1]):
            elemento = [] # Empty variable
            for t in range(8):
                elemento.insert(t, dif_alturas[t][i][j])    
            for n in elemento[:]:
                if n == nodata:     # Delete nodata items
                    elemento.remove(nodata)
            for n in elemento[:]:
                if n == primer_min[i][j]:   # Delete first minimum
                    elemento.remove(primer_min[i][j])
                    
            if (np.shape(elemento)[0] < 3): 
                segundo_min[i][j] = primer_min[i][j]
            else:
                segundo_min[i][j] = np.min(elemento)
                
    ## MOVE NEW DEM's TO PRINCIPAL FUNCTION                    
    return(primer_max, segundo_max, primer_min, segundo_min)
                    