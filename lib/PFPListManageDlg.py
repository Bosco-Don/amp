#!/usr/bin/python
# -*- coding: utf-8 -*-


from InternalModules.pfp_sdk.PFPUtil import *




#---------------------------------------------------------------------------

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
    
    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

#---------------------------------------------------------------------------

class CustomDataTable(gridlib.PyGridTableBase):
    def __init__(self):
        gridlib.PyGridTableBase.__init__(self)

        self.colLabels = ['No.', 'Description']

        #, gridlib.GRID_VALUE_STRING
        self.dataTypes = [gridlib.GRID_VALUE_STRING, gridlib.GRID_VALUE_STRING]
        
        self.data = []


    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data) + 1

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )

                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value) 

    #--------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

#---------------------------------------------------------------------------

class AnalysisCategoryList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent


        self.table = CustomDataTable()
        
        self.ModifyorNew = "None"
        self.preSelected = -1
        
        
        self.NowModify = False
        
     
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)


        gridlib.EVT_GRID_CELL_RIGHT_CLICK(self, self.OnRightDown)
        self.MainFrame = self.parent.GetParent().GetParent().GetParent()
        
        self.table.data.append(["none","insert new content.."])
        self.rowcount = 0
        
        self.SetTable(self.table, True)
        
        self.LoadData()
        
        
        
    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        
        self.TableName = "CategoryTable"
        
        try:
            SelectedContentsID = self.table.data[event.GetRow()][0]
        except:
            return
        
        Sequence = ""
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            Sequence = ResultList[0][0]
                    
        
        
        PopupMenu = wx.Menu()        
        
        PopupMenu.Append(-1, "Sequence : " + Sequence)
        OnUp = PopupMenu.Append(-1, "up")
        OnDown = PopupMenu.Append(-1, "down")
        
        self.PopUpSelectedRow = event.GetRow()
        
        self.Bind(wx.EVT_MENU, self.OnUp, OnUp)
        self.Bind(wx.EVT_MENU, self.OnDown, OnDown)
        
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPosition())
        
        return
    
    
    def OnUp(self, event):
        
        self.SequenceChange("Up")
        
        return 
    
    
    def OnDown(self, event):
        
        self.SequenceChange("Down")
        
        return
    
    def SequenceChange(self, UpORDown):
    
        
        SelectedContentsID = self.table.data[self.PopUpSelectedRow][0]
        
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            if UpORDown == "Up":
                        
                if int(ResultList[0][0]) == 0:
                    #wx.MessageBox("This content is top")
                    
                    return
                
                else:
                    
                    UserContentsLocation = ResultList[0][1]
                    Sequence = str(int(ResultList[0][0])-1)
                    
                    SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                    cursor.execute( SelectQuery )
                    ResultList = cursor.fetchone()
                    
                    UpperContentsID = ResultList[0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)+1) + "' where ContentsID = '" + UpperContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
            elif UpORDown == "Down":
                
                UserContentsLocation = ResultList[0][1]
                Sequence = str(int(ResultList[0][0])+1)
                
                SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and  UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall()
                
                if len(ResultList) <= 0:
                    
                    #wx.MessageBox("This content is bottom")
                    
                    return
                
                else:
                
                    LowerContentsID = ResultList[0][0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)-1) + "' where ContentsID = '" + LowerContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                
        else:
            return
                 
        
        con.close()
        
        self.LoadData()
        
        return
    
    
    
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):
        
        
        window = self.parent.GetGrandParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetGrandParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True and self.NowModifyRow != evt.GetRow():
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
        
        #GetCellTextColour (int row, int col) 
        
        self.nowSelected = evt.GetRow()
        
        nextStatus = self.GetCellTextColour(self.nowSelected, 1)
        
        self.SetReadOnly(self.nowSelected, 1, False)
        self.SetCellBackgroundColour(self.nowSelected, 1, '#ffffff') 
        self.SetCellTextColour(self.nowSelected, 1, '#000000')
        
        for idx in range(self.nowSelected+1, len(self.table.data)):

            TempNext = self.GetCellTextColour (idx, 1)

            if nextStatus == '#505050':
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
 
            elif nextStatus == '#000000':
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                
            nextStatus = TempNext
                
        
        
        #self.SetGridCursor(evt.GetRow(), 1)
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)
        
    def OnSelect(self, event):
        
        try:
            window = self.parent.GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
            window0 = self.parent.GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
            window1 = self.parent.GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
            window2 = self.parent.GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
            window3 = self.parent.GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
            
            if window.NowModify == True and self.NowModifyRow != event.GetRow():
                wx.MessageBox("Fill in the blank in Category List")
                return
            
            if window0.NowModify == True:
                wx.MessageBox("Fill in the blank in Analysis Point List")
                return 
            
            if window1.NowModify == True:
                wx.MessageBox("Fill in the blank in Vestige Location List")
                return 
            
            if window2.NowModify == True:
                wx.MessageBox("Fill in the blank in Related tool List")
                return 
            
            if window3.NowModify == True:
                wx.MessageBox("Fill in the blank in Description List")
                return 
            
            
            
            self.nowSelected = event.GetRow()
            
            if self.preSelected != self.nowSelected or self.preSelected == -1:
                self.preSelected = self.nowSelected 
                self.OriginalText = self.GetCellValue(event.GetRow(), 1)
                
                if self.rowcount > event.GetRow():
                    if self.table.data[event.GetRow()][1].strip() != "" and self.table.data[event.GetRow()][1].strip() != "insert new content..":
        
                        #AnalysisPoint Load
                        ###################
                                                                         
                        self.SelectedCategoryID = self.table.data[event.GetRow()][0]
                        
                        window = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList')
                        window.LoadData("", self.SelectedCategoryID)
                    
                        
                        
                        #other initialize
                        ###################
                        window1 = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
                        window1.table.data = []
                        for idx in range(1,window1.rowcount):
                            CurRow = window1.table.GetView().GetGridCursorRow() 
                            delmsg = gridlib.GridTableMessage(window1.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window1.table.GetView().ProcessTableMessage(delmsg) 
                        window1.rowcount = 0
                        if window1.rowcount == 0:
                            window1.table.data.append(["none","insert new content.."])
                            window1.rowcount += 0
                            msg = gridlib.GridTableMessage(window1.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                            window1.table.GetView().ProcessTableMessage(msg) 
                            delmsg = gridlib.GridTableMessage(window1.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window1.table.GetView().ProcessTableMessage(delmsg) 
                        
                        
                        
                        
                        
                        window2 = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                        window2.table.data = []
                        for idx in range(1,window2.rowcount):
                            CurRow = window2.table.GetView().GetGridCursorRow() 
                            delmsg = gridlib.GridTableMessage(window2.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window2.table.GetView().ProcessTableMessage(delmsg) 
                        window2.rowcount = 0
                        if window2.rowcount == 0:
                            window2.table.data.append(["none","insert new content.."])
                            window2.rowcount += 0
                            msg = gridlib.GridTableMessage(window2.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                            window2.table.GetView().ProcessTableMessage(msg) 
                            delmsg = gridlib.GridTableMessage(window2.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window2.table.GetView().ProcessTableMessage(delmsg) 
                            
                            
                            
                            
                        window3 = self.parent.GetGrandParent().FindWindowByName('AnalysisDescriptionOnList')
                        window3.table.data = []
                        for idx in range(1,window3.rowcount):
                            CurRow = window3.table.GetView().GetGridCursorRow() 
                            delmsg = gridlib.GridTableMessage(window3.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window3.table.GetView().ProcessTableMessage(delmsg) 
                        window3.rowcount = 0
                        if window3.rowcount == 0:
                            window3.table.data.append(["none","insert new content.."])
                            window3.rowcount += 0
                            msg = gridlib.GridTableMessage(window3.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                            window3.table.GetView().ProcessTableMessage(msg) 
                            delmsg = gridlib.GridTableMessage(window3.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window3.table.GetView().ProcessTableMessage(delmsg) 
                            
                            
                            
                            
                        window4 = self.parent.GetGrandParent().FindWindowByName('RelatedToolsForAnalysisOnList')
                        window4.table.data = []
                        for idx in range(1,window4.rowcount):
                            CurRow = window4.table.GetView().GetGridCursorRow() 
                            delmsg = gridlib.GridTableMessage(window4.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window4.table.GetView().ProcessTableMessage(delmsg) 
                        window4.rowcount = 0
                        if window4.rowcount == 0:
                            window4.table.data.append(["none","not compatible with this version.."])
                            window4.rowcount += 0
                            msg = gridlib.GridTableMessage(window4.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                            window4.table.GetView().ProcessTableMessage(msg) 
                            delmsg = gridlib.GridTableMessage(window4.table,            # the table 
                                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                                0,1)                                       # position, number of rows 
                            window4.table.GetView().ProcessTableMessage(delmsg) 
                        
                        #temp_listdb_con.close()
        except:
            return
        
    def OnCellChanged(self, event):
        #wx.MessageBox("Cell Changed, " + str(event.GetRow()) + ", " + self.GetCellValue(event.GetRow(), 1) + ", " + self.ModifyorNew )
        
        if self.NowModify == True and self.NowModifyRow == event.GetRow():
            self.NowModify = False
        
        UtilClass = Util()
     
        #insert
        #print self.OriginalText
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "insert new content..":
            
            #Get Related Tech Num
            #########################
            temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select ContentsID from CategoryTable"

            temp_listdb_cursor.execute( SelectQuery )
            ResultList = temp_listdb_cursor.fetchone()
            
            temp_listdb_con.close()
            RelatedTechNum = str(0)
            
            if ResultList == None:
                RelatedTechNum = str(0)
            else:    
                RelatedTechNum = str(int(ResultList[0])/100000)
            
            #Get UserContentsLocation
            #########################
            RelatedPublicidx = 1
            UserContentsLocation = "top" + RelatedTechNum
            DBPath = self.parent.GetParent().GetParent().GetParent().UserPFPListFilePath
            
            for idx in range(0, event.GetRow()):
                if self.GetCellTextColour (idx, 1) == '#505050':
                    UserContentsLocation = self.table.data[idx][0]
                    RelatedPublicidx = idx + 1
                
                
            if sys.argv[3] == "public":
                UserContentsLocation = "public"
                DBPath = self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath
            
            
            """
            DuplicateFlag = False
            """
            temp_listdb_con = sqlite3.connect( DBPath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            EncodedText = UtilClass.DummyCyber( self.parent.GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(event.GetRow(), 1), "")
            
            SelectQuery = "select * from CategoryTable where Text = '" + EncodedText + "'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultList = temp_listdb_cursor.fetchall()
    
            Cnt_Result = len(ResultList)
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultContentsID = temp_listdb_cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            
            #print "Cnt_Result = " + str(Cnt_Result)
            
            if Cnt_Result == 0 and self.GetCellValue(event.GetRow(), 1).strip() != "": 
                
                #Get related sequence
                #####################
                if "top" in UserContentsLocation or "public" in UserContentsLocation:
                    CurrSequence = str(event.GetRow())
                else:
                    CurrSequence = str(event.GetRow() - RelatedPublicidx)
                
                SelectQuery = "select Sequence, ContentsID from CategoryTable where cast(Sequence as integer) >= " + CurrSequence + " and UserContentsLocation = '" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()
        
                for Row in ResultList:
            
                    UpdateQuery = "update CategoryTable set Sequence = '" + str(int(Row[0]) + 1) +"' where ContentsID = '" + Row[1] + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()
                
                
                EncodedText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(event.GetRow(), 1), "")
                
                #user contents id is related public + 500000(ex FirstResponse's user contentsid == 6XXXXX)
                #############################################################################################
                if sys.argv[3] == "public":
                    InsertQuery = "insert into CategoryTable (Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, RelatedWebPage, UserContentsLocation) values ('"+ EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID) + "', 'n', 'http://portable-forensics.com', '" + UserContentsLocation + "' );"
                else:
                    InsertQuery = "insert into CategoryTable (Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, RelatedWebPage, UserContentsLocation) values ('"+ EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID + (int(RelatedTechNum) * 100000) + 500000) + "', 'n', 'http://portable-forensics.com', '" + UserContentsLocation + "' );"
                    
                temp_listdb_cursor.execute( InsertQuery )
                temp_listdb_con.commit()
                
                LastContentsID += 1
                NextContentsID += 1
                UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                
                #2013.12.07 - modify 
                SelectQuery = "select ContentsID from CategoryTable where Text = '" + EncodedText +"'"
        
                temp_listdb_cursor.execute( SelectQuery )
                ContentsID = temp_listdb_cursor.fetchone()[0]
                
                self.SelectedCategoryID = ContentsID
                window = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList')               
                window.LoadData("", ContentsID)
                
                self.table.data[event.GetRow()][0] = str(ContentsID)
                
                self.rowcount += 1
                
            else:
                
                wx.MessageBox("Contents is duplicated(or blank)")

                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
                
                    
                     
            temp_listdb_con.close()
        
        
        else:   #modify 
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdeateQuery = "update CategoryTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedCategoryID + "'"
        
                temp_listdb_cursor.execute( UpdeateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
                
            else:
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdeateQuery = "update CategoryTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedCategoryID + "'"
        
                temp_listdb_cursor.execute( UpdeateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
            
    def OnKeyDown(self, evt):
        
        UtilClass = Util()
        
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetGrandParent().FindWindowByName('AnalysisPointOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
                    window.SelectRow(1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                if self.GetCellTextColour(self.nowSelected, 1) == '#505050':
                    wx.MessageBox("Can not delete the public content")
                    return 
                
                DBPath = ""
                
                if sys.argv[3] == "public":
                    DBPath = self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath   
                else:
                    DBPath = self.parent.GetParent().GetParent().GetParent().UserPFPListFilePath
                    
                
                
                temp_listdb_con = sqlite3.connect( DBPath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdeateQuery = "update CategoryTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(self.nowSelected, 1), "") + "(.. delete..)" +"', isDeleted = 'y' where ContentsID = '" + self.SelectedCategoryID + "'"
        
                temp_listdb_cursor.execute( UpdeateQuery )
                temp_listdb_con.commit()
                
                #get UserContentsLocation
                SelectQuery = "select UserContentsLocation, Sequence from CategoryTable where ContentsID = '" + self.SelectedCategoryID + "'"

                temp_listdb_cursor.execute( SelectQuery )
                row = temp_listdb_cursor.fetchone()
                UserContentsLocation = row[0]
                Sequence = row[1]
                
                
                SelectQuery = "select Sequence, ContentsID from CategoryTable where cast(Sequence as integer) > " + Sequence + " and UserContentsLocation ='" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()

                for Row in ResultList:
            
                    UpdateQuery = "update CategoryTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()

                temp_listdb_con.close()
        
                self.table.data = []
                
                #print "NumofRows = " + str(self.rowcount)
                
                for idx in range(1,self.rowcount):
                    
                    CurRow = self.table.GetView().GetGridCursorRow() 
                    delmsg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0,1)                                       # position, number of rows 
                    self.table.GetView().ProcessTableMessage(delmsg) 
                    
                self.rowcount = 0
                
                #self.LoadData()
                
                
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"
        
                temp_listdb_cursor.execute( SelectQuery )
                PublicResultRows = temp_listdb_cursor.fetchall()
                
                
                
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"
        
                temp_listdb_cursor.execute( SelectQuery )
                UserResultRows = temp_listdb_cursor.fetchall()
                
                ResultRows = []
                
                if len(PublicResultRows) <= 0:
                    for UserRow in UserResultRows:
                        if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                            ResultRows.append(UserRow)
                    
                    for UserRow in UserResultRows:
                        if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                            ResultRows.append(UserRow)
                
                else:
                    for UserRow in UserResultRows:
                        if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                            ResultRows.append(UserRow)
                    
                    
                    for PublicRow in PublicResultRows:
                        if "(.. delete..)" not in PublicRow[0]:
                            ResultRows.append(PublicRow)
                        
                        for UserRow in UserResultRows:
                            if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0] and int(PublicRow[1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                                ResultRows.append(UserRow)
                    
                    for UserRow in UserResultRows:
                        if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                            ResultRows.append(UserRow)
                
                
                for Row in ResultRows:
                    
                    try:
                        DecodedText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, "", Row[0])
                    except:
                        DecodedText = Row[0]
                    
                    self.table.data.append([Row[1], DecodedText])
                    self.rowcount +=1
                    
                    msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                    self.table.GetView().ProcessTableMessage(msg) 
                     
                delmsg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                           
                if self.rowcount == 0:
                    self.table.data.append(["none","insert new content.."])
                    self.rowcount += 1
                    
                    msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                    self.table.GetView().ProcessTableMessage(msg) 
                     
                    delmsg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0,1)                                       # position, number of rows 
                    self.table.GetView().ProcessTableMessage(delmsg) 
                    
                for idx in range(0, len(self.table.data)):
                    if sys.argv[3] != "public" and int(self.table.data[idx][0]) < 500000:
                        self.SetReadOnly(idx, 1, True)
                        self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                        self.SetCellTextColour(idx, 1, '#505050')
                
        
    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')
        
    def LoadData(self):
        
        self.table.data = []
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from CategoryTable order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        if len(PublicResultRows) <= 0:
            for UserRow in UserResultRows:
                if "top0" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
        
        else:
            for UserRow in UserResultRows:
                if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                    ResultRows.append(UserRow)
            
            
            for PublicRow in PublicResultRows:
                if "(.. delete..)" not in PublicRow[0]:
                    ResultRows.append(PublicRow)
                
                for UserRow in UserResultRows:
                    if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0] and int(PublicRow[1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                        ResultRows.append(UserRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0] and int(PublicResultRows[0][1]) / 100000 == (int(UserRow[1])-500000) / 100000:
                    ResultRows.append(UserRow)

        
        temp_listdb_con.close()
                
                
                
                
        if len(ResultRows) > 0:
            for Row in ResultRows:
                
                try:
                    UtilClass = Util()
                    self.table.data.append([Row[1],UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().DecodedDummy, "", Row[0])])
                except:
                    self.table.data.append([Row[1],Row[0]])
                
                
                self.rowcount += 1
    
                msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.table.GetView().ProcessTableMessage(msg) 
                
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,               # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                0,1)                                                    # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                
        temp_listdb_con.close() 
        
        if self.rowcount == 0:
            self.table.data.append(["none","insert new content.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
        
        
        for idx in range(0, len(self.table.data)):
            try:
                if sys.argv[3] != "public" and int(self.table.data[idx][0]) < 500000:
                    self.SetReadOnly(idx, 1, True)
                    self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                    self.SetCellTextColour(idx, 1, '#505050')
            except:
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                
                
                
    
#---------------------------------------------------------------------------

class AnalysisPointList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent

        self.table = CustomDataTable()
        
        self.ModifyorNew = "None"
        
        self.table.data.append(["none","insert new content.."])
        self.rowcount = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        gridlib.EVT_GRID_CELL_RIGHT_CLICK(self, self.OnRightDown)
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent()

        self.SetTable(self.table, True)
        
        self.NowModify = False



    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.TableName = "AnPointTable"
        
        try:
            SelectedContentsID = self.table.data[event.GetRow()][0]
        except:
            return
        
        Sequence = ""
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            Sequence = ResultList[0][0]
                    
        
        
        PopupMenu = wx.Menu()        
        
        PopupMenu.Append(-1, "Sequence : " + Sequence)   
        
        OnUp = PopupMenu.Append(-1, "up")
        OnDown = PopupMenu.Append(-1, "down")
        
        self.PopUpSelectedRow = event.GetRow()
        
        self.Bind(wx.EVT_MENU, self.OnUp, OnUp)
        self.Bind(wx.EVT_MENU, self.OnDown, OnDown)
        
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPosition())
        
        return
    
    
    def OnUp(self, event):
        
        self.SequenceChange("Up")
        
        return 
    
    
    def OnDown(self, event):
        
        self.SequenceChange("Down")
        
        return
    
    def SequenceChange(self, UpORDown):
    
        
        SelectedContentsID = self.table.data[self.PopUpSelectedRow][0]
        
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            if UpORDown == "Up":
                        
                if int(ResultList[0][0]) == 0:
                    #wx.MessageBox("This content is top")
                    
                    return
                
                else:
                    
                    UserContentsLocation = ResultList[0][1]
                    Sequence = str(int(ResultList[0][0])-1)
                    
                    SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and CategoryID = '" + self.NowCategory + "' and UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                    cursor.execute( SelectQuery )
                    ResultList = cursor.fetchone()
                    
                    UpperContentsID = ResultList[0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)+1) + "' where ContentsID = '" + UpperContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
            elif UpORDown == "Down":
                
                UserContentsLocation = ResultList[0][1]
                Sequence = str(int(ResultList[0][0])+1)
                
                SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and CategoryID = '" + self.NowCategory + "' and UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall()
                
                if len(ResultList) <= 0:
                    
                    #wx.MessageBox("This content is bottom")
                    
                    return
                
                else:
                
                    LowerContentsID = ResultList[0][0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)-1) + "' where ContentsID = '" + LowerContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                
        else:
            return
                 
        
        con.close()
        
        self.LoadData("", self.NowCategory)
        
        return



    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):
        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True and self.NowModifyRow != evt.GetRow():
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
        
        
        
        
        self.nowSelected = evt.GetRow()
        
        nextStatus = self.GetCellTextColour(self.nowSelected, 1)
        
        self.SetReadOnly(self.nowSelected, 1, False)
        self.SetCellBackgroundColour(self.nowSelected, 1, '#ffffff') 
        self.SetCellTextColour(self.nowSelected, 1, '#000000')
        
        for idx in range(self.nowSelected+1, len(self.table.data)):

            TempNext = self.GetCellTextColour (idx, 1)

            if nextStatus == '#505050':
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
 
            elif nextStatus == '#000000':
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                
            nextStatus = TempNext
                
        
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)

    def OnSelect(self, event):
        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True and self.NowModifyRow != event.GetRow():
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        self.nowSelected = event.GetRow()
        self.OriginalText = self.GetCellValue(event.GetRow(), 1)
        
        windowVestigeLocation = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
        
        
        if self.rowcount > event.GetRow():
            if self.table.data[event.GetRow()][1].strip() != ""  and self.table.data[event.GetRow()][1].strip() != "insert new content..":
    
            
                self.SelectedAnPointID = self.table.data[event.GetRow()][0]
                
                windowVestigeLocation.LoadData("", self.NowCategory, self.SelectedAnPointID)

        
                window2 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                window2.table.data = []
                for idx in range(1,window2.rowcount):
                    CurRow = window2.table.GetView().GetGridCursorRow() 
                    delmsg = gridlib.GridTableMessage(window2.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window2.table.GetView().ProcessTableMessage(delmsg) 
                window2.rowcount = 0
                if window2.rowcount == 0:
                    window2.table.data.append(["none","insert new content.."])
                    window2.rowcount += 0
                    msg = gridlib.GridTableMessage(window2.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                    window2.table.GetView().ProcessTableMessage(msg) 
                    delmsg = gridlib.GridTableMessage(window2.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window2.table.GetView().ProcessTableMessage(delmsg) 
                    
                window3 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                window3.table.data = []
                for idx in range(1,window3.rowcount):
                    CurRow = window3.table.GetView().GetGridCursorRow() 
                    delmsg = gridlib.GridTableMessage(window3.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window3.table.GetView().ProcessTableMessage(delmsg) 
                window3.rowcount = 0
                if window3.rowcount == 0:
                    window3.table.data.append(["none","insert new content.."])
                    window3.rowcount += 0
                    msg = gridlib.GridTableMessage(window3.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                    window3.table.GetView().ProcessTableMessage(msg) 
                    delmsg = gridlib.GridTableMessage(window3.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window3.table.GetView().ProcessTableMessage(delmsg) 
                    
                window4 = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
                window4.table.data = []
                for idx in range(1,window4.rowcount):
                    CurRow = window4.table.GetView().GetGridCursorRow() 
                    delmsg = gridlib.GridTableMessage(window4.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window4.table.GetView().ProcessTableMessage(delmsg) 
                window4.rowcount = 0
                if window4.rowcount == 0:
                    window4.table.data.append(["none","insert new content.."])
                    window4.rowcount += 0
                    msg = gridlib.GridTableMessage(window4.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                    window4.table.GetView().ProcessTableMessage(msg) 
                    delmsg = gridlib.GridTableMessage(window4.table,            # the table 
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                        0,1)                                       # position, number of rows 
                    window4.table.GetView().ProcessTableMessage(delmsg) 
            

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnCellChanged(self, event):
        #wx.MessageBox("Cell Changed, " + str(event.GetRow()) + ", " + self.GetCellValue(event.GetRow(), 1) )
        
        if self.NowModify == True and self.NowModifyRow == event.GetRow():
            self.NowModify = False
        
        
        #Get Related Tech Num
        #########################
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select ContentsID from AnPointTable"

        temp_listdb_cursor.execute( SelectQuery )
        ResultList = temp_listdb_cursor.fetchall()
        
        temp_listdb_con.close()
        
        RelatedTechNum = str(0)
            
        if len(ResultList) == 0:
            RelatedTechNum = str(0)
        else:    
            RelatedTechNum = str(int(ResultList[0][0])/100000)
        
        #Get UserContentsLocation
        #########################
        RelatedPublicidx = 1
        UserContentsLocation = "top" + RelatedTechNum
        DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
        
        for idx in range(0, event.GetRow()):
            if self.GetCellTextColour (idx, 1) == '#505050':
                UserContentsLocation = self.table.data[idx][0]
                RelatedPublicidx = idx + 1
            
            
        if sys.argv[3] == "public":
            UserContentsLocation = "public"
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath
        
        
        UtilClass = Util()
        
        #insert
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "insert new content..":
            
            """
            DuplicateFlag = False
            """
                        
            temp_listdb_con = sqlite3.connect( DBPath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select * from AnPointTable where Text = '" + self.GetCellValue(event.GetRow(), 1) + "' and CategoryID = '" + self.NowCategory + "'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultList = temp_listdb_cursor.fetchall()
    
            Cnt_Result = len(ResultList)
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultContentsID = temp_listdb_cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            
            if Cnt_Result == 0 and self.GetCellValue(event.GetRow(), 1).strip() != "": 
                
                #Get related sequence
                #####################
                if "top" in UserContentsLocation or "public" in UserContentsLocation:
                    CurrSequence = str(event.GetRow())
                else:
                    CurrSequence = str(event.GetRow() - RelatedPublicidx)
                
                SelectQuery = "select Sequence, ContentsID from AnPointTable where cast(Sequence as integer) >= " + CurrSequence + " and CategoryID = '" + self.NowCategory + "' and UserContentsLocation = '" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()
        
                for Row in ResultList:
            
                    UpdateQuery = "update AnPointTable set Sequence = '" + str(int(Row[0]) + 1) +"' where ContentsID = '" + Row[1] + "' and UserContentsLocation = '" + UserContentsLocation + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()
                
                EncodedText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(event.GetRow(), 1), "")
                
                
                #user contents id is related public + 500000(ex FirstResponse's user contentsid == 6XXXXX)
                #############################################################################################
                if sys.argv[3] == "public":
                    InsertQuery = "insert into AnPointTable (CategoryID, Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, RelatedWebPage, UserContentsLocation) values ('" + self.NowCategory + "', '"+ EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID) + "', 'n', 'http://portable-forensics.com', '" + UserContentsLocation + "' );"
                else:
                    InsertQuery = "insert into AnPointTable (CategoryID, Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, RelatedWebPage, UserContentsLocation) values ('" + self.NowCategory + "', '"+ EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID + (int(RelatedTechNum) * 100000) + 500000) + "', 'n', 'http://portable-forensics.com', '" + UserContentsLocation + "' );"
                   
                   
                temp_listdb_cursor.execute( InsertQuery )
                temp_listdb_con.commit()
                
                LastContentsID += 1
                NextContentsID += 1
                UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                
                #2013.12.07 - modify 
                SelectQuery = "select ContentsID from AnPointTable where Text = '" + EncodedText +"' and CategoryID = '" + self.NowCategory + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                AnPointID = temp_listdb_cursor.fetchone()[0]
                
                self.SelectedAnPointID = AnPointID
                windowVestigeLocation = self.parent.GetGrandParent().FindWindowByName('VestigeLocationOnList')
                windowVestigeLocation.LoadData("", self.NowCategory, AnPointID)
                
                self.table.data[event.GetRow()][0] = str(AnPointID)
                
                self.rowcount += 1
                
            else:
                wx.MessageBox("Contents is duplicated(or blank)")
                
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
                    

            temp_listdb_con.close()

        else:   #modify
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdateQuery = "update AnPointTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedAnPointID + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
                
            else:
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdateQuery = "update AnPointTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedAnPointID + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
        
    def OnKeyDown(self, evt):
        
        UtilClass = Util()
        
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
                    
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                if self.GetCellTextColour(self.nowSelected, 1) == '#505050':
                    wx.MessageBox("Can not delete the public content")
                    return 
                
                DBPath = ""
                
                if sys.argv[3] == "public":
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
                else:
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                    
                
                
                temp_listdb_con = sqlite3.connect( DBPath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdeateQuery = "update AnPointTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(self.nowSelected, 1), "") + "(.. delete..)" +"', isDeleted = 'y' where ContentsID = '" + self.SelectedAnPointID + "'"
        
                temp_listdb_cursor.execute( UpdeateQuery )
                temp_listdb_con.commit()
                
                
                
                
                SelectQuery = "select Sequence, UserContentsLocation from AnPointTable where ContentsID = '" + self.SelectedAnPointID + "'"

                temp_listdb_cursor.execute( SelectQuery )
                row = temp_listdb_cursor.fetchone()
                Sequence = row[0]
                UserContentsLocation = row[1] 
                
                SelectQuery = "select Sequence, ContentsID from AnPointTable where cast(Sequence as integer) > " + Sequence + " and CategoryID = '" + self.NowCategory + "' and UserContentsLocation = '" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()
        
                for Row in ResultList:
            
                    UpdateQuery = "update AnPointTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()

                temp_listdb_con.close()
                
                
                self.LoadData("", self.NowCategory)

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')
        
    def LoadData(self, PublicPFPListFilePath, Category):
        
        #print Category
        self.NowCategory = Category
        
        self.table.data = []
        
        #print "NumofRows = " + str(self.rowcount)
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        
        
        
            
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from AnPointTable where CategoryID = '" + Category + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        for UserRow in UserResultRows:
            if "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:
                ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
                    
                    
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)            
                    
                    
                    
        
        if len(ResultRows) > 0:
            for Row in ResultRows:
                
                try:
                    UtilClass = Util()
                    self.table.data.append([Row[1],UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", Row[0])])
                except:
                    self.table.data.append([Row[1],Row[0]])
                
                
                self.rowcount += 1
    
                msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.table.GetView().ProcessTableMessage(msg) 
                
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,               # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                0,1)                                                    # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                
        temp_listdb_con.close() 
        
        if self.rowcount == 0:
            self.table.data.append(["none","insert new content.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
        
        
        for idx in range(0, len(self.table.data)):
            try:
                if sys.argv[3] != "public" and int(self.table.data[idx][0]) < 500000:
                    self.SetReadOnly(idx, 1, True)
                    self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                    self.SetCellTextColour(idx, 1, '#505050')
            except:
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
        
#---------------------------------------------------------------------------
            
class VestigeLocationList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent

        self.table = CustomDataTable()
        
        self.table.data.append(["none","insert new content.."])
        self.rowcount = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)   
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        gridlib.EVT_GRID_CELL_RIGHT_CLICK(self, self.OnRightDown)
        self.MainFrame = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()

        self.SetTable(self.table, True)
        
        self.NowModify = False


    def OnRightDown(self, event):
        #wx.MessageBox("Right click")
        
        self.TableName = "VesLocationTable"
        
        try:
            SelectedContentsID = self.table.data[event.GetRow()][0]
        except:
            return
        
        Sequence = ""
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            Sequence = ResultList[0][0]
                    
        
        
        PopupMenu = wx.Menu()        
        
        PopupMenu.Append(-1, "Sequence : " + Sequence)   
        
        OnUp = PopupMenu.Append(-1, "up")
        OnDown = PopupMenu.Append(-1, "down")
        
        self.PopUpSelectedRow = event.GetRow()
        
        self.Bind(wx.EVT_MENU, self.OnUp, OnUp)
        self.Bind(wx.EVT_MENU, self.OnDown, OnDown)
        
        
        #---Set Menu bar---
        self.PopupMenu(PopupMenu, event.GetPosition())
        
        return
    
    
    

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.

    def OnUp(self, event):
        
        self.SequenceChange("Up")
        
        return 
    
    
    def OnDown(self, event):
        
        self.SequenceChange("Down")
        
        return
    
    def SequenceChange(self, UpORDown):
        
        
        SelectedContentsID = self.table.data[self.PopUpSelectedRow][0]
        
        
        DBPath = ""
        if sys.argv[3] != "public":
            DBPath = self.MainFrame.UserPFPListFilePath
        else:
            DBPath = self.MainFrame.PublicPFPListFilePath
        
        
        con = sqlite3.connect( DBPath )
        cursor = con.cursor()
        
        SelectQuery = "select Sequence, UserContentsLocation from " + self.TableName + " where ContentsID = '" + SelectedContentsID + "'"

        cursor.execute( SelectQuery )
        ResultList = cursor.fetchall()

        
        
        if len(ResultList) > 0:
            
            if UpORDown == "Up":
                        
                if int(ResultList[0][0]) == 0:
                    #wx.MessageBox("This content is top")
                    
                    return
                
                else:
                    
                    UserContentsLocation = ResultList[0][1]
                    Sequence = str(int(ResultList[0][0])-1)
                    
                    SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and AnPointID = '" + self.NowAnalysisPoint + "' and UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                    cursor.execute( SelectQuery )
                    ResultList = cursor.fetchone()
                    
                    UpperContentsID = ResultList[0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)+1) + "' where ContentsID = '" + UpperContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
            elif UpORDown == "Down":
                
                UserContentsLocation = ResultList[0][1]
                Sequence = str(int(ResultList[0][0])+1)
                
                SelectQuery = "select ContentsID from " + self.TableName + " where isDeleted = 'n' and AnPointID = '" + self.NowAnalysisPoint + "' and UserContentsLocation = '" + UserContentsLocation + "' and Sequence = '" + Sequence + "'"
    
                cursor.execute( SelectQuery )
                ResultList = cursor.fetchall()
                
                if len(ResultList) <= 0:
                    
                    #wx.MessageBox("This content is bottom")
                    
                    return
                
                else:
                
                    LowerContentsID = ResultList[0][0]
                    
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + Sequence + "' where ContentsID = '" + SelectedContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                    
                    UpdateQuery = "update " + self.TableName + " set Sequence = '" + str(int(Sequence)-1) + "' where ContentsID = '" + LowerContentsID + "'" 
                    cursor.execute( UpdateQuery )
                    con.commit()
                
        else:
            return
                 
        
        con.close()
        
        self.LoadData("", self.NowCategory, self.NowAnalysisPoint)
        
        return
    
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):
        
        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True and self.NowModifyRow != evt.GetRow():
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
        
        
        
        self.nowSelected = evt.GetRow()
        
        nextStatus = self.GetCellTextColour(self.nowSelected, 1)
        
        self.SetReadOnly(self.nowSelected, 1, False)
        self.SetCellBackgroundColour(self.nowSelected, 1, '#ffffff') 
        self.SetCellTextColour(self.nowSelected, 1, '#000000')
        
        for idx in range(self.nowSelected+1, len(self.table.data)):

            TempNext = self.GetCellTextColour (idx, 1)

            if nextStatus == '#505050':
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
 
            elif nextStatus == '#000000':
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                
            nextStatus = TempNext
                
        
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)
        
    def OnSelect(self, event):
        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True and self.NowModifyRow != event.GetRow():
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        self.nowSelected = event.GetRow()
        self.OriginalText = self.GetCellValue(event.GetRow(), 1)
        
        windowRelatedToolsForAcquisition = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        windowAnalysisDescription = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        windowRelatedToolsForAnalysis = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
        
        if self.rowcount > event.GetRow():
            if self.table.data[event.GetRow()][1].strip() != ""  and self.table.data[event.GetRow()][1].strip() != "insert new content..":
                
                if self.GetCellTextColour (event.GetRow(), 1) == '#505050' or sys.argv[3] == 'public':   
    
                    
                    self.SelectedVesLocationID = self.table.data[event.GetRow()][0]
                    
                    windowRelatedToolsForAcquisition.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    windowAnalysisDescription.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    windowRelatedToolsForAnalysis.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    
                else:
                    
                    self.SelectedVesLocationID = self.table.data[event.GetRow()][0]
            
                    windowRelatedToolsForAcquisition.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    windowAnalysisDescription.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    windowRelatedToolsForAnalysis.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                    

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')
        
    def OnCellChanged(self, event):
        
        if self.NowModify == True and self.NowModifyRow == event.GetRow():
            self.NowModify = False
        
        
        #Get Related Tech Num
        #########################
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select ContentsID from AnPointTable"

        temp_listdb_cursor.execute( SelectQuery )
        ResultList = temp_listdb_cursor.fetchone()
        
        temp_listdb_con.close()
        
        RelatedTechNum = str(0)
            
        if ResultList == None:
            RelatedTechNum = str(0)
        else:    
            RelatedTechNum = str(int(ResultList[0])/100000)
        
        #Get UserContentsLocation
        #########################
        RelatedPublicidx = 1
        UserContentsLocation = "top" + RelatedTechNum
        DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
        
        for idx in range(0, event.GetRow()):
            if self.GetCellTextColour (idx, 1) == '#505050':
                UserContentsLocation = self.table.data[idx][0]
                RelatedPublicidx = idx + 1
            
            
        if sys.argv[3] == "public":
            UserContentsLocation = "public"
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath
        
        
        
        UtilClass = Util()
        
        #insert
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "insert new content..":
            
            temp_listdb_con = sqlite3.connect( DBPath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select * from VesLocationTable where Text = '" + self.GetCellValue(event.GetRow(), 1) + "' and AnPointID = '" + self.NowAnalysisPoint + "'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultList = temp_listdb_cursor.fetchall()
    
            Cnt_Result = len(ResultList)
            
            SelectQuery = "select LastContentsID, NextContentsID from ContentsIDTable where IDType = 'Local'"

            temp_listdb_cursor.execute( SelectQuery )
            ResultContentsID = temp_listdb_cursor.fetchone()
            LastContentsID = int(ResultContentsID[0])
            NextContentsID = int(ResultContentsID[1])
            
            if Cnt_Result == 0 and self.GetCellValue(event.GetRow(), 1).strip() != "": 
                
                #Get related sequence
                #####################
                if "top" in UserContentsLocation or "public" in UserContentsLocation:
                    CurrSequence = str(event.GetRow())
                else:
                    CurrSequence = str(event.GetRow() - RelatedPublicidx)
                
                SelectQuery = "select Sequence, ContentsID from VesLocationTable where cast(Sequence as integer) >= " + CurrSequence + " and AnPointID = '" + self.NowAnalysisPoint + "' and UserContentsLocation = '" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()
        
                for Row in ResultList:
            
                    UpdateQuery = "update VesLocationTable set Sequence = '" + str(int(Row[0]) + 1) + "' where ContentsID = '" + Row[1] + "' and UserContentsLocation = '" + UserContentsLocation + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()
                
                
                EncodedText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(event.GetRow(), 1), "")
                
                #user contents id is related public + 500000(ex FirstResponse's user contentsid == 6XXXXX)
                #############################################################################################
                if sys.argv[3] == "public":
                    InsertQuery = "insert into VesLocationTable (AnPointID, Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, UserContentsLocation) values ('" + self.NowAnalysisPoint + "', '" + EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID) + "', 'n', '" + UserContentsLocation + "' );"
                else:
                    InsertQuery = "insert into VesLocationTable (AnPointID, Text, Registrant, Contact, CreateTime, ModifyTime, isPublic, Sequence, ContentsID, isDeleted, UserContentsLocation) values ('" + self.NowAnalysisPoint + "', '" + EncodedText + "', '" + sys.argv[4] + "', '" + sys.argv[5] + "', '" + str(int(time.time())) + "', '" + str(int(time.time())) + "', 'n', '" + CurrSequence + "','" + str(NextContentsID + (int(RelatedTechNum) * 100000) + 500000) + "', 'n', '" + UserContentsLocation + "' );"
                   
                
                
                temp_listdb_cursor.execute( InsertQuery )
                temp_listdb_con.commit()
                
                LastContentsID += 1
                NextContentsID += 1
                UpdateQuery = "update ContentsIDTable set LastContentsID = '" + str(LastContentsID) + "', NextContentsID = '" + str(NextContentsID) + "' where IDType = 'Local'"
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                
                #2013.12.07 - modify 
                windowRelatedToolsForAcquisition = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                windowAnalysisDescription = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                windowRelatedToolsForAnalysis = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
    
                SelectQuery = "select ContentsID from VesLocationTable where Text = '" + EncodedText +"' and AnPointID = '" + self.NowAnalysisPoint + "'"
        
                temp_listdb_cursor.execute( SelectQuery )
                VesLocationID = temp_listdb_cursor.fetchone()[0]
                
                self.SelectedVesLocationID = VesLocationID
                    
                VestigeLocation = self.table.data[event.GetRow()][1]
                
                windowRelatedToolsForAcquisition.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                windowAnalysisDescription.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
                windowRelatedToolsForAnalysis.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.SelectedVesLocationID)
            
                self.table.data[event.GetRow()][0] = str(self.SelectedVesLocationID)
            
                self.rowcount += 1
                
            else:
                wx.MessageBox("Contents is duplicated(or blank)")
                
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
                
            temp_listdb_con.close()

        else:   #modify
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdateQuery = "update VesLocationTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedVesLocationID + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

            else:
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdateQuery = "update VesLocationTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.table.data[event.GetRow()][1], "") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.SelectedVesLocationID + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

                  
                        
    def OnKeyDown(self, evt):
        
        UtilClass = Util()
        
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
                    
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                if self.GetCellTextColour(self.nowSelected, 1) == '#505050':
                    wx.MessageBox("Can not delete the public content")
                    return 
                
                DBPath = ""
                
                if sys.argv[3] == "public":
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
                else:
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                    
                
                
                temp_listdb_con = sqlite3.connect( DBPath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                UpdeateQuery = "update VesLocationTable set Text = '" + UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, self.GetCellValue(self.nowSelected, 1), "") + "(.. delete..)" +"', isDeleted = 'y' where ContentsID = '" + self.SelectedVesLocationID + "'"
        
                temp_listdb_cursor.execute( UpdeateQuery )
                temp_listdb_con.commit()
                    
                
                
                SelectQuery = "select Sequence, UserContentsLocation from VesLocationTable where ContentsID = '" + self.SelectedVesLocationID + "'"

                temp_listdb_cursor.execute( SelectQuery )
                row = temp_listdb_cursor.fetchone()
                Sequence = row[0]
                UserContentsLocation = row[1] 
                
                
                SelectQuery = "select Sequence, ContentsID from VesLocationTable where cast(Sequence as integer) > " + Sequence + " and AnPointID = '" + self.NowAnalysisPoint + "' and UserContentsLocation = '" + UserContentsLocation + "'"

                temp_listdb_cursor.execute( SelectQuery )
                ResultList = temp_listdb_cursor.fetchall()
        
                for Row in ResultList:
            
                    UpdateQuery = "update VesLocationTable set Sequence = '" + str(int(Row[0]) - 1) +"' where ContentsID = '" + Row[1] + "'"
            
                    temp_listdb_cursor.execute( UpdateQuery )
                    temp_listdb_con.commit()
                    
                    
                    
                temp_listdb_con.close()
        
                
                self.LoadData("", self.NowCategory, self.NowAnalysisPoint)

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')

    def LoadData(self, PublicPFPListFilePath, Category, AnalysisPoint):
        
        self.table.data = []
        self.NowCategory = Category
        self.NowAnalysisPoint = AnalysisPoint
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        
               
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable where AnPointID = '" + AnalysisPoint + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        PublicResultRows = temp_listdb_cursor.fetchall()
        
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Text, ContentsID, UserContentsLocation from VesLocationTable where AnPointID = '" + AnalysisPoint + "' order by cast(Sequence as decimal)"

        temp_listdb_cursor.execute( SelectQuery )
        UserResultRows = temp_listdb_cursor.fetchall()
        
        ResultRows = []
        
        for UserRow in UserResultRows:
            if  "top" in UserRow[2] and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
        
        
        for PublicRow in PublicResultRows:
            if "(.. delete..)" not in PublicRow[0]:
                ResultRows.append(PublicRow)
            
            for UserRow in UserResultRows:
                if UserRow[2] == PublicRow[1] and "(.. delete..)" not in UserRow[0]:
                    ResultRows.append(UserRow)
                    
                    
        for UserRow in UserResultRows:
            if UserRow[2] == "bottom" and "(.. delete..)" not in UserRow[0]:
                ResultRows.append(UserRow)
                    
                    
        
        
        
        if len(ResultRows) > 0:
            for Row in ResultRows:
                try:
                    UtilClass = Util()
                    self.table.data.append([Row[1],UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", Row[0])])
                except:
                    self.table.data.append([Row[1],Row[0]])
                    

                self.rowcount += 1
    
                msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.table.GetView().ProcessTableMessage(msg) 
                
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,               # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                0,1)                                                    # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                    
        temp_listdb_con.close()
        
       
                            
        if self.rowcount == 0:
            self.table.data.append(["none","insert new content.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                            
        
        for idx in range(0, len(self.table.data)):
            try:
                if sys.argv[3] != "public" and int(self.table.data[idx][0]) < 500000:
                    self.SetReadOnly(idx, 1, True)
                    self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                    self.SetCellTextColour(idx, 1, '#505050')
            except:
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                            
class RelatedToolsForAcquisitionList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent

        self.table = CustomDataTable()
        
        self.table.data.append(["none","insert new content.."])
        self.rowcount = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)   
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.SetTable(self.table, True)
        
        self.NowModify = False

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):

	if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
            wx.MessageBox("sorry, can not modify public target.")
            
            return        

        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True and self.NowModifyRow != evt.GetRow():
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        
        
        
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)
        
    def OnSelect(self, event):

        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True and self.NowModifyRow != event.GetRow():
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True:
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        self.nowSelected = event.GetRow()
        self.OriginalText = self.GetCellValue(event.GetRow(), 1)

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')
        
    def OnCellChanged(self, event):
        
        if self.NowModify == True and self.NowModifyRow == event.GetRow():
            self.NowModify = False
        
        
        UtilClass = Util()
        
        #insert
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "insert new content..":
            
            
            DBPath = ""
                
            if sys.argv[3] == "public":
                DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
            else:
                DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                
                    
            temp_listdb_con = sqlite3.connect( DBPath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select AcquiTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"

            temp_listdb_cursor.execute( SelectQuery )
            String = temp_listdb_cursor.fetchone()[0]
            if String == None:
                DecodedString = None
            else:
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
                
            
            if self.GetCellValue(event.GetRow(), 1).strip() not in str(DecodedString) and self.GetCellValue(event.GetRow(), 1).strip() != "":
            
                arr = []            
                if DecodedString == None:
                    arr.insert(0, self.table.data[event.GetRow()][1])
                    
                else:
                
                    arr = DecodedString.split("\t")
                    arr.insert(event.GetRow(), self.table.data[event.GetRow()][1])
    
                ResultString = ""
                for row in arr:
                    ResultString += row
                    ResultString += "\t"
                    
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, ResultString, "")
                    
                UpdateQuery = "update VesLocationTable set AcquiTools = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
            
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
        
                temp_listdb_con.close()
                
                self.rowcount += 1
                
            else:
                wx.MessageBox("Contents is duplicated(or blank)")
                
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
            
        else:   #modify
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AcquiTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
                
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText , self.table.data[event.GetRow()][1])
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                            
                UpdateQuery = "update VesLocationTable set AcquiTools = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

            else:
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AcquiTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
                
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText , self.table.data[event.GetRow()][1])
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                            
                UpdateQuery = "update VesLocationTable set AcquiTools = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
                  
                        
    def OnKeyDown(self, evt):
        
        UtilClass = Util()
        
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAnalysisOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
                    
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                
                if self.GetCellTextColour(self.nowSelected, 1) == '#505050':
                    wx.MessageBox("Can not delete the public content")
                    return 
                
                DBPath = ""
                
                if sys.argv[3] == "public":
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
                else:
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                    
                
                
                temp_listdb_con = sqlite3.connect( DBPath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AcquiTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
            
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText + "\t" ,"")
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                                
                UpdateQuery = "update VesLocationTable set AcquiTools = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
               
                self.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.NowVestigeLocation)

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')

    def LoadData(self, PublicPFPListFilePath, Category, AnalysisPoint, VestigeLocation):
        
        self.table.data = []
        self.NowCategory = Category
        self.NowAnalysisPoint = AnalysisPoint
        self.NowVestigeLocation = VestigeLocation
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,               # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                0,1)                                                    # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        ResultText = ""
        DBPath = ""
        
        if int(VestigeLocation) < 500000:
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath
        else:
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
        
        temp_listdb_con = sqlite3.connect( DBPath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select AcquiTools from VesLocationTable where isDeleted = 'n' and ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        try:
            ResultText = temp_listdb_cursor.fetchone()[0]
        except:
            ResultText = ""

        
        try:
            UtilClass = Util()
            ResultText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", ResultText)
        except:
            ResultText = ResultText
        
        if ResultText != None:
            
            ResultRows = ResultText.split("\t")
            
            if len(ResultRows) > 1:
                for Row in ResultRows:
                    if Row.strip() != "":
                        
                        self.table.data.append(["",Row])
                        
                        self.rowcount += 1
            
                        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                        self.table.GetView().ProcessTableMessage(msg) 
                        
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,               # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                    0,1)                                                    # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
            
                       
        if self.rowcount == 0:
            self.table.data.append(["none","insert new content.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                
        temp_listdb_con.close()
        
        
        for idx in range(0, len(self.table.data)+1):
            if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
            else:
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
                
class AnalysisDescriptionList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent

        self.table = CustomDataTable()
        
        #self.table.data.append(["","insert new content.."])
        self.table.data.append(["none","insert new content.."])
        self.rowcount = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)   
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.SetTable(self.table, True)
        
        self.NowModify = False

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):

	if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
            wx.MessageBox("sorry, can not modify public target.")
            
            return        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True and self.NowModifyRow != evt.GetRow():
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        
        
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)
        
    def OnSelect(self, event):
        
        
        window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisCategoryOnList')
        window0 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisPointOnList')
        window1 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
        window2 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
        window3 = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('AnalysisDescriptionOnList')
        
        if window.NowModify == True:
            wx.MessageBox("Fill in the blank in Category List")
            return
        
        if window0.NowModify == True:
            wx.MessageBox("Fill in the blank in Analysis Point List")
            return 
        
        if window1.NowModify == True:
            wx.MessageBox("Fill in the blank in Vestige Location List")
            return 
        
        if window2.NowModify == True:
            wx.MessageBox("Fill in the blank in Related tool List")
            return 
        
        if window3.NowModify == True and self.NowModifyRow != event.GetRow():
            wx.MessageBox("Fill in the blank in Description List")
            return 
        
        
        self.nowSelected = event.GetRow()
        self.OriginalText = self.GetCellValue(event.GetRow(), 1)

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')
    
    def OnCellChanged(self, event):

        
        
        if self.NowModify == True and self.NowModifyRow == event.GetRow():
            self.NowModify = False
        
        
        UtilClass = Util()
        
        #insert
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "insert new content..":
            
            DBPath = ""
                
            if sys.argv[3] == "public":
                DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
            else:
                DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                
                    
            temp_listdb_con = sqlite3.connect( DBPath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select Description from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
            #print SelectQuery

            temp_listdb_cursor.execute( SelectQuery )
            String = temp_listdb_cursor.fetchone()[0]
            #print String
            if String == None:
                DecodedString = None
            else:
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)

            if self.GetCellValue(event.GetRow(), 1).strip() not in str(DecodedString) and self.GetCellValue(event.GetRow(), 1).strip() != "":

                arr = []            
                if DecodedString == None:
                    arr.insert(0, self.table.data[event.GetRow()][1])
                    
                else:
                    arr = DecodedString.split("\t")
                    arr.insert(event.GetRow(), self.table.data[event.GetRow()][1])
        
                ResultString = ""
                for row in arr:
                    ResultString += row
                    ResultString += "\t"
                    
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, ResultString, "")
                    
                UpdateQuery = "update VesLocationTable set Description = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
            
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
        
                temp_listdb_con.close()
                
                self.rowcount += 1
                
            else:
                wx.MessageBox("Contents is duplicated(or blank)")
                
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
            
    
        else:   #modify
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select Description from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
                
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText , self.table.data[event.GetRow()][1])
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                            
                UpdateQuery = "update VesLocationTable set Description = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

            else: 
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select Description from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
                
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText , self.table.data[event.GetRow()][1])
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                            
                UpdateQuery = "update VesLocationTable set Description = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

    def OnKeyDown(self, evt):
        
        UtilClass = Util()
        
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
            
            if evt.GetKeyCode() == wx.WXK_RIGHT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
                    
            elif evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('VestigeLocationOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                if self.GetCellTextColour(self.nowSelected, 1) == '#505050':
                    wx.MessageBox("Can not delete the public content")
                    return 
                
                DBPath = ""
                
                if sys.argv[3] == "public":
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath   
                else:
                    DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
                    
                
                
                temp_listdb_con = sqlite3.connect( DBPath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select Description from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                DecodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", String)
            
                DecodedAndRepacedString = DecodedString.replace( self.OriginalText + "\t" ,"")
                
                EncodedString = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, DecodedAndRepacedString, "")
                                
                UpdateQuery = "update VesLocationTable set Description = '" + EncodedString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
                
    
                self.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.NowVestigeLocation)

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')

    def LoadData(self, PublicPFPListFilePath, Category, AnalysisPoint, VestigeLocation):
        
        self.table.data = []
        self.NowCategory = Category
        self.NowAnalysisPoint = AnalysisPoint
        self.NowVestigeLocation = VestigeLocation
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        if int(VestigeLocation) < 500000:
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath
        else:
            DBPath = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().UserPFPListFilePath
        
        temp_listdb_con = sqlite3.connect( DBPath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select Description from VesLocationTable where isDeleted = 'n' and ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        try:
            ResultText = temp_listdb_cursor.fetchone()[0]
        except:
            ResultText = ""
        
        
        
        try:
            UtilClass = Util()
            ResultText = UtilClass.DummyCyber(self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().DecodedDummy, "", ResultText)
        except:
            ResultText = ResultText
        
        if ResultText != None:
        
            ResultRows = ResultText.split("\t")
            
            if len(ResultRows) > 1:
                for Row in ResultRows:
                    if Row.strip() != "":
                        self.table.data.append(["",Row])
                        self.rowcount += 1
            
                        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                        self.table.GetView().ProcessTableMessage(msg) 
                    
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,               # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                    0,1)                                                    # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
            
            
                            
        if self.rowcount == 0:
            self.table.data.append(["none","insert new content.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
                
        temp_listdb_con.close()
        
        #print "VesLocation ID = " + str(self.NowVestigeLocation)
        for idx in range(0, len(self.table.data)+1):
            if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
            else:
                self.SetReadOnly(idx, 1, False)
                self.SetCellBackgroundColour(idx, 1, '#ffffff') 
                self.SetCellTextColour(idx, 1, '#000000')
	
                
class RelatedToolsForAnalysisList(gridlib.Grid):
    def __init__(self, parent, id):
        gridlib.Grid.__init__(self, parent, -1)

        self.parent = parent

        self.table = CustomDataTable()
        
        self.table.data.append(["none","not compatible with this version.."])
        self.rowcount = 0
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        gridlib.EVT_GRID_SELECT_CELL(self, self.OnSelect)    
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)   
        gridlib.EVT_GRID_LABEL_LEFT_DCLICK(self, self.OnLabelLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChanged)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.SetTable(self.table, True)

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
            
    def OnLabelLeftDClick(self, evt):
        
        
        
        if self.NowModify == True:
            
            wx.MessageBox("Fill in the blank")
            
            return
        
        self.NowModify = True
        self.NowModifyRow = evt.GetRow()
        
        
        
        if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
            wx.MessageBox("sorry, can not modify public contents.")
            
            return
        #self.table.data.append(["",""])
        self.table.data.insert(evt.GetRow(), ["",""])

        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        self.table.GetView().ProcessTableMessage(msg)
        
        self.OriginalText = ""
            
    def OnSize(self, evt):
        #self.SetMargins(0,0)
        
        self.SetRowLabelSize(30)
        size = self.parent.GetSize()
        self.SetColSize(0, 0)
        self.SetColSize(1, size.x-35)
        
    def OnSelect(self, event):
        self.nowSelected = event.GetRow()
        self.OriginalText = self.GetCellValue(event.GetRow(), 1)

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')
        
    def OnCellChanged(self, event):
        if self.OriginalText.strip("\n").strip("\r") == "" or self.OriginalText.strip("\n").strip("\r") == "not compatible with this version..":
            
            temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
            temp_listdb_cursor = temp_listdb_con.cursor()
            
            SelectQuery = "select AnalyTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"

            temp_listdb_cursor.execute( SelectQuery )
            String = temp_listdb_cursor.fetchone()[0]
            
            if self.GetCellValue(event.GetRow(), 1).strip() not in str(String) and self.GetCellValue(event.GetRow(), 1).strip() != "":
            
                arr = []            
                if String == None:
                    arr.insert(0, self.table.data[event.GetRow()][1])
                    
                else:
                    arr = String.split("\t")
                    arr.insert(event.GetRow(), self.table.data[event.GetRow()][1])
    
                ResultString = ""
                for row in arr:
                    ResultString += row
                    ResultString += "\t"
                    
                UpdateQuery = "update VesLocationTable set AnalyTools = '" + ResultString +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
            
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
        
                temp_listdb_con.close()
                
                self.rowcount += 1
                
            else:
                wx.MessageBox("Contents is duplicated(or blank)")
                
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,            # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                    0,1)                                       # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
                #print self.table.data
                del self.table.data[event.GetRow()]
                #print self.table.data
            
    
        else:   #modify
            
            if sys.argv[3] == 'public':
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AnalyTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                            
                UpdateQuery = "update VesLocationTable set AnalyTools = '" + String.replace( self.OriginalText , self.table.data[event.GetRow()][1]) +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

            else:
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AnalyTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                            
                UpdateQuery = "update VesLocationTable set AnalyTools = '" + String.replace( self.OriginalText , self.table.data[event.GetRow()][1]) +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()

    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != 127 and evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != wx.WXK_RIGHT and evt.GetKeyCode() != wx.WXK_LEFT:
            evt.Skip()
            return
        
        else:
                    
            if evt.GetKeyCode() == wx.WXK_LEFT:
            
                window = self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().FindWindowByName('RelatedToolsForAcquisitionOnList')
                window.SetFocus()

                try : 
                    window.GetSelectedRows()[0]
                except:
                    window.SetGridCursor(0,1)
            
            elif evt.GetKeyCode() == wx.WXK_RETURN:
                
                self.DisableCellEditControl()
                success = self.MoveCursorRight(evt.ShiftDown())
                
            elif evt.GetKeyCode() == 127:
                
                if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
                    wx.MessageBox("sorry, can not modify public contents.")
                    
                    return
                
                temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
                temp_listdb_cursor = temp_listdb_con.cursor()
                
                SelectQuery = "select AnalyTools from VesLocationTable where ContentsID = '" + self.NowVestigeLocation + "'"
    
                temp_listdb_cursor.execute( SelectQuery )
                String = temp_listdb_cursor.fetchone()[0]
                
                                
                UpdateQuery = "update VesLocationTable set AnalyTools = '" + String.replace( self.OriginalText + "\t" ,"") +"', ModifyTime = '" + str(int(time.time())) + "' where ContentsID = '" + self.NowVestigeLocation + "'"
        
                temp_listdb_cursor.execute( UpdateQuery )
                temp_listdb_con.commit()
                    
                temp_listdb_con.close()
                
    
                self.LoadData("", self.NowCategory, self.NowAnalysisPoint, self.NowVestigeLocation)

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'GREEN')

    def LoadData(self, PublicPFPListFilePath, Category, AnalysisPoint, VestigeLocation):
        
        """
        self.table.data = []
        self.NowCategory = Category
        self.NowAnalysisPoint = AnalysisPoint
        self.NowVestigeLocation = VestigeLocation
        
        for idx in range(1,self.rowcount):
            CurRow = self.table.GetView().GetGridCursorRow() 
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        self.rowcount = 0
        
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select AnalyTools from VesLocationTable where isDeleted = 'n' and ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        try:
            ResultText = temp_listdb_cursor.fetchone()[0]
        except:
            ResultText = ""
        
        
        temp_listdb_con = sqlite3.connect( self.parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent().PublicPFPListFilePath )
        temp_listdb_cursor = temp_listdb_con.cursor()
        
        SelectQuery = "select AnalyTools from VesLocationTable where isDeleted = 'n' and ContentsID = '" + VestigeLocation + "'"

        temp_listdb_cursor.execute( SelectQuery )
        try:
            ResultText += temp_listdb_cursor.fetchone()[0]
        except:
            ResultText += ""
            
        
        
        if ResultText != None:
            
            ResultRows = ResultText.split("\t")
            
            if len(ResultRows) > 1:
                for Row in ResultRows:
                    if Row.strip() != "":
                        self.table.data.append(["",Row])
                        self.rowcount += 1
            
                        msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                        self.table.GetView().ProcessTableMessage(msg) 
                    
                CurRow = self.table.GetView().GetGridCursorRow() 
                delmsg = gridlib.GridTableMessage(self.table,               # the table 
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                  # what was done 
                    0,1)                                                    # position, number of rows 
                self.table.GetView().ProcessTableMessage(delmsg) 
                
            
                         
        if self.rowcount == 0:
            self.table.data.append(["none","not compatible with this version.."])
            self.rowcount += 0
            
            msg = gridlib.GridTableMessage(self.table, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.table.GetView().ProcessTableMessage(msg) 
             
            delmsg = gridlib.GridTableMessage(self.table,            # the table 
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,                # what was done 
                0,1)                                       # position, number of rows 
            self.table.GetView().ProcessTableMessage(delmsg) 
            
        temp_listdb_con.close()
        
        for idx in range(0, len(self.table.data)):
            if sys.argv[3] != "public" and int(self.NowVestigeLocation) < 500000:
                self.SetReadOnly(idx, 1, True)
                self.SetCellBackgroundColour(idx, 1, '#e2e0e0') 
                self.SetCellTextColour(idx, 1, '#505050')
        """
#---------------------------------------------------------------------------

class Example(wx.Frame):
    

    def __init__(self, parent, title, ModifyFlag):    
        super(Example, self).__init__(parent, title=title, pos=(100,100), size=(1100,600))

        if sys.argv[1] == "modi":
            self.PublicPFPListOriginalFilePath = sys.argv[2]
            self.PublicPFPListFilePath = "./PFPModule/PFPLib/temp_public_modi_" + str(time.time()) + ".pfplist.sqlite"
            
            if sys.argv[3] == "public":
                self.UserPFPListOriginalFilePath = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
            else:
                self.UserPFPListOriginalFilePath = sys.argv[3]
            self.UserPFPListFilePath = "./PFPModule/PFPLib/temp_user_modi_" + str(time.time()) + ".pfplist.sqlite"
            
            #os.system("dir")
            #print "copy " + self.PublicPFPListOriginalFilePath.replace("/","\\") + " " + self.PublicPFPListFilePath.replace("/","\\") 
            #shutil.copy(self.PublicPFPListOriginalFilePath, self.PublicPFPListFilePath) 
            os.system("copy \"" + self.PublicPFPListOriginalFilePath.replace("/","\\") + "\" " + self.PublicPFPListFilePath.replace("/","\\") )
            os.system("copy \"" + self.UserPFPListOriginalFilePath.replace("/","\\") + "\" " + self.UserPFPListFilePath.replace("/","\\") )
            #print "copy " + self.PublicPFPListOriginalFilePath.replace("/","\\") + " " + self.PublicPFPListFilePath.replace("/","\\")
            
            #Popen(["copy", self.PublicPFPListOriginalFilePath.replace("/","\\"), self.PublicPFPListFilePath.replace("/","\\")])
         
            #self.PFPListXML = parse(self.PublicPFPListFilePath)
        
        """    
        elif sys.argv[1] == "new":
            self.PublicPFPListOriginalFilePath = "./PFPModule/PFPLib/Dummy.pfplist.sqlite"
            self.PublicPFPListFilePath = "./PFPModule/PFPLib/temp_new_" + str(time.time()) + ".pfplist.sqlite"
            #self.PFPListXML = parse("./PFPModule/PFPLib/Dummy.pfplist.sqlite")
            
            #shutil.copy2(self.PublicPFPListOriginalFilePath, self.PublicPFPListFilePath)
            os.system("copy " + self.PublicPFPListOriginalFilePath.replace("/","\\") + " " + self.PublicPFPListFilePath.replace("/","\\") )
            
            self.PublicPFPListOriginalFilePath = "" 
        """
        
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
        
        #InitUI()
        hbox = wx.BoxSizer(wx.VERTICAL)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        splitter2 = wx.SplitterWindow(splitter, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        splitter3 = wx.SplitterWindow(splitter2, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        splitter41 = wx.SplitterWindow(splitter3, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        splitter42 = wx.SplitterWindow(splitter3, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        
        #panel0 - Analysis Category
        panel0 = wx.Panel(splitter, -1)

        panel01 = wx.Panel(panel0, -1, size=(-1, 25))
        panel01.SetBackgroundColour('BLACK')
        st0 = wx.StaticText(panel01, -1, 'Analysis Category', (5, 5))
        st0.SetForegroundColour('WHITE')

        panel02 = wx.Panel(panel0, -1, style=wx.BORDER_SUNKEN)
        vbox00 = wx.BoxSizer(wx.VERTICAL)
        list0 = AnalysisCategoryList(panel02, -1)
        list0.SetName('AnalysisCategoryOnList')
        
        vbox00.Add(list0, 1, wx.EXPAND)
        panel02.SetSizer(vbox00)
        
        vbox01 = wx.BoxSizer(wx.VERTICAL)
        vbox01.Add(panel01, 0, wx.EXPAND)
        vbox01.Add(panel02, 1, wx.EXPAND)

        panel0.SetSizer(vbox01)

        #panel1 - Analysis Point 
        panel1 = wx.Panel(splitter2, -1)
        panel11 = wx.Panel(panel1, -1, size=(-1, 25))
        panel11.SetBackgroundColour('BLACK')
        st1 = wx.StaticText(panel11, -1, 'Analysis Point', (5, 5))
        st1.SetForegroundColour('WHITE')

        panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
        vbox10 = wx.BoxSizer(wx.VERTICAL)
        list1 = AnalysisPointList(panel12, -1)
        list1.SetName('AnalysisPointOnList')

        vbox10.Add(list1, 1, wx.EXPAND)
        panel12.SetSizer(vbox10)

        vbox11 = wx.BoxSizer(wx.VERTICAL)
        vbox11.Add(panel11, 0, wx.EXPAND)
        vbox11.Add(panel12, 1, wx.EXPAND)

        panel1.SetSizer(vbox11)

        #panel2 - Vestige Location
        panel2 = wx.Panel(splitter41, -1)
        panel21 = wx.Panel(panel2, -1, size=(-1, 25))
        panel21.SetBackgroundColour('BLACK')
        st2 = wx.StaticText(panel21, -1, 'Target', (5, 5))
        st2.SetForegroundColour('WHITE')

        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_SUNKEN)
        vbox20 = wx.BoxSizer(wx.VERTICAL)
        list2 = VestigeLocationList(panel22, -1)
        list2.SetName('VestigeLocationOnList')
        vbox20.Add(list2, 1, wx.EXPAND)
        panel22.SetSizer(vbox20)

        vbox21 = wx.BoxSizer(wx.VERTICAL)
        vbox21.Add(panel21, 0, wx.EXPAND)
        vbox21.Add(panel22, 1, wx.EXPAND)

        panel2.SetSizer(vbox21)

        #panel3 -         
        panel3 = wx.Panel(splitter41, -1)
        panel31 = wx.Panel(panel3, -1, size=(-1, 25), style=wx.NO_BORDER)
        st3 = wx.StaticText(panel31, -1, 'Related tools', (5, 5))
        #st3 = wx.StaticText(panel31, -1, 'Related tools for acquisition', (5, 5))
        st3.SetForegroundColour('WHITE')

        panel31.SetBackgroundColour('BLACK')
        panel32 = wx.Panel(panel3, -1, style=wx.BORDER_SUNKEN)
        
        vbox30 = wx.BoxSizer(wx.VERTICAL)
        list3 = RelatedToolsForAcquisitionList(panel32, -1)
        list3.SetName('RelatedToolsForAcquisitionOnList')
        vbox30.Add(list3, 1, wx.EXPAND)
        panel32.SetSizer(vbox30)

        vbox31 = wx.BoxSizer(wx.VERTICAL)
        vbox31.Add(panel31, 0, wx.EXPAND)
        vbox31.Add(panel32, 1, wx.EXPAND)

        panel3.SetSizer(vbox31)
        
        #panel4
        panel4 = wx.Panel(splitter42, -1)
        panel41 = wx.Panel(panel4, -1, size=(-1, 25), style=wx.NO_BORDER)
        #st4 = wx.StaticText(panel41, -1, 'Reserved section', (5, 5))
        st4 = wx.StaticText(panel41, -1, 'Check List', (5, 5))
        st4.SetForegroundColour('WHITE')

        panel41.SetBackgroundColour('BLACK')
        panel42 = wx.Panel(panel4, -1, style=wx.BORDER_SUNKEN)
        
        vbox40 = wx.BoxSizer(wx.VERTICAL)
        list4 = AnalysisDescriptionList(panel42, -1)
        list4.SetName('AnalysisDescriptionOnList')
        vbox40.Add(list4, 1, wx.EXPAND)
        panel42.SetSizer(vbox40)

        vbox41 = wx.BoxSizer(wx.VERTICAL)
        vbox41.Add(panel41, 0, wx.EXPAND)
        vbox41.Add(panel42, 1, wx.EXPAND)

        panel4.SetSizer(vbox41)

        #panel5        
        panel5 = wx.Panel(splitter42, -1)
        panel51 = wx.Panel(panel5, -1, size=(-1, 25), style=wx.NO_BORDER)
        st5 = wx.StaticText(panel51, -1, 'Reserved section', (5, 5))
        #st5 = wx.StaticText(panel51, -1, 'Related tools for analysis', (5, 5))
        st5.SetForegroundColour('WHITE')

        panel51.SetBackgroundColour('BLACK')
        panel52 = wx.Panel(panel5, -1, style=wx.BORDER_SUNKEN)
        
        vbox50 = wx.BoxSizer(wx.VERTICAL)
        list5 = RelatedToolsForAnalysisList(panel52, -1)
        list5.SetName('RelatedToolsForAnalysisOnList')
        vbox50.Add(list5, 1, wx.EXPAND)
        panel52.SetSizer(vbox50)

        vbox51 = wx.BoxSizer(wx.VERTICAL)
        vbox51.Add(panel51, 0, wx.EXPAND)
        vbox51.Add(panel52, 1, wx.EXPAND)

        panel5.SetSizer(vbox51)
        
        
        #panel6    
        panel6 = wx.Panel(self, -1)
        
        panel63 = wx.Panel(panel6, -1, size=(20, 25), style=wx.NO_BORDER)
        self.ButtonSave = wx.Button(panel63, size=(60, -1), label = "Save")
        self.ButtonComplete = wx.Button(panel63, size=(60, -1), label = "Complete")
        self.ButtonCancel = wx.Button(panel63, size=(60, -1), label = "Cancel")
        self.staticAuthor = wx.StaticText(panel63, -1, '   Author : ', (5, 5))
        self.TextctrlAuthor = wx.TextCtrl(panel63)
        self.staticListFilePath = wx.StaticText(panel63, -1, '   file Path : ', (5, 5))
        self.TextctrlListFilePath = wx.TextCtrl(panel63)
        self.ButtonFilePath = wx.Button(panel63, size=(40, -1), label = "...")
        vbox61 = wx.BoxSizer(wx.HORIZONTAL)
        vbox61.Add(self.ButtonSave, 0, wx.EXPAND)
        vbox61.Add(self.ButtonComplete, 0, wx.EXPAND)
        vbox61.Add(self.ButtonCancel, 0, wx.EXPAND)
        vbox61.Add(self.staticAuthor, 0, wx.EXPAND)
        vbox61.Add(self.TextctrlAuthor, 0, wx.EXPAND)
        vbox61.Add(self.staticListFilePath, 0, wx.EXPAND)
        vbox61.Add(self.TextctrlListFilePath, 1, wx.EXPAND)
        vbox61.Add(self.ButtonFilePath, 0, wx.EXPAND)
        panel63.SetSizer(vbox61)

        vbox61 = wx.BoxSizer(wx.VERTICAL)
        vbox61.Add(panel63, 0, wx.EXPAND)
        
        self.TextctrlListFilePath.SetEditable(0)
        self.ButtonSave.Bind(wx.EVT_BUTTON, self.OnButtonSave)
        self.ButtonComplete.Bind(wx.EVT_BUTTON, self.OnButtonComplete)
        self.ButtonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        self.Bind(wx.EVT_CLOSE, self.OnButtonCancel)
        self.ButtonFilePath.Bind(wx.EVT_BUTTON, self.OnFilePath)
        
        panel6.SetSizer(vbox61)
        
        if sys.argv[1] == "modi":
   
                
            self.TextctrlAuthor.Disable()
            self.TextctrlListFilePath.WriteText(self.PublicPFPListOriginalFilePath)
            self.TextctrlListFilePath.Disable()
            self.ButtonFilePath.Disable()
        
        #Window Split
        hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM)
        hbox.Add(panel6, 0, wx.EXPAND)
        
        self.SetSizer(hbox)
        self.CreateStatusBar()
        self.SetBackgroundColour('WHITE')
        
        #main Splitter
        splitter.SplitVertically(panel0, splitter2, 250)
        splitter2.SplitVertically(panel1, splitter3, 250)
        splitter3.SplitVertically(splitter41, splitter42)
        splitter3.SetSashGravity(0.5)
        splitter41.SplitHorizontally(panel2, panel3)
        splitter41.SetSashGravity(1)
        splitter42.SplitHorizontally(panel4, panel5)
        splitter42.SetSashGravity(1)
        
        #menu.. Ctrl+S
        menu = wx.Menu()        
        Save  = menu.Append(-1, "&Save\tCtrl-S")             # with accelerator
        
        menu.AppendSeparator()
        exit = menu.Append(-1, "&Quit\tCtrl-Q")
        
        self.Bind(wx.EVT_MENU, self.OnButtonSave, Save)
        self.Bind(wx.EVT_MENU, self.OnButtonCancel, exit)
                  
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&Menu")
        self.SetMenuBar(menuBar)
        
        list0.SetFocus()
        
        try : 
            list0.GetSelectedRows()[0]
        except:
            list0.SetGridCursor(0,1)
        
    def OnButtonSave(self, event):
        
        self.PublicPFPListOriginalFilePath = self.TextctrlListFilePath.GetLineText(0)
        
        if sys.argv[1] == "modi":
            
            try:
                os.remove(self.PublicPFPListOriginalFilePath)
                os.remove(self.UserPFPListOriginalFilePath)
            except:
                os.system("del " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
                os.system("del " + self.UserPFPListOriginalFilePath.replace("/","\\") )
            #shutil.copy2(self.PublicPFPListFilePath, self.PublicPFPListOriginalFilePath)
            os.system("copy " + self.PublicPFPListFilePath.replace("/","\\") + " " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
            os.system("copy " + self.UserPFPListFilePath.replace("/","\\") + " " + self.UserPFPListOriginalFilePath.replace("/","\\") )
            #os.system("copy " + self.PublicPFPListFilePath + " " + self.PublicPFPListOriginalFilePath )
            
        elif sys.argv[1] == "new":
            
            if os.path.isdir(os.path.split(self.PublicPFPListOriginalFilePath)[0]):
            
                #shutil.copy2(self.PublicPFPListFilePath, self.PublicPFPListOriginalFilePath)
                os.system("copy " + self.PublicPFPListFilePath.replace("/","\\") + " " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
                os.system("copy " + self.UserPFPListFilePath.replace("/","\\") + " " + self.UserPFPListOriginalFilePath.replace("/","\\") )
                #os.system("copy " + self.PublicPFPListFilePath + " " + self.PublicPFPListOriginalFilePath )
                
            else:
                wx.MessageBox("Please check output path.")
        
        return
        
    def OnButtonComplete(self, event):
        
        self.PublicPFPListOriginalFilePath = self.TextctrlListFilePath.GetLineText(0)
        
        if sys.argv[1] == "modi":
            
            try:
                os.remove(self.PublicPFPListOriginalFilePath)
                os.remove(self.UserPFPListOriginalFilePath)
            except:
                os.system("del " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
                os.system("del " + self.UserPFPListOriginalFilePath.replace("/","\\") )
            #shutil.copy2(self.PublicPFPListFilePath, self.PublicPFPListOriginalFilePath)
            os.system("copy " + self.PublicPFPListFilePath.replace("/","\\") + " " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
            os.system("copy " + self.UserPFPListFilePath.replace("/","\\") + " " + self.UserPFPListOriginalFilePath.replace("/","\\") )
            
            try:
                os.remove(self.PublicPFPListFilePath)
                os.remove(self.UserPFPListFilePath)
            except:
                os.system("del " + self.PublicPFPListFilePath.replace("/","\\") )
                os.system("del " + self.UserPFPListFilePath.replace("/","\\") )
            sys.exit()
        
        """    
        elif sys.argv[1] == "new":
            
            if os.path.isdir(os.path.split(self.PublicPFPListOriginalFilePath)[0]):
            
                #shutil.copy2(self.PublicPFPListFilePath, self.PublicPFPListOriginalFilePath)
                os.system("copy " + self.PublicPFPListFilePath.replace("/","\\") + " " + self.PublicPFPListOriginalFilePath.replace("/","\\") )
                
                try:
                    os.remove(self.PublicPFPListFilePath)
                except:
                    os.system("del " + self.PublicPFPListFilePath.replace("/","\\") )
                sys.exit()
            else:
                wx.MessageBox("Please check output path.")
        """
        
        return
        
    def OnButtonCancel(self, event):
        
        try:
            os.remove(self.PublicPFPListFilePath)
            os.remove(self.UserPFPListFilePath)
        except:
            os.system("del " + self.PublicPFPListFilePath.replace("/","\\") )
            os.system("del " + self.UserPFPListFilePath.replace("/","\\") )
        sys.exit()
        #self.Close()
        
        return
        
    def OnFilePath(self, event):
        dlg = wx.DirDialog(self, message="Select Target Folder", defaultPath=os.getcwd(), style=wx.OPEN)
        
        SelectedFile = ""
        if dlg.ShowModal() == wx.ID_OK:
            SelectedFile = dlg.GetPath()
            
            self.TextctrlListFilePath.WriteText(SelectedFile + "\\NewList_"+strftime("%Y%m%d%H%M%S", gmtime())+".pfplist")
            
            self.PublicPFPListOriginalFilePath = SelectedFile + "\\NewList_"+strftime("%Y%m%d%H%M%S", gmtime())+".pfplist.sqlite"
        
        return

def main():
    
    app = wx.App()
    Example(None, title="PFP List editor", ModifyFlag=sys.argv[1])
    app.MainLoop()

if __name__ == '__main__':
    main() 
    
    