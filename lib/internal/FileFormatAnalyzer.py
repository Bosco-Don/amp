# -*- coding: 949 -*-
#!/usr/bin/python

#command..!
#q:
#".괮tility괦ortable Python 2.7.3.2괔pp굋ython.exe" ".괦FPModule괦FPLib괞nternalModules괚ileFormatAnalyzer.py"

from pfp_sdk.PFPUtil import *

from pfp_sdk.xlrd import *
from pfp_sdk.ParsingEngine import *
from pfp_sdk.ParsingEngine_v2 import *

PyFileLocation = "./PFPModule/PFPLib/InternalModules/" 


#---code for sume UI
TreeBaseClass = wx.TreeCtrl
images = None
ALLOW_AUI_FLOATING = True
DEFAULT_PERSPECTIVE = "Default Perspective"


penstyle = ["wx.SOLID", "wx.TRANSPARENT", "wx.DOT", "wx.LONG_DASH", "wx.DOT_DASH", "wx.USER_DASH",
           "wx.BDIAGONAL_HATCH", "wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
           "wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH"]

ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]

keyMap = {
    wx.WXK_BACK : "WXK_BACK",
    wx.WXK_TAB : "WXK_TAB",
    wx.WXK_RETURN : "WXK_RETURN",
    wx.WXK_ESCAPE : "WXK_ESCAPE",
    wx.WXK_SPACE : "WXK_SPACE",
    wx.WXK_DELETE : "WXK_DELETE",
    wx.WXK_START : "WXK_START",
    wx.WXK_LBUTTON : "WXK_LBUTTON",
    wx.WXK_RBUTTON : "WXK_RBUTTON",
    wx.WXK_CANCEL : "WXK_CANCEL",
    wx.WXK_MBUTTON : "WXK_MBUTTON",
    wx.WXK_CLEAR : "WXK_CLEAR",
    wx.WXK_SHIFT : "WXK_SHIFT",
    wx.WXK_ALT : "WXK_ALT",
    wx.WXK_CONTROL : "WXK_CONTROL",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
    wx.WXK_PRIOR : "WXK_PRIOR",
    wx.WXK_NEXT : "WXK_NEXT",
    wx.WXK_END : "WXK_END",
    wx.WXK_HOME : "WXK_HOME",
    wx.WXK_LEFT : "WXK_LEFT",
    wx.WXK_UP : "WXK_UP",
    wx.WXK_RIGHT : "WXK_RIGHT",
    wx.WXK_DOWN : "WXK_DOWN",
    wx.WXK_SELECT : "WXK_SELECT",
    wx.WXK_PRINT : "WXK_PRINT",
    wx.WXK_EXECUTE : "WXK_EXECUTE",
    wx.WXK_SNAPSHOT : "WXK_SNAPSHOT",
    wx.WXK_INSERT : "WXK_INSERT",
    wx.WXK_HELP : "WXK_HELP",
    wx.WXK_NUMPAD0 : "WXK_NUMPAD0",
    wx.WXK_NUMPAD1 : "WXK_NUMPAD1",
    wx.WXK_NUMPAD2 : "WXK_NUMPAD2",
    wx.WXK_NUMPAD3 : "WXK_NUMPAD3",
    wx.WXK_NUMPAD4 : "WXK_NUMPAD4",
    wx.WXK_NUMPAD5 : "WXK_NUMPAD5",
    wx.WXK_NUMPAD6 : "WXK_NUMPAD6",
    wx.WXK_NUMPAD7 : "WXK_NUMPAD7",
    wx.WXK_NUMPAD8 : "WXK_NUMPAD8",
    wx.WXK_NUMPAD9 : "WXK_NUMPAD9",
    wx.WXK_MULTIPLY : "WXK_MULTIPLY",
    wx.WXK_ADD : "WXK_ADD",
    wx.WXK_SEPARATOR : "WXK_SEPARATOR",
    wx.WXK_SUBTRACT : "WXK_SUBTRACT",
    wx.WXK_DECIMAL : "WXK_DECIMAL",
    wx.WXK_DIVIDE : "WXK_DIVIDE",
    wx.WXK_F1 : "WXK_F1",
    wx.WXK_F2 : "WXK_F2",
    wx.WXK_F3 : "WXK_F3",
    wx.WXK_F4 : "WXK_F4",
    wx.WXK_F5 : "WXK_F5",
    wx.WXK_F6 : "WXK_F6",
    wx.WXK_F7 : "WXK_F7",
    wx.WXK_F8 : "WXK_F8",
    wx.WXK_F9 : "WXK_F9",
    wx.WXK_F10 : "WXK_F10",
    wx.WXK_F11 : "WXK_F11",
    wx.WXK_F12 : "WXK_F12",
    wx.WXK_F13 : "WXK_F13",
    wx.WXK_F14 : "WXK_F14",
    wx.WXK_F15 : "WXK_F15",
    wx.WXK_F16 : "WXK_F16",
    wx.WXK_F17 : "WXK_F17",
    wx.WXK_F18 : "WXK_F18",
    wx.WXK_F19 : "WXK_F19",
    wx.WXK_F20 : "WXK_F20",
    wx.WXK_F21 : "WXK_F21",
    wx.WXK_F22 : "WXK_F22",
    wx.WXK_F23 : "WXK_F23",
    wx.WXK_F24 : "WXK_F24",
    wx.WXK_NUMLOCK : "WXK_NUMLOCK",
    wx.WXK_SCROLL : "WXK_SCROLL",
    wx.WXK_PAGEUP : "WXK_PAGEUP",
    wx.WXK_PAGEDOWN : "WXK_PAGEDOWN",
    wx.WXK_NUMPAD_SPACE : "WXK_NUMPAD_SPACE",
    wx.WXK_NUMPAD_TAB : "WXK_NUMPAD_TAB",
    wx.WXK_NUMPAD_ENTER : "WXK_NUMPAD_ENTER",
    wx.WXK_NUMPAD_F1 : "WXK_NUMPAD_F1",
    wx.WXK_NUMPAD_F2 : "WXK_NUMPAD_F2",
    wx.WXK_NUMPAD_F3 : "WXK_NUMPAD_F3",
    wx.WXK_NUMPAD_F4 : "WXK_NUMPAD_F4",
    wx.WXK_NUMPAD_HOME : "WXK_NUMPAD_HOME",
    wx.WXK_NUMPAD_LEFT : "WXK_NUMPAD_LEFT",
    wx.WXK_NUMPAD_UP : "WXK_NUMPAD_UP",
    wx.WXK_NUMPAD_RIGHT : "WXK_NUMPAD_RIGHT",
    wx.WXK_NUMPAD_DOWN : "WXK_NUMPAD_DOWN",
    wx.WXK_NUMPAD_PRIOR : "WXK_NUMPAD_PRIOR",
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
    wx.WXK_NUMPAD_NEXT : "WXK_NUMPAD_NEXT",
    wx.WXK_NUMPAD_PAGEDOWN : "WXK_NUMPAD_PAGEDOWN",
    wx.WXK_NUMPAD_END : "WXK_NUMPAD_END",
    wx.WXK_NUMPAD_BEGIN : "WXK_NUMPAD_BEGIN",
    wx.WXK_NUMPAD_INSERT : "WXK_NUMPAD_INSERT",
    wx.WXK_NUMPAD_DELETE : "WXK_NUMPAD_DELETE",
    wx.WXK_NUMPAD_EQUAL : "WXK_NUMPAD_EQUAL",
    wx.WXK_NUMPAD_MULTIPLY : "WXK_NUMPAD_MULTIPLY",
    wx.WXK_NUMPAD_ADD : "WXK_NUMPAD_ADD",
    wx.WXK_NUMPAD_SEPARATOR : "WXK_NUMPAD_SEPARATOR",
    wx.WXK_NUMPAD_SUBTRACT : "WXK_NUMPAD_SUBTRACT",
    wx.WXK_NUMPAD_DECIMAL : "WXK_NUMPAD_DECIMAL",
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE"
    }

_demoPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
             "book", "customcontrol", "morecontrols", "layout", "process", "clipboard",
             "images", "miscellaneous"]




