import wx
from model import EVENT
import wxutil as wu
from wxast import AdaptiveStaticText
from wxutil import fh, fw



class PanelSave(wx.Panel):
    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        size = size
        path = "images/logo.png"
        bitmap = wx.Bitmap(path)
        bitmap = wu.scale_bitmap(bitmap, size)

        super(wx.Panel, self).__init__(parent, -1, pos=pos, size = size)
        wu.ScaleBitmap(self, path, wx.Size(size.width//6, size.height//20), pos=((size.width - size.width // 6) // 2, fh(3)))

        wx.StaticLine(self, -1, pos = wx.Point(fw(), fh(10)), size=wx.Size(size.width - fw(2), 3))

        self.st = []


        self.st.append(AdaptiveStaticText(self, label="МЕДОСМОТР ПРОЙДЕН", parent_size=size, pos=wx.Point(0,fh(13)), size=wx.Size(size.width, fh(5)), style=wx.ALIGN_CENTER_HORIZONTAL, font_size=36, font_color=wu.GREEN))

        labels = [
            "ВРЕМЯ ИЗМЕРЕНИЯ:", 
            "ТЕМПЕРАТУРА:", 
            "АЛКОГОЛЬ:",
            "ВЕРХНЕЕ:",
            "НИЖНЕЕ:",
            "ПУЛЬС:",
            "АРИТМИЯ:",
            "ГИПЕРТОНИЯ:"]
        for i, label in enumerate(labels):
            AdaptiveStaticText(self, label, parent_size=size, pos=wx.Point(0,fh(23+(6*i))), size=wx.Size(size.width//2-fw(), fh()), style=wx.ALIGN_RIGHT, font_size=26, font_color=wu.BLUE)
            self.st.append(AdaptiveStaticText(self, "Н/Д", size, pos=wx.Point(size.width//2+fw()*2,fh(23+(6*i))), size=wx.Size(size.width//2-4*fw(), fh()), font_size=26, font_color=wu.GRAY))

        wx.StaticLine(self, -1, pos = wx.Point(fw(), fh(73)), size=wx.Size(size.width - fw(2), 3))

        AdaptiveStaticText(self, label="Подтвердите отсуттвие жалоб на самочувствие", parent_size=size, pos=wx.Point(size.width//4,fh(76+5*0)), size=wx.Size(size.width//2, fh(4)), style=wx.ALIGN_CENTER_HORIZONTAL, font_size=20, font_color=wu.GRAY)
        AdaptiveStaticText(self, label="нажмите кнопку НЕТ"                         , parent_size=size, pos=wx.Point(size.width//4,fh(76+5*1)), size=wx.Size(size.width//2, fh(4)), style=wx.ALIGN_CENTER_HORIZONTAL, font_size=20, font_color=wu.GREEN)
        AdaptiveStaticText(self, label="Либо пожалуйтесь на самочувствие"           , parent_size=size, pos=wx.Point(size.width//4,fh(76+5*2)), size=wx.Size(size.width//2, fh(4)), style=wx.ALIGN_CENTER_HORIZONTAL, font_size=20, font_color=wu.GRAY)
        AdaptiveStaticText(self, label="нажмите кнопку ДА"                          , parent_size=size, pos=wx.Point(size.width//4,fh(76+5*3)), size=wx.Size(size.width//2, fh(4)), style=wx.ALIGN_CENTER_HORIZONTAL, font_size=20, font_color=wu.RED)

        wx.StaticLine(self, -1, pos = wx.Point(fw(), fh(98)), size=wx.Size(size.width - fw(2), 3))

        size_btn:wx.Size = size / 8
        self.btnYes = wu.ButtonYes(self, wx.Point(fw(2),fh(80)), size_btn)
        self.btnYes.Bind(wx.EVT_LEFT_DOWN, self.onYesBtn)
        self.btnNo = wu.ButtonNo(self, wx.Point(size.width-fw(4)-size_btn.width,fh(80)), size_btn)
        self.btnNo.Bind(wx.EVT_LEFT_DOWN, self.onNoBtn)

    def onYesBtn(self, event):
        print("wxsave onYeslBtn " + event.GetEventObject().GetName())
        self.parent.automat.put_event(EVENT.BTN_YES)
        event.Skip()

    def onNoBtn(self, event):
        print("wxsave onNoBtn " + event.GetEventObject().GetName())
        self.parent.automat.put_event(EVENT.BTN_NO)
        event.Skip()


    def Show(self, show=True):
        self.st[0].SetLabel("МЕДОСМОТР ПРОЙДЕН")
        # "ВРЕМЯ ИЗМЕРЕНИЯ:", 
        self.st[1].SetLabel(self.parent.model.pump_data["T"] )
        # "ТЕМПЕРАТУРА:", 
        self.st[2].SetLabel(self.parent.model.piro_data)
        # "АЛКОГОЛЬ:",
        self.st[3].SetLabel("--")
        # "ВЕРХНЕЕ:",
        self.st[4].SetLabel(self.parent.model.pump_data["D"])
        # "НИЖНЕЕ:",
        self.st[5].SetLabel(self.parent.model.pump_data["S"])
        # "ПУЛЬС:",
        self.st[6].SetLabel(self.parent.model.pump_data["P"])
        # "АРИТМИЯ:",
        self.st[7].SetLabel(self.parent.model.pump_data["A"])
        # "ГИПЕРТОНИЯ:"]
        self.st[8].SetLabel(str(self.parent.model.row_id))


        return super().Show(show)

    def Hide(self):
        # self.st_err.SetLabel("")
        return super().Hide()

