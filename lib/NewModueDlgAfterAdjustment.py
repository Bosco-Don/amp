

from InternalModules.pfp_sdk.PFPUtil import *
from ExceptionHashListDlg import *
from GetModuleNameDlg import *

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


class ModuleListList(wx.ListCtrl, CheckListCtrlMixin, TextEditMixin, ListCtrlAutoWidthMixin):
    
    #list Checkbox example - http://zetcode.com/wxpython/advanced/
    ExecuteStatus = ""
    FilePath = ""
    
    def __init__(self, parent, id, NewModuleList):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx. LC_EDIT_LABELS)
        CheckListCtrlMixin.__init__(self)
        TextEditMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
    
    
        con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RfUmVzcG9uc2UucGZwbGlzdC5zcWxpdGU="))#"./PFPModule/PFPLib/PublicPFPList/public.1.LiveResponse.pfplist.sqlite" )
        cursor = con.cursor()
        
        SelectQuery = base64.b64decode("c2VsZWN0IFRleHQgZnJvbSBBblBvaW50VGFibGUgd2hlcmUgQ29udGVudHNJRCA9ICcxMDAwMjIn")#"select Text from AnPointTable where ContentsID = '500022'"
        cursor.execute(SelectQuery)
        
        Result = cursor.fetchone()
        
        con.close()
        
        #self.EncodedKey = "JuNZ1KK2BtbJ8IiZZbA34S50QFAH4nMd48TeoCK42cg="
        
        #print self.EncodedKey
        
        self.DecodedDummy = base64.b64decode(Result[0])
        
    
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
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/EmptyPrivateModule.png']
        
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.ExecuteStatus = "AllModule"
        self.parent = parent

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        self.InsertColumn(0, 'Module Path')
        self.InsertColumn(1, 'ModuleName')
        self.InsertColumn(2, 'ModuleName(reference)')
        self.InsertColumn(3, 'Similar from ModulePath')
        self.InsertColumn(4, 'Author')
        self.InsertColumn(5, 'Description')
        self.InsertColumn(6, 'Executable Type')
        self.InsertColumn(7, 'Platform')
        self.InsertColumn(8, 'is Portable')
        self.InsertColumn(9, 'Execute Path')
        self.InsertColumn(10, 'Module Web Page')
        self.InsertColumn(11, 'DownLoad Name')
        self.InsertColumn(12, 'Hash')
        self.InsertColumn(13, 'ContentsID')
        
        
        
        con = sqlite3.connect( "./PFPModule/PFPLib/PublicPFPList/public.modulelist.sqlite" ) #self.parent.GetParent().GetParent().default_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "Select ModuleName, ContentsID, ModulePath, DownLoadName from ModuleList"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        ModuleNameList = []
        DownloadNameList = []
        ModulePathList = []
        for row in ResultList:
            ModuleNameList.append(row[0])
            DownloadNameList.append(row[3])
            s = os.path.split(row[2])
            ModulePathList.append(s[1])
        
        con.close()
        
        con = sqlite3.connect( self.parent.GetParent().GetParent().default_modulelistDB_path )
        cursor = con.cursor()
        
        idx = 0
        for row in NewModuleList:
            
            s = os.path.split(row[0])
            ListFileName = s[1]
            
            CloseDownLoadName = ""
            
            try:
                CloseMatches = difflib.get_close_matches(s[1].strip(".exe").strip(".msi").strip(".pyc").strip(".py"), DownloadNameList)
                
                if len(CloseMatches) >= 1:
                    CloseDownLoadName = str(CloseMatches[0])
                
                for DownLoadName in DownloadNameList:
                    if (DownLoadName in s[1].replace("_", " ") or DownLoadName in s[1].replace(" ", "_")) or DownLoadName in s[0].replace("\\", "/"):
                        CloseDownLoadName = DownLoadName
                        break
            except:
                CloseDownLoadName = ""
            
            if CloseDownLoadName.strip() != "":
                
                SelectQuery = "Select * from ModuleList where DownLoadName = '" + CloseDownLoadName + "'"
            
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall() 
                
                if len(ResultList) != 0:
                
                    SelectQuery = "Select Author, Description, ExecutableType, OS, isPortable, DefaultPathAfterInstall, HomePage, ContentsID, DownLoadName, ModuleName from ModuleList where DownLoadName = '" + CloseDownLoadName + "'"
                    
                    cursor.execute( SelectQuery )
                    ResultRow = cursor.fetchone()
                    
                    UtilClass = Util()
                    
                    self.InsertStringItem(idx, row[0])
                    
                    try:
                        self.SetStringItem(idx, 1, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[9]))
                    except:
                        self.SetStringItem(idx, 1, ResultRow[9])
                    try:
                        self.SetStringItem(idx, 2, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[9]))
                    except:
                        self.SetStringItem(idx, 2, ResultRow[9])
                    try:
                        self.SetStringItem(idx, 3, "")
                    except:
                        self.SetStringItem(idx, 3, "")
                    try:
                        self.SetStringItem(idx, 4, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[0]))
                    except:
                        self.SetStringItem(idx, 4, ResultRow[0])
                    try:
                        self.SetStringItem(idx, 5, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[1]))
                    except:
                        self.SetStringItem(idx, 5, ResultRow[1])
                    try:
                        self.SetStringItem(idx, 6, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[2]))
                    except:
                        self.SetStringItem(idx, 6, ResultRow[2])
                    try:
                        self.SetStringItem(idx, 7, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[3]))
                    except:
                        self.SetStringItem(idx, 7, ResultRow[3])
                    try:
                        self.SetStringItem(idx, 8, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[4]))
                    except:
                        self.SetStringItem(idx, 8, ResultRow[4])
                    try:
                        self.SetStringItem(idx, 9, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[5]))
                    except:
                        self.SetStringItem(idx, 9, ResultRow[5])
                    try:
                        self.SetStringItem(idx, 10, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[6]))
                    except:
                        self.SetStringItem(idx, 10, ResultRow[6])
                    try:
                        self.SetStringItem(idx, 11, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[8]))
                        #self.SetStringItem(idx, 12, row[1])
                    except:
                        self.SetStringItem(idx, 11, ResultRow[8])
                        
                    self.SetStringItem(idx, 12, row[1])
                    
                    try:
                        self.SetStringItem(idx, 13, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[7]))
                    except:
                        self.SetStringItem(idx, 13, ResultRow[7])
                    
                    idx += 1
                else:
                    #self.ListInsert(idx, row[0], "", "", row[1] )
                    self.InsertStringItem(idx, row[0])
                    self.SetStringItem(idx, 1, ListFileName)
                    self.SetStringItem(idx, 2, "default")
                    self.SetStringItem(idx, 3, "")
                    self.SetStringItem(idx, 4, "New")
                    self.SetStringItem(idx, 5, "New")
                    if "CommonCli" in row[0]:
                        self.SetStringItem(idx, 6, "cli")
                    else:
                        self.SetStringItem(idx, 6, "gui")
                    if ".py" in ListFileName:
                        self.SetStringItem(idx, 7, "python")
                    else:
                        self.SetStringItem(idx, 7, "win")
                    if "Setupfiles" in row[0]:
                        self.SetStringItem(idx, 8, "n")
                    else:
                        self.SetStringItem(idx, 8, "y")
                    self.SetStringItem(idx, 9, "")
                    self.SetStringItem(idx, 10, "")
                    self.SetStringItem(idx, 11, "")
                    self.SetStringItem(idx, 12, row[1])
                    self.SetStringItem(idx, 13, "")
                    
                    idx += 1 
            
            else:
                #self.ListInsert(idx, row[0], "", "", row[1] )
                self.InsertStringItem(idx, row[0])
                self.SetStringItem(idx, 1, ListFileName)
                self.SetStringItem(idx, 2, "default")
                self.SetStringItem(idx, 3, "")
                self.SetStringItem(idx, 4, "New")
                self.SetStringItem(idx, 5, "New")
                if "CommonCli" in row[0]:
                    self.SetStringItem(idx, 6, "cli")
                else:
                    self.SetStringItem(idx, 6, "gui")
                if ".py" in ListFileName:
                    self.SetStringItem(idx, 7, "python")
                else:
                    self.SetStringItem(idx, 7, "win")
                if "Setupfiles" in row[0]:
                    self.SetStringItem(idx, 8, "n")
                else:
                    self.SetStringItem(idx, 8, "y")
                self.SetStringItem(idx, 9, "")
                self.SetStringItem(idx, 10, "")
                self.SetStringItem(idx, 11, "")
                self.SetStringItem(idx, 12, row[1])
                self.SetStringItem(idx, 13, "")
                
                idx += 1 
                
        con.close()
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 120)
        self.SetColumnWidth(2, 120)
        self.SetColumnWidth(3, 0)
        self.SetColumnWidth(4, 80)
        self.SetColumnWidth(5, 130)
        self.SetColumnWidth(6, 80)
        self.SetColumnWidth(7, 80)
        self.SetColumnWidth(8, 80)
        self.SetColumnWidth(9, 200)
        self.SetColumnWidth(10, 80)
        self.SetColumnWidth(11, 80)
        self.SetColumnWidth(12, 200)
        self.SetColumnWidth(13, size.x-5)
    
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        ParentWindow = self.parent.GetParent().GetParent()
        
        con = sqlite3.connect( ParentWindow.default_modulelistDB_path )
        cursor = con.cursor()
        
        #SelectQuery = "select Author from ModuleList where ModuleName = '" + event.GetText() + "';"
        
        #cursor.execute( SelectQuery )
        #ResultList = cursor.fetchone()
        
        PopupMenu = wx.Menu()        
        
        GetAttribute  = PopupMenu.Append(-1, "Set attribute of checked item by other module")             
        SetAttributeByDefault  = PopupMenu.Append(-1, "Set attribute of checked item by default")                         
        
        self.Bind(wx.EVT_MENU, ParentWindow.OnGetAttribute, GetAttribute)
        self.Bind(wx.EVT_MENU, ParentWindow.OnSetAttributeByDefault, SetAttributeByDefault)
        #self.Bind(wx.EVT_MENU, ParentWindow.OnModyfy, ModifyModule)
        #self.Bind(wx.EVT_MENU, ParentWindow.OnInsert, InsertModule)
        #self.Bind(wx.EVT_MENU, ParentWindow.OnModuleDownload, DownloadModules)
        
    
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPoint())
        
    def OnSize(self, event):
        
        event.Skip()

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
    

