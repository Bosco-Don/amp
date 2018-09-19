#!/usr/bin/python
# -*- coding: utf-8 -*-

from InternalModules.pfp_sdk.PFPUtil import *

class PFPConfig(wx.Dialog):
    

    def __init__(self, parent, title):    
        wx.Dialog.__init__(self, parent, title=title, size=(610, 450))

        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
        
        
        #read config file
        self.updatemain = ""
        self.updateserver = ""
        self.autoupdate = ""
        self.public_pfplist_path = ""
        self.default_pfplist_path = ""
        self.default_modulelistDB_path = ""
        self.interpreter_path = ""
        self.user = ""
        self.contact = ""
        
        self.idx = 0 

        
        config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "r")
        
        filelines = config_fp.readlines()
        for line in filelines:
            if "update main(url||ip)" in line:
                self.updatemain =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "update dir(url||ip)" in line:
                self.updateserver =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "autoupdate" in line:
                self.autoupdate =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "default public pfplist path" in line:
                self.public_pfplist_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "default user pfplist path" in line:
                self.default_pfplist_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "default public modulelistDB path" in line:
                self.default_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
                
            elif "default user modulelistDB path" in line:
                self.default_user_modulelistDB_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "interpreter path(win)" in line:
                self.interpreter_path =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "user(pfp id)" in line:
                self.user =  line.split(">")[1].strip("\"").strip("\n")
            
            elif "contact" in line:
                self.contact =  line.split(">")[1].strip("\"").strip("\n")
      
        panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(5, 5)

        #Main Text
        text1 = wx.StaticText(panel, label="Configure")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        #Logo
        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/SelfTest.png'))
        sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=5)

        #Default List path
        text2 = wx.StaticText(panel, label="Default PFP List")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc2 = wx.TextCtrl(panel)
        sizer.Add(self.tc2, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.tc2.WriteText(self.default_pfplist_path)
        
        self.button2 = wx.Button(panel, label="Browse..")
        sizer.Add(self.button2, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButtonPFPListPath)
        
        #Default Module path
        text3 = wx.StaticText(panel, label="Default ModuleList")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc3 = wx.TextCtrl(panel)
        sizer.Add(self.tc3, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.tc3.WriteText(self.default_modulelistDB_path)

        self.button3 = wx.Button(panel, label="Browse..")
        sizer.Add(self.button3, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButtonModuleListPath)
        
        #Interperter(win)
        text4 = wx.StaticText(panel, label="Interpreter(win)")
        sizer.Add(text4, pos=(4, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc4 = wx.TextCtrl(panel)
        sizer.Add(self.tc4, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)

        self.tc4.WriteText(self.interpreter_path)

        self.button4 = wx.Button(panel, label="Browse..")
        sizer.Add(self.button4, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button4.Bind(wx.EVT_BUTTON, self.OnButtonWinInterpreterPath)
        
        #Interperter(mac)
        text5 = wx.StaticText(panel, label="Interpreter(mac)")
        sizer.Add(text5, pos=(5, 0), flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.tc5 = wx.TextCtrl(panel)
        sizer.Add(self.tc5, pos=(5, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.tc5.Disable()

        self.button5 = wx.Button(panel, label="Browse..")
        sizer.Add(self.button5, pos=(5, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.button5.Bind(wx.EVT_BUTTON, self.OnButtonMacInterpreterPath)
        
        self.button5.Disable()
        
        #User
        text6 = wx.StaticText(panel, label="User(PFP ID)")
        sizer.Add(text6, pos=(6, 0), flag=wx.LEFT, border=5)
        
        self.tc6 = wx.TextCtrl(panel)
        sizer.Add(self.tc6, pos=(6, 1), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.tc6.Disable()
        
        self.tc6.WriteText(self.user)
        
            
        #Contact
        text61 = wx.StaticText(panel, label="           Contact")
        sizer.Add(text61, pos=(6, 2), flag=wx.LEFT, border=5)
        
        self.tc61 = wx.TextCtrl(panel)
        sizer.Add(self.tc61, pos=(6, 3), flag=wx.TOP|wx.EXPAND, border=5)
        
        self.tc61.Disable()
        
        self.tc61.WriteText(self.contact)

        #Update main 
        text7 = wx.StaticText(panel, label="Update Main")
        sizer.Add(text7, pos=(7, 0), flag=wx.LEFT, border=5)
        
        self.tc7 = wx.TextCtrl(panel)
        sizer.Add(self.tc7,  pos=(7, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=5)

        self.tc7.WriteText(self.updatemain)
        
        #Autoupdate
        self.chk8 = wx.CheckBox(panel, label=" Auto Update")
        sizer.Add(self.chk8, pos=(7, 3), span=(1, 5), flag=wx.LEFT|wx.TOP, border=5)
        
        if "true" in self.autoupdate.lower():
            self.chk8.SetValue(1)
            
        #Update dir  
        text8 = wx.StaticText(panel, label="Update Dir")
        sizer.Add(text8, pos=(8, 0), flag=wx.LEFT, border=5)
        
        self.tc8 = wx.TextCtrl(panel)
        sizer.Add(self.tc8,  pos=(8, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)

        self.tc8.WriteText(self.updateserver)
                
        #Last Button
        self.button90 = wx.Button(panel, label='Help')
        sizer.Add(self.button90, pos=(9, 0), flag=wx.LEFT, border=10)
        self.button90.Bind(wx.EVT_BUTTON, self.OnButtonHelp)

        self.button91 = wx.Button(panel, label="Apply")
        sizer.Add(self.button91, pos=(9, 2), flag=wx.BOTTOM|wx.RIGHT)
        self.button91.Bind(wx.EVT_BUTTON, self.OnButtonOK)

        self.button92 = wx.Button(panel, label="Cancel")
        sizer.Add(self.button92, pos=(9, 4), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=5)
        self.button92.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        
        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
        
        self.tc2.Disable()
        self.button2.Disable()
        self.tc3.Disable()
        self.button3.Disable()
        self.tc4.Disable()
        self.button4.Disable()
        self.tc5.Disable()
        self.button5.Disable()
        self.tc6.Disable()
        self.tc61.Disable()
        self.tc7.Disable()
        self.tc8.Disable() 
        
    def OnButtonPFPListPath(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/PFPModule/PFPLib/PublicPFPList", defaultFile="", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
        
            if SelectedFile.find("PFPModule\\PFPLib\\PublicPFPList") != -1:
                
                Num = SelectedFile.find("PFPModule\\PFPLib\\PublicPFPList")
                
                SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
                
                self.tc2.Clear()
                self.tc2.WriteText(SelectedFile)
                                 
            else : 
                wx.MessageBox("Select Module in %PFPROOT%/PFPModule/PFPLib/PublicPFPList")
        
        return
    
    def OnButtonModuleListPath(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile="", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
        
            if SelectedFile.find("UserModule") != -1:
                
                Num = SelectedFile.find("UserModule")
                
                SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
                
                self.tc3.Clear()
                self.tc3.WriteText(SelectedFile)
                                 
            else : 
                wx.MessageBox("Select Module in %PFPROOT%/UserModule")
        
        return
    
    def OnButtonWinInterpreterPath(self, event):
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/Utility", defaultFile="", style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
        
            if SelectedFile.find("PFPModule\\PFPLib\\PublicPFPList") != -1:
                
                Num = SelectedFile.find("PFPModule\\PFPLib\\PublicPFPList")
                
                SelectedFile = SelectedFile.replace(SelectedFile[0:Num], "./")
                SelectedFile = SelectedFile.replace("\\", "/")
                
                self.tc4.Clear()
                self.tc4.WriteText(SelectedFile)
                                 
            else : 
                wx.MessageBox("Select Module in %PFPROOT%/PFPModule/PFPLib/PublicPFPList")
        
        return
    
    def OnButtonMacInterpreterPath(self, event):
        
        return
    
    def OnButtonHelp(self, event):
        
        wx.MessageBox("Portable Forensic Platform - by Zurum\n\nContact : \tzurum86@gmail.com\nProject : \thttp://portable-forensics.com/\nblog : \thttp://portable-forensics.blogspot.kr/\n")
        
        return
    
    def OnButtonOK(self, event):
         
         
        self.updatemain = self.tc7.GetLineText(0)
        self.updateserver = self.tc8.GetLineText(0)
        if self.chk8.GetValue() == 1:
            self.autoupdate = "true"
        else:
            self.autoupdate = "false"
        self.default_pfplist_path = self.tc2.GetLineText(0)
        self.default_modulelistDB_path = self.tc3.GetLineText(0)
        self.interpreter_path_win = self.tc4.GetLineText(0)
        self.interpreter_path_mac = self.tc5.GetLineText(0)
        self.user = self.tc6.GetLineText(0)
        self.contact = self.tc61.GetLineText(0)
        
        
        os.remove("./PFPModule/PFPLib/pfpconfig.conf")
        new_config_fp = open("./PFPModule/PFPLib/pfpconfig.conf", "a+")
        
        new_config_fp.write("update main(url||ip)>"+self.updatemain+"\n")
        new_config_fp.write("update dir(url||ip)>"+self.updateserver+"\n")
        new_config_fp.write("autoupdate>"+self.autoupdate+"\n")
        new_config_fp.write("default public pfplist path>"+self.public_pfplist_path+"\n")
        new_config_fp.write("default user pfplist path>"+self.default_pfplist_path+"\n")
        new_config_fp.write("default public modulelistDB path>"+self.default_modulelistDB_path+"\n")
        new_config_fp.write("default user modulelistDB path>"+self.default_user_modulelistDB_path+"\n")
        new_config_fp.write("interpreter path(win)>"+self.interpreter_path_win+"\n")
        new_config_fp.write("interpreter path(mac)>"+self.interpreter_path_mac+"\n")
        new_config_fp.write("user(pfp id)>"+self.user+"\n")
        new_config_fp.write("contact>"+self.contact+"\n")
        
        wx.MessageBox("Please restart platform to apply")
        
        self.Close()
        
        return
    
    def OnButtonCancel(self, event):
        
        self.Close()
        
        return
"""
def main():
    
    app = wx.App()
    Example(None, title="PFP Configure")
    app.MainLoop()

if __name__ == '__main__':
    main() 
"""   
    