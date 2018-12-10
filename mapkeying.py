import wx


class MapKeying(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='MapKeying', size=(1200, 650))
        self.Center()
        panel = MapPanel(self)


class MapPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(1200, 650))

        self.SetBackgroundColour((204, 204, 204))

        self.gotoplot = wx.Button(self, label='前往/重新整理', pos=(702, 304), size=(166, 23), style=0)
        self.lockrelation = wx.Button(self, label='鎖定', pos=(806, 59), size=(75, 23), style=0)

        self.labeldbname = wx.StaticText(self, label='資料庫名稱', pos=(702, 20), size=(65, -1), style=wx.ALIGN_CENTRE)
        self.labelrelationname = wx.StaticText(self, label='資料表名稱', pos=(702, 40), size=(65, -1),
                                               style=wx.ALIGN_CENTRE)
        self.labelmaingrid = wx.StaticText(self, label='主格數', pos=(705, 184), size=(41, -1), style=wx.ALIGN_CENTRE)
        self.labelsubgrid = wx.StaticText(self, label='副格數', pos=(759, 184), size=(41, -1), style=wx.ALIGN_CENTRE)
        self.labelX = wx.StaticText(self, label='', pos=(1066, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelY = wx.StaticText(self, label='', pos=(1122, 579), size=(50, -1), style=wx.ALIGN_CENTRE)
        self.labelX.SetBackgroundColour("white")
        self.labelY.SetBackgroundColour("white")

        self.dbname = wx.TextCtrl(self, pos=(700, 59), size=(100, 22))
        self.relationname = wx.TextCtrl(self, pos=(770, 19), size=(111, 22))
        self.maingrid = wx.TextCtrl(self, pos=(702, 202), size=(48, 22))
        self.subgrid = wx.TextCtrl(self, pos=(756, 202), size=(48, 22))

        self.gotoplot.Bind(wx.EVT_BUTTON, self.changetext)
        self.lockrelation.Bind(wx.EVT_BUTTON, self.lock_relation)
        self.Bind(wx.EVT_MOTION, self.movemouse)
        self.Bind(wx.EVT_PAINT, self.drawline)

    def drawline(self, event):
        if not str.isnumeric(self.maingrid.GetValue()) or not str.isnumeric(self.subgrid.GetValue()):
            return
        elif int(self.maingrid.GetValue() == 0) or int(self.subgrid.GetValue() == 0):
            return
        else:
            pn = 500/int(self.maingrid.GetValue())
            pm = 500/int(self.maingrid.GetValue())/int(self.subgrid.GetValue())
            k = int(self.maingrid.GetValue())*int(self.subgrid.GetValue())
            g = wx.PaintDC(self)
            g.Clear()
            g.SetPen(wx.Pen(wx.BLACK, 1))
            for i in range(0, k+1):
                g.DrawLine(50, 50+pm*i, 550, 50+pm*i)
                g.DrawLine(50+pm*i, 50, 50+pm*i, 550)
            g.SetPen(wx.Pen(wx.RED, 2))
            for i in range(0, int(self.maingrid.GetValue())+1):
                g.DrawLine(50, 50+pn*i, 550, 50+pn*i)
                g.DrawLine(50+pn*i, 50, 50+pn*i, 550)

    def movemouse(self, event):
        x, y = self.ScreenToClient(wx.GetMousePosition())
        self.labelX.SetLabel(str(x-50))
        self.labelY.SetLabel(str(500-y+50))

    def changetext(self, event):
        self.Refresh()

    def lock_relation(self, event):
        if self.relationname.Enabled and self.dbname.Enabled:
            self.relationname.Enabled = False
            self.dbname.Enabled = False
            self.lockrelation.SetLabel('解除鎖定')
        else:
            self.dbname.Enabled = True
            self.relationname.Enabled = True
            self.lockrelation.SetLabel('鎖定')


if __name__ == '__main__':
    app = wx.App()
    frame = MapKeying(None)
    frame.Show(True)
    app.MainLoop()