#---Pane Classes------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---Center Panes------------------------------------------------------------------------
class TemplateViewer(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, log):
        self.parent = parent
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None
        self._grid_selecting_start = False
        self._in_selecting = False
        self._hex_cols = 16

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.CreateGrid(100, 100)#, gridlib.Grid.SelectRows)
        colour = '#e6f1f5'#'#d0dff1'#'#dce6f1'#'#e6f1f5'
        #self.SetGridLineColour(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE ))
        self.SetGridLineColour(colour)
        ##self.EnableEditing(False)


        self.isSelectedBlockExist = False
        self.SelectedBlock_StartX = 0
        self.SelectedBlock_StartY = 0
        self.SelectedBlock_EndX = 0
        self.SelectedBlock_EndY = 0
        self.SelectedBlock_OriginalColor = '#ffffff'
        self.SelectedBlock_OriginalDepth = 0   



        # simple cell formatting
        for idx in range(0,0x10):
            if idx < 10:
                self.SetColLabelValue(idx, str(idx))
            if idx == 10:
                self.SetColLabelValue(idx, 'A')
            if idx == 11:
                self.SetColLabelValue(idx, 'B')
            if idx == 12:
                self.SetColLabelValue(idx, 'C')
            if idx == 13:
                self.SetColLabelValue(idx, 'D')
            if idx == 14:
                self.SetColLabelValue(idx, 'E')
            if idx == 15:
                self.SetColLabelValue(idx, 'F')
            #if idx == 16:
            #    self.SetColLabelValue(idx, 'A')
            self.SetColSize(idx, 30)
            
        

        
        # test all the events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.GetGridWindow().Bind(wx.EVT_LEFT_DOWN, self.OnGridLeftDown)
        self.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnGridLeftUp)
        self.GetGridWindow().Bind(wx.EVT_MOTION, self.OnGridLeftMotion)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        
        

    def OnSize(self, event):
        size = self.parent.GetSize()
        
        for idx in range(0, 100):
            self.SetColSize(idx, 30)
            #self.SetColSize(idx, (size.x-101)/16)
            
        for idx in range(0, 100):
            self.SetRowSize(idx, 23)
            
        event.Skip()


    def OnGridLeftDown(self, event):
        start_pos = self._client_to_scroll_pos(event.X, event.Y)
        self._grid_selecting_start = self.XYToCell(*start_pos)
        event.Skip()

    def OnGridLeftUp(self, event):
        event.Skip()
        wx.CallAfter(self._set_selection, callback=self._reset_grid_selecting)

    def OnGridLeftMotion(self, event):
        if not self._in_selecting and self._grid_selecting_start:
            end_pos = self._client_to_scroll_pos(event.X, event.Y)
            end_pos = self.XYToCell(*end_pos)
            if end_pos != (-1, -1):
                wx.CallAfter(self._set_selection, end_pos=end_pos)
                
                
                
                
    def RowColToAddr(self, row, col, check_max=True):
        col = self._hex_cols - 1 if col >= self._hex_cols else col
        #print row, self._hex_cols, col
        addr = row * self._hex_cols + col
        if check_max:
            addr = self._check_addr_in_range(addr)
        return addr
    
    def Length(self):
        return self.GetTable().length

    def HexCols(self):
        return self._hex_cols

    def _reset_grid_selecting(self):
        self._grid_selecting_start = None
    
    def _client_to_scroll_pos(self, x, y):
        ppunit = self.GetScrollPixelsPerUnit()
        scroll_x = self.GetScrollPos(wx.HORIZONTAL)
        scroll_y = self.GetScrollPos(wx.VERTICAL)
        x += scroll_x * ppunit[0]
        y += scroll_y * ppunit[1]
        return x, y
    
    def _set_selection(self, end_pos=None, callback=None):
        self._in_selecting = True
        if end_pos and self._grid_selecting_start:
            cur_row, cur_col = self._grid_selecting_start
            end_row, end_col = end_pos

            if cur_col == self.HexCols:
                if cur_row > end_row:
                    cur_row, end_row = end_row, cur_row
                min_addr = self.RowColToAddr(cur_row, 0)
                max_addr = self.RowColToAddr(end_row, self.HexCols - 1)
                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
            else:
                if end_col == self.HexCols:
                    end_col -= 1
                if (cur_row, cur_col) == (end_row, end_col):
                    min_addr = max_addr = self.RowColToAddr(cur_row, cur_col, False)
                    if min_addr > self.Length:
                        min_addr = max_addr = self.Length
                else:
                    min_addr = self.RowColToAddr(cur_row, cur_col)
                    max_addr = self.RowColToAddr(end_row, end_col)
                    if min_addr > max_addr:
                        min_addr, max_addr = max_addr, min_addr

                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
        else:
            rows = self.GetSelectedRows()
            if rows:
                min_row = min(rows)
                max_row = max(rows)
                self.SetGridCursor(min_row, 0)
                self.ClearSelection()
                min_addr = self.RowColToAddr(min_row, 0)
                max_addr = self.RowColToAddr(max_row, self.HexCols - 1)
                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
            else:
                top_left = self.GetSelectionBlockTopLeft()
                bottom_right = self.GetSelectionBlockBottomRight()
                cells = self.GetSelectedCells()

                addrs = [self.RowColToAddr(row, col) for (row, col) in top_left + bottom_right + cells]
                if addrs:
                    min_addr = min(addrs)
                    max_addr = max(addrs)
                    self.SetSelection(min_addr, max_addr - min_addr + 1, False)
                #else:
                    #self._update_status(sel=1)

        self._in_selecting = False
        if callable(callback):
            callback()
        #self.grid.Refresh()

    def SetSelection(self, addr, length=1, jumpto=False):
        row, col = self.AddrToRowCol(addr)
        end_row, end_col = self.AddrToRowCol(addr + length - 1)

        self.Freeze()
        self.BeginBatch()
        self.SetGridCursor(row, col)
        if length > 0:
            # in same row
            if row == end_row:
                self.SelectBlock(row, col, end_row, end_col)
            elif end_row > row:
                #first row
                self.SelectBlock(row, col, row, self._hex_cols - 1)
                if end_row - row > 1:
                    self.SelectBlock(row + 1, 0, end_row - 1, self._hex_cols - 1, addToSelected=True)
                #last row
                self.SelectBlock(end_row, 0, end_row, end_col, addToSelected=True)
        self.EndBatch()
        self.Thaw()
        #self._update_status(sel=length)
        if jumpto:
            self.JumpTo(row, col)

    def AddrToRowCol(self, addr):
        return addr / self._hex_cols, addr % self._hex_cols


    def RowColToAddr(self, row, col, check_max=True):
        col = self._hex_cols - 1 if col >= self._hex_cols else col
        addr = row * self._hex_cols + col
        if check_max:
            addr = self._check_addr_in_range(addr)
        return addr


    def _check_addr_in_range(self, addr):
        addr = addr if addr > 0 else 0
        addr = addr if addr < self.Length else self.Length - 1
        return addr



    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()


    def OnCellLeftDClick(self, evt):

        #recover original selected block
        if self.isSelectedBlockExist == True:
            
            for y_idx in range(self.SelectedBlock_StartY, self.SelectedBlock_EndY+1):
                for x_idx in range(0, 16):
                    if y_idx == self.SelectedBlock_StartY and x_idx < self.SelectedBlock_StartX :
                        continue
                    if y_idx == self.SelectedBlock_EndY and x_idx >= self.SelectedBlock_EndX :
                        break
                    
                    self.SetCellBackgroundColour(y_idx, x_idx + self.SelectedBlock_OriginalDepth*17, self.SelectedBlock_OriginalColor) #"#dce6f1"
                    self.SetCellTextColour(y_idx, x_idx + self.SelectedBlock_OriginalDepth*17, "#000000")
                                
                    #if y_idx != StartY and x_idx != StartX:
                    Name = self.GetCellValue(y_idx, x_idx + self.SelectedBlock_OriginalDepth*17)
                    self.SetCellValue(y_idx, x_idx + self.SelectedBlock_OriginalDepth*17, Name)
        
        
        
        
        
        
        
        
        #Get new selected info
        #Get Colour
        Depth = evt.GetCol()/17
        SelectedY = evt.GetRow()
        SelectedX = evt.GetCol() - Depth*17
        self.SelectedBlock_OriginalColor = self.GetCellBackgroundColour(SelectedY, SelectedX + Depth*17)
        
        #Find Start
        StartX = 0
        StartY = 0
        
        FindFlag = False
        for y_idx in range(0, SelectedY+1):
            for x_idx in range(0, 16):
                if (SelectedY-y_idx)==SelectedY and (15-x_idx) > SelectedX:
                    continue
                
                if self.GetCellValue((SelectedY-y_idx), (15-x_idx) + Depth*17).strip() != "" or self.GetCellBackgroundColour((SelectedY-y_idx), (15-x_idx) + Depth*17) != self.SelectedBlock_OriginalColor:
                    
                    if self.GetCellBackgroundColour((SelectedY-y_idx), (15-x_idx) + Depth*17) != self.SelectedBlock_OriginalColor:
                        StartX = (15-x_idx)+1
                        StartY = (SelectedY-y_idx)

                        if StartX == 16:
                            StartX = 0
                            StartY = (SelectedY-y_idx) + 1
                    else:
                        StartX = (15-x_idx)
                        StartY = (SelectedY-y_idx)
                        
                    FindFlag = True
                    break
            if FindFlag == True:
                break
        #print str(StartY), str(StartX)
        
        
        #Find End
        EndX = 0
        EndY = 0
        
        FindFlag = False
        for y_idx in range(SelectedY, 100):
            for x_idx in range(0, 16):
                if x_idx == StartX and y_idx == StartY:
                    continue 
                if x_idx < SelectedX and y_idx == SelectedY:
                    continue 
                
                if self.GetCellValue(y_idx, x_idx + Depth*17).strip() != "" or self.GetCellBackgroundColour(y_idx, x_idx + Depth*17) != self.SelectedBlock_OriginalColor:
                    EndX = x_idx
                    EndY = y_idx
                    FindFlag = True
                    break
            if FindFlag == True:
                break
        #print str(EndY), str(EndX)
        
        
        
        
        
        
        #fill new
        self.SelectedBlock_StartX = StartX
        self.SelectedBlock_StartY = StartY
        self.SelectedBlock_EndX = EndX
        self.SelectedBlock_EndY = EndY
        self.SelectedBlock_OriginalColor = self.GetCellBackgroundColour(SelectedY, SelectedX + Depth*17)
        self.isSelectedBlockExist = True
        self.SelectedBlock_OriginalDepth = Depth
        
        for y_idx in range(StartY, EndY+1):
            for x_idx in range(0, 16):
                if y_idx == StartY and x_idx < StartX :
                    continue
                if y_idx == EndY and x_idx >= EndX :
                    break
                
                self.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#000000") #"#dce6f1"
                self.SetCellTextColour(y_idx, x_idx + Depth*17, "#ffffff")
                            
                #if y_idx != StartY and x_idx != StartX:
                Name = self.GetCellValue(y_idx, x_idx + Depth*17)
                self.SetCellValue(y_idx, x_idx + Depth*17, Name)
        
        evt.Skip()
        
        
        
        
        
        MainFrame = self.GetParent().GetParent().GetParent().GetParent().GetParent()
        
        #Query Setting
        Query = self.GetCellValue(StartY, StartX + Depth*17)
        
        SelectedY = evt.GetRow()
        SelectedX = evt.GetCol() - Depth*17
        
        for idx in range(1, Depth+1):
            #Find Start
            StartX = 0
            StartY = 0
            
            FindFlag = False
            
            Sub_Depth = evt.GetCol()/17 - idx
            self.TempColour = self.GetCellBackgroundColour(SelectedY, SelectedX + Sub_Depth*17)
            
            for y_idx in range(0, SelectedY):
                for x_idx in range(0, 16):
                    if (SelectedY-y_idx)==SelectedY and (15-x_idx) > SelectedX:
                        continue
                    
                    if self.GetCellValue((SelectedY-y_idx), (15-x_idx) + (Sub_Depth)*17).strip() != "" or self.GetCellBackgroundColour((SelectedY-y_idx), (15-x_idx) + (Sub_Depth)*17) != self.TempColour:
                        
                        if self.GetCellBackgroundColour((SelectedY-y_idx), (15-x_idx) + (Sub_Depth)*17) != self.TempColour:
                            StartX = (15-x_idx)+1
                            StartY = (SelectedY-y_idx)
    
                            if StartX == 16:
                                StartX = 0
                                StartY = (SelectedY-y_idx) + 1
                        else:
                            StartX = (15-x_idx)
                            StartY = (SelectedY-y_idx)
                            
                        FindFlag = True
                        break
                if FindFlag == True:
                    break
            """
            print "StartY = " + str(StartY)
            print "StartX = " + str(StartX)
            print "SelectedY = " + str(SelectedY)
            print "SelectedX = " + str(SelectedX)
            print "Depth = " + str(Depth)
            """
            Query = self.GetCellValue(StartY, StartX + (Sub_Depth)*17) + "." + Query
        
        
        #Set Tree Focus
        def TreeTraverse(parent, Depth, Query):
            item, cookie = MainFrame.tree.GetFirstChild(parent)
                
            while item.IsOk():
                 
                ItemName = MainFrame.tree.GetItemText(item)
                
                DepthString = ItemName.split("-")[2].strip()
                Depth = int(DepthString.strip().replace("d", ""))
                
                
                if Query.split(".")[Depth] in MainFrame.tree.GetItemText(item):
                    #print Query
                    #print int(Depth)
                    #print MainFrame.tree.GetItemText(item)
                    
                    MainFrame.tree.SelectItem(item)
                    if MainFrame.tree.ItemHasChildren(item) :
                        MainFrame.tree.Expand(item)
                
                #print "MainFrame.tree.GetItemText(item) = " +  str(MainFrame.tree.GetItemText(item))
                #print "Query = " + Query
                #print "(Depth + 1) = " + str((Depth + 1))
                #print ""
                
                if MainFrame.tree.ItemHasChildren(item) and len(Query.split(".")) > (Depth + 1):
                    Depth = Depth + 1
                    TreeTraverse(item, Depth, Query)
                    
                item = MainFrame.tree.GetNextSibling(item)

        
        TreeTraverse(MainFrame.root, 0, Query)
        
        
        """
        item, cookie = MainFrame.tree.GetFirstChild(MainFrame.root)
        MainFrame.tree.SelectItem(item)
        MainFrame.tree.Expand(item)
        """
        
        
        #Query sending
        
        
        MainFrame.ValuePaneTree.SendQueryAndResultSet(self.TemplatePath, self.TargetPath, Query)
        
        
        return

