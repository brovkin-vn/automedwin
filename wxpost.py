import wx
import wxutil as wu
from model import EVENT
from wxutil import fh, fw

class PanelPost(wx.Panel):
    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        size = size
        path = "images/postermed.png"
        bitmap = wx.Bitmap(path)
        bitmap = wu.scale_bitmap(bitmap, size)

        super(wx.Panel, self).__init__(parent, -1, size = size, pos=pos)
        sb = wu.ScaleBitmap(self, path, size) 

        size_btn:wx.Size = size / 9
        size_btn:wx.Size = size / 9
        # self.btnCancel = wu.ButtonCancel(self, wx.Point(fw(2),fh(80)), size_btn)

        # pos_btn = wx.Point(20, size.height - size_btn.height - 20)
        self.btn = wu.ButtonTest(sb, wx.Point(fw(2),fh(85)), size_btn)
        self.btn.Bind(wx.EVT_LEFT_UP, self.onTestBtn)

    def onTestBtn(self, event):
        print("onTestBtn")
        self.parent.automat.put_event(EVENT.TEST)
        event.Skip()
