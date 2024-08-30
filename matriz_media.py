#############################################################################
#
#    MATRIZ_MEDIA: This function take part on SMOOTH_DEM function and its  
#    aim is getting the mean items from the values of its neighbors, taking
#    into account edges of files
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
#   media = media(dates, shape, nodata)   dates --> Dates from the matrix
#                                         shape --> Shape of the matrix 
#                                         nodata --> Location of items without information
####################################################################################################

### FUNCTION DESCRIPTION ###
# (i) Generate variable to book some memory with numpy.zero (0)
# (ii) Filter nodata items and incorporate their location in new matrix as zero items (1)
# (iii) Apply conditions to boundary items and calculate mean item from their boundary neighbors (2)
# (iv) Study center items from the matrix  and calculate their mean item from their neighbors (3)
# (v) Finally, any item which is not considere is a nodata item (4)

### APPLY SCRIPT ###

def media(data, shape, nodata):
    media = np.zeros((shape))        # (0)
    for i in range(shape[0]):       
        for j in range(shape[1]):
            if data[i][j] == nodata:
                media[i][j] = nodata    # (1)
            elif data[i][j] > nodata:
                if i == 0 and j == 0:   # (2)
                    elementos = [data[i][j], data[i][j+1], data[i+1][j+1], data[i+1][j]]
                    for t in elementos[:]:
                        if t == nodata:                 # Delete nodata items
                            elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                elif i == 0 and j == (shape[1]-1):  # (2)
                    elementos = [data[i][j], data[i+1][j], data[i][j-1], data[i+1][j-1]]
                    for t in elementos[:]:
                        if t == nodata:                 # Delete nodata items
                            elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                elif i == (shape[0]-1) and j == 0:   #(2)
                    elementos = [data[i][j], data[i-1][j+1], data[i][j+1], data[i-1][j]]
                    for t in elementos[:]:
                        if t == nodata:                 # Delete nodata items
                            elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                elif i == (shape[0]-1) and j == (shape[1]-1):    #(2)
                    elementos = [data[i][j], data[i-1][j], data[i-1][j-1], data[i][j-1]]
                    for t in elementos[:]:
                        if t == nodata:                 # Delete nodata items
                            elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                elif j < (shape[1]-1) and j > 0:            # (3)
                    if i < (shape[0]-1) and i > 0:
                        elementos = [data[i][j], data[i-1][j+1], data[i][j+1], data[i+1][j+1], data[i-1][j], data[i+1][j], data[i-1][j-1], data[i][j-1], data[i+1][j-1]]
                        for t in elementos[:]:
                            if t == nodata:               # Delete nodata items
                                elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                    elif i == (shape[0]-1):             # (4)
                        elementos = [data[i][j], data[i-1][j+1], data[i][j+1], data[i-1][j], data[i-1][j-1], data[i][j-1]]
                        for t in elementos[:]:
                            if t == nodata:                # Delete nodata items
                                elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                    elif i == 0:                       # (4)
                        elementos = [data[i][j], data[i][j+1], data[i+1][j+1], data[i+1][j], data[i][j-1], data[i+1][j-1]]
                        for t in elementos[:]:
                            if t == nodata:     # Delete nodata items
                                elementos.remove(nodata)
                        media[i][j] = np.mean(elementos)
                elif j == (shape[1]-1) and 0 < i < (shape[0]-1):
                    elementos = [data[i][j], data[i-1][j], data[i+1][j], data[i-1][j-1], data[i][j-1], data[i+1][j-1]]
                    for t in elementos[:]:
                        if t == nodata:         # Delete nodata items
                            elementos.remove(nodata)
                    media[i][j] = np.mean(elementos)
                elif j == 0 and 0 < i < (shape[0]-1):   # (4)
                    elementos = [data[i][j], data[i-1][j+1], data[i][j+1], data[i+1][j+1], data[i-1][j], data[i+1][j]]
                    for t in elementos[:]:
                        if t == nodata:     # Delete nodata items
                            elementos.remove(nodata)
                    media[i][j] = np.mean(elementos)
            else:   # (4)
                media[i][j] = nodata
    return(media)

