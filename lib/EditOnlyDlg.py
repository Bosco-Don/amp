#!/usr/bin/python

from InternalModules.pfp_sdk.PFPUtil import *

class EditOnlyDlg(wx.Dialog):
    def __init__(self, parent, id, title, url):
        wx.Dialog.__init__(self, parent, id, title, size=(550, 80))

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.editctrl = wx.TextCtrl(self, size=(540, 50))
        
        self.button151 = wx.Button(self, label="Ok")
        self.button151.Bind(wx.EVT_BUTTON, self.OnButtonOK)
        
        vbox.Add(self.editctrl, 1, wx.ALIGN_CENTER)
        vbox.Add(self.button151, 0, wx.ALIGN_CENTER)

        self.SetSizer(vbox)
        
        try:
            self.editctrl.WriteText(url)
        except:
            print ""
            
        self.returnVal = ""

    def OnButtonOK(self, event):
        self.returnVal = self.editctrl.GetLineText(0)
        self.Close()

