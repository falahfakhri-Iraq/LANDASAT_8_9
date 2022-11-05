# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:21:10 2022

@author: FALAH FAKHRI
"""

# import required packages and libraries. 
    
from pathlib import Path
import functools
import operator
import pandas as pd
pd.set_option('display.max_rows', 30)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 220)
import os

data = []

def rename_landsat(dirpath:str):
        
    """
    rename landsat 8/9 images and save them in concise folder name. 
    
    parameter
    ---------
    dirpath: str path to the directory which contains the images.
    
    dirpath should be ended up with forward slash '/' to avoid,
    
    FileNotFoundError: [WinError 2].
    
    LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX

Where:

    L = Landsat
    X = Sensor (“C”=OLI/TIRS combined, “O”=OLI-only, “T”=TIRS-only, “E”=ETM+, “T”=“TM, “M”=MSS)
    SS = Satellite (”07”=Landsat 7, “08”=Landsat 8)
    LLL = Processing correction level (L1TP/L1GT/L1GS)
    PPP = WRS path
    RRR = WRS row
    YYYYMMDD = Acquisition year, month, day
    yyyymmdd - Processing year, month, day
    CC = Collection number (01, 02, …)
    TX = Collection category (“RT”=Real-Time, “T1”=Tier 1, “T2”=Tier 2)
    
    references
    
    https://www.usgs.gov/faqs/what-naming-convention-landsat-collections-level-1-scenes
    
    https://www.usgs.gov/faqs/what-naming-convention-landsat-collection-2-level-1-and-level-2-scenes
    
    """
    for path in Path(dirpath).glob('*.tar'): ### rglob
        print('image_path_name:\n',path, '\n', 'image_name\n',path.name)
        
        s = path.name
        LXSS = s.split("_")[0]
        LLLL = s.split("_")[1]
        Acquisition_year = s.split("_")[3]
        Processing_year = s.split("_")[4]
        
        name = LXSS,'_'+'_',LLLL+'_', Acquisition_year
        
        str = functools.reduce(operator.add, (name))
        
        os.rename(dirpath+s, dirpath+str+'.tar')
        
        
    for item in os.listdir(dirpath):
        
        if item.endswith('.tar'):
            
            name_1 = LXSS, LLLL, Acquisition_year, Processing_year
            
            data.append(name_1)        
            
            df = pd.DataFrame(data, columns=['LXSS',
                                             'LLLL',
                                             'Acquisition_year',
                                             'Processing_year'])
            
            
    print('\nBrief information table of landsat images\n', df)       
      
        
                
    os.makedirs(dirpath +'Landsat_dataframes', exist_ok=True)  
        
    df.to_csv(dirpath+'Landsat_dataframes/landsat9.csv', encoding='utf-8')
    
    
def main():
    
   pass
 
if __name__ == '__main__':
    
    main()     



