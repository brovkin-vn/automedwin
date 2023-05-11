from datetime import datetime
from cgi import print_arguments
from enum import auto
import wx
import automat as at
import wxutil as wu
from model import Model
from args import Args
from wxerro import PanelErro
from wxpost import PanelPost
from wxpump import PanelPump
from wxpiro import PanelPiro
from wxalco import PanelAlco
from wxsave import PanelSave
from wxtest import PanelTest
from wxwait import PanelWait
from wxerro import PanelErro


class Cmd:
    ID_TEST        = 8001
    ID_SHOW_POST   = 8002 
    ID_SHOW_PUMP   = 8003 
    ID_SHOW_PIRO   = 8004 
    ID_SHOW_ALCO   = 8005 
    ID_SHOW_SAVE   = 8006 
    ID_SHOW_TEST   = 8007
    ID_SHOW_ERRO   = 8008
    ID_SHOW_WAIT   = 8009

KWH = 1.77


class MainFrame(wx.Frame):
    def __init__(self, parent, title, log, model:Model, args:Args):
        self._model = model
        self._args = args
        wu.reset_screen_size()
        # size:wx.Size = wx.Display(0).GetGeometry().GetSize()*wu.SCALE
        size:wx.Size = wu.get_screen_size()
        # size = wx.Size(1366,768)

        size_frame = wx.Size(size.width, size.height+60)
        kwh = size.width / size.height
        pos = wx.Point(0, 0)
        # if (kwh < KWH):
        #     height = int(size.width / KWH)
        #     pos = wx.Point(0, (size.height - height) // 1)
        #     size.SetHeight(height)
        
        super().__init__(parent, title='MED',pos=(0,0),size=size_frame, style = wx.DEFAULT_FRAME_STYLE)
        self.BackgroundColour = wx.WHITE

        self._log = log

        self._buffer = ''
        self._tick = datetime.now() 
        # self.listener = pynput.keyboard.Listener(on_press=self.on_press)
        self._callback = None


        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(Cmd.ID_TEST, "&Test")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menubar.Append(fileMenu, "&File")

        panelMenu = wx.Menu()
        panelMenu.Append(Cmd.ID_SHOW_POST, "&1 Poster")
        panelMenu.Append(Cmd.ID_SHOW_PUMP, "&2 Pump")
        panelMenu.Append(Cmd.ID_SHOW_PIRO, "&3 Piro")
        panelMenu.Append(Cmd.ID_SHOW_ALCO, "&4 Alco")
        panelMenu.Append(Cmd.ID_SHOW_SAVE, "&5 Save")
        panelMenu.Append(Cmd.ID_SHOW_TEST, "&6 Test")
        panelMenu.Append(Cmd.ID_SHOW_ERRO, "&7 Error")
        panelMenu.Append(Cmd.ID_SHOW_WAIT, "&8 Wait")
        menubar.Append(panelMenu, "&Window")
        self.SetMenuBar(menubar) 

        self.Bind(wx.EVT_CLOSE, self.onClose)        
        self.Bind(wx.EVT_MENU, self.onQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onTest, id=Cmd.ID_TEST)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_POST)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_PUMP)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_PIRO)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_ALCO)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_SAVE)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_TEST)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_ERRO)
        self.Bind(wx.EVT_MENU, self.onShowPanel, id=Cmd.ID_SHOW_WAIT)
        self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook) 


        # panels list
        self.panelPost = PanelPost(self, size, pos) 
        self.panelPump = PanelPump(self, size, pos) 
        self.panelPiro = PanelPiro(self, size, pos) 
        self.panelAlco = PanelAlco(self, size, pos) 
        self.panelSave = PanelSave(self, size, pos) 
        self.panelTest = PanelTest(self, size, pos) 
        self.panelErro = PanelErro(self, size, pos) 
        self.panelWait = PanelWait(self, size, pos) 
        self.showPanel(self.panelWait)

        self._log.info(f'init wx module {id(self)}')

    @property
    def model(self):
        return self._model

    @property
    def args(self):
        return self._args

    # def onClickP(self, event):
    #     print("onClickP")

    @property
    def card(self):
        return self._card

    @property
    def buffer(self):
        return self._buffer

    def connect(self, foo):
        self._callback = foo

    def onCharHook(self, event):
        print("onCharHook", event.KeyCode, event.RawKeyCode, event.RawKeyFlags, chr(event.RawKeyCode))
        try:
            # print(f"{key.__dict__=}")
            tick = datetime.now()
            d = tick - self._tick
            self._tick = tick
            if ((d.days==0) and (d.seconds==0) and (d.microseconds < 80000)) or (len(self._buffer) == 0):
                self._buffer = self._buffer + chr(event.RawKeyCode)
                # self._buffer = self._buffer + key.char
            else:
                self._buffer = chr(event.RawKeyCode)
                # self._buffer = key.char

            # self._log.debug(f'{d.seconds=} {d.microseconds=} {self.buffer=}')
            if len(self._buffer) == 8:
                self._log.info(f'pass is read card={self._buffer}')
                self._card = self._buffer
                if self._callback:
                    self._callback(self.card)        
            
            
        except AttributeError as e:
            self._log.error(e)


    def onQuit(self, event):

        self.Close()        

    def onClose(self, event):
        self._log.info(f'app is close {id(self)}')
        self.automat.terminate()
        # self._log.info(f'app is close {id(self)}')
        event.Skip()

    def onTest(self, event):
        print('test')
        self.automat.put_event(Cmd.ID_TEST)
        self._log.info('test')


    def showPanel(self, panel):
        self.panelPost.Hide()
        self.panelPump.Hide()
        self.panelPiro.Hide()
        self.panelAlco.Hide()
        self.panelSave.Hide()
        self.panelTest.Hide()
        self.panelErro.Hide()
        self.panelWait.Hide()
        panel.Show()

    def onShowPanel(self, event):

        print(f"{event.Id=}")
        match event.Id:
            case Cmd.ID_SHOW_POST:
                self.showPanel(self.panelPost)
            case Cmd.ID_SHOW_PUMP:
                self.showPanel(self.panelPump)
            case Cmd.ID_SHOW_PIRO:
                self.showPanel(self.panelPiro)
            case Cmd.ID_SHOW_ALCO:
                self.showPanel(self.panelAlco)
            case Cmd.ID_SHOW_SAVE:
                self.showPanel(self.panelSave)
            case Cmd.ID_SHOW_TEST:
                self.showPanel(self.panelTest)
            case Cmd.ID_SHOW_ERRO:
                self.showPanel(self.panelErro)
            case Cmd.ID_SHOW_WAIT:
                self.showPanel(self.panelWait)

    def bindAutomat(self, automat):
        self.automat:at.Automat = automat
        self.automat.frame = self