class Enum(object):
    """ support class for enum
    """
    __names__ = None
    __items__ = None
    __special_names__ = []

    @classmethod
    def Name(cls, val):
        if cls.__names__ is None:
            cls.__names__ = dict([(getattr(cls, name), name) for name in dir(cls)
                                  if name and not name.startswith("_") and name not in cls.__special_names__ and
                                  not callable(getattr(cls, name))])

        return cls.__names__.get(val, val)

    @classmethod
    def Names(cls):
        return [name for name in dir(cls)
                if name and not name.startswith("_") and name not in cls.__special_names__ and
                not callable(getattr(cls, name))]

    @classmethod
    def Value(cls, name):
        items = cls.Items()
        if name not in items:
            raise AttributeError("No item '%s" % name)
        return items[name]

    @classmethod
    def Values(cls):
        return [getattr(cls, name) for name in dir(cls)
                if name and not name.startswith("_") and name not in cls.__special_names__ and
                not callable(getattr(cls, name))]

    @classmethod
    def Items(cls):
        if cls.__items__ is None:
            cls.__items__ = dict([(name, getattr(cls, name)) for name in dir(cls)
                                  if name and not name.startswith("_") and name not in cls.__special_names__ and
                                  not callable(getattr(cls, name))])
        return cls.__items__



class SEARCH_TYPES(Enum):
    Hexadecimal = "Hexadecimal"
    NormalText = "Normal Text"
    RegexText = "Regex Text"

class HexGridTable(wx.grid.PyGridTableBase):
    class Actions:
        EditCell = "EditCell"
        RemoveCells = "RemoveCells"
        InsertCells = "InsertCells"

    def __init__(self, binary, length=None, hex_cols=16):
        wx.grid.PyGridTableBase.__init__(self)

        if length is None:
            self.length = len(binary)
        else:
            self.length = length
        if self.length < 0:
            self.length = 0

        self.hex_cols = hex_cols
        self.cols_labels = ["%X" % i for i in range(self.hex_cols)] + ["        Dump       "]

        self.buffer = ctypes.create_string_buffer(self.length)
        ctypes.memmove(self.buffer, binary, self.length)

        self._string = None

        self._dump_cell_attr = wx.grid.GridCellAttr()
        self._dump_cell_attr.SetReadOnly(True)
        self._dump_cell_attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)

        self._alt_cell_attr = wx.grid.GridCellAttr()
        self._alt_cell_attr.SetBackgroundColour("#DDDDDD")
        self._page_row_attr = wx.grid.GridCellAttr()
        self._page_row_attr.SetBackgroundColour('#e6f1f5')
        self._range_attr = wx.grid.GridCellAttr()
        self._range_attr.SetBackgroundColour("#F2F5A9")
        self._changed_cell_attr = wx.grid.GridCellAttr()
        self._changed_cell_attr.SetBackgroundColour("#F2F5A9")
        self._changed_cell_attr.SetTextColour("red")

        self._changed_attr = {}

        self._changed_range = (-1, -1)
        self._undo_list = []
        self._redo_list = []

    @property
    def String(self):
        if self._string is None:
            self._string = ctypes.string_at(self.buffer, self.length)
        return self._string

    def _get_value_by_row_col(self, row, col, length=1):
        addr = row * self.hex_cols + col
        return self._get_value_by_addr(addr, length)

    def _get_value_by_addr(self, addr, length=1):
        end = addr + length
        if addr + length > self.length:
            end = self.length
        return self.buffer[addr:end]

    def _set_value_by_addr(self, addr, value):
        if addr > self.length:
            return False
        if addr == self.length:  # append one byte
            self.InsertRange(self.length, value)
        else:  # change one byte
            self.buffer[addr] = value
        self._string = None  # reset string
        return True

    def addr_to_row_col(self, addr):
        return addr / self.hex_cols, addr % self.hex_cols

    def row_col_to_addr(self, row, col):
        return row * self.hex_cols + col

    def _in_changed_range(self, addr):
        return self._changed_range[0] <= addr < self._changed_range[1]

    def Reset_Attr(self):
        self._changed_attr = {}

    def GetNumberCols(self):
        return self.hex_cols + 1

    def GetNumberRows(self):
        return (self.length + self.hex_cols) / self.hex_cols

    def GetColLabelValue(self, col):
        return self.cols_labels[col]

    def GetRowLabelValue(self, row):
        return "0x%X " % (row * self.hex_cols)

    def IsEmptyCell(self, row, col):
        addr = row * self.hex_cols + col
        if addr >= self.length:
            return True
        return False

    def GetAttr(self, row, col, kind=None):
        if col == self.hex_cols:  # disable cell editor for Dump col
            self._dump_cell_attr.IncRef()
            return self._dump_cell_attr
        addr = row * self.hex_cols + col

        if addr > self.length:  # disable cell editor for cells > length
            self._dump_cell_attr.IncRef()
            return self._dump_cell_attr

        if addr in self._changed_attr:  # return changed cells attr first
            attr = self._changed_attr[addr]
            if attr:
                attr.IncRef()
            return attr
        elif self._in_changed_range(addr):  # return range change attr
            self._range_attr.IncRef()
            return self._range_attr
        #elif row and not (row % 0x2):   # return pager attr
        #    self._page_row_attr.IncRef()
        #    return self._page_row_attr
        #elif col in [4, 5, 6, 7, 12, 13, 14, 15]:   # return range change attr
            #self._alt_cell_attr.IncRef()
            #return self._alt_cell_attr

        # return None for others

    def SetAttr(self, attr, row, col):
        addr = row * self.hex_cols + col
        if addr in self._changed_attr:   # decrease ref for saved attr
            old_attr = self._changed_attr[addr]
            if old_attr:
                old_attr.DecRef()
        self._changed_attr[addr] = attr  # save changed cell attr

    def GetValue(self, row, col):
        if col == self.hex_cols:  # dump col
            row_values = self._get_value_by_row_col(row, 0, 16)
            row_values = ["%c" % val if 0x20 <= ord(val) <= 0x7E else ". " for val in row_values if val]
            return "  " + "".join(row_values)
        else:
            val = self._get_value_by_row_col(row, col, 1)
            return val and "%02X" % ord(val)

    def SetValue(self, row, col, value):
        if col == self.hex_cols:
            pass
        else:
            addr = row * self.hex_cols + col
            value = chr(int(value, 16))

            attr = self.GetAttr(row, col)
            saved_val = self._get_value_by_addr(addr)

            in_range = addr < self.length  # add undo for addr < length

            if saved_val != value and self._set_value_by_addr(addr, value):
                self._changed_cell_attr.IncRef()
                self.SetAttr(self._changed_cell_attr, row, col)
                if in_range:
                    self._add_undo_action(self.Actions.EditCell, (addr, saved_val, attr))
                else:
                    if col == self.hex_cols - 1:
                        # this is the last row/col, append a row
                        msg = wxgrid.GridTableMessage(self,
                                                      wxgrid.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                                                      1)
                        self.GetView().ProcessTableMessage(msg)

    def SaveFile(self, output):
        """ output must be a file like object supports 'write' """
        output.write(ctypes.string_at(self.buffer, self.length))

    def GetBinary(self, start=0, length=None):
        if length is None:
            length = self.length
        if start + length > self.length:
            length = self.length - length
        return ctypes.string_at(ctypes.addressof(self.buffer) + start, length)

    def GetText(self, start=0, length=None):
        return binascii.b2a_hex(self.GetBinary(start, length)).upper()

    def InsertText(self, start, text):
        value = binascii.a2b_hex(text)
        self.InsertRange(start, value)

    def _delete_range(self, start, length):
        if start >= self.length:
            return ""
        self._changed_range = (-1, -1)

        deleted_data = ctypes.create_string_buffer(length)
        buf_addr = ctypes.addressof(self.buffer)
        if start + length > self.length:
            length = self.length - length
            ctypes.memmove(deleted_data, buf_addr + start, length)
            self.length -= length
        else:
            ctypes.memmove(deleted_data, buf_addr + start, length)
            ctypes.memmove(buf_addr + start, buf_addr + start + length, self.length - length - start)
            self.length -= length
            self.Reset_Attr()

        self._string = None  # reset string

        dispatcher.send("HexEditor.Changed", sender=self.GetView())

        return deleted_data

    def DeleteRange(self, start, length):
        deleted_data = self._delete_range(start, length)

        self._add_undo_action(self.Actions.RemoveCells, (start, length, deleted_data))

    def _insert_range(self, start, value):
        if start >= self.length:
            start = self.length

        length = len(value)
        new_buf = ctypes.create_string_buffer(self.length + length)
        new_buf_addr = ctypes.addressof(new_buf)

        old_addr = ctypes.addressof(self.buffer)

        self._changed_range = (start, start + length)

        ctypes.memmove(new_buf_addr, old_addr, start)  # copy range before insert point
        ctypes.memmove(new_buf_addr + start, value, length)  # copy insertion value
        # copy range after insert point
        ctypes.memmove(new_buf_addr + start + length, old_addr + start, self.length - start)

        self.buffer = new_buf
        self.length += length

        self.Reset_Attr()

        self._string = None  # reset string

        dispatcher.send("HexEditor.Changed", sender=self.GetView())

        return start

    def InsertRange(self, start, value):
        start = self._insert_range(start, value)

        self._add_undo_action(self.Actions.InsertCells, (start, value))

    def _add_undo_action(self, action, data):
        self._undo_list.append((action, data))
        if action == self.Actions.EditCell:
            return False
        return True

    def _add_redo_action(self, action, data):
        self._redo_list.append((action, data))
        if action == self.Actions.EditCell:
            return False
        return True

    def Undo(self):
        try:
            item = self._undo_list.pop()
            action, data = item
            action, data = self.Do(action, data)
            if action is False:
                return self._add_undo_action(*item)
            elif action is not None:
                return self._add_redo_action(action, data)
        except IndexError:
            return

    def Redo(self):
        try:
            item = self._redo_list.pop()
            action, data = item
            action, data = self.Do(action, data)
            if action is False:
                return self._add_redo_action(*item)
            if action is not None:
                return self._add_undo_action(action, data)
        except IndexError:
            return

    def Do(self, action, data):
        if action == self.Actions.EditCell:
            addr, value, attr = data
            row, col = self.addr_to_row_col(addr)
            saved_value = self._get_value_by_addr(addr)
            saved_attr = self.GetAttr(row, col)
            if self._set_value_by_addr(addr, value):
                self.SetAttr(attr, row, col)
                return  self.Actions.EditCell, (addr, saved_value, saved_attr)
            return False, False

        elif action == self.Actions.RemoveCells:
            start, length, deleted_data = data
            try:
                start = self._insert_range(start, deleted_data)
                return self.Actions.InsertCells, (start, deleted_data)
            except:
                return False, False

        elif action == self.Actions.InsertCells:
            start, deleted_data = data
            try:
                deleted_data = self._delete_range(start, len(deleted_data))
                return self.Actions.RemoveCells, (start, len(deleted_data), deleted_data)
            except:
                return False, False

        return None, None

    def FindIter(self, text, find_type=SEARCH_TYPES.Hexadecimal):
        """ return a iter """
        if find_type == SEARCH_TYPES.RegexText:
            regex = text
        elif find_type == SEARCH_TYPES.Hexadecimal:
            text = binascii.a2b_hex(text)
            regex = re.escape(text)
        elif find_type == SEARCH_TYPES.NormalText:
            regex = re.escape(text)
        else:
            raise Exception("unsupported search type")

        return self.FindRegex(regex)

    def FindRegex(self, regex):
        return re.finditer(regex, self.String)

    

