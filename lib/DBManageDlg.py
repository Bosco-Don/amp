#!/usr/bin/python
# -*- coding: utf-8 -*-


from InternalModules.pfp_sdk.PFPUtil import *


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




class DBManageDlg(wx.Dialog):
    

    def __init__(self, parent, title, ModifyFlag, DBPath, User, Contact, ContentsID):    
        wx.Dialog.__init__(self, parent, title=title, size=(700, 800), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.ModifyFlag = ModifyFlag
        self.DBPath = DBPath
        self.User = User
        self.Contact = Contact
        self.ContentsID = ContentsID

        self.InitUI(ModifyFlag)
        self.Centre()
        self.Show()     

    def InitUI(self, ModyfyFlag):
        
        con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RfUmVzcG9uc2UucGZwbGlzdC5zcWxpdGU="))#"./PFPModule/PFPLib/PublicPFPList/public.1.LiveResponse.pfplist.sqlite" )
        cursor = con.cursor()
        
        SelectQuery = base64.b64decode("c2VsZWN0IFRleHQgZnJvbSBBblBvaW50VGFibGUgd2hlcmUgQ29udGVudHNJRCA9ICcxMDAwMjIn")#"select Text from AnPointTable where ContentsID = '500022'"
        cursor.execute(SelectQuery)
        
        Result = cursor.fetchone()
        
        con.close()
        
        #self.EncodedKey = "JuNZ1KK2BtbJ8IiZZbA34S50QFAH4nMd48TeoCK42cg="
        
        #print self.EncodedKey
        
        self.DecodedDummy = base64.b64decode(Result[0])
        
        ResultList = []
        
        ModuleName = ""
                
        ModulePath = ""
        
        ExecutableType = ""
    
        ExecuteCount = ""
    
        Description = ""
    
        OS = ""
    
        DownLoadName = ""
    
        isDeleted = ""
    
        TargetExtender = ""
    
        TargetSignature = ""
    
        isPortable = ""
    
        isInstalled = ""
    
        DefaultPathAfterInstall = ""
    
        HomePage = ""
    
        UsedStatus = ""
    
        Author = ""
        
        AttrLoadDB = ""
        
        if ModyfyFlag == "modi" or ModyfyFlag == "insertUseReference":
            
            if(ModyfyFlag == "modi"):
                AttrLoadDB = self.DBPath
            elif ModyfyFlag == "insertUseReference":
                AttrLoadDB = "./PFPModule/PFPLib/PublicPFPList/public.modulelist.sqlite"
                
            con = sqlite3.connect( AttrLoadDB )
            cursor = con.cursor()
            
            SelectQuery = "select ModuleName, ModulePath, ExecutableType, ExecuteCount, Description, OS, DownLoadName, isDeleted, TargetExtender, TargetSignature, isPortable, isInstalled, DefaultPathAfterInstall, HomePage, UsedStatus, Author from ModuleList where ContentsID = '" + self.ContentsID.strip() + "';"
            cursor.execute( SelectQuery )
            ResultList = cursor.fetchone()
            con.close()
            
            UtilClass = Util()
            
            try:
                ModuleName = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[0])
            except:
                ModuleName = ResultList[0]
                
            try:    
                ModulePath = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[1])
            except:
                ModulePath = ResultList[1]
                
            try:
                ExecutableType = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[2])
            except:
                ExecutableType = ResultList[2]
                
            try:
                ExecuteCount = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[3])
            except:
                ExecuteCount = ResultList[3]
                
            try:
                Description = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[4])
            except:
                Description = ResultList[4]
                
            try:
                OS = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[5])
            except:
                OS = ResultList[5]
                
            try:
                DownLoadName = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[6])
            except:
                DownLoadName = ResultList[6]
                
            try:
                isDeleted = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[7])
            except:
                isDeleted = ResultList[7]
                
            try:
                TargetExtender = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[8])
            except:
                TargetExtender = ResultList[8]
                
            try:
                TargetSignature = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[9])
            except:
                TargetSignature = ResultList[9]
                
            try:
                isPortable = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[10])
            except:
                isPortable = ResultList[10]
                
            try:
                isInstalled = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[11])
            except:
                isInstalled = ResultList[11]
                
            try:
                DefaultPathAfterInstall = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[12])
            except:
                DefaultPathAfterInstall = ResultList[12]
                
            try:
                HomePage = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[13])
            except:
                HomePage = ResultList[13]
                
            try:
                UsedStatus = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[14])
            except:
                UsedStatus = ResultList[14]
                
            try:
                Author = UtilClass.DummyCyber(self.DecodedDummy, "", ResultList[15])
            except:
                Author = ResultList[15]
            
        
        
            
        panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(5, 5)

        #Main Text
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            text1 = wx.StaticText(panel, label="Modify Module")
            sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        else:
            text1 = wx.StaticText(panel, label="Input New")
            sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        #Logo
        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/SelfTest.png'))
        sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=5)

        #path
        text2 = wx.StaticText(panel, label="Module Path")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc2 = wx.TextCtrl(panel)
        sizer.Add(self.tc2, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.button2 = wx.Button(panel, label="Browse..")
        sizer.Add(self.button2, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonModulePath)
        
        self.tc2.Disable()
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc2.WriteText(ModulePath)
            #self.button2.Disable()
        
        #name
        text3 = wx.StaticText(panel, label="Module Name")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT, border=5)
        
        self.tc3 = wx.TextCtrl(panel)
        sizer.Add(self.tc3, pos=(3, 1), flag=wx.TOP|wx.EXPAND, border=5)
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc3.WriteText(ModuleName)
            #self.tc3.Disable()
            
        #Author
        text31 = wx.StaticText(panel, label="                    Author")
        sizer.Add(text31, pos=(3, 2), flag=wx.LEFT, border=5)
        
        self.tc31 = wx.TextCtrl(panel)
        sizer.Add(self.tc31, pos=(3, 3), flag=wx.TOP|wx.EXPAND, border=5)
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc31.WriteText(Author)

        #description        
        text4 = wx.StaticText(panel, label="Description")
        sizer.Add(text4, pos=(4, 0), flag=wx.LEFT, border=5)
        
        self.tc4 = wx.TextCtrl(panel)
        sizer.Add(self.tc4, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc4.WriteText(Description)
        
        #executable type and os
        text51 = wx.StaticText(panel, label="Executable Type")
        sizer.Add(text51, pos=(5, 0), flag=wx.LEFT, border=5)
        
        Typelist = ["gui", "cli"]
        self.combo51 = wx.ComboBox(panel, choices=Typelist)
        sizer.Add(self.combo51, pos=(5, 1), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.combo51.Bind(wx.EVT_COMBOBOX, self.OnExecutableTypeComboSelect)
        
        text52 = wx.StaticText(panel, label="                    Platform")
        sizer.Add(text52, pos=(5, 2), flag=wx.RIGHT|wx.EXPAND, border=5)
        
        PlatformList = ["Windows", "Mac OS X", "Linux", "python"]
        self.combo52 = wx.ComboBox(panel, choices=PlatformList)
        sizer.Add(self.combo52, pos=(5, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.combo51.WriteText("gui")
        self.combo52.WriteText("Windows")
        
        if ModyfyFlag == "modi" or ModyfyFlag == "insertUseReference":
            if 'gui' in ExecutableType:
                self.combo51.SetStringSelection("gui")
            if 'cli' in ExecutableType:
                self.combo51.SetStringSelection("cli")
                
            if 'win' in OS:
                self.combo52.SetStringSelection("Windows")
            if 'mac' in OS:
                self.combo52.SetStringSelection("Mac OS X")
            if 'lin' in OS:
                self.combo52.SetStringSelection("Linux")
            if 'python' in OS:
                self.combo52.SetStringSelection("python")
        
        #argument
        text6 = wx.StaticText(panel, label="Argument")
        sizer.Add(text6, pos=(6, 0), flag=wx.LEFT, border=5)
        
        self.tc61 = wx.TextCtrl(panel)
        sizer.Add(self.tc61, pos=(6, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.button6 = wx.Button(panel, label="Add")
        sizer.Add(self.button6, pos=(6, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button6.Bind(wx.EVT_BUTTON, self.OnButtonArgumentAdd)
        
        self.tc7 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.ST_NO_AUTORESIZE)
        sizer.Add(self.tc7, pos=(7, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        if 'cli' not in self.combo51.GetValue():
            self.tc61.SetEditable(0)
            self.tc7.SetEditable(0)
            self.button6.Disable()
            
        if ModyfyFlag == "modi" and 'cli' in self.combo51.GetValue():
            con = sqlite3.connect( self.DBPath )
            cursor = con.cursor()
            
            """
            SelectQuery = "select ContentsID from ModuleList where ModuleName = '" + self.ModuleName.replace("[#]","") + "';"
            cursor.execute( SelectQuery )
            ModuleIDRow = cursor.fetchone()
            """
            
            SelectQuery = "select Argument from ArgumentList where ModuleID = '" + self.ContentsID + "';"
            cursor.execute( SelectQuery )
            ArgumentResultList = cursor.fetchall()
            
            con.close()
            
            for ResultRow in ArgumentResultList:
                
                try:
                    Argument = UtilClass.DummyCyber(self.DecodedDummy, "", ResultRow[0])
                except:
                    Argument = ResultRow[0]
                
                self.tc7.AppendText(Argument + "\n")

        #The Portable Module
        self.chk8 = wx.CheckBox(panel, label=" Portable")
        sizer.Add(self.chk8, pos=(8, 0), span=(1, 1), flag=wx.LEFT|wx.TOP, border=5)
        self.chk8.Bind(wx.EVT_CHECKBOX, self.OnCheckisPortable)
        
        text8 = wx.StaticText(panel, label="     Execute Path")
        sizer.Add(text8, pos=(8, 1), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc8 = wx.TextCtrl(panel)
        sizer.Add(self.tc8, pos=(8, 2), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=5)
        if ((ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference") and (isPortable == 'n'):
            self.tc8.WriteText(DefaultPathAfterInstall)
        
        self.chk8.SetValue(1)
        self.tc8.SetEditable(0)
        
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            if 'y' in isPortable:
                self.chk8.SetValue(1)
                self.tc8.AppendText(ModulePath)
                self.tc8.SetEditable(0)
            else:
                self.chk8.SetValue(0)
                self.tc8.SetEditable(1)
        
        #file
        self.chk9 = wx.CheckBox(panel, label=" Module can analyze specific file format")
        sizer.Add(self.chk9, pos=(9, 0), span=(1, 5), flag=wx.LEFT|wx.TOP, border=5)
        self.chk9.Bind(wx.EVT_CHECKBOX, self.OnCheckfile)
        
        text10 = wx.StaticText(panel, label="Sample Path")
        sizer.Add(text10, pos=(10, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc10 = wx.TextCtrl(panel)
        sizer.Add(self.tc10, pos=(10, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.button10 = wx.Button(panel, label="Add")
        sizer.Add(self.button10, pos=(10, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button10.Bind(wx.EVT_BUTTON, self.OnButtonFileSamplePath)
        
        self.text11 = wx.StaticText(panel, label="Target Extender")
        sizer.Add(self.text11, pos=(11, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc11 = wx.TextCtrl(panel)
        sizer.Add(self.tc11, pos=(11, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc11.WriteText(TargetExtender)
        
        text12 = wx.StaticText(panel, label="Target Signature")
        sizer.Add(text12, pos=(12, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc12 = wx.TextCtrl(panel)
        sizer.Add(self.tc12, pos=(12, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc12.WriteText(TargetSignature)
        
        self.tc10.SetEditable(0)
        self.tc11.SetEditable(0)
        self.tc12.SetEditable(0)
        self.button10.Disable()
        
        #download link
        text13 = wx.StaticText(panel, label="[Optional]")
        sizer.Add(text13, pos=(13, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        text14 = wx.StaticText(panel, label="Module Web Page")
        sizer.Add(text14, pos=(14, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc14 = wx.TextCtrl(panel)
        sizer.Add(self.tc14, pos=(14, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc14.WriteText(HomePage)
            
        text15 = wx.StaticText(panel, label="DownLoad Name")
        sizer.Add(text15, pos=(15, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc15 = wx.TextCtrl(panel)
        sizer.Add(self.tc15, pos=(15, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        if(ModyfyFlag == "modi") or ModyfyFlag == "insertUseReference":
            self.tc15.WriteText(DownLoadName)
        
        #Last Button
        self.button150 = wx.Button(panel, label='Help')
        sizer.Add(self.button150, pos=(16, 0), flag=wx.LEFT, border=10)
        self.button150.Bind(wx.EVT_BUTTON, self.OnButtonHelp)

        self.button151 = wx.Button(panel, label="Ok")
        sizer.Add(self.button151, pos=(16, 2), flag=wx.BOTTOM|wx.RIGHT)
        self.button151.Bind(wx.EVT_BUTTON, self.OnButtonOK)

        self.button152 = wx.Button(panel, label="Cancel")
        sizer.Add(self.button152, pos=(16, 3), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=5)
        self.button152.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        
        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
        
    def OnExecutableTypeComboSelect(self, event):
        SelectedText = self.combo51.GetValue()
        
        if SelectedText == "cli":
            self.tc61.SetEditable(1)
            self.tc7.SetEditable(1)
            self.button6.Enable()
        else:
            self.tc61.SetEditable(0)
            self.tc7.SetEditable(0)
            self.button6.Disable()
            
            
    def OnCheckisPortable(self, event):
        isChecked = self.chk8.GetValue()
        
        if isChecked == 1:
            self.chk8.SetValue(1)
            self.tc8.SetEditable(0)
        else:
            self.chk8.SetValue(0)
            self.tc8.SetEditable(1)
            
    def OnCheckfile(self, event):
        isChecked = self.chk9.GetValue()
        
        if isChecked == 1:
            self.tc10.SetEditable(1)
            self.tc11.SetEditable(1)
            self.tc12.SetEditable(1)
            self.button10.Enable()
        else:
            self.tc10.SetEditable(0)
            self.tc11.SetEditable(0)
            self.tc12.SetEditable(0)
            self.button10.Disable()

            
    def OnButtonModulePath(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile="", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
        
                    
            if SelectedFile.find("UserModule") != -1:
                
                Num = SelectedFile.find("UserModule")
                
                SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
                
                self.tc2.Clear()
                self.tc2.WriteText(SelectedFile)
                
                if self.ModifyFlag != "modi" and self.tc3.GetLineText(0) == "" :
                    self.tc3.Clear()
                    self.tc3.WriteText(os.path.split(SelectedFile)[1])
                 
            elif SelectedFile.find("PFPModule\\PFPLib\\InternalModules") != -1:
                
                Num = SelectedFile.find("PFPModule\\PFPLib\\InternalModules")
                
                SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
    
                self.tc2.Clear()
                self.tc2.WriteText(SelectedFile)
                
                if self.ModifyFlag != "modi" and self.tc3.GetLineText(0) == "" :
                    self.tc3.Clear()
                    self.tc3.WriteText(os.path.split(SelectedFile)[1])
                                 
            else :
                SelectedFile = "./" + os.path.split(SelectedFile)[1]
                #SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
                
                self.tc2.Clear()
                self.tc2.WriteText(SelectedFile)
                
                if self.ModifyFlag != "modi" and self.tc3.GetLineText(0) == "" :
                    self.tc3.Clear()
                    self.tc3.WriteText(os.path.split(SelectedFile)[1])
                     
                #wx.MessageBox("Select Module in %PFPROOT%/UserModule/")
        
        return
    
    def OnButtonArgumentAdd(self, event):
        
        NewArgument = self.tc61.GetLineText(0)
        self.tc7.AppendText(NewArgument + "\n")
        
        return
    
    def OnButtonFileSamplePath(self, event):
        
        SelfTest = PFPUtil()
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultFile="", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
            
            self.tc10.Clear()
            self.tc10.WriteText(SelectedFile)
            
            self.tc11.WriteText(os.path.splitext(SelectedFile)[1] + ",")
            
            fp = open(SelectedFile)
            Hex = fp.read(2)
            Signature = SelfTest.HexValue_to_HexString(Hex)
            fp.close()
            self.tc12.WriteText(Signature + ",")
        
        return
    
    def OnButtonHelp(self, event):
        
        wx.MessageBox("Portable Forensic Platform - TheSOFT\n\nContact : \thttp://thesoft.org/\nblog : \thttp://portable-forensics.blogspot.kr/\n")
        
        return
    
    def OnButtonOK(self, event):
         
        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        ModuleName = self.tc3.GetLineText(0)
        
        """
        if self.ModifyFlag != "modi":
            ModuleName = self.tc3.GetLineText(0)
        else:
            ModuleName = self.tc3.GetLineText(0).replace(" ", "_")
        """
        if ModuleName.strip() == "":
            wx.MessageBox("Module name can not blank.")
            return 
            
        ModulePath = self.tc2.GetLineText(0)
        
        ExecutableType = self.combo51.GetValue()
        
        ExecuteCount = ""
        
        Description = self.tc4.GetLineText(0)
        
        OS = ""
        if self.combo52.GetValue() == "Windows":
            OS = "win"
        if self.combo52.GetValue() == "Mac OS X":
            OS = "mac"
        if self.combo52.GetValue() == "Linux":
            OS = "lin"
        if self.combo52.GetValue() == "python":
            OS = "python"
        
        AnalysisType = ""
        TargetExtender = ""
        TargetSignature = ""
        
        TargetExtender = self.tc11.GetLineText(0)
        TargetSignature = self.tc12.GetLineText(0)
            
        isPortable = ""
        isInstalled = ""
        DefaultPathAfterInstall = ""
        if self.chk8.GetValue() == 1:
            isPortable = "y"
            isInstalled = ""
            DefaultPathAfterInstall = ModulePath
        else :
            DefaultPathAfterInstall = self.tc8.GetLineText(0)
            isPortable = "n"
            isInstalled = ""
            if os.path.isfile(DefaultPathAfterInstall) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isfile(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")) \
                or os.path.isdir(DefaultPathAfterInstall) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files (x86)", "Program Files")) or os.path.isdir(DefaultPathAfterInstall.replace("Program Files", "Program Files (x86)")):
                isInstalled = "y"
            else :
                isInstalled = "n" 
            
        HomePage = self.tc14.GetLineText(0)
        
        DownLoadName = self.tc15.GetLineText(0)
        
        UsedStatus = "y"
        
        Author = self.tc31.GetLineText(0)
        
        #wx.MessageBox(ModuleName + ":" + ModulePath + ":" + ExecutableType + ":" +ExecuteCount + ":" +Description + ":" + OS + ":" +DownLoadName + ":" +AnalysisType + ":" +TargetExtender + ":" +TargetSignature + ":" +isPortable + ":" +isInstalled + ":" +DefaultPathAfterInstall + ":" +DownLoadLink + ":" +UsedStatus)
        

        UtilClass = Util()
        
        try:
            Author = UtilClass.DummyCyber(self.DecodedDummy, Author, "")
        except:
            Author = Author
        
        try:
            Description = UtilClass.DummyCyber(self.DecodedDummy, Description, "")
        except:
            Description = Description
            
        try:
            DefaultPathAfterInstall = UtilClass.DummyCyber(self.DecodedDummy, DefaultPathAfterInstall, "")
        except:
            DefaultPathAfterInstall = DefaultPathAfterInstall
            
        try:
            TargetExtender = UtilClass.DummyCyber(self.DecodedDummy, TargetExtender, "")
        except:
            TargetExtender = TargetExtender
            
        try:
            TargetSignature = UtilClass.DummyCyber(self.DecodedDummy, TargetSignature, "")
        except:
            TargetSignature = TargetSignature
            
        try:
            HomePage = UtilClass.DummyCyber(self.DecodedDummy, HomePage, "")
        except:
            HomePage = HomePage
        
        """    
        try:
            DownLoadName = UtilClass.DummyCyber(self.DecodedDummy, DownLoadName, "")
        except:
            DownLoadName = DownLoadName
        """
        
        #, Description, DefaultPathAfterInstall, TargetExtender, TargetSignature, HomePage, DownLoadLink, DownLoadName
        
        
        
        if self.ModifyFlag == 'insert' or self.ModifyFlag == "insertUseReference":
            Registrant = self.User
            Contact = self.Contact
            
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

            cursor.execute( SelectQuery )
            ResultContentsID = cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

            cursor.execute( SelectQuery )
            ResultContentsID = cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            
            #Calculate MD5
            md5Result = ""
            
            if ModulePath.strip() != "":
                md5Result = hashlib.md5(open(ModulePath,"rb").read()).hexdigest()
            
            self.ContentsID = str(NextContentsID)
            
            InsertQuery = "insert into ModuleList ( ModuleName , ModulePath , ExecutableType , ExecuteCount , Description , OS , DownLoadName , TargetExtender , TargetSignature , isPortable , isInstalled , DefaultPathAfterInstall , HomePage , UsedStatus , Author, isDeleted, CreateTime, ModifyTime, Registrant, Contact, isPublic, ContentsID, MD5 ) values ( '" + ModuleName + "','" + ModulePath + "','" + ExecutableType + "','" + ExecuteCount + "','" + Description + "','" + OS + "','" + DownLoadName + "','" + TargetExtender + "','" + TargetSignature + "','" + isPortable + "','" + isInstalled + "','" + DefaultPathAfterInstall + "','" + HomePage + "','" + UsedStatus + "','" + Author + "', '0', '" + str(int(time.time())) + "','" + str(int(time.time())) + "','" + Registrant + "','" + Contact + "', 'y', '" + str(NextContentsID) + "', '" + md5Result + "');"
            cursor.execute( InsertQuery )
            con.commit()
            
            
            LastContentsID += 1
            NextContentsID += 1
            UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
            cursor.execute( UpdateQuery )
            con.commit()
            
        elif self.ModifyFlag == 'modi':
            UpdateQuery = "update ModuleList set ModuleName = '" + ModuleName + "',ModulePath = '" + ModulePath + "',ExecutableType = '" + ExecutableType + "',ExecuteCount = '" + ExecuteCount + "',Description = '" + Description + "',OS='" + OS + "',DownLoadName='" + DownLoadName + "',TargetExtender='" + TargetExtender + "',TargetSignature='" + TargetSignature + "',isPortable='" + isPortable + "',isInstalled='" + isInstalled + "',DefaultPathAfterInstall='" + DefaultPathAfterInstall + "',HomePage='" + HomePage + "',Author='" + Author + "' where ContentsID = '" + self.ContentsID + "'"
            cursor.execute( UpdateQuery )
            con.commit()
            
            UpdateQuery = "update ModuleList set ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.ContentsID + "'"
            cursor.execute( UpdateQuery )
            con.commit()
            
            if os.path.isfile(ModulePath) or os.path.isfile(DefaultPathAfterInstall):
                UpdateQuery = "update ModuleList set UsedStatus='y' where ContentsID = '" + self.ContentsID + "'"
                cursor.execute( UpdateQuery )
                con.commit()
        
        #---Argument Add
        ################
        
        #wipe existing
        SelectQuery = "select Argument from ArgumentList where ModuleID = " + self.ContentsID
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        for row in ResultList:  
            DeleteFlag = True
            
            if row[0].strip() == "":
                continue
              
            for linenum in range(0,self.tc7.GetNumberOfLines()):
                Argument = self.tc7.GetLineText(linenum)
                
                if Argument.strip() == row[0]:
                    DeleteFlag = False
            
            if DeleteFlag == True:
                DeleteQuery = "delete from ArgumentList where ModuleID = " + self.ContentsID + " and Argument = '" + row[0] + "'"
                #print DeleteQuery
                cursor.execute( DeleteQuery )
                con.commit()
        
        #insert new
        for linenum in range(0,self.tc7.GetNumberOfLines()):  
            InsertFlag = True
            Argument = self.tc7.GetLineText(linenum)
            
            if Argument.strip() == "":
                continue
              
            for row in ResultList:
                
                if Argument.strip() == row[0]:
                    InsertFlag = False
            
            if InsertFlag == True:
                SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

                cursor.execute( SelectQuery )
                ResultContentsID = cursor.fetchone()
                LastContentsID = int(ResultContentsID[0])
                NextContentsID = int(ResultContentsID[1])

                UtilClass = Util()

                try:
                    Argument = UtilClass.DummyCyber(self.DecodedDummy, Argument, "")
                except:
                    Argument = Argument

                InsertQuery = "insert into ArgumentList ( ModuleID , Argument, ArgumentDescription , isDeleted, ContentsID, CreateTime, ModifyTime ) values ( " + self.ContentsID + ",'" + Argument.strip() + "','','1','" + str(NextContentsID) + "', '"+str(int(time.time()))+"', '"+str(int(time.time()))+"');"
                cursor.execute( InsertQuery )
                con.commit()
                
                LastContentsID += 1
                NextContentsID += 1
                UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                cursor.execute( UpdateQuery )
                con.commit()

            
        con.close()
        
        self.Close()
        
        return
    
    def OnButtonCancel(self, event):
        
        self.Close()
        
        return



    