# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 14:40:04 2022

@author: FALAH FAKHRI
"""

# import required packages and libraries.

from pathlib import Path
from glob import glob
import rasterio
import os
import numpy as np
from numpy import *
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt
from rasterio.plot import show 
import skimage.exposure
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep


class LandSatEightNine:
    """Read and retrieve raster bands, and their information"""
    
    def __init__(self, dirpath:int, band_number:int):
        
        for path in Path(dirpath).rglob('*_B'+str(band_number)+'.TIF'):
            band_name = os.path.splitext(path.name)[0]
            
            with rasterio.open(path) as src:
                self.band_name = band_name
                self.band = src.read((1))
                self.band_transform = src.transform
                self.band_crs = src.crs
                self.band_shape = src.shape
                self.band_profile = src.profile
                self.raster_img = np.rollaxis(self.band, 0, 1)
                self.dtype = src.dtypes
                
      
    def plotband(self, cmap='terrain'):
        """plot the original selected band individually"""
        
        band_array = self.band.astype('f4')
        band_array[band_array == 0] = np.nan
        fig, ax = plt.subplots(1, figsize=(12, 10))
        show(band_array, ax=ax, cmap=cmap)
        ax.set_title(
            'Original Band: '
            + self.band_name) 
            
        

class normalizer(LandSatEightNine):
    
    """normalize: normalize a numpy array, all values are between 0 and 1"""
    
    def __init__(self, dirpath:int, band_number:int):
        
        
        super().__init__(dirpath, band_number)
        
       
        array_min, array_max = self.raster_img.min(), self.raster_img.max() 
        Normalizedband = ((self.raster_img - array_min) / (array_max - array_min))
        self.Normalizedband = Normalizedband
        
        print('Minimum Value in Normalized band\n',self.Normalizedband.min())
        print('Maximum Value in Normalized band\n',self.Normalizedband.max())
        
        
    def plotnormalized(self):
        """plot the normalized band"""
        
        self.Normalizedband.astype('f4')
        
        self.Normalizedband[self.Normalizedband == 0] = np.nan
        
        fig, ax = plt.subplots(1, figsize=(12, 10))
        show(self.Normalizedband, ax=ax, cmap='terrain')
        ax.set_title(
            'Normalizedband '
            + self.band_name) 
             
        
      
def color_composite(b1, b2, b3, compositenme:str, cmap= 'summer'):
    """
    Visualize RBG composite image
    
    parameter
    ---------
    band1: any band as an input first band
    band2: any band as an input second band
    band3: any band as an input third band
        
    Natural Color 4 3 2
    False Color (urban) 7 6 4
    Color Infrared (vegetation)	5 4 3
    Agriculture 	6 5 2
    Healthy Vegetation 5 6 2
    Land/Water 	5 6 4
    Natural With Atmospheric Removal 7 5 3
    Shortwave Infrared 7 5 4
    Vegetation Analysis 6 5 4
    
    Band combinations are selected for a number of reasons and it is helpful to understand
    the spectral reflectance profiles of features you are interested in studying. 
    For example in the NIR false color composite shown above 
    healthy vegetation appears bright red as they reflect more near infrared than green. 
    Another common combination uses the shortwave infrared (shown as red), 
    the near infrared (green), and the green visible band (shown as blue). 
    In this false color composite vegetation appear bright green, 
    bare ground appears reddish and snow appears bright blue.
    Though there are many possible combinations of wavelength bands, 
    the table to the left is a list of some that are commonly used. 
    Bathymetric
    The bathymetric band combination 4 3 1
    uses the red (4), green (3) and coastal band to peak into water. 
    
    http://gsp.humboldt.edu/olm/Courses/GSP_216/lessons/composites.html
        
    """
    
    
    compos = np.dstack((b1, b2, b3))
    
    fig, ax = plt.subplots(1, figsize=(12, 10))
    ax.set_title('Three_Bands_composite: {}'.format(compositenme),
                 fontsize = 14,
                 fontweight ="bold")
       
    plt.imshow(compos, cmap = cmap)
    
def equalized_color_composite(b1, b2, b3, Equacompositenme:str, cmap='summer'):
    """
    adjust the brightness histogram of each single band
    
    parameter
    ---------
    band1: any band as an input first band
    band2: any band as an input second band
    band3: any band as an input third band
    Equacompositenme:str title of the composite bands
    """
    
    
    equ_b1 = skimage.exposure.equalize_hist(b1)
    equ_b2 = skimage.exposure.equalize_hist(b2)
    equ_b3 = skimage.exposure.equalize_hist(b3)
    
    equ_b1[equ_b1 == 0] = np.nan
    equ_b2[equ_b2 == 0] = np.nan
    equ_b2[equ_b2 == 0] = np.nan
    
    equ_compos = np.dstack((equ_b1, equ_b2, equ_b3))
    
    fig, ax = plt.subplots(1, figsize=(12, 10))
    ax.set_title('Equalized_three_Bands_composite: {}'.format(Equacompositenme),
                      fontsize = 14,
                      fontweight ="bold")
       
    plt.imshow(equ_compos, cmap=cmap)    
    


def plot_AllBAND_Hist(dirpath:str, landsat_dir:str):
    
    landsat_path = glob(os.path.join(dirpath, landsat_dir, "*B*.TIF"))
    
    landsat_path.sort()
    
    array_stack, meta_data = es.stack(landsat_path, nodata=-9999)
    
    colors_list = [
        "midnightblue",
        "Blue",
        "Green",
        "Red",
        "Maroon",
        "Purple",
        "Violet",
        "pink"
    ]
    
    
    titles = [" Coastal aerosol", 
              "Blue",
              "Green", 
              "Red",
              "NIR", 
              "SWIR 1",
              "SWIR 2", 
              "TIRS"
    ]
    
    
    ep.hist(array_stack,
            colors=colors_list, 
            title=titles,  
            bins=50, 
            cols=2
            )
    plt.show()
    
    return print(f'\n Landsat bands meta data:\n {meta_data}') 


def plot_AllBAND(dirpath:str, landsat_dir:str):
    
    landsat_path = glob(os.path.join(dirpath, landsat_dir, "*B*.TIF"))
    
    landsat_path.sort()
    
    array_stack, meta_data = es.stack(landsat_path, nodata=-9999)
    
    
    titles = [" Coastal aerosol", 
              "Blue",
              "Green", 
              "Red",
              "NIR", 
              "SWIR 1",
              "SWIR 2", 
              "TIRS"
    ]
    
    
    ep.plot_bands(array_stack, 
                  title=titles, 
                  cols=2
                  )
    plt.show()
    
    return print(f'\n Landsat bands meta data:\n {meta_data}')   

            
def NDVI(nir,red):
    """Calculates The normalized difference vegetation index (NDVI) 
    is a standardized index allowing you to generate an image displaying greenness,
    also known as relative biomass. 
    This index takes advantage of the contrast of characteristics between two bands 
    from a multispectral raster dataset—the chlorophyll pigment absorption in the red band
    and the high reflectivity of plant material in the near-infrared (NIR) band. 
        
    The value of this index ranges from -1 to 1.
    Reference: 
    Rondeaux, G., M. Steven, and F. Baret.
    Optimization of Soil-Adjusted Vegetation Indices.
    Remote Sensing of Environment 55 (1996): 95-107.
    parameters
    ----------
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    red: Band 4 - Red 	0.64-0.67, as an input.
    """
    nir = nir.astype('float')
    red = red.astype('float')
   
    NDVI = np.where(
           (nir+red)==0.,
           0,
           np.divide((nir - red) , (nir + red))) 
    
    return NDVI


def DBI(swir1, green, ndvi):
    """Calculate Dry bareness Index
    Reference:
    Rasul, A.; Balzter, H.; Ibrahim, G.R.F.; Hameed,
    H.M.; Wheeler, J.; Adamu, B.; Ibrahim, S.; Najmaddin, P.M.
    Applying Built-Up and Bare-Soil Indices from Landsat 8 to Cities in Dry Climates.
    Land 2018, 7, 81. https://doi.org/10.3390/land7030081
    
    parameters
    ----------
    swinr1: Band 6 - SWIR 1 	1.57-1.65 as an input.
    green: Band 3 - Green 	0.53-0.59 as an input
    ndvi: The normalized difference vegetation index (NDVI). 
    """
    swir1 = swir1.astype('float')
    green = green.astype('float')
    
    DBI = np.where(
           (swir1+green)==0.,
           0,
           np.divide((swir1 - green) , (swir1 + green))) 
    
    DBI = DBI - ndvi
            
    return DBI
    
def SAVI(red, nir, L=0.5):
    """Calculate Modified Soil-adjusted Vegetation Index
    The value of this index ranges from -1 to 1.
    Reference: 
    Huete, A. "A Soil-Adjusted Vegetation Index (SAVI).
    Remote Sensing of Environment 25 (1988): 295-309.
    parameters
    ----------
    red: Band 4 - Red 	0.64-0.67, as an input.
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    L  : amount of green vegetation cover
    """
    red = red.astype('float')
    nir = nir.astype('float')
    SAVI = np.where(
            (red+nir)==0.,
            0,
            np.divide((nir - red) , (nir + red + L)* (1 + L)))

    
    return SAVI

def MSAVI2(nir, red):
    
    """Calculate the Modified Soil Adjusted Vegetation Index (MSAVI2)
    Reference:
    Qi, J. et al., 1994, A modified soil vegetation adjusted index,
    Remote Sensing of Environment, Vol. 48, No. 2, 119–126.   
    parameters
    ----------
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    red: Band 4 - Red 	0.64-0.67, as an input.
    """
    nir = nir.astype('float')
    red = red.astype('float')
    
    MSAVI2 = (0.5) * (2*(nir + 1) - ((2 * nir + 1)**2 - 8*(nir - red))**0.5)
                  
   
    return MSAVI2 

  
def NDMI(nir, swinr1): 
    
    """Calculate the Normalized Difference Moisture Index (NDMI) 
        as it's sensitive to the moisture levels in vegetation.
        It is used to monitor droughts as well as monitor fuel levels in fire-prone areas.
    Reference:
    Wilson, E.H. and Sader, S.A., 2002, Detection of forest harvest
    type using multiple dates of Landsat TM imagery.
    Remote Sensing of Environment, 80 , pp. 385-396. 
    
    Skakun, R.S., Wulder, M.A. and Franklin, .S.E. (2003).
    Sensitivity of the thematic mapper enhanced 
    wetness difference index to detect mountain pine beetle red-attack damage.
    Remote Sensing of Environment, Vol. 86, Pp. 433-443.
    
    parameters
    ----------
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    swinr1: Band 6 - SWIR 1 	1.57-1.65, as an input.
    """
    nir = nir.astype('float')
    swinr1 = swinr1.astype('float')
    
    NDMI = np.where(
                  (nir+swinr1)==0.,
                  0,
                  np.divide((nir - swinr1) , (nir + swinr1))
                  )
   
    return NDMI    

    
     
def MNDWI(green, swinr):
    """Calculate Modified Normalized Difference Water Index
      Reference:
      Xu, H. 
      "Modification of Normalised Difference Water Index (NDWI) to Enhance Open Water Features 
      in Remotely Sensed Imagery.
      International Journal of Remote Sensing 27, No. 14 (2006): 3025-3033.
    
    parameters
    ----------
    green: Band 3 - Green 	0.53-0.59 as an input
    swinr: Band 6 - SWIR 1 	1.57-1.65 as an input
    """
    green = green.astype('float')
    swinr = swinr.astype('float')
      

    MNDWI = np.where(
           (green+swinr)==0.,
           0,
           np.divide((green - swinr) , (green + swinr))) 

    return MNDWI



def BAI(red, nir):
    """Calculate The Burn Area Index (BAI) to identify the areas
      of the terrain affected by fire.
      Reference:
      Chuvieco, E., M. Pilar Martin, and A. Palacios. 
      Assessment of Different Spectral Indices in the Red-Near-Infrared Spectral 
      Domain for Burned Land Discrimination.
      Remote Sensing of Environment 112 (2002): 2381-2396.
    
    parameters
    ----------
    red: Band 4 - Red 	0.64-0.67, as an input.
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    """
    red = red.astype('float')
    nir = nir.astype('float')
      
    BAI = np.where(
           (red+nir)==0.,
           0,
           np.divide(1 , ((0.1 -red)**2 + (0.06 - nir)**2))) 
    
    return BAI


def NBRI(nir, swinr):
    """Calculate The Normalized Burn Ration Index (NBRI)  emphasize burned areas,
      while mitigating illumination and atmospheric effects.
      Reference:
      Key, C. and N. Benson, N. 
      Landscape Assessment: Remote Sensing of Severity, 
      the Normalized Burn Ratio; and Ground Measure of Severity,
      the Composite Burn Index." FIREMON: Fire Effects Monitoring and Inventory System,
      RMRS-GTR, Ogden, UT: USDA Forest Service, Rocky Mountain Research Station (2005). 
    
    parameters
    ----------
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    swinr: Band 6 - SWIR 1 	1.57-1.65 as an input
    """
    nir = nir.astype('float')
    swinr = swinr.astype('float')
      
    NBRI = np.where(
           (nir+swinr)==0.,
           0,
           np.divide((nir - swinr) , (nir + swinr))) 
    
    return NBRI

def NDBI(swinr, nir, ndvi):
    """Calculate Normalized Difference Built-up Index
    Reference:
    Zha, Y., J. Gao, and S. Ni.
    Use of Normalized Difference Built-Up Index in Automatically 
    Mapping Urban Areas from TM Imagery.
    International Journal of Remote Sensing 24, no. 3 (2003): 583-594.
    parameter
    ---------
    swinr: Band 6 - SWIR 1 	1.57-1.65 as an input
    nir: Band 5 - Near Infrared (NIR) 	0.85-0.88 as an input.
    ndvi: The normalized difference vegetation index (NDVI).
    """
    
    swinr = swinr.astype('float')
    nir = nir.astype('float')
    
    NDBI =  np.where(
           (swinr+nir)==0.,
           0,
           np.divide((swinr - nir) , (swinr + nir))) 
    
    NDBI =  NDBI - ndvi
    
    return NDBI


def plot_plot(bandpath:str, fname:str, cmap='summer'):
    """plot any an individual array band or/and index
    parameters
    ----------
    bandpath: string as input
    cmap: colormap, 'RdYlGn' as an input default.
          for more detailes please visit, 
    https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html#miscellaneous
    fname: product title as an input str.
    
    """
    
    with rasterio.open(bandpath) as src:
        
        band = src.read(1)
        
        band[band == 0] = np.nan
        
        fig, ax = plt.subplots(1, figsize=(12, 10))
        
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False, style='plain') 
        ax.set_title(' Product Title : {}'.format(fname),
                     fontsize = 14,
                     fontweight ="bold")
           
        plt.imshow(band, cmap = cmap, alpha=1) 
        
      
def write_raster(raster, crs, transform, output_file):
    """Save any an individaul array band or/and index
        parameters
        ----------
        raster: an array of band or/and index.
        crs: The coordinate Reference system of any known array band.
        transform: The transform of any known array band.
        output_file: The directory path and the file name with its extension '.tif'.
    """
    profile = {
        'driver': 'GTiff',
        'compress': 'lzw',
        'width': raster.shape[0],
        'height': raster.shape[1],
        'crs': crs,
        'transform': transform,
        'dtype': raster.dtype,
        'count': 1,
        'tiled': False,
        'interleave': 'band',
        'nodata': 0
    }

    profile.update(
        dtype=raster.dtype,
        height=raster.shape[0],
        width=raster.shape[1],
        nodata=0,
        compress='lzw')

    with rasterio.open(output_file, 'w', **profile) as out:
        out.write_band(1, raster) 
        
     
    
def main():
    
    pass
 
if __name__ == '__main__':
    
    main()   