class HexViewer(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    
    
    
    def __init__(self, parent, log):
        self.parent = parent
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None
        
        self.isSelectedBlockExist = False
        self.RowsThatIncludesSelectedData = []

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        #self.CreateGrid(MaxRow, 17)
        self.CreateGrid(300, 17)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        colour = wx.WHITE#'#e6f1f5'
        self.SetGridLineColour(colour)
        self.SetLabelBackgroundColour("#e2e8f0")
        
        
        self._grid_selecting_start = False
        self._in_selecting = False
        self._hex_cols = 16
        
        
        for idx in range(0,0x11):
            if idx < 10:
                self.SetColLabelValue(idx, str(idx))
            if idx == 10:
                self.SetColLabelValue(idx, 'A')
            if idx == 11:
                self.SetColLabelValue(idx, 'B')
            if idx == 12:
                self.SetColLabelValue(idx, 'C')
            if idx == 13:
                self.SetColLabelValue(idx, 'D')
            if idx == 14:
                self.SetColLabelValue(idx, 'E')
            if idx == 15:
                self.SetColLabelValue(idx, 'F')
            if idx == 16:
                self.SetColLabelValue(idx, 'Dump')
                self.SetColSize(idx, 140)
            if idx <= 15:
                self.SetColSize(idx, 30)
        
        
        # test all the events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.GetGridWindow().Bind(wx.EVT_LEFT_DOWN, self.OnGridLeftDown)
        self.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnGridLeftUp)
        self.GetGridWindow().Bind(wx.EVT_MOTION, self.OnGridLeftMotion)
        
    
        
        
    def ThreadFileLoad(self):
        #print "ThreadFileLoad, Target Path = " + self.TargetPath
        fp = open(self.TargetPath, 'rb')
        
        #fp.seek(Offset)
        HexValue = ''
        idx = 0
        length = os.path.getsize(self.TargetPath)
        readBuffer = fp.read(length) 
        #print readBuffer
        
        table = HexGridTable(readBuffer, length)
        self.BeginBatch()
        self.ClearGrid()
        self._grid_selecting_start = None
        self.SetTable(table)
        #table.AutoSize()
        size = self.parent.GetSize()
        for idx in range(0, 16):
            self.SetColSize(idx, (size.x-250)/16)
        self.SetColSize(16, 140)
        self.EndBatch()
        
        fp.close()
        
        """
        #while readBuffer:
        for Value in readBuffer:
            UpperValue = (ord(Value) & 0xF0) >> 4
            LowerValue = ord(Value) & 0x0F
            
            if UpperValue >= 0 and UpperValue <= 9:
                HexValue = str(UpperValue)
            elif UpperValue == 10:
                HexValue = 'A'
            elif UpperValue == 11:
                HexValue = 'B'
            elif UpperValue == 12:
                HexValue = 'C'
            elif UpperValue == 13:
                HexValue = 'D'
            elif UpperValue == 14:
                HexValue = 'E'
            elif UpperValue == 15:
                HexValue = 'F'
                
            if LowerValue >= 0 and LowerValue <= 9:
                HexValue += str(LowerValue)
            elif LowerValue == 10:
                HexValue += 'A'
            elif LowerValue == 11:
                HexValue += 'B'
            elif LowerValue == 12:
                HexValue += 'C'
            elif LowerValue == 13:
                HexValue += 'D'
            elif LowerValue == 14:
                HexValue += 'E'
            elif LowerValue == 15:
                HexValue += 'F'
                
            self.SetCellValue(idx/16, idx%16, HexValue)
            if idx%16 == 15:
                self.SetCellValue(idx/16, 16, ". . . . . . . . . . . . . . . .")
            if (idx/16) % 2 == 0:
                colour = '#e6f1f5'
                self.SetCellBackgroundColour(idx/16, idx%16, colour)
            idx += 1

        
            #readBuffer = fp.read(int(4096))
        """
    
    
    
        
        
    def OnSize(self, event):
        size = self.parent.GetSize()
        
        #for idx in range(0, 16):
        #    self.SetColSize(idx, (size.x-250)/16)
        #self.SetColSize(16, 140)
        event.Skip()
        
        
    def OnGridLeftDown(self, event):
        start_pos = self._client_to_scroll_pos(event.X, event.Y)
        self._grid_selecting_start = self.XYToCell(*start_pos)
        event.Skip()

    def OnGridLeftUp(self, event):
        event.Skip()
        wx.CallAfter(self._set_selection, callback=self._reset_grid_selecting)

    def OnGridLeftMotion(self, event):
        if not self._in_selecting and self._grid_selecting_start:
            end_pos = self._client_to_scroll_pos(event.X, event.Y)
            end_pos = self.XYToCell(*end_pos)
            if end_pos != (-1, -1):
                wx.CallAfter(self._set_selection, end_pos=end_pos)
                
                
                
                
    def RowColToAddr(self, row, col, check_max=True):
        col = self._hex_cols - 1 if col >= self._hex_cols else col
        #print row, self._hex_cols, col
        addr = row * self._hex_cols + col
        if check_max:
            addr = self._check_addr_in_range(addr)
        return addr
    
    def Length(self):
        return self.GetTable().length

    def HexCols(self):
        return self._hex_cols

    def _reset_grid_selecting(self):
        self._grid_selecting_start = None
    
    def _client_to_scroll_pos(self, x, y):
        ppunit = self.GetScrollPixelsPerUnit()
        scroll_x = self.GetScrollPos(wx.HORIZONTAL)
        scroll_y = self.GetScrollPos(wx.VERTICAL)
        x += scroll_x * ppunit[0]
        y += scroll_y * ppunit[1]
        return x, y
    
    def _set_selection(self, end_pos=None, callback=None):
        self._in_selecting = True
        if end_pos and self._grid_selecting_start:
            cur_row, cur_col = self._grid_selecting_start
            end_row, end_col = end_pos

            if cur_col == self.HexCols:
                if cur_row > end_row:
                    cur_row, end_row = end_row, cur_row
                min_addr = self.RowColToAddr(cur_row, 0)
                max_addr = self.RowColToAddr(end_row, self.HexCols - 1)
                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
            else:
                if end_col == self.HexCols:
                    end_col -= 1
                if (cur_row, cur_col) == (end_row, end_col):
                    min_addr = max_addr = self.RowColToAddr(cur_row, cur_col, False)
                    if min_addr > self.Length:
                        min_addr = max_addr = self.Length
                else:
                    min_addr = self.RowColToAddr(cur_row, cur_col)
                    max_addr = self.RowColToAddr(end_row, end_col)
                    if min_addr > max_addr:
                        min_addr, max_addr = max_addr, min_addr

                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
        else:
            rows = self.GetSelectedRows()
            if rows:
                min_row = min(rows)
                max_row = max(rows)
                self.SetGridCursor(min_row, 0)
                self.ClearSelection()
                min_addr = self.RowColToAddr(min_row, 0)
                max_addr = self.RowColToAddr(max_row, self.HexCols - 1)
                self.SetSelection(min_addr, max_addr - min_addr + 1, False)
            else:
                top_left = self.GetSelectionBlockTopLeft()
                bottom_right = self.GetSelectionBlockBottomRight()
                cells = self.GetSelectedCells()

                addrs = [self.RowColToAddr(row, col) for (row, col) in top_left + bottom_right + cells]
                if addrs:
                    min_addr = min(addrs)
                    max_addr = max(addrs)
                    self.SetSelection(min_addr, max_addr - min_addr + 1, False)
                #else:
                    #self._update_status(sel=1)

        self._in_selecting = False
        if callable(callback):
            callback()
        #self.grid.Refresh()

    def SetSelection(self, addr, length=1, jumpto=False):
        row, col = self.AddrToRowCol(addr)
        end_row, end_col = self.AddrToRowCol(addr + length - 1)

        self.Freeze()
        self.BeginBatch()
        self.SetGridCursor(row, col)
        if length > 0:
            # in same row
            if row == end_row:
                self.SelectBlock(row, col, end_row, end_col)
            elif end_row > row:
                #first row
                self.SelectBlock(row, col, row, self._hex_cols - 1)
                if end_row - row > 1:
                    self.SelectBlock(row + 1, 0, end_row - 1, self._hex_cols - 1, addToSelected=True)
                #last row
                self.SelectBlock(end_row, 0, end_row, end_col, addToSelected=True)
        self.EndBatch()
        self.Thaw()
        #self._update_status(sel=length)
        if jumpto:
            self.JumpTo(row, col)

    def AddrToRowCol(self, addr):
        return addr / self._hex_cols, addr % self._hex_cols


    def RowColToAddr(self, row, col, check_max=True):
        col = self._hex_cols - 1 if col >= self._hex_cols else col
        addr = row * self._hex_cols + col
        if check_max:
            addr = self._check_addr_in_range(addr)
        return addr


    def _check_addr_in_range(self, addr):
        addr = addr if addr > 0 else 0
        addr = addr if addr < self.Length else self.Length - 1
        return addr



    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()



