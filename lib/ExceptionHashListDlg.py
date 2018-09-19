
from InternalModules.pfp_sdk.PFPUtil import *

class ModuleListList(wx.ListCtrl, CheckListCtrlMixin, TextEditMixin, ListCtrlAutoWidthMixin):
    
    #list Checkbox example - http://zetcode.com/wxpython/advanced/
    ExecuteStatus = ""
    FilePath = ""
    
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx. LC_EDIT_LABELS)
        CheckListCtrlMixin.__init__(self)
        TextEditMixin.__init__(self)
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
                  'PFPModule/PFPLib/InternalModules/pfp_sdk/icons/EmptyPrivateModule.png']
        
        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)    
    
        self.ExecuteStatus = "AllModule"
        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.InsertColumn(0, 'Original Path')
        self.InsertColumn(1, 'MD5')

        
        con = sqlite3.connect( self.parent.GetParent().GetParent().default_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "Select FileName, MD5 from ExceptionHashList"
        
        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()
        
        idx = 0
        for row in ResultList:
            self.InsertStringItem(idx, row[0])
            self.SetStringItem(idx, 1, row[1])
                    
            idx += 1
            
        
        size = self.parent.GetSize()
        self.SetColumnWidth(0, 300)
        self.SetColumnWidth(1, size.x-5)
        
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

class ExceptionHashListDlg(wx.Dialog):

    def __init__(self, parent, log, DBPath):

        wx.Dialog.__init__(self, parent, -1, "Excepted hash list..", size=(550, 600), style= wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)
        
        self.default_modulelistDB_path = DBPath
        
        panel = wx.Panel(self, -1)
        
        panel1 = wx.Panel(panel, -1, size=(-1, 25), style=wx.NO_BORDER)
        st = wx.StaticText(panel1, -1, 'Excepted hash list', (5, 5))
        st.SetForegroundColour('WHITE')
        panel1.SetBackgroundColour('BLACK')
        
        panel2 = wx.Panel(panel, -1, style=wx.BORDER_SUNKEN)
        list = ModuleListList(panel2, -1)
        list.SetName('ModuleListOnList')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(list, 1, wx.EXPAND)
        panel2.SetSizer(vbox0)
        
        panel3 = wx.Panel(panel, -1, size=(25, -1), style=wx.NO_BORDER)
        self.CheckAll = wx.BitmapButton(panel3, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/CheckAll.png'))
        self.ReleaseAll = wx.BitmapButton(panel3, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/ReleaseAll.png'))
        self.Deletebutton = wx.Button(panel3, label="Delete")
        list1 = Statusbar(panel3, -1)
        list1.SetName('Statusbar')
        
        vbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox2.Add(self.CheckAll, 0, wx.EXPAND)
        vbox2.Add(self.ReleaseAll, 0, wx.EXPAND)
        vbox2.Add(self.Deletebutton, 0, wx.EXPAND)
        vbox2.Add(list1, 1, wx.EXPAND)
        self.CheckAll.Bind(wx.EVT_BUTTON, self.OnCheckAll)
        self.ReleaseAll.Bind(wx.EVT_BUTTON, self.OnReleaseAll)
        self.Deletebutton.Bind(wx.EVT_BUTTON, self.OnDelete)
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
    
    def OnDelete(self, event):
        
        dlg = wx.MessageDialog(None, "Are you sure to delete the selected item from exception list?", 'warning', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        result = dlg.ShowModal() 
        
        if result == wx.ID_OK:
          
            con = sqlite3.connect( self.default_modulelistDB_path )
            cursor = con.cursor()
            
            window = self.FindWindowByName('ModuleListOnList')
            for index in range(window.GetItemCount()-1, -1, -1):
                if window.IsChecked(index): 
                    
                    MD5 = window.GetItem(index,1).GetText()
                    
                    DeleteQuery = "delete from ExceptionHashList where MD5 = '" + MD5 + "'"
            
                    cursor.execute( DeleteQuery )
                    con.commit()
                    
                    
            window.DeleteAllItems()
            
            SelectQuery = "Select FileName, MD5 from ExceptionHashList"
        
            cursor.execute( SelectQuery )
            ResultList = cursor.fetchall()
            
            idx = 0
            for row in ResultList:
                window.InsertStringItem(idx, row[0])
                window.SetStringItem(idx, 1, row[1])
                        
                idx += 1
                         
            con.close()
            
            
            
    
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

