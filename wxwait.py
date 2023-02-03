import wx
import wxutil as wu
from wxast import AdaptiveStaticText
from wxutil import fh, fw
from model import EVENT

import wx.lib.newevent
StartTimerEvent, EVT_START_TIMER = wx.lib.newevent.NewEvent()

class PanelWait(wx.Panel):

    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        super().__init__(parent, -1, size=size, pos=pos)
        
        self.index_text = 0
        self.wait_text = [
            "Подождите, идет загрузка страницы . . .",
            "Подождите, идет загрузка страницы . .",
            "Подождите, идет загрузка страницы .",
            "Подождите, идет загрузка страницы",
        ]
        
        self.st_err = AdaptiveStaticText(self, label=self.wait_text[0] ,parent_size=size,  
            pos=wx.Point(fw(25),fh(37)), size=wx.Size(size.width-fw(4), fh()), font_size=26, 
            style=wx.ALIGN_LEFT,  font_color=wu.GRAY)
        
        size_btn:wx.Size = size / 9
        self.btnCancel = wu.ButtonCancel(self, wx.Point(fw(2),fh(85)), size_btn)
        self.btnCancel.Bind(wx.EVT_LEFT_DOWN, self.onYesCancel)

        self.timer = wx.Timer(self)
        # self.timer.Start(300)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.Bind(EVT_START_TIMER, self.onStartTimer)
    
    def onStartTimer(self, event):
        self.timer.Start(333)

    def Show(self, show=True):
        wx.PostEvent(self, StartTimerEvent())
        return super().Show(show)

    def Hide(self):
        self.timer.Stop()
        # for child in self.Children:
        #     child.Hide()
        return super().Hide()


    def onTimer(self, event):
        if self.IsShown:
            self.index_text = len(self.wait_text)-1 if self.index_text == 0 else self.index_text - 1 
            # print(f"onTimer {self.index_text=}")
            self.st_err.SetLabelText(self.wait_text[self.index_text])


    def onYesCancel(self, event):
        print("onCancelBtn")
        self.parent.automat.put_event(9876)
        self.parent.automat.put_event(EVENT.CANCEL)
        event.Skip()