class EditorPane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.parent = parent
        
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        
        panel1 = wx.Panel(self, -1, style=wx.NO_BORDER)
        self.TemplateViewerGrid = TemplateViewer(panel1, sys.stdout)
        self.TemplateViewerGrid.SetName('TemplateViewer')
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(self.TemplateViewerGrid, 1, wx.EXPAND)
        panel1.SetSizer(vbox0)
        
        
        
        self.TextCtrl1 = wx.TextCtrl(self)
        
        
        # add the windows to the splitter and split it.
        
        leftBox.Add(panel1, 1, wx.EXPAND)
        leftBox.Add(self.TextCtrl1, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(leftBox)
        
        
        

#----
#---Bottom Panes------------------------------------------------------------------------
class ValueOfDataBlockTree(gizmos.TreeListCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style =    wx.TR_DEFAULT_STYLE
                            #| wx.TR_HAS_BUTTONS
                            #| wx.TR_TWIST_BUTTONS
                            | wx.TR_ROW_LINES
                            #| wx.TR_COLUMN_LINES
                            #| wx.TR_NO_LINES 
                            | wx.TR_FULL_ROW_HIGHLIGHT,
                 log=None):

        gizmos.TreeListCtrl.__init__(self, parent, id, pos, size, style)
        
        self.parent = parent
        
        self.MainFrame = self.parent.GetParent()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnLeftDClick)
        
        
        self.SelectedHexOffset = 0
        self.SelectedHexLength = 0
        self.SelectedBlock_OriginalBackgroundColor = '#ffffff'
        self.SelectedBlock_OriginalTextColor = '#ffffff'
        self.isSelectedBlockExist = False
        

        treestyles = []
        events = []

        self.events = events
        self.styles = treestyles
        self.item = None
        
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider_GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        if os.path.isfile('pfp_sdk/icons/bitmaps/aquanotflagged.ico'):
            self.folder_close_idx = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            self.folder_open_idx = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotchecked.ico'))
        else:
            self.folder_close_idx = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            self.folder_open_idx = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotchecked.ico'))
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        
        # create some columns
        self.AddColumn("Data block name")
        self.AddColumn("Value")
        self.AddColumn("Hex value")
        self.AddColumn("File offset")
        self.AddColumn("Data length")
        self.SetMainColumn(0) # the one with the tree in it...
        
        size = self.parent.GetSize()
        
        self.SetColumnWidth(0, 250)
        self.SetColumnWidth(1, 200)
        self.SetColumnWidth(2, 200)
        self.SetColumnWidth(3, 100)
        self.SetColumnWidth(4, size.x-5-250-250-100-100)
        
        
    def OnLeftDClick(self, event):
        
        #print "aaa"
        
        MainFrame = self.GetParent().GetParent()

        
        #recover original selected block
        if self.isSelectedBlockExist == True:
            
            #fill the related data
            FillLength = 0
            if int(self.SelectedHexLength) > 5000:
                FillLength = 5000
            else:
                FillLength = int(self.SelectedHexLength)
            
            for idx in range(0, FillLength):
                offset = int(self.SelectedHexOffset) + idx
                HexY = offset/16
                HexX = offset%16
    
            
                MainFrame.list1.SetCellBackgroundColour(HexY, HexX, self.SelectedBlock_OriginalBackgroundColor) #"#dce6f1"
                MainFrame.list1.SetCellTextColour(HexY, HexX, self.SelectedBlock_OriginalTextColor)
                        
                Name = MainFrame.list1.GetCellValue(HexY, HexX)
                MainFrame.list1.SetCellValue(HexY, HexX, Name)
            
            
            
        #Fill the black to new selected block       
        Length = int(self.GetItemText(event.Item, 4))
        Start_Offset = int(self.GetItemText(event.Item, 3))
        
        
        
        self.SelectedHexOffset = Start_Offset
        self.SelectedHexLength = Length
        self.SelectedBlock_OriginalBackgroundColor = MainFrame.list1.GetCellBackgroundColour(Start_Offset/16, Start_Offset%16)
        self.SelectedBlock_OriginalTextColor = MainFrame.list1.GetCellTextColour(Start_Offset/16, Start_Offset%16)
        self.isSelectedBlockExist = True
        
        
        #fill the related data
        FillLength = 0
        if int(Length) > 5000:
            FillLength = 5000
        else:
            FillLength = int(Length)
        for idx in range(0, int(FillLength)):
            offset = int(Start_Offset) + idx
            HexY = offset/16
            HexX = offset%16

        
            MainFrame.list1.SetCellBackgroundColour(HexY, HexX, "#f6dcf6") #"#dce6f1"
            MainFrame.list1.SetCellTextColour(HexY, HexX, "#808080")
                    
            Name = MainFrame.list1.GetCellValue(HexY, HexX)
            MainFrame.list1.SetCellValue(HexY, HexX, Name)

                
        
        #Set focus 
        MainFrame.list1.SetGridCursor(Start_Offset/16, Start_Offset%16)
        MainFrame.list1.MakeCellVisible(Start_Offset/16, Start_Offset%16)
        
        return

        
        
    def OnSize(self, event):
        #size = self.parent.GetSize()
        #self.SetColumnWidth(0, 250)
        #self.SetColumnWidth(1, 200)
        #self.SetColumnWidth(2, 200)
        #self.SetColumnWidth(3, 100)
        #self.SetColumnWidth(4, size.x-5-250-250-100-100)
        event.Skip()
        


    def SendQueryAndResultSet(self, TemplatePath, TargetPath, Query):
        
        
        MainFrame = self.GetParent().GetParent()
        self.SelectedHexOffset = 0
        self.SelectedHexLength = 0
        self.SelectedBlock_OriginalBackgroundColor = '#ffffff'
        self.SelectedBlock_OriginalTextColor = '#ffffff'
        self.isSelectedBlockExist = False
        
        if MainFrame.list1.isSelectedBlockExist == True:
            
            #print MainFrame.list1.RowsThatIncludesSelectedData
            for Rowidx in MainFrame.list1.RowsThatIncludesSelectedData:
                colour = '#ffffff'
                #if Rowidx % 2 == 0:
                #    colour = '#e6f1f5'
                
                #print colour
                
                for jdx in range(0, 16):
                    MainFrame.list1.SetCellBackgroundColour(Rowidx, jdx, colour)
                    MainFrame.list1.SetCellTextColour(Rowidx, jdx, '#000000')
                    Name = MainFrame.list1.GetCellValue(Rowidx, jdx)
                    MainFrame.list1.SetCellValue(Rowidx, jdx, Name)
        
        
        
        

        
        QueryResult = MainFrame.PE.QueryInterpreter(Query, TargetPath) #v2
            #[0] = Block Name 
            #[1] = "Value", "Group", "Array", "List
            #[2] =    if "Value",     QueryResult
            #[2] =    if "Group",     SubBlockNames... [~, ~, ~]
            #[2] =    if "Array",     ReturnQuery... [~[0], ~[1], ~[2]]
            #[2] =    if "List",      ReturnQuery... [~<0>, ~<1>, ~<2>]
        
        def SetResult(QueryResult, Query):
        
            ResultSet = []
            #[0]    : ???
            #[1]    : ??
            #[1]    : ??? 
        
            ResultSet.append(Query)     #QueryResult[0])
            ResultSet.append(QueryResult[1])
            
            if QueryResult[1] == "Value":
                ResultSet.append(QueryResult)
                
            elif QueryResult[1] == "Group" or QueryResult[1] == "Array" or QueryResult[1] == "List":
                SubSet = []
                for SubBlockName_or_SubQuery in QueryResult[2]:
                    
                    SubQuery = ""
                    if QueryResult[1] == "Group" :                                  SubQuery = Query+"."+SubBlockName_or_SubQuery
                    elif QueryResult[1] == "Array" or QueryResult[1] == "List" :    SubQuery = SubBlockName_or_SubQuery
                    SubResult = MainFrame.PE.QueryInterpreter(SubQuery, TargetPath)
                
                    SubResultList = SetResult(SubResult, SubQuery)
                    SubSet.append(SubResultList)
                
                ResultSet.append(SubSet)
                
            return ResultSet
        
        ResultList = SetResult(QueryResult, Query)
        #---결과 출력 주석 있음
        #print "ResultList = " + str(ResultList)
          
        self.DeleteAllItems()
        
        self.AlreadyGetStartFlag = False
        self.FocusY = 0
        self.FocusX = 0
        
                    
        
        self.root = self.AddRoot(Query)
        self.SetItemText(self.root, "", 1)
        self.SetItemText(self.root, "", 2)
        self.SetItemImage(self.root, self.folder_close_idx, which = wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.folder_open_idx, which = wx.TreeItemIcon_Expanded)
        
        
        self.TreeInsert(ResultList, self.root)
        
        
        #Set focus 
        MainFrame.list1.SetGridCursor(self.FocusY, self.FocusX)
        MainFrame.list1.MakeCellVisible(self.FocusY, self.FocusX)
        
        self.Expand(self.root)
        
        MainFrame.page1.TextCtrl1.Clear()
        MainFrame.page1.TextCtrl1.WriteText('"' + Query + '" , "' + TargetPath + '" , "' + TemplatePath + '"')
        
        
    def TreeInsert(self, List, parent):
                
        dummyStr = ""
        dummyList = []
        if List[1] == "Group" or List[1] == "Array" or List[1] == "List":
            child = self.AppendItem(parent, str(List[0]))
            self.SetItemText(child, List[1], 1)
            self.SetItemText(child, "-", 2)
            self.SetItemText(child, "-", 3)
            self.SetItemText(child, "-", 4)
            
            for element in List[2]:
                self.TreeInsert(element, child)
                
            self.SetItemImage(child, self.folder_close_idx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.folder_open_idx, which = wx.TreeItemIcon_Expanded)
            self.Expand(child)
            

        elif List[1] == "Value":
            child = self.AppendItem(parent, str(List[0]))
            
            self.SetItemText(child, str(List[2][2]), 1)
            self.SetItemText(child, str(List[2][5]), 2)
            self.SetItemText(child, str(List[2][3]), 3)
            self.SetItemText(child, str(List[2][4]), 4)
            
            self.Fill_Hex_Block(List[2][3], List[2][4])

            
            self.SetItemImage(child, self.folder_close_idx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.folder_open_idx, which = wx.TreeItemIcon_Expanded)
            self.Expand(child)
            
    def Fill_Hex_Block(self, Offset, Length): 
        
        MainFrame = self.GetParent().GetParent()
        #fill the related data
        FillLength = 0
        #print element[3]
        if int(Length) > 5000:
            FillLength = 5000
        else:
            FillLength = int(Length)
        for idx in range(0, FillLength):
            offset = int(Offset) + idx
            HexY = offset/16
            HexX = offset%16
            
            if self.AlreadyGetStartFlag == False:
                self.FocusY = int(Offset)/16
                self.FocusX = int(Offset)%16
                self.AlreadyGetStartFlag = True

        
            MainFrame.list1.SetCellBackgroundColour(HexY, HexX, "#000000") #"#dce6f1"
            MainFrame.list1.SetCellTextColour(HexY, HexX, "#ffffff")
                    
            Name = MainFrame.list1.GetCellValue(HexY, HexX)
            MainFrame.list1.SetCellValue(HexY, HexX, Name)
            
            if HexY not in MainFrame.list1.RowsThatIncludesSelectedData:
                MainFrame.list1.RowsThatIncludesSelectedData.append(HexY)
                
            MainFrame.list1.isSelectedBlockExist = True
        
    

        