#---------------------------------------------------------------------------

class NewModuleDlgAfterAdjustment(wx.Dialog):

    def __init__(self, parent, log, NewModuleList, DBPath):

        wx.Dialog.__init__(self, parent, -1, "New Modules..", size=(1600, 600), style= wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)
        
        self.default_modulelistDB_path = DBPath
        
        con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RfUmVzcG9uc2UucGZwbGlzdC5zcWxpdGU="))#"./PFPModule/PFPLib/PublicPFPList/public.1.LiveResponse.pfplist.sqlite" )
        cursor = con.cursor()
        
        SelectQuery = base64.b64decode("c2VsZWN0IFRleHQgZnJvbSBBblBvaW50VGFibGUgd2hlcmUgQ29udGVudHNJRCA9ICcxMDAwMjIn")#"select Text from AnPointTable where ContentsID = '500022'"
        cursor.execute(SelectQuery)
        
        Result = cursor.fetchone()
        
        con.close()
        
        #self.EncodedKey = "JuNZ1KK2BtbJ8IiZZbA34S50QFAH4nMd48TeoCK42cg="
        
        #print self.EncodedKey
        
        self.DecodedDummy = base64.b64decode(Result[0])
        
        panel = wx.Panel(self, -1)
        
        panel1 = wx.Panel(panel, -1, size=(-1, 25), style=wx.NO_BORDER)
        st = wx.StaticText(panel1, -1, 'Module List for newly import', (5, 5))
        st.SetForegroundColour('WHITE')
        panel1.SetBackgroundColour('BLACK')
        
        panel2 = wx.Panel(panel, -1, style=wx.BORDER_SUNKEN)
        list = ModuleListList(panel2, -1, NewModuleList)
        list.SetName('ModuleListOnList')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(list, 1, wx.EXPAND)
        panel2.SetSizer(vbox0)
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        self.CheckAll = wx.BitmapButton(panel3, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll.png'))
        self.ReleaseAll = wx.BitmapButton(panel3, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll.png'))
        self.Exceptbutton = wx.Button(panel3, label="Except")
        self.ExceptListbutton = wx.Button(panel3, label="Except List")
        self.Insertbutton = wx.Button(panel3, label="Insert")
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        
        vbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox2.Add(self.CheckAll, 0, wx.EXPAND)
        vbox2.Add(self.ReleaseAll, 0, wx.EXPAND)
        vbox2.Add(self.Exceptbutton, 0, wx.EXPAND)
        vbox2.Add(self.ExceptListbutton, 0, wx.EXPAND)
        vbox2.Add(self.Insertbutton, 0, wx.EXPAND)
        vbox2.Add(list1, 1, wx.EXPAND)
        self.CheckAll.Bind(wx.EVT_BUTTON, self.OnCheckAll)
        self.ReleaseAll.Bind(wx.EVT_BUTTON, self.OnReleaseAll)
        self.Exceptbutton.Bind(wx.EVT_BUTTON, self.OnExcept)
        self.ExceptListbutton.Bind(wx.EVT_BUTTON, self.OnExceptList)
        self.Insertbutton.Bind(wx.EVT_BUTTON, self.OnInsert)
        self.CheckAll.SetToolTip(wx.ToolTip("Check All"))
        self.ReleaseAll.SetToolTip(wx.ToolTip("Release All"))
        panel3.SetSizer(vbox2)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(panel2, 1, wx.EXPAND)
        vbox1.Add(panel3, 0, wx.EXPAND)
        
        panel.SetSizer(vbox1)

        #TestUltimateListCtrl(panel, log, NewModuleList)


        #self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()

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
    
    def OnExcept(self, event):
        
        dlg = wx.MessageDialog(None, "Are you sure to expect the selected modules?", 'warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:
          
            con = sqlite3.connect( self.default_modulelistDB_path )
            cursor = con.cursor()
            
            window = self.FindWindowByName('ModuleListOnList')
            for index in range(window.GetItemCount()-1, -1, -1):
                if window.IsChecked(index): 
                    
                    FilePath = window.GetItem(index,0).GetText()
                    MD5 = window.GetItem(index,11).GetText()
                    
                    InsertQuery = "Insert into ExceptionHashList (RowID, FileName, MD5) values (null, '" + FilePath + "', '" + MD5 + "')"
            
                    cursor.execute( InsertQuery )
                    con.commit()
                    
                    window.DeleteItem(index)     
    
            con.close()
    
        return
    
    def OnExceptList(self, event):
        
        dia = ExceptionHashListDlg(None, sys.stdout, self.default_modulelistDB_path)
        dia.ShowModal()
        dia.Destroy()
        
        return
    
    def OnInsert(self, event):
        
        #Get user and contact
        self.user = ""
        self.contact = ""
        
        config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "r")
        filelines = config_fp.readlines()
        config_fp.close()
        
        for line in filelines:
            if "user(pfp id)" in line:
                self.user =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "contact" in line:
                self.contact =  line.split(">")[1].strip("\"").strip("\n")
        
        
        window = self.FindWindowByName('ModuleListOnList')
        for idx in range(window.GetItemCount()-1, -1, -1):
        #for idx in range(window.GetItemCount()):
            if window.IsChecked(idx): 
                
                con = sqlite3.connect( self.default_modulelistDB_path )
                cursor = con.cursor()
                
                #is Modulename duplicated?
                SelectQuery = "select * from ModuleList where ModuleName = '" +window.GetItem(idx,1).GetText()+ "'"
                cursor.execute( SelectQuery )
                EmptyTestResultList = cursor.fetchall()
                
                if len(EmptyTestResultList) > 0 or window.GetItem(idx,1).GetText() == "default":
                    wx.MessageBox("ModuleName(" + window.GetItem(idx,1).GetText() + ") is conflict")
                    continue
                
                else:
                
                    if window.GetItem(idx,2).GetText() == "default":
                        TargetExtender = ""
                        TargetSignature = "" 
                    else:
                        SelectQuery = "select TargetExtender, TargetSignature from ModuleList where ModuleName = '" + window.GetItem(idx,2).GetText() +"'"
                        cursor.execute( SelectQuery )
                        ResultRow = cursor.fetchone()
                        
                        TargetExtender = ResultRow[0]
                        TargetSignature = ResultRow[1]
                    
                    UtilClass = Util()
                        
                    
                    ModuleName = window.GetItem(idx,1).GetText()
                    ModulePath = window.GetItem(idx,0).GetText() 
                    ExecutableType = window.GetItem(idx,6).GetText() 
                    ExecuteCount = "" 
                    Description = UtilClass.DummyCyber(self.DecodedDummy, window.GetItem(idx,5).GetText(), "")
                    OS = window.GetItem(idx,7).GetText() 
                    DownLoadName = UtilClass.DummyCyber(self.DecodedDummy, "") 
                    isPortable = window.GetItem(idx,8).GetText() 
                    isInstalled = "" 
                    DefaultPathAfterInstall = UtilClass.DummyCyber(self.DecodedDummy, window.GetItem(idx,9).GetText(), "") 
                    HomePage = UtilClass.DummyCyber(self.DecodedDummy, window.GetItem(idx,10).GetText(), "") 
                    UsedStatus = "y" 
                    Author = UtilClass.DummyCyber(self.DecodedDummy, window.GetItem(idx,4).GetText(), "")
                    Registrant = self.user
                    Contact = self.contact
                    md5Result = window.GetItem(idx,11).GetText()
                    ContentsID = window.GetItem(idx,12).GetText()
              
    
                    if ContentsID == "":
                        #Get next contents id
                        SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"
                        cursor.execute( SelectQuery )
                        ResultContentsID = cursor.fetchone()
                        LastContentsID = int(ResultContentsID[0])
                        NextContentsID = int(ResultContentsID[1])
                        
                        ContentsID = str(NextContentsID)
                        
                        #set next contents id
                        LastContentsID += 1
                        NextContentsID += 1
                        UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                        cursor.execute( UpdateQuery )
                        con.commit()
                    
                    InsertQuery = "insert into ModuleList ( ModuleName , ModulePath , ExecutableType , ExecuteCount , Description , OS , DownLoadName , TargetExtender , TargetSignature , isPortable , isInstalled , DefaultPathAfterInstall , HomePage , UsedStatus , Author, isDeleted, CreateTime, ModifyTime, Registrant, Contact, isPublic, ContentsID, MD5 ) values ( '" + ModuleName + "','" + ModulePath + "','" + ExecutableType + "','" + ExecuteCount + "','" + Description + "','" + OS + "','" + DownLoadName + "','" + TargetExtender + "','" + TargetSignature + "','" + isPortable + "','" + isInstalled + "','" + DefaultPathAfterInstall + "','" + HomePage + "','" + UsedStatus + "','" + Author + "', '0', '" + str(int(time.time())) + "','" + str(int(time.time())) + "','" + Registrant + "','" + Contact + "', 'n', '" + ContentsID + "', '" + md5Result + "');"
                    cursor.execute( InsertQuery )
                    con.commit()
                
                    
                    window.ToggleItem(idx)
                    window.DeleteItem(idx)
                con.close()
        return

    def OnGetAttribute(self, event):
        
        dia = GetModuleNameDlg(None, sys.stdout, self.default_modulelistDB_path)
        dia.ShowModal()
        
        dia.SelectedModuleName
        #wx.MessageBox(dia.SelectedModuleName)
        dia.Destroy()
        
        con = sqlite3.connect( "./PFPModule/PFPLib/PublicPFPList/public.modulelist.sqlite" )
        cursor = con.cursor()
        
        window = self.FindWindowByName('ModuleListOnList')
        
        FocusedItem = window.GetFocusedItem()
        
        SelectQuery = "Select Author, Description, ExecutableType, OS, isPortable, DefaultPathAfterInstall, HomePage, ContentsID, DownLoadName, ModuleName from ModuleList where ModuleName = '" + dia.SelectedModuleName + "'"
                
        cursor.execute( SelectQuery )
        ResultRow = cursor.fetchone()
        
        UtilClass = Util()
        
        #window.InsertStringItem(FocusedItem, row[0])
        try:
            window.SetStringItem(FocusedItem, 1, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[9]))
        except:
            window.SetStringItem(FocusedItem, 1, ResultRow[9])
        try:
            window.SetStringItem(FocusedItem, 2, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[9]))
        except:
            window.SetStringItem(FocusedItem, 2, ResultRow[9])
        try:
            window.SetStringItem(FocusedItem, 3, "")
        except:
            window.SetStringItem(FocusedItem, 3, "")
        try:
            window.SetStringItem(FocusedItem, 4, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[0]))
        except:
            window.SetStringItem(FocusedItem, 4, ResultRow[0])
        try:
            window.SetStringItem(FocusedItem, 5, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[1]))
        except:
            window.SetStringItem(FocusedItem, 5, ResultRow[1])
        try:
            window.SetStringItem(FocusedItem, 6, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[2]))
        except:
            window.SetStringItem(FocusedItem, 6, ResultRow[2])
        try:
            window.SetStringItem(FocusedItem, 7, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[3]))
        except:
            window.SetStringItem(FocusedItem, 7, ResultRow[3])
        try:
            window.SetStringItem(FocusedItem, 8, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[4]))
        except:
            window.SetStringItem(FocusedItem, 8, ResultRow[4])
        try:
            window.SetStringItem(FocusedItem, 9, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[5]))
        except:
            window.SetStringItem(FocusedItem, 9, ResultRow[5])
        try:
            window.SetStringItem(FocusedItem, 10, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[6]))
        except:
            window.SetStringItem(FocusedItem, 10, ResultRow[6])
        try:
            window.SetStringItem(FocusedItem, 11, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[8]))
            #window.SetStringItem(FocusedItem, 12, row[1])
        except:
            window.SetStringItem(FocusedItem, 11, ResultRow[8])
        try:
            window.SetStringItem(FocusedItem, 13, UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[7]))
        except:
            window.SetStringItem(FocusedItem, 13, ResultRow[7])
        
        
        
        return
    
    def OnSetAttributeByDefault(self, event):
        
        window = self.FindWindowByName('ModuleListOnList')
        for idx in range(window.GetItemCount()):
            if window.IsChecked(idx): 
                #window.SetStringItem(idx, 0, row[0])
                #window.SetStringItem(idx, 1, ListFileName)
                window.SetStringItem(idx, 2, "default")
                window.SetStringItem(idx, 3, "")
                window.SetStringItem(idx, 4, "New")
                window.SetStringItem(idx, 5, "New")
                if "CommonCli" in window.GetItem(idx,0).GetText():
                    window.SetStringItem(idx, 6, "cli")
                else:
                    window.SetStringItem(idx, 6, "gui")
                if ".py" in window.GetItem(idx,1).GetText():
                    window.SetStringItem(idx, 7, "python")
                else:
                    window.SetStringItem(idx, 7, "win")
                if "Setupfiles" in window.GetItem(idx,0).GetText():
                    window.SetStringItem(idx, 8, "n")
                else:
                    window.SetStringItem(idx, 8, "y")
                window.SetStringItem(idx, 9, "")
                window.SetStringItem(idx, 10, "")
                #window.SetStringItem(idx, 11, row[1])
        
        return
    
#---------------------------------------------------------------------------
"""
if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()
"""

