#!/usr/bin/python
# -*- coding: utf-8 -*-

# newclass.py

from pfp_sdk.PFPUtil import *


class Example(wx.Frame):
    

    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, pos=(100,100), size=(800, 230))

        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
        
        
        #read config file
        self.default_modulelistDB_path = ""
        self.user = ""
        self.contact = ""

      
        panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(9, 9)

        #---Main Text
        text1 = wx.StaticText(panel, label="  Category")
        sizer.Add(text1, pos=(0, 0), flag=wx.EXPAND, border=50)

        #---Logo
        #icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('PFPModule/icons/SelfTest.png'))
        #sizer.Add(icon, pos=(0, 3), flag=wx.EXPAND, border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 4), flag=wx.EXPAND|wx.BOTTOM, border=5)

        #---Category Combo
        text2 = wx.StaticText(panel, label="  Category Name")
        sizer.Add(text2, pos=(2, 0), flag=wx.EXPAND, border=5)
        
        self.tc2 = wx.TextCtrl(panel)
        sizer.Add(self.tc2, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        text3 = wx.StaticText(panel, label="  Description")
        sizer.Add(text3, pos=(3, 0), flag=wx.EXPAND, border=5)
        
        self.tc3 = wx.TextCtrl(panel)
        sizer.Add(self.tc3, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
              
        #---Last Buttons
        
        self.button91 = wx.Button(panel, label="Apply", size = wx.Size(70,30))
        sizer.Add(self.button91, pos=(4, 1), span=(1, 1), flag=wx.ALIGN_RIGHT)
        self.button91.Bind(wx.EVT_BUTTON, self.OnButtonOK)

        self.button92 = wx.Button(panel, label="Cancel", size = wx.Size(70,30))
        sizer.Add(self.button92, pos=(4, 2), span=(1, 1), flag=wx.ALIGN_LEFT)
        self.button92.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        
        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
    
    def OnButtonOK(self, event):
         
        #Add RowID of Module into ModuleIDs field in the ModuleCategory table
        
        con = sqlite3.connect( self.default_modulelistDB_path )
        cursor = con.cursor()
        
        SelectQuery = "select * from ModuleCategory;"
        
        cursor.execute( SelectQuery )
        Results = cursor.fetchall()
        
        count = 0 
        for row in Results:
            if row[1].lower() == self.tc2.GetValue().lower():
                count += 1
        
        if count > 0:
            wx.MessageBox("Category Name is duplicated")
            return
        
        InsertQuery = "insert into ModuleCategory values (null, '" + self.tc2.GetValue() + "', '"+ self.tc3.GetValue() +"', '')"
        cursor.execute( InsertQuery )
        con.commit()
        
        con.close()
        
        self.Close()
        
        return
    
    def OnButtonCancel(self, event):
        
        self.Close()
        
        return

def main():
    
    app = wx.App()
    Example(None, title="Module Category Setting")
    app.MainLoop()

if __name__ == '__main__':
    main() 
    
    