#----
#---Left Panes------------------------------------------------------------------------
class TemplateStructureTree(ExpansionState, TreeBaseClass):
    def __init__(self, parent):
        TreeBaseClass.__init__(self, parent, style=wx.TR_DEFAULT_STYLE|
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.BuildTreeImageList()
        
        
        
        self._treeList =[]
        self.TemplatePath = "pfp_sdk/struct_template/template_pe.xls"
        self.TargetPath = "pfp_sdk/struct_template/test_target.exe"
        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        
        
        
    def OnLeftDClick(self, event):
        
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        
        ItemName = self.GetItemText(item)
        MainFrame = self.GetParent().GetParent().GetParent()
        
        
        BlockName = ItemName.split("-")[0].strip()
        PositionString = ItemName.split("-")[1].strip()
        DepthString = ItemName.split("-")[2].strip()
        Depth = int(DepthString.strip().replace("d", ""))
        StartPosition = PositionString.split("/")[0]
        EndPosition = PositionString.split("/")[1]
        
        StartX = int(StartPosition.replace("(","").replace(")","").split(",")[0])
        StartY = int(StartPosition.replace("(","").replace(")","").split(",")[1])
        
        EndX = int(EndPosition.replace("(","").replace(")","").split(",")[0])
        EndY = int(EndPosition.replace("(","").replace(")","").split(",")[1])
        
        
        Query = BlockName
        child = item
        for idx in range(0, Depth):
            parent = self.GetItemParent(child)
            ParentName = self.GetItemText(parent)
            Query = ParentName.split("-")[0].strip() + "." + Query
            child = parent
        
        #print Query    
        #print ItemName   
        
        MainFrame.nb.SetSelection(0) 
        TemplateGridPage = MainFrame.nb.GetPage(0)
        
        
        if EndX == 0:
            TemplateGridPage.TemplateViewerGrid.SetGridCursor(EndY-1, 15 + Depth*17)
            TemplateGridPage.TemplateViewerGrid.MakeCellVisible(EndY-1, 15 + Depth*17)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(StartY, StartX + Depth*17, StartY, StartX + Depth*17)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(StartY, StartX + Depth*17, EndY-1, 15 + Depth*17)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(0, 0 + Depth*17, 1, 1 + Depth*17-1)
        else:
            TemplateGridPage.TemplateViewerGrid.SetGridCursor(EndY, EndX + Depth*17)
            TemplateGridPage.TemplateViewerGrid.MakeCellVisible(EndY, EndX + Depth*17)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(StartY, StartX + Depth*17, StartY, StartX + Depth*17)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(StartY, StartX + Depth*17, EndY, EndX + Depth*17-1)
            #TemplateGridPage.TemplateViewerGrid.SelectBlock(0, 0 + Depth*17, 1, 1 + Depth*17-1)



        
        #recover original selected block
        if TemplateGridPage.TemplateViewerGrid.isSelectedBlockExist == True:
            
            for y_idx in range(TemplateGridPage.TemplateViewerGrid.SelectedBlock_StartY, TemplateGridPage.TemplateViewerGrid.SelectedBlock_EndY+1):
                for x_idx in range(0, 16):
                    if y_idx == TemplateGridPage.TemplateViewerGrid.SelectedBlock_StartY and x_idx < TemplateGridPage.TemplateViewerGrid.SelectedBlock_StartX :
                        continue
                    if y_idx == TemplateGridPage.TemplateViewerGrid.SelectedBlock_EndY and x_idx >= TemplateGridPage.TemplateViewerGrid.SelectedBlock_EndX :
                        break
                    
                    TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalDepth*17, TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalColor) #"#dce6f1"
                    TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalDepth*17, "#000000")
                                
                    #if y_idx != StartY and x_idx != StartX:
                    Name = TemplateGridPage.TemplateViewerGrid.GetCellValue(y_idx, x_idx + TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalDepth*17)
                    TemplateGridPage.TemplateViewerGrid.SetCellValue(y_idx, x_idx + TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalDepth*17, Name)
        
        
        
        
        #Fill the black to new selected block
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_StartX = StartX
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_StartY = StartY
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_EndX = EndX
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_EndY = EndY
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalColor = TemplateGridPage.TemplateViewerGrid.GetCellBackgroundColour(StartY, StartX + Depth*17)
        TemplateGridPage.TemplateViewerGrid.isSelectedBlockExist = True
        TemplateGridPage.TemplateViewerGrid.SelectedBlock_OriginalDepth = Depth
        
        for y_idx in range(StartY, EndY+1):
            for x_idx in range(0, 16):
                if y_idx == StartY and x_idx < StartX :
                    continue
                if y_idx == EndY and x_idx >= EndX :
                    break
                
                TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#000000") #"#dce6f1"
                TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#ffffff")
                            
                #if y_idx != StartY and x_idx != StartX:
                Name = TemplateGridPage.TemplateViewerGrid.GetCellValue(y_idx, x_idx + Depth*17)
                TemplateGridPage.TemplateViewerGrid.SetCellValue(y_idx, x_idx + Depth*17, Name)
        
        
        MainFrame.ValuePaneTree.SendQueryAndResultSet(self.TemplatePath, self.TargetPath, Query)


    def AppendItem(self, parent, text, image=-1, wnd=None):
        
        item = TreeBaseClass.AppendItem(self, parent, text, image=image)
        return item
            
    def BuildTreeImageList(self):
        il = wx.ImageList(16, 16)
        if os.path.isfile('pfp_sdk/icons/bitmaps/aquanotflagged.ico'):
            idx1 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx2 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx3 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx4 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx5 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
        else:
            idx1 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx2 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx3 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx4 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx5 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))


        self.AssignImageList(il)


    def GetItemIdentity(self, item):
        return self.GetPyData(item)


    def OpenTemplateFile(self):
        
        self.AddingStatic0BlockCount = 0
        self.AddingVariable0BlockCount = 0
        self.AddingStatic1BlockCount = 0
        self.AddingVariable1BlockCount = 0
        self.AddingStatic2BlockCount = 0
        self.AddingVariable2BlockCount = 0
        self.AddingStatic3BlockCount = 0
        self.AddingVariable3BlockCount = 0
        self.MainDepth_idx_x = 4
        self.Depth_interval = 18
        self.Start_y_idx = 4
        self.EOF_y_idx = 0
        self.sublist = []
        
        workbook = open_workbook(self.TemplatePath, formatting_info=True)
        sheet = workbook.sheet_by_index(0)
        rows, cols = sheet.nrows, sheet.ncols


        for y_idx in range(self.Start_y_idx, rows):
            if "EOF" == sheet.cell_value(y_idx, 4).strip():
                self.EOF_y_idx = y_idx
                break;
            
        if self.EOF_y_idx == 0 :
            wx.MessageBox("invalid template file.")
            #print "invalid template file."
            return
        
        
        
        def TemplateLoad(StartX, StartY, EndX, EndY, Depth): 
            list = []
            #print str(StartY + self.Start_y_idx) + "~" + str(EndY + self.Start_y_idx)
            #print str(self.MainDepth_idx_x + (self.Depth_interval*Depth)) + "~" + str(self.MainDepth_idx_x + (self.Depth_interval*self.Depth)+16)
            
            
            for y_idx in range( StartY + self.Start_y_idx, EndY + self.Start_y_idx + 1):
                for x_idx in range(4 + (18*Depth), 4 + (18*Depth)+16):
                    
                    if StartY + self.Start_y_idx == y_idx  and x_idx < StartX + 4 + (18*Depth) :
                        continue
                    if EndY + self.Start_y_idx == y_idx and x_idx >= EndX + 4 + (18*Depth):
                        break
                    
                    
                    
                    if sheet.cell_value(y_idx, x_idx).strip() != "" and sheet.cell_value(y_idx, x_idx).strip() != "EOB"  and sheet.cell_value(y_idx, x_idx).strip() != "EOF":
                        isVar = "static"
                        isArray = "None"
                        if "<listoffset:" in sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().lower():
                            BlockName = sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().split("<")[0] + "<list>"
                        elif "[array" in sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().lower():
                            BlockName = sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().split("[")[0] + "[arr]"
                        elif "<consecutivestart:" in sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().lower():
                            BlockName = sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().split("<")[0] + "<consecutive>"
                        else:
                            BlockName = sheet.cell_value(y_idx, x_idx).strip().split("(")[0].strip().split("[")[0]
                        
                        
                        
                        if len(sheet.cell_value(y_idx, x_idx).strip().split("(")[1].split(",")) >= 3:
                            isVar = "variable"
                            
                        Sub_StartX = x_idx - (self.MainDepth_idx_x + (self.Depth_interval*Depth))
                        Sub_StartY = y_idx - self.Start_y_idx
                        Sub_EndX = 0
                        Sub_EndY = 0
                        
                        FindFlag = False
                        for sub_y_idx in range( Sub_StartY + self.Start_y_idx, EndY + self.Start_y_idx + 1):
                            for sub_x_idx in range(4 + 18*Depth, 4 + 18*Depth + 16):
                        
                                if "" != sheet.cell_value(sub_y_idx, sub_x_idx).strip() and ((Sub_StartY + self.Start_y_idx) * 16) + (Sub_StartX + 4 + (18*Depth)) < (sub_y_idx * 16) + sub_x_idx:
                                    Sub_EndX = sub_x_idx - (4 + 18*Depth)
                                    Sub_EndY = sub_y_idx - self.Start_y_idx
                                    
                                    FindFlag = True
                                    
                                    break
                                
                            if FindFlag == True:
                                break
                        
                        
                        BlockName += " - (" + str(Sub_StartX) + "," +  str(Sub_StartY) + ")/(" + str(Sub_EndX) + "," +  str(Sub_EndY) + ") - d" + str(Depth) + " - " + isVar
                        #try:
                        #print BlockName
                        DataType = sheet.cell_value(y_idx, x_idx).strip().split(",")[1].strip().replace("(","")
                        
                        sublist = []
                        if  "group" in DataType.lower() :
                            sublist = TemplateLoad(Sub_StartX, Sub_StartY, Sub_EndX, Sub_EndY, Depth+1)               
                            
                                          
                        list.append([BlockName,sublist])
            
            return list

        StartX = 0
        StartY = 0
        EndX = 16
        EndY = self.EOF_y_idx - self.Start_y_idx
        list = []
        list = TemplateLoad(StartX, StartY, EndX, EndY, 0)
        
        #print list
        self._treeList = []
        for element in list:
            self._treeList.append(element)
                        
        

#---------------------------------------------------------------------------

