'''
Created on 2013. 4. 5.

@author: Zurum
'''

#from . import *
from pfp_sdk.PFPUtil import *
from pfp_sdk.SampleClass import *
from pfp_sdk.SamplePackage.SamplePackageClass import *  

class SampleCLIModule(object):
    '''
    classdocs
    '''

    
    ##The methods are defined as follow
    ###################################        
        
    def SampleFunc(self): # 
        
        SamplsSDKClass = SampleClass()
        SamplsSDKPackageClass = SamplePackageClass()
        
        Result = SamplsSDKClass.SampleAddFunc(2, 3)
        PackageResult = SamplsSDKPackageClass.SampleAddFunc(2, 3)
        
        print Result
        print PackageResult
        
        return
        
        
def main():
    
    ModuleClass = SampleCLIModule()
    
    ModuleClass.SampleFunc()
    
    return

if __name__ == '__main__':
    main() 