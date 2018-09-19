# coding: utf-8
#!/usr/bin/python


from InternalModules.pfp_sdk.PFPUtil import *

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


class TargetList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/filesystem_meta_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.parent = parent
        
        self.idx = 0
        
        self.InsertColumn(0, 'File system')
        self.InsertColumn(1, 'Path')
        self.InsertColumn(2, 'ImagePath')
        
        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 150)


    def OnRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        PopupMenu = wx.Menu()        
    
        #AddimageMenu = PopupMenu.Append(wx.ID_ANY, "Add image file")
        #self.Bind(wx.EVT_MENU, self.OnAddimage, AddimageMenu)
        
        AddmountedvolumeMenu = PopupMenu.Append(wx.ID_ANY, "Add mounted volume")
        self.Bind(wx.EVT_MENU, self.OnAddmountedvolume, AddmountedvolumeMenu)
        
        if os.path.isfile("PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe"):
            AddimagefileMenu = PopupMenu.Append(wx.ID_ANY, "Add image file")
            self.Bind(wx.EVT_MENU, self.OnAddimagefile, AddimagefileMenu)
            
        #print item, flags 
        if 0 <= item:
            self.current = item
            #self.SelectItem(item)
            DeleteMenu = PopupMenu.Append(wx.ID_ANY, "Delete")
            self.Bind(wx.EVT_MENU, self.OnDelete, DeleteMenu)


        #self.PopUpSelectedRow = event.GetRow()
        
        self.PopupMenu(PopupMenu, event.GetPosition())
        
        
    def OnAddimage(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target Volume", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
            
            
            #is volume valid
            ######################
            ResultLines = []
            path = os.path.abspath(".")
            pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\pfp_sdk\\bin\\tsk_bin\\fsstat.exe")
            cmdARGS = [pathchange.decode('cp949'), SelectedFile]
            #print cmdARGS
            self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.pipe.stdin.close()
 
            self.NowTerminalProcessPid = self.pipe.pid 
    
            while self.pipe.poll() == None:
                result = self.pipe.stdout.readline()
                if result.strip() != "":
                    ResultLines.append(result.strip())
                    
            result = self.pipe.stdout.readline()
            if result.strip() != "":
                ResultLines.append(result.strip())
            
            
            try:
                if "FILE SYSTEM INFORMATION" in ResultLines[0]:
                    FirstLine = ResultLines[0]
            except:
                wx.MessageBox("Invalid volume. cannot determine file system type.")
                return
            
            
            if "FILE SYSTEM INFORMATION" in ResultLines[0]:
        
                self.InsertStringItem(self.idx, ResultLines[2].split(":")[1].strip())
                self.SetStringItem(self.idx, 1, " " + SelectedFile)
                self.idx += 1           
                
                return
                
            else:
                
                wx.MessageBox("Invalid volume. cannot determine file system type.")
                
                return
        
        
        #self.List41.InsertStringItem(self.targetidx, "[...]")
        
        
        return
    
    
    def OnAddmountedvolume(self, event):
        
        dlg = wx.DirDialog(self, message="Select Target Volume", style=wx.OPEN)
        
        SelectedVolume = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedVolume = dlg.GetPath()
            
            
            #is volume valid
            ######################
            ResultLines = []
            path = os.path.abspath(".")
            pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\pfp_sdk\\bin\\tsk_bin\\fsstat.exe")
            cmdARGS = [pathchange.decode('cp949'), "\\\\.\\" + SelectedVolume.replace("\\", "")]
            #print cmdARGS
            self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.pipe.stdin.close()
 
            self.NowTerminalProcessPid = self.pipe.pid 
    
            while self.pipe.poll() == None:
                result = self.pipe.stdout.readline()
                if result.strip() != "":
                    ResultLines.append(result.strip())
                    
            result = self.pipe.stdout.readline()
            if result.strip() != "":
                ResultLines.append(result.strip())
            
            try:
                if "FILE SYSTEM INFORMATION" in ResultLines[0]:
                    FirstLine = ResultLines[0]
            except:
                wx.MessageBox("Invalid volume. cannot determine file system type.")
                return
            
            if "FILE SYSTEM INFORMATION" in ResultLines[0]:
                   
                self.InsertStringItem(self.idx, ResultLines[2].split(":")[1].strip())
                self.SetStringItem(self.idx, 1, " " + "\\\\.\\" + SelectedVolume.replace("\\", ""))
                self.idx += 1
                
                return
                
            else:
                
                wx.MessageBox("Invalid volume. cannot determine file system type.")
                
                return
                
    
    
    def OnAddimagefile(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target Volume", style=wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
            
            #Mount Image
            #MIP로 1차 시도 후, 
            #안될 경우 2차 OSF 64비트, 
            #또 안되면 OSF 32비트로 진행 
            ######################
            ResultLines = []
            BlankDrvLetter = ""
            RecievedDriveLetters = []
            path = os.path.abspath(".")
            
            if sys.argv[1] == "True":   #is managing on == true 일 경우 
                pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe")
                cmdARGS = [pathchange.decode('cp949'), "mount", SelectedFile, "/B:F", "/A:T", "/T:1"]
            else:
                AA = 1
                """ OSF 마운트는 고려할 게 참 많다..
                DrvLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                              "r", "s", "t", "u", "v", "w", "x", "y", "z"]
                for DrvLetter in DrvLetters:
                    if os.path.isdir(DrvLetter + ":") == False:
                        BlankDrvLetter = DrvLetter
                pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\OSFMount(x64)\\OSFMount.com")
                cmdARGS = [pathchange.decode('cp949'), "-a", "-t", "file", "-f", SelectedFile, "-m", BlankDrvLetter + ":"]
                #RecievedDriveLetters = ??
                """
                
            #print cmdARGS
            self.pipe = subprocess.Popen(cmdARGS, shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.pipe.stdin.close()
 
            self.NowTerminalProcessPid = self.pipe.pid 
    
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
                            RecievedDriveLetters.append(line.strip().split(":")[1].strip())
                            self.InsertStringItem(self.idx, "Mnt as " + line.strip().split(":")[1].strip() + ":")
                            self.SetStringItem(self.idx, 1, " " + os.path.split(SelectedFile)[1]+":"+str(part_count))
                            self.SetStringItem(self.idx, 2, SelectedFile)
                            self.idx += 1
                            part_count += 1
                
            if "Created device" in ResultString:
                self.InsertStringItem(self.idx, "Mnt as " + BlankDrvLetter + ":")
                self.SetStringItem(self.idx, 1, " " + os.path.split(SelectedFile)[1])
                self.SetStringItem(self.idx, 2, SelectedFile)
                self.idx += 1
                    
        
        return
    
    
    
    
    def OnDelete(self, event):
        
        self.DeleteItem(self.current)
        self.idx -= 1
        
        return
    
    


class LogList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/process_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.parent = parent
        self.idx = 0


class CaseCreateDlg(wx.Frame):
    

    def __init__(self, parent, title):    
        #wx.Dialog.__init__(self, parent, title=title, size=(700, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        super(CaseCreateDlg, self).__init__(parent, title=title, pos=(100,100), size=(700,600))

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
        self.Cancel = False
        #self.Bind(wx.EVT_CLOSE, self.OnButtonCancel)
            
        
        self.panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(5, 5)

                
        #name
        text1 = wx.StaticText(self.panel, label="     Case Name")
        sizer.Add(text1, pos=(1, 0), flag=wx.LEFT, border=5)
        
        self.tc1 = wx.TextCtrl(self.panel)
        sizer.Add(self.tc1, pos=(1, 1), flag=wx.TOP|wx.EXPAND, border=5)
        self.tc1.WriteText("Case")
        
        
        
        #path
        text2 = wx.StaticText(self.panel, label="     Case Path")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc2 = wx.TextCtrl(self.panel)
        sizer.Add(self.tc2, pos=(2, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=5)
        #self.tc2.WriteText("%UserProfile%\Desktop")
        
        self.button2 = wx.Button(self.panel, label="Browse..")
        sizer.Add(self.button2, pos=(2, 3), flag=wx.TOP|wx.RIGHT, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonModulePath)
        
        self.tc2.Disable()
        
        
      
        #executable type and os
        text31 = wx.StaticText(self.panel, label="     Timezone")
        sizer.Add(text31, pos=(3, 0), flag=wx.LEFT, border=5)
        
        Typelist = ["(UTC-12:00) International Date Line West",
                    "(UTC-11:00) Coordinated Universal Time -11",
                    "(UTC-10:00) Hawaii",
                    "(UTC-09:00) Alaska",
                    "(UTC-08:00) Pacific Time (US and Canada)",
                    "(UTC-08:00) Baja California",
                    "(UTC-07:00) Mountain Time (US and Canada)",
                    "(UTC-07:00) Chihuahua, La Paz, Mazatlan",
                    "(UTC-07:00) Arizona",
                    "(UTC-06:00) Saskatchewan",
                    "(UTC-06:00) Central America",
                    "(UTC-06:00) Central Time (US and Canada)",
                    "(UTC-06:00) Guadalajara, Mexico City, Monterrey",
                    "(UTC-05:00) Eastern Time (US and Canada)",
                    "(UTC-05:00) Bogota, Lima, Quito",
                    "(UTC-05:00) Indiana (East) ",
                    "(UTC-04:30) Caracas",
                    "(UTC-04:00) Atlantic Time (Canada)",
                    "(UTC-04:00) Cuiaba",
                    "(UTC-04:00) Santiago",
                    "(UTC-04:00) Georgetown, La Paz, Manaus, San Juan",
                    "(UTC-04:00) Asuncion",
                    "(UTC-03:30) Newfoundland",
                    "(UTC-03:00) Brasilia",
                    "(UTC-03:00) Greenland",
                    "(UTC-03:00) Montevideo",
                    "(UTC-03:00) Cayenne, Fortaleza",
                    "(UTC-03:00) Buenos Aires",
                    "(UTC-02:00) Mid-Atlantic",
                    "(UTC-02:00) Coordinated Universal Time -02",
                    "(UTC-01:00) Azores",
                    "(UTC-01:00) Cabo Verde Is.",
                    "(UTC-00:00) Dublin, Edinburgh, Lisbon, London",
                    "(UTC-00:00) Monrovia, Reykjavik",
                    "(UTC-00:00) Casablanca",
                    "(UTC-00:00) Coordinated Universal Time",
                    "(UTC+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague",
                    "(UTC+01:00) Sarajevo, Skopje, Warsaw, Zagreb",
                    "(UTC+01:00) Brussels, Copenhagen, Madrid, Paris",
                    "(UTC+01:00) West Central Africa",
                    "(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna",
                    "(UTC+01:00) Windhoek",
                    "(UTC+02:00) Minsk",
                    "(UTC+02:00) Cairo",
                    "(UTC+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius",
                    "(UTC+02:00) Athens, Bucharest",
                    "(UTC+02:00) Jerusalem",
                    "(UTC+02:00) Amman",
                    "(UTC+02:00) Beirut",
                    "(UTC+02:00) Harare, Pretoria",
                    "(UTC+02:00) Damascus",
                    "(UTC+02:00) Istanbul",
                    "(UTC+03:00) Kuwait, Riyadh",
                    "(UTC+03:00) Baghdad",
                    "(UTC+03:00) Nairobi",
                    "(UTC+03:00) Kaliningrad",
                    "(UTC+03:30) Tehran",
                    "(UTC+04:00) Moscow, St. Petersburg, Volgograd",
                    "(UTC+04:00) Abu Dhabi, Muscat",
                    "(UTC+04:00) Baku",
                    "(UTC+04:00) Yerevan",
                    "(UTC+04:00) Tbilisi",
                    "(UTC+04:00) Port Louis",
                    "(UTC+04:30) Kabul",
                    "(UTC+05:00) Tashkent",
                    "(UTC+05:00) Islamabad, Karachi",
                    "(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi",
                    "(UTC+05:30) Sri Jayawardenepura",
                    "(UTC+05:45) Kathmandu",
                    "(UTC+06:00) Ekaterinburg",
                    "(UTC+06:00) Astana",
                    "(UTC+06:00) Dhaka",
                    "(UTC+06:30) Yangon (Rangoon)",
                    "(UTC+07:00) Novosibirsk",
                    "(UTC+07:00) Bangkok, Hanoi, Jakarta",
                    "(UTC+08:00) Krasnoyarsk",
                    "(UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi",
                    "(UTC+08:00) Kuala Lumpur, Singapore",
                    "(UTC+08:00) Taipei",
                    "(UTC+08:00) Perth",
                    "(UTC+08:00) Ulaanbaatar",
                    "(UTC+09:00) Irkutsk",
                    "(UTC+09:00) Seoul",
                    "(UTC+09:00) Osaka, Sapporo, Tokyo",
                    "(UTC+09:30) Darwin",
                    "(UTC+09:30) Adelaide",
                    "(UTC+10:00) Yakutsk",
                    "(UTC+10:00) Canberra, Melbourne, Sydney",
                    "(UTC+10:00) Brisbane",
                    "(UTC+10:00) Hobart",
                    "(UTC+10:00) Guam, Port Moresby",
                    "(UTC+11:00) Vladivostok",
                    "(UTC+11:00) Solomon Is., New Caledonia",
                    "(UTC+12:00) Magadan",
                    "(UTC+12:00) Fiji",
                    "(UTC+12:00) Auckland, Wellington",
                    "(UTC+12:00) Coordinated Universal Time +12",
                    "(UTC+13:00) Nuku alofa"]

        self.combo31 = wx.ComboBox(self.panel, choices=Typelist)
        sizer.Add(self.combo31, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.combo31.Bind(wx.EVT_COMBOBOX, self.OnTimezoneCombo)
        
        self.combo31.SetValue("(UTC+09:00) Seoul")
        
        
        #Target List
        text41 = wx.StaticText(self.panel, label="     Target")
        sizer.Add(text41, pos=(4, 0), flag=wx.LEFT, border=5)
        
        self.List41 = TargetList(self.panel, -1)
        sizer.Add(self.List41, pos=(4, 1), span=(3, 3), flag=wx.EXPAND, border=5)
        

        #Include Artifacts extraction
        text71 = wx.StaticText(self.panel, label="     Option")
        sizer.Add(text71, pos=(7, 0), flag=wx.LEFT, border=5)
        
        self.chk7 = wx.CheckBox(self.panel, label=" Extract main artifacts")
        sizer.Add(self.chk7, pos=(7, 1), span=(1, 1), flag=wx.LEFT|wx.TOP, border=5)
        self.chk7.Bind(wx.EVT_CHECKBOX, self.OnCheckArtifactsExtract)
        
        self.chk8 = wx.CheckBox(self.panel, label=" TimeLine analysis(Create plaso dump file)")
        sizer.Add(self.chk8, pos=(8, 1), span=(1, 5), flag=wx.LEFT|wx.TOP, border=5)
        self.chk8.Bind(wx.EVT_CHECKBOX, self.OnCheckTimeLineAn)
        
        self.chk7.Enable(True)
        self.chk7.SetValue(1)
        self.chk8.Enable(True)
        self.chk8.SetValue(1)
        
        
        #Log listctrl
        text91 = wx.StaticText(self.panel, label="     Progress")
        sizer.Add(text91, pos=(9, 0), flag=wx.LEFT, border=5)
        
        self.List91 = LogList(self.panel, -1)
        sizer.Add(self.List91, pos=(9, 1), span=(4, 3), flag=wx.EXPAND, border=5)
        
        self.List91.InsertColumn(0, 'Progress')
        
        
        
        #Last Button
        self.button130 = wx.Button(self.panel, label='Help')
        sizer.Add(self.button130, pos=(13, 0), flag=wx.LEFT, border=10)
        self.button130.Bind(wx.EVT_BUTTON, self.OnButtonHelp)

        self.button131 = wx.Button(self.panel, label="Ok")
        sizer.Add(self.button131, pos=(13, 1), flag=wx.BOTTOM|wx.RIGHT)
        self.button131.Bind(wx.EVT_BUTTON, self.OnButtonOK)
        
        self.button133 = wx.Button(self.panel, label="Open")
        sizer.Add(self.button133, pos=(13, 2), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=5)
        self.button133.Bind(wx.EVT_BUTTON, self.OnButtonOpen)
        self.button133.Enable(False)

        self.button132 = wx.Button(self.panel, label="Close")
        sizer.Add(self.button132, pos=(13, 3), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=5)
        self.button132.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        #self.button132.Enable(False)
        
        sizer.AddGrowableCol(2)
        self.panel.SetSizer(sizer)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def OnTimezoneCombo(self, event):
        SelectedText = self.combo51.GetValue()
        
        if SelectedText == "cli":
            self.tc61.SetEditable(1)
            self.tc7.SetEditable(1)
            self.button6.Enable()
        else:
            self.tc61.SetEditable(0)
            self.tc7.SetEditable(0)
            self.button6.Disable()
            
            
    def OnCheckArtifactsExtract(self, event):
        isChecked = self.chk7.GetValue()
        
        if isChecked == 1:
            self.chk7.SetValue(1)
            self.chk8.Enable(True)            
            return
        
        else:
            self.chk7.SetValue(0)
            self.chk8.SetValue(0)
            self.chk8.Enable(False)
            return
            
            
    def OnCheckTimeLineAn(self, event):
        isChecked = self.chk8.GetValue()
        
        if isChecked == 1:
            
            return
        else:
            
            return

            
    def OnButtonModulePath(self, event):
        
        dlg = wx.DirDialog(self, message="Select Target File", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath() + "\\PFPCase_" + str(time.time()) + "\\"
        
        
            self.tc2.Clear()
            self.tc2.WriteText(SelectedFile)
                 
        
        return
    
    
    def OnButtonHelp(self, event):
        
        wx.MessageBox("Portable Forensic Platform - TheSOFT\n\nContact : \thttp://thesoft.org/\nblog : \thttp://portable-forensics.blogspot.kr/\n")
        
        return
    
    
    def OnButtonOK(self, event):
         
        """변수 설정"""
        self.List91.InsertStringItem(self.List91.idx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" Set values for case creation")
        self.List91.idx+=1
        
        #For Release
        
        #케이스 이름 입력 확인
        self.CaseName = self.tc1.GetLineText(0)
        #케이스 경로 입력 확인 
        self.OutputPath = self.tc2.GetLineText(0)
        
        
        #For Debug
        #self.CaseName = "Test"
        #self.OutputPath = "Q:\\\\PFPCase_1470037233.74\\"
        #self.CasePath = "Q:\\PFPCase_1470037233.74\\Test"
        #self.logPath = self.OutputPath + "\\" + self.CaseName + "\\Case_Logs.log"
        
        #케이스 타겟 입력 확인
        TargetPaths = []
        for index in range(self.List41.GetItemCount()):
            TargetPaths.append(self.List41.GetItem(index,0).GetText())
            
            
        
        """조건 검사"""
        
        if self.CaseName == "":
            wx.MessageBox("Please insert case name")
            return
        
        if self.OutputPath == "":
            wx.MessageBox("Please insert output path")
            return
        
        if TargetPaths == []:
            wx.MessageBox("Please insert target path")
            return
        
        
        """케이스 경로 생성(FileDlg 설정경로\\케이스이름\\)"""
        
        #Code
        try:
            self.OutputPath = self.OutputPath.replace("\\\\", "\\")
            os.makedirs(self.OutputPath)
            os.makedirs(self.OutputPath + "\\" + self.CaseName)
            os.makedirs(self.OutputPath + "\\" + self.CaseName + "\\Temp")
            #os.makedirs(self.OutputPath + "\\" + self.CaseName + "\\Extract")
            self.CasePath = self.OutputPath + "\\" + self.CaseName
            self.CasePath = self.CasePath.replace("\\\\", "\\")
        except:
            wx.MessageBox("Case folder creation error. Please check case name and output path")
            return
        
        #Log파일 생성
        self.logPath = self.OutputPath + "\\" + self.CaseName + "\\Case_Logs.log"
        fp_log = open(self.logPath, 'w') 
        fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" Create log file for case \"" + self.CaseName + "\"\n")
        fp_log.close()
        
        
        """loaddb 구동 및 결과물 생성"""
        
        #Code
        self.List91.InsertStringItem(self.List91.idx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" Target analysis is begun")
        #self.List91.SetStringItem(self.idx, 0, "[.........]")
        self.List91.idx+=1
        
        
        self.button131.Enable(False)
        self.button2.Enable(False)
        self.button133.Enable(True)
        
        
        threads = []
        th = threading.Thread(target=self.ThreadProcessing, args=())
        th.start()
        threads.append(th)
        
    
    def ThreadProcessing(self):
        
        #볼륨으로 지정한 것들은 스레드 돌려버령
        for index in range(self.List41.GetItemCount()):
            if "Mnt" not in self.List41.GetItem(index,0).GetText().strip():
                TargetPath = self.List41.GetItem(index,1).GetText().strip()
                isImage = "False"
                threads = []
                th = threading.Thread(target=self.ThreadLoadDB, args=(TargetPath, None, isImage, index))
                th.start()
                threads.append(th)
                
                wx.Sleep(4.0)
                
                
        #마운트 된 것들은 안정성을 위해 순차 진행하고..
        for index in range(self.List41.GetItemCount()):
            if "Mnt" in self.List41.GetItem(index,0).GetText().strip():
                isImage = "True"
                TargetPath = self.List41.GetItem(index,1).GetText().strip()
                #수행 및 종료
                
                #fp_log = open(self.logPath, 'a') 
                #fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" Target, " + TargetPath + ", analysis is begun" + "\n")
                #fp_log.close()
                self.ThreadLoadDB(TargetPath, None, isImage, index)
                
                #while th.is_alive() == True:
                #    wx.Sleep(0.1)
            
        return
        
        
        return
    
    
    def ThreadLoadDB(self, TargetPath, Dummy, isImage, index):
            
        """loaddb 결과물 생성"""
        
        t = time.time()
        path = os.path.abspath(".")
        pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\pfp_sdk\\bin\\tsk_bin\\loaddb.bat")
        if isImage == "True": 
            DBPath = self.CasePath + "\\(img)" + TargetPath.replace("~", "_").replace(":", "~") + "~_pfp_load_result_"+str(t)+".casedb"
        else:
            DBPath = self.CasePath + "\\" + TargetPath.replace("\\", "_").replace(":", "") + "_pfp_load_result_"+str(t)+".casedb"
        
        #print pathchange
        #print TargetPath
        #print DBPath
        
        #For Relase
        Process = None
        if isImage == "True": 
            Process = Popen([pathchange.decode('cp949'), "\\\\.\\"+self.List41.GetItem(index,0).GetText().split(" ")[2].decode('cp949'), DBPath.decode('cp949')], shell=True)
        else: 
            Process = Popen([pathchange.decode('cp949'), TargetPath.decode('cp949'), DBPath.decode('cp949')], shell=True)
        #For Debug
        #Process = Popen(["copy", "C:\\Users\\JSJ\\Desktop\\PFPCase_1469195954.19\\ExtractTest\\__._C_pfp_load_result_1469195970.37.casedb", DBPath.decode('cp949')], shell=True)
        #elif 'Q' in TargetPath : Process = Popen(["copy", "C:\\Users\\JSJ\\Desktop\\PFPCase_1469195954.19\\ExtractTest\\__._Q_pfp_load_result_1469195971.38.casedb", DBPath.decode('cp949')], shell=True)
        
        max = 0
        LogIdx = self.List91.idx
        self.List91.idx+=1
        self.List91.InsertStringItem(LogIdx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Target analysis, progressing..  []")
        while Process.poll() is None: 
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Target analysis, progressing..  ["
            for idx in range(0, max):
                LogKeyword += "."
            LogKeyword += "]"
            
            time.sleep(0.5)
            
            self.List91.SetStringItem(LogIdx, 0, LogKeyword)
            max += 1
            if max == 10:
                max = 0
        
        LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Target analysis, Complete"
        self.List91.SetStringItem(LogIdx, 0, LogKeyword)
        
        fp_log = open(self.logPath, 'a') 
        fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Target analysis, Complete" + "\n")
        fp_log.close()
        
        
        
        """pfp-list와 연동"""
        self.List91.InsertStringItem(self.List91.idx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create volume PFP-list..")
        #self.List91.SetStringItem(self.idx, 0, "[.........]")
        self.List91.idx+=1
        
        threads = []
        th = threading.Thread(target=self.ThreadSetCasePFPList, args=(TargetPath, DBPath, isImage, index))
        th.start()
        threads.append(th)
        
        max = 0
        LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create volume PFP-list, progressing..[]"
        LogIdx = self.List91.idx
        self.List91.idx+=1
        self.List91.InsertStringItem(LogIdx, LogKeyword)
        while th.is_alive() == True: 
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create volume PFP-list, progressing..  ["
            for idx in range(0, max):
                LogKeyword += "."
            LogKeyword += "]"
            
            time.sleep(0.5)
            
            self.List91.SetStringItem(LogIdx, 0, LogKeyword)
            max += 1
            if max == 10:
                max = 0
        
        LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create volume PFP-list, Complete"
        self.List91.SetStringItem(LogIdx, 0, LogKeyword)
        
        fp_log = open(self.logPath, 'a') 
        fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create volume PFP-list, Complete" + "\n")
        fp_log.close()
            
            
            
        """자동 추출"""
        
        isChecked = self.chk7.GetValue()
        if isChecked == 1:
            
            self.List91.InsertStringItem(self.List91.idx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Extract main artifact..")
            #self.List91.SetStringItem(self.idx, 0, "[.........]")
            self.List91.idx+=1
            
            threads = []
            th = threading.Thread(target=self.ThreadAutoExtract, args=(TargetPath, DBPath, isImage, index))
            th.start()
            threads.append(th)
            
            max = 0
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Extract main artifact, progressing..[]"
            LogIdx = self.List91.idx
            self.List91.idx+=1
            self.List91.InsertStringItem(LogIdx, LogKeyword)
            while th.is_alive() == True: 
                LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Extract main artifact, progressing..  ["
                for idx in range(0, max):
                    LogKeyword += "."
                LogKeyword += "]"
                
                time.sleep(0.5)
                
                self.List91.SetStringItem(LogIdx, 0, LogKeyword)
                max += 1
                if max == 10:
                    max = 0
            
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Extract main artifact, Complete"
            self.List91.SetStringItem(LogIdx, 0, LogKeyword)
            
            fp_log = open(self.logPath, 'a') 
            fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Extract main artifact, Complete" + "\n")
            fp_log.close()
        
        
        
        """타임라인 Dump 생성(아티팩트가 추출되어야만 체크할 수 있도록 설정해 두었음)"""
        isChecked = self.chk7.GetValue()
        if isChecked == 1:
            self.List91.InsertStringItem(self.List91.idx, strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create timeline(plaso dump file)..")
            #self.List91.SetStringItem(self.idx, 0, "[.........]")
            self.List91.idx+=1
            
            threads = []
            th = threading.Thread(target=self.ThreadCreateTimeLine, args=(TargetPath, DBPath, isImage, index))
            th.start()
            threads.append(th)
            
            max = 0
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create timeline(plaso dump file), progressing..[]"
            LogIdx = self.List91.idx
            self.List91.idx+=1
            self.List91.InsertStringItem(LogIdx, LogKeyword)
            while th.is_alive() == True: 
                LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create timeline(plaso dump file), progressing..  ["
                for idx in range(0, max):
                    LogKeyword += "."
                LogKeyword += "]"
                
                time.sleep(0.5)
                
                self.List91.SetStringItem(LogIdx, 0, LogKeyword)
                max += 1
                if max == 10:
                    max = 0
            
            LogKeyword = strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create timeline(plaso dump file), Complete"
            self.List91.SetStringItem(LogIdx, 0, LogKeyword)
            
            fp_log = open(self.logPath, 'a') 
            fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time()))+" ("+TargetPath+") Create timeline(plaso dump file), Complete" + "\n")
            fp_log.close()
        
            
        #wx.MessageBox(TargetPath + " : Volume's case data create process is done.\nCase Path : " + self.CasePath)
        #os.system("explorer " + self.CasePath)
        #self.button132.Enable(True)
        #self.Close()
        
    
    
    def ThreadSetCasePFPList(self, TargetPath, TskResultDBPath, isImage, index):
    
        CasePFPListPath = self.CasePath + "\\CaseData"
        if not os.path.isdir(CasePFPListPath) : os.makedirs(CasePFPListPath)
        CaseVolumePath = ""
        if isImage == "True":
            CaseImagePath = CasePFPListPath + "\\" + TargetPath.split(":")[0]
            if not os.path.isdir(CaseImagePath) : os.makedirs(CaseImagePath)
            ImagePathFile = CaseImagePath + "\\ImagePath.txt"
            fp = open(ImagePathFile, "w")
            fp.write(self.List41.GetItem(index,2).GetText())
            fp.close()
            CaseVolumePath = CaseImagePath + "\\" + TargetPath.split(":")[1]
        else:
            CaseVolumePath = CasePFPListPath + "\\" + TargetPath.replace("\\", "").replace(":", "").replace(".", "")
        CaseExtractPath = CaseVolumePath + "\\Extract"
        if not os.path.isdir(CaseVolumePath) : os.makedirs(CaseVolumePath)
        if not os.path.isdir(CaseExtractPath) : os.makedirs(CaseExtractPath)
        abspath = os.path.abspath(".")
        
        fisrt_pfplist = os.path.join(abspath, "PFPModule\\PFPLib\\PublicPFPList\\public.1.First_Response.pfplist.sqlite")
        copied_fisrt_pfplist = CaseVolumePath + "\\" + "public.1.First_Response.pfplist.sqlite"
        artifact_pfplist = os.path.join(abspath, "PFPModule\\PFPLib\\PublicPFPList\\public.2.Artifact_Analysis.pfplist.sqlite")
        copied_artifact_pfplist = CaseVolumePath + "\\" + "public.2.Artifact_Analysis.pfplist.sqlite"
        user_pfplist = os.path.join(abspath, "UserModule\\UserDefine.pfplist.sqlite")
        copied_user_pfplist = CaseVolumePath + "\\" + "UserDefine.pfplist.sqlite"
        
        Process = Popen(["copy", fisrt_pfplist.decode('cp949'), copied_fisrt_pfplist.decode('cp949')], shell=True)
        while Process.poll() is None:   time.sleep(0.5)
        Process = Popen(["copy", artifact_pfplist.decode('cp949'), copied_artifact_pfplist.decode('cp949')], shell=True)
        while Process.poll() is None:   time.sleep(0.5)
        Process = Popen(["copy", user_pfplist.decode('cp949'), copied_user_pfplist.decode('cp949')], shell=True)
        while Process.poll() is None:   time.sleep(0.5)
        #os.system("copy \"" + self.PublicPFPListOriginalFilePath.replace("/","\\") + "\" " + self.PublicPFPListFilePath.replace("/","\\") )
        
        """이미지와 관련있는 컨텐츠만 남기기!!"""
        #Code
        CaseDBs = [CaseVolumePath + "\\" + "public.1.First_Response.pfplist.sqlite",
                   CaseVolumePath + "\\" + "public.2.Artifact_Analysis.pfplist.sqlite",
                   CaseVolumePath + "\\" + "UserDefine.pfplist.sqlite"]    #업데이트 대상 
        
        self.CaseDBPath = TskResultDBPath
        tsk_db_con = sqlite3.connect( self.CaseDBPath )
        tsk_db_cursor = tsk_db_con.cursor()
        
        for CaseDB in CaseDBs:
            
            #print CaseDB
            casedb_con = sqlite3.connect( CaseDB.decode('cp949') )
            casedb_cursor = casedb_con.cursor()
            
            SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable"
            
            casedb_cursor.execute( SelectQuery )
            SelectedRows = casedb_cursor.fetchall()
            
            for Row in SelectedRows:
            
                InsertString = ""
                try:
                    UtilClass = Util()
                    InsertString = UtilClass.DummyCyber(self.DecodedDummy, "", Row[0])
                except:
                    InsertString = Row[0]
                
                #print InsertString
                if '[*]' in InsertString or '[+]' in InsertString or '[-]' in InsertString or '[RegKey]' in InsertString:
                    #print "!!!!!!!!!!!!!!!"
                    UpdateQuery = "Update VesLocationTable set Registrant = 'Case_Data' where ContentsID = '" + Row[1] + "'"
                    casedb_cursor.execute(UpdateQuery)
                    casedb_con.commit()
                    
                else:
                    """
                    [케이스 db 이용 작업 남은 todo..]
                    - 분석 경로 정확히 입력하는것 했음 (%UserProfile%\Sample은 Users\샬라\샬라\샬라\샬라\Sample인 경우도 인식을 하는데.. 이거 방지는?)
                    - *.evt 할때 대소문자 구분 없이 되도록 수정 필요 / Usanjrnl 확인 못하네~
                    - 추출(단순 추출시 db에서 inode 가져오도록, 재귀 추출)
                    """
                    #if "*." in os.path.split(InsertString)[1]:
                    #    InsertString = os.path.split(InsertString)[0]
                    if InsertString[len(InsertString)-1] == "\\":
                        InsertString = InsertString[0:len(InsertString)-1]
                    
                    replacedString = InsertString.replace("\\", "/")
                    if str(type(replacedString)) == "<type 'unicode'>":
                        replacedString = replacedString.encode('utf8')
                    if ':' == replacedString[1]:
                        #replacedString = replacedString.split(":")[1]
                        replacedString = replacedString[2:]
                    #if "UserDefine.pfplist.sqlite" in CaseDB: 
                    #print replacedString
                    #print str([replacedString])
                    #print str(type(replacedString))
                    replacedString_A = replacedString
                    replacedString_B = replacedString
                    if "%systemdrive%" in replacedString.lower():     
                        replacedString_A = replacedString.lower().replace("%systemdrive%", "")
                        replacedString_B = replacedString.lower().replace("%systemdrive%", "")
                    if "%systemroot%" in replacedString.lower():     
                        replacedString_A = replacedString.lower().replace("%systemroot%", "/windows")
                        replacedString_B = replacedString.lower().replace("%systemroot%", "/windows")
                    if "%windir%" in replacedString.lower():     
                        replacedString_A = replacedString.lower().replace("%windir%", "/windows")
                        replacedString_B = replacedString.lower().replace("%windir%", "/windows")
                    if "%programdata%" in replacedString.lower():     
                        replacedString_A = replacedString.lower().replace("%programdata%", "/programdata")
                        replacedString_B = replacedString.lower().replace("%programdata%", "/programdata")
                    if "%userprofile%" in replacedString.lower():     
                        replacedString_A = replacedString.lower().replace("%userprofile%", "/users/%")
                        replacedString_B = replacedString.lower().replace("%userprofile%", "/documents and settings/%")
                    
                    try:
                        ParentPath_A = os.path.split(replacedString_A)[0]
                        TargetName_A = os.path.split(replacedString_A)[1].replace("*", "%")
                        #print "replacedString = " + replacedString
                        #print "replacedString_A = " + replacedString_A
                        #print "ParentPath_A = " + ParentPath_A
                        if ParentPath_A[len(ParentPath_A)-1] != "/":
                            ParentPath_A = ParentPath_A + "/"
                            
                        ParentPath_B = os.path.split(replacedString_B)[0]
                        TargetName_B = os.path.split(replacedString_B)[1].replace("*", "%")
                        if ParentPath_B[len(ParentPath_B)-1] != "/":
                            ParentPath_B = ParentPath_B + "/"
                        
                        
                        """쿼리의 구성을 Rawhandler에 있는 것처럼 정확하게 가져올 수 있도록 구성"""
                        SelectQuery_A = "select parent_path, name from tsk_files where parent_path like '" + ParentPath_A + "' and name like '" + TargetName_A + "' COLLATE NOCASE;"
                        SelectQuery_B = "select parent_path, name from tsk_files where parent_path like '" + ParentPath_B + "' and name like '" + TargetName_B + "' COLLATE NOCASE;"
                
                        #print SelectQuery
                        tsk_db_cursor.execute( SelectQuery_A )
                        SelectedRows_A = tsk_db_cursor.fetchall()
                        
                        tsk_db_cursor.execute( SelectQuery_B )
                        SelectedRows_B = tsk_db_cursor.fetchall()
                        
                        #print "len(SelectedRows) = " + str(len(SelectedRows))
                        if len(SelectedRows_A) + len(SelectedRows_B) > 0:
                            UpdateQuery = "Update VesLocationTable set Registrant = 'Case_Data' where ContentsID = '" + Row[1] + "'"
                            casedb_cursor.execute(UpdateQuery)
                            casedb_con.commit()
                            
                    except:
                        print "exception error(in ThreadSetCasePFPList) : " + replacedString
                        continue
                    
            casedb_con.close()
        tsk_db_con.close()
    
    
    
    
    
    
    
    
    def ThreadAutoExtract(self, TargetPath, TskResultDBPath, isImage, index):
        SelectedModuleList = []
        

        CasePFPListPath = self.CasePath + "\\CaseData"
        if not os.path.isdir(CasePFPListPath) : os.makedirs(CasePFPListPath)
        CaseVolumePath = ""
        if isImage == "True":
            CaseImagePath = CasePFPListPath + "\\" + TargetPath.split(":")[0]
            if not os.path.isdir(CaseImagePath) : os.makedirs(CaseImagePath)
            ImagePathFile = CaseImagePath + "\\ImagePath.txt"
            fp = open(ImagePathFile, "w")
            fp.write(self.List41.GetItem(index,2).GetText())
            fp.close()
            CaseVolumePath = CaseImagePath + "\\" + TargetPath.split(":")[1]
        else:
            CaseVolumePath = CasePFPListPath + "\\" + TargetPath.replace("\\", "").replace(":", "").replace(".", "")
        CaseExtractPath = CaseVolumePath + "\\Extract"
        if not os.path.isdir(CaseVolumePath) : os.makedirs(CaseVolumePath)
        if not os.path.isdir(CaseExtractPath) : os.makedirs(CaseExtractPath)
        
        
        
        #우선 FirstResponse, UserDefine PFP-List에서 AnPointID가 100040이며, Registrant가 Case_Data이고 [-]/[+]/[*]를 포함하지 않은 것의 목록을 가져온다. 
        #Select Text, ContentsID from VesLocationTable where AnPointID=100040 and Registrant='Case_Data'
        SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable where AnPointID = '100040' and Registrant = 'Case_Data' order by cast(Sequence as decimal)"
        
        temp_listdb_con = sqlite3.connect( os.path.join(CaseVolumePath, "public.1.First_Response.pfplist.sqlite") )
        temp_listdb_cursor = temp_listdb_con.cursor()
        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        temp_listdb_con.close()
        
        temp_listdb_con = sqlite3.connect( os.path.join(CaseVolumePath, "UserDefine.pfplist.sqlite") )
        temp_listdb_cursor = temp_listdb_con.cursor()
        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        temp_listdb_con.close()
        
        #print "UserResultRows = " + str(UserResultRows)

        ResultRows = []        
        for UserRow in UserResultRows:
            if "(.. delete..)" not in UserRow[0]: ResultRows.append(UserRow)
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]: ResultRows.append(PublicRow)
        """
        for UserRow in UserResultRows:
            if  "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:              ResultRows.append(UserRow)
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:                                     ResultRows.append(PublicRow)
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:    ResultRows.append(UserRow)
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:            ResultRows.append(UserRow)
        """
        for Row in ResultRows:
            """행 삽입"""
            InsertString = ""
            try:
                UtilClass = Util()
                InsertString = UtilClass.DummyCyber(self.DecodedDummy, "", Row[0])
            except:
                InsertString = Row[0]
        
            if "[*]" not in InsertString and "[+]" not in InsertString and "[-]" not in InsertString: 
                SelectedModuleList.append(InsertString)
        
        
        
        
        
        #SetPath 함수를 복사하여 txt 파일을 만든다. 
        #파일 목록의 임시 파일 생성 및 추출 모듈 구동
        TempFileName = os.path.join(CaseVolumePath, "extract_list.dat")
        fp = open(TempFileName, 'w')
        AnTargetRoot = ""
        if isImage == "True":   AnTargetRoot = self.List41.GetItem(index,0).GetText().split(" ")[2]
        else:                   AnTargetRoot = TargetPath.replace("\\", "").replace(":", "").replace(".", "") + ":" 
        for Item in SelectedModuleList:        
            Keyword = Item
            RetList = self.SetPath(Keyword + "\t None", AnTargetRoot)
            
            #Make abs paths from env variable
            for Keyword in RetList: fp.write(Keyword + "\n")
        fp.close()
        
        
        
        
        
        
        #PFPExtractor를 호출한다. (이때 여기서 호출되는 PFP-Extractor는 자동으로 Start 버튼이 눌리도록 한다.
        Process = Popen(["./Utility/Portable Python 2.7.3.2/App/pythonw.exe", ".\PFPModule\PFPLib\PFPExtractor.pyc", TempFileName, TskResultDBPath, isImage])
        while Process.poll() is None: 
            time.sleep(0.5)


        
        return
    
    
    
    
    
    def ThreadCreateTimeLine(self, TargetPath, TskResultDBPath, isImage, index):
        
        CasePFPListPath = self.CasePath + "\\CaseData"
        if not os.path.isdir(CasePFPListPath) : os.makedirs(CasePFPListPath)
        CaseVolumePath = ""
        if isImage == "True":
            CaseImagePath = CasePFPListPath + "\\" + TargetPath.split(":")[0]
            if not os.path.isdir(CaseImagePath) : os.makedirs(CaseImagePath)
            ImagePathFile = CaseImagePath + "\\ImagePath.txt"
            fp = open(ImagePathFile, "w")
            fp.write(self.List41.GetItem(index,2).GetText())
            fp.close()
            CaseVolumePath = CaseImagePath + "\\" + TargetPath.split(":")[1]
        else:
            CaseVolumePath = CasePFPListPath + "\\" + TargetPath.replace("\\", "").replace(":", "").replace(".", "")
        CaseExtractPath = CaseVolumePath + "\\Extract"
        if not os.path.isdir(CaseVolumePath) : os.makedirs(CaseVolumePath)
        if not os.path.isdir(CaseExtractPath) : os.makedirs(CaseExtractPath)
        
        
        
        ExtractRoot = CaseExtractPath
        TargetPath.replace("\\", "").replace(":", "").replace(".", "")
        #아래의 예시 => C:\Users\JSJ\Desktop\PFPCase_1470015290.97\Test\CaseData\C\Extract\C
        Extracted_Data_Root = ""
        if isImage == "True":   Extracted_Data_Root = os.path.join(ExtractRoot, self.List41.GetItem(index,0).GetText().split(" ")[2].replace(":", ""))
        else:                   Extracted_Data_Root = os.path.join(ExtractRoot, TargetPath.replace("\\", "").replace(":", "").replace(".", ""))
        #아래의 예시 => C:\Users\JSJ\Desktop\PFPCase_1470015290.97\Test\CaseData\C\TimeLine_Result.dump
        ResultDumpFilePath = os.path.join(CaseVolumePath, "TimeLine_Result.dump")
        
        print ["./plaso/log2timeline.exe -z Asia/Seoul --workers 5", ResultDumpFilePath, Extracted_Data_Root]
        Process = Popen(["./PFPModule/PFPLib/InternalModules/plaso/log2timeline.exe", "-z", "Asia/Seoul", "--workers", "5", ResultDumpFilePath, Extracted_Data_Root])
        while Process.poll() is None: 
            time.sleep(0.5)
        
        return
    
    
    
    
    
    
    
    def SetPath(self, Keyword, AnTargetRoot):
        
        retKeyword = []
        
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
    
    
    def OnButtonOpen(self, event):
        
        os.system("explorer " + self.CasePath)
        
        return
    
    def OnClose(self, event):
        dialog = wx.MessageDialog(self, message = "Just close case create dialog, ok?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
        response = dialog.ShowModal()
        
        if (response == wx.ID_YES):
            self.Cancel = True
            self.Destroy()
    
    
    def OnButtonCancel(self, event):
        
        if not os.path.isfile("PFPModule\\PFPLib\\InternalModules\\MIP\\MIP.exe"):
            dialog = wx.MessageDialog(self, message = "Just close case create dialog, ok?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
            response = dialog.ShowModal()
            
            if (response == wx.ID_YES):
                self.Cancel = True
                self.Destroy()
        
        else:
            dialog = wx.MessageDialog(self, message = "Are you sure you want to unmounting all images and quit?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
            response = dialog.ShowModal()
            
            if (response == wx.ID_YES):
                self.Cancel = True
                
                
                ResultLines = []
                path = os.path.abspath(".")
                
                
                if sys.argv[1] == "True":   #is managing on == true 일 경우 
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
                else:
                    AA = 1
                    """OSF 는 참 고려할 것이 많음.. 
                    DrvLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                                  "r", "s", "t", "u", "v", "w", "x", "y", "z"]
                    for DrvLetter in DrvLetters:
                        pathchange = os.path.join(path, "PFPModule\\PFPLib\\InternalModules\\OSFMount(x64)\\OSFMount.com")
                        cmdARGS = [pathchange.decode('cp949'), "-d", "-m", DrvLetter + ":"]
                        
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
                    """
                
            
            
            
            self.Destroy()
        
        return
    
    
    def LogWrite(self, LogMsg):
        
        fp_log = open(self.logPath, 'a') 
        fp_log.write(strftime("[%Y/%m/%d %H:%M:%S]", time.localtime(time.time())) + LogMsg + "\n")
        fp_log.close()
        
        return


def main():
    
    app = wx.App()
    #frame = PFPGui.Show()
    CaseCreateDlg(None, 'PFP - New Case')
    app.MainLoop()

if __name__ == '__main__':
    main() 

    