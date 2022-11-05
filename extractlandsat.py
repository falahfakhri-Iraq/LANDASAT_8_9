# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:25:47 2022

@author: FALAH FAKHRI
"""

# import required packages and libraries.  

import tarfile
import os


def extract_landsat(dirpath:str):
    
    """
    extract landsat 8/9 tar images, and save them in a new concise name folders. 
    
    parameter
    ---------
    dirpath: str path to the directory which contains the images.
    
    dirpath should be ended up with forward slash '/' in order to complete the 
    
    extraction process in the new folders. 
    
    """
  
    for filename in os.listdir(dirpath):
            
        if filename.endswith('.tar'):
            
            name = os.path.splitext(filename)[0]
            
            os.makedirs(dirpath +name, exist_ok=True) 
            
            file = tarfile.open(os.path.join(dirpath,filename))
        
            for dir in os.listdir(dirpath):
                
                if dir == name:
                    
                    # print(os.path.join(dir, filename))
                   
                    file.extractall(os.path.join(dirpath+dir))
                    
                    print('\nextracted is done in the new folder', os.path.join(dir, filename))
                    
def main():
    
    pass
 
if __name__ == '__main__':
    
    main()   
              














