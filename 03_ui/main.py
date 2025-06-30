from MyProjectBase import *
import time

class MyFrame(MyFrame2):
    def __init__(self,parent):
        super().__init__(parent)
        
    def ClozeZaUindou( self, event ):
        print("sexy")
        self.Close()
        
    def OnExit( self, event ):
        time.sleep(10)
        event.Skip()
                       
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show()
        return True
        
        
app = MyApp(False)
app.MainLoop()
