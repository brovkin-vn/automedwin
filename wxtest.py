from unittest import result
import wx
from args import Args
from model import EVENT
import wxutil as wu
from wxast import AdaptiveStaticText
from wxutil import fh, fw
from check import alco, piro, addr, server1, server2, router1, router2

import wx.lib.newevent
TestTimerEvent, EVT_TEST_TIMER = wx.lib.newevent.NewEvent()


class PanelTest(wx.Panel):
    def __init__(self, parent, size:wx.Size, pos=wx.Point(0,0)):
        self.parent = parent
        super().__init__(parent, -1, size=size, pos=pos)

        self.test_resutl_text = [
            "Подождите, идет тестирование...",
            "Тест заврешен успешно",
            "Тест завершен с ошибками"
        ]
        self.test_result_color = [wu.GRAY, wu.GREEN, wu.RED]
        self.test_processs_state = 0
        self.test_step_number = 0
        
        AdaptiveStaticText(self, label="Экран диагностики" ,parent_size=size,    pos=wx.Point(fw(2),fh(3+(6*0))), size=wx.Size(size.width//2-fw(), fh()), font_size=32, font_color=wu.BLUE)
        
        self.checklist = []
        # self.test = [alco, piro, addr, router1, router2, server1, server2]
        self.test = []
        if parent.args.enable_alco: self.test.append(alco)
        if parent.args.enable_piro: self.test.append(piro)
        self.test += [addr, router1, router2, server1, server2]
        self.labels = []
        if parent.args.enable_alco: self.labels.append("Алкотестер")
        if parent.args.enable_piro: self.labels.append("Пирометр")
        self.labels += [
            "Интернет"   ,
            "Роутер 1"   ,
            "Роутер 2"   ,
            "Сервер ПМО" ,
            "Сeрвер СКУД"
        ]
        
        self.index_test = 0
        self.st = list()
        for i, label in enumerate(self.labels):
            self.st.append(AdaptiveStaticText(self, label=f"# {label}" ,parent_size=size, pos=wx.Point(fw(4),fh(15+(6*i))), size=wx.Size(fw(49), fh()), font_size=26, font_color=wu.GRAY))
        # if parent.args.enable_alco:
        #     self.st.append(AdaptiveStaticText(self, label="# Алкотестер" ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*2))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # if parent.args.enable_piro:
        #     self.st.append(AdaptiveStaticText(self, label="# Пирометр"   ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*3))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # self.st.append(AdaptiveStaticText(self, label="# Интернет"   ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*4))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # self.st.append(AdaptiveStaticText(self, label="# Роутер 1"   ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*5))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # self.st.append(AdaptiveStaticText(self, label="# Роутер 2"   ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*6))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # self.st.append(AdaptiveStaticText(self, label="# Сервер ПМО" ,parent_size=size, pos=wx.Point(fw(4),fh(3+(6*7))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        # self.st.append(AdaptiveStaticText(self, label="# Сeрвер СКУД",parent_size=size, pos=wx.Point(fw(4),fh(3+(6*8))), size=wx.Size(size.width//2-fw(), fh()), font_size=26, font_color=wu.GRAY))
        
        
        self.st_result = AdaptiveStaticText(self, label=self.test_resutl_text[0], parent_size=size, pos=wx.Point(fw(2),fh(3+(6*10))), size=wx.Size(size.width//2-fw(), fh()), font_size=32, font_color=self.test_result_color[0])

        size_btn:wx.Size = size / 9
        self.btnCancel = wu.ButtonCancel(self, wx.Point(fw(2),fh(85)), size_btn)
        self.btnCancel.Bind(wx.EVT_LEFT_DOWN, self.onYesCancel)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.Bind(EVT_TEST_TIMER, self.onStartTimer)
    
    def onStartTimer(self, event):
        self.index_test = 0
        self.timer.Start(333)

    def onTimer(self, event):
        if self.IsShown:
            print(f"onTimer {self.index_test=}")
            result, data = self.test[self.index_test]()
            print(result, data)
            self.checklist.append(result)
            if result:
                self.st[self.index_test].SetForegroundColour(wu.GREEN)
                self.st[self.index_test].SetLabelText(f"+ {self.labels[self.index_test]} - {data}")
            else:
                self.st[self.index_test].SetForegroundColour(wu.RED)
                self.st[self.index_test].SetLabelText(f"- {self.labels[self.index_test]} - {data}")

            # self.index_test = len(self.st)-1 if self.index_test == 0 else self.index_test - 1 
            self.index_test = self.index_test + 1 if self.index_test < len(self.st)-1 else 0
            
            if self.index_test == 0: # and all tests
                self.timer.Stop()
                print(f"{self.checklist=}")
                if all(self.checklist):
                    self.st_result.SetForegroundColour(wu.GREEN)
                    self.st_result.SetLabelText(self.test_resutl_text[1])
                else:
                    self.st_result.SetForegroundColour(wu.RED)
                    self.st_result.SetLabelText(self.test_resutl_text[2])
            


    def onYesCancel(self, event):
        print("onCancelBtn")
        self.parent.automat.put_event(EVENT.CANCEL)
        event.Skip()

    def Show(self, show=True):

        self.checklist = []
        self.st_result.SetForegroundColour(wu.GRAY)
        self.st_result.SetLabelText(self.test_resutl_text[0])

        for index in range(len(self.st)):
            self.st[index].SetForegroundColour(wu.GRAY)
            self.st[index].SetLabelText("# "+self.labels[index])

        wx.PostEvent(self, TestTimerEvent())
        return super().Show(show) 

    def Hide(self):
        self.timer.Stop()
        return super().Hide()


