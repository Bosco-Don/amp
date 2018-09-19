#!/usr/bin/python
# -*- coding: utf-8 -*-

from InternalModules.pfp_sdk.PFPUtil import *
from CategoryAddDlg import *

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




class CheckList(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
        #set image
        images = ['PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/download_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Unit_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/Commercial_16_16.png', 
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/EmptyModule_16_16.png']
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.ExecuteStatus = "AllModule"
        self.parent = parent



class CategorySetting(wx.Dialog):
    

    def __init__(self, parent, title, isManaged = False):    
        wx.Dialog.__init__(self, parent, title=title, size=(900, 850))

        self.isManaged = isManaged
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
      
        self.panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(9, 9)

        #---Main Text
        text1 = wx.StaticText(self.panel, label="  Category")
        sizer.Add(text1, pos=(0, 0), flag=wx.EXPAND, border=50)

        #---Logo
        icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/SelfTest.png'))
        sizer.Add(icon, pos=(0, 14), flag=wx.EXPAND, border=5)

        line = wx.StaticLine(self.panel)
        sizer.Add(line, pos=(1, 0), span=(1, 15), flag=wx.EXPAND|wx.BOTTOM, border=5)

        #---Category Combo
        text2 = wx.StaticText(self.panel, label="  Category")
        sizer.Add(text2, pos=(2, 0), flag=wx.EXPAND, border=5)
        
        
        self.DBPath = ""
        
        if self.isManaged == True:
            self.DBPath = self.default_modulelistDB_path
        else:
            self.DBPath = self.default_user_modulelistDB_path
        
        #insert all Category into Combobox
        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select CategoryName, Description from ModuleCategory order by CategoryName COLLATE NOCASE;"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        con.close()
        
        self.Typelist = []
        
        for row in ResultList:
            self.Typelist.append(row[0])
        
        self.combo21 = wx.ComboBox(self.panel, choices=self.Typelist)
        sizer.Add(self.combo21, pos=(2, 1), span=(1, 12), flag=wx.EXPAND, border=5)
        
        self.combo21.Bind(wx.EVT_COMBOBOX, self.OnComboSelect)
        
        #---Combo Add Button
        self.button2 = wx.Button(self.panel, label="Add", size = wx.Size(40,30))
        sizer.Add(self.button2, pos=(2, 13), flag=wx.EXPAND, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonAddCategory)
        
        #---Combo Delete Button
        self.button2 = wx.Button(self.panel, label="Del", size = wx.Size(40,30))
        sizer.Add(self.button2, pos=(2, 14), flag=wx.EXPAND, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonDelCategory)
        
        #---Description
        text3 = wx.StaticText(self.panel, label="  Description")
        sizer.Add(text3, pos=(3, 0), flag=wx.EXPAND, border=5)
        
        self.text31 = wx.StaticText(self.panel, label="description of selected category")
        sizer.Add(self.text31, pos=(3, 1), flag=wx.EXPAND, border=5)
        
        #---Twin ListCtrl
        self.List41 = CheckList(self.panel, -1)
        sizer.Add(self.List41, pos=(4, 0), span=(10, 15), flag=wx.EXPAND, border=5)
        
        #insert all module into right list
        
        #SelectQuery = "select ModuleName, Author, Description, ContentsID from ModuleList where (OS = 'win' or OS = 'python') and isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        SelectQuery = "select ModuleName, Author, Description, ContentsID from ModuleList where isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[2] = "[UD]" + lst[2]
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        self.List41.InsertColumn(0, 'Module Name')
        self.List41.InsertColumn(1, 'Author')
        self.List41.InsertColumn(2, 'Description')
        self.List41.InsertColumn(3, 'ContentsID')
        
        size = self.List41.GetSize()
        
        self.List41.SetColumnWidth(0, 130)
        self.List41.SetColumnWidth(1, 80)
        self.List41.SetColumnWidth(2, size.x-5)
        self.List41.SetColumnWidth(3, 0)
        
        idx = 0
        for row in MergedResultList:
            
            UtilClass = Util()
        
            try:
                Author = UtilClass.DummyCyber(self.DecodedDummy, "", row[1])
            except:
                Author = UserResultList[1]
                
            try:
                if "[UD]" in row[2]:
                    Description = "[UD]" + UtilClass.DummyCyber(self.DecodedDummy, "", row[2].replace("[UD]", ""))
                else:
                    Description = UtilClass.DummyCyber(self.DecodedDummy, "", row[2])
            except:
                Description = row[2]
            
            self.List41.InsertStringItem(idx, row[0])
            self.List41.SetStringItem(idx, 1, Author)
            self.List41.SetStringItem(idx, 2, Description)
            self.List41.SetStringItem(idx, 3, str(row[3]))
            
            if "[UD]" in row[2]:
                self.List41.SetItemBackgroundColour(idx, '#e6f1f5')
                
            idx += 1 
        
        #---Button +
        self.button41 = wx.Button(self.panel, label="+", size = wx.Size(30,30))
        sizer.Add(self.button41, pos=(14, 0), span=(1, 2), flag=wx.ALIGN_RIGHT, border=5)
        self.button41.Bind(wx.EVT_BUTTON, self.OnButtonAddModule)
        
        #---Button -
        self.button42 = wx.Button(self.panel, label="-", size = wx.Size(30,30))
        sizer.Add(self.button42, pos=(14, 2), span=(1, 2), flag=wx.ALIGN_LEFT, border=5)
        self.button42.Bind(wx.EVT_BUTTON, self.OnButtonRemoveModule)
        
        self.List42 = CheckList(self.panel, -1)
        sizer.Add(self.List42, pos=(15, 0), span=(10, 15), flag=wx.EXPAND, border=5)
        
        self.List42.InsertColumn(0, 'Module Name')
        self.List42.InsertColumn(1, 'Author')
        self.List42.InsertColumn(2, 'Description')
        self.List42.InsertColumn(3, 'ContentsID')
        
        size = self.List42.GetSize()
        
        self.List42.SetColumnWidth(0, 130)
        self.List42.SetColumnWidth(1, 80)
        self.List42.SetColumnWidth(2, size.x-5)
        self.List42.SetColumnWidth(3, 0)
              
        #---Last Buttons
        
        self.button91 = wx.Button(self.panel, label="Apply", size = wx.Size(70,30))
        sizer.Add(self.button91, pos=(26, 0), span=(1, 2), flag=wx.ALIGN_RIGHT)
        self.button91.Bind(wx.EVT_BUTTON, self.OnButtonOK)

        self.button92 = wx.Button(self.panel, label="Close", size = wx.Size(70,30))
        sizer.Add(self.button92, pos=(26, 2), span=(1, 2), flag=wx.ALIGN_LEFT)
        self.button92.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        
        sizer.AddGrowableCol(2)
        
        self.panel.SetSizer(sizer)
        
    def OnComboSelect(self, event):
        
        UtilClass = Util()
        
        #old selected category apply
        ModuleIDs = ""
        
        for index in range(self.List42.GetItemCount()):
            ModuleIDs += self.List42.GetItem(index,3).GetText()
            ModuleIDs += ","
        
        ModuleIDs = UtilClass.DummyCyber(self.DecodedDummy, ModuleIDs, "")
        
        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        UpdateQuery = "update ModuleCategory set ModuleIDs = '" + ModuleIDs + "' where CategoryName = '" + self.OldSelectedText + "'"
        cursor.execute( UpdateQuery )
        con.commit()
        
        con.close()
        
        
        #view new selected category
        SelectedText = self.combo21.GetValue()
        self.OldSelectedText = SelectedText
        
        
        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select ModuleIDs from ModuleCategory where CategoryName = '" + SelectedText + "';"
        
        cursor.execute( SelectQuery )
        ModuleIDs = cursor.fetchone()
        
        
        
        try:
            ModuleIDs = UtilClass.DummyCyber(self.DecodedDummy, "", ModuleIDs[0])
        except:
            ModuleIDs = ModuleIDs[0]
        
        Tokens = ModuleIDs.split(",")
        
        #print str(ModuleIDs).strip('u()\'')
        #print Tokens
        
        #print Tokens
        #print len(Tokens)
        
        #---Upper list initialization
        #SelectQuery = "select ModuleName, Author, Description, ContentsID from ModuleList where (OS = 'win' or OS = 'python') and isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        SelectQuery = "select ModuleName, Author, Description, ContentsID from ModuleList where isDeleted = '0' order by ModuleName COLLATE NOCASE;"
        
        #Get From User DB
        ##############
        con = sqlite3.connect( self.default_user_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        UserResultList = cursor.fetchall()
        
        idx = 0
        for row in UserResultList:
            lst = list(row)
            lst[2] = "[UD]" + lst[2]
            UserResultList[idx] = tuple(lst) 
            idx += 1
        
        con.close()
        
        #Get From Public DB
        ################
        con = sqlite3.connect( self.default_modulelistDB_path )
        cursor = con.cursor()
        
        cursor.execute( SelectQuery )
        PublicResultList = cursor.fetchall()
        
        con.close()
        
        #Merge and sort
        ###############
        MergedResultList = UserResultList + PublicResultList
        MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
        
        self.List41.DeleteAllItems()
        
        idx = 0
        for row in MergedResultList:
            
            try:
                Author = UtilClass.DummyCyber(self.DecodedDummy, "", row[1])
            except:
                Author = UserResultList[1]
                
            try:
                if "[UD]" in row[2]:
                    Description = "[UD]" + UtilClass.DummyCyber(self.DecodedDummy, "", row[2].replace("[UD]", ""))
                else:
                    Description = UtilClass.DummyCyber(self.DecodedDummy, "", row[2])
            except:
                Description = row[2]
            
            self.List41.InsertStringItem(idx, row[0])
            self.List41.SetStringItem(idx, 1, Author)
            self.List41.SetStringItem(idx, 2, Description)
            self.List41.SetStringItem(idx, 3, str(row[3]))
            
            if "[UD]" in row[2]:
                self.List41.SetItemBackgroundColour(idx, '#e6f1f5')
            
            idx += 1 
        
        #---Lower list initialization
        if len(Tokens) <= 2:
            self.List42.DeleteAllItems()
               
        else :
            SelectQuery = "select ModuleName, Author, Description, ContentsID from ModuleList where"
            
            for ModuleID in Tokens:
                try:
                    float(ModuleID)
                    SelectQuery += " or ContentsID = "
                    SelectQuery += ModuleID
                
                except ValueError:
                    continue
                
                
            SelectQuery = SelectQuery.replace("where or", "where")
            
            SelectQuery += " order by ModuleName COLLATE NOCASE"
            
            
            #Get From User DB
            ##############
            con = sqlite3.connect( self.default_user_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            UserResultList = cursor.fetchall()
            
            idx = 0
            for row in UserResultList:
                lst = list(row)
                lst[2] = "[UD]" + lst[2]
                UserResultList[idx] = tuple(lst) 
                idx += 1
            
            con.close()
            
            #Get From Public DB
            ################
            con = sqlite3.connect( self.default_modulelistDB_path )
            cursor = con.cursor()
            
            cursor.execute( SelectQuery )
            PublicResultList = cursor.fetchall()
            
            con.close()
            
            #Merge and sort
            ###############
            MergedResultList = UserResultList + PublicResultList
            MergedResultList.sort(key=lambda t : tuple(t[0].lower()))
            
            
            
            
            self.List42.DeleteAllItems()
            
            self.SelectedListid = 0
            for row in MergedResultList:
                
                UtilClass = Util()
        
                try:
                    Author = UtilClass.DummyCyber(self.DecodedDummy, "", row[1])
                except:
                    Author = UserResultList[1]
                    
                try:
                    if "[UD]" in row[2]:
                        Description = "[UD]" + UtilClass.DummyCyber(self.DecodedDummy, "", row[2].replace("[UD]", ""))
                    else:
                        Description = UtilClass.DummyCyber(self.DecodedDummy, "", row[2])
                except:
                    Description = row[2]
                    
                
                self.List42.InsertStringItem(self.SelectedListid, row[0])
                self.List42.SetStringItem(self.SelectedListid, 1, Author)
                self.List42.SetStringItem(self.SelectedListid, 2, Description)
                self.List42.SetStringItem(self.SelectedListid, 3, str(row[3]))
                
                if "[UD]" in row[2]:
                    self.List42.SetItemBackgroundColour(self.SelectedListid, '#e6f1f5')
                
                self.SelectedListid += 1 
            
            con.close()
        
        #Get ModuleID in the Selected category and insert list into List42 (self.SelectedListid += 1)
            
    def OnButtonAddCategory(self, event):
        
        dia = CategoryAddDlg(self, 'Add Category', self.isManaged)
        dia.ShowModal()
        dia.Destroy()
        
        #os.system("\"" + self.interpreter_path + "\" .\PFPModule\PFPLib\CategoryAddDlg.pyc")

        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select CategoryName, Description from ModuleCategory order by CategoryName COLLATE NOCASE;"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        con.close()
        
        self.combo21.Clear()
          
        for row in ResultList:
            self.combo21.Append(row[0])
            
        return
    
    def OnButtonDelCategory(self, event):

        dlg = wx.MessageDialog(None, 'Are you sure to delete category?', 'Warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:

            SelectedText = self.combo21.GetValue()
    
            con = sqlite3.connect( self.DBPath )
            cursor = con.cursor()
            
            DeleteQuery = "delete from ModuleCategory where CategoryName = '" + SelectedText + "'"
            
            cursor.execute( DeleteQuery )
            con.commit()
            
            SelectQuery = "select CategoryName, Description from ModuleCategory order by CategoryName COLLATE NOCASE;"
            
            cursor.execute( SelectQuery )
            ResultList = cursor.fetchall()
            
            con.close()
            
            self.combo21.Clear()
              
            for row in ResultList:
                self.combo21.Append(row[0])
        
        return
    
    def OnButtonAddModule(self, event):
        
        self.SelectedListidx = self.List42.GetItemCount()
        
        for index in range(self.List41.GetItemCount()):
            if self.List41.IsChecked(index): 
                self.List42.InsertStringItem(self.SelectedListidx, self.List41.GetItemText(index))
                self.List42.SetStringItem(self.SelectedListidx, 1, self.List41.GetItem(index,1).GetText())
                self.List42.SetStringItem(self.SelectedListidx, 2, self.List41.GetItem(index,2).GetText())
                self.List42.SetStringItem(self.SelectedListidx, 3, self.List41.GetItem(index,3).GetText())
                self.SelectedListidx += 1
                
        return
    
    def OnButtonRemoveModule(self, event):
    
        for index in range(self.List42.GetItemCount()-1, -1, -1):
            if self.List42.IsChecked(index): 
                
                self.List42.DeleteItem(index)
                self.SelectedListidx -= 1      
    
        return
    
    
    def OnButtonOK(self, event):
        
        UtilClass = Util()
        
        
        #Add ContentsID of Module into ModuleIDs field in the ModuleCategory table
        ModuleIDs = ""
        
        for index in range(self.List42.GetItemCount()):
            ModuleIDs += self.List42.GetItem(index,3).GetText()
            ModuleIDs += ","
        
        ModuleIDs = UtilClass.DummyCyber(self.DecodedDummy, ModuleIDs, "")
        
        SelectedText = self.combo21.GetValue()
        
        con = sqlite3.connect( self.DBPath )
        cursor = con.cursor()
        
        UpdateQuery = "update ModuleCategory set ModuleIDs = '" + ModuleIDs + "' where CategoryName = '" + SelectedText + "'"
        cursor.execute( UpdateQuery )
        con.commit()
        
        self.Close()
        
        return
    
    
    def OnButtonCancel(self, event):
        
        self.Close()
        
        return
"""
def main():
    
    app = wx.App()
    Example(None, title="Module Category Setting")
    app.MainLoop()

if __name__ == '__main__':
    main() 
"""    
    