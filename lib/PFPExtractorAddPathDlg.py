#!/usr/bin/python

from InternalModules.pfp_sdk.PFPUtil import *


class PFPExtractorAddPathDlg(wx.Dialog):
    def __init__(self, parent, title):    
        wx.Dialog.__init__(self, parent, title=title, size=(600,400), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.isManaged = False
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
        

        self.panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(9, 9)

        #---ListCtrl
        #self.List41 = CheckList(self.panel, -1)
        #sizer.Add(self.List41, pos=(4, 0), span=(22, 15), flag=wx.EXPAND, border=5)
        
        self.text41 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.ST_NO_AUTORESIZE) 
        sizer.Add(self.text41, pos=(0, 0), span=(12, 15), flag=wx.TOP|wx.EXPAND, border=5)
        
        
        #---Last Buttons
        self.buttonDirDlg = wx.Button(self.panel, label="dir dlg", size = wx.Size(70,30))
        sizer.Add(self.buttonDirDlg, pos=(12, 0), span=(1, 1), flag=wx.ALIGN_RIGHT)
        self.buttonDirDlg.Bind(wx.EVT_BUTTON, self.OnButtonDirDlg)
        
        self.buttonFileDlg = wx.Button(self.panel, label="file dlg", size = wx.Size(70,30))
        sizer.Add(self.buttonFileDlg, pos=(12, 1), span=(1, 1), flag=wx.ALIGN_RIGHT)
        self.buttonFileDlg.Bind(wx.EVT_BUTTON, self.OnButtonFileDlg)

        self.buttonOK = wx.Button(self.panel, label="OK", size = wx.Size(70,30))
        sizer.Add(self.buttonOK, pos=(12, 2), span=(1, 1), flag=wx.ALIGN_RIGHT)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOK)
        
        sizer.AddGrowableCol(2)
        
        self.panel.SetSizer(sizer)
        
            
        self.returnVal = ""


    def OnButtonDirDlg(self, event):
        
        dlg = wx.DirDialog(self, message="Select Target Folder", style=wx.OPEN)
        Target = ""
        if dlg.ShowModal() == wx.ID_OK:
            Target = dlg.GetPath().encode('cp949') 
            self.text41.AppendText("\n" + Target)
            
    
    def OnButtonFileDlg(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target file", style=wx.OPEN)
        Target = ""
        if dlg.ShowModal() == wx.ID_OK:
            Target = dlg.GetPath().encode('cp949') 
            self.text41.AppendText("\n" + Target)
    

    def OnButtonOK(self, event):
        for linenum in range(0,self.text41.GetNumberOfLines()):
            self.returnVal += self.text41.GetLineText(linenum)
            self.returnVal += "\n"
            
        self.Close()

