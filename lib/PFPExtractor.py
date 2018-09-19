#!/usr/bin/python
# -*- coding: utf-8 -*-

from PFPExtractorAddPathDlg import *
from InternalModules.pfp_sdk.PFPUtil import *
from CategoryAddDlg import *

import sys
reload(sys)
sys.setdefaultencoding('cp949')

class Util(object):
    
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




#class CheckList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
class CheckList(wx.ListCtrl):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES )
        #wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        #CheckListCtrlMixin.__init__(self)
        #ListCtrlAutoWidthMixin.__init__(self)
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/suspend_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/go_button_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Check_icon_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.parent = parent
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        
    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-100)
        self.SetColumnWidth(1, 100)
        event.Skip()
        
        
    def OnRightDown(self, event):
        self.SelectedID = event.GetText()
        self.SelectedIndex = event.GetIndex()
        
        
        #if self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().isPFPOnManaging == True:
        
        PopupMenu = wx.Menu()        
        
        AddPath  = PopupMenu.Append(-1, "insert")
        DeletePath  = PopupMenu.Append(-1, "Delete")
                     
        self.Bind(wx.EVT_MENU, self.OnAddPath, AddPath)
        self.Bind(wx.EVT_MENU, self.OnDeletePath, DeletePath)
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPoint())


    def OnAddPath(self, event):
        dia = PFPExtractorAddPathDlg(self, 'Add Path')
        dia.ShowModal()
        
        if dia.returnVal.strip() != "":
            #wx.MessageBox(dia.returnVal)
            Token = dia.returnVal.split('\n')
            #print Token
            for idx in range(len(Token)-1, -1, -1):
                #print Token[idx]
                if Token[idx].strip() == "":    continue
                self.InsertStringItem(self.SelectedIndex, Token[idx])    
                self.SetStringItem(self.SelectedIndex, 1, "Queued")
                self.SetItemImage(self.SelectedIndex, 0)
            
        
        return
        
    def OnDeletePath(self, event):
        item = self.GetFirstSelected()
        firstitem = item
        count = 0 
        while item != -1: 
            count += 1
            #wx.MessageBox(self.GetItem(item,0).GetText())
            item = self.GetNextSelected(item)
        
        for idx in range(0,count):
            self.DeleteItem(firstitem)
        
        return




