# coding: utf-8
'''
Created on 2014. 12. 15.

@author: JSJ
'''

import os
import sys
from pfp_sdk.RawHandler import *
from pfp_sdk.PFPUtil import *



def ExtractFunc(Keyword, ExtractFolder):

    CaseDBPath = sys.argv[3]
    RawHandlerClass = RawHandler()

    isSetExtender = False
    Extender = ""
    if "*." in os.path.split(Keyword)[1]:
        Extender = os.path.split(Keyword)[1].replace("*.", "")
        isSetExtender = True
        Keyword = os.path.split(Keyword)[0]

    result = []
    if CaseDBPath == "None":
        if Keyword[len(Keyword)-1] == "\\":
            Keyword = Keyword[0:len(Keyword)-1]
        result = RawHandlerClass.PathCheck(Keyword)
    else:
        if Keyword[len(Keyword)-1] == "\\":
            Keyword = Keyword[0:len(Keyword)-1]
        result = RawHandlerClass.PathCheck(Keyword, caseDBPath=CaseDBPath.decode('utf8'))
    
    
    if result[0] == "dir":        
        
        filepath = result[1][0][0]
        
        if sys.argv[5] == "True":   #Hierarchy is setted
            OutputDirName = os.path.join(ExtractFolder, os.path.split(filepath)[0].replace(":",""))
        else : 
            #print "ExtractFolder = " + ExtractFolder
            #print "Keyword = " + Keyword
            #print "os.path.split(Keyword)[1] = " + os.path.split(Keyword)[1]
            OutputDirName = os.path.join(ExtractFolder, os.path.split(Keyword)[1])
            if os.path.isdir(OutputDirName):
                #print "Dup!!"
                for idx in range(1, 10000):
                    if os.path.isdir(OutputDirName+"_"+str(idx)): continue
                    else: 
                        OutputDirName = OutputDirName+"_"+str(idx)
                        break
                    
        RawHandlerClass.MakeDirectory(OutputDirName)
        #print "OutputDirName = " + OutputDirName
        
        for inode_list in result[1]:
            if inode_list[1] == None or (os.path.split(inode_list[0])[1] == "." or os.path.split(inode_list[0])[1] == ".."):
                continue
            
            if inode_list[2] == 'dir':
                if sys.argv[4] == "True": #reculsive is setted
                    if sys.argv[5] == "True":  ExtractFunc(inode_list[0], ExtractFolder)
                    else :  ExtractFunc(inode_list[0], OutputDirName)
                    continue
                else:
                    continue
            

            if isSetExtender == True and (Extender not in os.path.split(inode_list[0])[1]):
                continue
            
            OutputFile = OutputDirName + "\\" + os.path.split(inode_list[0])[1].replace(":","_")
            RawHandlerClass.RawCopy_by_Tsk(inode_list[1], inode_list[0], OutputFile)
            #print "OutputDirName + \"\\\" + os.path.split(inode_list[0])[1] = " + OutputDirName + "\\" + os.path.split(inode_list[0])[1]
            
            #Time stamp regeneration
            hFile = win32file.CreateFile(OutputFile, win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ, None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_BACKUP_SEMANTICS,None)
            try:
                #SetFiletime(hfile, ctime, atime, mtime)
                win32file.SetFileTime(hFile, int(inode_list[6]), int(inode_list[4]), int(inode_list[3]))
            finally:
                win32api.CloseHandle(hFile)



    elif result[0] == "file":
        
        
        filepath = result[1][0]
        #print "result = " + str(result)
        if sys.argv[5] == "True":   #Hierarchy is setted
            OutputDirName = os.path.join(ExtractFolder, os.path.split(filepath)[0].replace(":",""))
            RawHandlerClass.MakeDirectory(OutputDirName)
            OutputFile = OutputDirName + "\\" + os.path.split(filepath)[1].replace(":","_")
        else : 
            OutputDirName = ExtractFolder
            OutputFile = OutputDirName + "\\" + os.path.split(filepath)[1].replace(":","_")
            if os.path.isfile(OutputFile):
                for idx in range(1, 10000):
                    if os.path.isdir(OutputFile+"_"+str(idx)): continue
                    else: 
                        OutputFile = OutputFile+"_"+str(idx)
                        break
        
        RawHandlerClass.RawCopy_by_Tsk(result[1][1], result[1][0], OutputFile)
        
        OutputFile = os.path.join(os.path.split(OutputFile)[0],os.path.split(OutputFile)[1].replace(":", "_"))
        hFile = win32file.CreateFile(OutputFile, win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ, None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_BACKUP_SEMANTICS,None)
        try:
            #SetFiletime(hfile, ctime, atime, mtime)
            win32file.SetFileTime(hFile, int(result[1][6]), int(result[1][4]), int(result[1][3]))
        finally:
            win32api.CloseHandle(hFile)
        
        
    else:

        Dummy = 0
        #print "File or Folder is not exist."
        
    
    
    return
    
    
    
    
    
def main():
    
    Keyword = sys.argv[1].strip()
    ExtractFolder = sys.argv[2]

    ExtractFunc(Keyword, ExtractFolder)
    
    

if __name__ == '__main__':
    main()
    