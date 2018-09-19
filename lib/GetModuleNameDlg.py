
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


class ModuleListList(wx.ListCtrl):
    
    #list Checkbox example - http://zetcode.com/wxpython/advanced/
    ExecuteStatus = ""
    FilePath = ""
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx. LC_EDIT_LABELS)
    
    
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
    
        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivated)

        self.InsertColumn(0, 'Module Name')
        self.InsertColumn(1, 'Description')

        
        con = sqlite3.connect( self.parent.GetParent().GetParent().default_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "Select ModuleName, Description, ContentsID from ModuleList order by ModuleName COLLATE NOCASE"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        con.close()
        
        idx = 0
        
        UtilClass = Util()
        
        for row in ResultList:
            try:
                con = sqlite3.connect( self.parent.GetParent().GetParent().default_user_modulelistDB_path )
                cursor = con.cursor()
                
                SelectQuery = "Select * from ModuleList where ContentsID = '" + row[2] + "'"
                
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall()
                
                con.close()
                
                if len(ResultList) == 0:
                    self.InsertStringItem(idx, row[0])
                    
                    try:
                        self.SetStringItem(idx, 1, UtilClass.DummyCyber(self.DecodedDummy, "", row[1]))
                    except:
                        self.SetStringItem(idx, 1, row[1])

                        
                    idx += 1
            except:
                continue
            
        
        size = self.parent.GetParent().GetParent().GetSize()
        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, size.x-5)
        
    def OnSize(self, event):
        
        event.Skip()
        
    def OnActivated(self, event):
         
        index = event.GetIndex()
        
        self.parent.GetParent().GetParent().SelectedModuleName = self.GetItem(index,0).GetText()
        
        dlg = wx.MessageDialog(None, "Select " + self.parent.GetParent().GetParent().SelectedModuleName + ", OK?", 'information', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        result = dlg.ShowModal() 
        if result == wx.ID_OK:    
            self.parent.GetParent().GetParent().Close()

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

class GetModuleNameDlg(wx.Dialog):

    def __init__(self, parent, log, DBPath):

        wx.Dialog.__init__(self, parent, -1, "Select Module Name..", size=(550, 600), style= wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)
        
        self.SelectedModuleName = ""
        self.default_user_modulelistDB_path = DBPath
        self.default_modulelistDB_path = "./PFPModule/PFPLib/PublicPFPList/public.modulelist.sqlite"
        
        
        con = sqlite3.connect( base64.b64decode("Li9QRlBNb2R1bGUvUEZQTGliL1B1YmxpY1BGUExpc3QvcHVibGljLjEuRmlyc3RSZXNwb25zZS5wZnBsaXN0LnNxbGl0ZQ=="))#"./PFPModule/PFPLib/PublicPFPList/public.1.LiveResponse.pfplist.sqlite" )
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
        st = wx.StaticText(panel1, -1, 'Module List in Reference Database', (5, 5))
        st.SetForegroundColour('WHITE')
        panel1.SetBackgroundColour('BLACK')
        
        panel2 = wx.Panel(panel, -1, style=wx.BORDER_SUNKEN)
        list = ModuleListList(panel2, -1)
        list.SetName('ModuleListOnList')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(list, 1, wx.EXPAND)
        panel2.SetSizer(vbox0)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel1, 0, wx.EXPAND)
        vbox1.Add(panel2, 1, wx.EXPAND)
        
        panel.SetSizer(vbox1)

        #TestUltimateListCtrl(panel, log, NewModuleList)


        #self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()

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