class PFPExtractor(wx.Frame):
    

    def __init__(self, parent, title):    
        super(PFPExtractor, self).__init__(parent, title=title, pos=(100,100), size=(700,880))

        self.isManaged = False
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
        
        con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RfUmVzcG9uc2UucGZwbGlzdC5zcWxpdGU="))#"./PFPModule/PFPLib/PublicPFPList/public.1.LiveResponse.pfplist.sqlite" )
        cursor = con.cursor()
        
        SelectQuery = base64.b64decode("c2VsZWN0IFRleHQgZnJvbSBBblBvaW50VGFibGUgd2hlcmUgQ29udGVudHNJRCA9ICcxMDAwMjIn")#"select Text from AnPointTable where ContentsID = '500022'"
        cursor.execute(SelectQuery)
        
        Result = cursor.fetchone()
        
        con.close()
        
        #self.EncodedKey = "JuNZ1KK2BtbJ8IiZZbA34S50QFAH4nMd48TeoCK42cg="
        
        #print self.EncodedKey
        
        self.DecodedDummy = base64.b64decode(Result[0])
        
        self.OldSelectedText = ""
        
        #read config file
        self.default_modulelistDB_path = ""
        self.default_user_modulelistDB_path = ""
        self.user = ""
        self.contact = ""
        self.interpreter_path = ""
        
        self.idx = 0 

        self.SelectedListidx = 0
        
        config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "r")
        
        filelines = config_fp.readlines()
        for line in filelines:
            
            if "default public modulelistDB path" in line:
                self.default_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "default user modulelistDB path" in line:
                self.default_user_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "user(pfp id)" in line:
                self.user =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "contact" in line:
                self.contact =  line.split(">")[1].strip("\"").strip("\n")
                
            elif "interpreter path(win)" in line:
                self.interpreter_path =  line.split(">")[1].strip("\"").strip("\n")
                
            elif "interpreter path(wingui)" in line:
                self.interpreter_path_gui =  line.split(">")[1].strip("\"").strip("\n")
      
        self.panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(9, 9)

        #---Main Text
        text1 = wx.StaticText(self.panel, label="")
        sizer.Add(text1, pos=(0, 0), flag=wx.EXPAND, border=50)

        #---Logo
        icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/extract_file_21_21.png'))
        sizer.Add(icon, pos=(0, 14), flag=wx.EXPAND, border=5)

        line = wx.StaticLine(self.panel)
        sizer.Add(line, pos=(1, 0), span=(1, 15), flag=wx.EXPAND|wx.BOTTOM, border=5)

        #---Category Combo
        text2 = wx.StaticText(self.panel, label="  Result Path")
        sizer.Add(text2, pos=(2, 0), flag=wx.EXPAND, border=5)
        
        
        self.DBPath = ""
        
        if self.isManaged == True:
            self.DBPath = self.default_modulelistDB_path
        else:
            self.DBPath = self.default_user_modulelistDB_path
        
        #insert all Category into Combobox
        self.text21 = wx.TextCtrl(self.panel)
        sizer.Add(self.text21, pos=(2, 1), span=(1, 13), flag=wx.TOP|wx.EXPAND, border=5)
        self.text21.SetEditable(0)
        self.text21.SetValue("C:\\")
        
        #---... Button
        self.button2 = wx.Button(self.panel, label="...", size = wx.Size(40,30))
        sizer.Add(self.button2, pos=(2, 14), flag=wx.EXPAND, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonSelectPath)
        
        #---Description
        text3 = wx.StaticText(self.panel, label="  Target paths for raw copy extraction")
        sizer.Add(text3, pos=(3, 0), span=(1, 10), flag=wx.EXPAND, border=5)
        
        #---ListCtrl
        self.List41 = CheckList(self.panel, -1)
        sizer.Add(self.List41, pos=(4, 0), span=(22, 15), flag=wx.EXPAND, border=5)
        
        self.List41.InsertColumn(0, 'Target Path')
        self.List41.InsertColumn(1, 'Status')
        self.List41.InsertColumn(2, 'iNode')
        
        size = self.List41.GetSize()
        
        self.List41.SetColumnWidth(0, 800)
        self.List41.SetColumnWidth(1, 100-5)
        
        #---Check boxes
        self.chk_Recursive = wx.CheckBox(self.panel, label=" Extract elements in child folder recursively")
        sizer.Add(self.chk_Recursive, pos=(26, 0), span=(1, 15), flag=wx.LEFT|wx.TOP, border=5)
        self.chk_Recursive.Bind(wx.EVT_CHECKBOX, self.OnCheckisRecursive)
        
        self.chk_Original_Path = wx.CheckBox(self.panel, label=" Create folder hierarchy as original path folder")
        sizer.Add(self.chk_Original_Path, pos=(27, 0), span=(1, 15), flag=wx.LEFT|wx.TOP, border=5)
        self.chk_Original_Path.Bind(wx.EVT_CHECKBOX, self.OnCheckisOriginal_Path)
        self.chk_Original_Path.SetValue(1)
              
        #---Last Buttons
        self.buttonAddPath = wx.Button(self.panel, label="Add", size = wx.Size(70,30))
        sizer.Add(self.buttonAddPath, pos=(28, 0), span=(1, 2), flag=wx.ALIGN_RIGHT)
        self.buttonAddPath.Bind(wx.EVT_BUTTON, self.OnButtonAddPath)
        
        self.buttonStart = wx.Button(self.panel, label="Start", size = wx.Size(70,30))
        sizer.Add(self.buttonStart, pos=(28, 2), span=(1, 2), flag=wx.ALIGN_RIGHT)
        self.buttonStart.Bind(wx.EVT_BUTTON, self.OnButtonOK)

        self.buttonFolderOpen = wx.Button(self.panel, label="Open", size = wx.Size(70,30))
        sizer.Add(self.buttonFolderOpen, pos=(28, 4), span=(1, 2), flag=wx.ALIGN_LEFT)
        self.buttonFolderOpen.Bind(wx.EVT_BUTTON, self.OnButtonFolderOpen)
        self.buttonFolderOpen.Enable(False)
        
        sizer.AddGrowableCol(2)
        
        self.panel.SetSizer(sizer)
        
        #set target folder
        if sys.argv[2] == "None":
            dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
            TargetFolder = ""
            if dlg.ShowModal() == wx.ID_OK:
                TargetFolder = dlg.GetPath().encode('cp949') 
                self.text21.SetValue(TargetFolder)
        else: 
            if sys.argv[3] == "True":   self.text21.SetValue(os.path.split(sys.argv[2])[0] + "\\CaseData\\" + os.path.split(sys.argv[2])[1].split("~")[0].split(")")[1] + "\\" + os.path.split(sys.argv[2])[1].split("~")[1] + "\\Extract")
            else:                       self.text21.SetValue(os.path.split(sys.argv[2])[0] + "\\CaseData\\" + os.path.split(sys.argv[2])[1].split("p")[0].replace("_","").replace(".","") + "\\Extract")
        
        #Read Target file
        if sys.argv[1] != "None":
            #print list
            fp = open(sys.argv[1], 'r')
            idx = 0
            while 1:
                line = fp.readline()
                if not line: break 
            
                Keyword = line.strip()
                self.List41.InsertStringItem(idx, Keyword.split('\t')[0].replace("\\\\", "\\"))    
                self.List41.SetStringItem(idx, 1, "Queued")
                self.List41.SetStringItem(idx, 2, Keyword.split('\t')[1])
                self.List41.SetItemImage(idx, 0)
                idx += 1
                
            fp.close()
            
                
        if os.path.split(sys.argv[1])[1] == "extract_list.dat" :
            threads = []
            th = threading.Thread(target=self.ThreadExtract, args=())
            th.start()
            threads.append(th)
            
            #while th.is_alive() == True: 
            #    time.sleep(0.5)
            
            #self.Close()
            
    
    def OnCheckisRecursive(self, event):
        isChecked = self.chk_Recursive.GetValue()
        
        if isChecked == 1:  
            self.chk_Recursive.SetValue(1)
            #self.chk_Original_Path.Enable(False)
            #self.chk_Original_Path.SetValue(1)
        else:               
            self.chk_Recursive.SetValue(0)
            #self.chk_Original_Path.Enable(True)

    def OnCheckisOriginal_Path(self, event):
        isChecked = self.chk_Original_Path.GetValue()
        
        if isChecked == 1:  
            self.chk_Original_Path.SetValue(1)
            #self.chk_Recursive.Enable(True)
        else:               
            self.chk_Original_Path.SetValue(0)
            #self.chk_Recursive.Enable(False)
            #self.chk_Recursive.SetValue(0)
    
    
    def OnButtonSelectPath(self, event):

        dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
        TargetFolder = ""
        if dlg.ShowModal() == wx.ID_OK:
            TargetFolder = dlg.GetPath().encode('cp949') 
            self.text21.SetValue(TargetFolder)

        return
    
    
    def OnButtonAddPath(self,event):
        dia = PFPExtractorAddPathDlg(self, 'Add Path')
        dia.ShowModal()
        
        if dia.returnVal.strip() != "":
            #wx.MessageBox(dia.returnVal)
            Token = dia.returnVal.split('\n')
            #print Token
            lastidx = self.List41.GetItemCount()    
            for idx in range(len(Token)-1, -1, -1):
                #print Token[idx]
                if Token[idx].strip() == "":    continue
                self.List41.InsertStringItem(lastidx, Token[idx])    
                self.List41.SetStringItem(lastidx, 1, "Queued")
                self.List41.SetItemImage(lastidx, 0)

    
    def OnButtonOK(self, event):
        
        threads = []
        th = threading.Thread(target=self.ThreadExtract, args=())
        th.start()
        threads.append(th)
        
        return
    
    def ThreadExtract(self):
        self.buttonStart.Enable(False)
        
        ExtractFolder = self.text21.GetValue()
        if os.path.split(sys.argv[1])[1] == "extract_list.dat" :
            ExtractFolder = ExtractFolder
        else:
            ExtractFolder = os.path.join(ExtractFolder, "Copy_" + str(time.time()))
            os.mkdir(ExtractFolder)
        self.ResultFolder = ExtractFolder
        self.buttonFolderOpen.Enable(True)
        RecursiveFlag = "False"
        HierarchyFlag = "False"
        if self.chk_Recursive.GetValue() == 1: RecursiveFlag = "True"
        if self.chk_Original_Path.GetValue() == 1 : HierarchyFlag = "True"
        #print RecursiveFlag
        #print HierarchyFlag
        
        for index in range(self.List41.GetItemCount()):
            self.List41.SetStringItem(index, 1, "Pending")
        
        for index in range(self.List41.GetItemCount()):

            line = self.List41.GetItem(index, 0).GetText()
            Keyword = line.strip()
            
            self.List41.SetStringItem(index, 1, "Processing")
            self.List41.SetItemColumnImage(index, 0, 1)
            
            if "Users\\Default User" in Keyword.encode('cp949') or "Users\\Default" in Keyword.encode('cp949'):
                self.List41.SetStringItem(index, 0, Keyword)
                self.List41.SetStringItem(index, 1, "Done")
                self.List41.SetItemColumnImage(index, 0, 2)
                continue
            
            #print "casedb : " + sys.argv[2]
            #print "Keyword = " + Keyword
            #print type(Keyword) 
            Process = Popen( [self.interpreter_path_gui, 
                              "./PFPModule/PFPLib/InternalModules/TSK_Extractor.pyc", 
                              Keyword, 
                              ExtractFolder, 
                              sys.argv[2],      #Case Folder 
                              RecursiveFlag,
                              HierarchyFlag], shell=True)
            
            max = 0
            while Process.poll() is None:
                ProcKeyword = Keyword + " ["
                for idx in range(0, max):
                    ProcKeyword += "."
                ProcKeyword += "]"
                
                time.sleep(0.5)
                
                self.List41.SetStringItem(index, 0, ProcKeyword)
                max += 1
                if max == 10:
                    max = 0
    
            self.List41.SetStringItem(index, 0, Keyword)
            self.List41.SetStringItem(index, 1, "Done")
            self.List41.SetItemColumnImage(index, 0, 2)
            
            
        if os.path.split(sys.argv[1])[1] == "extract_list.dat" :
            self.Close()
            

        return
    
    
    def OnButtonFolderOpen(self, event):
        
        os.system("explorer \"" + self.ResultFolder +"\"")
        
        return

def main():
    
    app = wx.App()
    PFPExtractor(None, title="PFP Extractor")
    app.MainLoop()

if __name__ == '__main__':
    main() 

    