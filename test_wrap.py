import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.st = wx.StaticText(self.pnl, id=1, label="Lor ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. Lorem ipsum ... laborum. ", pos=(0, 0),
                                size=wx.DefaultSize, style=0, name="statictext")

        # self.st.Wrap(300)

        self.SetSize((350, 250))
        self.Center()


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
