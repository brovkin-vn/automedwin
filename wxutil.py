from ctypes.wintypes import PINT
import wx
print('start wxutil')

BLUE  = wx.Colour(20,20,200)
GREEN = wx.Colour(20,200,20)
RED   = wx.Colour(200,20,20)
GRAY  = wx.Colour(60,60,60)

# _screen_size:wx.Size = wx.Size(1366, 768) * 4 / 4 #
# _screen_size:wx.Size = wx.Size(1024, 768) * 4 / 4 #
# _screen_size:wx.Size = wx.Display(0).GetGeometry().GetSize()*SCALE
# _dh  = _screen_size.height / 100
# _dw = _screen_size.width / 100

def reset_screen_size():
    pass
    # _screen_size:wx.Size = wx.Display(0).GetGeometry().GetSize()*SCALE
    # print(f'reset_screen_size {_screen_size=}')
    # _dh = _screen_size.height / 100
    # _dw = _screen_size.width / 100

def get_screen_size():
    SCALE = 2/2
    # _screen_size:wx.Size = wx.Size(1024, 768)
    # _screen_size:wx.Size = wx.Size(1366, 768)
    # _screen_size:wx.Size = wx.Size(1920, 1080)
    # _screen_size:wx.Size = wx.Size(1280, 720)
    _screen_size:wx.Size = wx.Display(0).GetGeometry().GetSize()*SCALE
    print(f'get_screen_size {_screen_size=}')
    return _screen_size    

def fh(y:int = 1):
    _screen_size:wx.Size = get_screen_size()
    _dh = _screen_size.height / 100
    return int(_dh * y)
def fw(x:int = 1):
    _screen_size:wx.Size = get_screen_size()
    _dw = _screen_size.width / 100
    return int(_dw * x)


def scale_bitmap(bitmap:wx.Bitmap, size:wx.Size):
    image = bitmap.ConvertToImage()
    image = image.Scale(size.width, size.height, wx.IMAGE_QUALITY_HIGH)
    result = image.ConvertToBitmap()
    return result

class ScaleBitmap(wx.StaticBitmap):
    def __init__(self, parent, path, size:wx.Size, pos=wx.Point(0,0)):
        self.parent=parent
        size = size

        bitmap = wx.Bitmap(path)
        bitmap = scale_bitmap(bitmap, size)

        super(wx.StaticBitmap, self).__init__(parent, -1, bitmap, pos=pos, size = size)


class MovableButton(wx.Panel):
    def __init__(self, parent,path_up, path_down, pos:wx.Point, size:wx.Size):
        bitmap_up = wx.Bitmap(path_up)
        bitmap_up = scale_bitmap(bitmap_up, size)
        bitmap_down = wx.Bitmap(path_down)
        bitmap_down = scale_bitmap(bitmap_down, size)

        super(wx.Panel, self).__init__(parent, -1, pos=pos, size = size)
        self.BackgroundColour = wx.GREEN
        self.sb_up = ScaleBitmap(self, path_up, size) 
        self.sb_down = ScaleBitmap(self, path_down, size) 
        self.sb_down.Hide()
        self.sb_down.Bind(wx.EVT_LEFT_UP, self.onClickUp)
        self.sb_up.Bind(wx.EVT_LEFT_DOWN, self.onClickDown)

    def onClickDown(self, event):
        self.sb_up.Hide()
        self.sb_down.Show()
        wx.PostEvent(self, event)
        event.Skip()
        
        
    def onClickUp(self, event):
        self.sb_up.Show()
        self.sb_down.Hide()
        wx.PostEvent(self, event)
        event.Skip()


class ButtonTest(MovableButton):
    # self.btn = wu.MovableButton(sb, "images/buttons/buttons_2022_test.png", "images/buttons/buttons_2022_test_v2.png", pos_btn, size_btn)
    def __init__(self, parent, pos: wx.Point, size: wx.Size):
        path_up = "images/buttons/buttons_2022_test.png"
        path_down = "images/buttons/buttons_2022_test_v2.png"
        super().__init__(parent, path_up, path_down, pos, size)

class ButtonYes(MovableButton):
    # self.btn = wu.MovableButton(sb, "images/buttons/buttons_2022_test.png", "images/buttons/buttons_2022_test_v2.png", pos_btn, size_btn)
    def __init__(self, parent, pos: wx.Point, size: wx.Size):
        path_up = "images/buttons/buttons_2022_yes.png"
        path_down = "images/buttons/buttons_2022_yes_v2.png"
        super().__init__(parent, path_up, path_down, pos, size)

class ButtonNo(MovableButton):
    # self.btn = wu.MovableButton(sb, "images/buttons/buttons_2022_test.png", "images/buttons/buttons_2022_test_v2.png", pos_btn, size_btn)
    def __init__(self, parent, pos: wx.Point, size: wx.Size):
        path_up = "images/buttons/buttons_2022_no.png"
        path_down = "images/buttons/buttons_2022_no_v2.png"
        super().__init__(parent, path_up, path_down, pos, size)

class ButtonCancel(MovableButton):
    # self.btn = wu.MovableButton(sb, "images/buttons/buttons_2022_test.png", "images/buttons/buttons_2022_test_v2.png", pos_btn, size_btn)
    def __init__(self, parent, pos: wx.Point, size: wx.Size):
        path_up = "images/buttons/buttons_2022_cancel.png"
        path_down = "images/buttons/buttons_2022_cancel_v2.png"
        super().__init__(parent, path_up, path_down, pos, size)

class ButtonExit(MovableButton):
    # self.btn = wu.MovableButton(sb, "images/buttons/buttons_2022_test.png", "images/buttons/buttons_2022_test_v2.png", pos_btn, size_btn)
    def __init__(self, parent, pos: wx.Point, size: wx.Size):
        path_up = "images/buttons/buttons_2022_exit.png"
        path_down = "images/buttons/buttons_2022_exit_v2.png"
        super().__init__(parent, path_up, path_down, pos, size)




        

