import wx
from model import EVENT
import wxutil as wu

class PanelPiro(wx.Panel):
    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        size = size
        path = "images/posterpiro.png"
        bitmap = wx.Bitmap(path)
        bitmap = wu.scale_bitmap(bitmap, size)

        super(wx.Panel, self).__init__(parent, -1, pos=pos, size = size)
        sb = wu.ScaleBitmap(self, path, size) 
        
        size_btn:wx.Size = size / 9
        pos_btn = wx.Point(size.width - size_btn.width - 30, size.height - size_btn.height - 10)
        self.btn = wu.ButtonCancel(sb, pos_btn, size_btn)
        self.btn.Bind(wx.EVT_LEFT_DOWN, self.onCancelBtn)

    def onCancelBtn(self, event):
        self.parent.automat.put_event(EVENT.CANCEL)
        event.Skip()
