#############################################################################
#
#    SMOOTH_DEM: Numerical method to get an smooth DEM and different 
#    useful DEMs with maximum and minimum items around their environment
#    by .TIFF files
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
import math 
import rasterio as rio

#############################################################################
## CHARGE DEM (Digital Elevation Model): ##
#############################################################################

# SEARCHING PATH (only .TIFF format):
path= r''
os.chdir(path)
files = glob.glob('.tif')

# CHARGE DATES OF DEM
for file in files:
    d1 = rio.open(file)
    metao= d1.meta         # Metadata
    data = d1.read(1)      # Data variable
    
# SCRIPT CONFIGURATION
shape = data.shape # Data shape
pos = np.where(data > 0) # Items position with dates
tam = np.shape(pos) # Number of items with dates

# METADATA FORMAT:
metao['dtype'] = 'float32'

# SMOOTH MATRIX CALCULATION
from matriz_media import media # Call matriz_media function
media = media(data, shape, metao['nodata'])
with rio.open('imagen_media.tif', 'w', **metao) as fo:
    fo.write(media.astype('float32'),1) # Save new DEM 

#############################################################################
## DEM's WITH MAXIMUM AND MINIMUM ITEMS ##
#############################################################################

# CALL diferencia_alturas FUNCTION
from diferencia_alturas import max_min 

## (I) FIRSTLY FOR ORIGINAL DEM
max_min_data = max_min(data, shape, metao['nodata'])

# CHARGE DATES, GET MAXIMUM AND MINIMUM AND SAVE NEW DEM's IN .TIFF FILES 

## FIRST MAXIMUM ##
primer_max_data = max_min_data[0] 
with rio.open('primer_maximo_data.tif','w', **metao) as fo:
    fo.write(primer_max_data.astype('float32'),1) # Save new DEM
    
## SECOND MAXIMUM ##
segundo_max_data = max_min_data[1] 
with rio.open('segundo_maximo_data.tif','w', **metao) as fo:
    fo.write(segundo_max_data.astype('float32'),1) # Save new DEM

## FIST MINIMUM ##
primer_min_data = max_min_data[2] 
with rio.open('primer_minimo_data.tif','w', **metao) as fo:
    fo.write(primer_min_data.astype('float32'),1) # Save new DEM
    
## SECOND MINIMUM ##
segundo_min_data = max_min_data[3] 
with rio.open('segundo_minimo_data.tif','w', **metao) as fo:
    fo.write(segundo_min_data.astype('float32'),1) # Save new DEM


## (II) NOW APPLIED TO SMOOTHED DEM
max_min_media = max_min(media, shape, metao['nodata'])

# CHARGE DATES, GET MAXIMUM AND MINIMUM AND SAVE NEW DEM's IN .TIFF FILES 

## FIRST MAXIMUM ##
primer_max_media = max_min_media[0] 
with rio.open('primer_maximo_media.tif','w', **metao) as fo:
    fo.write(primer_max_media.astype('float32'),1) # Save new DEM

## SECOND MAXIMUM ##
segundo_max_media = max_min_media[1] 
with rio.open('segundo_maximo_media.tif','w', **metao) as fo:
    fo.write(segundo_max_media.astype('float32'),1) # Save new DEM

## FIST MINIMUM ##
primer_min_media = max_min_media[2] 
with rio.open('primer_minimo_media.tif','w', **metao) as fo:
    fo.write(primer_min_media.astype('float32'),1) # Save new DEM
 
## SECOND MINIMUM ##
segundo_min_media = max_min_media[3] 
with rio.open('segundo_minimo_media.tif','w', **metao) as fo:
    fo.write(segundo_min_media.astype('float32'),1) # Save new DEM