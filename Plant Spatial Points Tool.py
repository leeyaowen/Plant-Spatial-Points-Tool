import wx
import wx.grid as wxgrid
import psycopg2


class MapKeying(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Plant Spatial Points Tool', size=(1200, 650),
                          style=wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION)
        self.Center()
        panel = MapPanel(self)


class MapPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # set background color
        self.SetBackgroundColour((240, 240, 240))

        # set Groupbox
        self.plotsizebox = wx.StaticBox(self, label='Area size', pos=(700, 90), size=(152, 88))
        self.newdtbox = wx.StaticBox(self, label='New data detail', pos=(905, 44), size=(192, 254))
        self.deletedtbox = wx.StaticBox(self, label='Delete tag', pos=(905, 333), size=(192, 88))

        # set button
        self.btnlockrelation = wx.Button(self, label='lock', pos=(806, 59), size=(75, 23), style=0)
        self.btngotoplot = wx.Button(self, label='Go/Refresh', pos=(702, 304), size=(166, 23), style=0)
        self.newdt = wx.Button(self, label='Add data', pos=(905, 15), size=(73, 23))
        self.newconfirm = wx.Button(self.newdtbox, label='Confirm', pos=(21, 212), size=(147, 23))
        self.deletedt = wx.Button(self, label='Delete data', pos=(905, 304), size=(75, 23))
        self.deleteconfirm = wx.Button(self.deletedtbox, label='Confirm', pos=(21, 49), size=(147, 23))

        # set Label
        self.labeldbname = wx.StaticText(self, label='Database', pos=(702, 20), size=(65, -1), style=wx.ALIGN_CENTRE)
        self.labelrelationname = wx.StaticText(self, label='Relation', pos=(702, 40), size=(65, -1),
                                               style=wx.ALIGN_CENTRE)
        self.labelmaingrid = wx.StaticText(self, label='grid.major', pos=(705, 184), size=(60, -1), style=wx.ALIGN_CENTRE)
        self.labelsubgrid = wx.StaticText(self, label='grid.minor', pos=(780, 184), size=(60, -1), style=wx.ALIGN_CENTRE)
        self.labelwantplot = wx.StaticText(self, label='Quadrat position', pos=(700, 230), size=(168, -1), style=wx.ALIGN_CENTRE)
        self.labelx1 = wx.StaticText(self, label='x1', pos=(702, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labely1 = wx.StaticText(self, label='y1', pos=(745, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labelx2 = wx.StaticText(self, label='x2', pos=(788, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labely2 = wx.StaticText(self, label='y2', pos=(831, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labelentertag = wx.StaticText(self, label='Target tag', pos=(700, 341), size=(100, -1),
                                           style=wx.ALIGN_CENTRE)
        self.labelquadrat = wx.StaticText(self, label='Current data', pos=(698, 420), size=(89, -1), style=wx.ALIGN_CENTRE)
        self.labelX = wx.StaticText(self, label='', pos=(1066, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelY = wx.StaticText(self, label='', pos=(1122, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelX.SetBackgroundColour('white')
        self.labelY.SetBackgroundColour('white')
        self.labelnewdtx1 = wx.StaticText(self.newdtbox, label='x1', pos=(19, 21), size=(17, -1))
        self.labelnewdty1 = wx.StaticText(self.newdtbox, label='y1', pos=(19, 49), size=(17, -1))
        self.labelnewdtx2 = wx.StaticText(self.newdtbox, label='x2', pos=(19, 77), size=(17, -1))
        self.labelnewdty2 = wx.StaticText(self.newdtbox, label='y2', pos=(19, 105), size=(17, -1))
        self.labelnewdttag = wx.StaticText(self.newdtbox, label='tag', pos=(19, 133), size=(19, -1))
        self.labelnewdtsp = wx.StaticText(self.newdtbox, label='sp', pos=(19, 161), size=(15, -1))
        self.labelnewdtdbh = wx.StaticText(self.newdtbox, label='dbh', pos=(19, 189), size=(23, -1))
        self.labeldeletetag = wx.StaticText(self.deletedtbox, label='tag', pos=(19, 25), size=(20, -1))

        # set Textbox
        self.dbname = wx.TextCtrl(self, pos=(770, 19), size=(111, 22))
        self.relationname = wx.TextCtrl(self, pos=(700, 59), size=(100, 22))
        self.maingrid = wx.TextCtrl(self, pos=(702, 202), size=(48, 22))
        self.subgrid = wx.TextCtrl(self, pos=(780, 202), size=(48, 22))
        self.x1 = wx.TextCtrl(self, pos=(702, 276), size=(37, 22))
        self.y1 = wx.TextCtrl(self, pos=(745, 276), size=(37, 22))
        self.x2 = wx.TextCtrl(self, pos=(788, 276), size=(37, 22))
        self.y2 = wx.TextCtrl(self, pos=(831, 276), size=(37, 22))
        self.entertag = wx.TextCtrl(self, pos=(700, 367), size=(100, 22))
        self.newx1 = wx.TextCtrl(self.newdtbox, pos=(68, 16), size=(100, 22))
        self.newy1 = wx.TextCtrl(self.newdtbox, pos=(68, 44), size=(100, 22))
        self.newx2 = wx.TextCtrl(self.newdtbox, pos=(68, 72), size=(100, 22))
        self.newy2 = wx.TextCtrl(self.newdtbox, pos=(68, 100), size=(100, 22))
        self.newtag = wx.TextCtrl(self.newdtbox, pos=(68, 128), size=(100, 22))
        self.newsp = wx.TextCtrl(self.newdtbox, pos=(68, 156), size=(100, 22))
        self.newdbh = wx.TextCtrl(self.newdtbox, pos=(68, 184), size=(100, 22))
        self.deletetag = wx.TextCtrl(self.deletedtbox, pos=(68, 21), size=(100, 22))

        # set table
        self.datagrid = wxgrid.Grid(self, pos=(698, 445), size=(480, 120))
        self.datagrid.CreateGrid(0, 0)
        self.datagrid.HideRowLabels()
        self.datagrid.SetLabelBackgroundColour(wx.WHITE)

        # set Radiobutton
        self.plotsize1 = wx.RadioButton(self.plotsizebox, label='1x1', pos=(11, 21), size=(47, 16))
        self.plotsize10 = wx.RadioButton(self.plotsizebox, label='5x5', pos=(11, 43), size=(47, 16))
        self.plotsize20 = wx.RadioButton(self.plotsizebox, label='10x10', pos=(11, 66), size=(59, 16))
        self.plotsize10.SetValue(True)

        # set tab sort
        taborder = (self.dbname, self.relationname, self.btnlockrelation, self.maingrid, self.subgrid, self.x1,
                    self.y1, self.x2, self.y2, self.btngotoplot, self.entertag)
        for i in range(0, len(taborder)-1):
            taborder[i + 1].MoveAfterInTabOrder(taborder[i])

        # 設定緩衝區大小，把黑色部分消除(避免最小化、被其他視窗覆蓋導致圖形消失)
        self.buffer = wx.Bitmap(1200, 650)
        g = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        g.Clear()

        # bind event
        self.btngotoplot.Bind(wx.EVT_BUTTON, self.drawlineandoldpoint)
        self.btnlockrelation.Bind(wx.EVT_BUTTON, self.lockrelation)
        self.newdt.Bind(wx.EVT_BUTTON, self.newdtclick)
        self.newconfirm.Bind(wx.EVT_BUTTON, self.newconfirmclick)
        self.deletedt.Bind(wx.EVT_BUTTON, self.deletedtclick)
        self.deleteconfirm.Bind(wx.EVT_BUTTON, self.deleteconfrimclick)
        self.plotsize1.Bind(wx.EVT_RADIOBUTTON, self.size1change)
        self.plotsize10.Bind(wx.EVT_RADIOBUTTON, self.size10change)
        self.plotsize20.Bind(wx.EVT_RADIOBUTTON, self.size20change)
        self.Bind(wx.EVT_MOTION, self.movemouse)
        self.Bind(wx.EVT_LEFT_DOWN, self.drawpoint)
        self.Bind(wx.EVT_PAINT, self.bufferpaint)
        self.dbname.SetFocus()

        # set parameter
        self.dbnametext = ''
        self.relationnametext = ''
        self.plotsize = 10
        self.newdtbox.Enabled = False
        self.deletedtbox.Enabled = False

    # draw lines/points and table
    def drawlineandoldpoint(self, event):
        maingridvalue = self.maingrid.GetValue()
        subgridvalue = self.subgrid.GetValue()

        if not str.isnumeric(maingridvalue) or not str.isnumeric(subgridvalue):
            return
        elif int(maingridvalue == 0) or int(subgridvalue == 0):
            return
        else:
            pn = 500/int(maingridvalue)
            pm = 500/int(maingridvalue)/int(subgridvalue)
            k = int(maingridvalue)*int(subgridvalue)
            g = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            g.Clear()
            g.SetPen(wx.Pen(wx.BLACK, 1))
            for i in range(0, k+1):
                g.DrawLine(50, 50+pm*i, 550, 50+pm*i)
                g.DrawLine(50+pm*i, 50, 50+pm*i, 550)
            g.SetPen(wx.Pen(wx.RED, 2))
            for i in range(0, int(maingridvalue)+1):
                g.DrawLine(50, 50+pn*i, 550, 50+pn*i)
                g.DrawLine(50+pn*i, 50, 50+pn*i, 550)

            if self.x1.GetValue() != '' and self.y1.GetValue() != '' and self.x2.GetValue() != '' and \
                    self.y2.GetValue() != '':

                # noinspection PyBroadException
                try:
                    conn = psycopg2.connect(database=self.dbnametext, user='postgres', password='2717484',
                                            host='localhost', port='5432')
                    cur = conn.cursor()
                    cur.execute('select * from ' + self.relationnametext + ' where "x1"=\'' + self.x1.GetValue() +
                                '\' and "y1"=\'' + self.y1.GetValue() + '\' and "x2"=\'' + self.x2.GetValue() +
                                '\' and "y2"=\'' + self.y2.GetValue() + '\'')
                    # x1value = "'%s'" % (self.x1.GetValue())
                    # cur.execute("select * from %s where x1 = %s and y1 = %s and x2 = %s and y2 = %s" %
                    #             (self.relationnametext, x1value, '\'' + self.y1.GetValue() +
                    #              '\'', '\'' + self.x2.GetValue() + '\'', '\'' + self.y2.GetValue() + '\''))
                except Exception:
                    wx.MessageBox('database or relation error!')
                else:
                    plotrows = cur.fetchall()
                    taglist = []
                    colnames = cur.description
                    conn.close()
                    for i in range(0, len(plotrows)):
                        taglist.append(plotrows[i][4])

                    g = wx.BufferedDC(wx.ClientDC(self), self.buffer)
                    g.SetPen(wx.Pen(wx.BLUE, 1))
                    g.SetBrush(wx.Brush('grey', style=wx.BRUSHSTYLE_TRANSPARENT))
                    g.SetTextForeground(wx.BLUE)
                    if self.plotsize == 1:
                        for i in range(0, len(plotrows)):
                            if plotrows[i][7] is None or plotrows[i][8] is None:
                                continue
                            else:
                                g.DrawEllipse(float(plotrows[i][7])*5 + 50, 500 - float(plotrows[i][8])*5 + 50, 3, 3)
                                g.DrawText(taglist[i], float(plotrows[i][7])*5 + 50 + 2, 500 - float(plotrows[i][8])*5 +
                                           50 + 2)
                    elif self.plotsize == 10:
                        for i in range(0, len(plotrows)):
                            if plotrows[i][7] is None or plotrows[i][8] is None:
                                continue
                            else:
                                g.DrawEllipse(int(plotrows[i][7]) + 50, 500 - int(plotrows[i][8]) + 50, 3, 3)
                                g.DrawText(taglist[i], int(float(plotrows[i][7])) + 50 + 2, 500 - int(float(plotrows[i][8])) + 50 + 2)
                    elif self.plotsize == 20:
                        for i in range(0, len(plotrows)):
                            if plotrows[i][7] is None or plotrows[i][8] is None:
                                continue
                            else:
                                g.DrawEllipse(int(plotrows[i][7])/2 + 50, 500 - int(plotrows[i][8])/2 + 50, 3, 3)
                                g.DrawText(taglist[i], int(plotrows[i][7])/2 + 50 + 2, 500 - int(plotrows[i][8])/2 +
                                           50 + 2)

                    currentcol, newcol = (self.datagrid.GetNumberCols(), len(colnames))
                    if newcol < currentcol:
                        self.datagrid.DeleteCols(0, currentcol - newcol)
                    if newcol > currentcol:
                        self.datagrid.AppendCols(newcol - currentcol)
                    currentrow, newrow = (self.datagrid.GetNumberRows(), len(plotrows))
                    if newrow < currentrow:
                        self.datagrid.DeleteRows(0, currentrow - newrow)
                    if newrow > currentrow:
                        self.datagrid.AppendRows(newrow - currentrow)

                    for p in range(0, len(plotrows)):
                        for j in range(0, len(colnames)):
                            if plotrows[p][j] is None:
                                self.datagrid.SetCellValue(p, j, str(''))
                            else:
                                self.datagrid.SetCellValue(p, j, str(plotrows[p][j]))
                                self.datagrid.SetReadOnly(p, j)
                                self.datagrid.DisableRowResize(p)

                    for p in range(0, len(colnames)):
                        self.datagrid.SetColLabelValue(p, colnames[p][0])
                        self.datagrid.AutoSizeColumn(p)
                        self.datagrid.DisableColResize(p)

    # mouse position
    def movemouse(self, event):
        x, y = self.ScreenToClient(wx.GetMousePosition())
        self.labelX.SetLabel(str(x-50))
        self.labelY.SetLabel(str(500-y+50))

    # database and relation lock/unlock
    def lockrelation(self, event):
        if self.relationname.Enabled and self.dbname.Enabled:
            self.dbnametext = self.dbname.GetValue()
            self.relationnametext = self.relationname.GetValue()
            self.relationname.Enabled = False
            self.dbname.Enabled = False
            self.btnlockrelation.SetLabel('unlock')
        else:
            self.dbname.Enabled = True
            self.relationname.Enabled = True
            self.btnlockrelation.SetLabel('lock')

    # draw points
    def drawpoint(self, event):
        x3 = int(self.labelX.GetLabel())
        y3 = int(self.labelY.GetLabel())
        tag = str(self.entertag.GetValue())
        if tag == '':
            return

        if x3 > 500 or x3 < 0 or y3 > 500 or y3 < 0:
            wx.MessageBox('out of range!', caption='out of range')
            return
        elif self.x1.GetValue() != '' and self.y1.GetValue() != '' and self.x2.GetValue() != '' \
                and self.y2.GetValue() != '' and tag.strip() != '':

            conn = psycopg2.connect(database=self.dbnametext, user='postgres', password='2717484',
                                    host='localhost', port='5432')
            cur = conn.cursor()
            cur.execute('select tag from ' + self.relationnametext + ' where "x1"=\'' + self.x1.GetValue() +
                        '\' and "y1"=\'' + self.y1.GetValue() + '\' and "x2"=\'' + self.x2.GetValue() +
                        '\' and "y2"=\'' + self.y2.GetValue() + '\'')
            tagrows = cur.fetchall()
            taglist = []
            for i in range(0, len(tagrows)):
                taglist.append(tagrows[i][0])
            if str(self.entertag.GetValue()) in taglist:
                x, y = self.ScreenToClient(wx.GetMousePosition())
                g = wx.BufferedDC(wx.ClientDC(self), self.buffer)
                g.SetPen(wx.Pen(wx.BLUE, 1))
                g.SetBrush(wx.Brush('grey', style=wx.BRUSHSTYLE_TRANSPARENT))
                g.DrawEllipse(x, y, 3, 3)
                g.SetTextForeground(wx.BLUE)
                g.DrawText(tag, x+2, y+2)
                if self.plotsize == 1:
                    cur.execute('update ' + self.relationnametext + ' set "x3"=\'' + str(x3/5) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                    cur.execute('update ' + self.relationnametext + ' set "y3"=\'' + str(y3/5) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                elif self.plotsize == 10:
                    cur.execute('update ' + self.relationnametext + ' set "x3"=\'' + str(x3) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                    cur.execute('update ' + self.relationnametext + ' set "y3"=\'' + str(y3) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                elif self.plotsize == 20:
                    cur.execute('update ' + self.relationnametext + ' set "x3"=\'' + str(x3*2) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                    cur.execute('update ' + self.relationnametext + ' set "y3"=\'' + str(y3*2) + '\' where "tag"=\'' +
                                tag + '\'')
                    conn.commit()
                conn.close()
            else:
                wx.MessageBox('no data in this quadrat!')
                conn.close()

    def bufferpaint(self, event):
        wx.BufferedPaintDC(self, self.buffer)

    def newdtclick(self, event):
        if self.dbnametext == '':
            wx.MessageBox('no database')
            return

        self.newdtbox.Enabled = True
        self.newx1.SetFocus()

        conn = psycopg2.connect(database=self.dbnametext, user='postgres', password='2717484',
                                host='localhost', port='5432')
        cur = conn.cursor()
        cur.execute('select distinct "sp" from ' + self.relationnametext)
        sprows = cur.fetchall()
        splist = []
        conn.close()
        for i in range(0, len(sprows)):
            splist.append(sprows[i][0])
        self.newsp.AutoComplete(splist)

    def newconfirmclick(self, event):
        if str(self.newx1.GetValue()).strip() == '' or str(self.newy1.GetValue()).strip() == '' or \
                str(self.newx2.GetValue()).strip() == '' or str(self.newy2.GetValue()).strip() == '' or \
                str(self.newtag.GetValue()).strip() == '' or str(self.newsp.GetValue()).strip() == '':
            wx.MessageBox('data not enough!')
            self.newdtbox.Enabled = False
            return

        x1 = str(self.newx1.GetValue()).strip()
        y1 = str(self.newy1.GetValue()).strip()
        x2 = str(self.newx2.GetValue()).strip()
        y2 = str(self.newy2.GetValue()).strip()
        tag = str(self.newtag.GetValue()).strip()
        sp = str(self.newsp.GetValue()).strip()
        dbh = str(self.newdbh.GetValue()).strip()

        # noinspection PyBroadException
        try:
            conn = psycopg2.connect(database=self.dbnametext, user='postgres', password='2717484',
                                    host='localhost', port='5432')
            cur = conn.cursor()
            cur.execute('insert into ' + self.relationnametext + ' ("x1","y1","x2","y2","tag","sp","dbh") values ' +
                        '(\'' + x1 + '\',\'' + y1 + '\',\'' + x2 + '\',\'' + y2 + '\',\'' + tag + '\',\'' +
                        sp + '\',' + dbh + ')')
            conn.commit()
            conn.close()
            wx.MessageBox('Successfully added!')
            self.newx1.SetValue('')
            self.newy1.SetValue('')
            self.newx2.SetValue('')
            self.newy2.SetValue('')
            self.newtag.SetValue('')
            self.newsp.SetValue('')
            self.newdbh.SetValue('')
            self.newdtbox.Enabled = False
            self.drawlineandoldpoint(event)
        except Exception as err:
            wx.MessageBox(str(err))

    def deletedtclick(self, event):
        if self.dbnametext == '':
            wx.MessageBox('no database')
            return
        self.deletedtbox.Enabled = True
        self.deletetag.SetFocus()

    def deleteconfrimclick(self, event):
        if self.x1.GetValue() != '' and self.y1.GetValue() != '' and self.x2.GetValue() != '' \
                and self.y2.GetValue() != '' and self.deletetag.GetValue() != '':
            conn = psycopg2.connect(database=self.dbnametext, user='postgres', password='2717484',
                                    host='localhost', port='5432')
            cur = conn.cursor()
            cur.execute('select tag from ' + self.relationnametext + ' where "x1"=\'' + self.x1.GetValue() +
                        '\' and "y1"=\'' + self.y1.GetValue() + '\' and "x2"=\'' + self.x2.GetValue() +
                        '\' and "y2"=\'' + self.y2.GetValue() + '\'')
            tagrows = cur.fetchall()
            deletetaglist = []
            for i in range(0, len(tagrows)):
                deletetaglist.append(tagrows[i][0])
            if str(self.deletetag.GetValue()) in deletetaglist:
                cur.execute('delete from ' + self.relationnametext + ' where tag = \'' + self.deletetag.GetValue() +
                            '\'')
                conn.commit()
                conn.close()
                wx.MessageBox('Successfully deleted')
                self.deletetag.SetValue('')
                self.deletedtbox.Enabled = False
                self.drawlineandoldpoint(event)
            else:
                conn.close()
                wx.MessageBox('tag not in this quadrat!')
                self.deletetag.SetValue('')
                self.deletedtbox.Enabled = False
        else:
            wx.MessageBox('go to target quadrat or type target tag first')
            self.deletedtbox.Enabled = False

    def size1change(self, event):
        self.plotsize = 1

    def size10change(self, event):
        self.plotsize = 10

    def size20change(self, event):
        self.plotsize = 20


if __name__ == '__main__':
    app = wx.App()
    frame = MapKeying(None)
    frame.Show(True)
    app.MainLoop()
