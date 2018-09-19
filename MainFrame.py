# coding: utf-8
#!/usr/bin/python

#from win32com.client import Dispatch


#for internalmodule compile
#from PFPLib.InternalModules.FileFormatAnalyzer import *
from PFPLib.InternalModules.TSK_Extractor import *
from PFPLib.InternalModules.SampleCLIModule import *
from PFPLib.InternalModules.SampleGUIModule import *



#for sdk complie
from PFPLib.InternalModules.pfp_sdk.PFPUtil import *
from PFPLib.InternalModules.pfp_sdk.RawHandler import *
from PFPLib.InternalModules.pfp_sdk.SampleClass import *
from PFPLib.InternalModules.pfp_sdk.SamplePackage.SamplePackageClass import *
#from PFPLib.InternalModules.pfp_sdk.PFA_SQLite_Analyzer import *


#for pfp component complie
from PFPLib.PFPUpdater_v2 import *
from PFPLib.License_and_Update_information import *
from PFPLib.DBManageDlg import *
from PFPLib.CaseCreateDlg import *
from PFPLib.PFPListManageDlg import *
from PFPLib.PFPConfig import *
from PFPLib.CategorySetting import *
from PFPLib.CategoryAddDlg import *
from PFPLib.NewModueDlgAfterAdjustment import *
from PFPLib.ExceptionHashListDlg import *
from PFPLib.GetModuleNameDlg import *
from PFPLib.EditOnlyDlg import *
from PFPLib.TrayIcon import *
from PFPLib.PFPExtractor import *
from PFPLib.PFPExtractorAddPathDlg import *
from PFPLib.InternalModules.FileFormatAnalyzer import *




#---code for File Version Check
#---###################################
VOS_DOS             = 0x00010000L
VOS_OS216           = 0x00020000L
VOS_OS232           = 0x00030000L
VOS_NT              = 0x00040000L
VOS__BASE           = 0x00000000L
VOS__WINDOWS16      = 0x00000001L
VOS__PM16           = 0x00000002L
VOS__PM32           = 0x00000003L
VOS__WINDOWS32      = 0x00000004L
VOS_DOS_WINDOWS16   = 0x00010001L
VOS_DOS_WINDOWS32   = 0x00010004L
VOS_OS216_PM16      = 0x00020002L
VOS_OS232_PM32      = 0x00030003L
VOS_NT_WINDOWS32    = 0x00040004L


def normalizer(s):
    for j in range(len(s)):
        if len(s[j]) > 3:
            k = s[j][2:]
        else:
            k = '0' + s[j][2:]
        s[j] = k
    return s
        
def calcversioninfo(fn):
    ostypes = [VOS_DOS, VOS_NT, VOS__WINDOWS32, VOS_DOS_WINDOWS16,
               VOS_DOS_WINDOWS32, VOS_NT_WINDOWS32]
               
    verstrings = []                                        
    sigstrings = findsignatures(fn)
    if sigstrings[0] == '':
        #print 'No Version Information Available'
        return
    for i in sigstrings:
        FV = normalizer(i.split(',')[8:16])
        FOS = normalizer(i.split(',')[32:36])
        hexver = FV[3]+FV[2]+FV[1]+FV[0]+':'+FV[7]+FV[6]+FV[5]+FV[4]
        OStag = long('0x' + FOS[3]+FOS[2]+FOS[1]+FOS[0] + 'L',16)
        if OStag not in ostypes:
           continue
        if hexver not in verstrings:
           verstrings.append(hexver)                   
    myver = max(verstrings)
    return parsver(myver)

def createparsestruct(b):
    s= ''
    for i in range(len(b)):
        s += hex(ord(b[i]))+','
    return s[:-1]                                         
 
def findsignatures(file):
    f = open(file, 'rb')
    sz = f.read()
    f.close()
    res = []
    indx=sz.find('\xbd\x04\xef\xfe')
    cnt = sz.count('\xbd\x04\xef\xfe')
    while cnt > 1:
        s = createparsestruct(sz[indx:indx+52])
        sz = sz[indx+1:]
        cnt = sz.count('\xbd\x04\xef\xfe')
        indx=sz.find('\xbd\x04\xef\xfe')
        res.append(s)
    res.append(createparsestruct(sz[indx:indx+52]))
    return res

def parsver(v):
    a,b,c,d = v[:4], v[4:8], v[9:13], v[13:]
    return str(int(a,16)) + '.'+ str(int(b,16))     +'.' + str(int(c,16)) + '.' + str(int(d,16))



#---code for sume UI
penstyle = ["wx.SOLID", "wx.TRANSPARENT", "wx.DOT", "wx.LONG_DASH", "wx.DOT_DASH", "wx.USER_DASH",
           "wx.BDIAGONAL_HATCH", "wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
           "wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH"]

ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]

keyMap = {
    wx.WXK_BACK : "WXK_BACK",
    wx.WXK_TAB : "WXK_TAB",
    wx.WXK_RETURN : "WXK_RETURN",
    wx.WXK_ESCAPE : "WXK_ESCAPE",
    wx.WXK_SPACE : "WXK_SPACE",
    wx.WXK_DELETE : "WXK_DELETE",
    wx.WXK_START : "WXK_START",
    wx.WXK_LBUTTON : "WXK_LBUTTON",
    wx.WXK_RBUTTON : "WXK_RBUTTON",
    wx.WXK_CANCEL : "WXK_CANCEL",
    wx.WXK_MBUTTON : "WXK_MBUTTON",
    wx.WXK_CLEAR : "WXK_CLEAR",
    wx.WXK_SHIFT : "WXK_SHIFT",
    wx.WXK_ALT : "WXK_ALT",
    wx.WXK_CONTROL : "WXK_CONTROL",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
    wx.WXK_PRIOR : "WXK_PRIOR",
    wx.WXK_NEXT : "WXK_NEXT",
    wx.WXK_END : "WXK_END",
    wx.WXK_HOME : "WXK_HOME",
    wx.WXK_LEFT : "WXK_LEFT",
    wx.WXK_UP : "WXK_UP",
    wx.WXK_RIGHT : "WXK_RIGHT",
    wx.WXK_DOWN : "WXK_DOWN",
    wx.WXK_SELECT : "WXK_SELECT",
    wx.WXK_PRINT : "WXK_PRINT",
    wx.WXK_EXECUTE : "WXK_EXECUTE",
    wx.WXK_SNAPSHOT : "WXK_SNAPSHOT",
    wx.WXK_INSERT : "WXK_INSERT",
    wx.WXK_HELP : "WXK_HELP",
    wx.WXK_NUMPAD0 : "WXK_NUMPAD0",
    wx.WXK_NUMPAD1 : "WXK_NUMPAD1",
    wx.WXK_NUMPAD2 : "WXK_NUMPAD2",
    wx.WXK_NUMPAD3 : "WXK_NUMPAD3",
    wx.WXK_NUMPAD4 : "WXK_NUMPAD4",
    wx.WXK_NUMPAD5 : "WXK_NUMPAD5",
    wx.WXK_NUMPAD6 : "WXK_NUMPAD6",
    wx.WXK_NUMPAD7 : "WXK_NUMPAD7",
    wx.WXK_NUMPAD8 : "WXK_NUMPAD8",
    wx.WXK_NUMPAD9 : "WXK_NUMPAD9",
    wx.WXK_MULTIPLY : "WXK_MULTIPLY",
    wx.WXK_ADD : "WXK_ADD",
    wx.WXK_SEPARATOR : "WXK_SEPARATOR",
    wx.WXK_SUBTRACT : "WXK_SUBTRACT",
    wx.WXK_DECIMAL : "WXK_DECIMAL",
    wx.WXK_DIVIDE : "WXK_DIVIDE",
    wx.WXK_F1 : "WXK_F1",
    wx.WXK_F2 : "WXK_F2",
    wx.WXK_F3 : "WXK_F3",
    wx.WXK_F4 : "WXK_F4",
    wx.WXK_F5 : "WXK_F5",
    wx.WXK_F6 : "WXK_F6",
    wx.WXK_F7 : "WXK_F7",
    wx.WXK_F8 : "WXK_F8",
    wx.WXK_F9 : "WXK_F9",
    wx.WXK_F10 : "WXK_F10",
    wx.WXK_F11 : "WXK_F11",
    wx.WXK_F12 : "WXK_F12",
    wx.WXK_F13 : "WXK_F13",
    wx.WXK_F14 : "WXK_F14",
    wx.WXK_F15 : "WXK_F15",
    wx.WXK_F16 : "WXK_F16",
    wx.WXK_F17 : "WXK_F17",
    wx.WXK_F18 : "WXK_F18",
    wx.WXK_F19 : "WXK_F19",
    wx.WXK_F20 : "WXK_F20",
    wx.WXK_F21 : "WXK_F21",
    wx.WXK_F22 : "WXK_F22",
    wx.WXK_F23 : "WXK_F23",
    wx.WXK_F24 : "WXK_F24",
    wx.WXK_NUMLOCK : "WXK_NUMLOCK",
    wx.WXK_SCROLL : "WXK_SCROLL",
    wx.WXK_PAGEUP : "WXK_PAGEUP",
    wx.WXK_PAGEDOWN : "WXK_PAGEDOWN",
    wx.WXK_NUMPAD_SPACE : "WXK_NUMPAD_SPACE",
    wx.WXK_NUMPAD_TAB : "WXK_NUMPAD_TAB",
    wx.WXK_NUMPAD_ENTER : "WXK_NUMPAD_ENTER",
    wx.WXK_NUMPAD_F1 : "WXK_NUMPAD_F1",
    wx.WXK_NUMPAD_F2 : "WXK_NUMPAD_F2",
    wx.WXK_NUMPAD_F3 : "WXK_NUMPAD_F3",
    wx.WXK_NUMPAD_F4 : "WXK_NUMPAD_F4",
    wx.WXK_NUMPAD_HOME : "WXK_NUMPAD_HOME",
    wx.WXK_NUMPAD_LEFT : "WXK_NUMPAD_LEFT",
    wx.WXK_NUMPAD_UP : "WXK_NUMPAD_UP",
    wx.WXK_NUMPAD_RIGHT : "WXK_NUMPAD_RIGHT",
    wx.WXK_NUMPAD_DOWN : "WXK_NUMPAD_DOWN",
    wx.WXK_NUMPAD_PRIOR : "WXK_NUMPAD_PRIOR",
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
    wx.WXK_NUMPAD_NEXT : "WXK_NUMPAD_NEXT",
    wx.WXK_NUMPAD_PAGEDOWN : "WXK_NUMPAD_PAGEDOWN",
    wx.WXK_NUMPAD_END : "WXK_NUMPAD_END",
    wx.WXK_NUMPAD_BEGIN : "WXK_NUMPAD_BEGIN",
    wx.WXK_NUMPAD_INSERT : "WXK_NUMPAD_INSERT",
    wx.WXK_NUMPAD_DELETE : "WXK_NUMPAD_DELETE",
    wx.WXK_NUMPAD_EQUAL : "WXK_NUMPAD_EQUAL",
    wx.WXK_NUMPAD_MULTIPLY : "WXK_NUMPAD_MULTIPLY",
    wx.WXK_NUMPAD_ADD : "WXK_NUMPAD_ADD",
    wx.WXK_NUMPAD_SEPARATOR : "WXK_NUMPAD_SEPARATOR",
    wx.WXK_NUMPAD_SUBTRACT : "WXK_NUMPAD_SUBTRACT",
    wx.WXK_NUMPAD_DECIMAL : "WXK_NUMPAD_DECIMAL",
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE"
    }






#---###################################
#---PFP Main Frame Clases Start
#---###################################

class Util(object):
    
    def ModuleExecute(self, ModuleName, ModulePath, ModuleCount, DBPath, DecodedDummy, Parameter = ""):
        
        Platform = sys.platform
        SelfTest = PFPUtil()
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        #counting++
        Count = 0
                            
        if ModuleCount == '':
            Count = 1
            UpdateQuery = "update ModuleList set ExecuteCount = '" + str(Count) + "' where ModulePath = '" + ModulePath + "'"
        else:
            Count = int(ModuleCount) + 1
            UpdateQuery = "update ModuleList set ExecuteCount = '" + str(Count) + "' where ModulePath = '" + ModulePath + "'"
            
        #print UpdateQuery
        #print "[+] set execute count = " + str(Count) + ", " + ModuleName 
            
        cursor.execute(UpdateQuery)
        con.commit()
        
        SelectQuery = "select ExecutableType, UsedStatus, isInstalled, DefaultPathAfterInstall, isPortable, HomePage, OS from ModuleList where ModulePath = '" + ModulePath + "'"
        cursor.execute(SelectQuery)
        
        ResultList = cursor.fetchone()
        
        try:
            DefaultPathAfterInstall = self.DummyCyber(DecodedDummy, "", ResultList[3])
        except:
            DefaultPathAfterInstall = ResultList[3]
        
        if "y" != ResultList[1]:
            
            if "have to buy" in ResultList[1]:
            
                Printstring =  "You can use this module after purchasing of the following\n\n"
                Printstring +=  "1. Purchase and Copy(or decompress) module into your PFP\n"
                if ResultList[5] != None and ResultList[5].strip() != "":
                    Printstring += "   (Home page : " + ResultList[5] + ")\n"
                Printstring += "2. Modify path of the module\n"
                Printstring += "3. Enjoy new module via PFP\n\n"
                Printstring += "Do you want to redirect to module homepage?"
                
                dlg = wx.MessageDialog(None, Printstring, 'Info', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    os.system("start " + ResultList[5])
            
            elif "can auto download" in ResultList[1]:
                
                wx.MessageBox("Download first. please :)" + "\n" + "You can download this module Automatically.")
            
            elif "have to download directly with license agreement" in ResultList[1]: 
            
                Printstring =  "Module download require license agreement\n\n"
                Printstring +=  "You can use this module after download from module homepage directly\n\n"
                Printstring +=  "1. DownLoad and Copy(or decompress) module into your PFP\n"
                if ResultList[5] != None and ResultList[5].strip() != "":
                    Printstring += "   (Home page : " + ResultList[5] + ")\n"
                Printstring += "2. Modify path of the module\n"
                Printstring += "3. Enjoy new module via PFP\n\n"
                Printstring += "Do you want to redirect to module homepage?"
                
                dlg = wx.MessageDialog(None, Printstring, 'Info', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    os.system("start " + ResultList[5])
            
            elif "have to download directly (not compatible with auto download system)" in ResultList[1]:
                
                Printstring =  "Module download page is not compatible with our automatic download system\n\n"
                Printstring +=  "You can use this module after download from module homepage directly\n\n"
                Printstring +=  "1. Purchase and Copy(or decompress) module into your PFP\n"
                if ResultList[5] != None and ResultList[5].strip() != "":
                    Printstring += "   (Home page : " + ResultList[5] + ")\n"
                Printstring += "2. Modify path of the module\n"
                Printstring += "3. Enjoy new module via PFP\n\n"
                Printstring += "Do you want to redirect to module homepage?"
                
                dlg = wx.MessageDialog(None, Printstring, 'Info', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    os.system("start " + ResultList[5])
                
            else:
                
                wx.MessageBox("Module is empty")
                
            return 
        
        if 'win32' in Platform:
            
            interpreter_path_gui = ""
                        
            config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "r")
            
            filelines = config_fp.readlines()
            config_fp.close()
            for line in filelines:
                if "interpreter path(wingui)" in line:
                    interpreter_path_gui =  line.split(">")[1].strip("\"").strip("\n")
                
            if "gui" in ResultList[0].lower():
                
                if "py" in ResultList[6].lower():
                    if Parameter == "":
                        #print "\"" + interpreter_path + "\" " + ModulePath.encode('cp949')
                        #os.system("\"" + interpreter_path_gui + "\" " + ModulePath.encode('cp949') )
                        Popen( [interpreter_path_gui, ModulePath.encode('cp949')] )
                    else:
                        #print interpreter_path, ModulePath.encode('cp949'), Parameter.encode('cp949')
                        Popen( [interpreter_path_gui, ModulePath.encode('cp949'), Parameter.encode('cp949')] )
                        #os.system("\"" + self.interpreter_path + "\" " + ModulePath.encode('cp949') )
                
            
                elif ("n" in ResultList[4] and "n" in ResultList[2]) or "y" in ResultList[4]:     #it is ( install module and not installed ) or portable

                    if "n" in ResultList[4]:        
                    #install module which is not installed
                        #if '.msi' in ModulePath:
                        ModuleExecutePath = ModulePath.replace('/','\\')
                        #print ModulePath.encode('cp949')
                        #print ModuleExecutePath
                        try:
                            Process = Popen( [ModuleExecutePath.encode('cp949')], shell = False)
                        except:
                            try:
                                Process = Popen( [ModuleExecutePath.encode('cp949')], shell = True)
                            except:
                                os.system("start " + os.path.split(ModuleExecutePath)[0])
                        #else:
                        #    Popen( [ModulePath.encode('cp949')])
                        
                        threads = []
                        th = threading.Thread(target=self.ThreadModuleInstall, args=(Process, ModulePath, DBPath, DefaultPathAfterInstall))
                        th.start()
                        threads.append(th)
                        
                    else:                           
                    #portable module
                    
                        try:
                            if Parameter == "" and ResultList[6] != "python":
                                
                                
                                s = os.path.split(ModulePath)
                                #print s[0]
                                os.chdir(s[0].encode('cp949'))
                                
                                Process = Popen( [s[1].encode('cp949')] )
                                
                                for idx in range(ModulePath.count("/")-1):
                                    os.chdir("..")
                                
                                
                                #Popen( [ModulePath.encode('cp949')] )
                            elif ResultList[6] == "python":
                                Popen( [interpreter_path_gui.encode('cp949'), ModulePath.encode('cp949')] )
                            else:
                                
                                
                                s = os.path.split(ModulePath)
                                #print s[0]
                                os.chdir(s[0].encode('cp949'))
                                
                                Process = Popen( [s[1].encode('cp949'), Parameter.encode('cp949')] )
                                
                                for idx in range(ModulePath.count("/")-1):
                                    os.chdir("..")
                                
                                #Popen( [ModulePath.encode('cp949'), Parameter.encode('cp949')] )
                        except:
                            os.system("start " + os.path.split(ModulePath)[0])
                            
                        
                else:                               
                #install module which is installed

                    if os.path.isdir(DefaultPathAfterInstall) == True:
                        os.system("explorer \"" + DefaultPathAfterInstall + "\"") 

                    else:
                        try:
                            if Parameter == "":
                                Popen( [DefaultPathAfterInstall.encode('cp949')] )
                            else:
                                Popen( [DefaultPathAfterInstall.encode('cp949'), Parameter.encode('cp949')] )
                        except:
                            
                            if "Program Files (x86)" in DefaultPathAfterInstall:
                                if Parameter == "":
                                    Popen( [DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files").encode('cp949')] )
                                else:
                                    Popen( [DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files").encode('cp949'), Parameter.encode('cp949')] )
                            else:
                                if Parameter == "":
                                    Popen( [DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)").encode('cp949')] )
                                else:
                                    Popen( [DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)").encode('cp949'), Parameter.encode('cp949')] )
                        
            
            

        if 'darwin' in Platform:
            ModulePath.replace(" ","\ ")
            ModulePath.replace("(","\(")
            ModulePath.replace(")","\)")
            
            if "py" in ResultList[0][0]:
                os.system("sudo python " + '"' + ModulePath.encode('utf8') + '"' )
            
            elif "g" in ResultList[0][0]:  
                os.system("sudo open " + '"' + ModulePath.encode('utf8') + '"' )
            
            elif "c" in ResultList[0][0]:
                print "cli module"
                
            else: 
                print "Executabla type error"
    
    def ThreadModuleInstall(self, Process, ModulePath, DBPath, DefaultPathAfterInstall):
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        while Process.poll() is None: 
            time.sleep(0.5)
    
        print "installation process is done."
    
        if os.path.isfile(DefaultPathAfterInstall) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")) \
            or os.path.isdir(DefaultPathAfterInstall) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")):
            UpdateQuery = "update ModuleList set isInstalled = 'y' where ModulePath = '" + ModulePath + "'"
            cursor.execute(UpdateQuery)
            con.commit()
            
        con.close()
            
        return

    def FileHashCalc(self, FilePath):
        
        Hash = FilePath
        
        return Hash


# generate a random secret key
    #BLOCK_SIZE = 32
    #secret = os.urandom(BLOCK_SIZE)
   
    def DummyCyber(self, secret, plaintext, ciphertext):
        
        # the block size for the cipher object; must be 16, 24, or 32 for AES
        BLOCK_SIZE = 32
        
        # the character used for padding--with a block cipher such as AES, the value
        # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'
        
        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        
        # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        
        
        
        # create a cipher object using the random secret
        cipher = AES.new(secret)
        
        # encode a string
        if plaintext.strip() != "":
            try:
                encoded = EncodeAES(cipher, plaintext)
            except:
                encoded = plaintext
            #print 'Encrypted string:', encoded
            return encoded
        
        # decode the encoded string
        if ciphertext.strip() != "":
            try:
                decoded = DecodeAES(cipher, ciphertext)
            except:
                decoded = ciphertext
            #print 'Decrypted string:', decoded
            return decoded

        return ""



#---code for drag and drop UI

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, setFn):
        wx.FileDropTarget.__init__(self)
        
        self.setFn = setFn

    def OnDropFiles(self, x, y, filenames):
        
        self.setFn(x, y, filenames)
       

class ListDrop(wx.PyDropTarget):
    """ Drop target for simple lists. """

    def __init__(self, setFn):
        """ Arguments:
         - setFn: Function to call on drop.
        """
        wx.PyDropTarget.__init__(self)

        self.setFn = setFn

        # specify the type of data we will accept
        self.data = wx.PyTextDataObject()
        self.SetDataObject(self.data)

    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object
        if self.GetData():
            self.setFn(x, y, self.data.GetText())

        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d


#---code for PFP-List viewing
class AnalysisCategoryList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)

        self.listidx = 0

        self.parent = parent
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent()
        self.PublicPFPListFilePath = self.parent.GetParent().GetParent().GetParent().GetParent().public_pfplist_path
        self.PFPListFilePath = self.parent.GetParent().GetParent().GetParent().GetParent().default_pfplist_path
        #self.PFPListFilePath = "./PFPModule/PFPLib/PublicPFPList/public.windowsfamily.pfplist.sqlite"
  
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal1.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal1.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal1.png']
        self.il = wx.ImageList(32, 32)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.InsertColumn(1, '')
        
        self.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
 
 
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)
 
 
    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """

        # Create the data object: Just use plain text.
        data = wx.PyTextDataObject()
        idx = e.GetIndex()
        ContentsID = self.GetItem(idx, 0).GetText()
        Text = self.GetItem(idx, 1).GetText()
        #DBPath + Query + ContentsID
        """
        "select Text, ContentsID from CategoryTable"
        "select Text, ContentsID from AnPointTable"
        "select Text, ContentsID from VesLocationTable"
        Location = "Category"
        Location = "Analysis Point"
        Location = "Target"
        """
        
        ContentsPath = self.PublicPFPListFilePath + "[Token]" + "select Text, ContentsID from CategoryTable" + "[Token]" + ContentsID
        data.SetText( "Category" + "[_Token_]" + Text + "[_Token_]" + ContentsPath)
        #DBPath + "[Token]" + Query + "[Token]" + ResultRow[1]

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        """
        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            # It's possible we are dragging/dropping from this list to this list.  In which case, the
            # index we are removing may have changed...

            # Find correct position.
            pos = self.FindItem(idx, ContentsID)
            self.DeleteItem(pos)
        """ 
        
    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 0)
        self.SetColumnWidth(1, size.x-5)
        event.Skip()
        
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.SelectedID = event.GetText()
        self.SelectedIndex = event.GetIndex()
        
        ParentWindow = self.parent.GetParent().GetParent().GetParent().GetParent()
        
        ParentWindow.PopupMenuLocation = "Category"
        
        if self.parent.GetParent().GetParent().GetParent().GetParent().isPFPOnManaging == True:
        
            PopupMenu = wx.Menu()        
            
            EnterRelatedWebPage  = PopupMenu.Append(-1, "Enter Related Web Page")                        
                         
            self.Bind(wx.EVT_MENU, ParentWindow.OnEnterRelatedWebPage, EnterRelatedWebPage)
            
            #---Set Menu bar---
            self.PopupMenu(PopupMenu, event.GetPoint())

    def OnSelect(self, event):
        
                
        #load AnPoint..
        ContentsID = event.GetText()
        window = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList') 
        window.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, ContentsID)
        
        #initialize 3-brother and vestige location
        windowVestigeLocation = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
        windowRelatedToolsForAcquisition = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        windowAnalysisDescription = self.parent.GetGrandParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        #windowRelatedToolsForAnalysis = self.parent.GetGrandParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
        
        #for i in range(0,100):
        windowVestigeLocation.DeleteAllItems()#.DeleteItem(0)
        windowRelatedToolsForAcquisition.DeleteAllItems()#.DeleteItem(0)
        windowAnalysisDescription.DeleteAllItems()#.DeleteItem(0)
        #windowRelatedToolsForAnalysis.DeleteAllItems()#.DeleteItem(0)
        
        
        
        #Set related web page link
        DBPath = ""
        if self.GetItemBackgroundColour(event.GetIndex()) == '#e6f1f5':
            DBPath = self.PFPListFilePath
        else:
            DBPath = self.PublicPFPListFilePath
            
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        

        
        SelectQuery = "select RelatedWebPage from CategoryTable where ContentsID = '" + ContentsID + "'"
        cursor.execute( SelectQuery )
        
        ResultRow = cursor.fetchone()
        
        con.close()
        
        try:
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.SetURL(ResultRow[0])
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.SetToolTip(wx.ToolTip(ResultRow[0]))
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.UpdateLink()
            
            window0 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('Related Web Page Status')
            window0.SetLine(ResultRow[0])
        except:
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.SetURL("")
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.SetToolTip(wx.ToolTip(""))
            self.parent.GetParent().GetParent().GetParent().GetParent()._hyper2.UpdateLink()
            
            window0 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('Related Web Page Status')
            window0.SetLine("")
        

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')
        
    def LoadData(self, PublicFilePath, UserFilePath):
        
        temp_listdb_con = sqlite3.connect( PublicFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( UserFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        if len(PublicResultRows) <= 0:
            for UserRow in UserResultRows:
                if "top0" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
        
        else:
            for UserRow in UserResultRows:
                if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                if "(.. delete..)" not in PublicRow[0]:
                    ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0] and int(PublicRow[1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                        ResultRows.append(UserRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                    ResultRows.append(UserRow)
                    
        for Row in ResultRows:
            
            self.InsertStringItem(self.listidx, Row[1])
            
            try:
                UtilClass = Util()
                self.SetStringItem(self.listidx, 1, UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", Row[0]))
                
            except:
                self.SetStringItem(self.listidx, 1, Row[0])
                
            self.SetItemColumnImage(self.listidx,1, 1)
            if int(Row[1]) >= 500000 :
                self.SetItemBackgroundColour(self.listidx, '#e6f1f5')
            self.listidx +=1
            
        temp_listdb_con.close()
        
    def OnKeyDown(self, evt):
        
        if evt.GetKeyCode() != wx.WXK_TAB and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList')
                window.SetFocus()
                if window.GetFocusedItem() == -1:
                   window.Select(0) 

class AnalysisPointList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)

        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.InsertColumn(0, '')
        self.InsertColumn(1, '')

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)
 
 
    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """

        # Create the data object: Just use plain text.
        data = wx.PyTextDataObject()
        idx = e.GetIndex()
        ContentsID = self.GetItem(idx, 0).GetText()
        Text = self.GetItem(idx, 1).GetText()
        #DBPath + Query + ContentsID
        """
        "select Text, ContentsID from CategoryTable"
        "select Text, ContentsID from AnPointTable"
        "select Text, ContentsID from VesLocationTable"
        Location = "Category"
        Location = "Analysis Point"
        Location = "Target"
        """
        
        ContentsPath = self.PublicPFPListFilePath + "[Token]" + "select Text, ContentsID from AnPointTable" + "[Token]" + ContentsID
        data.SetText( "Analysis Point" + "[_Token_]" + Text + "[_Token_]" + ContentsPath)
        #DBPath + "[Token]" + Query + "[Token]" + ResultRow[1]

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        """
        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            # It's possible we are dragging/dropping from this list to this list.  In which case, the
            # index we are removing may have changed...

            # Find correct position.
            pos = self.FindItem(idx, ContentsID)
            self.DeleteItem(pos)
        """



    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 0)
        self.SetColumnWidth(1, size.x-5)
        event.Skip()



    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.SelectedID = event.GetText()
        self.SelectedIndex = event.GetIndex()
        
        ParentWindow = self.GetGrandParent().GetGrandParent().GetGrandParent()
        
        ParentWindow.PopupMenuLocation = "AnPoint"
        
        if self.GetGrandParent().GetGrandParent().GetGrandParent().isPFPOnManaging == True:
        
            PopupMenu = wx.Menu()        
            
            EnterRelatedWebPage  = PopupMenu.Append(-1, "Enter Related Web Page")                        
                         
            self.Bind(wx.EVT_MENU, ParentWindow.OnEnterRelatedWebPage, EnterRelatedWebPage)
            
            #---Set Menu bar---
            self.PopupMenu(PopupMenu, event.GetPoint())



    def OnSelect(self, event):
        
        UtilClass = Util()
        
        windowVestigeLocation = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
        
        AnPointID = event.GetText()
            
        #Load VestigeLocation
        windowVestigeLocation.LoadData(self.PublicPFPListFilePath, self.UserPFPListFilePath, self.NowCategory, AnPointID)

        #initialize 3-brother
        windowRelatedToolsForAcquisition = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        windowAnalysisDescription = self.parent.GetGrandParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        #windowRelatedToolsForAnalysis = self.parent.GetGrandParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
        
        #for i in range(0,100):
        windowRelatedToolsForAcquisition.DeleteAllItems()#.DeleteItem(0)
        windowAnalysisDescription.DeleteAllItems()#.DeleteItem(0)
        #windowRelatedToolsForAnalysis.DeleteAllItems()#.DeleteItem(0)
        
        DBPath = ""
        if self.GetItemBackgroundColour(event.GetIndex()) == '#e6f1f5':
            DBPath = self.UserPFPListFilePath
        else:
            DBPath = self.PublicPFPListFilePath
            
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        

        
        SelectQuery = "select RelatedWebPage from AnPointTable where ContentsID = '" + AnPointID + "'"
        cursor.execute( SelectQuery )
        
        ResultRow = cursor.fetchone()
        
        con.close()
        
        try:
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.SetURL(ResultRow[0])
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.SetToolTip(wx.ToolTip(ResultRow[0]))
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.UpdateLink()
            
            window0 = self.GetGrandParent().GetGrandParent().GetGrandParent().FindWindowByName('Related Web Page Status')
            window0.SetLine(ResultRow[0])
        except:
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.SetURL("")
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.SetToolTip(wx.ToolTip(""))
            self.GetGrandParent().GetGrandParent().GetGrandParent()._hyper2.UpdateLink()
            
            window0 = self.GetGrandParent().GetGrandParent().GetGrandParent().FindWindowByName('Related Web Page Status')
            window0.SetLine("")
        

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')
        
    def LoadData(self, PublicPFPListFilePath, UserPFPListFilePath, Category):
        
        self.PublicPFPListFilePath = PublicPFPListFilePath
        self.UserPFPListFilePath = UserPFPListFilePath
        self.NowCategory = Category
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal2.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal2.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal2.png']
        self.il = wx.ImageList(32, 32)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        

        
        
        #for i in range(0,100):
        self.DeleteAllItems()#.DeleteItem(0)

        temp_listdb_con = sqlite3.connect( PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        for UserRow in UserResultRows:
            if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:
                ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
                    
                    
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)  
                
        
        
        #self.InsertColumn(0, '')
        
        idx = 0 
        for Row in ResultRows:
            
            self.InsertStringItem(idx, Row[1])
            
            try:
                UtilClass = Util()
                self.SetStringItem(idx, 1, UtilClass.DummyCyber(self.GetGrandParent().GetGrandParent().GetGrandParent().DecodedDummy, "", Row[0]))
                
            except:
                self.SetStringItem(idx, 1, Row[0])
                
            self.SetItemColumnImage(idx,1, 1)
            
            if int(Row[1]) > 500000 :
                self.SetItemBackgroundColour(idx, '#e6f1f5')
            idx +=1
                        
        temp_listdb_con.close()
        
            
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_TAB and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                windowVestigeLocation = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
                windowVestigeLocation.SetFocus()
                if windowVestigeLocation.GetFocusedItem() == -1:
                   windowVestigeLocation.Select(0) 
                
            elif evt.GetKeyCode() == wx.WXK_LEFT:
                
                windowCategory = self.parent.GetGrandParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
                windowCategory.SetFocus()
                if windowCategory.GetFocusedItem() == -1:
                   windowCategory.Select(0) 
            
class VestigeLocationList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent, id):
        #wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/information_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/right_arrow_16_16.png',
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/registry_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)   

        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.InsertColumn(0, '')
        self.InsertColumn(1, '')

        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)
        
        self.ActivationFlag = False
        self.FileSystemRunValue = False
        self.RegistryRunValue = False
        
        self.NowComboSelected = ""
        
        self.FileSystemThreadEndFlag = False
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
 
 
 
 
    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """

        # Create the data object: Just use plain text.
        data = wx.PyTextDataObject()
        idx = e.GetIndex()
        ContentsID = self.GetItem(idx, 1).GetText()
        Text = self.GetItem(idx, 0).GetText()
        #DBPath + Query + ContentsID
        """
        "select Text, ContentsID from CategoryTable"
        "select Text, ContentsID from AnPointTable"
        "select Text, ContentsID from VesLocationTable"
        Location = "Category"
        Location = "Analysis Point"
        Location = "Target"
        """
        
        ContentsPath = self.PublicPFPListFilePath + "[Token]" + "select Text, ContentsID from VesLocationTable" + "[Token]" + ContentsID
        data.SetText( "Target" + "[_Token_]" + Text + "[_Token_]" + ContentsPath)
        #DBPath + "[Token]" + Query + "[Token]" + ResultRow[1]

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        """
        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            # It's possible we are dragging/dropping from this list to this list.  In which case, the
            # index we are removing may have changed...

            # Find correct position.
            pos = self.FindItem(idx, ContentsID)
            self.DeleteItem(pos)
        """



    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        self.SetColumnWidth(1, 0)
        event.Skip()
        
        
        
    def OnActivated(self, event):

        if self.ActivationFlag == True:
            wx.MessageBox("Please wait. other process is running")

        else:
            self.NowKeyword = event.GetText()
            
            threads = []
            th = threading.Thread(target=self.ThreadActivation, args=())
            th.start()
            threads.append(th)


        return

    def SetRegistryTreeAndList(self):
        
        """
        if self.RegistryRunValue == True:
            wx.MessageBox("Registry Lookup processing is Running.")
            
            return
        """
        
        #try:
            
        SelfTest = PFPUtil()
        #self.RegistryRunValue = True
        
        
        Keyword = self.NowRegistryComboSelected
        
        windowTargetStatusBar = self.parent.GetGrandParent().FindWindowByName('VestigeLocationStatusbar')
        NoteBook = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().nb
        Registry_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().Registry_Page
        FileSystem_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FileSystem_Page
        AnTargetRoot = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().AnalysisTargetRoot
        System_inode = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().System_inode
        MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        RawHandlerClass = RawHandler()
        
        
        
        
        #print "MainFrame.System_inode : "
        #print MainFrame.System_inode
        
        
        
        
        #List Setting 
        
        ResultValues = []
        ResultSubKeys = []
        
        
        HivePath = ""
        KeyPath = ""
        
        #print Keyword
        if "hku\\.default" in Keyword.lower():
            HivePath = AnTargetRoot + "\\Windows\\System32\\config\\default"
            KeyPath = Keyword[13:]
            
        elif "hklm\\software" in Keyword.lower():
            HivePath = AnTargetRoot + "\\Windows\\System32\\config\\software"
            KeyPath = Keyword[14:]
            
        elif "hklm\\security" in Keyword.lower():
            HivePath = AnTargetRoot + "\\Windows\\System32\\config\\security"
            KeyPath = Keyword[14:]
            
        elif "hklm\\system" in Keyword.lower():
            HivePath = AnTargetRoot + "\\Windows\\System32\\config\\system"
            KeyPath = Keyword[12:]
            
        elif "hklm\\sam" in Keyword.lower():
            HivePath = AnTargetRoot + "\\Windows\\System32\\config\\sam"
            KeyPath = Keyword[9:]
            
        elif "hku\\" in Keyword.lower():
            
            if len(Keyword.split("\\")) > 3:
            
                if Keyword.split("\\")[2].lower() == "software" and Keyword.split("\\")[3].lower() == "classes":
                    UserDir = ""
                    if os.path.isdir(AnTargetRoot+"\\Users"):
                        UserDir = AnTargetRoot+"\\Users\\"
                    elif os.path.isdir(AnTargetRoot+"\\Documents and Settings"):
                        UserDir = AnTargetRoot+"\\Documents and Settings\\"
                        
                    HivePath = UserDir + Keyword.split("\\")[1] + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat"
                    KeyPath = Keyword.replace("HKU\\"  + Keyword.split("\\")[1] + "\\Software\\Classes\\","").replace("HKU\\"  + Keyword.split("\\")[1] + "\\software\\classes\\","").replace("HKU\\"  + Keyword.split("\\")[1] + "\\SOFTWARE\\CLASSES\\","")
                    KeyPath = KeyPath.replace("HKU\\"  + Keyword.split("\\")[1] + "\\Software\\Classes","").replace("HKU\\"  + Keyword.split("\\")[1] + "\\software\\classes","").replace("HKU\\"  + Keyword.split("\\")[1] + "\\SOFTWARE\\CLASSES","")
                    
            
                else:
                    UserDir = ""
                    if os.path.isdir(AnTargetRoot+"\\Users"):
                        UserDir = AnTargetRoot+"\\Users\\"
                    elif os.path.isdir(AnTargetRoot+"\\Documents and Settings"):
                        UserDir = AnTargetRoot+"\\Documents and Settings\\"
                    
                    HivePath = UserDir + Keyword.split("\\")[1] + "\\NTUSER.DAT"
                    KeyPath = Keyword.replace("HKU\\"  + Keyword.split("\\")[1] + "\\","")
                    KeyPath = KeyPath.replace("HKU\\"  + Keyword.split("\\")[1],"")
                    
            else:
                UserDir = ""
                if os.path.isdir(AnTargetRoot+"\\Users"):
                    UserDir = AnTargetRoot+"\\Users\\"
                elif os.path.isdir(AnTargetRoot+"\\Documents and Settings"):
                    UserDir = AnTargetRoot+"\\Documents and Settings\\"
                    
                HivePath = UserDir + Keyword.split("\\")[1] + "\\NTUSER.DAT"
                KeyPath = Keyword.replace("HKU\\"  + Keyword.split("\\")[1] + "\\","")
                KeyPath = KeyPath.replace("HKU\\"  + Keyword.split("\\")[1],"")
                
                    
        else:
            wx.MessageBox("invalid key")
            
            Registry_Page.combo.SetValue(Registry_Page.OriginalCombo)
            
            self.RegistryRunValue = False    
            
            return
        
        #print "KeyPath = " + KeyPath
        #print "HivePath = " + HivePath
        
        if KeyPath.strip() == "":
            KeyPath = "\\"
        
        """
        if KeyPath.strip() == "":
            wx.MessageBox("Key is not existed(or root)")
            
            self.RegistryRunValue = False    
            
            return
        """
        
        
        windowTargetStatusBar.SetLine('Now interpret filesystem and hive structure.....')
        
        has_inode = False
        inode = None
        for tuple in System_inode:
            if HivePath.lower() == tuple[0].lower(): 
                inode = tuple[1]
                has_inode = True
            
            if has_inode == True:
                break
        
        if inode == None:
            Ret_List = []
            if MainFrame.isCaseSet == True:
                Ret_List = RawHandlerClass.get_inode(HivePath, caseDBPath=MainFrame.CaseDBPath)
            else:
                Ret_List = RawHandlerClass.get_inode(HivePath)
            for element in Ret_List:
                MainFrame.System_inode.append(element)
                
                if element[0].lower() in HivePath.lower():
                    inode = element[1]

        #print "MainFrame.System_inode = "                
        #print MainFrame.System_inode
        
        
        ret_depth, ResultValues, ResultSubKeys = RawHandlerClass.Reg_GetValue(HivePath, inode, KeyPath)
        
        windowTargetStatusBar.SetLine('TargetRoot = ' + AnTargetRoot + ', Look up RegKey : ' + Keyword)
        
        #print ResultValues    
            
        #Reg Key not found
        #if len(ResultValues) > 0:
        Tokens = KeyPath.split("\\")
        
        #print "ret_depth = " + str(ret_depth)
        #print "len(Tokens) = " + str(len(Tokens))
        if ret_depth != len(Tokens):
            XKeyIdx = ret_depth #int(ResultValues[0][0].split(":")[1])
            ReAssembleKey = ""
            LostValue = ""
            Token = KeyPath.split("\\")
            for idx in range(0, XKeyIdx):
                ReAssembleKey += Token[idx] + "\\"
            
            for idx in range(XKeyIdx, len(Token)):
                LostValue += Token[idx] + "\\"
                
            KeyPath = ReAssembleKey
            
            """
            if KeyPath.strip() == "":
                wx.MessageBox("Key is not existed(or root)")
                
                self.RegistryRunValue = False    
                
                return
            """    
            #ResultValues, ResultSubKeys = RawHandlerClass.Reg_GetValue(HivePath, KeyPath)
            
            
            ComboText = Registry_Page.combo.GetValue()
            Registry_Page.OriginalCombo = ComboText
            
            ComboValue = ComboText.replace(ReAssembleKey, ReAssembleKey + "<")
            
            ComboValue += ">"
            
            ComboText = Registry_Page.combo.GetValue()
            Registry_Page.OriginalCombo = ComboText
            
            Registry_Page.combo.SetValue(ComboValue.split("<")[0])  #.split("<")[0] 이거 제거하면 HKLM\~~\~~\<~~> 이렇식으로 표시됨 (예전 방법) 15.08.08
            
            #Registry_Page.combo.SetValue(ReAssembleKey)
            

        if KeyPath[len(KeyPath)-1] == "\\":
            KeyPath = KeyPath[0:len(KeyPath)-1]
        Token = KeyPath.split("\\")
            
        Registry_Page.tree.DeleteAllItems()
        
        Registry_Page.tree.root = Registry_Page.tree.AddRoot("Registry Lookup Result")

        if not(Registry_Page.tree.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            Registry_Page.tree.SetItemImage(Registry_Page.tree.root, Registry_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
            Registry_Page.tree.SetItemImage(Registry_Page.tree.root, Registry_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
            
            
        
        child = Registry_Page.tree.AppendItem(Registry_Page.tree.root, Token[len(Token)-1])

        Registry_Page.tree.SetItemImage(child, Registry_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
        Registry_Page.tree.SetItemImage(child, Registry_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
        
        
        Registry_Page.tree.Expand(Registry_Page.tree.root)
        Registry_Page.tree.SelectItem(child)



        
        Registry_Page.list.DeleteAllItems()
        
        idx = 0
        
        Registry_Page.list.InsertStringItem(idx, "SubKey")    
        Registry_Page.list.SetStringItem(idx, 1, "..")
        Registry_Page.list.SetItemImage(idx, 0)
        
        idx += 1
        
        for SubKey in ResultSubKeys:
            
            Registry_Page.list.InsertStringItem(idx, "SubKey")    
            Registry_Page.list.SetStringItem(idx, 1, SubKey[0])
            Registry_Page.list.SetStringItem(idx, 2, str(SubKey[1]))
            Registry_Page.list.SetItemImage(idx, 0)
            
            Subchild = Registry_Page.tree.AppendItem(child, SubKey[0])

            Registry_Page.tree.SetItemImage(Subchild, Registry_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
            Registry_Page.tree.SetItemImage(Subchild, Registry_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
            
            idx += 1
            
        def HexValue_to_HexString(HexValues):
        
            text = ''
            
            for Value in HexValues:
                UpperValue = (ord(Value) & 0xF0) >> 4
                LowerValue = ord(Value) & 0x0F
                
                if UpperValue >= 0 and UpperValue <= 9:
                    text += str(UpperValue)
                elif UpperValue == 10:
                    text += 'A'
                elif UpperValue == 11:
                    text += 'B'
                elif UpperValue == 12:
                    text += 'C'
                elif UpperValue == 13:
                    text += 'D'
                elif UpperValue == 14:
                    text += 'E'
                elif UpperValue == 15:
                    text += 'F'
                    
                if LowerValue >= 0 and LowerValue <= 9:
                    text += str(LowerValue)
                elif LowerValue == 10:
                    text += 'A'
                elif LowerValue == 11:
                    text += 'B'
                elif LowerValue == 12:
                    text += 'C'
                elif LowerValue == 13:
                    text += 'D'
                elif LowerValue == 14:
                    text += 'E'
                elif LowerValue == 15:
                    text += 'F'
                
                text += ' '
                            
            return text
            
        for Value in ResultValues:
            
            Registry_Page.list.InsertStringItem(idx, "Value")    
            Registry_Page.list.SetStringItem(idx, 1, Value[0])
            Registry_Page.list.SetStringItem(idx, 2, Value[1])
            if "bin" in Value[1].lower():
                TextHex = "0x"
                if len(Value[2]) > 100:
                    TextHex += HexValue_to_HexString(Value[2][0:100])
                    TextHex += "..."
                else : 
                    TextHex += HexValue_to_HexString(Value[2])
                Registry_Page.list.SetStringItem(idx, 3, TextHex)
            else:
                try:
                    Registry_Page.list.SetStringItem(idx, 3, str(Value[2]))
                except:
                    Registry_Page.list.SetStringItem(idx, 3, "[Value error]")
            if "SZ" in Value[1]:
                Registry_Page.list.SetItemImage(idx, 2)
            else:
                Registry_Page.list.SetItemImage(idx, 1)
            
            idx += 1
            
        Registry_Page.tree.Expand(child)
        
        #self.RegistryRunValue = False    
            
                
        #except:
        #    print "exception error(in SetRegistryTreeAndList)" 
        #    self.RegistryRunValue = False


    def ThreadActivation(self):

        self.ActivationFlag = True
        
        #try:
        Keyword = self.NowKeyword 
        
        windowTargetStatusBar = self.parent.GetGrandParent().FindWindowByName('VestigeLocationStatusbar')
        ModuleListWindow = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('ModuleListOnList')
        NoteBook = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().nb
        Registry_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().Registry_Page
        FileSystem_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FileSystem_Page
        AnTargetRoot = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().AnalysisTargetRoot

        RawHandlerClass = RawHandler()




        #print Keyword
        if "[*]" in Keyword or "[-]" in Keyword.lower() or "[+]" in Keyword.lower():
            wx.MessageBox("Can not execute category item")
            windowTargetStatusBar.SetLine('Can not execute category item')
            
            
            self.ActivationFlag = False
            
            return
        
        
        
        elif "[RegKey]" in Keyword or "[regkey]" in Keyword.lower():
            
            PossibleKeys = []
            
            Keyword = Keyword.replace("[RegKey]", "").replace("[regkey]", "").replace("[REGKEY]", "").replace("[REGKey]", "").strip()
            if Keyword[len(Keyword)-1] == "\\":
                Keyword = Keyword[0:len(Keyword)-1]
                
                
            UserDir = ""
        
            if os.path.isdir(AnTargetRoot+"\\Users"):
                UserDir = AnTargetRoot+"\\Users\\"
            elif os.path.isdir(AnTargetRoot+"\\Documents and Settings"):
                UserDir = AnTargetRoot+"\\Documents and Settings\\"
                
            if "controlset00x" in Keyword.lower() or "currentcontrolset" in Keyword.lower() or "controlset00#" in Keyword.lower() or "controlsetxxx" in Keyword.lower():
                KeywordList = [Keyword.replace("ControlSet00X", "ControlSet001").replace("CurrentControlSet", "ControlSet001").replace("ControlSet00#", "ControlSet001").replace("ControlSetXXX", "ControlSet001")]
                KeywordList.append(Keyword.replace("ControlSet00X", "ControlSet002").replace("CurrentControlSet", "ControlSet002").replace("ControlSet00#", "ControlSet002").replace("ControlSetXXX", "ControlSet002"))
                
            else:
                KeywordList = [Keyword]
            
            for Keyword in KeywordList:
                if "hkcu\\software\\classes" in Keyword.lower():
                        
                    flist = os.listdir(UserDir)
                    for f in flist:
                        SubDir = os.path.join(UserDir, f)
                        if os.path.isfile(SubDir + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat"):
                            PossibleKeys.append(Keyword.replace("HKCU", "HKU\\"+f))
                            
                elif "hku\\{user}\\software\\classes"  in Keyword.lower():
                        
                    flist = os.listdir(UserDir)
                    for f in flist:
                        SubDir = os.path.join(UserDir, f)
                        #print UserDir
                        #print SubDir
                        #print SubDir + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat"
                        #print "isfile = " + str(os.path.isfile(SubDir + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat"))
                        if os.path.isfile(SubDir + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat"):
                            PossibleKeys.append(Keyword.replace("HKU\\{USER}", "HKU\\"+f))
                            
                elif "hkcu\\" in Keyword.lower():
                        
                    flist = os.listdir(UserDir)
                    for f in flist:
                        SubDir = os.path.join(UserDir, f)
                        if os.path.isfile(os.path.join(SubDir, "NTUSER.DAT")):
                            PossibleKeys.append(Keyword.replace("HKCU", "HKU\\"+f))
                            
                elif "hku\\{user}" in Keyword.lower():
                        
                    flist = os.listdir(UserDir)
                    for f in flist:
                        SubDir = os.path.join(UserDir, f)
                        if os.path.isfile(os.path.join(SubDir, "NTUSER.DAT")):
                            PossibleKeys.append(Keyword.replace("HKU\\{USER}", "HKU\\"+f))
                            
                elif "hkcr\\" in Keyword.lower():
                    PossibleKeys.append(Keyword.replace("HKCR", "HKLM\\Software\\Classes"))
                    #HKCU\\Software\\Classes
                    """
                    flist = os.listdir(UserDir)
                    for f in flist:
                        SubDir = os.path.join(UserDir, f)
                        if os.path.isfile(os.path.join(SubDir, "NTUSER.DAT")):
                            PossibleKeys.append(Keyword.replace("HKCR\\", "HKU\\"+f+"\\Software\\Classes\\"))
                    """
                    
                else:
                    PossibleKeys.append(Keyword)
            
            
            
                
            
            Registry_Page.combo.Clear()
            
            for Keyword in PossibleKeys:
                if "HKU\\Default User\\" not in Keyword:
                    Registry_Page.combo.Append(Keyword)
                
            ComboText = Registry_Page.combo.GetValue()
            Registry_Page.OriginalCombo = ComboText
            Registry_Page.combo.SetValue(PossibleKeys[0])
            
            
            
            
            
            self.NowRegistryComboSelected = PossibleKeys[0]
            
            
            
            
            #self.SetRegistryTreeAndList()
            threads = []
            th = threading.Thread(target=self.SetRegistryTreeAndList, args=())
            th.start()
            threads.append(th)
            
            progressMax = 100
            dialog = wx.ProgressDialog("Registry Lookup progress", "Please wait..", progressMax,
                    style=wx.PD_ELAPSED_TIME )
            
            while th.is_alive() == True:
                wx.Sleep(1)
                dialog.Pulse()
            
            dialog.Destroy()
            
            
            """
            max = 0
            
            while th.is_alive() == True:
                
                LogKeyword = 'Reg Key Lookup = ' + PossibleKeys[0] + " ["
                for idx in range(0, max):
                    LogKeyword += "."
                LogKeyword += "]"
                
                time.sleep(0.5)
            
                windowTargetStatusBar.SetLine(LogKeyword)
                
                max += 1
                if max == 10:
                    max = 0
                #th.join()
            """
            
            
            
                
            Registry_Page.list.SetFocus()
            NoteBook.SetSelection(3)
            #ModuleListWindow.FindModuleByName("[Public] Registry(Windows)")
            
            
            
        
        
        else: #elif os.path.isdir(Keyword) or os.path.isdir(Keyword): 
            
            if Keyword[len(Keyword)-1] == "\\":
                Keyword = Keyword[0:len(Keyword)-1]
            
                
            ComboText = FileSystem_Page.combo.GetValue()               
            RetList = self.SetPath(Keyword)
        
            FileSystem_Page.combo.Clear()
            
            for Keyword in RetList:
                FileSystem_Page.combo.Append(Keyword)
                
            #print ComboText
            FileSystem_Page.OriginalCombo = ComboText
            FileSystem_Page.combo.SetValue(RetList[0])
            
            windowTargetStatusBar.SetLine('TargetRoot = ' + AnTargetRoot + ', Get Meta : ' + Keyword)
            NoteBook.SetSelection(2)
            #ModuleListWindow.FindModuleByName("[Public] File System")
            
            
            
            self.NowComboSelected = RetList[0]
            
            
            #self.SetFileSystemTreeAndList()
            threads = []
            th = threading.Thread(target=self.SetFileSystemTreeAndList, args=())
            th.start()
            threads.append(th)
            
            progressMax = 100
            dialog = wx.ProgressDialog("Filesystem Lookup progress", "Please wait..", progressMax,
                    style=wx.PD_ELAPSED_TIME )
            
            while th.is_alive() == True:
                wx.Sleep(1)
                dialog.Pulse()
            
            dialog.Destroy()
            
            
            
            """
            max = 0
            windowTargetStatusBar.SetDefaultStyle(wx.TextAttr(wx.BLUE))
            
            while th.is_alive() == True:
                
                LogKeyword = 'FS Lookup = TargetRoot : ' + AnTargetRoot + ', Keyword : ' + Keyword + " ["
                for idx in range(0, max):
                    LogKeyword += "."
                LogKeyword += "]"
                
                time.sleep(0.5)
            
                windowTargetStatusBar.SetLine(LogKeyword)
                
                
                max += 1
                if max == 10:
                    max = 0
                #th.join()
            """
            
            windowTargetStatusBar.SetLine("Complete (Target root = " + AnTargetRoot + ")")
            

            
            
            
        self.ActivationFlag = False
        #print "????"
        #windowTargetStatusBar.SetLine('TargetRoot = ' + AnTargetRoot)
    
    
    
    
    
        #except:
        #    wx.MessageBox("Exception. in Thread activation")
        #    windowTargetStatusBar.SetLine('Exception...  TargetRoot = ' + AnTargetRoot)
        #    self.ActivationFlag = False
    
        return 
    
    
    def SetFileSystemTreeAndList(self):

        windowTargetStatusBar = self.parent.GetGrandParent().FindWindowByName('VestigeLocationStatusbar')
        NoteBook = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().nb
        Registry_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().Registry_Page
        FileSystem_Page = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FileSystem_Page
        AnTargetRoot = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().AnalysisTargetRoot
        System_inode = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().System_inode
        MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        
        
        
        
        #other therad check
        if self.FileSystemRunValue == True:
            dlg = wx.MessageDialog(None, "FileSystem Lookup processing is Running. Are you sure to terminate it?", 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                FileSystem_Page.combo.SetValue(FileSystem_Page.OriginalCombo)
                dlg.Destroy()
                return
            
            
            self.FileSystemThreadEndFlag = True
            FileSystem_Page.combo.SetValue(FileSystem_Page.OriginalCombo)
            self.FileSystemRunValue = False
            self.FileSystemThreadEndFlag = False
            
            
            return
        
        
        
        
        
        
        
        #try:
        self.FileSystemRunValue = True
        Keyword = self.NowComboSelected
        RawHandlerClass = RawHandler()
        
        #print [Keyword]
        #print type(Keyword)
        
        
        Token = Keyword.split("\\")
        
        
        #Tree and List init
        ###################
        
        #Tree init
        FileSystem_Page.tree.DeleteAllItems()
        FileSystem_Page.tree.root = FileSystem_Page.tree.AddRoot("FileSystem Meta Lookup Result")

        if not(FileSystem_Page.tree.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            FileSystem_Page.tree.SetItemImage(FileSystem_Page.tree.root, FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
            FileSystem_Page.tree.SetItemImage(FileSystem_Page.tree.root, FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
            
            
        
        child = FileSystem_Page.tree.AppendItem(FileSystem_Page.tree.root, Token[len(Token)-1])

        FileSystem_Page.tree.SetItemImage(child, FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
        FileSystem_Page.tree.SetItemImage(child, FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
        
        
        FileSystem_Page.tree.Expand(FileSystem_Page.tree.root)
        FileSystem_Page.tree.SelectItem(child)
        

        #List init
        FileSystem_Page.list.DeleteAllItems()
        idx = 0
        
        
        
        #windowTargetStatusBar.SetLine('Path is being Checked.. >> ' + Keyword)
        
        
        isSetExtender = False
        Extender = ""
        if "*." in os.path.split(Keyword)[1]:
            Extender = os.path.split(Keyword)[1].replace("*.", "")
            isSetExtender = True
            Keyword = os.path.split(Keyword)[0]
        
        
        has_inode = False
        inode = None
        for tuple in System_inode:
            if Keyword.lower() == tuple[0].lower(): 
                inode = tuple[1]
                has_inode = True
            
            if has_inode == True:
                break
        
        #print System_inode
        #print "insert inode = " + str(inode)
        if MainFrame.isCaseSet == True:
            result = RawHandlerClass.PathCheck(Keyword.encode('cp949'), caseDBPath=MainFrame.CaseDBPath)
        else:
            #print "type!!!!= " + str(type(Keyword))
            #print Keyword
            result = RawHandlerClass.PathCheck(Keyword.encode('cp949'), inode_in=inode)
            #print result
        def InsertData(inode_list, idx):
            if inode_list[2] == "file":
                FileSystem_Page.list.InsertStringItem(idx, "File")  
                #FileSystem_Page.list.SetItemImage(idx, 1)
            else:
                FileSystem_Page.list.InsertStringItem(idx, "Dir")
                #FileSystem_Page.list.SetItemImage(idx, 0)
            try:
                FileSystem_Page.list.SetStringItem(idx, 1, str(os.path.split(inode_list[0])[1]))
                if str(os.path.split(inode_list[0])[1]) == ".." : FileSystem_Page.list.SetItemColumnImage(idx, 0, 6)
                if inode_list[2] == "file": FileSystem_Page.list.SetItemColumnImage(idx, 1, 3)
                else:                       FileSystem_Page.list.SetItemColumnImage(idx, 1, 2)
            except:
                FileSystem_Page.list.SetStringItem(idx, 1, "Value error")
            FileSystem_Page.list.SetStringItem(idx, 2, str(inode_list[1])) 
            FileSystem_Page.list.SetStringItem(idx, 3, strftime("%Y/%m/%d %H:%M:%S", time.localtime(inode_list[3])))
            FileSystem_Page.list.SetStringItem(idx, 4, strftime("%Y/%m/%d %H:%M:%S", time.localtime(inode_list[4])))
            FileSystem_Page.list.SetStringItem(idx, 5, strftime("%Y/%m/%d %H:%M:%S", time.localtime(inode_list[6])))
            FileSystem_Page.list.SetStringItem(idx, 6, strftime("%Y/%m/%d %H:%M:%S", time.localtime(inode_list[5])))
            #print inode_list
            FileSystem_Page.list.SetStringItem(idx, 7, str(inode_list[7]))
            if inode_list[2] == "file":
                try:
                    FileSystem_Page.list.SetStringItem(idx, 8, str(os.path.split(inode_list[0])[0]))
                except:
                    FileSystem_Page.list.SetStringItem(idx, 8, "Value error")
            else:
                FileSystem_Page.list.SetStringItem(idx, 8, Keyword)
            FileSystem_Page.list.SetStringItem(idx, 9, str(inode_list[3]) + ":" + str(inode_list[4]) + ":" + str(inode_list[6]) + ":" + str(inode_list[5]))
            FileSystem_Page.list.SetStringItem(idx, 10, "")
        
        
        if result[0] == "dir":
            
            #add inode in System inode list
            if inode == None:
                for inode_list in result[1]:
                    if os.path.split(inode_list[0])[1] == ".":
                        MainFrame.System_inode.append(inode_list)
            
            
            
            #Print Dir
            for inode_list in result[1]:
                if inode_list[1] == None or (os.path.split(inode_list[0])[1] == ".") or inode_list[2] == "file":    # or os.path.split(inode_list[0])[1] == ".."):
                    continue
                if isSetExtender == True and (Extender not in os.path.split(inode_list[0])[1]):
                    continue
                #Set List
                InsertData(inode_list, idx)
                idx += 1
                #Set Tree
                SubChild = FileSystem_Page.tree.AppendItem(child, str(os.path.split(inode_list[0])[1]))
                FileSystem_Page.tree.SetItemImage(SubChild, FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
                FileSystem_Page.tree.SetItemImage(SubChild, FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
                FileSystem_Page.tree.Expand(child)
            
            #Print File    
            for inode_list in result[1]:
                if inode_list[1] == None or (os.path.split(inode_list[0])[1] == ".") or inode_list[2] != "file":    # or os.path.split(inode_list[0])[1] == ".."):
                    continue
                if isSetExtender == True and (Extender not in os.path.split(inode_list[0])[1]):
                    continue
                InsertData(inode_list, idx)
                idx += 1
            
                    

        elif result[0] == "file":
            if inode == None:
                MainFrame.System_inode.append(result[1])
            
            #print "extract : " + result[1][0] + " " + str(result[1][1])
            FileSystem_Page.combo.SetValue(os.path.split(Keyword)[0])
            InsertData(result[1], idx)
            idx += 1
            
        else:
            wx.MessageBox("There is no result")
            
        
        #windowTargetStatusBar.SetLine("Complete (Target root = " + AnTargetRoot + ")")
        self.FileSystemRunValue = False
                    
        #except:
        #    self.FileSystemRunValue = False




    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        self.SelectedID = event.GetText()
        self.SelectedIndex = event.GetIndex()
        
        
        #if self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().isPFPOnManaging == True:
        
        PopupMenu = wx.Menu()        
        
        RawCopy  = PopupMenu.Append(-1, "Extract(raw copy, checked item)")
        if MainFrame.isPremium == True:
            CopyToClipboard  = PopupMenu.Append(-1, "Copy to Clipboard(selected item)")
            Execute  = PopupMenu.Append(-1, "Execute with explorer")
        else: 
            CopyToClipboard  = PopupMenu.Append(-1, "Copy to Clipboard(Premium Only)")
                     
        self.Bind(wx.EVT_MENU, self.RawCopy_SelectedTarget, RawCopy)
        self.Bind(wx.EVT_MENU, MainFrame.OnCopy, CopyToClipboard)
        self.Bind(wx.EVT_MENU, self.OnExecute, Execute)
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPoint())
            
            
    def RawCopy_SelectedTarget(self, event):
        
        #if self.ActivationFlag == True:
        #    wx.MessageBox("Please wait. other process is running")

        #else:
        
        threads = []
        th = threading.Thread(target=self.ThreadExtract, args=())
        th.start()
        threads.append(th)


        return
    
    def OnExecute(self, event):    
        MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        if MainFrame.isPremium == True:
            itemidx = self.GetFocusedItem()
            os.system("explorer \"" + os.path.split(self.GetItemText(itemidx).strip())[0] + "\"")
                
        else:
            wx.MessageBox("Please use premium PFP.")
        
    
    def ThreadExtract(self):
        MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #리스트에서 체크 목록 가져오기
        SelectedModuleList = []
            
        for index in range(self.GetItemCount()):
            if self.IsChecked(index): 
                SelectedModuleList.append(self.GetItemText(index))     #"Find selected Data"
        
        #파일 목록의 임시 파일 생성 및 추출 모듈 구동
        TempFileName = "./PFPModule/UpdateTemp/temp_extractlist_" + str(time.time()) + ".dat"
        fp = open(TempFileName, 'w')
        for Item in SelectedModuleList:
                
            Keyword = Item
            RetList = self.SetPath(Keyword + "\t None")
            
            #Make abs paths from env variable
            for Keyword in RetList: fp.write(Keyword + "\n")
                
        fp.close()
        
        #텟스트 파일 넘기며, Extractor 구동
        
        if MainFrame.isCaseSet == True: 
            if "(img)" in self.MainFrame.CaseDBPath:    Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, MainFrame.CaseDBPath, "True"])
            else:                                       Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, self.MainFrame.CaseDBPath, "False"])
        else:                                           Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, "None"])
        
        while Process.poll() is None: 
            time.sleep(0.5)
            
        os.system( "del " + TempFileName.replace("/", "\\") )
        
        
        """
        self.ActivationFlag = True 
        
        try:
            windowTargetStatusBar = self.parent.GetGrandParent().FindWindowByName('VestigeLocationStatusbar')
            AnTargetRoot = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().AnalysisTargetRoot
            System_inode = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().System_inode
            MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
    
            SelectedModuleList = []
            
            for index in range(self.GetItemCount()):
                if self.IsChecked(index): 
                    SelectedModuleList.append(self.GetItemText(index))     #"Find selected Data"
                    
            
            windowTargetStatusBar.SetLine('Select Target folder')
            
            
            dlg = wx.DirDialog(self, message="Select target dir for extarct", style=wx.OPEN)
                        
            SelectedPath = ""
            if dlg.ShowModal() == wx.ID_OK:                    
                SelectedPath = dlg.GetPath()
                
            else:
                
                self.ActivationFlag = False
                return
            
            
            
            
            ExtractFolder = os.path.join(SelectedPath, "PFP_Extract_Result_" + str(time.time()))
            
            os.mkdir(ExtractFolder)
            
            
            
            
            
            
            #파일 목록의 임시 파일 생성 및 추출 모듈 구동
            TempFileName = "./PFPModule/UpdateTemp/temp_extractlist_" + str(time.time()) + ".dat"
            fp = open(TempFileName, 'w')
            for Item in SelectedModuleList:
                    
                Keyword = Item
                RetList = self.SetPath(Keyword)
                
                #Make abs paths from env variable
                for Keyword in RetList: fp.write(Keyword + "\n")
                    
    
            fp.close()
            
            if MainFrame.isCaseSet == True:
                MainFrame.RawHandlerClass.FileListExtract(MainFrame.interpreter_path_gui, TempFileName, ExtractFolder, windowTargetStatusBar, MainFrame.CaseDBPath)
            else:
                MainFrame.RawHandlerClass.FileListExtract(MainFrame.interpreter_path_gui, TempFileName, ExtractFolder, windowTargetStatusBar)
    
            os.system( "del " + TempFileName.replace("/", "\\") )
            windowTargetStatusBar.SetLine('TargetRoot = ' + AnTargetRoot)
            self.ActivationFlag = False
        
             
        except:
            wx.MessageBox("Exception. in Thread extract")
            self.ActivationFlag = False
        """     
        
        return 
    
    def SetPath(self, Keyword):
        
        retKeyword = []
        
        AnTargetRoot = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().AnalysisTargetRoot
        
        if "%SystemDrive%" in Keyword:
            retKeyword.append(Keyword.replace("%SystemDrive%", AnTargetRoot))
        elif "%SystemRoot%" in Keyword:
            retKeyword.append(Keyword.replace("%SystemRoot%", AnTargetRoot+"\\Windows"))
        elif "%WinDir%" in Keyword:
            retKeyword.append(Keyword.replace("%WinDir%", AnTargetRoot+"\\Windows"))
        elif "%ProgramData%" in Keyword:
            retKeyword.append(Keyword.replace("%ProgramData%", AnTargetRoot+"\\ProgramData"))
        elif "%UserProfile%" in Keyword:           
            UserDir = ""
        
            if os.path.isdir(AnTargetRoot+"\\Users"):
                UserDir = AnTargetRoot+"\\Users\\"
            elif os.path.isdir(AnTargetRoot+"\\Documents and Settings"):
                UserDir = AnTargetRoot+"\\Documents and Settings\\"
                
            flist = os.listdir(UserDir)
            for f in flist:
                SubDir = os.path.join(UserDir, f)
                if os.path.isdir(SubDir):
                    retKeyword.append(Keyword.replace("%UserProfile%", SubDir))

            
        else: 
            retKeyword.append(Keyword)
            
        
        return retKeyword


    def OnSelect(self, event):
        windowRelatedToolsForAcquisition = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        windowAnalysisDescription = self.parent.GetGrandParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        #windowRelatedToolsForAnalysis = self.parent.GetGrandParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
        

        self.VestigeLocation = self.GetItem(event.GetIndex(),1).GetText()
        
        #print "Ves ID = " + self.VestigeLocation 
        
        if self.GetItemBackgroundColour(event.GetIndex()) == '#e6f1f5':
            windowRelatedToolsForAcquisition.LoadData(self.MainFrame.default_pfplist_path, self.NowCategory, self.AnalysisPoint, self.VestigeLocation)
            windowAnalysisDescription.LoadData(self.MainFrame.default_pfplist_path, self.NowCategory, self.AnalysisPoint, self.VestigeLocation)
        else:
            windowRelatedToolsForAcquisition.LoadData(self.MainFrame.public_pfplist_path, self.NowCategory, self.AnalysisPoint, self.VestigeLocation)
            windowAnalysisDescription.LoadData(self.MainFrame.public_pfplist_path, self.NowCategory, self.AnalysisPoint, self.VestigeLocation)
        #windowRelatedToolsForAnalysis.LoadData(self.PFPListFilePath, self.NowCategory, self.AnalysisPoint, self.VestigeLocation)

    def LoadData(self, PublicPFPListFilePath, UserPFPListFilePath, Category, AnalysisPoint):

        
        self.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
        self.UserPFPListFilePath = self.MainFrame.default_pfplist_path

        self.NowCategory = Category
        self.AnalysisPoint = AnalysisPoint
        
        #for i in range(0,100):
        self.DeleteAllItems()#.DeleteItem(0)




        temp_listdb_con = sqlite3.connect( PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        if self.MainFrame.isCaseSet == True:
            SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable where AnPointID = '" + AnalysisPoint + "' and Registrant = 'Case_Data' order by cast(Sequence as decimal)"
        else:
            SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable where AnPointID = '" + AnalysisPoint + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        #print UserPFPListFilePath
        temp_listdb_con = sqlite3.connect( UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        for UserRow in UserResultRows:
            if  "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:
                ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
                    
                    
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
          
          
          
        idx = 0 
        for Row in ResultRows:
            
            """행 삽입"""
            InsertString = ""
            try:
                UtilClass = Util()
                InsertString = UtilClass.DummyCyber(self.GetGrandParent().GetGrandParent().GetGrandParent().GetGrandParent().DecodedDummy, "", Row[0])
            except:
                InsertString = Row[0]
            
                
            self.InsertStringItem(idx, InsertString)
            self.SetStringItem(idx, 1, Row[1])
                
            
            
            
            
            """행 색상, 아이콘 세팅"""
            if int(Row[1]) > 500000 :
                self.SetItemBackgroundColour(idx, '#e6f1f5')
                if "[*]" in InsertString:
                    self.SetItemColumnImage(idx,0, 2)
                elif "[+]" in InsertString:
                    self.SetItemColumnImage(idx,0, 3)
                if "[-]" in InsertString:
                    self.SetItemColumnImage(idx,0, 4)
                if "[RegKey]" in InsertString:
                    self.SetItemColumnImage(idx,0, 5)
                
            elif "[*]" in InsertString:
                self.SetItemColumnImage(idx,0, 2)
                self.SetItemBackgroundColour(idx, '#fdf5e6')
            elif "[+]" in InsertString:
                self.SetItemColumnImage(idx,0, 3)
            elif "[-]" in InsertString:
                self.SetItemColumnImage(idx,0, 4)
            if "[RegKey]" in InsertString:
                    self.SetItemColumnImage(idx,0, 5)
                
            idx +=1
                        
        
        temp_listdb_con.close()        
        

      
                            
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_TAB and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                windowAnalysisDescription = self.parent.GetGrandParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                windowAnalysisDescription.SetFocus()
                if windowAnalysisDescription.GetFocusedItem() == -1:
                    windowAnalysisDescription.Select(0)
                
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                windowAnalysisDescription = self.parent.GetGrandParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
                windowAnalysisDescription.SetFocus()
                if windowAnalysisDescription.GetFocusedItem() == -1:
                    windowAnalysisDescription.Select(0)
                            
class RelatedToolsForAcquisitionList(wx.ListCtrl):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)

        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.InsertColumn(0, '')


    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()
        
    def OnActivated(self, event):

        window = self.parent.GetGrandParent().GetGrandParent().GetGrandParent().FindWindowByName('ModuleListOnList')
        Keyword = event.GetText()
        if "[Public]" in Keyword or "[UserDefine]" in Keyword:
            window.FindModuleByName(Keyword.strip("\n").strip("\t").strip("\r"))
        else:
            if len(Keyword.split(" ")) > 1:
                window.FindModuleByName(Keyword.split(" ")[0].strip("\n").strip("\t").strip("\r"), Keyword.replace(Keyword.split(" ")[0]+" ", ""))
            else:
                window.FindModuleByName(Keyword.split(" ")[0].strip("\n").strip("\t").strip("\r"))
    
        return 

    def LoadData(self, PFPListFilePath, Category, AnalysisPoint, VestigeLocation):
        
        
        self.PFPListFilePath = PFPListFilePath
        self.NowCategory = Category
        self.AnalysisPoint = AnalysisPoint
        
        #for i in range(0,100):
        self.DeleteAllItems()#.DeleteItem(0)

        temp_listdb_con = sqlite3.connect( self.PFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select AcquiTools from VesLocationTable where ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        ResultText = temp_listdb_cursor.fetchone()[0]
        
        try:
            UtilClass = Util()
            ResultText = UtilClass.DummyCyber(self.parent.GetGrandParent().GetGrandParent().GetGrandParent().GetParent().DecodedDummy, "", ResultText)
        except:
            ResultText = ResultText
        
        if ResultText != None:
            
            ResultRows = ResultText.split("\t")
            
            idx = 0 
            for Row in ResultRows:
                if Row.strip() != "":
                    
                    self.InsertStringItem(idx, Row)
                    idx +=1
                
        temp_listdb_con.close()

   
                                    
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_TAB and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetGrandParent().GetGrandParent().GetGrandParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
                window.SetFocus()
                if window.GetFocusedItem() == -1:
                   window.Select(0)
                
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetGrandParent().GetGrandParent().GetGrandParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                window.SetFocus()
                if window.GetFocusedItem() == -1:
                   window.Select(0)
                
            
class AnalysisDescriptionList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)

        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.InsertColumn(0, '')


    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()

    def LoadData(self, PFPListFilePath, Category, AnalysisPoint, VestigeLocation):
        
        
        self.PFPListFilePath = PFPListFilePath
        self.NowCategory = Category
        self.AnalysisPoint = AnalysisPoint
        
        #for i in range(0,100):
        self.DeleteAllItems()#.DeleteItem(0)

        temp_listdb_con = sqlite3.connect( self.PFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Description from VesLocationTable where ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        ResultText = temp_listdb_cursor.fetchone()[0]
        
        try:
            UtilClass = Util()
            ResultText = UtilClass.DummyCyber(self.parent.GetGrandParent().GetGrandParent().GetGrandParent().DecodedDummy, "", ResultText)
        except:
            ResultText = ResultText
        
        if ResultText != None:
            
            ResultRows = ResultText.split("\t")
            
            idx = 0 
            for Row in ResultRows:
                if Row.strip() != "":
                    
                    self.InsertStringItem(idx, Row)
                        
                    idx +=1
            
        temp_listdb_con.close()
        
                      
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_TAB and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetGrandParent().GetGrandParent().GetGrandParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                window.SetFocus()
                if window.GetFocusedItem() == -1:
                   window.Select(0)
                
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetGrandParent().GetGrandParent().GetGrandParent().GetParent().FindWindowByName('VestigeLocationOnList')
                window.SetFocus()
                if window.GetFocusedItem() == -1:
                   window.Select(0)
                
            

#---code for module list
class ModuleListList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    
    #list Checkbox example - http://zetcode.com/wxpython/advanced/
    ExecuteStatus = ""
    FilePath = ""
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
    
        self.OS = ""
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/download_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Unit_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Commercial_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/EmptyModule_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/gui_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/cli_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/EmptyPrivateModule.png',
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
    
        self.SelectedArgument = ""
        self.ExecuteStatus = "AllModule"
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent()

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)
        #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListCtrlColClick)
        self.sortedCol = -1

        self.InsertColumn(0, 'Module Name')
        self.InsertColumn(1, 'Author')
        self.InsertColumn(2, 'Description')
        self.InsertColumn(3, '>')
        self.InsertColumn(4, 'Version')
        self.InsertColumn(5, 'Last modify time')
        self.InsertColumn(6, 'ModulePath')
        
        SelfTest = PFPUtil()
        
        Platform = sys.platform
        
        
        SelectQuery = ''
        if 'win32' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID, DownLoadName from ModuleList where (OS = 'win' or OS = 'python' or OS = 'wincmd') and isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        elif 'darwin' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID, DownLoadName from ModuleList where OS = 'mac' order by ModuleName COLLATE NOCASE;"
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[1] = lst[1] + " - [User Define]"
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        #Merge and sort
        ###############
        
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        idx = 0
        if self.MainFrame.isPremium == True:
            self.InsertStringItem(idx, "[*]PFPModules")
            self.SetItemBackgroundColour(idx, '#fdf5e6')
            self.SetItemColumnImage(idx,0, 9)
            idx += 1        
            for row in MergedResultList:
                if 'pfpmodule' in row[9].lower():
                    idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8], True )
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
            
            self.InsertStringItem(idx, "[*]3rd party Forensic Modules")
            self.SetItemBackgroundColour(idx, '#fdf5e6')
            self.SetItemColumnImage(idx,0, 9)
            idx += 1        
        for row in MergedResultList:
            if 'pfpmodule' not in row[9].lower():
                idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8] )
            
            
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 130)
        self.SetColumnWidth(1, 80)
        self.SetColumnWidth(2, 300)
        self.SetColumnWidth(3, 0)
        self.SetColumnWidth(4, 0)
        self.SetColumnWidth(5, 130)
        self.SetColumnWidth(6, size.x-5)
        
        
        dt = FileDropTarget(self._insert)
        self.SetDropTarget(dt)
        
        self.DragAndDropFlag = False
        
        
    def OnListCtrlColClick(self, event):
        col = event.GetColumn()
        index = event.GetIndex()
        if self.sortedCol == col:
            self.itemList.reverse()
        else:
            self.itemList.sort(key=index)
            self.sortedCol = col
            
        self.loadList()

        
        
    def _insert(self, x, y, filenames):
        """ Insert text at given x, y coordinates --- used with drag-and-drop. """

        self.DragAndDropFlag = True
        
        self.DropedFile = filenames[0]
        
        self.FileSelect()
        
        self.DragAndDropFlag = False
        
         
        
        return

    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        ModulePath = self.GetItem(event.GetIndex(),6).GetText()
        
        ParentWindow = self.MainFrame
        
        PopupMenu = wx.Menu()        
        if os.path.isfile(ModulePath):
            try:
                PopupMenu.Append(-1, "File Version : " + calcversioninfo(ModulePath))
            except:
                PopupMenu.Append(-1, "File Version : no information")
            PopupMenu.AppendSeparator()
            
        OpenHomePage  = PopupMenu.Append(-1, "Open homepage")           
        FolderOpen = PopupMenu.Append(-1, "Folder open")             
        ModifyModule  = PopupMenu.Append(-1, "Modify the module")
        PopupMenu.AppendSeparator()
        
        colour = self.GetItemBackgroundColour(event.GetIndex()) 
        if colour == '#e6f1f5':
            InsertModule  = PopupMenu.Append(-1, "Import new module")
            self.Bind(wx.EVT_MENU, ParentWindow.OnInsert, InsertModule)
        else:
            InsertModuleUseReference  = PopupMenu.Append(-1, "Import new module, by using this reference")
            self.Bind(wx.EVT_MENU, ParentWindow.OnInsertUseReference, InsertModuleUseReference)
            
        if self.ExecuteStatus == "Recycle":
            RecoverModules  = PopupMenu.Append(-1, "Recover selected modules")
            self.Bind(wx.EVT_MENU, ParentWindow.OnRecover, RecoverModules)
        else :
            DeleteModules  = PopupMenu.Append(-1, "Delete selected modules")
            self.Bind(wx.EVT_MENU, ParentWindow.OnDelete, DeleteModules)
        #DownloadModules  = PopupMenu.Append(-1, "Download selected modules")              
        
        
        self.Bind(wx.EVT_MENU, ParentWindow.OnHomePageOpen, OpenHomePage)
        self.Bind(wx.EVT_MENU, ParentWindow.OnFolderOpen, FolderOpen)
        self.Bind(wx.EVT_MENU, ParentWindow.OnModyfy, ModifyModule)
        #self.Bind(wx.EVT_MENU, ParentWindow.OnInsert, InsertModule)
        #self.Bind(wx.EVT_MENU, ParentWindow.OnModuleDownload, DownloadModules)
        
    
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPoint())

    def OnSize(self, event):
        
        event.Skip()
        
    def OnActivated(self, event=None, Argument=""):
        
        index = 0 
        if event != None:
            index = event.GetIndex()
        
        #---cli Arguments is activated.. 
        if self.ExecuteStatus == "Cli Argument":
            #self.parent.GetParent().GetParent().GetParent().GetParent().tc7.Clear() 
            #self.parent.GetParent().GetParent().GetParent().GetParent().tc7.AppendText("#")
            
            #self.parent.GetParent().GetParent().GetParent().GetParent().tc7.AppendText(self.GetItem(index,0).GetText().lower() + " ")
            
            InputArgument = ""
            
            if Argument == "":  InputArgument = self.GetItem(index,2).GetText()
            else: InputArgument = Argument
            
            ResultArgument = "\"" + self.GetItem(index,6).GetText() + "\" "

            SplittedInput = InputArgument.split(" ")
            
            for Token in SplittedInput:
                                 
                if '%DIR' in Token:
                    SubToken = Token.split(":")[1].split("%")
                    RemainStr = ""
                    Message = SubToken[0]
                    if len(SubToken) > 1:
                        RemainStr = SubToken[1]
                    dlg = wx.DirDialog(self, message="Select target dir for " + Message, defaultPath=os.getcwd(), style=wx.OPEN)
                    
                    SelectedDrive = ""
                    if dlg.ShowModal() == wx.ID_OK:                    
                        SelectedDrive = dlg.GetPath()
                    
                    ResultArgument += "\""
                    ResultArgument += SelectedDrive.replace("/", "\\") #Token.replace("%DIR%", SelectedDrive.replace("/", "\\"))
                    ResultArgument += RemainStr
                    ResultArgument += "\""
                    ResultArgument += " "
                    
                elif '%FILE' in Token:
                    SubToken = Token.split(":")[1].split("%")
                    RemainStr = ""
                    Message = SubToken[0]
                    if len(SubToken) > 1:
                        RemainStr = SubToken[1]
                    
                    dlg = wx.FileDialog(self, message="Select target file for " + Message, defaultFile="", style=wx.OPEN)
        
                    SelectedFile = ""
                    if dlg.ShowModal() == wx.ID_OK:
                        SelectedFile = dlg.GetPath()

                    ResultArgument += "\""
                    ResultArgument += SelectedFile.replace("/", "\\") #Token.replace("%FILE%", SelectedFile.replace("/", "\\"))
                    ResultArgument += RemainStr
                    ResultArgument += "\""
                    ResultArgument += " "
                    
                else:
                    ResultArgument += Token
                    ResultArgument += " "
                """
                elif '%NUM%' in InputArgument:
                    ArgumentSetting = InputArgument.replace("%NUM%", Number)
                    
                elif '%TEXT%' in InputArgument:
                    ArgumentSetting = InputArgument.replace("%TEXT%", Number)
                """
                
            if "python" in self.OS.lower():
                ResultArgument = "\"" + self.MainFrame.interpreter_path + "\"" + " " + ResultArgument
            
            ResultArgument = ResultArgument.replace(" None ", "")
            ResultArgument = ResultArgument.replace(" None", "")
            ResultArgument = ResultArgument.replace("None", "")
            
            PFPUtil().Copy_to_Clipboard(ResultArgument)
            #wx.MessageBox("Copy to clipboard : " + ResultArgument)
            
            dlg = wx.MessageDialog(None, "Open new terminal?\n\nCopy to clipboard : " + ResultArgument, 'Info', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                os.system("start")
            
            #os.system("start")
            
            #self.parent.GetParent().GetParent().GetParent().GetParent().tc7.AppendText(ResultArgument)
            self.ExecuteStatus == "None"
            
            return
        
        
        
        colour = self.GetItemBackgroundColour(index) 
        DBFilePath = ""
        if colour == '#e6f1f5':
            DBFilePath = self.MainFrame.default_user_modulelistDB_path
        elif colour == '#f3f3ff':
            DBFilePath = self.MainFrame.default_modulelistDB_path
        else : 
            DBFilePath = self.MainFrame.default_modulelistDB_path
            wx.MessageBox("Can not launch the reference(white background) module.")
            return
        
        
        
        
        ContentsID = self.GetItem(index,3).GetText() #event.GetText().strip("[#]")
        
        con = sqlite3.connect( DBFilePath )
        cursor = con.cursor()
        
        SelectQuery = "select ModuleName, ModulePath, ExecuteCount, ExecutableType, OS, Author, UsedStatus, ContentsID from ModuleList where ContentsID = '" + ContentsID + "';"
        
        
        #print SelectQuery
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchone()
        
        con.close()
        
        if "cli" in ResultList[3].lower():
        #CLI Module
            
            if "y" == ResultList[6].lower():
            
                con = sqlite3.connect( DBFilePath )
                cursor = con.cursor()
            
                SelectQuery = "select ContentsID from ModuleList where ModuleName = '" + ResultList[0] + "';"
                cursor.execute( SelectQuery )
                ModuleIDRow = cursor.fetchone()
    
                if "python" in ResultList[4].lower():
                    self.CliArgument(str(ModuleIDRow[0]), ResultList[0], ResultList[5], ResultList[1], "python")
                else:    
                    self.CliArgument(str(ModuleIDRow[0]), ResultList[0], ResultList[5], ResultList[1], "")
    
                con.close()  
            
            else:
                UtilClass = Util()
                
                if self.ExecuteStatus == "File":
                    UtilClass.ModuleExecute(ResultList[0], ResultList[1], ResultList[2], DBFilePath, self.MainFrame.DecodedDummy, self.FilePath)
                else:
                    UtilClass.ModuleExecute(ResultList[0], ResultList[1], ResultList[2], DBFilePath, self.MainFrame.DecodedDummy, "")
              
        
        else:
        #GUI Module
            UtilClass = Util()
            
            if self.ExecuteStatus == "File":
                UtilClass.ModuleExecute(ResultList[0], ResultList[1], ResultList[2], DBFilePath, self.MainFrame.DecodedDummy, self.FilePath)
            else:
                UtilClass.ModuleExecute(ResultList[0], ResultList[1], ResultList[2], DBFilePath, self.MainFrame.DecodedDummy, "")        
            
    def ListInsert(self, idx, UsedStatus, ModuleName, Author, Description, ModulePath, ExecutableType, ContentsID, isPFPModule = False):
        
        UtilClass = Util()
        rootParent = self.MainFrame
        #print rootParent.EncodedKey
        #print rootParent.DecodedDummy
        isPublic = 'y'
        
        
        #about private list .. 
        if (rootParent.isPFPOnManaging == False) and ContentsID != "None":
            SelectQuery = "select isPublic from ModuleList where ContentsID = '" + ContentsID + "'"
            
            DBPath = ""
            if int(ContentsID) >= 500000:
                DBPath = rootParent.default_user_modulelistDB_path
            else:
                DBPath = rootParent.default_modulelistDB_path
                
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            try:
                isPublic = cursor.fetchone()[0]
            except:
                isPublic = 'n'
            
        if isPublic == 'n' and self.ExecuteStatus != 'Cli Argument':
            #print ModuleName
            #print SelectQuery
            #print 
            return idx
            
        if rootParent.ReferenceViewMode == False: 
            if " - [User Define]" in Description or self.ExecuteStatus == 'Cli Argument' or isPFPModule == True:
                Dummycode = 0
            else:
                return idx
        
        try:
            if " - [User Define]" in Description:
                Description = UtilClass.DummyCyber(rootParent.DecodedDummy, "", Description.replace(" - [User Define]", "")) + " - [User Define]"
            else:
                Description = UtilClass.DummyCyber(rootParent.DecodedDummy, "", Description)
        except:
            Description = Description
            
        try:
            Author = UtilClass.DummyCyber(rootParent.DecodedDummy, "", Author)
        except:
            Author = Author
            
        try:
            UsedStatus = UtilClass.DummyCyber(rootParent.DecodedDummy, "", UsedStatus)
        except:
            UsedStatus = UsedStatus    
            
            
        if UsedStatus != "y":
            
            self.InsertStringItem(idx, ModuleName)
            self.SetStringItem(idx, 1, Author)
            self.SetStringItem(idx, 2, Description)
            self.SetStringItem(idx, 3, ContentsID)
            self.SetStringItem(idx, 4, "")
            try:
                filemtime = datetime.datetime.fromtimestamp(os.path.getmtime(ModulePath)).strftime('%y/%m/%d %H:%M')
                self.SetStringItem(idx, 5, str(filemtime))  #and can use getatime & getctime
            except:
                self.SetStringItem(idx, 5, "")
            self.SetStringItem(idx, 6, ModulePath)
            
            if "have to buy" in UsedStatus:
            
                self.SetItemColumnImage(idx,2, 4)
            
            elif "can auto download" in UsedStatus:
                
                self.SetStringItem(idx, 0, ModuleName+"[#]")
                self.SetItemColumnImage(idx,2, 2)
            
            elif "have to download directly with license agreement" in UsedStatus or "have to download directly (not compatible with auto download system)" in UsedStatus :
                
                self.SetItemColumnImage(idx,2, 5)
                
            elif "is empty" in UsedStatus :
                
                self.SetItemColumnImage(idx,2, 8)
                
            #else: 
            #    self.SetItemColumnImage(idx,2, 7)
                
        else : 
            
            self.InsertStringItem(idx, ModuleName)
            self.SetStringItem(idx, 1, Author)
            self.SetStringItem(idx, 2, Description)
            self.SetStringItem(idx, 3, ContentsID)
            self.SetStringItem(idx, 4, "")
            try:
                #print time.localtime()
                #print os.path.getmtime(ModulePath)
                #print datetime.datetime.fromtimestamp(os.path.getmtime(ModulePath)).strftime('%y/%m/%d %H:%M:%S')
                #print time.ctime(os.path.getmtime(ModulePath))
                filemtime = datetime.datetime.fromtimestamp(os.path.getmtime(ModulePath)).strftime('%y/%m/%d %H:%M')
                self.SetStringItem(idx, 5, str(filemtime))  #and can use getatime & getctime
            except:
                self.SetStringItem(idx, 5, "")
            self.SetStringItem(idx, 6, ModulePath)
            
        if ExecutableType == "gui":
            self.SetItemColumnImage(idx, 2, 6)
            self.SetItemColumnImage(idx, 3, 6)
        else:     
            self.SetItemColumnImage(idx, 2, 7)
            self.SetItemColumnImage(idx, 3, 7) 
            
        if " - [User Define]" in Description:
            self.SetItemBackgroundColour(idx, '#e6f1f5')
        elif rootParent.ReferenceViewMode == False and " - [User Define]" not in Description:
            self.SetItemBackgroundColour(idx, '#f3f3ff')
            
        idx += 1
        
        #Check!!140512
        #self.threads = []
        #th = threading.Thread(target=self.ThreadModuleVersion, args=())
        #th.start()
        #self.threads.append(th)
        
        
        return idx

    def FindModuleByName(self, Keyword, Argument = ""):
        
        rootParent = self.MainFrame
            
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        #print Keyword
        
        if "[Public]" in Keyword or "[UserDefine]" in Keyword:
        
            rootParent.category_combo.Replace(0, len(rootParent.category_combo.GetValue()), Keyword) 
        
            window = rootParent.FindWindowByName('ModuleListOnList')
            window.CategorySelected()
            
            StatusWindow = rootParent.FindWindowByName('ModuleStatusbar')
            StatusWindow.SetLine("Category : " + Keyword )
            
        else:
        
            self.ExecuteStatus = "Find Module By Name"
            
            #for i in range(0,500):
            self.DeleteAllItems()#.DeleteItem(0)
            
            Platform = sys.platform
            
            
            
            SelectQuery = ''
            if 'win32' in Platform:
                SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID from ModuleList where (OS = 'win' or OS = 'python' or OS = 'wincmd') and isDeleted = '0' order by ModuleName COLLATE NOCASE;"
            elif 'darwin' in Platform:
                SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID from ModuleList where OS = 'mac' order by ModuleName COLLATE NOCASE;"
            
            
            #Get From User DB
            ##############
            con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            UserResultList = cursor.fetchall()
            
            idx = 0
            for row in UserResultList:
                lst = list(row)
                lst[1] = lst[1] + " - [User Define]"
                UserResultList[idx] = tuple(lst) 
                idx += 1
            
            con.close()
            
            #Get From Public DB
            ################
            con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            PublicResultList = cursor.fetchall()
            
            con.close()
            
            #Merge and sort
            ###############
            MergedResultList = UserResultList + PublicResultList
            MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
            
            Searchidx = 0
            User_idx = 0
            UserModuleType = []
            SearchModuleNameList = []
            SearchExcuteReadyPathList = []
            SearchExcuteCountList = []
            
            UtilClass = Util()
            
            #print Keyword.lower()
            for row in MergedResultList:
                #print row[0].lower()
                if Keyword.lower().strip() in row[0].lower().strip():
                    SearchModuleNameList.append(row[0])
                    SearchExcuteReadyPathList.append(row[2])
                    SearchExcuteCountList.append(row[3])
                    
                    Searchidx = self.ListInsert(Searchidx, row[5], row[0], row[6], row[1], row[2], row[4], row[8] )
                    if " - [User Define]" in row[1]:
                        User_idx += 1
                        UserModuleType.append(row[4])
                        
            #print User_idx
            if Searchidx == 0:
                wx.MessageBox("There is no related module in your platform")
            
            elif User_idx == 1:
                #print SearchExcuteReadyPathList[0]
                #UtilClass.ModuleExecute(SearchModuleNameList[0], SearchExcuteReadyPathList[0], SearchExcuteCountList[0], rootParent.default_modulelistDB_path, rootParent.DecodedDummy, "")
                self.OnActivated()
                
                if self.ExecuteStatus == "Cli Argument":
                    
                    if Argument == "": Argument = "None"
                    self.OnActivated(Argument=Argument)
            

    def FileSelect(self, FilePath = "None"):
        
        self.ExecuteStatus = "File"
        
        
        Platform = sys.platform
        SelfTest = PFPUtil()
        
        
        
        SelectedFile = ""
        
        if FilePath == "None":
            
            dlg = wx.FileDialog(self, message="Select Target File", defaultFile="", style=wx.OPEN)
            
            if self.DragAndDropFlag == False:
            
                if dlg.ShowModal() == wx.ID_OK:
                    SelectedFile = dlg.GetPath()
                    
            else:
                SelectedFile = self.DropedFile
                
        else:
            SelectedFile = FilePath
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        Signature = "None"
        
        if os.path.isfile(SelectedFile):
            
            fp = open(SelectedFile)
            Hex = fp.read(2)
            Signature = SelfTest.HexValue_to_HexString(Hex)
            if Signature.strip() == "":
                Signature = "can not read.(system file or not existed)"
            fp.close()
            
        SplitedList = SelectedFile.split('.')
        extender = SplitedList[len(SplitedList)-1] 
        
       
        # set dedicated list 
        SelectQuery = ''
        if 'win' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, TargetExtender, TargetSignature, ContentsID, DownLoadName from ModuleList where (OS = 'win' or OS = 'python' or OS = 'wincmd') and isDeleted = '0' order by ExecuteCount desc"
        if 'darwin' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, TargetExtender, TargetSignature, ContentsID, DownLoadName from ModuleList where OS = 'mac' order by ExecuteCount desc"
        
        
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[1] = lst[1] + " - [User Define]"
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        
        
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        
        
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        
        
                    
        #for i in range(0,500):
        self.DeleteAllItems()#.DeleteItem(0)
        
        
        
    
        #set common list
        idx = 0
        self.InsertStringItem(idx, "[*]File related modules")
        self.SetItemBackgroundColour(idx, '#fdf5e6')
        self.SetItemColumnImage(idx,0, 9)
        idx += 1
        
        
        UtilClass = Util()
        rootParent = self.MainFrame
        
        
        #특정 확장자에만 매치되는 모듈을 머지 리스트에 추가
        """
        if self.MainFrame.isPremium == True:
            for row in MergedResultList:
                if "pfpmodule" in row[11].lower() and (extender in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8]) or str(Signature) in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[9])):
                    idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[10], True )
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
        """
        
        for row in MergedResultList:
            if extender in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8]) or str(Signature) in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[9]):
                if self.MainFrame.isPremium == False and "pfpmodule" in row[11].lower():    #프리미엄이 아닐 때는, PFPModule로 설정된건 띄우지 않기 
                    continue
                idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[10] )
                if 'pfpmodule' in row[11].lower():
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
                
        
        #allfile 이나 *라고 적혀있는 파일... 추가 ㅎ 
        #set common list
        self.InsertStringItem(idx, "[*]Common modules")
        self.SetItemBackgroundColour(idx, '#fdf5e6')
        self.SetItemColumnImage(idx,0, 9)
        idx += 1        
        
        """
        if self.MainFrame.isPremium == True:
            for row in MergedResultList:
                if "pfpmodule" in row[11].lower() and ('all' in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8]) or '*' in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8])):
                    idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[10], True )
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
        """
        
        for row in MergedResultList:
            if 'all' in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8]) or '*' in UtilClass.DummyCyber(rootParent.DecodedDummy, "", row[8]):
                if self.MainFrame.isPremium == False and "pfpmodule" in row[11].lower():    #프리미엄이 아닐 때는, PFPModule로 설정된건 띄우지 않기 
                    continue
                idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[10] )
                if 'pfpmodule' in row[11].lower():
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
    
        if FilePath == "None":
            SelfTest.Copy_to_Clipboard(SelectedFile)
        
        self.FilePath = SelectedFile
    
        
        
        return

    def AllModule(self):
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        self.ExecuteStatus = "AllModule"
        
        #for i in range(0,500):
        self.DeleteAllItems()
        #self.ClearAll()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        SelfTest = PFPUtil()
        
        Platform = sys.platform
        
        SelectQuery = ''
        if 'win32' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID, DownLoadName from ModuleList where (OS = 'win' or OS = 'python' or OS = 'wincmd') and isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        elif 'darwin' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID, DownLoadName from ModuleList where OS = 'mac' and isDeleted = '0'  order by ModuleName COLLATE NOCASE;"
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[1] = lst[1] + " - [User Define]"
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        #set common list
        idx = 0
        #프리미엄일 경우에만 PFP 모듈 존재 확인 및 구동
        if self.MainFrame.isPremium == True:
            self.InsertStringItem(idx, "[*]PFPModules")
            self.SetItemBackgroundColour(idx, '#fdf5e6')
            self.SetItemColumnImage(idx,0, 9)
            idx += 1        
            for row in MergedResultList:
                if 'pfpmodule' in row[9].lower():
                    idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8], True )
                    self.SetItemBackgroundColour(idx-1, '#f3f3ff')
            
            self.InsertStringItem(idx, "[*]3rd party Forensic Modules")
            self.SetItemBackgroundColour(idx, '#fdf5e6')
            self.SetItemColumnImage(idx,0, 9)
            idx += 1             
        for row in MergedResultList:
            if 'pfpmodule' not in row[9].lower():
                idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8] )
        
        self.SortItems(wx.LC_SORT_ASCENDING)
        #LC_SORT_ASCENDING: Sort in ascending order. (You must still supply a comparison callback in ListCtrl.SortItems .)
        #LC_SORT_DESCENDING

            
    def CliArgument(self, ModuleID, ModuleName, Author, ModulePath, OS):
        
        """
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 300)
        self.SetColumnWidth(1, 0)
        self.SetColumnWidth(2, size.x-5)
        self.SetColumnWidth(3, 0)
        """
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        self.ExecuteStatus = "Cli Argument"
        if "python" in OS.lower():
            self.OS = "python"
        else:
            self.OS = ""
        
        #for i in range(0,500):
        self.DeleteAllItems()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        SelfTest = PFPUtil()
        
        Platform = sys.platform
        
        
        SelectQuery = "select Argument, ArgumentDescription, ContentsID from ArgumentList where ModuleID = '" + ModuleID + "'"

        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[1] = lst[1] + " - [User Define]"
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        
        idx = 0
        if len(MergedResultList) == 0:
            idx = self.ListInsert(idx, '', ModuleName, Author, "None", ModulePath, "cli", "None")
            
        else:
            for row in MergedResultList:  
                idx = self.ListInsert(idx, '', ModuleName, Author, row[0], ModulePath, "cli", row[2])
            
    def CategorySelected(self):
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        self.ExecuteStatus = "CategorySelected"
        
        #for i in range(0,500):
        self.DeleteAllItems()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        SelfTest = PFPUtil()
        
        Platform = sys.platform
        
        SelectedText = rootParent.category_combo.GetValue()
        DBPath = ""
        
        #print SelectedText
        
        UtilClass = Util()
        rootParent = self.MainFrame
        
        
        if "[Public]" in SelectedText:
            DBPath = rootParent.default_modulelistDB_path
            SelectedText = SelectedText.replace("[Public] ", "")
        elif "[UserDefine]" in SelectedText:
            DBPath = rootParent.default_user_modulelistDB_path
            SelectedText = SelectedText.replace("[UserDefine] ", "")
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select ModuleIDs from ModuleCategory where CategoryName = '" + SelectedText + "' COLLATE NOCASE;"
        
        cursor.execute( SelectQuery )
        ModuleIDs = cursor.fetchone()
        
        try:
            ModuleIDs = UtilClass.DummyCyber(rootParent.DecodedDummy, "", ModuleIDs[0])
        except:
            ModuleIDs = ModuleIDs[0]
        
        con.close()
        
        #Tokens = #str(ModuleIDs).strip('u()\'').split(",")
        Tokens = ModuleIDs.split(",")
        
        #print str(ModuleIDs).strip('u()\'')
        #print Tokens
               
        SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID, DownLoadName from ModuleList where"
        
        QueryMakeFlag = False
        
        for ModuleID in Tokens:
            try:
                float(ModuleID)
                SelectQuery += " or ContentsID = "
                SelectQuery += ModuleID
            
                QueryMakeFlag = True
            except ValueError:
                continue
                
        if QueryMakeFlag == True:
                
            SelectQuery = SelectQuery.replace("where or", "where")
            SelectQuery += " order by ModuleName COLLATE NOCASE"
            
            #print SelectQuery 
            
            #print SelectQuery
            
            #Get From User DB
            ##############
            con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
            cursor = con.cursor()
            
            #print SelectQuery
            cursor.execute( SelectQuery )
            UserResultList = cursor.fetchall()
            
            
            
            idx = 0
            for row in UserResultList:
                lst = list(row)
                lst[1] = lst[1] + " - [User Define]"
                UserResultList[idx] = tuple(lst) 
                idx += 1
            
            con.close()
            
            
            
            #Get From Public DB
            ################
            con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            PublicResultList = cursor.fetchall()
            
            con.close()
            
            #Merge and sort
            ###############
            MergedResultList = UserResultList + PublicResultList
            MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
            
            #set common list
            idx = 0
            if self.MainFrame.isPremium == True:
                self.InsertStringItem(idx, "[*]PFPModules")
                self.SetItemBackgroundColour(idx, '#fdf5e6')
                self.SetItemColumnImage(idx,0, 9)
                idx += 1        
                for row in MergedResultList:
                    if 'pfpmodule' in row[9].lower():
                        idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8], True )
                        self.SetItemBackgroundColour(idx-1, '#f3f3ff')
                
                self.InsertStringItem(idx, "[*]3rd party Forensic Modules")
                self.SetItemBackgroundColour(idx, '#fdf5e6')
                self.SetItemColumnImage(idx,0, 9)
                idx += 1     
            for row in MergedResultList:
                if 'pfpmodule' not in row[9].lower():  
                    idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8]) 
            
    def ModuleImport(self, ResultList):
        
        self.ExecuteStatus = "Select Module to import"
        
        self.DeleteAllItems()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        idx = 0
        for row in ResultList:
            self.InsertStringItem(idx, row[0])
            self.SetStringItem(idx, 1, row[1])
            self.SetStringItem(idx, 2, row[2])
            #print '\t['+str(idx) +'].'+row[0]+'('+row[1]+')' 
            idx += 1
            
    def UnitModule(self):
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Enable()
        rootParent.Modyfy.Enable()
        rootParent.Delete.Enable()
        rootParent.Recover.Disable()
        rootParent.ShareExport.Enable()
        rootParent.ShareImport.Enable()
        rootParent.ModuleDownload.Enable()
        
        UnitInst = UnitModules()
        
        self.ExecuteStatus = "Unit Module"
        
        self.DeleteAllItems()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        UnitList = UnitInst.GetList()
        
        idx = 0
        for module in UnitList:
            self.InsertStringItem(idx, "[Unit] " + module[0])
            self.SetStringItem(idx, 1, "by " + module[1]) 
            self.SetItemImage(idx, 3)
            idx += 1  
            
    def Recycle(self):
        
        rootParent = self.MainFrame
        
        rootParent.Insert.Disable()
        rootParent.Modyfy.Disable()
        rootParent.Delete.Disable()
        rootParent.Recover.Enable()
        rootParent.ShareExport.Disable()
        rootParent.ShareImport.Disable()
        rootParent.ModuleDownload.Disable()
        
        self.ExecuteStatus = "Recycle"
        
        self.DeleteAllItems()
        #for i in range(0,500):
        #    self.DeleteItem(0)
        
        SelfTest = PFPUtil()
        
        Platform = sys.platform
        
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = ''
        if 'win32' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID from ModuleList where (OS = 'win' or OS = 'python' or OS = 'wincmd') and isDeleted = '1' order by ModuleName COLLATE NOCASE;"
        elif 'darwin' in Platform:
            SelectQuery = "select ModuleName, Description, ModulePath, ExecuteCount, ExecutableType, UsedStatus, Author, DownLoadLink, ContentsID from ModuleList where OS = 'mac' and isDeleted = '1'  order by ModuleName COLLATE NOCASE;"
        
        
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.MainFrame.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[1] = lst[1] + " - [User Define]"
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.MainFrame.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        idx = 0
        for row in MergedResultList:
            
            idx = self.ListInsert(idx, row[5], row[0], row[6], row[1], row[2], row[4], row[8] )
            
            
    def ThreadModuleVersion(self):
    
        for index in range(self.GetItemCount()):
            
            ModulePath = self.GetItem(index, 6).GetText()
            
            try:
                self.SetStringItem(index, 4, calcversioninfo(ModulePath))
            except:
                self.SetStringItem(index, 4, "")
        
        return
                

#---code for some status bar
class Statusbar(wx.TextCtrl):
    
    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, id)
        
        self.parent = parent
        self.SetEditable(0)
        self.WriteText('status')
        
        return 

    def SetLine(self, Log):
        
        self.Clear()
        self.WriteText(Log)
        
        return


class VestigeLocationStatusbar(wx.TextCtrl):
    
    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, id)
        
        self.parent = parent
        self.SetEditable(0)
        self.WriteText('-*-')
        
        return 

    def SetLine(self, Log):
        
        self.Clear()
        self.WriteText(Log)
        
        return
    
class RelatedWebPageStatusbar(wx.TextCtrl):
    
    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, id)
        
        self.parent = parent
        self.SetEditable(0)
        self.WriteText('http://portable-forensics.com')
        
        return 

    def SetLine(self, Log):
        
        self.Clear()
        self.WriteText(Log)
        
        return

#---code for PFP Application(Tab control)
class SearchResult(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()    
        
        #print self.MainFrame.default_pfplist_path

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        self.InsertColumn(0, 'Location')
        self.InsertColumn(1, 'Result')
        self.InsertColumn(2, 'ContentsPath')
        
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 130)
        self.SetColumnWidth(1, size.x-5)
        self.SetColumnWidth(2, 0)

    def OnSize(self, event):
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 130)
        self.SetColumnWidth(1, size.x-5)
        self.SetColumnWidth(2, 0)
        event.Skip()
        
        return
        
    def OnActivated(self, event):

        Location = self.GetItem(event.GetIndex(),0).GetText()
        ResultString = self.GetItem(event.GetIndex(),1).GetText()
        ContentsPath = self.GetItem(event.GetIndex(),2).GetText()
        
        Tokens = ContentsPath.split("[Token]")
        #wx.MessageBox(Tokens[0] + " _ " + Tokens[1] + " _ " + Tokens[2]) 
        
        DBPath = Tokens[0]
        Query = Tokens[1]
        ContentsID = Tokens[2]
        

        window0 = self.MainFrame.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.MainFrame.FindWindowByName('AnalysisPointOnList')
        window2 = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window3 = self.MainFrame.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.MainFrame.FindWindowByName('AnalysisDescriptionOnList')
        Modulewindow = self.MainFrame.FindWindowByName('ModuleListOnList')
        #window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        

        if Location == "Category":
        
            self.MainFrame.public_pfplist_path = DBPath
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
                        
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == ContentsID.strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
                
        elif Location == "Analysis Point":
            
            self.MainFrame.public_pfplist_path = DBPath
            
            #GetParentIds...
            ################
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + ContentsID + "'")
            ResultRow = cursor.fetchone()
            
            CategoryID = ResultRow[0]
            
            con.close()
            
            
            
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
            #Load Category
            #############            
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == str(CategoryID).strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
            
            #Load AnPoint
            #############
            window1.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, str(CategoryID))
            
            window1.SetFocus()
            for index in range(window1.GetItemCount()):
                if window1.GetItem(index,0).GetText().strip() == ContentsID.strip():
                    window1.Focus(index)
                    window1.Select(index,True)
                    break
            
        elif Location == "Target" or Location == "Check List" or Location == "Related tools":
            
            self.MainFrame.public_pfplist_path = DBPath
            
            #GetParentIds...
            ################
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            cursor.execute("Select AnPointID, Text from VesLocationTable where ContentsID = '" + ContentsID + "'")
            ResultRow = cursor.fetchone()
            
            AnPointID = ResultRow[0]
            SelectedText = ResultRow[1]
            
            cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + str(AnPointID) + "'")
            ResultRow = cursor.fetchone()
            
            CategoryID = ResultRow[0]
            
            con.close()
            
            
            
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
            #Load Category
            #############            
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == str(CategoryID).strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
            #Load AnPoint
            #############
            window1.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, str(CategoryID))
            
            window1.SetFocus()
            for index in range(window1.GetItemCount()):
                if window1.GetItem(index,0).GetText().strip() == str(AnPointID).strip():
                    window1.Focus(index)
                    window1.Select(index,True)
                    break
            
            
            #Load Target
            #############
            window2.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, window1.NowCategory, str(AnPointID))
            
            
            if Location == "Target" :
            
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                    
            elif Location == "Related tools":
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                
                window3.SetFocus()
                for index in range(window3.GetItemCount()):
                    if window3.GetItem(index,0).GetText().strip() == ResultString.strip():
                        window3.Focus(index)
                        window3.Select(index,True)
                        break
                
            elif Location == "Check List":
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                
                window4.SetFocus()
                for index in range(window4.GetItemCount()):
                    if window4.GetItem(index,0).GetText().strip() == ResultString.strip():
                        window4.Focus(index)
                        window4.Select(index,True)
                        break
                
                
        elif "Module" in Location:
            
            Modulewindow.AllModule()
        #\\\\!!! 
            
            Modulewindow.SetFocus()
            for index in range(Modulewindow.GetItemCount()):
                if Modulewindow.GetItem(index,3).GetText().strip() == ContentsID.strip():
                    Modulewindow.Focus(index)
                    Modulewindow.Select(index,True)
                    break
            
            
        return 


class SearchPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #panel6    
        panel = wx.Panel(self, -1)
        #panel6 = wx.Panel(splitter, -1)
        
        

        
        panel1 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        self.Search = wx.BitmapButton(panel1, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Search.png'))
        self.Search.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        self.tcSearchKeyword = wx.TextCtrl(panel1)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.tcSearchKeyword, 1, wx.EXPAND)
        vbox.Add(self.Search, 0, wx.EXPAND)
        panel1.SetSizer(vbox)
        


        
        
        panel2 = wx.Panel(panel, -1, style=wx.NO_BORDER)
        list = SearchResult(panel2, -1)
        list.SetName('SearchResult')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(list, 1, wx.EXPAND)
        panel2.SetSizer(vbox0)
        
        
        
        
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        vbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(list1, 1, wx.EXPAND)
        panel3.SetSizer(vbox1)





        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(panel2, 1, wx.EXPAND)
        vbox1.Add(panel3, 0, wx.EXPAND)
        panel.SetSizer(vbox1)
        
        
        
        
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(panel, 1, wx.EXPAND)
        self.SetSizer(vbox2)
        
    def OnSearchButton(self, event):
        
        SearchListWindow = self.FindWindowByName('SearchResult')
        
        SearchListWindow.DeleteAllItems()
        
        DBPathList = ["./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite",
                      "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite",
                      "./PFPModule/PFPLib/PublicPFPList/public.modulelist.sqlite"]
        
        DBPathList.append( self.MainFrame.default_pfplist_path)
        DBPathList.append( self.MainFrame.default_user_modulelistDB_path) 
        
        #print self.MainFrame.default_pfplist_path
        
        QueryList = ["select Text, ContentsID from AnPointTable where ContentsID != '100022' and isDeleted = 'n'",
                     "select Text, ContentsID from CategoryTable where isDeleted = 'n'",
                     "select Text, ContentsID from VesLocationTable where isDeleted = 'n'",
                     "select Description, ContentsID from VesLocationTable where isDeleted = 'n'",
                     "select AcquiTools, ContentsID from VesLocationTable where isDeleted = 'n'",
                     "select Argument, ContentsID from ArgumentList where isDeleted = '1'",
                     "select ModuleName, ContentsID from ModuleList where isDeleted = '0'",
                     "select Author, ContentsID from ModuleList where isDeleted = '0'",
                     "select Description, ContentsID from ModuleList where isDeleted = '0'",
                     "select HomePage, ContentsID from ModuleList where isDeleted = '0'"]
                    
        
        idx = 0
        
        for DBPath in DBPathList:
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            for Query in QueryList:
                
                try:
                    cursor.execute(Query)
                except:
                    continue
                
                ResultList = cursor.fetchall()
                
                if len(ResultList) > 0:
                    for ResultRow in ResultList:
                        
                        if ResultRow[0] == None:
                            continue
                        
                        if "(.. delete..)" in ResultRow[0]:
                            continue
                        
                        UtilClass = Util()
                        try:
                            ResultString = UtilClass.DummyCyber(self.MainFrame.DecodedDummy, "", ResultRow[0])
                        except:
                            ResultString = ResultRow[0]
                        
                        #print ResultString + "\n\n\n\n"
                        
                        if self.tcSearchKeyword.GetLineText(0).lower() in ResultString.lower():
                        
                            Location = ""
                            if "select Text, ContentsID from AnPointTable" in Query:
                                Location = "Analysis Point"
                            elif "select Text, ContentsID from CategoryTable" in Query:
                                Location = "Category"
                            elif "select Text, ContentsID from VesLocationTable" in Query:
                                Location = "Target"
                            elif "select Description, ContentsID from VesLocationTable" in Query:
                                Location = "Check List"
                            elif "select AcquiTools, ContentsID from VesLocationTable" in Query:
                                Location = "Related tools"
                            elif "select Argument, ContentsID from ArgumentList" in Query:
                                Location = "Module Argument"
                            elif "select ModuleName, ContentsID from ModuleList" in Query:
                                Location = "Module Name"
                            elif "select Author, ContentsID from ModuleList" in Query:
                                Location = "Module Author"
                            elif "select Description, ContentsID from ModuleList" in Query:
                                Location = "Module Description"
                            elif "select HomePage, ContentsID from ModuleList" in Query:
                                Location = "Module HomePage"
                            
                        
                            #DBPath + Query + ContentsID
                            ContentsPath = DBPath + "[Token]" + Query + "[Token]" + ResultRow[1]
                            
                            if "select Description, ContentsID from VesLocationTable" in Query or "select AcquiTools, ContentsID from VesLocationTable" in Query:
                                ResultRows = ResultString.split("\t")
            
                                for Row in ResultRows:
                                    if Row.strip() != "":
                                        
                                        if self.tcSearchKeyword.GetLineText(0).lower() in Row.lower():
                                            SearchListWindow.InsertStringItem(idx, Location)
                                            SearchListWindow.SetStringItem(idx, 1, Row)
                                            SearchListWindow.SetStringItem(idx, 2, ContentsPath)
                                                
                                            idx +=1
                            
                            else:
                                SearchListWindow.InsertStringItem(idx, Location)
                                SearchListWindow.SetStringItem(idx, 1, ResultString)
                                SearchListWindow.SetStringItem(idx, 2, ContentsPath)
                            
                                idx += 1
                    
                
        
            con.close()
        
        
        if idx == 0:
            wx.MessageBox("There is no result")
        
        return
    
    def OnKeyDown(self, evt):
        
        key = evt.GetKeyCode()
        #wx.MessageBox(str(key))
        
        if str(key) == "13":                #Key == esc
            self.OnSearchButton("")
            
        elif str(key) == "8":               #KeyCode = backspace
            inspos = self.tcSearchKeyword.GetInsertionPoint()
            self.tcSearchKeyword.Remove(inspos-1, inspos)
            
        else:
            self.tcSearchKeyword.write(chr(key))
                
        return




class ProcessSearchResult(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self.parent = parent
        self.PublicContents = False
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()    
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        #print self.MainFrame.default_pfplist_path

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CategoryIcon_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/AnPointIcon_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/TargetIcon_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)   

        self.InsertColumn(0, '> Location')
        self.InsertColumn(1, 'Related Contents')
        self.InsertColumn(2, 'ContentsPath')
        self.InsertColumn(3, 'ProcessID')
        
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, size.x-5)
        self.SetColumnWidth(2, 0)
        self.SetColumnWidth(3, 0)
        
        dt = ListDrop(self._insert)
        self.SetDropTarget(dt)
        
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
 

 
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.SelectedIndex = event.GetIndex()
        
        colour = self.GetItemBackgroundColour(self.SelectedIndex)
        
        
        if self.MainFrame.isPFPOnManaging == True and colour == '#e6f1f5':
        
            PopupMenu = wx.Menu()        
            
            ConvertToPublicContents  = PopupMenu.Append(-1, "Convert to public contents")                        
                         
            self.Bind(wx.EVT_MENU, self.ConvertToPublicContents, ConvertToPublicContents)
            
            #---Set Menu bar---
            self.PopupMenu(PopupMenu, event.GetPoint())
            
            
        
    def ConvertToPublicContents(self, event):
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        con = sqlite3.connect( self.User_Process_SQLite )
        cursor = con.cursor()
        
        
        
        #sharing select    
        SelectQuery = "select * from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        insertRow = cursor.fetchone()

        #module list insert
        InsertQuery = "insert into ProcessContentsTable values ( "

        fieldidx = 0
        for field in insertRow:
            
            if field == None:
                InsertQuery += "''"
            else:
                InsertQuery += "'" + field + "'"
            if fieldidx < len(insertRow)-1:
                InsertQuery += ","
                
            fieldidx += 1
            
        InsertQuery += ");"
        
        
        
        SelectQuery = "select ParentID, UserContentsLocation from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        ParentID = UserRow[0]
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        con = sqlite3.connect( self.Public_Process_SQLite )
        cursor = con.cursor()
        
        
        
        SelectQuery = "select Sequence from ProcessContentsTable where ContentsID = '" + UserRow[1] + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        try:
            Sequence = UserRow[0]
        except:
            Sequence = '-1'
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) >= " + str(int(Sequence)+1) + " and ParentID = '" + ParentID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) + 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()
        
        
        
        #print InsertQuery
        cursor.execute( InsertQuery )        
        con.commit()
        
        
        
        
        
        SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
        
        cursor.execute( SelectQuery )
        ResultContentsID = cursor.fetchone()
        LastContentsID = int(ResultContentsID[0])
        NextContentsID = int(ResultContentsID[1])
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'n', UserContentsLocation = 'public', Sequence = '" + str(int(Sequence)+1) + "' ,ContentsID = '" + str(NextContentsID) + "' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        self.SetStringItem(self.SelectedIndex, 3, str(NextContentsID))
        
        
        
        LastContentsID += 1
        NextContentsID += 1
        UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
        cursor.execute( UpdateQuery )
        con.commit()
        
        
        
        
        
        self.SetItemBackgroundColour(self.SelectedIndex, '#ffffff')
        
        
        return    
    
    
    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """
        self.PublicContents = False

        # Create the data object: Just use plain text.
        data = wx.PyTextDataObject()
        idx = e.GetIndex()
        
        colour = self.GetItemBackgroundColour(idx)
        if colour != '#e6f1f5' and self.MainFrame.isPFPOnManaging != True:
            wx.MessageBox("Can not modify the public contents")
            return
        
        if colour != '#e6f1f5':
            self.PublicContents = True
        
        Location = self.GetItem(idx, 0).GetText()
        Text = self.GetItem(idx, 1).GetText()
        ContentsPath = self.GetItem(idx, 2).GetText()
        ProcessID = self.GetItem(idx, 3).GetText()
        
        
        data.SetText( Location + "[_Token_]" + Text + "[_Token_]" + ContentsPath + "[_Token_]" + ProcessID)
        #DBPath + "[Token]" + Query + "[Token]" + ResultRow[1]
        
        pos = self.FindItem(idx, Location)
        self.DeleteItem(pos)

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        
        
        
        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            # It's possible we are dragging/dropping from this list to this list.  In which case, the
            # index we are removing may have changed...

            # Find correct position.
            #pos = self.FindItem(idx, ContentsPath)
            #self.DeleteItem(pos)
            return
        
        else:
            
            strs = "Are you sure to delete the dragged contents?"
            dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            
            
    
            if dlg.ShowModal() not in [wx.ID_NO, wx.ID_CANCEL]:
                self.PublicContents = False
                return
            else:
                self.InsertStringItem(idx, Location)
                if Location == "ProcessGroup":
                    self.SetItemColumnImage(idx, 0, 0)
                elif Location == "Category":
                    self.SetItemColumnImage(idx, 0, 1)
                elif Location == "Analysis Point":
                    self.SetItemColumnImage(idx, 0, 2)
                elif Location == "Target":
                    self.SetItemColumnImage(idx, 0, 3)    
                self.SetStringItem(idx, 1, Text)
                self.SetStringItem(idx, 2, ContentsPath)
                self.SetStringItem(idx, 3, ProcessID)
                    
                if self.PublicContents == False:
                    self.SetItemBackgroundColour(idx, '#e6f1f5')
                    
                self.PublicContents = False
        
        
    
    
    def _insert(self, x, y, text):
        """ Insert text at given x, y coordinates --- used with drag-and-drop. """

        # Clean text.
        import string
        text = filter(lambda x: x in (string.letters + string.digits + string.punctuation + ' '), text)

        # Find insertion point.
        index, flags = self.HitTest((x, y))

        if index == wx.NOT_FOUND:
            if flags & wx.LIST_HITTEST_NOWHERE:
                index = self.GetItemCount()
            else:
                return

        
        try:
            # Get bounding rectangle for the item the user is dropping over.
            rect = self.GetItemRect(index)
    
            # If the user is dropping into the lower half of the rect, we want to insert _after_ this item.
            if y > rect.y + rect.height/2:
                index += 1
        except:
            print ""
        
        
        s = text.split("[_Token_]")

        self.InsertStringItem(index, s[0])
        if s[0] == "ProcessGroup":
            self.SetItemColumnImage(index, 0, 0)
        elif s[0] == "Category":
            self.SetItemColumnImage(index, 0, 1)
        elif s[0] == "Analysis Point":
            self.SetItemColumnImage(index, 0, 2)
        elif s[0] == "Target":
            self.SetItemColumnImage(index, 0, 3)    
        self.SetStringItem(index, 1, s[1])
        self.SetStringItem(index, 2, s[2])
        if len(s) > 3:
            self.SetStringItem(index, 3, s[3])
            
        if self.PublicContents != True:
            self.SetItemBackgroundColour(index, '#e6f1f5')
            
            
        self.PublicContents = False
        

    def OnSize(self, event):
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, size.x-5)
        self.SetColumnWidth(2, 0)
        self.SetColumnWidth(3, 0)
        event.Skip()
        
        return
        
    def OnActivated(self, event):

        Location = self.GetItem(event.GetIndex(),0).GetText()
        ResultString = self.GetItem(event.GetIndex(),1).GetText()
        ContentsPath = self.GetItem(event.GetIndex(),2).GetText()
        
        Tokens = ContentsPath.split("[Token]")
        #wx.MessageBox(Tokens[0] + " _ " + Tokens[1] + " _ " + Tokens[2]) 
        
        DBPath = Tokens[0]
        Query = Tokens[1]
        ContentsID = Tokens[2]
        

        window0 = self.MainFrame.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.MainFrame.FindWindowByName('AnalysisPointOnList')
        window2 = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window3 = self.MainFrame.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.MainFrame.FindWindowByName('AnalysisDescriptionOnList')
        Modulewindow = self.MainFrame.FindWindowByName('ModuleListOnList')
        #window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        

        if Location == "Category":
        
            self.MainFrame.public_pfplist_path = DBPath
            
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
                        
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == ContentsID.strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
                
        elif Location == "Analysis Point":
            
            try:
                self.MainFrame.public_pfplist_path = DBPath
            
                #GetParentIds...
                ################
                con = sqlite3.connect( DBPath )
                cursor = con.cursor()
                
                cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + ContentsID + "'")
                ResultRow = cursor.fetchone()
                
                CategoryID = ResultRow[0]
                
                con.close()
            except:
                self.MainFrame.public_pfplist_path = DBPath
            
                #GetParentIds...
                ################
                con = sqlite3.connect( self.MainFrame.default_pfplist_path )
                cursor = con.cursor()
                
                cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + ContentsID + "'")
                ResultRow = cursor.fetchone()
                
                CategoryID = ResultRow[0]
                
                con.close()
            
            
            
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
            #Load Category
            #############            
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == str(CategoryID).strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
            
            #Load AnPoint
            #############
            window1.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, str(CategoryID))
            
            window1.SetFocus()
            for index in range(window1.GetItemCount()):
                if window1.GetItem(index,0).GetText().strip() == ContentsID.strip():
                    window1.Focus(index)
                    window1.Select(index,True)
                    break
            
        elif Location == "Target" or Location == "Check List" or Location == "Related tools":
            
            self.MainFrame.public_pfplist_path = DBPath
            
            #GetParentIds...
            ################
            try:
                con = sqlite3.connect( DBPath )
                cursor = con.cursor()
                
                cursor.execute("Select AnPointID, Text from VesLocationTable where ContentsID = '" + ContentsID + "'")
                ResultRow = cursor.fetchone()
                
                AnPointID = ResultRow[0]
                SelectedText = ResultRow[1]
                
                cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + str(AnPointID) + "'")
                ResultRow = cursor.fetchone()
                
                CategoryID = ResultRow[0]
                
                con.close()
            except:
                con = sqlite3.connect( self.MainFrame.default_pfplist_path )
                cursor = con.cursor()
                
                cursor.execute("Select AnPointID, Text from VesLocationTable where ContentsID = '" + ContentsID + "'")
                ResultRow = cursor.fetchone()
                
                AnPointID = ResultRow[0]
                SelectedText = ResultRow[1]
                
                con.close()
                try:
                    con = sqlite3.connect( DBPath )
                    cursor = con.cursor()
                    
                    cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + str(AnPointID) + "'")
                    ResultRow = cursor.fetchone()
                    
                    CategoryID = ResultRow[0]
                    
                    con.close()
                except:
                    con = sqlite3.connect( self.MainFrame.default_pfplist_path )
                    cursor = con.cursor()
                    
                    cursor.execute("Select CategoryID from AnPointTable where ContentsID = '" + str(AnPointID) + "'")
                    ResultRow = cursor.fetchone()
                    
                    CategoryID = ResultRow[0]
                    
                    con.close()
            
            
            
            
            if "public.1.First_Response.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
                
            elif "public.2.Artifact_Analysis.pfplist.sqlite" in DBPath:
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
                
            #elif "public.2.Disk_Analysis.pfplist.sqlite" in DBPath:
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
            
            if 500000 <= int(ContentsID) and 600000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("UserDefine(TechGroup)")
            elif 600000 <= int(ContentsID) and 700000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("First_Response(win)")
            elif 700000 <= int(ContentsID) and 800000 > int(ContentsID):
                self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Artifact_Analysis.pfplist.sqlite"
                self.MainFrame.pfplist_category_combo.SetValue("Windows_System_Analysis")
            #elif 800000 <= int(ContentsID) and 900000 > int(ContentsID):
            #    self.MainFrame.public_pfplist_path = "./PFPModule/PFPLib/PublicPFPList/public.2.Disk_Analysis.pfplist.sqlite"
            #    self.MainFrame.pfplist_category_combo.SetValue("2.Disk_Analysis")
        
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            #window5.DeleteAllItems()
            
            window0.listidx = 0
            
            #Load Category
            #############            
            window0.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path)
            #window0.LoadData(self.default_pfplist_path)
            
            window0.PublicPFPListFilePath = self.MainFrame.public_pfplist_path
            
            window0.SetFocus()
            for index in range(window0.GetItemCount()):
                if window0.GetItem(index,0).GetText().strip() == str(CategoryID).strip():
                    window0.Focus(index)
                    window0.Select(index,True)
                    break
            
            #Load AnPoint
            #############
            window1.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, str(CategoryID))
            
            window1.SetFocus()
            for index in range(window1.GetItemCount()):
                if window1.GetItem(index,0).GetText().strip() == str(AnPointID).strip():
                    window1.Focus(index)
                    window1.Select(index,True)
                    break
            
            
            #Load Target
            #############
            window2.LoadData(self.MainFrame.public_pfplist_path, self.MainFrame.default_pfplist_path, window1.NowCategory, str(AnPointID))
            
            
            if Location == "Target" :
            
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                    
            elif Location == "Related tools":
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                
                window3.SetFocus()
                for index in range(window3.GetItemCount()):
                    if window3.GetItem(index,0).GetText().strip() == ResultString.strip():
                        window3.Focus(index)
                        window3.Select(index,True)
                        break
                
            elif Location == "Check List":
                window2.SetFocus()
                for index in range(window2.GetItemCount()):
                    if window2.GetItem(index,1).GetText().strip() == ContentsID.strip():
                        window2.Focus(index)
                        window2.Select(index,True)
                        break
                
                window4.SetFocus()
                for index in range(window4.GetItemCount()):
                    if window4.GetItem(index,0).GetText().strip() == ResultString.strip():
                        window4.Focus(index)
                        window4.Select(index,True)
                        break
                
                
        elif "Module" in Location:
            
            Modulewindow.AllModule()
        #\\\\!!! 
            
            Modulewindow.SetFocus()
            for index in range(Modulewindow.GetItemCount()):
                if Modulewindow.GetItem(index,3).GetText().strip() == ContentsID.strip():
                    Modulewindow.Focus(index)
                    Modulewindow.Select(index,True)
                    break
            
            
        return 


class ProcessTreeCtrl(CT.CustomTreeCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 agwStyle=CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_ROW_LINES|CT.TR_TWIST_BUTTONS,
                 log=None):

        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        #self.MainFrame = self.parent.GetGrandParent()
        
        self.DBPath = "" 
        self.PreSelectedID = ""
        
        alldata = dir(CT)

        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)

        self.events = events
        self.styles = treestyles
        self.item = None
        
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        self.folder_close_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png'))
        self.folder_open_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_check_16_16.png'))
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.

        
        if self.MainFrame.isPremium == True:
            self.RootParentID = "Artifact classification"
            self.LoadData("Artifact classification")
        else:
            self.RootParentID = "Artifact classification"
            self.LoadData("UserDefine(Favorite)")
        
        
        self.PreSelectedItem = self.root

        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)
        
        if not hasattr(mainframe, "leftpanel"):
            self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)
        
        
        self.DoSelectItem(self.root)
        

    def LoadData(self, ParentID, ParentNode=None):
    
        
        if ParentNode != None:
            

            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                if PublicRow[0] == "ProcessGroup":
                    ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                        ResultRows.append(UserRow)
            
            
            
            
            
            
            for ResultRow in ResultRows:
            
                child = self.AppendItem(ParentNode, ResultRow[1])
    
                self.SetPyData(child, ResultRow[4])
                self.SetItemImage(child, self.folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.folder_open_idx, wx.TreeItemIcon_Expanded)
                try:
                    if int(ResultRow[4]) < 100000:
                        self.SetItemBackgroundColour(child, '#e6f1f5')
                except:
                    print ""
            
                
                
                
                
                
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubPublicResultRows = cursor.fetchall()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubUserResultRows = cursor.fetchall()
                
                SubResultRows = []
                
                
                for UserRow in SubUserResultRows:
                    if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                        SubResultRows.append(UserRow)
                
                
                for PublicRow in SubPublicResultRows:
                    if PublicRow[0] == "ProcessGroup":
                        SubResultRows.append(PublicRow)
                    
                    for UserRow in SubUserResultRows:
                        if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                            SubResultRows.append(UserRow)
                
                

        
                if len(SubResultRows) > 0:      
                    self.LoadData( ResultRow[4], child)
                    
                        
            
        else:
            
            self.DeleteAllItems()
            
            
            self.UserDBPath = self.User_Process_SQLite
            
            self.PublicDBPath = self.Public_Process_SQLite
    
    
            #print "\n\n\n\\ this is !!!" + self.DBPath + "\n\n\n\\"
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where Location = 'ProcessRoot' and ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            ResultRows = cursor.fetchall()
            
            con.close()
            
            for ResultRow in ResultRows:
                
                self.root = self.AddRoot(ResultRow[1])
    
                if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
                    self.SetPyData(self.root, ResultRow[4])
                    self.RootParentID = ResultRow[4]
                    self.SetItemImage(self.root, self.folder_close_idx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(self.root, self.folder_open_idx, wx.TreeItemIcon_Expanded)

        
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubPublicResultRows = cursor.fetchall()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubUserResultRows = cursor.fetchall()
                
                SubResultRows = []
                
                
                for UserRow in SubUserResultRows:
                    if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                        SubResultRows.append(UserRow)
                
                
                for PublicRow in SubPublicResultRows:
                    if PublicRow[0] == "ProcessGroup":
                        SubResultRows.append(PublicRow)
                    
                    for UserRow in SubUserResultRows:
                        if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                            SubResultRows.append(UserRow)

        
                if len(SubResultRows) > 0:
                    self.LoadData( ResultRow[4], self.root)
                    
                
            con.close()
            
            
            
            
            
            #Load Selected members
            RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
            
            RelatedContentsWindow.DeleteAllItems()
            
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + self.RootParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + self.RootParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5]:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4]:
                        ResultRows.append(UserRow)
                        
                        
            
            
            idx = 0
            
            for ResultRow in ResultRows:
                
                RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
                if ResultRow[0] == "ProcessGroup":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
                elif ResultRow[0] == "Category":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
                elif ResultRow[0] == "Analysis Point":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
                elif ResultRow[0] == "Target":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
                RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
                RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
                RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
                
                #try:
                if int(ResultRow[4]) < 100000 :
                    RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')
    
                
                idx += 1
            
            con.close()
            
            self.PreSelectedID = self.GetPyData(self.root)
            self.PreSelectedItem = self.root

        


        """
        textctrl = wx.TextCtrl(self, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        self.gauge = wx.Gauge(self, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(0)
        combobox = wx.ComboBox(self, -1, choices=["That", "Was", "A", "Nice", "Holyday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)

        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        lenArtIds = len(ArtIDs) - 2
        """

        """
        for x in range(15):
            if x == 1:
                child = self.AppendItem(self.root, "Item %d" % x)# + "\nHello World\nHappy wxPython-ing!")
                self.SetItemBold(child, True)
            else:
                child = self.AppendItem(self.root, "Item %d" % x)
            self.SetPyData(child, None)
            self.SetItemImage(child, folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, folder_open_idx, wx.TreeItemIcon_Expanded)
            

            if random.randint(0, 3) == 0:
                self.SetItemLeftImage(child, random.randint(0, lenArtIds))

            for y in range(5):
                if y == 0 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2, wnd=self.gauge)
                elif y == 1 and x == 2:
                    last = self.AppendItem(child, "Item %d-%s" % (x, chr(ord("a")+y)), ct_type=1, wnd=textctrl)
                    if random.randint(0, 3) == 1:
                        self.SetItem3State(last, True)
                        
                elif 2 < y < 4:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
                elif y == 4 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), wnd=combobox)
                else:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2)
                    
                self.SetPyData(last, None)
                self.SetItemImage(last, folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(last, folder_open_idx, wx.TreeItemIcon_Expanded)

                if random.randint(0, 3) == 0:
                    self.SetItemLeftImage(last, random.randint(0, lenArtIds))
                    
                for z in range(5):
                    if z > 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
                        if random.randint(0, 3) == 1:
                            self.SetItem3State(item, True)
                    elif 0 < z <= 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=2)
                    elif z == 0:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                        self.SetItemHyperText(item, True)
                    self.SetPyData(item, None)
                    self.SetItemImage(item, folder_close_idx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(item, folder_open_idx, wx.TreeItemIcon_Expanded)

                    if random.randint(0, 3) == 0:
                        self.SetItemLeftImage(item, random.randint(0, lenArtIds))

        
            
        """


        return

    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        
        evt = "CT." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, None)
                self.Bind(wx.EVT_RIGHT_UP, None)
            self.Bind(eval(evt), binder)
        else:
            self.Bind(eval(evt), None)
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                style = style | eval("CT." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)
            

    def OnCompareItems(self, item1, item2):
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        
        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1

    
    def OnIdle(self, event):

        """
        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()
        """
        return 

    #---RightDown

    def OnRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        if item:
            
            self.current = item
            
            self.SelectItem(item)
            
            
            PopupMenu = wx.Menu()        
        
            OnDelete = PopupMenu.Append(wx.ID_ANY, "Delete Group")
            OnAddSub = PopupMenu.Append(wx.ID_ANY, "Add Sub Group")
            #OnAddSibling = PopupMenu.Append(wx.ID_ANY, "Add Sibling Group")
    
            #---Set Menu bar---
            
            
            #self.PopUpSelectedRow = event.GetRow()
            self.Bind(wx.EVT_MENU, self.OnItemDelete, OnDelete)
            self.Bind(wx.EVT_MENU, self.OnItemAddSub, OnAddSub)
            #self.Bind(wx.EVT_MENU, self.OnItemAddSibling, OnAddSibling)
            
            self.PopupMenu(PopupMenu, event.GetPosition())
            
            """
            self.item = item
            self.log.write("OnRightClick: %s, %s, %s" % (self.GetItemText(item), type(item), item.__class__) + "\n")
            """
            

    def OnRightUp(self, event):
        
        item = self.item
        
        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return


        """
        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)

        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)
        
        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
        
        menu = wx.Menu()

        item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()
        if haswin:
            enabled = self.GetItemWindowEnabled(item)
            if enabled:
                strs = "Disable Associated Widget"
            else:
                strs = "Enable Associated Widget"
        else:
            strs = "Enable Associated Widget"
        item6 = menu.Append(wx.ID_ANY, strs)

        if not haswin:
            item6.Enable(False)

        item7 = menu.Append(wx.ID_ANY, "Disable Item")
        
        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        
        self.PopupMenu(menu)
        menu.Destroy()
        """

    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)
        dlg.Destroy()


    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            
        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        

    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])


    def OnEnableWindow(self, event):

        enable = self.GetItemWindowEnabled(self.current)
        self.SetItemWindowEnabled(self.current, not enable)


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        

    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()        
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], CT.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], CT.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], CT.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], CT.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "CustomTreeCtrlDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                
        
    #---Delete Item
    def OnItemDelete(self, event):

        
        colour = self.GetItemBackgroundColour(self.current)
        if colour != '#e6f1f5' and self.MainFrame.isPFPOnManaging != True:
            wx.MessageBox("Can not delete the public contents")
            return
        

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None
        
        
        CurrentID = self.GetPyData(self.item)
        
        DBPath = ""
        
        if colour == '#e6f1f5':
            DBPath = self.UserDBPath
        else:
            DBPath = self.PublicDBPath
            
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        UpdateQuery = "update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + CurrentID + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        SelectQuery = "select ParentID, Sequence from ProcessContentsTable where ContentsID = '" + CurrentID + "'"
        cursor.execute( SelectQuery )
        ResultRow = cursor.fetchone()
        
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) > " + ResultRow[1] + " and ParentID ='" + ResultRow[0] + "'"
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()

        con.close()
        

    #---Add Tree item

    def OnItemAddSub(self, event):

        dlg = wx.TextEntryDialog(self, "Please enter the new process group", 'group naming', 'insert new..')
        
        
        
        

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            
            self.SetItemImage(newitem, self.folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(newitem, self.folder_open_idx, wx.TreeItemIcon_Expanded)
            self.SetItemBackgroundColour(newitem, '#e6f1f5')
            self.EnsureVisible(newitem)
            
            
            
            #insert
            ParentID = self.GetPyData(self.current)
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            ProcessCategory = "Process" 
            Location  = "ProcessGroup"
            Text  = newname
            ContentsPath  = ""
            Description  = ""
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
    
            cursor.execute( SelectQuery )
            ResultContentsID = cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            ContentsID  = str(NextContentsID)
            self.SetPyData(newitem, ContentsID)
            InsertParentID  = ParentID
            isDeleted  = "n"
            Author  = "Guest"
            Contact  = "Guest"
            
            UserContentsLocation = ""
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            UserContentsLocation = "top"
            cursor.execute("Select ContentsID from ProcessContentsTable where isDeleted = 'n' and ParentID = '"+ InsertParentID +"' order by cast(Sequence as decimal)")
            ResultRows = cursor.fetchall()
            for ResultRow in ResultRows:
                UserContentsLocation = ResultRow[0]
            
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            cursor.execute("Select * from ProcessContentsTable where isDeleted = 'n' and  ParentID = '"+ InsertParentID +"' and UserContentsLocation = '" + UserContentsLocation + "'")
            ResultRows = cursor.fetchall()
            Sequence  = str(len(ResultRows))
            
            
            
            InsertQuery = "insert into ProcessContentsTable ( ProcessCategory , Location , Text , ContentsPath , Description , ContentsID , ParentID , isDeleted , Author , Contact , Sequence, UserContentsLocation ) values ( '" + ProcessCategory + "','" + Location + "','" + Text + "','" + ContentsPath + "','" + Description + "','" + ContentsID + "','" + InsertParentID + "','" + isDeleted + "','" + Author + "','" + Contact + "','" + Sequence + "','" + UserContentsLocation + "');"
            cursor.execute( InsertQuery )
            con.commit()
            
            
            
            LastContentsID += 1
            NextContentsID += 1
            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
            cursor.execute( UpdateQuery )
            con.commit()
            
            
            
            #Load Selected members
            RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
            
            RelatedContentsWindow.DeleteAllItems()
            
            
            
            
            
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5]:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4]:
                        ResultRows.append(UserRow)
            

            
            idx = 0
            
            for ResultRow in ResultRows:
                
                RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
                RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
                RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
                RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
                if ResultRow[0] == "ProcessGroup":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
                elif ResultRow[0] == "Category":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
                elif ResultRow[0] == "Analysis Point":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
                elif ResultRow[0] == "Target":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
            
                if int(ResultRow[4]) < 100000 :
                    RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')
                
                idx += 1
            
            con.close()  
            

        dlg.Destroy()


    def OnItemAddSibling(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)
            
            
            

        dlg.Destroy()
        

    def OnBeginEdit(self, event):
        
        self.log.write("OnBeginEdit" + "\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one..." + "\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d" % (self.GetItemText(child), self.IsVisible(child)) + "\n")
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):
        
        self.log.write("OnEndEdit: %s %s" %(event.IsEditCancelled(), event.GetLabel()))
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.write(", You can't enter digits..." + "\n")
                event.Veto()
                return
            
        self.log.write("\n")


    def OnLeftDClick(self, event):
        """
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item and (flags & CT.TREE_HITTEST_ONITEMLABEL):
            if self.GetAGWWindowStyleFlag() & CT.TR_EDIT_LABELS:
                self.log.write("OnLeftDClick: %s (manually starting label edit)"% self.GetItemText(item) + "\n")
                self.EditLabel(item)
            else:
                self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")
        """
        event.Skip()                
        

    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemExpanded: %s" % self.GetItemText(item) + "\n")


    def OnItemExpanding(self, event):
        
        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemExpanding: %s" % self.GetItemText(item) + "\n")
            
        event.Skip()

        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemCollapsed: %s" % self.GetItemText(item) + "\n")
            

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemCollapsing: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()

    
    #---Sel Change
    
        
    def OnSelChanged(self, event):

        

        #wx.MessageBox("~~")
        self.item = event.GetItem()
        ParentID = self.GetPyData(self.item)
        #print "NowID = " + ParentID
        #print "PreID = " + self.PreSelectedID
        RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
        
        ChangedFlag = False
        
        con = sqlite3.connect( self.PublicDBPath )
        cursor = con.cursor()
        
        
        cursor.execute("Select * from ProcessContentsTable where ParentID = '"+ self.PreSelectedID +"' and isDeleted = 'n'")
        PublicResultRows = cursor.fetchall()    
        
        con = sqlite3.connect( self.UserDBPath )
        cursor = con.cursor()
        
        
        cursor.execute("Select * from ProcessContentsTable where ParentID = '"+ self.PreSelectedID +"' and isDeleted = 'n'")
        UserResultRows = cursor.fetchall()    
        
        #print RelatedContentsWindow.GetItemCount() 
        #print len(ResultRows)
        
        if RelatedContentsWindow.GetItemCount() != (len(PublicResultRows) + len(UserResultRows)):
            #print "Number of contents is Diffrent!!"
            ChangedFlag = True    
        
        
        Publicidx = 0
        Useridx = 0
        NowPublic = "top"
        
        for _idx in range(RelatedContentsWindow.GetItemCount()):
            
            colour = RelatedContentsWindow.GetItemBackgroundColour(_idx)
            
            if colour != '#e6f1f5':
                
                ContentsID = RelatedContentsWindow.GetItem(_idx, 3).GetText()
                NowPublic = ContentsID
                
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                SelectQuery = "Select * from ProcessContentsTable where Sequence = '"+ str(Publicidx) +"' and ContentsID = '"+ ContentsID +"' and isDeleted = 'n'"
                #print "Query = " + SelectQuery
                cursor.execute(SelectQuery)
                ResultRows = cursor.fetchall()
                
                #print ResultRows
                
                if len(ResultRows) == 0:
                    #print RelatedContentsWindow.GetItem(_idx, 1).GetText() + ", id = " + ContentsID + " is changed..!!"
                    ChangedFlag = True
                    break
                    
                Publicidx += 1
                Useridx = 0
                
            else:
                ContentsID = RelatedContentsWindow.GetItem(_idx, 3).GetText()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                SelectQuery = "Select * from ProcessContentsTable where Sequence = '"+ str(Useridx) +"' and ContentsID = '"+ ContentsID +"' and UserContentsLocation = '" + NowPublic + "' and isDeleted = 'n'"
                #print "Query = " + SelectQuery
                cursor.execute(SelectQuery)
                ResultRows = cursor.fetchall()
                
                #print ResultRows
                
                if len(ResultRows) == 0:
                    #print RelatedContentsWindow.GetItem(_idx, 1).GetText() + ", id = " + ContentsID + " is changed..!!"
                    ChangedFlag = True
                    break
                    
                Useridx += 1
        

        con.close()
        

        if ChangedFlag == True:
            
            strs = "Process contents is changed. Are you sure to save?"
            dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    
            if dlg.ShowModal() not in [wx.ID_NO, wx.ID_CANCEL]:
                
                
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                UpdateQuery = "Update ProcessContentsTable set isDeleted = 'y' where ParentID = '"+ self.PreSelectedID +"'"
                cursor.execute(UpdateQuery)
                con.commit()
                
                
                PublicIdx = 0 
    
                for idx in range(0, RelatedContentsWindow.GetItemCount()):
                    
                    colour = RelatedContentsWindow.GetItemBackgroundColour(idx)
                    if colour == '#e6f1f5':
                        
                        continue
                           
                    else:
                
                        cursor.execute("Select * from ProcessContentsTable where ContentsID = '" + RelatedContentsWindow.GetItem(idx, 3).GetText() + "'")
                        ResultRows = cursor.fetchall()
                        
                        if len(ResultRows) <= 0:
                            #insert
                            ProcessCategory = "Process" 
                            Location  = RelatedContentsWindow.GetItem(idx, 0).GetText()
                            Text  = RelatedContentsWindow.GetItem(idx, 1).GetText()
                            ContentsPath  = RelatedContentsWindow.GetItem(idx, 2).GetText()
                            Description  = ""
                            
                            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
        
                            cursor.execute( SelectQuery )
                            ResultContentsID = cursor.fetchone()
                            LastContentsID = int(ResultContentsID[0])
                            NextContentsID = int(ResultContentsID[1])
                            
                            ContentsID  = str(NextContentsID)
                            
                            InsertParentID  = self.PreSelectedID
                            
                            
                            isDeleted  = "n"
                            Author  = "Guest"
                            Contact  = "Guest"
                            Sequence  = str(PublicIdx)
                            
                            InsertQuery = "insert into ProcessContentsTable ( ProcessCategory , Location , Text , ContentsPath , Description , ContentsID , ParentID , isDeleted , Author , Contact , Sequence ) values ( '" + ProcessCategory + "','" + Location + "','" + Text + "','" + ContentsPath + "','" + Description + "','" + ContentsID + "','" + InsertParentID + "','" + isDeleted + "','" + Author + "','" + Contact + "','" + Sequence + "');"
                            cursor.execute( InsertQuery )
                            con.commit()
                            
                            
                            
                            LastContentsID += 1
                            NextContentsID += 1
                            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                            cursor.execute( UpdateQuery )
                            con.commit()
                            
                        else:
                            #Sequence Update
                            UpdateQuery = "Update ProcessContentsTable set isDeleted = 'n', Sequence = '" + str(PublicIdx) + "', UserContentsLocation = 'public' where ContentsID = '" + RelatedContentsWindow.GetItem(idx, 3).GetText() + "'"
                            cursor.execute(UpdateQuery)
                            con.commit()
                            
                        PublicIdx += 1
                    
                
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                UpdateQuery = "Update ProcessContentsTable set isDeleted = 'y' where ParentID = '"+ self.PreSelectedID +"'"
                cursor.execute(UpdateQuery)
                con.commit()
                
                
                UserIdx = 0 
                UserContentsLocation = "top"
    
                for idx in range(0, RelatedContentsWindow.GetItemCount()):
                    
                    colour = RelatedContentsWindow.GetItemBackgroundColour(idx)
                    if colour != '#e6f1f5':
                        
                        UserContentsLocation = RelatedContentsWindow.GetItem(idx, 3).GetText()
                        UserIdx = 0
                        
                        
                    else:
                        
                        
                        cursor.execute("Select * from ProcessContentsTable where ContentsID = '" + RelatedContentsWindow.GetItem(idx, 3).GetText() + "'")
                        ResultRows = cursor.fetchall()
                        
                        if len(ResultRows) <= 0:
                            #insert
                            ProcessCategory = "Process" 
                            Location  = RelatedContentsWindow.GetItem(idx, 0).GetText()
                            Text  = RelatedContentsWindow.GetItem(idx, 1).GetText()
                            ContentsPath  = RelatedContentsWindow.GetItem(idx, 2).GetText()
                            Description  = ""
                            
                            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
        
                            cursor.execute( SelectQuery )
                            ResultContentsID = cursor.fetchone()
                            LastContentsID = int(ResultContentsID[0])
                            NextContentsID = int(ResultContentsID[1])
                            
                            ContentsID  = str(NextContentsID)
                            
                            InsertParentID  = self.PreSelectedID
                            
                            
                            isDeleted  = "n"
                            Author  = "Guest"
                            Contact  = "Guest"
                            Sequence  = str(idx)
                            
                            InsertQuery = "insert into ProcessContentsTable ( ProcessCategory , Location , Text , ContentsPath , Description , ContentsID , ParentID , isDeleted , Author , Contact , Sequence, UserContentsLocation ) values ( '" + ProcessCategory + "','" + Location + "','" + Text + "','" + ContentsPath + "','" + Description + "','" + ContentsID + "','" + InsertParentID + "','" + isDeleted + "','" + Author + "','" + Contact + "','" + Sequence + "','" + UserContentsLocation + "');"
                            cursor.execute( InsertQuery )
                            con.commit()
                            
                            
                            
                            LastContentsID += 1
                            NextContentsID += 1
                            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                            cursor.execute( UpdateQuery )
                            con.commit()
                            
                        else:
                            #Sequence Update
                            UpdateQuery = "Update ProcessContentsTable set isDeleted = 'n', Sequence = '" + str(UserIdx) + "', UserContentsLocation = '" + UserContentsLocation + "' where ContentsID = '" + RelatedContentsWindow.GetItem(idx, 3).GetText() + "'"
                            cursor.execute(UpdateQuery)
                            con.commit()
                            
                        UserIdx += 1
                
                self.DeleteChildren(self.PreSelectedItem)        
                self.LoadData( self.PreSelectedID, self.PreSelectedItem)

        
        con.close()


            
        
        #Load Selected members
        RelatedContentsWindow.DeleteAllItems()
        
        con = sqlite3.connect( self.PublicDBPath )
        cursor = con.cursor()
        
        cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
        PublicResultRows = cursor.fetchall()
        
        con = sqlite3.connect( self.UserDBPath )
        cursor = con.cursor()
        
        cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
        UserResultRows = cursor.fetchall()
        
        ResultRows = []
        
        
        for UserRow in UserResultRows:
            if "top" in UserRow[5]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[5] == PublicRow[4]:
                    ResultRows.append(UserRow)
                    
                    
        
        
        idx = 0
        
        for ResultRow in ResultRows:
            
            RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
            if ResultRow[0] == "ProcessGroup":
                RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
            elif ResultRow[0] == "Category":
                RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
            elif ResultRow[0] == "Analysis Point":
                RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
            elif ResultRow[0] == "Target":
                RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
            RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
            RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
            RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
            
            #try:
            if int(ResultRow[4]) < 100000 :
                RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')

            
            idx += 1
        
        con.close()
        
        
        """
        temp_listdb_con = sqlite3.connect( PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        for UserRow in UserResultRows:
            if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:
                ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
                    
                    
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)  
                
        
        
        #self.InsertColumn(0, '')
        
        idx = 0 
        for Row in ResultRows:
            
            self.InsertStringItem(idx, Row[1])
            
            try:
                UtilClass = Util()
                self.SetStringItem(idx, 1, UtilClass.DummyCyber(self.GetGrandParent().GetGrandParent().GetGrandParent().DecodedDummy, "", Row[0]))
                
            except:
                self.SetStringItem(idx, 1, Row[0])
                
            self.SetItemColumnImage(idx,1, 1)
            
            if int(Row[1]) > 500000 :
                self.SetItemBackgroundColour(idx, '#e6f1f5')
            idx +=1
                        
        temp_listdb_con.close()
        """
        
        
            
        """
        if self.item:
            self.log.write("OnSelChanged: %s" % self.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.write(", BoundingRect: %s" % self.GetBoundingRect(self.item, True) + "\n")
            else:
                self.log.write("\n")
        """     
        
        self.PreSelectedID = self.GetPyData(self.item)
        self.PreSelectedItem = self.item
        
        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()
        """
        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s" % olditemtext + " To %s" % self.GetItemText(item) + "\n")
        """       
        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Drag..." + "\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Right Drag..." + "\n")

            event.Allow()
        

    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!" + "\n")

        event.Skip()            


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s" % self.GetItemText(item) + "\n")
        event.Skip()
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()
        

    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

        event.Skip()

        
    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s" % self.GetItemText(self.item) + "\n")
            

    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()

        
class ProcessPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #panel6    
        panel = wx.Panel(self, -1)
        #panel6 = wx.Panel(splitter, -1)
        
        

        
        panel1 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        #self.Load = wx.BitmapButton(panel1, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/fileopen.png'))
        #self.Load.Bind(wx.EVT_BUTTON, self.OnLoadButton)
        self.ProcessList = []
        if self.MainFrame.isPremium == True:
            self.ProcessList.append("Artifact classification")
        self.ProcessList.append("UserDefine(Favorite)")                  
        self.forensic_process_combo = wx.ComboBox(panel1, choices=self.ProcessList)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.forensic_process_combo, 1, wx.EXPAND)
        #vbox.Add(self.Load, 0, wx.EXPAND)
        self.forensic_process_combo.Bind(wx.EVT_COMBOBOX, self.OnProcessComboSelect)
        panel1.SetSizer(vbox)
        
        if self.MainFrame.isPremium == True:
            self.forensic_process_combo.SetValue("Artifact classification and additional analysis factor")
        else:
            self.forensic_process_combo.SetValue("UserDefine(Favorite)")


        splitter = wx.SplitterWindow(panel, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

        panel2_2 = wx.Panel(splitter, -1, style=wx.NO_BORDER)
        list = ProcessSearchResult(panel2_2, -1)
        list.SetName('RelatedContents')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(list, 1, wx.EXPAND)
        panel2_2.SetSizer(vbox0)
        

        self.tree = ProcessTreeCtrl(splitter, -1, 
                                   style=wx.NO_BORDER,
                                   agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_ROW_LINES | CT.TR_FULL_ROW_HIGHLIGHT
                                   | CT.TR_TOOLTIP_ON_LONG_ITEMS)# | CT.TR_HIDE_ROOT)   
        self.tree.SetBackgroundColour('WHITE')
        
        
        
        
        splitter.SplitVertically(self.tree, panel2_2, 250)
        
        
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        vbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(list1, 1, wx.EXPAND)
        panel3.SetSizer(vbox1)





        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(splitter, 1, wx.EXPAND)
        vbox1.Add(panel3, 0, wx.EXPAND)
        panel.SetSizer(vbox1)
        
        
        
        
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(panel, 1, wx.EXPAND)
        self.SetSizer(vbox2)

    def OnProcessComboSelect(self, event):
        
        SelectedText = self.forensic_process_combo.GetValue()
        
        self.tree.LoadData(SelectedText)
        
        return 

    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile="", style=wx.OPEN)
        NewPFPListFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            NewPFPListFile = dlg.GetPath()
        
        return






class RegistryList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self.parent = parent
        self.PublicContents = False
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()    
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        #print self.MainFrame.default_pfplist_path

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Reg_BINARY_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Reg_SZ_16_16.png', 'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/TargetIcon_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)   

        self.InsertColumn(0, '> Type')
        self.InsertColumn(1, 'Name')
        self.InsertColumn(2, 'Data Type')
        self.InsertColumn(3, 'Data')
        
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, 200)
        self.SetColumnWidth(2, 200)
        self.SetColumnWidth(3, size.x-5)
        

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
 

 
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.SelectedIndex = event.GetIndex()
        
        colour = self.GetItemBackgroundColour(self.SelectedIndex)
        
        
        if self.MainFrame.isPFPOnManaging == True and colour == '#e6f1f5':
        
            PopupMenu = wx.Menu()        
            
            ConvertToPublicContents  = PopupMenu.Append(-1, "Convert to public contents")                        
                         
            self.Bind(wx.EVT_MENU, self.ConvertToPublicContents, ConvertToPublicContents)
            
            #---Set Menu bar---
            self.PopupMenu(PopupMenu, event.GetPoint())
            
            
        
    def ConvertToPublicContents(self, event):
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        con = sqlite3.connect( self.User_Process_SQLite )
        cursor = con.cursor()
        
        
        
        #sharing select    
        SelectQuery = "select * from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        insertRow = cursor.fetchone()

        #module list insert
        InsertQuery = "insert into ProcessContentsTable values ( "

        fieldidx = 0
        for field in insertRow:
            
            if field == None:
                InsertQuery += "''"
            else:
                InsertQuery += "'" + field + "'"
            if fieldidx < len(insertRow)-1:
                InsertQuery += ","
                
            fieldidx += 1
            
        InsertQuery += ");"
        
        
        
        SelectQuery = "select ParentID, UserContentsLocation from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        ParentID = UserRow[0]
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        con = sqlite3.connect( self.Public_Process_SQLite )
        cursor = con.cursor()
        
        
        
        SelectQuery = "select Sequence from ProcessContentsTable where ContentsID = '" + UserRow[1] + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        try:
            Sequence = UserRow[0]
        except:
            Sequence = '-1'
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) >= " + str(int(Sequence)+1) + " and ParentID = '" + ParentID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) + 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()
        
        
        
        #print InsertQuery
        cursor.execute( InsertQuery )        
        con.commit()
        
        
        
        
        
        SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
        
        cursor.execute( SelectQuery )
        ResultContentsID = cursor.fetchone()
        LastContentsID = int(ResultContentsID[0])
        NextContentsID = int(ResultContentsID[1])
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'n', UserContentsLocation = 'public', Sequence = '" + str(int(Sequence)+1) + "' ,ContentsID = '" + str(NextContentsID) + "' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        self.SetStringItem(self.SelectedIndex, 3, str(NextContentsID))
        
        
        
        LastContentsID += 1
        NextContentsID += 1
        UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
        cursor.execute( UpdateQuery )
        con.commit()
        
        
        
        
        
        self.SetItemBackgroundColour(self.SelectedIndex, '#ffffff')
        
        
        return    
    
    

    def OnSize(self, event):
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, 200)
        self.SetColumnWidth(2, 200)
        self.SetColumnWidth(3, size.x-5)
        event.Skip()
        
        return
        
    
    def ThreadActivation(self):
    
    
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window.ActivationFlag = True
    
    
        if self.Type == "Value":
            wx.MessageBox("Data lookup func will be added")
            
        elif self.Type == "SubKey":
            comboPath = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
            if comboPath[len(comboPath)-1] == "\\":
                comboPath = comboPath[0:len(comboPath)-1]
            
            if self.Name == "..":
                ComboText = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
                self.parent.GetParent().GetParent().GetParent().OriginalCombo = ComboText
                window.NowRegistryComboSelected = os.path.split(comboPath)[0]
                self.parent.GetParent().GetParent().GetParent().combo.SetValue(os.path.split(comboPath)[0])
            else:
                ComboText = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
                self.parent.GetParent().GetParent().GetParent().OriginalCombo = ComboText
                window.NowRegistryComboSelected = comboPath.split("<")[0].strip() + "\\" + self.Name
                self.parent.GetParent().GetParent().GetParent().combo.SetValue(comboPath.split("<")[0].strip() + "\\" + self.Name)
                
            threads = []
            th = threading.Thread(target=window.SetRegistryTreeAndList, args=())
            th.start()
            threads.append(th)
            
            
            progressMax = 100
            dialog = wx.ProgressDialog("Registry Lookup progress", "Please wait..", progressMax, style=wx.PD_ELAPSED_TIME )
            
            while th.is_alive() == True:
                wx.Sleep(0.1)
                dialog.Pulse()
            
            dialog.Destroy()
            
            size = self.parent.GetSize()
            self.SetColumnWidth(0, 20)
            

        window.ActivationFlag = False
        
        return
    
    
    def OnActivated(self, event):

        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        
        if window.ActivationFlag == True:
            wx.MessageBox("Please wait. other process is running")

        else:
            self.Type = self.GetItem(event.GetIndex(),0).GetText()
            self.Name = self.GetItem(event.GetIndex(),1).GetText()
            
            threads = []
            th = threading.Thread(target=self.ThreadActivation, args=())
            th.start()
            threads.append(th)

        
            
        return 


class RegistryTree(CT.CustomTreeCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 agwStyle=CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_ROW_LINES|CT.TR_TWIST_BUTTONS,
                 log=None):

        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        #self.MainFrame = self.parent.GetGrandParent()
        
        self.DBPath = "" 
        self.PreSelectedID = ""
        
        alldata = dir(CT)

        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)

        self.events = events
        self.styles = treestyles
        self.item = None
        
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        self.folder_close_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png'))
        self.folder_open_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_check_16_16.png'))
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.


        self.root = self.AddRoot("Registry Lookup Result")

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SetItemImage(self.root, self.folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root, self.folder_open_idx, wx.TreeItemIcon_Expanded)


        
        self.PreSelectedItem = self.root

        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)
        
        if not hasattr(mainframe, "leftpanel"):
            self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)
        
        
        self.DoSelectItem(self.root)
        

    def LoadData(self, ParentID, ParentNode = None):
    
        
        if ParentNode != None:
            

            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                if PublicRow[0] == "ProcessGroup":
                    ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                        ResultRows.append(UserRow)
            
            
            
            
            
            
            for ResultRow in ResultRows:
            
                child = self.AppendItem(ParentNode, ResultRow[1])
    
                self.SetPyData(child, ResultRow[4])
                self.SetItemImage(child, self.folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.folder_open_idx, wx.TreeItemIcon_Expanded)
                try:
                    if int(ResultRow[4]) < 100000:
                        self.SetItemBackgroundColour(child, '#e6f1f5')
                except:
                    print ""
            
                
                
                
                
                
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubPublicResultRows = cursor.fetchall()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubUserResultRows = cursor.fetchall()
                
                SubResultRows = []
                
                
                for UserRow in SubUserResultRows:
                    if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                        SubResultRows.append(UserRow)
                
                
                for PublicRow in SubPublicResultRows:
                    if PublicRow[0] == "ProcessGroup":
                        SubResultRows.append(PublicRow)
                    
                    for UserRow in SubUserResultRows:
                        if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                            SubResultRows.append(UserRow)
                
                

        
                if len(SubResultRows) > 0:      
                    self.LoadData( ResultRow[4], child)
                    
                        
            
        else:
       
            
            self.DeleteAllItems()
                           
            self.root = self.AddRoot(ResultRow[1])

            if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
                self.SetPyData(self.root, ResultRow[4])
                self.RootParentID = ResultRow[4]
                self.SetItemImage(self.root, self.folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(self.root, self.folder_open_idx, wx.TreeItemIcon_Expanded)

        
        return

    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        
        evt = "CT." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, None)
                self.Bind(wx.EVT_RIGHT_UP, None)
            self.Bind(eval(evt), binder)
        else:
            self.Bind(eval(evt), None)
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                style = style | eval("CT." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)
            

    def OnCompareItems(self, item1, item2):
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        
        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1

    
    def OnIdle(self, event):

        """
        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()
        """
        return 

    #---RightDown

    def OnRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        if item:
            
            self.current = item
            
            self.SelectItem(item)
            
            
            PopupMenu = wx.Menu()        
        
            OnDelete = PopupMenu.Append(wx.ID_ANY, "Delete Group")
            OnAddSub = PopupMenu.Append(wx.ID_ANY, "Add Sub Group")
            #OnAddSibling = PopupMenu.Append(wx.ID_ANY, "Add Sibling Group")
    
            #---Set Menu bar---
            
            
            #self.PopUpSelectedRow = event.GetRow()
            self.Bind(wx.EVT_MENU, self.OnItemDelete, OnDelete)
            self.Bind(wx.EVT_MENU, self.OnItemAddSub, OnAddSub)
            #self.Bind(wx.EVT_MENU, self.OnItemAddSibling, OnAddSibling)
            
            self.PopupMenu(PopupMenu, event.GetPosition())
            
            """
            self.item = item
            self.log.write("OnRightClick: %s, %s, %s" % (self.GetItemText(item), type(item), item.__class__) + "\n")
            """
            

    def OnRightUp(self, event):
        
        item = self.item
        
        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return


        """
        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)

        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)
        
        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
        
        menu = wx.Menu()

        item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()
        if haswin:
            enabled = self.GetItemWindowEnabled(item)
            if enabled:
                strs = "Disable Associated Widget"
            else:
                strs = "Enable Associated Widget"
        else:
            strs = "Enable Associated Widget"
        item6 = menu.Append(wx.ID_ANY, strs)

        if not haswin:
            item6.Enable(False)

        item7 = menu.Append(wx.ID_ANY, "Disable Item")
        
        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        
        self.PopupMenu(menu)
        menu.Destroy()
        """

    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)
        dlg.Destroy()


    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            
        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        

    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])


    def OnEnableWindow(self, event):

        enable = self.GetItemWindowEnabled(self.current)
        self.SetItemWindowEnabled(self.current, not enable)


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        

    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()        
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], CT.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], CT.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], CT.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], CT.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "CustomTreeCtrlDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                
        
    #---Delete Item
    def OnItemDelete(self, event):

        
        colour = self.GetItemBackgroundColour(self.current)
        if colour != '#e6f1f5' and self.MainFrame.isPFPOnManaging != True:
            wx.MessageBox("Can not delete the public contents")
            return
        

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None
        
        
        CurrentID = self.GetPyData(self.item)
        
        DBPath = ""
        
        if colour == '#e6f1f5':
            DBPath = self.UserDBPath
        else:
            DBPath = self.PublicDBPath
            
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        UpdateQuery = "update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + CurrentID + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        SelectQuery = "select ParentID, Sequence from ProcessContentsTable where ContentsID = '" + CurrentID + "'"
        cursor.execute( SelectQuery )
        ResultRow = cursor.fetchone()
        
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) > " + ResultRow[1] + " and ParentID ='" + ResultRow[0] + "'"
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()

        con.close()
        

    #---Add Tree item

    def OnItemAddSub(self, event):

        dlg = wx.TextEntryDialog(self, "Please enter the new process group", 'group naming', 'insert new..')
        
        
        
        

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            
            self.SetItemImage(newitem, self.folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(newitem, self.folder_open_idx, wx.TreeItemIcon_Expanded)
            self.SetItemBackgroundColour(newitem, '#e6f1f5')
            self.EnsureVisible(newitem)
            
            
            
            #insert
            ParentID = self.GetPyData(self.current)
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            ProcessCategory = "Process" 
            Location  = "ProcessGroup"
            Text  = newname
            ContentsPath  = ""
            Description  = ""
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
    
            cursor.execute( SelectQuery )
            ResultContentsID = cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            ContentsID  = str(NextContentsID)
            self.SetPyData(newitem, ContentsID)
            InsertParentID  = ParentID
            isDeleted  = "n"
            Author  = "Guest"
            Contact  = "Guest"
            
            UserContentsLocation = ""
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            UserContentsLocation = "top"
            cursor.execute("Select ContentsID from ProcessContentsTable where isDeleted = 'n' and ParentID = '"+ InsertParentID +"' order by cast(Sequence as decimal)")
            ResultRows = cursor.fetchall()
            for ResultRow in ResultRows:
                UserContentsLocation = ResultRow[0]
            
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            cursor.execute("Select * from ProcessContentsTable where isDeleted = 'n' and  ParentID = '"+ InsertParentID +"' and UserContentsLocation = '" + UserContentsLocation + "'")
            ResultRows = cursor.fetchall()
            Sequence  = str(len(ResultRows))
            
            
            
            InsertQuery = "insert into ProcessContentsTable ( ProcessCategory , Location , Text , ContentsPath , Description , ContentsID , ParentID , isDeleted , Author , Contact , Sequence, UserContentsLocation ) values ( '" + ProcessCategory + "','" + Location + "','" + Text + "','" + ContentsPath + "','" + Description + "','" + ContentsID + "','" + InsertParentID + "','" + isDeleted + "','" + Author + "','" + Contact + "','" + Sequence + "','" + UserContentsLocation + "');"
            cursor.execute( InsertQuery )
            con.commit()
            
            
            
            LastContentsID += 1
            NextContentsID += 1
            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
            cursor.execute( UpdateQuery )
            con.commit()
            
            
            
            #Load Selected members
            RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
            
            RelatedContentsWindow.DeleteAllItems()
            
            
            
            
            
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5]:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4]:
                        ResultRows.append(UserRow)
            

            
            idx = 0
            
            for ResultRow in ResultRows:
                
                RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
                RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
                RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
                RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
                if ResultRow[0] == "ProcessGroup":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
                elif ResultRow[0] == "Category":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
                elif ResultRow[0] == "Analysis Point":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
                elif ResultRow[0] == "Target":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
            
                if int(ResultRow[4]) < 100000 :
                    RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')
                
                idx += 1
            
            con.close()  
            

        dlg.Destroy()


    def OnItemAddSibling(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)
            
            
            

        dlg.Destroy()
        

    def OnBeginEdit(self, event):
        
        self.log.write("OnBeginEdit" + "\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one..." + "\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d" % (self.GetItemText(child), self.IsVisible(child)) + "\n")
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):
        
        self.log.write("OnEndEdit: %s %s" %(event.IsEditCancelled(), event.GetLabel()))
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.write(", You can't enter digits..." + "\n")
                event.Veto()
                return
            
        self.log.write("\n")


    def OnLeftDClick(self, event):
        """
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item and (flags & CT.TREE_HITTEST_ONITEMLABEL):
            if self.GetAGWWindowStyleFlag() & CT.TR_EDIT_LABELS:
                self.log.write("OnLeftDClick: %s (manually starting label edit)"% self.GetItemText(item) + "\n")
                self.EditLabel(item)
            else:
                self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")
        """
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        Name = self.GetItemText(item)
        
        
        comboPath = self.parent.GetParent().GetParent().combo.GetValue()
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window.NowRegistryComboSelected = comboPath.split("<")[0].strip() + "\\" + Name
        
        ComboText = self.parent.GetParent().GetParent().combo.GetValue()
        self.parent.GetParent().GetParent().OriginalCombo = ComboText
        self.parent.GetParent().GetParent().combo.SetValue(comboPath.split("<")[0].strip() + "\\" + Name)
            
        threads = []
        th = threading.Thread(target=window.SetRegistryTreeAndList, args=())
        th.start()
        threads.append(th)
        
        
        event.Skip()                
        

    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemExpanded: %s" % self.GetItemText(item) + "\n")


    def OnItemExpanding(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanding: %s" % self.GetItemText(item) + "\n")
            
        event.Skip()

        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item) + "\n")
            

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsing: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()

    
    #---Sel Change
    
        
    def OnSelChanged(self, event):

        
        
        
        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()
        """
        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s" % olditemtext + " To %s" % self.GetItemText(item) + "\n")
        """       
        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Drag..." + "\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Right Drag..." + "\n")

            event.Allow()
        

    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!" + "\n")

        event.Skip()            


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s" % self.GetItemText(item) + "\n")
        event.Skip()
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()
        

    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

        event.Skip()

        
    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s" % self.GetItemText(self.item) + "\n")
            

    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()
     
        
class RegistryPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #panel6    
        panel = wx.Panel(self, -1)
        #panel6 = wx.Panel(splitter, -1)
        
        

        
        panel1 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        
        self.ManualQueryButton = wx.BitmapButton(panel1, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/fileopen.png'))
        self.ManualQueryButton.Bind(wx.EVT_BUTTON, self.OnManualQueryButton)
        
        self.ComboList = []                 
        self.combo = wx.ComboBox(panel1, choices=self.ComboList, style=wx.TE_PROCESS_ENTER)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.combo, 1, wx.EXPAND)
        vbox.Add(self.ManualQueryButton, 0, wx.EXPAND)
        
        self.combo.Bind(wx.EVT_COMBOBOX, self.OnComboSelect)
        self.combo.Bind(wx.EVT_TEXT_ENTER, self.OnManualQueryButton)
        
        panel1.SetSizer(vbox)
        
        self.combo.SetValue("")
        





        splitter = wx.SplitterWindow(panel, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

        panel2_2 = wx.Panel(splitter, -1, style=wx.NO_BORDER)
        self.list = RegistryList(panel2_2, -1)
        self.list.SetName('RelatedContents')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(self.list, 1, wx.EXPAND)
        panel2_2.SetSizer(vbox0)
        

        self.tree = RegistryTree(splitter, -1, 
                                   style=wx.NO_BORDER,
                                   agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_ROW_LINES | CT.TR_FULL_ROW_HIGHLIGHT
                                   | CT.TR_TOOLTIP_ON_LONG_ITEMS)# | CT.TR_HIDE_ROOT)   
        self.tree.SetBackgroundColour('WHITE')
        
        
        
        
        splitter.SplitVertically(self.tree, panel2_2, 250)
        
        
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        vbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(list1, 1, wx.EXPAND)
        panel3.SetSizer(vbox1)





        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(splitter, 1, wx.EXPAND)
        vbox1.Add(panel3, 0, wx.EXPAND)
        panel.SetSizer(vbox1)
        
        
        
        
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(panel, 1, wx.EXPAND)
        self.SetSizer(vbox2)
        
        self.OriginalCombo = ""

    def OnComboSelect(self, event):
        
        SelectedText = self.combo.GetValue()
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
            
            
        window.NowRegistryComboSelected = SelectedText
            
           
        threads = []
        th = threading.Thread(target=window.SetRegistryTreeAndList, args=())
        th.start()
        threads.append(th)
        
        return 

    def OnManualQueryButton(self, event):
        SelectedText = self.combo.GetValue()
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
            
        
            
        window.NowKeyword = "[RegKey]" + SelectedText
        
        threads = []
        th = threading.Thread(target=window.ThreadActivation, args=())
        th.start()
        threads.append(th)

        
        return



#self.SetItemColumnImage(idx, 2, 6)
class FileSystemMetaList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
    

        self.parent = parent
        self.PublicContents = False
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()    
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        #print self.MainFrame.default_pfplist_path

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll_16_16.png',
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/file_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/AnPointIcon_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/TargetIcon_16_16.png',
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Export.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)   

        self.InsertColumn(0, '> Location')
        self.InsertColumn(1, 'Name')
        self.InsertColumn(2, 'inode(entry No.)')
        self.InsertColumn(3, 'mtime')
        self.InsertColumn(4, 'atime')
        self.InsertColumn(5, 'ctime')
        self.InsertColumn(6, 'crtime')
        self.InsertColumn(7, 'size')
        self.InsertColumn(8, 'Full path')
        self.InsertColumn(9, '')
        self.InsertColumn(10, '')
        """
        self.InsertColumn(2, 'ctime')
        self.InsertColumn(3, 'mtime')
        self.InsertColumn(4, 'atime')
        self.InsertColumn(5, '$FN ctime')
        self.InsertColumn(6, '$FN mtime')
        self.InsertColumn(7, '$FN atime')
        self.InsertColumn(8, '$Std ctime')
        self.InsertColumn(9, '$Std mtime')
        self.InsertColumn(10, '$Std atime')
        """
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, 250)
        self.SetColumnWidth(2, 110)
        self.SetColumnWidth(3, 160)
        self.SetColumnWidth(4, 160)
        self.SetColumnWidth(5, 160)
        self.SetColumnWidth(6, 160)
        self.SetColumnWidth(7, 120)
        self.SetColumnWidth(8, 300)
        self.SetColumnWidth(9, 0)
        self.SetColumnWidth(10, 0)
        
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
 

 
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        #self.SelectedIndex = event.GetIndex()
        
        PopupMenu = wx.Menu()        
        
        CheckAll  = PopupMenu.Append(-1, "Check All")
        self.Bind(wx.EVT_MENU, self.OnCheckAll, CheckAll)
        UnCheckAll  = PopupMenu.Append(-1, "UnCheck All")
        self.Bind(wx.EVT_MENU, self.OnUnCheckAll, UnCheckAll)
        RawCopy  = PopupMenu.Append(-1, "Extract(raw copy, seleted item)")
        self.Bind(wx.EVT_MENU, self.RawCopy_SelectedTarget, RawCopy)
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPoint())
    
    
    def RawCopy_SelectedTarget(self, event):
        
        threads = []
        th = threading.Thread(target=self.ThreadExtract, args=())
        th.start()
        threads.append(th)

        return
    
    
    def ThreadExtract(self):
        #리스트에서 체크 목록 가져오기
        SelectedModuleList = []
            
        for index in range(self.GetItemCount()):
            if self.IsChecked(index): 
                SelectedModuleList.append([self.GetItem(index, 8).GetText() + "\\" + self.GetItem(index, 1).GetText(),
                                           self.GetItem(index, 2).GetText()])     #"Find selected Data"
        
        #파일 목록의 임시 파일 생성 및 추출 모듈 구동
        TempFileName = "./PFPModule/UpdateTemp/temp_extractlist_FSLookup_" + str(time.time()) + ".dat"
        fp = open(TempFileName, 'w')
        for Item in SelectedModuleList:
                
            Keyword = Item[0]
            iNode = Item[1]
            #RetList = self.SetPath(Keyword)
            
            #Make abs paths from env variable
            #for Keyword in RetList: fp.write(Keyword + "\t" + iNode + "\n")
            fp.write(Keyword + "\t" + iNode + "\n")
                
        fp.close()
        
        #텟스트 파일 넘기며, Extractor 구동
        if self.MainFrame.isCaseSet == True: 
            if "(img)" in self.MainFrame.CaseDBPath:    Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, self.MainFrame.CaseDBPath, "True"])
            else:                                       Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, self.MainFrame.CaseDBPath, "False"])
        else:                                           Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, "None"])
        
        while Process.poll() is None: 
            time.sleep(0.5)    
            
        os.system( "del " + TempFileName.replace("/", "\\") )
        
    def OnCheckAll(self,event):
        for index in range(self.GetItemCount()):
            if not self.IsChecked(index): 
                self.ToggleItem(index)
        
        return
    
    def OnUnCheckAll(self,event):
        for index in range(self.GetItemCount()):
            if self.IsChecked(index): 
                self.ToggleItem(index)
        
        return
        
    def ConvertToPublicContents(self, event):
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        
        con = sqlite3.connect( self.User_Process_SQLite )
        cursor = con.cursor()
        
        
        
        #sharing select    
        SelectQuery = "select * from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        insertRow = cursor.fetchone()

        #module list insert
        InsertQuery = "insert into ProcessContentsTable values ( "

        fieldidx = 0
        for field in insertRow:
            
            if field == None:
                InsertQuery += "''"
            else:
                InsertQuery += "'" + field + "'"
            if fieldidx < len(insertRow)-1:
                InsertQuery += ","
                
            fieldidx += 1
            
        InsertQuery += ");"
        
        
        
        SelectQuery = "select ParentID, UserContentsLocation from ProcessContentsTable where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        ParentID = UserRow[0]
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        con = sqlite3.connect( self.Public_Process_SQLite )
        cursor = con.cursor()
        
        
        
        SelectQuery = "select Sequence from ProcessContentsTable where ContentsID = '" + UserRow[1] + "'"

        cursor.execute( SelectQuery )
        UserRow = cursor.fetchone()
        
        try:
            Sequence = UserRow[0]
        except:
            Sequence = '-1'
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) >= " + str(int(Sequence)+1) + " and ParentID = '" + ParentID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) + 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()
        
        
        
        #print InsertQuery
        cursor.execute( InsertQuery )        
        con.commit()
        
        
        
        
        
        SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
        
        cursor.execute( SelectQuery )
        ResultContentsID = cursor.fetchone()
        LastContentsID = int(ResultContentsID[0])
        NextContentsID = int(ResultContentsID[1])
        
        
        UpdateQuery = "Update ProcessContentsTable set isDeleted = 'n', UserContentsLocation = 'public', Sequence = '" + str(int(Sequence)+1) + "' ,ContentsID = '" + str(NextContentsID) + "' where ContentsID = '" + self.GetItem(self.SelectedIndex, 3).GetText() + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        self.SetStringItem(self.SelectedIndex, 3, str(NextContentsID))
        
        
        
        LastContentsID += 1
        NextContentsID += 1
        UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
        cursor.execute( UpdateQuery )
        con.commit()
        
        
        
        
        
        self.SetItemBackgroundColour(self.SelectedIndex, '#ffffff')
        
        
        return    
    
    

    def OnSize(self, event):
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, 250)
        self.SetColumnWidth(2, 110)
        self.SetColumnWidth(3, 160)
        self.SetColumnWidth(4, 160)
        self.SetColumnWidth(5, 160)
        self.SetColumnWidth(6, 160)
        self.SetColumnWidth(7, 120)
        self.SetColumnWidth(8, 300)
        self.SetColumnWidth(9, 0)
        self.SetColumnWidth(10, 0)
        event.Skip()
        
        return
    
    
    
    def ThreadActivation(self):

        window0 = self.MainFrame.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.MainFrame.FindWindowByName('AnalysisPointOnList')
        window2 = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window3 = self.MainFrame.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.MainFrame.FindWindowByName('AnalysisDescriptionOnList')
        Modulewindow = self.MainFrame.FindWindowByName('ModuleListOnList')
        #window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        
        window2.ActivationFlag = True
        
        
        if self.Type == "File":

            #Check Disk space
            #################
            ResultLines = []
            cmdARGS = ["fsutil", "volume", "diskfree", "q:"]
                            
            self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.pipe.stdin.close()
 
            self.NowTerminalProcessPid = self.pipe.pid 
    
            while self.pipe.poll() == None:
                result = self.pipe.stdout.readline().decode('cp949')
                if result.strip() != "":
                    ResultLines.append(result.strip())
                    
            result = self.pipe.stdout.readline().decode('cp949')
            if result.strip() != "":
                ResultLines.append(result.strip())

            #print ResultLines

            #wx.MessageBox("File size : " + str(int(Size)/1024) + " KB \nResidual space : \t" + str(ResultLines[0].split(":")[1].strip()) + " KB \nDisk space : \t\t" + str(ResultLines[1].split(":")[1].strip()) + " KB")
            
            if int(self.FileSize)/1024 <= int(ResultLines[0].split(":")[1].strip()):
            
                TempPath = os.path.abspath(".") + "\\Temp\\"
                if self.MainFrame.isCaseSet == True:
                    TempPath = self.MainFrame.CasePath + "\\Temp\\"
                else:
                    TempPath = os.path.abspath(".") + "\\Temp\\"
                
                dlg = wx.MessageDialog(None, "Are you sure to continue? \n\nFile size : " + str(int(self.FileSize)/1024) + " KB \nResidual space : \t" + str(ResultLines[0].split(":")[1].strip()) + " KB \nDisk space : \t\t" + str(ResultLines[1].split(":")[1].strip()) + " KB\nTemp path : " + TempPath, 'Info', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    #def RawCopy_by_Tsk(self, inode_in, Path, OutputPath):
                    Tempfile = TempPath + str(time.time()) + "_" +self.Name.replace(":", "_")
                    
                    #self.MainFrame.RawHandlerClass.RawCopy_by_Tsk(int(inode), Path + "\\" + Name, Tempfile)
                    threads = []
                    th = threading.Thread(target=self.MainFrame.RawHandlerClass.RawCopy_by_Tsk, args=(int(self.inode), self.Path + "\\" + self.Name, Tempfile))
                    #th = threading.Thread(target=self.MainFrame.RawHandlerClass.RawCopy_by_Tsk, args=(None, self.Path + "\\" + self.Name, Tempfile))
                    th.start()
                    threads.append(th)
                    
                    progressMax = 100
                    dialog = wx.ProgressDialog("File extracting progress", "Please wait..", progressMax, style=wx.PD_ELAPSED_TIME )
                    
                    while th.is_alive() == True:
                        wx.Sleep(1)
                        dialog.Pulse()
                    
                    dialog.Destroy()
                    
                    #change filetime
                    ######################
                    hFile = win32file.CreateFile(Tempfile.decode("cp949"), win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ, None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_BACKUP_SEMANTICS,None)
                    try:
                        win32file.SetFileTime(hFile, int(self.timeset.split(":")[2]), int(self.timeset.split(":")[1]), int(self.timeset.split(":")[0]))
                    finally:
                        win32api.CloseHandle(hFile)
                    
                    
                    Modulewindow.FileSelect(Tempfile)
                    
                    window2.ActivationFlag = False
                    return 
            
            else :
                wx.MessageBox("There is not enough disk space for temp directory.  \n\nFile size : " + str(int(self.FileSize)/1024) + " KB \nResidual space : \t" + str(ResultLines[0].split(":")[1].strip()) + " KB \nDisk space : \t\t" + str(ResultLines[1].split(":")[1].strip()) + " KB\nTemp path : " + os.path.abspath(".") + "\\Temp")
                
                window2.ActivationFlag = False
                return
            
            
            
        elif self.Type == "Dir":
            comboPath = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
            
            if self.Name == "..":
                ComboText = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
                self.parent.GetParent().GetParent().GetParent().OriginalCombo = ComboText
                window2.NowComboSelected = os.path.split(comboPath)[0]
                self.parent.GetParent().GetParent().GetParent().combo.SetValue(os.path.split(comboPath)[0])
            else:
                ComboText = self.parent.GetParent().GetParent().GetParent().combo.GetValue()
                self.parent.GetParent().GetParent().GetParent().OriginalCombo = ComboText
                NewCombo = ""
                if comboPath.split("<")[0].strip()[len(comboPath.split("<")[0].strip())-1] != "\\":
                    NewCombo = window2.NowComboSelected = comboPath.split("<")[0].strip() + "\\" + self.Name
                else:
                    NewCombo = window2.NowComboSelected = comboPath.split("<")[0].strip() + self.Name
                self.parent.GetParent().GetParent().GetParent().combo.SetValue(NewCombo)
                
            threads = []
            th = threading.Thread(target=window2.SetFileSystemTreeAndList, args=())
            th.start()
            threads.append(th)
            
            
            progressMax = 100
            dialog = wx.ProgressDialog("Filesystem Lookup progress", "Please wait..", progressMax, style=wx.PD_ELAPSED_TIME )
            
            while th.is_alive() == True:
                wx.Sleep(0.1)
                dialog.Pulse()
            
            dialog.Destroy()
            
            size = self.parent.GetSize()
            self.SetColumnWidth(0, 20)
            
            window2.ActivationFlag = False
            
            return 
        
           
        window2.ActivationFlag = False
        return 
    
    
        
    def OnActivated(self, event):
        
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        
        if window.ActivationFlag == True:
            wx.MessageBox("Please wait. other process is running")

        else:
            self.Type = self.GetItem(event.GetIndex(),0).GetText()
            self.Name = self.GetItem(event.GetIndex(),1).GetText()
            self.inode = self.GetItem(event.GetIndex(),2).GetText()
            self.mtime = self.GetItem(event.GetIndex(),3).GetText()
            self.atime = self.GetItem(event.GetIndex(),4).GetText()
            self.ctime = self.GetItem(event.GetIndex(),5).GetText()
            self.FileSize = self.GetItem(event.GetIndex(),7).GetText()
            self.Path = self.GetItem(event.GetIndex(),8).GetText()
            self.timeset = self.GetItem(event.GetIndex(),9).GetText()
            
            threads = []
            th = threading.Thread(target=self.ThreadActivation, args=())
            th.start()
            threads.append(th)


        return
        


class FileSystemMetaTree(CT.CustomTreeCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER|wx.WANTS_CHARS,
                 agwStyle=CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT|CT.TR_ROW_LINES|CT.TR_TWIST_BUTTONS,
                 log=None):

        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        
        self.Public_Process_SQLite = "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite"
        self.User_Process_SQLite = "./UserModule/userdefine.process.sqlite"
        #self.MainFrame = self.parent.GetGrandParent()
        
        self.DBPath = "" 
        self.PreSelectedID = ""
        
        alldata = dir(CT)

        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)

        self.events = events
        self.styles = treestyles
        self.item = None
        
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        self.folder_close_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_uncheck_16_16.png'))
        self.folder_open_idx = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/folder_check_16_16.png'))
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.

        self.root = self.AddRoot("FileSystem Meta Lookup Result")

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SetItemImage(self.root, self.folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root, self.folder_open_idx, wx.TreeItemIcon_Expanded)
        
        self.PreSelectedItem = self.root

        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)
        
        if not hasattr(mainframe, "leftpanel"):
            self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)
        
        
        self.DoSelectItem(self.root)
        

    def LoadData(self, ParentID, ParentNode = None):
    
        
        if ParentNode != None:
            

            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                if PublicRow[0] == "ProcessGroup":
                    ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                        ResultRows.append(UserRow)
            
            
            
            
            
            
            for ResultRow in ResultRows:
            
                child = self.AppendItem(ParentNode, ResultRow[1])
    
                self.SetPyData(child, ResultRow[4])
                self.SetItemImage(child, self.folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.folder_open_idx, wx.TreeItemIcon_Expanded)
                try:
                    if int(ResultRow[4]) < 100000:
                        self.SetItemBackgroundColour(child, '#e6f1f5')
                except:
                    print ""
            
                
                
                
                
                
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubPublicResultRows = cursor.fetchall()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubUserResultRows = cursor.fetchall()
                
                SubResultRows = []
                
                
                for UserRow in SubUserResultRows:
                    if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                        SubResultRows.append(UserRow)
                
                
                for PublicRow in SubPublicResultRows:
                    if PublicRow[0] == "ProcessGroup":
                        SubResultRows.append(PublicRow)
                    
                    for UserRow in SubUserResultRows:
                        if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                            SubResultRows.append(UserRow)
                
                

        
                if len(SubResultRows) > 0:      
                    self.LoadData( ResultRow[4], child)
                    
                        
            
        else:
            
            self.DeleteAllItems()
            
            
            self.UserDBPath = self.User_Process_SQLite
            
            self.PublicDBPath = self.Public_Process_SQLite
    
    
            #print "\n\n\n\\ this is !!!" + self.DBPath + "\n\n\n\\"
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where Location = 'ProcessRoot' and ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            ResultRows = cursor.fetchall()
            
            con.close()
            
            for ResultRow in ResultRows:
                
                self.root = self.AddRoot(ResultRow[1])
    
                if not(self.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
                    self.SetPyData(self.root, ResultRow[4])
                    self.RootParentID = ResultRow[4]
                    self.SetItemImage(self.root, self.folder_close_idx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(self.root, self.folder_open_idx, wx.TreeItemIcon_Expanded)

        
                con = sqlite3.connect( self.PublicDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubPublicResultRows = cursor.fetchall()
                
                con = sqlite3.connect( self.UserDBPath )
                cursor = con.cursor()
                
                cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation  from ProcessContentsTable where ParentID = '" + ResultRow[4] + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
                SubUserResultRows = cursor.fetchall()
                
                SubResultRows = []
                
                
                for UserRow in SubUserResultRows:
                    if "top" in UserRow[5] and UserRow[0] == "ProcessGroup":
                        SubResultRows.append(UserRow)
                
                
                for PublicRow in SubPublicResultRows:
                    if PublicRow[0] == "ProcessGroup":
                        SubResultRows.append(PublicRow)
                    
                    for UserRow in SubUserResultRows:
                        if UserRow[5] == PublicRow[4] and UserRow[0] == "ProcessGroup":
                            SubResultRows.append(UserRow)

        
                if len(SubResultRows) > 0:
                    self.LoadData( ResultRow[4], self.root)
                    
                
            con.close()
            
            
            
            
            
            #Load Selected members
            RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
            
            RelatedContentsWindow.DeleteAllItems()
            
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + self.RootParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + self.RootParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5]:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4]:
                        ResultRows.append(UserRow)
                        
                        
            
            
            idx = 0
            
            for ResultRow in ResultRows:
                
                RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
                if ResultRow[0] == "ProcessGroup":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
                elif ResultRow[0] == "Category":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
                elif ResultRow[0] == "Analysis Point":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
                elif ResultRow[0] == "Target":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
                RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
                RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
                RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
                
                #try:
                if int(ResultRow[4]) < 100000 :
                    RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')
    
                
                idx += 1
            
            con.close()
            
            self.PreSelectedID = self.GetPyData(self.root)
            self.PreSelectedItem = self.root

        


        """
        textctrl = wx.TextCtrl(self, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        self.gauge = wx.Gauge(self, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(0)
        combobox = wx.ComboBox(self, -1, choices=["That", "Was", "A", "Nice", "Holyday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)

        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        lenArtIds = len(ArtIDs) - 2
        """

        """
        for x in range(15):
            if x == 1:
                child = self.AppendItem(self.root, "Item %d" % x)# + "\nHello World\nHappy wxPython-ing!")
                self.SetItemBold(child, True)
            else:
                child = self.AppendItem(self.root, "Item %d" % x)
            self.SetPyData(child, None)
            self.SetItemImage(child, folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, folder_open_idx, wx.TreeItemIcon_Expanded)
            

            if random.randint(0, 3) == 0:
                self.SetItemLeftImage(child, random.randint(0, lenArtIds))

            for y in range(5):
                if y == 0 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2, wnd=self.gauge)
                elif y == 1 and x == 2:
                    last = self.AppendItem(child, "Item %d-%s" % (x, chr(ord("a")+y)), ct_type=1, wnd=textctrl)
                    if random.randint(0, 3) == 1:
                        self.SetItem3State(last, True)
                        
                elif 2 < y < 4:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
                elif y == 4 and x == 1:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), wnd=combobox)
                else:
                    last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2)
                    
                self.SetPyData(last, None)
                self.SetItemImage(last, folder_close_idx, wx.TreeItemIcon_Normal)
                self.SetItemImage(last, folder_open_idx, wx.TreeItemIcon_Expanded)

                if random.randint(0, 3) == 0:
                    self.SetItemLeftImage(last, random.randint(0, lenArtIds))
                    
                for z in range(5):
                    if z > 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
                        if random.randint(0, 3) == 1:
                            self.SetItem3State(item, True)
                    elif 0 < z <= 2:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=2)
                    elif z == 0:
                        item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                        self.SetItemHyperText(item, True)
                    self.SetPyData(item, None)
                    self.SetItemImage(item, folder_close_idx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(item, folder_open_idx, wx.TreeItemIcon_Expanded)

                    if random.randint(0, 3) == 0:
                        self.SetItemLeftImage(item, random.randint(0, lenArtIds))

        
            
        """


        return

    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()
        
        evt = "CT." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, None)
                self.Bind(wx.EVT_RIGHT_UP, None)
            self.Bind(eval(evt), binder)
        else:
            self.Bind(eval(evt), None)
            if evt == "CT.EVT_TREE_BEGIN_RDRAG":
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                style = style | eval("CT." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)
            

    def OnCompareItems(self, item1, item2):
        
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        
        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1

    
    def OnIdle(self, event):

        """
        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()
        """
        return 

    #---RightDown

    def OnRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        if item:
            
            self.current = item
            
            self.SelectItem(item)
            
            
            PopupMenu = wx.Menu()        
        
            OnDelete = PopupMenu.Append(wx.ID_ANY, "Delete Group")
            OnAddSub = PopupMenu.Append(wx.ID_ANY, "Add Sub Group")
            #OnAddSibling = PopupMenu.Append(wx.ID_ANY, "Add Sibling Group")
    
            #---Set Menu bar---
            
            
            #self.PopUpSelectedRow = event.GetRow()
            self.Bind(wx.EVT_MENU, self.OnItemDelete, OnDelete)
            self.Bind(wx.EVT_MENU, self.OnItemAddSub, OnAddSub)
            #self.Bind(wx.EVT_MENU, self.OnItemAddSibling, OnAddSibling)
            
            self.PopupMenu(PopupMenu, event.GetPosition())
            
            """
            self.item = item
            self.log.write("OnRightClick: %s, %s, %s" % (self.GetItemText(item), type(item), item.__class__) + "\n")
            """
            

    def OnRightUp(self, event):
        
        item = self.item
        
        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return


        """
        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)

        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)
        
        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}
        
        menu = wx.Menu()

        item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()
        if haswin:
            enabled = self.GetItemWindowEnabled(item)
            if enabled:
                strs = "Disable Associated Widget"
            else:
                strs = "Enable Associated Widget"
        else:
            strs = "Enable Associated Widget"
        item6 = menu.Append(wx.ID_ANY, strs)

        if not haswin:
            item6.Enable(False)

        item7 = menu.Append(wx.ID_ANY, "Disable Item")
        
        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        
        self.PopupMenu(menu)
        menu.Destroy()
        """

    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)
        dlg.Destroy()


    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)
        
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            
        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        

    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])


    def OnEnableWindow(self, event):

        enable = self.GetItemWindowEnabled(self.current)
        self.SetItemWindowEnabled(self.current, not enable)


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        

    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()        
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], CT.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], CT.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], CT.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], CT.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "CustomTreeCtrlDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                
        
    #---Delete Item
    def OnItemDelete(self, event):

        
        colour = self.GetItemBackgroundColour(self.current)
        if colour != '#e6f1f5' and self.MainFrame.isPFPOnManaging != True:
            wx.MessageBox("Can not delete the public contents")
            return
        

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None
        
        
        CurrentID = self.GetPyData(self.item)
        
        DBPath = ""
        
        if colour == '#e6f1f5':
            DBPath = self.UserDBPath
        else:
            DBPath = self.PublicDBPath
            
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        UpdateQuery = "update ProcessContentsTable set isDeleted = 'y' where ContentsID = '" + CurrentID + "'"
        cursor.execute(UpdateQuery)
        con.commit()
        
        
        
        SelectQuery = "select ParentID, Sequence from ProcessContentsTable where ContentsID = '" + CurrentID + "'"
        cursor.execute( SelectQuery )
        ResultRow = cursor.fetchone()
        
        
        
        SelectQuery = "select Sequence, ContentsID from ProcessContentsTable where cast(Sequence as integer) > " + ResultRow[1] + " and ParentID ='" + ResultRow[0] + "'"
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        for Row in ResultList:
    
            UpdateQuery = "update ProcessContentsTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
    
            cursor.execute( UpdateQuery )
            con.commit()

        con.close()
        

    #---Add Tree item

    def OnItemAddSub(self, event):

        dlg = wx.TextEntryDialog(self, "Please enter the new process group", 'group naming', 'insert new..')
        
        
        
        

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            
            self.SetItemImage(newitem, self.folder_close_idx, wx.TreeItemIcon_Normal)
            self.SetItemImage(newitem, self.folder_open_idx, wx.TreeItemIcon_Expanded)
            self.SetItemBackgroundColour(newitem, '#e6f1f5')
            self.EnsureVisible(newitem)
            
            
            
            #insert
            ParentID = self.GetPyData(self.current)
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            ProcessCategory = "Process" 
            Location  = "ProcessGroup"
            Text  = newname
            ContentsPath  = ""
            Description  = ""
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
    
            cursor.execute( SelectQuery )
            ResultContentsID = cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            ContentsID  = str(NextContentsID)
            self.SetPyData(newitem, ContentsID)
            InsertParentID  = ParentID
            isDeleted  = "n"
            Author  = "Guest"
            Contact  = "Guest"
            
            UserContentsLocation = ""
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            UserContentsLocation = "top"
            cursor.execute("Select ContentsID from ProcessContentsTable where isDeleted = 'n' and ParentID = '"+ InsertParentID +"' order by cast(Sequence as decimal)")
            ResultRows = cursor.fetchall()
            for ResultRow in ResultRows:
                UserContentsLocation = ResultRow[0]
            
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            cursor.execute("Select * from ProcessContentsTable where isDeleted = 'n' and  ParentID = '"+ InsertParentID +"' and UserContentsLocation = '" + UserContentsLocation + "'")
            ResultRows = cursor.fetchall()
            Sequence  = str(len(ResultRows))
            
            
            
            InsertQuery = "insert into ProcessContentsTable ( ProcessCategory , Location , Text , ContentsPath , Description , ContentsID , ParentID , isDeleted , Author , Contact , Sequence, UserContentsLocation ) values ( '" + ProcessCategory + "','" + Location + "','" + Text + "','" + ContentsPath + "','" + Description + "','" + ContentsID + "','" + InsertParentID + "','" + isDeleted + "','" + Author + "','" + Contact + "','" + Sequence + "','" + UserContentsLocation + "');"
            cursor.execute( InsertQuery )
            con.commit()
            
            
            
            LastContentsID += 1
            NextContentsID += 1
            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
            cursor.execute( UpdateQuery )
            con.commit()
            
            
            
            #Load Selected members
            RelatedContentsWindow = self.GetParent().FindWindowByName('RelatedContents')
            
            RelatedContentsWindow.DeleteAllItems()
            
            
            
            
            
            con = sqlite3.connect( self.PublicDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            PublicResultRows = cursor.fetchall()
            
            con = sqlite3.connect( self.UserDBPath )
            cursor = con.cursor()
            
            cursor.execute("Select Location, Text, ContentsPath, Description, ContentsID, UserContentsLocation from ProcessContentsTable where ParentID = '" + ParentID + "' and isDeleted = 'n' order by cast(Sequence as decimal)")
            UserResultRows = cursor.fetchall()
            
            ResultRows = []
            
            
            for UserRow in UserResultRows:
                if "top" in UserRow[5]:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[5] == PublicRow[4]:
                        ResultRows.append(UserRow)
            

            
            idx = 0
            
            for ResultRow in ResultRows:
                
                RelatedContentsWindow.InsertStringItem(idx, ResultRow[0])
                RelatedContentsWindow.SetStringItem(idx, 1, ResultRow[1])
                RelatedContentsWindow.SetStringItem(idx, 2, ResultRow[2])
                RelatedContentsWindow.SetStringItem(idx, 3, ResultRow[4])
                if ResultRow[0] == "ProcessGroup":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 0)
                elif ResultRow[0] == "Category":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 1)
                elif ResultRow[0] == "Analysis Point":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 2)
                elif ResultRow[0] == "Target":
                    RelatedContentsWindow.SetItemColumnImage(idx, 0, 3)
            
                if int(ResultRow[4]) < 100000 :
                    RelatedContentsWindow.SetItemBackgroundColour(idx, '#e6f1f5')
                
                idx += 1
            
            con.close()  
            

        dlg.Destroy()


    def OnItemAddSibling(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)
            
            
            

        dlg.Destroy()
        

    def OnBeginEdit(self, event):
        
        self.log.write("OnBeginEdit" + "\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one..." + "\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d" % (self.GetItemText(child), self.IsVisible(child)) + "\n")
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):
        
        self.log.write("OnEndEdit: %s %s" %(event.IsEditCancelled(), event.GetLabel()))
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.write(", You can't enter digits..." + "\n")
                event.Veto()
                return
            
        self.log.write("\n")


    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        Name = self.GetItemText(item)
        
        
        comboPath = self.parent.GetParent().GetParent().combo.GetValue()
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        window.NowComboSelected = comboPath.split("<")[0].strip() + "\\" + Name
        
        ComboText = self.parent.GetParent().GetParent().combo.GetValue()
        self.parent.GetParent().GetParent().OriginalCombo = ComboText
        self.parent.GetParent().GetParent().combo.SetValue(comboPath.split("<")[0].strip() + "\\" + Name)
            
        threads = []
        th = threading.Thread(target=window.SetFileSystemTreeAndList, args=())
        th.start()
        threads.append(th)
        
        event.Skip()                
        

    def OnItemExpanded(self, event):
        
        item = event.GetItem()
        #if item:
        #    self.log.write("OnItemExpanded: %s" % self.GetItemText(item) + "\n")


    def OnItemExpanding(self, event):
        
        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanding: %s" % self.GetItemText(item) + "\n")
            
        event.Skip()

        
    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item) + "\n")
            

    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsing: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()

    
    #---Sel Change
    
        
    def OnSelChanged(self, event):

        
        
        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()
        """
        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s" % olditemtext + " To %s" % self.GetItemText(item) + "\n")
        """       
        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Drag..." + "\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            #self.log.write("Beginning Right Drag..." + "\n")

            event.Allow()
        

    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!" + "\n")

        event.Skip()            


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s" % self.GetItemText(item) + "\n")
        event.Skip()
        

    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()
        

    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")
    
        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()
        
        
    def OnActivate(self, event):
        
        if self.item:
            self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

        event.Skip()

        
    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s" % self.GetItemText(self.item) + "\n")
            

    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()
     
        
class FileSystemMetaPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #panel6    
        panel = wx.Panel(self, -1)
        #panel6 = wx.Panel(splitter, -1)
        
        

        #Create buttons
        ###############
        panel1 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        self.ManualQueryButton = wx.BitmapButton(panel1, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/go_button_16_16.png'))
        self.ManualQueryButton.Bind(wx.EVT_BUTTON, self.OnManualQueryButton)
        self.ManualQueryButton.SetToolTip(wx.ToolTip("Get result"))
        
        self.GetPathButton = wx.BitmapButton(panel1, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/fileopen.png'))
        self.GetPathButton.Bind(wx.EVT_BUTTON, self.OnGetPathButton)
        self.GetPathButton.SetToolTip(wx.ToolTip("Set new path"))
        
        #Create Combo
        ###############
        self.ProcessList = []     
        self.combo = wx.ComboBox(panel1, choices=self.ProcessList, style=wx.TE_PROCESS_ENTER)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.combo, 1, wx.EXPAND)
        vbox.Add(self.ManualQueryButton, 0, wx.EXPAND)
        vbox.Add(self.GetPathButton, 0, wx.EXPAND)
        
        self.combo.Bind(wx.EVT_COMBOBOX, self.OnComboSelect)
        self.combo.Bind(wx.EVT_TEXT_ENTER, self.OnManualQueryButton)
        panel1.SetSizer(vbox)
        
        

        splitter = wx.SplitterWindow(panel, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

        panel2_2 = wx.Panel(splitter, -1, style=wx.NO_BORDER)
        self.list = FileSystemMetaList(panel2_2, -1)
        self.list.SetName('RelatedContents')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(self.list, 1, wx.EXPAND)
        panel2_2.SetSizer(vbox0)
        

        self.tree = FileSystemMetaTree(splitter, -1, 
                                   style=wx.NO_BORDER,
                                   agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | CT.TR_ROW_LINES | CT.TR_FULL_ROW_HIGHLIGHT
                                   | CT.TR_TOOLTIP_ON_LONG_ITEMS)# | CT.TR_HIDE_ROOT)   
        self.tree.SetBackgroundColour('WHITE')
        
        
        
        
        splitter.SplitVertically(self.tree, panel2_2, 250)
        
        
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        vbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(list1, 1, wx.EXPAND)
        panel3.SetSizer(vbox1)





        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(splitter, 1, wx.EXPAND)
        vbox1.Add(panel3, 0, wx.EXPAND)
        panel.SetSizer(vbox1)
        
        
        
        
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(panel, 1, wx.EXPAND)
        self.SetSizer(vbox2)
        
        self.OriginalCombo = ""

    def OnComboSelect(self, event):
        
        
        SelectedText = self.combo.GetValue()
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        
        if window.ActivationFlag == True:
            wx.MessageBox("Please wait. other process is running")

        else:
            window.NowKeyword = SelectedText
            
            threads = []
            th = threading.Thread(target=window.ThreadActivation, args=())
            th.start()
            threads.append(th)


        return
        
    
    """
    def ThreadComboSelect(self):
        
        
        
        SelectedText = self.combo.GetValue()
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
        windowTargetStatusBar = self.MainFrame.FindWindowByName('VestigeLocationStatusbar')
            
        window.NowComboSelected = SelectedText
            
            
        
        threads = []
        th = threading.Thread(target=window.SetFileSystemTreeAndList, args=())
        th.start()
        threads.append(th)
        
        max = 0
        while th.is_alive() == True:
            
            LogKeyword = 'FS Lookup(Combo Select) = ' + SelectedText + " ["
            for idx in range(0, max):
                LogKeyword += "."
            LogKeyword += "]"
            
            time.sleep(0.5)
        
            windowTargetStatusBar.SetLine(LogKeyword)
            
            max += 1
            if max == 10:
                max = 0
            #th.join()
        
        windowTargetStatusBar.SetLine("Complete.")
        
        return 
    """

    def OnGetPathButton(self, event):
        
        dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
        TargetFolder = ""
        if dlg.ShowModal() == wx.ID_OK:
            TargetFolder = dlg.GetPath().encode('cp949') 
            self.combo.SetValue(TargetFolder)
            
        
        return
    
    
    def OnManualQueryButton(self, event):
        
        SelectedText = self.combo.GetValue()
        
        window = self.MainFrame.FindWindowByName('VestigeLocationOnList')
            
        
            
        window.NowKeyword = SelectedText
        
        threads = []
        th = threading.Thread(target=window.ThreadActivation, args=())
        th.start()
        threads.append(th)
            
        
        return





#---###################################
#---PFP Main Frame Clases End
#---###################################



class PFPGui(wx.Frame):
    
    ImportFlag = "NotImporting"
    
    def __init__(self, parent, id, title):
        
        wx.Frame.__init__(self, parent, id, title, pos=(100,100), size=(1100,600))
        
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.tbIcon = PFPIcon(self)
    
        
        
        try:
            #---initial setting
            #---###################
            self.System_inode = []
            
            UtilClass = Util()
            
            PopupMenuLocation = ""
            
            reload(sys)
            sys.setdefaultencoding('cp949')
            
                                               
            con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RfUmVzcG9uc2UucGZwbGlzdC5zcWxpdGU="))#"./PFPModule/PFPLib/PublicPFPList/public.1.First_Response.pfplist.sqlite" )
            cursor = con.cursor()
            
            SelectQuery = base64.b64decode("c2VsZWN0IFRleHQgZnJvbSBBblBvaW50VGFibGUgd2hlcmUgQ29udGVudHNJRCA9ICcxMDAwMjIn")#"select Text from AnPointTable where ContentsID = '100022'"
            cursor.execute(SelectQuery)
            
            Result = cursor.fetchone()
            con.close()
    
            self.DecodedDummy = base64.b64decode(Result[0])
            
            ciper = UtilClass.DummyCyber(self.DecodedDummy, "what a good tools", "")
            plain = UtilClass.DummyCyber(self.DecodedDummy, "", ciper)
            plain = UtilClass.DummyCyber(self.DecodedDummy, "", "wmRImNzDld98uLdBnh9kHRk4HhZBwvIKvlrn716X5fQ=")
    
    
    
    
    
    
    
    
            #---Authorization check
            #---###################
            self.isPFPOnManaging = False
            self.isPremium = False
            self.isafirst = False
            try:
                if os.path.isfile("./UserModule/wmRImN2zDld98u2L3dBnh39kHRk4HhZ5BwvIKvlrn716X35fQ.dat"):
                    self.isPFPOnManaging = True
                    self.isPremium = True
            except:
                self.isPFPOnManaging = False
                self.isPremium = False
            
            
            
            
            try:
                if os.path.isfile("./PFPModule/UpdateTemp/wmRmNzld98uLdnh9kRk4HhZBwvIKvrn716XfQ.dat") or os.path.isfile("./UserModule/wmRmNzld98uLdnh9kRk4HhZBwvIKvrn716XfQ.dat"):
                    self.isPremium = True
            except:
                self.isPremium = False
            
            
            
            try:
                if os.path.isfile("./PFPModule/UpdateTemp/wmRAmNz-ld98uFLdInh9kRRk4SHhZBwvTIKvrn716XfQ.dat") or os.path.isfile("./UserModule/wmRAmNz-ld98uFLdInh9kRRk4SHhZBwvTIKvrn716XfQ.dat"):
                    self.isPremium = True
                    self.isafirst = False
            except:
                self.isPremium = False
                self.isafirst = False
            
            
            
            #---initial variable..
            ################################
            SelfTest = PFPUtil()
            self.ReferenceViewMode = True
            
            self.changedir = ""
            self.cmdhistory = []
            self.cmdhistorypos = -1
            self.filepos = 0
            self.PreTab = ""
            self.RawHandlerClass = RawHandler()
            
            
            
            
            
            #---read config file and variable setting
            #---########################################
            
            #set variable 
            self.public_pfplist_path = ""
            self.updatemain = ""
            self.updateserver = ""
            self.autoupdate = ""
            self.default_pfplist_path = ""
            self.default_modulelistDB_path = ""         #public modulelist
            self.default_user_modulelistDB_path = ""    #user modulelist
            self.default_user_processDB_path = "./UserModule/userdefine.process.sqlite"
            self.interpreter_path = ""
            self.interpreter_path_gui = ""
            self.user = ""
            self.contact = ""
            self.AnalysisTargetRoot = "C:"
            self.PublicPFPListPath = "./PFPModule/PFPLib/PublicPFPList/"
            
            #read config file
            config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "r")
            filelines = config_fp.readlines()
            config_fp.close()
            for line in filelines:
                if "update main(url||ip)" in line:
                    self.updatemain =  line.split(">")[1].strip("\"").strip("\n")
                elif "update dir(url||ip)" in line:
                    self.updateserver =  line.split(">")[1].strip("\"").strip("\n")
                elif "autoupdate" in line:
                    self.autoupdate =  line.split(">")[1].strip("\"").strip("\n")
                elif "default public pfplist path" in line:
                    self.public_pfplist_path = line.split(">")[1].strip("\"").strip("\n")
                    self.live_public_pfplist_path = line.split(">")[1].strip("\"").strip("\n")
                elif "default user pfplist path" in line:
                    self.default_pfplist_path =  line.split(">")[1].strip("\"").strip("\n")
                    self.live_user_pfplist_path =  line.split(">")[1].strip("\"").strip("\n")
                elif "default public modulelistDB path" in line:
                    self.default_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
                elif "default user modulelistDB path" in line:
                    self.default_user_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
                elif "interpreter path(win)" in line:
                    self.interpreter_path =  line.split(">")[1].strip("\"").strip("\n")
                elif "interpreter path(wingui)" in line:
                    self.interpreter_path_gui =  line.split(">")[1].strip("\"").strip("\n")
                elif "user(pfp id)" in line:
                    self.user =  line.split(">")[1].strip("\"").strip("\n")
                elif "contact" in line:
                    self.contact =  line.split(">")[1].strip("\"").strip("\n")
    
            
            
            
            
            
            
            
            
           
    
            
            #---#############################################################################################################################
            #---UI Setting Start                                                                                                            #
            #---############################################################################################################################# 
            
            
            
            
            #---UI-Setting
            #---##############
            
            
            ico = wx.Icon('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/tray_p1.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
            
            
            
            #splitters..
            hbox = wx.BoxSizer(wx.VERTICAL)
            splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            splitterUpper = wx.SplitterWindow(splitter, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            splitterLower = wx.SplitterWindow(splitter, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            splitter2 = wx.SplitterWindow(splitterUpper, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            splitter3 = wx.SplitterWindow(splitter2, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            splitter41 = wx.SplitterWindow(splitter3, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
            
            
            
            
            #panel0 - Analysis Category
            panel0 = wx.Panel(splitterUpper, -1)
    
            panel01 = wx.Panel(panel0, -1, size=(-1, 25))
            panel01.SetBackgroundColour('BLACK')
            st0 = wx.StaticText(panel01, -1, 'Analysis Category', (5, 5))
            st0.SetForegroundColour('WHITE')
    
            panel02 = wx.Panel(panel0, -1, style=wx.BORDER_SUNKEN)
            vbox00 = wx.BoxSizer(wx.VERTICAL)
            list0 = AnalysisCategoryList(panel02, -1)
            list0.SetName('AnalysisCategoryOnList')
            
            vbox00.Add(list0, 1, wx.EXPAND)
            panel02.SetSizer(vbox00)
            
            panel03 = wx.Panel(panel0, -1, size=(25, -1), style=wx.NO_BORDER)
            
            self.AnListFileOpen = wx.BitmapButton(panel03, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/fileopen.png'))
            self.AnListModify = wx.BitmapButton(panel03, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Modify.png'))
            
            self.PublicPFPList = []
            """
            for root, dirs, files in os.walk("./PFPModule/PFPLib/PublicPFPList"):
                for file in files:
                    if "public" in file and "pfplist.sqlite" in file:
                        self.PublicPFPList.append(file.replace("public.","").replace(".pfplist.sqlite",""))
            """
            self.PublicPFPList.append("1.First_Response")
            self.PublicPFPList.append("2.Artifact_Analysis")
            self.PublicPFPList.append("UserDefine(TechGroup)")                  
            self.pfplist_category_combo = wx.ComboBox(panel03, choices=self.PublicPFPList)
            
            vbox01 = wx.BoxSizer(wx.HORIZONTAL)
            
            vbox01.Add(self.AnListFileOpen, 0, wx.EXPAND)
            vbox01.Add(self.AnListModify, 0, wx.EXPAND)
            vbox01.Add(self.pfplist_category_combo, 1, wx.EXPAND)
            
            self.AnListFileOpen.Bind(wx.EVT_BUTTON, self.OnAnListFileOpen)
            self.AnListModify.Bind(wx.EVT_BUTTON, self.OnAnListModify)
            self.pfplist_category_combo.Bind(wx.EVT_COMBOBOX, self.OnPFPListComboSelect)
            self.pfplist_category_combo.SetValue("2.Artifact_Analysis")
            
            self.AnListFileOpen.SetToolTip(wx.ToolTip("Open PFP-List file"))
            self.AnListModify.SetToolTip(wx.ToolTip("Modify Current PFP-List file"))
    
    
            panel03.SetSizer(vbox01)
    
            vbox01 = wx.BoxSizer(wx.VERTICAL)
            vbox01.Add(panel01, 0, wx.EXPAND)
            vbox01.Add(panel02, 1, wx.EXPAND)
            vbox01.Add(panel03, 0, wx.EXPAND)
    
            panel0.SetSizer(vbox01)
    
    
    
    
            #panel1 - Analysis Point 
            panel1 = wx.Panel(splitter2, -1)
            panel11 = wx.Panel(panel1, -1, size=(-1, 25))
            panel11.SetBackgroundColour('BLACK')
            st1 = wx.StaticText(panel11, -1, 'Analysis Point', (5, 5))
            st1.SetForegroundColour('WHITE')
    
            panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
            vbox10 = wx.BoxSizer(wx.VERTICAL)
            list1 = AnalysisPointList(panel12, -1)
            list1.SetName('AnalysisPointOnList')
    
            vbox10.Add(list1, 1, wx.EXPAND)
            panel12.SetSizer(vbox10)
            
            panel13 = wx.Panel(panel1, -1, size=(25, -1), style=wx.NO_BORDER)
            self._hyper2 = hl.HyperLinkCtrl(panel13, wx.ID_ANY, "Page Link ", URL="http://naver.com")
            
            self._hyper2.SetColours("BLACK", "BLACK", "BLACK")
            self._hyper2.EnableRollover(True)
            self._hyper2.SetUnderlines(False, False, True)
            self._hyper2.SetBold(True)
            
            
            self._hyper2.SetURL("http://portable-forensics.com")
            self._hyper2.SetToolTip(wx.ToolTip("http://portable-forensics.com"))
            self._hyper2.UpdateLink()
            self.list11 = RelatedWebPageStatusbar(panel13, -1)
            self.list11.SetName('Related Web Page Status')
            vbox11 = wx.BoxSizer(wx.HORIZONTAL)
            
            vbox11.Add(self._hyper2, 0, wx.EXPAND)
            vbox11.Add(self.list11, 1, wx.EXPAND)
    
            panel13.SetSizer(vbox11)
    
            vbox11 = wx.BoxSizer(wx.VERTICAL)
            vbox11.Add(panel11, 0, wx.EXPAND)
            vbox11.Add(panel12, 1, wx.EXPAND)
            vbox11.Add(panel13, 0, wx.EXPAND)
    
            panel1.SetSizer(vbox11)
    
    
    
    
            #panel2 - Vestige Location
            panel2 = wx.Panel(splitter41, -1)
            #panel2 = wx.Panel(splitter3, -1)
            panel21 = wx.Panel(panel2, -1, size=(-1, 25))
            panel21.SetBackgroundColour('BLACK')
            st2 = wx.StaticText(panel21, -1, 'Target', (5, 5))
            st2.SetForegroundColour('WHITE')
    
            panel22 = wx.Panel(panel2, -1, style=wx.BORDER_SUNKEN)
            vbox20 = wx.BoxSizer(wx.VERTICAL)
            list2 = VestigeLocationList(panel22, -1)
            list2.SetName('VestigeLocationOnList')
            vbox20.Add(list2, 1, wx.EXPAND)
            panel22.SetSizer(vbox20)
            
            panel23 = wx.Panel(panel2, -1, size=(25, -1), style=wx.NO_BORDER)
            self.VestigeLocationCheckAll = wx.BitmapButton(panel23, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll.png'))
            self.VestigeLocationReleaseAll = wx.BitmapButton(panel23, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll.png'))
            self.VestigeLocationSetTargetRoot = wx.BitmapButton(panel23, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/fileopen.png'))
            self.VestigeLocationFileExtract = wx.BitmapButton(panel23, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Export.png'))
            self.case_target_combo_list = []
            self.case_target_combo = wx.ComboBox(panel23, choices=self.case_target_combo_list)
            list21 = VestigeLocationStatusbar(panel23, -1)
            list21.SetName('VestigeLocationStatusbar')
            vbox21 = wx.BoxSizer(wx.HORIZONTAL)
            vbox21.Add(self.VestigeLocationCheckAll, 0, wx.EXPAND)
            vbox21.Add(self.VestigeLocationReleaseAll, 0, wx.EXPAND)
            vbox21.Add(self.VestigeLocationSetTargetRoot, 0, wx.EXPAND)
            #vbox21.Add(self.VestigeLocationFileExtract, 0, wx.EXPAND)
            vbox21.Add(self.case_target_combo, 0, wx.EXPAND)
            vbox21.Add(list21, 1, wx.EXPAND)
            
            self.case_target_combo.Bind(wx.EVT_COMBOBOX, self.OnCastTargetComboSelect)
            self.VestigeLocationCheckAll.Bind(wx.EVT_BUTTON, self.OnVestigeLocationCheckAll)
            self.VestigeLocationReleaseAll.Bind(wx.EVT_BUTTON, self.OnVestigeLocationReleaseAll)
            self.VestigeLocationSetTargetRoot.Bind(wx.EVT_BUTTON, self.OnVestigeLocationSetTargetRoot)
            self.VestigeLocationFileExtract.Bind(wx.EVT_BUTTON, self.OnVestigeLocationFileExtract)
            self.pfplist_category_combo.Bind(wx.EVT_COMBOBOX, self.OnPFPListComboSelect)
            
            self.VestigeLocationCheckAll.SetToolTip(wx.ToolTip("Check All"))
            self.VestigeLocationReleaseAll.SetToolTip(wx.ToolTip("Release All"))
            self.VestigeLocationSetTargetRoot.SetToolTip(wx.ToolTip("Change target root"))
            self.VestigeLocationFileExtract.SetToolTip(wx.ToolTip("Extract the selected item"))
            
            self.case_target_combo.Enable(False)
            #self.case_target_combo.SetValue("[Live              ]")
            
            #self.VestigeLocationFileExtract.Disable()
    
            panel23.SetSizer(vbox21)
    
            vbox21 = wx.BoxSizer(wx.VERTICAL)
            vbox21.Add(panel21, 0, wx.EXPAND)
            vbox21.Add(panel22, 1, wx.EXPAND)
            vbox21.Add(panel23, 0, wx.EXPAND)
    
            panel2.SetSizer(vbox21)
    
    
    
    
            #panel3 -         
            panel3 = wx.Panel(splitter41, -1)
            #panel3 = wx.Panel(splitter3, -1)
            panel31 = wx.Panel(panel3, -1, size=(-1, 25), style=wx.NO_BORDER)
            st3 = wx.StaticText(panel31, -1, 'Related tools', (5, 5))
            #st3 = wx.StaticText(panel31, -1, 'Related tools for acquisition', (5, 5))
            st3.SetForegroundColour('WHITE')
    
            panel31.SetBackgroundColour('BLACK')
            panel32 = wx.Panel(panel3, -1, style=wx.BORDER_SUNKEN)
            
            vbox30 = wx.BoxSizer(wx.VERTICAL)
            list3 = RelatedToolsForAcquisitionList(panel32, -1)
            list3.SetName('RelatedToolsForAcquisitionOnList')
            vbox30.Add(list3, 1, wx.EXPAND)
            panel32.SetSizer(vbox30)
    
            vbox31 = wx.BoxSizer(wx.VERTICAL)
            vbox31.Add(panel31, 0, wx.EXPAND)
            vbox31.Add(panel32, 1, wx.EXPAND)
    
            panel3.SetSizer(vbox31)
    
    
            
            
            #panel4
            #panel4 = wx.Panel(splitter42, -1)
            panel4 = wx.Panel(splitter3, -1)
            panel41 = wx.Panel(panel4, -1, size=(-1, 25), style=wx.NO_BORDER)
            st4 = wx.StaticText(panel41, -1, 'Check List', (5, 5))
            st4.SetForegroundColour('WHITE')
    
            panel41.SetBackgroundColour('BLACK')
            panel42 = wx.Panel(panel4, -1, style=wx.BORDER_SUNKEN)
            
            vbox40 = wx.BoxSizer(wx.VERTICAL)
            list4 = AnalysisDescriptionList(panel42, -1)
            list4.SetName('AnalysisDescriptionOnList')
            vbox40.Add(list4, 1, wx.EXPAND)
            panel42.SetSizer(vbox40)
    
            vbox41 = wx.BoxSizer(wx.VERTICAL)
            vbox41.Add(panel41, 0, wx.EXPAND)
            vbox41.Add(panel42, 1, wx.EXPAND)
    
            panel4.SetSizer(vbox41)
    
    
    
            
            #panel6    
            panel6 = wx.Panel(splitterLower, -1)
            #panel6 = wx.Panel(splitter, -1)
            
            panel61 = wx.Panel(panel6, -1, size=(-1, 25), style=wx.NO_BORDER)
            st6 = wx.StaticText(panel61, -1, 'Module List', (5, 5))
            st6.SetForegroundColour('WHITE')
            panel61.SetBackgroundColour('BLACK')
            
            panel62 = wx.Panel(panel6, -1, style=wx.BORDER_SUNKEN)
            list6 = ModuleListList(panel62, -1)
            list6.SetName('ModuleListOnList')
            vbox60 = wx.BoxSizer(wx.VERTICAL)
            vbox60.Add(list6, 1, wx.EXPAND)
            panel62.SetSizer(vbox60)
            
            panel63 = wx.Panel(panel6, -1, size=(25, -1), style=wx.NO_BORDER)
            self.CheckAll = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll.png'))
            self.ReleaseAll = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll.png'))
            self.Insert = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Insert.png'))
            self.Modyfy = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Modify.png'))
            self.Delete = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Delete.png'))
            self.Recover = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/recover.png'))
            self.ShareExport = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Export.png'))
            self.ShareImport = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Import.png'))
            self.ModuleDownload = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/download.png'))
            self.ModulePathAdjustment  = wx.BitmapButton(panel63, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ModulePathModify.png'))
            list61 = Statusbar(panel63, -1)
            list61.SetName('ModuleStatusbar')
            list61.SetLine("Module Status")
            self.CheckShowReference  = wx.CheckBox(panel63, -1, 'Show reference')
            vbox61 = wx.BoxSizer(wx.HORIZONTAL)
            vbox61.Add(self.CheckAll, 0, wx.EXPAND)
            vbox61.Add(self.ReleaseAll, 0, wx.EXPAND)
            vbox61.Add(self.Insert, 0, wx.EXPAND)
            vbox61.Add(self.Modyfy, 0, wx.EXPAND)
            vbox61.Add(self.Delete, 0, wx.EXPAND)
            vbox61.Add(self.Recover, 0, wx.EXPAND)
            vbox61.Add(self.ModulePathAdjustment, 0, wx.EXPAND)
            vbox61.Add(list61, 1, wx.EXPAND)
            vbox61.Add(self.CheckShowReference, 0, wx.EXPAND)
            self.CheckAll.Bind(wx.EVT_BUTTON, self.OnCheckAll)
            self.ReleaseAll.Bind(wx.EVT_BUTTON, self.OnReleaseAll)
            self.Insert.Bind(wx.EVT_BUTTON, self.OnInsert)
            self.Modyfy.Bind(wx.EVT_BUTTON, self.OnModyfy)
            self.Delete.Bind(wx.EVT_BUTTON, self.OnDelete)
            self.Recover.Bind(wx.EVT_BUTTON, self.OnRecover)
            self.ShareExport.Bind(wx.EVT_BUTTON, self.OnShareExport)
            self.ShareImport.Bind(wx.EVT_BUTTON, self.OnShareImport)
            self.ModulePathAdjustment.Bind(wx.EVT_BUTTON, self.OnModulePathAdjustment)
            self.CheckShowReference.Bind(wx.EVT_CHECKBOX, self.OnCheckShowReference)
            self.CheckAll.SetToolTip(wx.ToolTip("Check All"))
            self.ReleaseAll.SetToolTip(wx.ToolTip("Release All"))
            self.Insert.SetToolTip(wx.ToolTip("Insert New Module"))
            self.Modyfy.SetToolTip(wx.ToolTip("Modify the Focused Module"))
            self.Delete.SetToolTip(wx.ToolTip("Delete the Selected Module"))
            self.Recover.SetToolTip(wx.ToolTip("Deleted Module Recovery(in recycle)"))
            self.ShareExport.SetToolTip(wx.ToolTip("Make PFP-Archive into %PFPROOT%"))
            self.ShareImport.SetToolTip(wx.ToolTip("Import Module from PFP-Archive"))
            self.ModuleDownload.SetToolTip(wx.ToolTip("Selected module download automatically"))
            self.ModulePathAdjustment.SetToolTip(wx.ToolTip("Module path adjustment in this platform"))
    
            self.CheckShowReference.SetValue(True)
            self.ReferenceViewMode = True
            
            self.Recover.Disable()
    
            panel63.SetSizer(vbox61)
    
            vbox61 = wx.BoxSizer(wx.VERTICAL)
            vbox61.Add(panel61, 0, wx.EXPAND)
            vbox61.Add(panel62, 1, wx.EXPAND)
            vbox61.Add(panel63, 0, wx.EXPAND)
            
            panel6.SetSizer(vbox61)
    
    
        
            
            #panel7
            panel7 = wx.Panel(splitterLower, -1)
            #panel6 = wx.Panel(splitter, -1)
            
            panel71 = wx.Panel(panel7, -1, size=(-1, 25), style=wx.NO_BORDER)
            st7 = wx.StaticText(panel71, -1, 'Quick Utilization', (5, 5))
            st7.SetForegroundColour('WHITE')
            panel71.SetBackgroundColour('BLACK')
                
            
            panel72 = wx.Panel(panel7, -1, style=wx.BORDER_SUNKEN)
            self.nb = wx.Notebook(panel72)
            
            vbox70 = wx.BoxSizer(wx.VERTICAL)
            vbox70.Add(self.nb, 1, wx.EXPAND)
            panel72.SetSizer(vbox70)
    
            
            il = wx.ImageList(16, 16)
            idx1 = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Search_16_16.png'))
            idx2 = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/process_16_16.png'))
            idx3 = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/registry_16_16.png'))
            idx4 = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/filesystem_meta_16_16.png'))
            idx5 = il.Add(bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/filesystem_meta_16_16.png'))
            self.nb.AssignImageList(il)
            
            page1 = SearchPage(self.nb)
            self.nb.AddPage(page1, "Search")
            self.nb.SetPageImage(0, idx1)
            
            self.processpage = ProcessPage(self.nb)
            self.nb.AddPage(self.processpage, "Classification, Favorite")
            self.nb.SetPageImage(1, idx2)
            
            self.FileSystem_Page = FileSystemMetaPage(self.nb)
            self.nb.AddPage(self.FileSystem_Page, "File Lookup")
            self.nb.SetPageImage(2, idx4)
            
            self.Registry_Page = RegistryPage(self.nb)
            self.nb.AddPage(self.Registry_Page, "Lookup(Registry)")
            self.nb.SetPageImage(3, idx3)
            
            vbox71 = wx.BoxSizer(wx.VERTICAL)
            vbox71.Add(panel71, 0, wx.EXPAND)
            vbox71.Add(panel72, 1, wx.EXPAND)
            panel7.SetSizer(vbox71)
    
    
            
            
            #toolbar
            toolbar = self.CreateToolBar()
            toolbar.AddLabelTool(2, 'All Module', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/AllModule.png'))
            toolbar.AddLabelTool(3, 'File Select', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/File.png'))
            toolbar.AddLabelTool(4, 'Recycle', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Recycle.png'))
            toolbar.AddSeparator ()
            toolbar.AddLabelTool(5, 'New Terminal', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Terminal.png'))
            if self.isPFPOnManaging == True:
                toolbar.AddLabelTool(9, 'PowerShell ISE', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/PowerShell_21_21__.png'))
            toolbar.AddLabelTool(6, 'PFP Extractor', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/extract_file_21_21.png'))
            if self.isPFPOnManaging == True:
                toolbar.AddLabelTool(7, 'PFP Format Analyzer', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/format_analysis_21_21.png'))
                toolbar.AddLabelTool(8, 'Python Editor', wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/NotepadppPortable_21_21.png'))
            toolbar.AddSeparator ()
            category_label = wx.StaticText(toolbar, -1, "Shortcut : ", wx.Point(0, 0))
            
            toolbar.SetToolShortHelp(2, 'Show all module(Ctrl + A)')
            toolbar.SetToolShortHelp(3, 'View modules for selected file(Ctrl + F)')
            toolbar.SetToolShortHelp(4, 'Deleted Module')
            toolbar.SetToolShortHelp(5, 'Launch Terminal(Ctrl + T)')
            toolbar.SetToolShortHelp(6, 'Launch PFP Extractor(Ctrl + E)')
            if self.isPFPOnManaging == True:
                toolbar.SetToolShortHelp(7, 'PFP Format Analyzer')
                toolbar.SetToolShortHelp(8, 'Python Editor')
                toolbar.SetToolShortHelp(9, 'PowerShell ISE')
            
            
            
            
            #get shortcut data from user db
            con = sqlite3.connect( self.default_user_modulelistDB_path )
            cursor = con.cursor()
            
            SelectQuery = "select CategoryName, Description from ModuleCategory order by CategoryName COLLATE NOCASE;"
            
            cursor.execute( SelectQuery )
            UserResultList = cursor.fetchall()
            
            idx = 0
            for row in UserResultList:
                lst = list(row)
                lst[0] = "[UserDefine] " + lst[0]
                UserResultList[idx] = tuple(lst) 
                idx += 1
            
            con.close()
            
            #get shortcut data from public db
            con = sqlite3.connect( self.default_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            PublicResultList = cursor.fetchall()
            
            idx = 0
            for row in PublicResultList:
                lst = list(row)
                lst[0] = "[Public] " + lst[0]
                PublicResultList[idx] = tuple(lst) 
                idx += 1
            
            con.close()
            
            #Merge and sort
            ###############
            MergedResultList = UserResultList + PublicResultList
            MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
            
            self.Typelist = []
            
            idx = 0
            for row in MergedResultList:
                
                self.Typelist.append(row[0])
    
            self.category_combo = wx.ComboBox(toolbar, choices=self.Typelist)
            self.category_combo.Bind(wx.EVT_COMBOBOX, self.OnComboSelect)
            toolbar.AddControl (category_label)
            toolbar.AddControl (self.category_combo)
            
            toolbar.Realize()
    
            #binding
            self.Bind(wx.EVT_TOOL, page1.OnSearchButton, id=1)
            self.Bind(wx.EVT_TOOL, self.OnAllModule, id=2)
            self.Bind(wx.EVT_TOOL, self.OnFileSelect, id=3)
            self.Bind(wx.EVT_TOOL, self.OnReCycle, id=4)
            self.Bind(wx.EVT_TOOL, self.OnNewTerminal, id=5)
            self.Bind(wx.EVT_TOOL, self.OnLaunchPFPExtractor, id=6)
            self.Bind(wx.EVT_TOOL, self.OnLaunchPFPFormatAnalyzer, id=7)
            self.Bind(wx.EVT_TOOL, self.OnLaunchPythonEditor, id=8)
            self.Bind(wx.EVT_TOOL, self.OnLaunchPowerShellISE, id=9)
            
    
    
    
            
            
            #Create Menu bar
            
            #Menu / Case Menu
            ###################
            menu = wx.Menu()        
            
            #Case management
            self.isCaseSet = False
            self.newCaseMenu = menu.Append(-1, "New Case")                      #Make new case db and Set Case values
            self.openCaseMenu = menu.Append(-1, "Open Case")                    #Set Case values by already excisted case db
            menu.AppendSeparator()
            self.closeCaseMenu = menu.Append(-1, "Close Case")                  #Case related value initialization (title, Value, Menu, etc.._
            menu.AppendSeparator()
            self.openfolderCaseMenu = menu.Append(-1, "Open Case Folder")       #Open folder(by explorer)
            self.processresultCaseMenu = menu.Append(-1, "Case Process Result") #Parsing result (Not yet..)
            menu.AppendSeparator()
            
            self.processresultCaseMenu.Enable(True) 
            self.closeCaseMenu.Enable(True)
            if self.isPFPOnManaging == False:
                self.newCaseMenu.Enable(False)
                self.openCaseMenu.Enable(False)
                self.newCaseMenu.SetItemLabel("New Case(Now developing..)")
                self.openCaseMenu.SetItemLabel("Open Case(Now developing..)")
            self.openfolderCaseMenu.Enable(False)                           #Not yet..
            self.closeCaseMenu.Enable(False)
            self.openfolderCaseMenu.Enable(False)
            self.processresultCaseMenu.Enable(False) 
            
            
            self.Bind(wx.EVT_MENU, self.OnnewCase, self.newCaseMenu)
            self.Bind(wx.EVT_MENU, self.OnopenCase, self.openCaseMenu)
            self.Bind(wx.EVT_MENU, self.OncloseCase, self.closeCaseMenu)
            self.Bind(wx.EVT_MENU, self.OnopenfolderCase, self.openfolderCaseMenu)
            self.Bind(wx.EVT_MENU, self.OnprocessresultCase, self.processresultCaseMenu)
            
            #Module view
            AllModule  = menu.Append(-1, "&All Module\tCtrl-A")             # with accelerator
            FileSelect  = menu.Append(-1, "&File Select\tCtrl-F")           # with accelerator
            LaunchTerminal  = menu.Append(-1, "&Launch Terminal\tCtrl-T")           # with accelerator
            LaunchPFPExtractor  = menu.Append(-1, "&Launch PFP Extractor\tCtrl-E")           # with accelerator
            HideWindow  = menu.Append(-1, "&Hide Window\tCtrl-H")           # with accelerator
            #SelfTestMenu = menu.Append(-1, "&Self Test\tCtrl-S")                # with mnemonic
            #NotApplicable  = menu.Append(-1, "&Not Applicable\tCtrl-N")     # with accelerator
            menu.AppendSeparator()
            exit = menu.Append(-1, "&Quit\tCtrl-Q")
            
            self.Bind(wx.EVT_MENU, self.OnAllModule, AllModule)
            self.Bind(wx.EVT_MENU, self.OnFileSelect, FileSelect)
            self.Bind(wx.EVT_MENU, self.OnNewTerminal, LaunchTerminal)
            self.Bind(wx.EVT_MENU, self.OnLaunchPFPExtractor, LaunchPFPExtractor)
            self.Bind(wx.EVT_MENU, self.OnHideWindow, HideWindow)
            #self.Bind(wx.EVT_MENU, self.OnSelfTest, SelfTestMenu)
            #self.Bind(wx.EVT_MENU, self.OnNotApplicable, NotApplicable)
            self.Bind(wx.EVT_MENU, self.ExitApp, exit)
            
            
            #Edit Menu
            menuEdit = wx.Menu()        
            
            Copy  = menuEdit.Append(-1, "&Copy Text\tCtrl-C")             # with accelerator
            menuEdit.AppendSeparator()
            Config  = menuEdit.Append(-1, "&Configuration")             # with accelerator
            CategorySetting  = menuEdit.Append(-1, "&Shortcut Setting")             # with accelerator
            
            self.Bind(wx.EVT_MENU, self.OnCopy, Copy)
            self.Bind(wx.EVT_MENU, self.OnConfig, Config)
            self.Bind(wx.EVT_MENU, self.OnCategorySetting, CategorySetting)
            
            
            #Panel Menu
            menuPanel = wx.Menu()        
            PFPListPanelMenu  = menuPanel.Append(-1, "&Focus on PFP-List\tCtrl-P")             # with accelerator
            ModuleLauncherMenu  = menuPanel.Append(-1, "&Focus on Module Launcher\tCtrl-M")             # with accelerator
            
            self.Bind(wx.EVT_MENU, self.OnFocusPFPList, PFPListPanelMenu)
            self.Bind(wx.EVT_MENU, self.OnFocusModuleLauncher, ModuleLauncherMenu)
            
            
            #Management Menu
            menuManage = wx.Menu()        
            
            self.PublicPFPManage = menuManage.Append(-1, "Pulbic PFP-List setting")
            menuManage.AppendSeparator()
            self.PublicShortcutManage = menuManage.Append(-1, "Pulbic Shortcut setting")
            menuManage.AppendSeparator()
            self.PublicModuleInsert = menuManage.Append(-1, "Public Module Insert")
            self.PublicModuleModify = menuManage.Append(-1, "Public Module Modify")
            self.PublicModuleDelete = menuManage.Append(-1, "Public Module Delete")
            self.PublicModuleRecover = menuManage.Append(-1, "Public Module Recover")                     
            
            self.Bind(wx.EVT_MENU, self.OnPublicPFPListManage, self.PublicPFPManage)
            self.Bind(wx.EVT_MENU, self.OnPublicShortcutManage, self.PublicShortcutManage)
            self.Bind(wx.EVT_MENU, self.OnPublicModuleInsert, self.PublicModuleInsert)
            self.Bind(wx.EVT_MENU, self.OnPublicModuleModify, self.PublicModuleModify)
            self.Bind(wx.EVT_MENU, self.OnPublicModuleDelete, self.PublicModuleDelete)
            self.Bind(wx.EVT_MENU, self.OnPublicModuleRecover, self.PublicModuleRecover)
        
        
            #Set Menu bar
            menuBar = wx.MenuBar()
            menuBar.Append(menu, "&Menu")
            menuBar.Append(menuEdit, "&Edit")
            menuBar.Append(menuPanel, "&Panel")
            if self.isPFPOnManaging == True:
                menuBar.Append(menuManage, "&Manage")
            
            self.SetMenuBar(menuBar)
    
            acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('Q'), exit.GetId())])
            self.SetAcceleratorTable(acceltbl)
    
    
    
    
    
            #Splitter settting
            ######################
            hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM)
            
            self.SetSizer(hbox)
            self.CreateStatusBar()
            self.SetBackgroundColour('WHITE')
            
            #main Splitter
            splitter.SplitHorizontally(splitterUpper, splitterLower)
            splitter.SetSashGravity(0.5)
            
            #Lower Splitter - Module List and Terminal
            
            splitterLower.SplitVertically(panel6, panel7, 500)
            splitterLower.SetSashGravity(0)
            
            #Upper Splitter - Analysis Point List
            splitterUpper.SplitVertically(panel0, splitter2, 250)
            splitter2.SplitVertically(panel1, splitter3, 250)
    
            #Show 3 section(not split related tools)
            splitter3.SplitVertically(splitter41, panel4)
            splitter3.SetSashGravity(1)
            splitter41.SplitHorizontally(panel2, panel3)
            splitter41.SetSashGravity(1)
            
            self.Centre()
            self.Show(True)
            
            #self.CheckAll.SetFocus()
            list0.SetFocus()
            if list0.GetFocusedItem() == -1:
                list0.Select(0) 
            
            #Tab order setting
            order = (self.VestigeLocationCheckAll, self.VestigeLocationReleaseAll, self.VestigeLocationFileExtract)
            for i in xrange(len(order) - 1):
                    order[i+1].MoveAfterInTabOrder(order[i])
            
            
            
            
            self.processpage.SetFocus()
            self.nb.SetSelection(1)
            
            #---#############################################################################################################################
            #---UI Setting End                                                                                                              #
            #---#############################################################################################################################        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            #---Start the updater
            #---#####################
            if self.isPFPOnManaging == False:
                Updatedia = PFPUpdater_v2(self, 'PFP Updater')
                Updatedia.ShowModal()
                if Updatedia.isUpdated == True:
                    wx.MessageBox("Platform is terminated")
                    self.Close()
                    #sys.exit()
                    #self.onClose()
                Updatedia.Destroy()
            
            
            
            
            
            
            
            
            
            
            #---Update information and License agreement window popup
            #---########################################################
            Non_Agreement_PopupFlag = True
            
            #Agreement check
            md5Result = hashlib.md5(open("./PFPModule/PFPLib/License_and_Update_information.pyc","rb").read()).hexdigest()
            
            copy_fp = open("./PFPModule/UpdateTemp/copy", "r")
            filelines = copy_fp.readlines()
            copy_fp.close()
            
            for line in filelines:
                if str(get_mac())+"_"+str(md5Result) in line:
                    Non_Agreement_PopupFlag = False
                    
                    
    
            if Non_Agreement_PopupFlag == True:
                dia = License_and_Update_information(self, 'License agreement')
                dia.ShowModal()
                dia.Destroy()
            
            #re-Agreement check    
            md5Result = hashlib.md5(open("./PFPModule/PFPLib/License_and_Update_information.pyc","rb").read()).hexdigest()
            
            copy_fp = open("./PFPModule/UpdateTemp/copy", "r")
            filelines = copy_fp.readlines()
            copy_fp.close()
            
            for line in filelines:
                if str(get_mac())+"_"+str(md5Result) in line:
                    Non_Agreement_PopupFlag = False
            
            
            if Non_Agreement_PopupFlag == True:
                self.Close()
            
            
        
            
            
            
            #---Create or alter DB
            #---##############################
            
            
            #---initialize threading
            #---###############################################################
            threads = []
            th = threading.Thread(target=self.ThreadInitialSetting, args=())
            th.start()
            threads.append(th)
        
        
        #초기 UI 세팅 시  DB 문제가 발생혈 경우 아래 코드에서 처리
        except:
            
            #Make User Process DB
            con = sqlite3.connect( self.default_user_processDB_path )
            cursor = con.cursor()
            
            try:
                CreateQuery = "CREATE TABLE [ProcessContentsTable] ([ProcessCategory] TEXT, [Location] TEXT, [Text] TEXT, [ContentsPath] TEXT, [Description] TEXT, [ContentsID] TEXT,[ParentID] CHAR, [isDeleted] TEXT, [Author] TEXT, [Contact] TEXT, [Sequence] TEXT, [UserContentsLocation] TEXT, [reserved2] TEXT, [reserved3] TEXT, [reserved4] TEXT, [reserved5] TEXT, [reserved6] TEXT, [reserved7] TEXT, [reserved8] TEXT, [reserved9] TEXT, [reserved10] TEXT);"
                cursor.execute( CreateQuery )
                con.commit()
            except:
                print " "
                
            try:
                CreateQuery = "CREATE TABLE [ContentsIDTable] ([IDType] TEXT, [LastContentsID] TEXT, [NextContentsID] TEXT);"
                cursor.execute( CreateQuery )
                con.commit()
                
                InsertQuery = "Insert into ContentsIDTable values('Local', '0', '1');"
                cursor.execute( InsertQuery )
                con.commit()
            except:
                print " "
                
                
            #Module DB Update
            con = sqlite3.connect( self.default_user_modulelistDB_path )
            cursor = con.cursor()
            
            try:
                CreateQuery = "Create Table ModuleCategory (RowID INTEGER PRIMARY KEY AUTOINCREMENT, CategoryName TEXT, Description TEXT, ModuleIDs TEXT)"
                cursor.execute( CreateQuery )
                con.commit()
            except:
                print " "
            try:
                CreateQuery = "Create Table ExceptionHashList (RowID INTEGER PRIMARY KEY AUTOINCREMENT, FileName TEXT, MD5 TEXT)"
                cursor.execute( CreateQuery )
                con.commit()
                
                
            except:
                print " "
                
                
            #Alter Table.. if not 
            try:
                AlterQuery = "Alter Table ModuleCategory add column ContentsID TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ModuleCategory add column CreateTime TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ModuleCategory add column ModifyTime TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ModuleCategory add column isPublic TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ArgumentList add column ContentsID TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ArgumentList add column CreateTime TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ArgumentList add column ModifyTime TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
            try:
                AlterQuery = "Alter Table ArgumentList add column isPublic TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
                
            con.close()
            
            
            #PFP-List DB Update
            
            con = sqlite3.connect( self.default_pfplist_path_asdfasdf )
            cursor = con.cursor()
            
            
            try:
                AlterQuery = "Alter Table AnPointTable add column RelatedWebPage TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
                
            try:
                AlterQuery = "Alter Table CategoryTable add column RelatedWebPage TEXT;"
                cursor.execute( AlterQuery )
                con.commit()
            except:
                print " "
                
            try:
                AlterQuery = "Alter Table AnPointTable add column UserContentsLocation TEXT;"
                cursor.execute( AlterQuery )
                
                UpdateQuery = "Update AnPointTable set UserContentsLocation = 'top0';"
                cursor.execute( UpdateQuery )
                con.commit()
            except:
                print " "
                
            try:
                AlterQuery = "Alter Table CategoryTable add column UserContentsLocation TEXT;"
                cursor.execute( AlterQuery )
                
                UpdateQuery = "Update CategoryTable set UserContentsLocation = 'top0';"
                cursor.execute( UpdateQuery )
                con.commit()
            except:
                print " "
                
            try:
                AlterQuery = "Alter Table VesLocationTable add column UserContentsLocation TEXT;"
                cursor.execute( AlterQuery )
                
                UpdateQuery = "Update VesLocationTable set UserContentsLocation = 'top0';"
                cursor.execute( UpdateQuery )
                con.commit()
            except:
                print " "
                
            try:
                SelectQuery = "Select LastContentsID, NextContentsID from ContentsIDTable"
                cursor.execute( SelectQuery )
                
                ResultRow = cursor.fetchone()
                
                LastContentsID = ResultRow[0]
                
                NextContentsID = ResultRow[1]
                
                if int(LastContentsID) >= 500000:
                    LastContentsID = str(int(LastContentsID) - 500000)
                    
                if int(NextContentsID) >= 500000:
                    NextContentsID = str(int(NextContentsID) - 500000)
                    
                #print LastContentsID, NextContentsID
                
                UpdateQuery = "Update ContentsIDTable set LastContentsID = '" + LastContentsID + "', NextContentsID = '" + NextContentsID + "';"
                cursor.execute( UpdateQuery )
                con.commit()
            except:
                print " "
                
            con.close()
    
    
            
            #PFP-List DB Update
            con = sqlite3.connect( "./PFPModule/PFPLib/PublicPFPList/public.process.sqlite" )
            cursor = con.cursor()
            
            try:
                SelectQuery = "Select ContentsPath, ContentsID from ProcessContentsTable"
                cursor.execute( SelectQuery )
                
                ResultRows = cursor.fetchall()
                
                for ResultRow in ResultRows:
                
                    ContentsPath = ResultRow[0]
                    ContentsID = ResultRow[1]
                    
                    if "public.3.Windows_System_Analysis.pfplist.sqlite" in ContentsPath:
                        ContentsPath = ContentsPath.replace("public.3.Windows_System_Analysis.pfplist.sqlite", "public.2.Artifact_Analysis.pfplist.sqlite")
                        
                    
                    UpdateQuery = "Update ProcessContentsTable set ContentsPath = '" + ContentsPath + "' where ContentsID = '" + ContentsID + "';"
                    cursor.execute( UpdateQuery )
                    con.commit()
            except:
                print " "
                
            con.close()
    
            
            wx.MessageBox("Database is altered. please relaunch the platform")
            
            
    
    
    
    
    #----------------------------------------------------------------------
    
    def Set_Initial_LookupTab_InCase(self):
        
        
        #self.CaseTargetPath, self.CaseName, self.CaseDBPath
        
        #filesystem meta lookup result
        #self.FileSystem_Page
        #Tree init
        self.FileSystem_Page.tree.DeleteAllItems()
        self.FileSystem_Page.tree.root = self.FileSystem_Page.tree.AddRoot(self.CaseTargetPath + " [" + self.CaseName + "]")

        if not(self.FileSystem_Page.tree.GetAGWWindowStyleFlag() & CT.TR_HIDE_ROOT):
            self.FileSystem_Page.tree.SetItemImage(self.FileSystem_Page.tree.root, self.FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
            self.FileSystem_Page.tree.SetItemImage(self.FileSystem_Page.tree.root, self.FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
            
            
        tsk_db_con = sqlite3.connect( self.CaseDBPath )
        tsk_db_cursor = tsk_db_con.cursor()
        
        #dir_type이 3이면 폴더, 5면 파일.
        SelectQuery = "select meta_addr, dir_type, mtime, atime, ctime, crtime, size, name from tsk_files where parent_path == '/';"
        
        tsk_db_cursor.execute( SelectQuery )
        SelectedRows = tsk_db_cursor.fetchall()
        #print "SelectedRows = " + str(SelectedRows)
        #print 
        #print len(SelectedRows)
        
        
        #print SelectedRows
        if len(SelectedRows) > 0:
            for Row in SelectedRows:
                if Row[1] == 3 and Row[7] != "." and Row[7] != ".." and Row[7].strip() != "":
                    child = self.FileSystem_Page.tree.AppendItem(self.FileSystem_Page.tree.root, Row[7])
        
                    self.FileSystem_Page.tree.SetItemImage(child, self.FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
                    self.FileSystem_Page.tree.SetItemImage(child, self.FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
                    
                    #하위에 데이터가 있을 경우 더미를 삽입..
                    SelectQuery = "select count(obj_id) from tsk_files where parent_path == '/"+Row[7]+"/';"
                    #print SelectQuery
        
                    tsk_db_cursor.execute( SelectQuery )
                    Row = tsk_db_cursor.fetchone()
                    if Row[0] > 0:
                        SubChild = self.FileSystem_Page.tree.AppendItem(child, "Dummy")
                     
        else : 
            child = self.FileSystem_Page.tree.AppendItem(self.FileSystem_Page.tree.root, "There is no child")
    
            self.FileSystem_Page.tree.SetItemImage(child, self.FileSystem_Page.tree.folder_close_idx, wx.TreeItemIcon_Normal)
            self.FileSystem_Page.tree.SetItemImage(child, self.FileSystem_Page.tree.folder_open_idx, wx.TreeItemIcon_Expanded)
        
        
        self.FileSystem_Page.tree.Expand(self.FileSystem_Page.tree.root)
        self.FileSystem_Page.tree.SelectItem(child)
        

        #List init
        self.FileSystem_Page.list.DeleteAllItems()
        tsk_db_con.close()
        
        return
    
    
    
    def OnCastTargetComboSelect(self, event):
        """케이스 내에 분석 대상 선택하면, 타겟 루트, DBPath 설정 변경해주기..! """
        SelectedText = self.case_target_combo.GetValue()
        #print SelectedText
        
        for TargetDB in self.TargetDBList:
            if TargetDB[1] in SelectedText.split("(")[0]:
                self.CaseDBPath = self.CasePath + "\\" + TargetDB[0]
                self.CaseTargetPath = TargetDB[1]
                self.DateTime = TargetDB[2]
                break
        #print self.CaseDBPath        
    
    
        
        """pfp-list를 케이스용으로 연결해야함"""
        if "|" in self.CaseTargetPath : self.PublicPFPListPath = self.CasePath + "\\CaseData\\" + self.CaseTargetPath.split("|")[0].strip() + "\\"
        else :                          self.PublicPFPListPath = self.CasePath + "\\CaseData\\" + self.CaseTargetPath.replace(":", "") + "\\"
        self.public_pfplist_path = self.PublicPFPListPath + "public.2.Artifact_Analysis.pfplist.sqlite"
        #print self.public_pfplist_path
        self.default_pfplist_path = self.PublicPFPListPath + "UserDefine.pfplist.sqlite"
        #print self.default_pfplist_path
        
        self.SetTitle(self.CaseName + "(" + self.DateTime + ", " + self.CaseTargetPath + ") - " + self.CasePath)
        
        if "|" in self.CaseTargetPath :     self.AnalysisTargetRoot = self.CaseTargetPath.split("|")[1].strip()
        else :                              self.AnalysisTargetRoot = self.CaseTargetPath 
        window = self.FindWindowByName('VestigeLocationStatusbar')
        window.SetLine('Target Root = ' + self.CaseTargetPath)
        
        
        """새로운  pfp-list를 화면에 세팅"""
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        
        window0.DeleteAllItems()
        window1.DeleteAllItems()
        window2.DeleteAllItems()
        window3.DeleteAllItems()
        window4.DeleteAllItems()
        
        window0.listidx = 0
        
        window0.LoadData(self.public_pfplist_path.decode('cp949'), self.default_pfplist_path.decode('cp949'))
        window0.PublicPFPListFilePath = self.public_pfplist_path
        
        self.pfplist_category_combo.SetValue("2.Artifact_Analysis")
        
        return 
    
    def OnnewCase(self, event):     #Make new case db and Set Case values
        
        #텟스트 파일 넘기며, Extractor 구동
        """신 Case 생성 코드"""
        if self.isPFPOnManaging == True:
            Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\CaseCreateDlg.pyc", "True"])
        else:
            Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\CaseCreateDlg.pyc", "False"])
        
        """구 Case 생성 코드"""
        """
        #케이스 생성  
        Casedia = CaseCreateDlg(self, 'New Case')
        Casedia.ShowModal()
        
        if Casedia.Cancel == True:  return
        else:
            self.SetCaseStatus(Casedia.CasePath, Casedia.CaseName)  #Case 상태 세팅
        
            return
        Casedia.Destroy()
        """
    
    def OnopenCase(self, event):    #Set Case values by already excisted case db
        
        """Case 열람 코드"""
        dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
        TargetFolder = ""
        if dlg.ShowModal() == wx.ID_OK:
            TargetFolder = dlg.GetPath().encode('cp949') 
            self.SetCaseStatus(TargetFolder, TargetFolder.split("\\")[len(TargetFolder.split("\\"))-1]) #Case 상태 세팅
        
        return
    
    
    def SetCaseStatus(self, CasePath, CaseName):
        
        """Case DB Load"""
        self.CasePath = CasePath
        self.CaseName = CaseName
        self.CaseTargetPath = "None" 
        self.DateTime = "None"
        self.TargetDBList = []
        for root, dirs, files in os.walk(self.CasePath):
            for file in files:
                if os.path.split(file)[0] not in (self.CasePath + "\\"):
                    break
                
                DBName = os.path.split(file)[1]
                if "(img)" in DBName:
                    if not os.path.isfile("PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe"):
                        wx.MessageBox("Cannot open the case. that include result from image file \n please Check path -> '.\\PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe'")
                        return
                    
                    ImageAlreadyInserted = False
                    for list in self.TargetDBList:
                        if DBName.split("~")[0].replace("(img)", "") in list[1]:
                            ImageAlreadyInserted = True
                    if ImageAlreadyInserted == True: continue
                    
                    #이미지 마운팅!! 
                    ##############################################
                    fp = open(CasePath + "\\CaseData\\" + DBName.split("_")[0].replace("(img)", "").split("~")[0] + "\\ImagePath.txt", 'r')
                    SelectedFile = fp.readline()
                    fp.close
                    path = os.path.abspath(".") 
                    
                    #if self.isPFPOnManaging == True:   #is managing on == true 일 경우
                    pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe")
                    cmdARGS = [pathchange.decode('cp949'), "mount", SelectedFile, "/B:F", "/A:T", "/T:1"]
                    #else:   AA = 1    #OSF 마운트는 고려할 게 참 많다..
                        
                    self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                    self.pipe.stdin.close()
                    self.NowTerminalProcessPid = self.pipe.pid 
            
                    ResultLines = []
                    ResultString = ""            
                    while self.pipe.poll() == None:
                        result = self.pipe.stdout.readline()
                        if result.strip() != "":
                            ResultLines.append(result.strip())
                            ResultString += (result.strip() + "\n")
                            
                    result = self.pipe.stdout.readline()
                    if result.strip() != "":
                        ResultLines.append(result.strip())
                        ResultString += (result.strip() + "\n")
                        
                    wx.MessageBox(ResultString)
                    
                    if "Drive Letter:" in ResultString:
                        part_count = 1
                        for line in ResultLines:
                            if "Drive Letter:" in line:
                                DrvLetter = line.strip().split(":")[1].strip()
                                if len(DrvLetter) <= 2:
                                    CaseTargetPath = DBName.split("_")[0].replace("(img)", "").split("~")[0] + "\\" + str(part_count)
                                    CaseTargetPath = CaseTargetPath + "|" + line.strip().split(":")[1].strip() + ":"
                                    NewDBName = DBName
                                    for file in files:
                                        if DBName.split("~")[0] in file and "~"+str(part_count)+"~" in file:
                                            NewDBName = os.path.split(file)[1]
                                    DateTime = strftime("%Y/%m/%d %H:%M:%S", time.localtime(float(NewDBName.split("_")[4].replace(".casedb", ""))))
                                    self.TargetDBList.append([NewDBName, CaseTargetPath, DateTime])
                                    part_count += 1   
                    #if "Created device" in ResultString:
                    
                    #이미지 마운팅!! 
                    ##############################################
                    
                    
                else:
                    try:
                        CaseTargetPath = DBName.split("_")[3] + ":"
                        DateTime = strftime("%Y/%m/%d %H:%M:%S", time.localtime(float(DBName.split("_")[7].replace(".casedb", ""))))
                        self.TargetDBList.append([DBName, CaseTargetPath, DateTime])
                    except: continue
        self.CaseDBPath = CasePath + "\\" + self.TargetDBList[0][0]
        self.CaseTargetPath = self.TargetDBList[0][1]
        self.DateTime = self.TargetDBList[0][2]
        
    
    
        """Case 상태 세팅"""
        #self.VestigeLocationSetTargetRoot.Enable(False)
        self.VestigeLocationSetTargetRoot.SetToolTip(wx.ToolTip("Open Case Folder"))
        self.newCaseMenu.Enable(False)
        self.openCaseMenu.Enable(False)
        self.closeCaseMenu.Enable(True)
        self.openfolderCaseMenu.Enable(True)
        self.processresultCaseMenu.Enable(False)    #Not ye
        self.case_target_combo.Clear()
        for TargetDB in self.TargetDBList:
            self.case_target_combo.Append(TargetDB[1] + " (" + TargetDB[2] + ")")
        self.case_target_combo.Enable(True)
        self.isCaseSet = True
        if self.isPFPOnManaging == True:
            self.PublicPFPManage.Enable(False)
        self.AnListFileOpen.Enable(False)
        self.AnListModify.Enable(False)
        
        """pfp-list를 케이스용으로 연결해야함"""
        #self.live_public_pfplist_path = self.public_pfplist_path
        #self.live_user_pfplist_path = self.default_pfplist_path
        self.PublicPFPListPath = ""
        if "|" in self.CaseTargetPath : self.PublicPFPListPath = CasePath + "\\CaseData\\" + self.CaseTargetPath.split("|")[0].strip() + "\\"
        else :  self.PublicPFPListPath = CasePath + "\\CaseData\\" + self.CaseTargetPath.replace(":", "") + "\\"
        self.public_pfplist_path = self.PublicPFPListPath + "public.2.Artifact_Analysis.pfplist.sqlite"
        #print self.public_pfplist_path
        self.default_pfplist_path = self.PublicPFPListPath + "UserDefine.pfplist.sqlite"
        #print self.default_pfplist_path
        
        self.SetTitle(self.CaseName + "(" + self.DateTime + ", " + self.CaseTargetPath + ") - " + self.CasePath)
        
        self.AnalysisTargetRoot = ""
        if "|" in self.CaseTargetPath : self.AnalysisTargetRoot = self.CaseTargetPath.split("|")[1].strip()
        else : self.AnalysisTargetRoot = self.CaseTargetPath 
        window = self.FindWindowByName('VestigeLocationStatusbar')
        window.SetLine('Target Root = ' + self.CaseTargetPath)
        
        
        #"""파일 시스템 룩업 페이지에서 트리를 세팅..!(루트만 세팅하고, 하위에 폴더가 있으면 Dumy를 넣어주기)"""
        #self.Set_Initial_LookupTab_InCase()
        
        
        
        """새로운  pfp-list를 화면에 세팅"""
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        
        window0.DeleteAllItems()
        window1.DeleteAllItems()
        window2.DeleteAllItems()
        window3.DeleteAllItems()
        window4.DeleteAllItems()
        
        window0.listidx = 0
        
        window0.LoadData(self.public_pfplist_path.decode('cp949'), self.default_pfplist_path.decode('cp949'))
        window0.PublicPFPListFilePath = self.public_pfplist_path
        
        self.pfplist_category_combo.SetValue("2.Artifact_Analysis")
    
        return
    
    
    def OncloseCase(self, event):   #Case related value initialization (title, Value, Menu, etc..)
        
        dlg = wx.MessageDialog(None, 'Are you sure to close this case?', 'Warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:
        
            #self.VestigeLocationSetTargetRoot.Enable(True)
            self.VestigeLocationSetTargetRoot.SetToolTip(wx.ToolTip("Change target root"))
            self.newCaseMenu.Enable(True)
            self.openCaseMenu.Enable(True)
            self.closeCaseMenu.Enable(False)
            self.openfolderCaseMenu.Enable(False)
            self.processresultCaseMenu.Enable(False)    #Not yet
            #self.case_target_combo_list = ["aaa", "bbb"]
            self.case_target_combo.Enable(False)
            self.isCaseSet = False
            if self.isPFPOnManaging == True:
                self.PublicPFPManage.Enable(True)
            self.AnListFileOpen.Enable(True)
            self.AnListModify.Enable(True)
            self.PublicPFPListPath = "./PFPModule/PFPLib/PublicPFPList/"
            self.public_pfplist_path = self.live_public_pfplist_path
            self.user_pfplist_path = self.live_user_pfplist_path
            #print self.public_pfplist_path
            #print self.user_pfplist_path
            
            self.SetTitle("PFP - Portable Forensic Platform (by TheSOFT with DFRC)")
            
            self.AnalysisTargetRoot = "C:"
            window = self.FindWindowByName('VestigeLocationStatusbar')
            window.SetLine('Target Root = ' + self.AnalysisTargetRoot)
            
            """원래 pfp-list를 화면에 세팅"""
            window0 = self.FindWindowByName('AnalysisCategoryOnList')
            window1 = self.FindWindowByName('AnalysisPointOnList')
            window2 = self.FindWindowByName('VestigeLocationOnList')
            window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
            window4 = self.FindWindowByName('AnalysisDescriptionOnList')
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            window4.DeleteAllItems()
            
            window0.listidx = 0
            
            window0.LoadData(self.public_pfplist_path.decode('cp949'), self.default_pfplist_path.decode('cp949'))
            window0.PublicPFPListFilePath = self.public_pfplist_path
            
            self.pfplist_category_combo.SetValue("2.Artifact_Analysis")
        
        
            
            if os.path.isfile("PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe"):
                dialog = wx.MessageDialog(self, message = "Do you want dismount all images mounted by MIP?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
                response = dialog.ShowModal()
                
                if (response == wx.ID_YES):
                
                    path = os.path.abspath(".")
                    pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe")
                    cmdARGS = [pathchange.decode('cp949'), "unmount", "/all"]
                    #print cmdARGS
                    self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                    self.pipe.stdin.close()
         
                    self.NowTerminalProcessPid = self.pipe.pid 
            
                    ResultString = ""
                    while self.pipe.poll() == None:
                        result = self.pipe.stdout.readline()
                        if result.strip() != "":    ResultString += (result.strip() + "\n") #ResultLines.append(result.strip())
                    result = self.pipe.stdout.readline()
                    if result.strip() != "":    ResultString += (result.strip() + "\n")     #ResultLines.append(result.strip())
                        
                    wx.MessageBox(ResultString)
        
        
        
        
        return
    
    
    def OnopenfolderCase(self, event):  #Open folder(by explorer)
        
        wx.MessageBox("OnopenfolderCase")
        
        return
    
    
    def OnprocessresultCase(self, event):   #Parsing result (Not yet..)
        
        wx.MessageBox("OnprocessresultCase")
        
        return
    
    
    
    
    
    def onClose(self, evt):
        
        #Destroy the taskbar icon and the frame
        dialog = wx.MessageDialog(self, message = "Are you sure you want to quit?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
        response = dialog.ShowModal()
    
        if (response == wx.ID_YES):
            self.tbIcon.RemoveIcon()
            self.tbIcon.Destroy()
            #self.tbIcon.Close()
            #self.Close()
            self.Destroy()
        
        
    def onMinimize(self, event):
        
        #When minimizing, hide the frame so it "minimizes to tray"
        #self.Hide()
        return
        
    
        
        
                
        
 
    def OnAllModule(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        window.AllModule()
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("All Module")

    
    def OnFileSelect(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        window.FileSelect()
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("Target File : " + window.FilePath)
        
    
    def OnSelfTest(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        window.UnitModule()
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("Unit Modules")
    

    
    def OnNotApplicable(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        os.system("explorer .\\UserModule\\NotApplicable")
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("Not Applicable Module loading")
        
    
    def OnReCycle(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        window.Recycle()
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("Recycle")
        
        
    
    def OnNewTerminal(self, event):
        os.chdir(".\\UserModule\CommonCli")
        os.system("start")
        os.chdir("..\\..\\")
        
    def OnLaunchPFPExtractor(self, event):
        
        threads = []
        th = threading.Thread(target=self.ThreadLaunchExtractor, args=())
        th.start()
        threads.append(th)
        
    def OnHideWindow(self, event):
        
        self.Hide()
        
        return 
   
   
    def OnLaunchPFPFormatAnalyzer(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        
        if window.ExecuteStatus == "File":
            Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\InternalModules\FileFormatAnalyzer.pyc", window.FilePath])
        else:
            Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\InternalModules\FileFormatAnalyzer.pyc"])
        
        
        return
        
        
    def OnLaunchPythonEditor(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        if window.ExecuteStatus == "File":
            Process = Popen(["./PFPModule/PFPLib/InternalModules/npp.6.3.3.bin/notepad++.exe", window.FilePath])
        else:
            Process = Popen(["./PFPModule/PFPLib/InternalModules/npp.6.3.3.bin/notepad++.exe", "./PFPModule/PFPLib/InternalModules/UnitWork.py"])
        
        
        return
        
        
    def OnLaunchPowerShellISE(self, event):
        
        os.system("start " + "%windir%/system32/WindowsPowerShell/v1.0/PowerShell_ISE.exe")
        
        return
        
    def ThreadLaunchExtractor(self):
        
        #os.system("\"" + self.interpreter_path + "\" .\PFPModule\PFPLib\PFPListManageDlg.pyc new Select_File_Path " + self.user + " " + self.contact)
        
        #Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", "None", ""])
        if self.isCaseSet == True:  Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", "None", self.CaseDBPath])
        else:                       Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", "None", "None"])
        while Process.poll() is None: 
            time.sleep(0.5)
        
    
    def OnComboSelect(self, event):
        
        SelectedText = self.category_combo.GetValue()
        
        window = self.FindWindowByName('ModuleListOnList')
        window.CategorySelected()
        
        StatusWindow = self.FindWindowByName('ModuleStatusbar')
        StatusWindow.SetLine("Category : " + SelectedText )

    
    def ExitApp(self, event):
        self.Close()
        
    
    def OnCopy(self, event):

        if self.isPremium == True:
            window = self.FindFocus()
            if window.GetName() == "VestigeLocationOnList":
                #itemidx = window.GetFocusedItem()
                
                StringData = ""
                item = window.GetFirstSelected()
                while item != -1: 
                    StringData += window.GetItemText(item).strip()
                    StringData += "\n"
                    item = window.GetNextSelected(item)
                
                SelfTest = PFPUtil()
                
                SelfTest.Copy_to_Clipboard(StringData)
                
        else:
            wx.MessageBox("Please use premium PFP.")
        
    
    def OnConfig(self, event):
        
        dia = PFPConfig(self, 'Configuration')
        dia.ShowModal()
        dia.Destroy()
        
        #os.system("\"" + self.interpreter_path + "\" .\PFPModule\PFPLib\PFPConfig.pyc")

        return
    
    
    def RunShortcutSetting(self, mode = False):
    
        dia = CategorySetting(self, 'Category Setting', mode)
        dia.ShowModal()
        dia.Destroy()

        SelectQuery = "select CategoryName, Description from ModuleCategory order by CategoryName COLLATE NOCASE;"
        
        #Get From User DB
        con = sqlite3.connect( self.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[0] = "[UserDefine] " + lst[0]
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Get From Public DB
        con = sqlite3.connect( self.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        idx = 0
        for row in PublicResultList:
            lst = list(row)
            lst[0] = "[Public] " + lst[0]
            PublicResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Merge and sort
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        
        self.category_combo.Clear()
          
        
        for row in MergedResultList:
            self.category_combo.Append(row[0])
            
        return

    
    def OnCategorySetting(self, event):
        
        self.RunShortcutSetting()

        return
        
        
    def OnFocusPFPList(self, event):
        window = self.FindWindowByName('AnalysisCategoryOnList')
        window.SetFocus()
        if window.GetFocusedItem() == -1:
            window.Select(0) 
        
        
    def OnFocusModuleLauncher(self, event):
        window = self.FindWindowByName('ModuleListOnList')
        window.SetFocus()
        if window.GetFocusedItem() == -1:
            window.Select(0) 
        
        
    def OnFocusTerminalEmul(self, event):
        window = self.FindWindowByName('TerminalCommander')
        window.SetFocus()


    def OnPublicPFPListManage(self, event):
        
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        
        
        
        threads = []
        th = threading.Thread(target=self.ThreadAnListModify, args=(window0, window1, window2, window3, window4, window5, "modi", self.AnListModify, "public setting"))
        th.start()
        threads.append(th)
        
        
    def OnPublicShortcutManage(self, event):
        
        self.RunShortcutSetting(True)

        return
        
        
    def OnPublicModuleInsert(self, event):
        
        self.RunModuleDlg(True)
        
        return
        
        
    def OnPublicModuleModify(self, event):
        
        self.RunModuleDlg(isManaged = True, mode = 'modi')
        
        return
    
    
    def OnPublicModuleDelete(self, event):
        
        self.RunDelete(True)
        
        return
    
    
    def OnPublicModuleRecover(self, event):
        
        self.RunRecover(True)
        
        return
        
        
    def OnAnListFileOpen(self, event):
        UtilClass = Util()
        
        
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile="", style=wx.OPEN)
        NewPFPListFile = ""
        
        
        
        if dlg.ShowModal() == wx.ID_OK:
            NewPFPListFile = dlg.GetPath()
        
            window0 = self.FindWindowByName('AnalysisCategoryOnList')
            window0.PFPListFilePath = NewPFPListFile
            self.default_pfplist_path = NewPFPListFile

            window1 = self.FindWindowByName('AnalysisPointOnList')
            window2 = self.FindWindowByName('VestigeLocationOnList')
            window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
            window4 = self.FindWindowByName('AnalysisDescriptionOnList')
            window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
            
            
            window0.listidx = 0
            
            
            
            
            con = sqlite3.connect( self.public_pfplist_path )
            cursor = con.cursor()
            
            try:
                AlterQuery = "Alter Table AnPointTable add column RelatedWebPage TEXT;"
                cursor.execute( AlterQuery )
            except:
                print " "
                
            con.close()
            
            
            
            con = sqlite3.connect( self.default_pfplist_path )
            cursor = con.cursor()
            
            try:
                AlterQuery = "Alter Table AnPointTable add column RelatedWebPage TEXT;"
                cursor.execute( AlterQuery )
            except:
                print " "
                
            con.close()
            
            
            
            
            
            window0.LoadData(self.public_pfplist_path, self.default_pfplist_path)
            
            
        return



    def OnAnListModify(self, event):
        
        
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        
        
        temp_listdb_con = sqlite3.connect( self.default_pfplist_path )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select * from CategoryTable where isPublic = 'y'"
        temp_listdb_cursor.execute( SelectQuery )
        CategoryResultList = temp_listdb_cursor.fetchall()
        
        temp_listdb_con.close()
        
        if len(CategoryResultList) != 0:
            wx.MessageBox("Can not modify the public pfplist.")
            
            return

        
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        
        
        
        threads = []
        th = threading.Thread(target=self.ThreadAnListModify, args=(window0, window1, window2, window3, window4, window5, "modi", self.AnListModify))
        th.start()
        threads.append(th)
        
        return
    
    
    
    def OnAnListFileNew(self, event):
        
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        window5 = self.FindWindowByName('RelatedToolsForAnalysisOnList')
        
        threads = []
        th = threading.Thread(target=self.ThreadAnListModify, args=(window0, window1, window2, window3, window4, window5, "new", self.AnListModify))
        th.start()
        threads.append(th)
        
        
        return

    
    
    def OnPFPListComboSelect(self, event):
        
        SelectedText = self.pfplist_category_combo.GetValue()
        
        self.public_pfplist_path = self.PublicPFPListPath + "public." + SelectedText + ".pfplist.sqlite"

        #print "PUBLIC PFP LIST = " + self.public_pfplist_path
        #print "USER PFP LIST = " + self.default_pfplist_path
        
        if "UserDefine(TechGroup)" in SelectedText:
            self.public_pfplist_path = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
        
        window0 = self.FindWindowByName('AnalysisCategoryOnList')
        window1 = self.FindWindowByName('AnalysisPointOnList')
        window2 = self.FindWindowByName('VestigeLocationOnList')
        window3 = self.FindWindowByName('RelatedToolsForAcquisitionOnList')
        window4 = self.FindWindowByName('AnalysisDescriptionOnList')
        
        window0.DeleteAllItems()
        window1.DeleteAllItems()
        window2.DeleteAllItems()
        window3.DeleteAllItems()
        window4.DeleteAllItems()
        
        window0.listidx = 0
        
        window0.LoadData(self.public_pfplist_path.decode('cp949'), self.default_pfplist_path.decode('cp949'))
        window0.PublicPFPListFilePath = self.public_pfplist_path
        
        return
    
    
    
    def OnVestigeLocationCheckAll(self, event):
        
        window = self.FindWindowByName('VestigeLocationOnList')
        for index in range(window.GetItemCount()):
            if not window.IsChecked(index): 
                window.ToggleItem(index)
        
        return
    
    
        
    def OnVestigeLocationReleaseAll(self, event):
        
        window = self.FindWindowByName('VestigeLocationOnList')
        for index in range(window.GetItemCount()):
            if window.IsChecked(index): 
                window.ToggleItem(index)
        
        return
    
    
    
    def OnVestigeLocationSetTargetRoot(self, event):
        if self.isCaseSet == True:
            os.system("explorer \"" + self.CasePath.replace("/","\\") + "\"") 
        else:
            dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
            TargetFolder = ""
            if dlg.ShowModal() == wx.ID_OK:
                TargetFolder = dlg.GetPath().encode('cp949')
                
                if TargetFolder[len(TargetFolder)-1] == "\\":
                    self.AnalysisTargetRoot = TargetFolder[0:len(TargetFolder)-1]
                else:
                    self.AnalysisTargetRoot = TargetFolder[0:len(TargetFolder)]
                
                window = self.FindWindowByName('VestigeLocationStatusbar')
                window.SetLine('Target Root = ' + self.AnalysisTargetRoot)
    
    
    
    def OnVestigeLocationFileExtract(self, event):
        
        threads = []
        th = threading.Thread(target=self.ThreadFileExtract, args=())
        th.start()
        threads.append(th)
    

    
    def OnCheckAll(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        for index in range(window.GetItemCount()):
            if not window.IsChecked(index): 
                window.ToggleItem(index)
        
        return
    
    
        
    def OnReleaseAll(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        for index in range(window.GetItemCount()):
            if window.IsChecked(index): 
                window.ToggleItem(index)
        
        return
    
    
    
    def RunModuleDlg(self, isManaged = False, mode = 'insert'):
        
        #self.Enable(False) 
        
        #os.system("\"" + self.interpreter_path + "\" .\PFPModule\PFPLib\DBManageDlg.pyc insert " + self.default_modulelistDB_path + " " + self.user + " " + self.contact)
        window = self.FindWindowByName('ModuleListOnList')
        
        FocusedItem = window.GetFocusedItem()
        FocusedItemIDText = ""
        
        if mode =='modi':
            
            colour = window.GetItemBackgroundColour(FocusedItem) 
            
            if isManaged == False and colour != '#e6f1f5':
                wx.MessageBox("Sorry. You can not modify the public module")
                
                return
            
            if isManaged == True and colour == '#e6f1f5':
                wx.MessageBox("Please select the public module")
                
                return
            
            if FocusedItem == -1:
                wx.MessageBox("Select the Module in ModuleList")
                
                return
            else:
                FocusedItemIDText = window.GetItem(FocusedItem,3).GetText()
        
        if mode == "insertUseReference":
            FocusedItemIDText = window.GetItem(FocusedItem,3).GetText()
            #print "ID = " + FocusedItemIDText

        DBPath = ""
        if isManaged == True:
            DBPath = self.default_modulelistDB_path
        else:
            DBPath = self.default_user_modulelistDB_path
            
        #print DBPath
        
        dia = DBManageDlg(self, 'Module Insert', mode, DBPath, self.user, self.contact, FocusedItemIDText)
        dia.ShowModal()
        dia.Destroy()

        window.AllModule()
        
        window.Focus(FocusedItem)
        window.Select(FocusedItem,True)
        
        #self.Enable(True) 
        
        return
    
    
    
    def OnInsert(self, event):
        
        self.RunModuleDlg()
        
        return
    
    
    
    def OnInsertUseReference(self, event):
        
        self.RunModuleDlg(isManaged = False, mode = 'insertUseReference')
        
        return
    
    
    
    def OnHomePageOpen(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        FocusedItem = window.GetFocusedItem() 
        
        DBPath = ""
        colour = window.GetItemBackgroundColour(FocusedItem) 
            
        if colour == '#e6f1f5':
            DBPath = self.default_user_modulelistDB_path
        
        if colour != '#e6f1f5':
            DBPath = self.default_modulelistDB_path
        
        temp_con = sqlite3.connect( DBPath )
        temp_cursor = temp_con.cursor()
        
        SelectQuery = "select HomePage from ModuleList where ModuleName = '" + window.GetItemText(FocusedItem) + "'"
        temp_cursor.execute( SelectQuery )
        ResultList = temp_cursor.fetchone()
        
        UtilClass = Util()
        
        plain = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[0])
        
        if "http://" in plain or "ftp://" in plain or "ftps://" in plain or "https://" in plain:
            os.system("start " + plain)
        else :
            wx.MessageBox("Homepage url is not registered or wrong")
        
        temp_con.close()
    
    
        
    def OnFolderOpen(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        FocusedItem = window.GetFocusedItem() 
        
        DBPath = ""
        colour = window.GetItemBackgroundColour(FocusedItem) 
            
        if colour == '#e6f1f5':
            DBPath = self.default_user_modulelistDB_path
        
        if colour != '#e6f1f5':
            DBPath = self.default_modulelistDB_path
        
        temp_con = sqlite3.connect( DBPath )
        temp_cursor = temp_con.cursor()
        
        SelectQuery = "select ModulePath from ModuleList where ContentsID = '" + window.GetItem(FocusedItem,3).GetText().strip() + "'"
        temp_cursor.execute( SelectQuery )
        ResultList = temp_cursor.fetchone()
        temp_con.close()
        
        UtilClass = Util()
        
        #plain = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[0])
        
        if os.path.isdir(ResultList[0]) == True or os.path.isfile(ResultList[0]):
        
            s = os.path.split(ResultList[0])
    
            os.system("explorer \"" + s[0].replace("/","\\") + "\"") 
            
        else:
            wx.MessageBox("Path is not exsistance")
    
    
    
    def OnModyfy(self, event):
        
        self.RunModuleDlg(isManaged = False, mode = 'modi')
        
        return
    
    
    
    def RunDelete(self, isManaged = False):
        
        dlg = wx.MessageDialog(None, 'Are you sure to delete the selected module?', 'Warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:
            
            window = self.FindWindowByName('ModuleListOnList')
            statuswindow = self.FindWindowByName('ModuleStatusbar')
            
            for index in range(window.GetItemCount()):
                if window.IsChecked(index): 
                    
                    colour = window.GetItemBackgroundColour(index) 
                    
                    if isManaged == False and colour != '#e6f1f5':
                        
                        continue
                    
                    if isManaged == True and colour == '#e6f1f5':
                        
                        continue
                    
                    DBPath = ""
                    if isManaged == True:
                        DBPath = self.default_modulelistDB_path
                    else:
                        DBPath = self.default_user_modulelistDB_path
                    
                    con = sqlite3.connect( DBPath )
                    cursor = con.cursor()
                    
                    UpdateQuery = "update ModuleList set isDeleted = '1' where ContentsID = '" + window.GetItem(index,3).GetText().strip() + "'"
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    con.close()
                    
            statuswindow.SetLine("Delete Modules")
            window.AllModule()
            
        return
    
    
    
    def RunRecover(self, isManaged = False):
    
        window = self.FindWindowByName('ModuleListOnList')
        statuswindow = self.FindWindowByName('ModuleStatusbar')
        for index in range(window.GetItemCount()):
            if window.IsChecked(index): 
                
                colour = window.GetItemBackgroundColour(index) 
                    
                if isManaged == False and colour != '#e6f1f5':
                    
                    continue
                
                if isManaged == True and colour == '#e6f1f5':
                    
                    continue
                
                DBPath = ""
                if isManaged == True:
                    DBPath = self.default_modulelistDB_path
                else:
                    DBPath = self.default_user_modulelistDB_path
                
                con = sqlite3.connect( DBPath )
                cursor = con.cursor()
                
                UpdateQuery = "update ModuleList set isDeleted = '0' where ContentsID = '" + window.GetItem(index,3).GetText().strip() + "'"
                cursor.execute( UpdateQuery )
                con.commit()
                
                con.close()
                
        statuswindow.SetLine("Selected Module is recovered")
        window.AllModule()
        
        return 
    
    
    
    def OnDelete(self, event):
        
        self.RunDelete()
        
        return 
    
    
        
    def OnRecover(self, event):
        
        self.RunRecover()
        
        return
    
    
    
    def OnShareExport(self, event):
        
        dlg = wx.MessageDialog(None, 'Are you sure to export the selected module?', 'Warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:
            threads = []
            th = threading.Thread(target=self.ThreadShareExport, args=())
            th.start()
            threads.append(th)
    
    
    
    def OnShareImport(self, event):
        
        if self.ImportFlag == "NotImporting":
            SelfTest = PFPUtil()
            
            dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd(), defaultFile="", style=wx.OPEN)
            self.ImportSelectedFile = ""
            if dlg.ShowModal() == wx.ID_OK:
            
                self.ImportSelectedFile = dlg.GetPath()
            
                SelfTest.TarExport(self.ImportSelectedFile, 'Sharing.sqlite')
                    
                con = sqlite3.connect( 'Sharing.sqlite' )
                cursor = con.cursor()
            
                SelectQuery = "select ModuleName, Description, ModulePath from ModuleList order by ModuleName COLLATE NOCASE;"
                
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall()
                
                window = self.FindWindowByName('ModuleListOnList')
                window.ModuleImport(ResultList) 
                
                StatusWindow = self.FindWindowByName('ModuleStatusbar')
                StatusWindow.SetLine("Sharing List")
                
                con.close() 
                
                try:
                    os.remove( 'Sharing.sqlite' )
                except:
                    os.system( "del Sharing.sqlite" )
                
                self.Insert.Disable()
                self.Modyfy.Disable()
                self.Delete.Disable()
                self.ShareExport.Disable()
                self.ModuleDownload.Disable() 
                
                self.ImportFlag = "NowImporting"
                
        elif self.ImportFlag == "NowImporting":
            
            dlg = wx.MessageDialog(None, 'Are you sure to import the selected module?', 'Warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
            result = dlg.ShowModal() 
            
            if result == wx.ID_OK:
                threads = []
                th = threading.Thread(target=self.ThreadShareImport, args=())
                th.start()
                threads.append(th)
            
        return
    
    
    
    def OnModulePathAdjustment(self, event):
        
        threads = []
        th = threading.Thread(target=self.ThreadPathAdjustment, args=())
        th.start()
        threads.append(th)
        
        return
    
    
    
    def OnCheckShowReference(self, event):
        
        if self.CheckShowReference.IsChecked() == True:
            self.ReferenceViewMode = True
        else:
            self.ReferenceViewMode = False 
        
        window = self.FindWindowByName('ModuleListOnList')
        window.AllModule()
        
        return
    
    
    
    def OnEnterRelatedWebPage(self, event):
    
        if self.PopupMenuLocation == "Category":
            UtilClass = Util()
            window1 = self.FindWindowByName('AnalysisCategoryOnList')
    
            DBPath = ""
            
            if window1.GetItemBackgroundColour(window1.SelectedIndex) == '#e6f1f5':
                DBPath = window1.PFPListFilePath
            else:
                DBPath = window1.PublicPFPListFilePath
    
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            SelectQuery = "select RelatedWebPage from CategoryTable where ContentsID = '" + window1.SelectedID + "'"
            cursor.execute( SelectQuery )
            
            ResultRow = cursor.fetchone()
            
            
            dia = EditOnlyDlg(self, -1, 'Enter Related Web Page', ResultRow[0])
            dia.ShowModal()
            
            if dia.returnVal.strip() != "":
            
                UpdateQuery = "update CategoryTable set RelatedWebPage = '" + dia.returnVal + "' where ContentsID = '" + window1.SelectedID + "'"
                cursor.execute( UpdateQuery )
                con.commit()
                
            
            dia.Destroy()
            con.close()
            
        else:
            UtilClass = Util()
            window1 = self.FindWindowByName('AnalysisPointOnList')
    
            DBPath = ""
            
            if window1.GetItemBackgroundColour(window1.SelectedIndex) == '#e6f1f5':
                DBPath = window1.UserPFPListFilePath
            else:
                DBPath = window1.PublicPFPListFilePath
    
            con = sqlite3.connect( DBPath )
            cursor = con.cursor()
            
            SelectQuery = "select RelatedWebPage from AnPointTable where ContentsID = '" + window1.SelectedID + "'"
            cursor.execute( SelectQuery )
            
            ResultRow = cursor.fetchone()
            
            
            dia = EditOnlyDlg(self, -1, 'Enter Related Web Page', ResultRow[0])
            val = dia.ShowModal()
            
            if dia.returnVal.strip() != "":
            
                UpdateQuery = "update AnPointTable set RelatedWebPage = '" + dia.returnVal + "' where ContentsID = '" + window1.SelectedID + "'"
                cursor.execute( UpdateQuery )
                con.commit()
                
            
            dia.Destroy()
            con.close()
    
        return



        
    def ThreadShareExport(self):  
        
        SelectedModuleList = []
        
        window = self.FindWindowByName('ModuleListOnList')
        statuswindow = self.FindWindowByName('ModuleStatusbar')
        
        for index in range(window.GetItemCount()):
            if window.IsChecked(index): 
                SelectedModuleList.append(window.GetItemText(index))     #"Find selected Data"
                
        SelfTest = PFPUtil()
        
        #modulelist con
        ModuleListcon = sqlite3.connect( self.default_modulelistDB_path )
        Modulelistcursor = ModuleListcon.cursor()

        SelectQuery = "select ModuleName, ModulePath from ModuleList order by ModuleName COLLATE NOCASE;"
        
        Modulelistcursor.execute( SelectQuery )
        ResultList = Modulelistcursor.fetchall()

        #Sharing DB con       
        if os.path.isfile( 'Sharing.sqlite' ) == True:
            try:
                os.remove( 'Sharing.sqlite' )
            except:
                os.system( "del Sharing.sqlite" )
        shutil.copy ( './PFPModule/PFPLib/Dummy.sqlite' , 'Sharing.sqlite')
        
        Sharingcon = sqlite3.connect( 'Sharing.sqlite' )
        Sharingcursor = Sharingcon.cursor()
        
        ResultTarName = 'Sharing_'+strftime("%Y%m%d%H%M%S", gmtime())+'.pfparc'
        
        for SelectedModuleName in SelectedModuleList:
            
            for row in ResultList:
                if SelectedModuleName in row[0]:
                    
                    statuswindow.SetLine(SelectedModuleName + " : " + row[0])
                    
                    if row[1].count('/') >= 4:     #it is in folder
                        
                        s = os.path.split(row[1])
        
                        SelfTest.TarMaker(ResultTarName, s[0])
                        
                        statuswindow.SetLine(SelectedModuleName + " : " + s[0])
                    
                    elif row[1].count('/') == 3:    #it is single file
                        
                        SelfTest.TarMaker(ResultTarName, row[1])
                        
                        statuswindow.SetLine(SelectedModuleName + " : " + row[1])
    
                    
                    #sharing select    
                    SelectQuery = "select * from ModuleList where ModulePath = '" + row[1] + "'"

                    Modulelistcursor.execute( SelectQuery )
                    insertRow = Modulelistcursor.fetchone()

                    #module list insert
                    InsertQuery = "insert into ModuleList values ( null, "
        
                    fieldidx = 0
                    for field in insertRow:
                        if fieldidx != 0:
                            if field == None:
                                InsertQuery += "''"
                            else:
                                InsertQuery += "'" + field + "'"
                            if fieldidx < len(insertRow)-1:
                                InsertQuery += ","
                        fieldidx += 1
                        
                    InsertQuery += ");"
                    
                    Sharingcursor.execute( InsertQuery )        
                    Sharingcon.commit()
        
        ModuleListcon.close()
        Sharingcon.close()
        SelfTest.TarMaker(ResultTarName, 'Sharing.sqlite' )
        try:
            os.remove( 'Sharing.sqlite' )
        except:
            os.system( "del Sharing.sqlite" )
        
        statuswindow.SetLine("Export complete : " + ResultTarName)
        
        return
    
    def ThreadShareImport(self):
        
        #init and find selected module
        SelfTest = PFPUtil()
        
        SelectedModuleList = []
        
        window = self.FindWindowByName('ModuleListOnList')
        statuswindow = self.FindWindowByName('ModuleStatusbar')
        
        for index in range(window.GetItemCount()):
            if window.IsChecked(index): 
                SelectedModuleList.append(window.GetItemText(index))
        
        #Sharing.sqlite -> open, read 
        SelfTest.TarExport(self.ImportSelectedFile, 'Sharing.sqlite')
        
        Sharingcon = sqlite3.connect( 'Sharing.sqlite' )
        Sharingcursor = Sharingcon.cursor()
    
        SelectQuery = "select ModuleName, ModulePath from ModuleList order by ModuleName COLLATE NOCASE;"
        
        Sharingcursor.execute( SelectQuery )
        ResultList = Sharingcursor.fetchall()
        
        #public.modulelist.sqlite -> write
        ModuleListcon = sqlite3.connect( self.default_modulelistDB_path )
        ModuleListcursor = ModuleListcon.cursor()
        
        #import module in selected menu list
        for SelectedModuleName in SelectedModuleList:
            
            for row in ResultList:
                if SelectedModuleName in row[0]:
            
                    SelectQuery = "select * from ModuleList where ModulePath = '" + row[1] + "'"

                    ModuleListcursor.execute( SelectQuery )
                    Results = ModuleListcursor.fetchall()
                    
                    if len(Results) >= 1:
                        statuswindow.SetLine(row[0] + " is already imported")
                        
                    else:
                        
                        statuswindow.SetLine(SelectedModuleName + " : " + row[1])
                                        
                        if row[1].count('/') >= 4:     #it is in folder
                            
                            s = os.path.split(row[1]) 
                            SelfTest.TarExport(self.ImportSelectedFile, s[0].strip("./"))
                        
                        elif row[1].count('/') == 3:    #it is single file
                             
                            SelfTest.TarExport(self.ImportSelectedFile, row[1].strip("./"))
                        
                        #sharing select    
                        SelectQuery = "select * from ModuleList where ModulePath = '" + row[1] + "'"

                        Sharingcursor.execute( SelectQuery )
                        insertRow = Sharingcursor.fetchone()

                        #module list insert
                        InsertQuery = "insert into ModuleList values ( null, "
        
                        fieldidx = 0
                        for field in insertRow:
                            if fieldidx != 0:
                                if field == None:
                                    InsertQuery += "''"
                                else:
                                    InsertQuery += "'" + field + "'"
                                if fieldidx < len(insertRow)-1:
                                    InsertQuery += ","
                            fieldidx += 1
                            
                        InsertQuery += ");"
                        
                        ModuleListcursor.execute( InsertQuery )        
                        ModuleListcon.commit()
    
        ModuleListcon.close()
        Sharingcon.close()
        
        try:
            os.remove( 'Sharing.sqlite' )
        except:
            os.system( "del Sharing.sqlite" )
        
        statuswindow.SetLine("Module import complete")
        
        self.Insert.Enable()
        self.Modyfy.Enable()
        self.Delete.Enable()
        self.ShareExport.Enable()
        self.ModuleDownload.Enable()
        
        self.ImportFlag = "NotImporting"
        
        window.AllModule()
        
        
        
        
        
        
        
        
    def ThreadInitialSetting(self):
        
        
        
        
        
        #dll download..

        DLLPath = "/Utility/Portable Python 2.7.3.2/App/Lib/site-packages/win32/pythoncom27.dll"
        if not os.path.isfile("." + DLLPath):
            urllib.urlretrieve(self.updateserver + DLLPath, "." + DLLPath)
        
        DLLPath = "/Utility/Portable Python 2.7.3.2/App/Lib/site-packages/win32/pythoncomloader27.dll"
        if not os.path.isfile("." + DLLPath):
            urllib.urlretrieve(self.updateserver + DLLPath, "." + DLLPath)
            
        DLLPath = "/Utility/Portable Python 2.7.3.2/App/Lib/site-packages/win32/pywintypes27.dll"
        if not os.path.isfile("." + DLLPath):
            urllib.urlretrieve(self.updateserver + DLLPath, "." + DLLPath)

        import win32api
        import win32file
        import win32con        
        
        
        
        
        
        
        
        
        # Module Path, Install status Check
        ###################################
        
        UtilClass = Util()
        
        statuswindow = self.FindWindowByName('ModuleStatusbar')
        
        
        
        #Set Module exist
        con = sqlite3.connect( self.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "select ModulePath, ModuleName, DownLoadLink, HomePage from ModuleList"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        idx = 0
        
        for Record in ResultList:
            
            LogString = "Thread : Check the module existence status (" + str(idx) + "/" + str(len(ResultList)) + ")"
            statuswindow.SetLine(LogString)  
            idx += 1
            
            DownLoadLink = ""
            
            try:
                DownLoadLink = UtilClass.DummyCyber(self.DecodedDummy, "", Record[2])
            except:
                if Record[2] == None:
                    DownLoadLink = ""
                else: 
                    DownLoadLink = Record[2]
                    
            try:
                HomePage = UtilClass.DummyCyber(self.DecodedDummy, "", Record[3])
            except:
                if Record[3] == None:
                    HomePage = ""
                else: 
                    HomePage = Record[3]
            
            if os.path.isfile(Record[0]) or (os.path.isdir(Record[0]) and '.app' in Record[0]) :
                UpdateQuery = "update ModuleList set UsedStatus = 'y' where ModuleName = '" + Record[1] + "'"
            else : 
                #if 'http://' in DownLoadLink or 'https://' in Record[2]:
                #    UpdateQuery = "update ModuleList set UsedStatus = 'can auto download' where ModuleName = '" + Record[1] + "'"
                if 'Internal' in DownLoadLink or "Internal" == HomePage:
                    UpdateQuery = "update ModuleList set UsedStatus = 'y' where ModuleName = '" + Record[1] + "'"
                elif 'charged' in DownLoadLink:
                    UpdateQuery = "update ModuleList set UsedStatus = 'have to buy' where ModuleName = '" + Record[1] + "'"
                elif 'license agreement' in DownLoadLink:
                    UpdateQuery = "update ModuleList set UsedStatus = 'have to download directly with license agreement' where ModuleName = '" + Record[1] + "'"
                elif 'not compatible' in DownLoadLink:
                    UpdateQuery = "update ModuleList set UsedStatus = 'have to download directly (not compatible with auto download system)' where ModuleName = '" + Record[1] + "'"
                else:
                    UpdateQuery = "update ModuleList set UsedStatus = 'is empty' where ModuleName = '" + Record[1] + "'"
                
            cursor.execute(UpdateQuery)
            con.commit()
            
        #Set Not Portable Module is installed
        SelectQuery = "select DefaultPathAfterInstall, ModuleName, DownLoadLink from ModuleList where isPortable = 'n'"
            
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        idx = 1
        
        for Record in ResultList:
            
            LogString = "Thread : Check the module installation status (" + str(idx) + "/" + str(len(ResultList)) + ")"
            statuswindow.SetLine(LogString)  
            idx += 1
            
            try:
                DefaultPathAfterInstall = UtilClass.DummyCyber(self.DecodedDummy, "", Record[0])
            except:
                DefaultPathAfterInstall = Record[0]
            
            if os.path.isfile(DefaultPathAfterInstall) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")) \
                or os.path.isdir(DefaultPathAfterInstall) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")):
                UpdateQuery = "update ModuleList set isInstalled ='y' where ModuleName = '" + Record[1] + "'"
            else :
                UpdateQuery = "update ModuleList set isInstalled ='n' where ModuleName = '" + Record[1] + "'" 
                
            cursor.execute(UpdateQuery)
            con.commit()
            
        LogString = "-*-"
        statuswindow.SetLine(LogString)
            
        con.close()
        
        
        
        if self.isPFPOnManaging == True:
            LogString = "PFP is launched by manager mode"
            statuswindow.SetLine(LogString) 
            response=urllib2.urlopen("http://portable-forensics.com/count_manage.html",timeout=5)
        elif self.isafirst == True:
            LogString = "PFP is launched by apremium mode"
            statuswindow.SetLine(LogString) 
            response=urllib2.urlopen("http://portable-forensics.com/count_apremium.html",timeout=5)
        elif self.isPremium == True:
            LogString = "PFP is launched by premium mode"
            statuswindow.SetLine(LogString) 
            response=urllib2.urlopen("http://portable-forensics.com/count_premium.html",timeout=5)
        else:
            LogString = "PFP is launched by user mode"
            statuswindow.SetLine(LogString) 
            response=urllib2.urlopen("http://portable-forensics.com/count.html",timeout=5)
    
        #LogString = "-*-"
        #statuswindow.SetLine(LogString)  
        
        
        
    
    def ThreadPathAdjustment(self):
        
        ReferenceDB = self.default_modulelistDB_path
        LocalUserDB = self.default_user_modulelistDB_path
        
        window = self.FindWindowByName('ModuleListOnList')
        statuswindow = self.FindWindowByName('ModuleStatusbar')
        
        statuswindow.SetLine("Thread : module path adjustment") 
        
        Default = os.getcwd().replace("\\","/")+"/UserModule"
        dlg = wx.DirDialog(self, message="Select Target Folder", defaultPath=Default, style=wx.OPEN)
        TargetFolder = ""
        if dlg.ShowModal() == wx.ID_OK:
            TargetFolder = dlg.GetPath().encode('cp949')
            #print type(TargetFolder)
            
            if TargetFolder.find("UserModule") == -1:
                wx.MessageBox("Select Module in %PFPROOT%/UserModule/")
                
                return
            
            
            NewModuleList = []
            
            LogString = ""
            idx = 0
            FullLength = 0
            
                    
            #System cmd register
            #Check Module List hash in Reference
            try:
                UtilClass = Util()
                HomePage = UtilClass.DummyCyber(self.DecodedDummy, "Internal", "")
            except:
                HomePage = "Internal"
            SelectQuery = "Select MD5, ContentsID, HomePage, ModuleName from ModuleList where HomePage = '" + HomePage + "'"
            
            con = sqlite3.connect( ReferenceDB )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            ReferenceResultList = cursor.fetchall()

            con.close()
            
            for row in ReferenceResultList:
                
                SelectQuery = "Select * from ModuleList Where ContentsID = '" + row[1] + "'"
                                    
                con = sqlite3.connect( LocalUserDB )
                cursor = con.cursor()
                
                cursor.execute( SelectQuery )
                LocalDBResultList = cursor.fetchall()
                
                con.close()
                
                #target is not registered yet!!! do register
                if len(LocalDBResultList) == 0:
                    #Get attribute from Reference
                    con = sqlite3.connect( ReferenceDB )
                    cursor = con.cursor()
                    
                    SelectQuery = "select * from ModuleList where ContentsID = " + row[1]
                    
                    cursor.execute( SelectQuery )
                    ReferenceResultRow = cursor.fetchone()
                    
                    #Set Insert query for local DB (set module path and md5, and other is same to reference) 
                    con = sqlite3.connect( LocalUserDB )
                    cursor = con.cursor()

                    InsertQuery = "insert into ModuleList values ( null, "
                    fieldidx = 0
                    for field in ReferenceResultRow:
                        if fieldidx != 0:
                            if field == None:
                                InsertQuery += "''"
                            else:
                                InsertQuery += "'" + str(field) + "'"
                            if fieldidx < len(ReferenceResultRow)-1:
                                InsertQuery += ","
                        fieldidx += 1
                    InsertQuery += ");"
        
                    cursor.execute( InsertQuery )
                    con.commit()
                    
                    
                    UpdateQuery = "Update ModuleList set ModulePath = '" + row[3].lower() + "', MD5 = '' where ContentsID = '" + row[1] + "'"
                    
                    #print UpdateQuery
                
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    
                    
                    con.close()            
            
            
            #Count pe file in folder
            for root, dirs, files in os.walk(TargetFolder):
                rootpath = os.path.join(os.path.abspath(TargetFolder), root)
                Num = rootpath.find("UserModule")
                
                rootpath = rootpath.replace(TargetFolder[0:Num], "./")
                rootpath = rootpath.replace("\\", "/")
                
                for file in files:
                    
                    try:
                        if (".exe" in os.path.splitext(file)[1] or ".msi" in os.path.splitext(file)[1] or ".py" in os.path.splitext(file)[1] or ".bat" in os.path.splitext(file)[1] or ".cmd" in os.path.splitext(file)[1]) and "NotApplicable" not in rootpath:
                            FullLength += 1
                    except:
                        continue
        
            #Path adjustment
            for root, dirs, files in os.walk(TargetFolder):
                rootpath = os.path.join(os.path.abspath(TargetFolder), root)
                Num = rootpath.find("UserModule")
                
                rootpath = rootpath.replace(TargetFolder[0:Num], "./")
                rootpath = rootpath.replace("\\", "/")
                
                for file in files:

                    #try:
                    if (".exe" in os.path.splitext(file)[1] or ".msi" in os.path.splitext(file)[1] or ".py" in os.path.splitext(file)[1] or ".com" in os.path.splitext(file)[1] or ".bat" in os.path.splitext(file)[1]) and "NotApplicable" not in rootpath:
                        
                        
                        LogString = "Thread : module path adjustment (" + str(idx) + "/" + str(FullLength) + ")"
                        statuswindow.SetLine(LogString)  
                        idx += 1
                        
                        filepath = os.path.join(rootpath, file)
                        filepath = filepath.replace("\\", "/")
                        
                        md5Result = ""#hashlib.md5(open(filepath.decode("cp949"),"rb").read()).hexdigest()
                        
                        
                        
                        #Check Exception List in LocalUser
                        SelectQuery = "Select * from ExceptionHashList Where FileName = '" + filepath + "'"
                        
                        con = sqlite3.connect( LocalUserDB )
                        cursor = con.cursor()
                        
                        cursor.execute( SelectQuery )
                        LocalDBResultList = cursor.fetchall()
                        
                        con.close()
                        
                        if len(LocalDBResultList) != 0:
                            continue
                            
                        

                        #파일 검색하여 모듈에 넣기
                        SelectQuery = "Select DownLoadName, ContentsID from ModuleList"
                        
                        con = sqlite3.connect( ReferenceDB )
                        cursor = con.cursor()
                        
                        cursor.execute( SelectQuery )
                        ReferenceResultList = cursor.fetchall()
                        
                        con.close()
                        
                        count = 0
                        TargetContentsID = 0
                        for ReferenceResult in ReferenceResultList:
                            #print type(filepath)
                            if (ReferenceResult[0].strip() != "") and (ReferenceResult[0] in filepath):
                                #print filepath
                                count += 1
                                TargetContentsID = ReferenceResult[1]
                                break
                            
                        
                        if count == 0:   #Module is not in the Reference
                        
                            NewModuleList.append((filepath, md5Result))
                        
                        #Set User Module DB (copied from public db)
                        else:
                            SelectQuery = "Select * from ModuleList Where ContentsID = '" + TargetContentsID + "'"
                            
                            con = sqlite3.connect( LocalUserDB )
                            cursor = con.cursor()
                            
                            cursor.execute( SelectQuery )
                            LocalDBResultList = cursor.fetchall()
                            
                            con.close()
                            
                            #target is not registered yet!!! do register
                            if len(LocalDBResultList) == 0:
                                #print "in if!!!!!"
                                
                                #Get attribute from Reference
                                con = sqlite3.connect( ReferenceDB )
                                cursor = con.cursor()
                                
                                SelectQuery = "select * from ModuleList where ContentsID = '" + TargetContentsID + "'"
                                
                                cursor.execute( SelectQuery )
                                ReferenceResultRow = cursor.fetchone()
                                
                                #Set Insert query for local DB (set module path and md5, and other is same to reference) 
                                con = sqlite3.connect( LocalUserDB )
                                cursor = con.cursor()

                                InsertQuery = "insert into ModuleList values ( null, "
                                fieldidx = 0
                                for field in ReferenceResultRow:
                                    if fieldidx != 0:
                                        if field == None:
                                            InsertQuery += "''"
                                        else:
                                            InsertQuery += "'" + str(field) + "'"
                                        if fieldidx < len(ReferenceResultRow)-1:
                                            InsertQuery += ","
                                    fieldidx += 1
                                InsertQuery += ");"
                    
                                cursor.execute( InsertQuery )
                                con.commit()
                                
                                UpdateQuery = "Update ModuleList set ModulePath = '" + filepath + "', MD5 = '" + md5Result + "' where ContentsID = '" + TargetContentsID + "'"
                    
                                #print UpdateQuery
                    
                                cursor.execute( UpdateQuery )
                                con.commit()
                                
                                con.close()
                            
                            #target is already registered!!! just path adjustment!!
                            elif len(LocalDBResultList) != 0:
                                
                                
                                #Get attribute from Reference
                                con = sqlite3.connect( LocalUserDB )
                                cursor = con.cursor()
                                
                                UpdateQuery = "Update ModuleList set ModulePath = '" + filepath + "' where ContentsID = '" + TargetContentsID + "'"
                    
                                cursor.execute( UpdateQuery )
                                con.commit()
                                
                                con.close()
                            
            
            
            
            statuswindow.SetLine("Complete : module path adjustment")

            #New Module import 
            dlg = wx.MessageDialog(None, "Module path adjustment complete.\n\nAre you want to import new module in target folder?", 'information', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
            result = dlg.ShowModal() 
            
            if result == wx.ID_OK:
                
                dia = NewModuleDlgAfterAdjustment(None, sys.stdout, NewModuleList, self.default_user_modulelistDB_path)
                dia.ShowModal()
                dia.Destroy()
                
        
        
                
        #Set Not Portable Module is installed
        con = sqlite3.connect( self.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "select DefaultPathAfterInstall, ModuleName, DownLoadLink from ModuleList where isPortable = 'n'"
            
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        idx = 0
        
        for Record in ResultList:
            
            LogString = "Thread : Check the module installation status (" + str(idx) + "/" + str(len(ResultList)) + ")"
            statuswindow.SetLine(LogString)  
            idx += 1
            
            try:
                UtilClass = Util()
                DefaultPathAfterInstall = UtilClass.DummyCyber(self.DecodedDummy, "", Record[0])
            except:
                DefaultPathAfterInstall = Record[0]
            
            if os.path.isfile(DefaultPathAfterInstall) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")) \
                or os.path.isdir(DefaultPathAfterInstall) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")):
                UpdateQuery = "update ModuleList set isInstalled ='y' where ModuleName = '" + Record[1] + "'"
            else :
                UpdateQuery = "update ModuleList set isInstalled ='n' where ModuleName = '" + Record[1] + "'" 
                
            cursor.execute(UpdateQuery)
            con.commit()
            
        con.close()
                
        LogString = "-*-"
        statuswindow.SetLine(LogString)
        
        window.AllModule()     
            
            
            
    
    def ThreadAnListModify(self, window0, window1, window2, window3, window4, window5, status, AnListModify, mode = "default"):
        
        #self.AnListFileOpen.Enable(False)
        self.AnListModify.Enable(False)
        #self.AnListFileNew.Enable(False)
        

        
        if status == "new":
            os.system("\"" + self.interpreter_path + "\" .\PFPModule\PFPLib\PFPListManageDlg.pyc new Select_File_Path " + self.user + " " + self.contact)
            
            
        
        else :
            #here!!
            if mode == "public setting":
                Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPListManageDlg.pyc", "modi", self.public_pfplist_path, "public", self.user, self.contact])
                
                while Process.poll() is None: 
                    time.sleep(0.5)
        
            else :
                Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPListManageDlg.pyc", "modi", self.public_pfplist_path, self.default_pfplist_path, self.user, self.contact])
                
                while Process.poll() is None: 
                    time.sleep(0.5)
        
            
            
            window0.DeleteAllItems()
            window1.DeleteAllItems()
            window2.DeleteAllItems()
            window3.DeleteAllItems()
 
            
            window0.listidx = 0
            window0.LoadData(self.public_pfplist_path, self.default_pfplist_path)

            
            self.PFPListDBArrangement(self.public_pfplist_path, self.default_pfplist_path)

        
        self.AnListModify.Enable(True)



    def PFPListDBArrangement(self, PublicDB, UserDB):

        #AnPoint... setting
        PublicCon = sqlite3.connect( PublicDB )
        UserCon = sqlite3.connect( UserDB )
        PublicCursor = PublicCon.cursor()
        UserCursor = UserCon.cursor()
        
        SelectQuery = "select CategoryID, ContentsID, Text from AnPointTable where isDeleted = 'n'"
        
        PublicCursor.execute( SelectQuery )
        UserCursor.execute( SelectQuery )
        ResultList = PublicCursor.fetchall()
        UserResultList = UserCursor.fetchall()
        
        for Record in ResultList:
            
            SelectQuery = "select * from CategoryTable where ContentsID = '" + str(Record[0]) + "' and isDeleted = 'n'" 
            #print SelectQuery
            PublicCursor.execute( SelectQuery )
            SubResultList = PublicCursor.fetchall()
            
            if len(SubResultList) > 0:
                continue
            else:
                UpdateQuery = "update AnPointTable set isDeleted = 'y', Text = '" + (str(Record[2]) + "(.. delete..)") + "' where ContentsID = '" + str(Record[1]) + "'"
                #print UpdateQuery
                PublicCursor.execute( UpdateQuery )
                PublicCon.commit()
        """    
        for Record in UserResultList:
            
            SelectQuery = "select * from CategoryTable where ContentsID = '" + str(Record[0]) + "' and isDeleted = 'n'" 
        
            UserCursor.execute( SelectQuery )
            SubResultList = UserCursor.fetchall()
            
            if len(SubResultList) > 0:
                continue
            else:
                UpdateQuery = "update AnPointTable set isDeleted = 'y', Text = '" + (str(Record[2]) + "(.. delete..)") + "' where ContentsID = '" + str(Record[1]) + "'"
                UserCursor.execute( UpdateQuery )
                UserCon.commit()
        """
                

        
        
        

        #Ves Location...setting
        
        SelectQuery = "select AnPointID, ContentsID, Text from VesLocationTable where isDeleted = 'n'"
        
        PublicCursor.execute( SelectQuery )
        UserCursor.execute( SelectQuery )
        ResultList = PublicCursor.fetchall()
        UserResultList = UserCursor.fetchall()
        
        for Record in ResultList:
            
            SelectQuery = "select * from AnPointTable where ContentsID = '" + str(Record[0]) + "' and isDeleted = 'n'" 
        
            PublicCursor.execute( SelectQuery )
            SubResultList = PublicCursor.fetchall()
            
            if len(SubResultList) > 0:
                continue
            else:
                UpdateQuery = "update VesLocationTable set isDeleted = 'y', Text = '" + (str(Record[2]) + "(.. delete..)") + "' where ContentsID = '" + str(Record[1]) + "'"
                PublicCursor.execute( UpdateQuery )
                PublicCon.commit()
        """        
        for Record in UserResultList:
            
            SelectQuery = "select * from AnPointTable where ContentsID = '" + str(Record[0]) + "' and isDeleted = 'n'" 
        
            UserCursor.execute( SelectQuery )
            SubResultList = UserCursor.fetchall()
            
            if len(SubResultList) > 0:
                continue
            else:
                UpdateQuery = "update VesLocationTable set isDeleted = 'y', Text = '" + (str(Record[2]) + "(.. delete..)") + "' where ContentsID = '" + str(Record[1]) + "'"
                UserCursor.execute( UpdateQuery )
                UserCon.commit()
        """
        PublicCon.close()
        UserCon.close()


def main():
    
    app = wx.App()
    #frame = PFPGui.Show()
    PFPGui(None, -1, 'PFP - Portable Forensic Platform (by TheSOFT with DFRC)')
    app.MainLoop()

if __name__ == '__main__':
    main() 
