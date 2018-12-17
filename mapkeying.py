import wx
import wx.grid as wxgrid
import psycopg2


class MapKeying(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='MapKeying', size=(1200, 650),
                          style=wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION)
        self.Center()
        panel = MapPanel(self)


class MapPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # 設定背景顏色
        self.SetBackgroundColour((240, 240, 240))

        # 設定按鈕
        self.btngotoplot = wx.Button(self, label='前往/重新整理', pos=(702, 304), size=(166, 23), style=0)
        self.btnlockrelation = wx.Button(self, label='鎖定', pos=(806, 59), size=(75, 23), style=0)

        # 設定Label
        self.labeldbname = wx.StaticText(self, label='資料庫名稱', pos=(702, 20), size=(65, -1), style=wx.ALIGN_CENTRE)
        self.labelrelationname = wx.StaticText(self, label='資料表名稱', pos=(702, 40), size=(65, -1),
                                               style=wx.ALIGN_CENTRE)
        self.labelmaingrid = wx.StaticText(self, label='主格數', pos=(705, 184), size=(41, -1), style=wx.ALIGN_CENTRE)
        self.labelsubgrid = wx.StaticText(self, label='副格數', pos=(759, 184), size=(41, -1), style=wx.ALIGN_CENTRE)
        self.labelwantplot = wx.StaticText(self, label='欲輸入樣方', pos=(700, 230), size=(168, -1), style=wx.ALIGN_CENTRE)
        self.labelx1 = wx.StaticText(self, label='x1', pos=(702, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labely1 = wx.StaticText(self, label='y1', pos=(745, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labelx2 = wx.StaticText(self, label='x2', pos=(788, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labely2 = wx.StaticText(self, label='y2', pos=(831, 251), size=(37, -1), style=wx.ALIGN_CENTRE)
        self.labelentertag = wx.StaticText(self, label='欲輸入tag', pos=(700, 341), size=(100, -1),
                                           style=wx.ALIGN_CENTRE)
        self.labelquadrat = wx.StaticText(self, label='小樣方資料顯示', pos=(698, 400), size=(89, -1), style=wx.ALIGN_CENTRE)
        self.labelX = wx.StaticText(self, label='', pos=(1066, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelY = wx.StaticText(self, label='', pos=(1122, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelX.SetBackgroundColour('white')
        self.labelY.SetBackgroundColour('white')

        # 設定Textbox
        self.dbname = wx.TextCtrl(self, pos=(770, 19), size=(111, 22))
        self.relationname = wx.TextCtrl(self, pos=(700, 59), size=(100, 22))
        self.maingrid = wx.TextCtrl(self, pos=(702, 202), size=(48, 22))
        self.subgrid = wx.TextCtrl(self, pos=(756, 202), size=(48, 22))
        self.x1 = wx.TextCtrl(self, pos=(702, 276), size=(37, 22))
        self.y1 = wx.TextCtrl(self, pos=(745, 276), size=(37, 22))
        self.x2 = wx.TextCtrl(self, pos=(788, 276), size=(37, 22))
        self.y2 = wx.TextCtrl(self, pos=(831, 276), size=(37, 22))
        self.entertag = wx.TextCtrl(self, pos=(700, 367), size=(100, 22))

        # 設定表格
        self.datagrid = wxgrid.Grid(self, pos=(698, 420), size=(480, 150))
        self.datagrid.CreateGrid(0, 0)
        self.datagrid.HideRowLabels()
        self.datagrid.SetLabelBackgroundColour(wx.WHITE)

        # 設定tab順序
        taborder = (self.dbname, self.relationname, self.btnlockrelation, self.maingrid, self.subgrid, self.x1, self.y1,
                    self.x2, self.y2, self.btngotoplot, self.entertag)
        self.relationname.MoveAfterInTabOrder(self.dbname)
        for i in range(len(taborder)-1):
            taborder[i + 1].MoveAfterInTabOrder(taborder[i])

        # 設定緩衝區大小，把黑色部分消除(避免最小化、被其他視窗覆蓋導致圖形消失)
        self.buffer = wx.Bitmap(1200, 650)
        g = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        g.Clear()

        # 設定事件
        self.btngotoplot.Bind(wx.EVT_BUTTON, self.refresh)
        self.btngotoplot.Bind(wx.EVT_BUTTON, self.drawlineandoldpoint)
        self.btnlockrelation.Bind(wx.EVT_BUTTON, self.lockrelation)
        self.Bind(wx.EVT_MOTION, self.movemouse)
        self.Bind(wx.EVT_LEFT_DOWN, self.drawpoint)
        self.Bind(wx.EVT_PAINT, self.bufferpaint)

        self.dbnametext = ''
        self.relationnametext = ''

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
                except Exception:
                    wx.MessageBox('資料庫或資料表名稱錯誤或未鎖定!')
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
                    for i in range(0, len(plotrows)):
                        if plotrows[i][7] is None or plotrows[i][8] is None:
                            continue
                        else:
                            g.DrawEllipse(int(plotrows[i][7]) + 50, 500 - int(plotrows[i][8]) + 50, 3, 3)
                            g.DrawText(taglist[i], int(plotrows[i][7]) + 50 + 2, 500 - int(plotrows[i][8]) + 50 + 2)

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
                            self.datagrid.SetCellValue(p, j, str(plotrows[p][j]))
                            self.datagrid.SetReadOnly(p, j)
                            self.datagrid.DisableRowResize(p)

                    for p in range(0, len(colnames)):
                        self.datagrid.SetColLabelValue(p, colnames[p][0])
                        self.datagrid.AutoSizeColumn(p)
                        self.datagrid.DisableColResize(p)

    def movemouse(self, event):
        x, y = self.ScreenToClient(wx.GetMousePosition())
        self.labelX.SetLabel(str(x-50))
        self.labelY.SetLabel(str(500-y+50))

    def refresh(self, event):
        self.Refresh()

    def lockrelation(self, event):
        if self.relationname.Enabled and self.dbname.Enabled:
            self.dbnametext = self.dbname.GetValue()
            self.relationnametext = self.relationname.GetValue()
            self.relationname.Enabled = False
            self.dbname.Enabled = False
            self.btnlockrelation.SetLabel('解除鎖定')
        else:
            self.dbname.Enabled = True
            self.relationname.Enabled = True
            self.btnlockrelation.SetLabel('鎖定')

    def drawpoint(self, event):
        x3 = int(self.labelX.GetLabel())
        y3 = int(self.labelY.GetLabel())
        tag = str(self.entertag.GetValue())
        if tag == '':
            return

        if x3 > 500 or x3 < 0 or y3 > 500 or y3 < 0:
            wx.MessageBox('超出範圍!', caption='超出範圍警告')
            return
        elif self.x1.GetValue() != '' and self.y1.GetValue() != '' and self.x2.GetValue() != '' \
                and self.y2.GetValue() != '' and tag.strip():

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
                cur.execute('update plotdata set "x3"=\'' + str(x3) + '\' where "tag"=\'' + tag + '\'')
                conn.commit()
                cur.execute('update plotdata set "y3"=\'' + str(y3) + '\' where "tag"=\'' + tag + '\'')
                conn.commit()
                conn.close()
            else:
                wx.MessageBox('此小樣方無此資料!')

    def bufferpaint(self, event):
        wx.BufferedPaintDC(self, self.buffer)


if __name__ == '__main__':
    app = wx.App()
    frame = MapKeying(None)
    frame.Show(True)
    app.MainLoop()