class Main_Frame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size = (1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.SetMinSize((640,480))
        
        #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        #exit
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)


        pnl = wx.Panel(self)
        self.pnl = pnl
        
        
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)


        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        #self.PE = ParsingEngine()
        self.PE = ParsingEngine_v2()
        

        # Create a Notebook
        self.nb = wx.Notebook(pnl, -1, style=wx.CLIP_CHILDREN)
        il = wx.ImageList(16, 16)
        if os.path.isfile('pfp_sdk/icons/bitmaps/aquanotflagged.ico'):
            idx1 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx2 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx3 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx4 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx5 = il.Add(bitmap=wx.Bitmap('pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
        else:
            idx1 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx2 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx3 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx4 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
            idx5 = il.Add(bitmap=wx.Bitmap(PyFileLocation+'pfp_sdk/icons/bitmaps/aquanotflagged.ico'))
        self.nb.AssignImageList(il)
        
        
        ico = wx.Icon('PFPModule/PFPLib/InternalModules/pfp_sdk/icons/tray_f1.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        

        # Create a TreeCtrl
        leftPanel = wx.Panel(pnl, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        self.treeMap = {}
        self.searchItems = {}
        
        self.tree = TemplateStructureTree(leftPanel)
        
        self.filter = wx.SearchCtrl(leftPanel, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancelBtn)
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Sample Name")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Sample Content")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)
        
        


            
        
        self.BuildMenuBar()
        
        #here!!! crash!!!!
        self.page1 = EditorPane(self.nb)
        self.nb.AddPage(self.page1, "Structure(Map) view", imageId=0)

        
        # Set up a log window
        self.ValuePaneTree = ValueOfDataBlockTree(pnl, -1)# | CT.TR_HIDE_ROOT)   
        self.ValuePaneTree.SetBackgroundColour('WHITE')
        

        
        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.tree, 1, wx.EXPAND)
        leftBox.Add(wx.StaticText(leftPanel, label = "Filter:"), 0, wx.TOP|wx.LEFT, 5)
        leftBox.Add(self.filter, 0, wx.EXPAND|wx.ALL, 5)
        leftPanel.SetSizer(leftBox)

        
        # Use the aui manager to set up everything
        self.mgr.AddPane(self.nb, wx.aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(leftPanel,
                         wx.aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((300, -1)).
                         MinSize((300, -1)).
                         Floatable(ALLOW_AUI_FLOATING).FloatingSize((240, 700)).
                         Caption("Structure(Tree) view").
                         CloseButton(False).
                         Name("LeftTree"))
        self.mgr.AddPane(self.ValuePaneTree,
                         wx.aui.AuiPaneInfo().
                         Bottom().BestSize((-1, 200)).
                         MinSize((-1, 200)).
                         Floatable(False).FloatingSize((500, 160)).
                         Caption("Values of data block").
                         CloseButton(False).
                         Name("BottomTree"))
        
        
        
        panel2 = wx.Panel(pnl, -1, size=(25, -1), style=wx.NO_BORDER)
        self.list1 = HexViewer(panel2, sys.stdout)
        self.list1.SetName('Statusbar')
        vbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1.Add(self.list1, 1, wx.EXPAND)
        panel2.SetSizer(vbox1)
        
        
        self.mgr.AddPane(panel2, wx.aui.AuiPaneInfo().Right().Layer(2).Caption("Hex View").
                         MinSize((650, -1)).
                         Floatable(ALLOW_AUI_FLOATING).FloatingSize((240, 650)).
                         CloseButton(False).
                         Name("HexViewer"))
        
        

        self.mgr.Update()

        self.page1.TextCtrl1.WriteText("Query information")
        self.page1.TextCtrl1.SetEditable(False)

        #print sys.argv
        if len(sys.argv) >= 2:
            if os.path.isfile(str(sys.argv[1])) == True:
                
                self.OnFileOpen(None, str(sys.argv[1]))
            else:
                self.OnFileOpen(None)
        else:
            self.OnFileOpen(None)
        
            
            
    def TemplateClear(self):
        
        TemplateGridPage = self.page1
        
        TemplateGridPage.TemplateViewerGrid.ClearGrid() 
        
        for y_idx in range(0, 100):
            for x_idx in range(0, 17*5):
                TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx, "#ffffff") #"#dce6f1"                    
                #TemplateGridPage.TemplateViewerGrid.SetCellValue(y_idx, x_idx, "")
        

    def SetTemplateView(self, TremItemName):
        
        TemplateGridPage = self.page1
        ItemName = TremItemName
        #print ItemName
        
        BlockName = ItemName.split("-")[0].strip()
        PositionString = ItemName.split("-")[1].strip()
        DepthString = ItemName.split("-")[2].strip()
        isVariable = ItemName.split("-")[3].strip()
        Depth = int(DepthString.strip().replace("d", ""))
        StartPosition = PositionString.split("/")[0]
        EndPosition = PositionString.split("/")[1]
        
        StartX = int(StartPosition.replace("(","").replace(")","").split(",")[0])
        StartY = int(StartPosition.replace("(","").replace(")","").split(",")[1])
        
        EndX = int(EndPosition.replace("(","").replace(")","").split(",")[0])
        EndY = int(EndPosition.replace("(","").replace(")","").split(",")[1])
        
        TemplateGridPage.TemplateViewerGrid.SetCellValue(StartY, StartX + Depth*17, BlockName)
        TemplateGridPage.TemplateViewerGrid.SetReadOnly(StartY, StartX + Depth*17)
        TemplateGridPage.TemplateViewerGrid.EnableEditing(False)
        
        for y_idx in range(StartY, EndY+1):
            for x_idx in range(0, 16):
                if y_idx == StartY and x_idx < StartX :
                    continue
                if y_idx == EndY and x_idx >= EndX :
                    break
                #print "(" + str(x_idx) + "," + str(y_idx) + ")"
                #TemplateGridPage.TemplateViewerGrid.SetCellFont(y_idx, x_idx, wx.Font(10, wx.ROMAN, wx.ITALIC, wx.BOLD))
                """
                if self.tree.AddingBlockCount % 4 == 3:
                    TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx, "#c5d9f1") #"#"
                    TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx, "#000000")
                el
                """
                if  "var" in isVariable.lower():
                    if Depth == 0:
                        if self.tree.AddingVariable0BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#F8CBAD") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else:    
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#fce4d6") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif  Depth == 1:
                        if self.tree.AddingVariable1BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#F8CBAD") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else:    
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#fce4d6") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif  Depth == 2:
                        if self.tree.AddingVariable2BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#F8CBAD") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else:    
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#fce4d6") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif  Depth == 3:
                        if self.tree.AddingVariable3BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#F8CBAD") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else:    
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#fce4d6") #"#dce6f1"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    
                else:
                    if Depth == 0:
                        if self.tree.AddingStatic0BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#c5d9f1") #"#f2dcdb"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else :
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#dce6f1") #"#fde9d9"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif Depth == 1:
                        if self.tree.AddingStatic1BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#c5d9f1") #"#f2dcdb"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else :
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#dce6f1") #"#fde9d9"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif Depth == 2:
                        if self.tree.AddingStatic2BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#c5d9f1") #"#f2dcdb"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else :
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#dce6f1") #"#fde9d9"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    elif Depth == 3:
                        if self.tree.AddingStatic3BlockCount % 2 == 1:
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#c5d9f1") #"#f2dcdb"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                        else :
                            TemplateGridPage.TemplateViewerGrid.SetCellBackgroundColour(y_idx, x_idx + Depth*17, "#dce6f1") #"#fde9d9"
                            TemplateGridPage.TemplateViewerGrid.SetCellTextColour(y_idx, x_idx + Depth*17, "#000000")
                    
                    
                    
                    
                if y_idx != StartY and x_idx != StartX:
                    TemplateGridPage.TemplateViewerGrid.SetCellValue(y_idx, x_idx + Depth*17, " ")
                    TemplateGridPage.TemplateViewerGrid.SetCellValue(y_idx, x_idx + Depth*17, "")
        
        if  "var" in isVariable.lower():
            if Depth == 0:
                self.tree.AddingVariable0BlockCount += 1
            if Depth == 1:
                self.tree.AddingVariable1BlockCount += 1
            if Depth == 2:
                self.tree.AddingVariable2BlockCount += 1
            if Depth == 3:
                self.tree.AddingVariable3BlockCount += 1 
        else:
            if Depth == 0:
                self.tree.AddingStatic0BlockCount += 1
            if Depth == 1:
                self.tree.AddingStatic1BlockCount += 1
            if Depth == 2:
                self.tree.AddingStatic2BlockCount += 1
            if Depth == 3:
                self.tree.AddingStatic3BlockCount += 1
        

    """
    def ReadConfigurationFile(self):

        self.auiConfigurations = {}
        self.expansionState = [0, 1]

        config = GetConfig()
        val = config.Read('ExpansionState')
        if val:
            self.expansionState = eval(val)

        val = config.Read('AUIPerspectives')
        if val:
            self.auiConfigurations = eval(val)
    """

    def BuildMenuBar(self):

        # Make a File menu
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()

        FileOpenitem = menu.Append(-1, '&File Open (Ctrl-F)', 'Open file to analysis', wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnFileOpen, FileOpenitem)
        
        TemplateChangeitem = menu.Append(-1, '&Change Map file (Ctrl-T)', 'Change Map file', wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnTemplateChange, TemplateChangeitem)
        
        TemplateFileOpenitem = menu.Append(-1, '&Map File Open(by system editor)', 'Map file open by system editor', wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnTemplateFileOpen, TemplateFileOpenitem)
        
        Refreshitem = menu.Append(-1, '&Refresh (F5)', 'Refresh', wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnRefresh, Refreshitem)
         
        exitItem = wx.MenuItem(menu, -1, 'E&xit Ctrl-Q', 'Quit!')
        #exitItem.SetBitmap(images.catalog['exit'].GetBitmap())
        #menu.AppendItem(exitItem)
        #self.Bind(wx.EVT_MENU, self.OnFileExit, exitItem)

        wx.App.SetMacExitMenuItemId(exitItem.GetId())
        self.mainmenu.Append(menu, '&File')

        self.SetMenuBar(self.mainmenu)

        if True:
            # This is another way to set Accelerators, in addition to
            # using the '<key>' syntax in the menu items.
            aTable = wx.AcceleratorTable([(wx.ACCEL_ALT,  ord('X'), exitItem.GetId()),
                                          (wx.ACCEL_NORMAL,  wx.WXK_F5, Refreshitem.GetId()),
                                          #(wx.ACCEL_CTRL, ord('H'), helpItem.GetId()),
                                          #(wx.ACCEL_CTRL, ord('F'), findItem.GetId()),
                                          #(wx.ACCEL_NORMAL, wx.WXK_F3, findNextItem.GetId()),
                                          #(wx.ACCEL_NORMAL, wx.WXK_F9, shellItem.GetId()),
                                          ])
            self.SetAcceleratorTable(aTable)
            

    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        
        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
                
                
        
                
                
                    
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Template Structure")
        self.tree.SetItemImage(self.root, 0)
        self.tree.SetItemPyData(self.root, 0)

        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The old native treectrl on MSW has a bug where it doesn't
        # draw all of the text for an item if the font is larger than
        # the default.  It seems to be clipping the item's label as if
        # it was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo or wx.GetApp().GetComCtl32Version() >= 600:
            treeFont.SetPointSize(treeFont.GetPointSize()+2)
            treeFont.SetWeight(wx.BOLD)
            catFont.SetWeight(wx.BOLD)
            
        self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        
        
        
        def PrintWithIndent(List, parent):
            for element in List:

                #print element[0]
                #print filter
                if filter:
                    if filter.lower() in element[0].lower():
                        inserteditem = self.tree.AppendItem(parent, element[0], image=count)
                
                        #print type(element[1])
                        #print element[1]
                        if len(element[1]) > 0 :
                            PrintWithIndent(element[1], inserteditem)
                            
                else:
                    inserteditem = self.tree.AppendItem(parent, element[0], image=count)
                
                    #print type(element[1])
                    #print element[1]
                    if len(element[1]) > 0 :
                        PrintWithIndent(element[1], inserteditem)

        if len(self.tree._treeList) > 0:
            PrintWithIndent(self.tree._treeList, self.root)
        
        
        """
        for category, items in self.tree._treeList:
            count += 1
            if filter:
                items = [item for item in items if filter.lower() in item.lower()]
                
            if items:
                child = self.tree.AppendItem(self.root, category, image=count)
                self.tree.SetItemFont(child, catFont)
                self.tree.SetItemPyData(child, count)
                if not firstChild: firstChild = child
                for childItem in items:
                    image = count
                    if DoesModifiedExist(childItem):
                        image = len(_demoPngs)
                    theDemo = self.tree.AppendItem(child, childItem, image=image)
                    self.tree.SetItemPyData(theDemo, count)
                    self.treeMap[childItem] = theDemo
                    if current and (childItem, category) == current:
                        selectItem = theDemo
        """
                        
                    
        self.tree.Expand(self.root)
        if firstChild:
            self.tree.Expand(firstChild)
        if filter:
            self.tree.ExpandAll()
        elif expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False
        
        self.tree.Thaw()
        self.searchItems = {}


    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()
        
        if fullSearch:
            self.OnSearch()
        else:
            self.RecreateTree()
            

    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        
        for category, items in self.tree._treeList:
            self.searchItems[category] = []
            for childItem in items:
                if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
        self.RecreateTree()            


    def OnSearchCancelBtn(self, event):
        self.filter.SetValue('')
        self.OnSearch()
        

    def SetTreeModified(self, modified):
        item = self.tree.GetSelection()
        if modified:
            image = len(_demoPngs)
        else:
            image = self.tree.GetItemPyData(item)
        self.tree.SetItemImage(item, image)



    # Menu methods
    def OnFileExit(self, *event):
        
        return
        #self.Close()
        
    def HexValue_to_HexString(self, HexValues):
        
        text = ''
        
        for Value in HexValues:
            UpperValue = (ord(Value) & 0xF0) >> 4
            LowerValue = ord(Value) & 0x0F
            
            if UpperValue >= 0 and UpperValue <= 9:
                text += str(UpperValue)
            elif UpperValue == 10:
                text += 'A'
            elif UpperValue == 11:
                text += 'B'
            elif UpperValue == 12:
                text += 'C'
            elif UpperValue == 13:
                text += 'D'
            elif UpperValue == 14:
                text += 'E'
            elif UpperValue == 15:
                text += 'F'
                
            if LowerValue >= 0 and LowerValue <= 9:
                text += str(LowerValue)
            elif LowerValue == 10:
                text += 'A'
            elif LowerValue == 11:
                text += 'B'
            elif LowerValue == 12:
                text += 'C'
            elif LowerValue == 13:
                text += 'D'
            elif LowerValue == 14:
                text += 'E'
            elif LowerValue == 15:
                text += 'F'
                        
        return text
    
    def OnRefresh(self, event):
        
        #wx.MessageBox("refresh")
        #template tree setting
        self.tree.OpenTemplateFile()
        self.RecreateTree()
        self.tree.SelectItem(self.root)

        #template grid setting
        self.nb.SetSelection(0)
        self.TemplateClear()      
        def TreeTraverse(parent):
            item, cookie = self.tree.GetFirstChild(parent)
            while item.IsOk():
                self.SetTemplateView(self.tree.GetItemText(item))
                if self.tree.ItemHasChildren(item):
                    TreeTraverse(item)
                item = self.tree.GetNextSibling(item)
        TreeTraverse(self.root)
        
        
        self.PE = None
        self.PE = ParsingEngine_v2()
        self.PE.GetBlockInfo_InTemplate(self.tree.TemplatePath)
        
        return

    def OnTemplateFileOpen(self, event):
        
        abs = os.path.abspath(self.tree.TemplatePath)
        os.system('explorer "' + abs + '"')
        
        return


    def OnTemplateChange(self, event):
        
        
        dlg = None
        DlgResult = None
        
        dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile=os.getcwd()+"/UserModule", style=wx.OPEN)
        dlg.SetPath(os.getcwd()+"/PFPModule/PFPLib/InternalModules/pfp_sdk/struct_template/*.*")

        NewPFPListFile = ""
        
        DlgResult = dlg.ShowModal()
    
        
        if  DlgResult == wx.ID_OK:
            #set target
            TemplatePath = dlg.GetPath()
                
            self.page1.TemplateViewerGrid.TemplatePath = TemplatePath
            self.tree.TemplatePath = TemplatePath
            
            #template tree setting
            self.tree.OpenTemplateFile()
            self.RecreateTree()
            self.tree.SelectItem(self.root)
    
            #template grid setting
            self.nb.SetSelection(0)
            self.TemplateClear()      
            def TreeTraverse(parent):
                item, cookie = self.tree.GetFirstChild(parent)
                while item.IsOk():
                    self.SetTemplateView(self.tree.GetItemText(item))
                    if self.tree.ItemHasChildren(item):
                        TreeTraverse(item)
                    item = self.tree.GetNextSibling(item)
            TreeTraverse(self.root)
            
            self.PE = None
            self.PE = ParsingEngine_v2()
            self.PE.GetBlockInfo_InTemplate(TemplatePath)
    
        return


    def OnFileOpen(self, event, FilePath = None):
        
        dlg = None
        DlgResult = None
        
        if FilePath == None:
            dlg = wx.FileDialog(self, message="Select Target File", defaultDir=os.getcwd()+"/UserModule", defaultFile=os.getcwd()+"/UserModule", style=wx.OPEN)
            dlg.SetPath(os.getcwd()+"/Testbed/Format_Test_Sample/*.*")

            NewPFPListFile = ""
            
            DlgResult = dlg.ShowModal()
        
        
        
        if  DlgResult == wx.ID_OK or FilePath != None:
            #set target
            if FilePath != None:
                TargetPath = FilePath
            else:
                TargetPath = dlg.GetPath()
            
            #set templage
            TemplatePath = ""
            TemplateList = [['.exe,.sys,.dll', '0:4D5A', "pfp_sdk/struct_template/template_pe.xls"],
                            ['.pf', '0:1A00', "pfp_sdk/struct_template/template_pf_ver26.xls"],
                            ['.pf', '0:1E00', "pfp_sdk/struct_template/template_pf_ver26.xls"],
                            ['.pf', '0:1700', "pfp_sdk/struct_template/template_pf_ver23.xls"],
                            ['.pf', '0:1100', "pfp_sdk/struct_template/template_pf_ver17.xls"],
                            ['.lnk_', '0:4C00', "pfp_sdk/struct_template/template_shortcut.xls"],
                            ['.trx', '4:1612', "pfp_sdk/struct_template/template_Superfetch_trx.xls"],
                            ['.db', '0:4D45', "pfp_sdk/struct_template/template_Superfetch_compressed.xls"],
                            ['.evt', '4:4C66', "pfp_sdk/struct_template/template_evt.xls"],
                            ['.evtx', '0:456C', "pfp_sdk/struct_template/template_evtx.xls"],
                            ['.*', '0:0100', "pfp_sdk/struct_template/template_$i.xls"],
                            ['', '0:7265', "pfp_sdk/struct_template/template_registry_hive.xls"],
                            ['', '0:0500', "pfp_sdk/struct_template/template_info2.xls"],
                            ['.dat', '0:436C', "pfp_sdk/struct_template/template_index-dat.xls"],
                            ['.db', '0:434D', "pfp_sdk/struct_template/template_thumbcache_db.xls"],
                            ['.sqlite', '0:5351', "pfp_sdk/struct_template/template_sqlite.xls"]]
                            #['.*', '0:D0CF', "pfp_sdk/struct_template/template_compound.xls"]]
                            #['.*', '0:5351', "pfp_sdk/struct_template/template_sqlite.xls"]]
                            #['.db', '0:0100', "pfp_sdk/struct_template/template_Superfetch_non_compressed.xls"]]
                            
            
            for SubList in TemplateList:
                
                fp = open(TargetPath, 'rb')
                
                HexValue = ''
                idx = 0
                #length = os.path.getsize(TargetPath)
                #readBuffer = fp.read(length)
                #Hex = readBuffer[0:2]
                                
                Offset = SubList[1].split(':')[0]
                #print ""
                #print "SubList = " + str(SubList)
                #print "Target Path = " + TargetPath
                #print "Offset = " + Offset 
                fp.seek(int(Offset))
                Hex = fp.read(2)
                #print "Hex = "
                #print "readbuffer = "
                #print readBuffer
                Signature = self.HexValue_to_HexString(Hex)
                if Signature.strip() == "":
                    Signature = "can not read.(system file or not existed)"
                fp.close()
                
                
                #print "sig offset = " + str(SubList[1].split(':')[0])
                #print Signature
                
                
                if (os.path.splitext(TargetPath)[1].lower() in SubList[0] or ".*" == SubList[0]) and Signature in SubList[1]:
                    #print SubList[2]
                    TemplatePath = SubList[2]
                    break
            
            if TemplatePath == "":
                TemplatePath = "pfp_sdk/struct_template/template_master_map.xls"
            
            
            if os.path.isfile(TemplatePath) == False:
                TemplatePath = "PFPModule/PFPLib/InternalModules/" + TemplatePath
            
            #print TemplatePath
            
            self.list1.TargetPath = TargetPath
            self.page1.TemplateViewerGrid.TargetPath = TargetPath
            self.tree.TargetPath = TargetPath
            
            self.page1.TemplateViewerGrid.TemplatePath = TemplatePath
            self.tree.TemplatePath = TemplatePath
    
            
            
            #Hex Setting
            threads = []
            th = threading.Thread(target=self.list1.ThreadFileLoad, args=())
            th.start()
            threads.append(th)
            
            
            
            
            #template tree setting
            self.tree.OpenTemplateFile()
            self.RecreateTree()
            self.tree.SelectItem(self.root)
    
            
            #template grid setting
            self.nb.SetSelection(0)
            self.TemplateClear()      
            def TreeTraverse(parent):
                item, cookie = self.tree.GetFirstChild(parent)
                while item.IsOk():
                    self.SetTemplateView(self.tree.GetItemText(item))
                    if self.tree.ItemHasChildren(item):
                        TreeTraverse(item)
                    item = self.tree.GetNextSibling(item)
            TreeTraverse(self.root)
            
            
            
            self.PE.GetBlockInfo_InTemplate(TemplatePath)
            
            
            
            return


    def OnCloseWindow(self, event):
        self.Destroy()
        """
        try:
            self.page1.mgr.DetachPane(self.page1.pnl)
            self.page1.pnl.Destroy()
            self.page1.mgr.Update()
            #self.page1.Destroy()
            #self.Destroy()
        except:
            #self.Destroy()
            return
        """    
        #self.Close()
        
        
    def OnExitApp(self, event):
        wx.GetApp().Exit()
        #self.Destroy()
        #self.Close()

    # Makes sure the user was intending to quit the application
    def OnCloseFrame(self, event):
        dialog = wx.MessageDialog(self, message = "Are you sure you want to quit?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
        response = dialog.ShowModal()
    
        if (response == wx.ID_YES):
            self.OnExitApp(event)
        else:
            event.StopPropagation()


class FileFormatAnalyzer(wx.App):
    def OnInit(self):

        self.SetAppName("wxPyDemo")
        
        frame = Main_Frame(None, "File format analyzer")
        frame.Show()

        return True


def main():
    
    app = FileFormatAnalyzer(False)
    app.MainLoop()



if __name__ == '__main__':
    main()
