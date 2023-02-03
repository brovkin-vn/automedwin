import wx


COLOR_1 = wx.Colour( 70, 70, 110) 

BASE_HEIGTT = 768
BASE_WIDTH = 1366

class AdaptiveStaticText(wx.StaticText):
    def __init__(self, parent, label, parent_size=wx.Size(BASE_WIDTH, BASE_HEIGTT), pos=wx.Point(10, 10),font_size = 28, font_color = COLOR_1, style=wx.ALIGN_LEFT, size=wx.Size()):
        self.parent=parent
        super(wx.StaticText, self).__init__(parent, -1, label, pos=pos, style=style, size=size)
        self.BackgroundColour = wx.WHITE
        self.ForegroundColour = font_color
        font:wx.Font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font_size = int(font_size * parent_size.width /BASE_WIDTH )
        font.SetPointSize(font_size)
        self.SetFont(font)






