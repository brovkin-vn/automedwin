import wx
import wxutil as wu
from wxast import AdaptiveStaticText
from wxutil import fh, fw

from model import EVENT


class PanelErro(wx.Panel):

    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        super().__init__(parent, -1, size=size, pos=pos)
        
        self.st_err = AdaptiveStaticText(self, label="",parent_size=size,pos=wx.Point(fw(2),fh(2)),size=wx.Size(fw(98), fh(20)), font_size=24, font_color=wu.RED)
        self.st_err.Wrap(fw(96))

        size_btn:wx.Size = size / 9
        self.btnCancel = wu.ButtonCancel(self, wx.Point(fw(2),fh(85)), size_btn)
        self.btnCancel.Bind(wx.EVT_LEFT_DOWN, self.onYesCancel)


    def onYesCancel(self, event):
        print("onCancelBtn")
        self.parent.automat.put_event(EVENT.CANCEL)

    def Show(self, show=True):
        print(f"PanelErro.Show: {self.parent.model.last_error_message=}")
        self.st_err.SetLabel(f"Произошла ошибка: {self.parent.model.last_error_message}")
        self.st_err.Wrap(fw(96))
        return super().Show(show) 

    def Hide(self):
        self.st_err.SetLabel("")
        return super().Hide()



