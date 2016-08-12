import sys
from pyhooked import Hook, KeyboardEvent
import threading
from PySide.QtCore import * 
from PySide.QtGui import * 

class MyWindow(QMainWindow): 
    def __init__(self, *args): 
        QMainWindow.__init__(self, *args)

        self.label = QLabel(self)
        self.label.setText('A PySide Window')
        self.resize(640,480)
        hk=Hook() #make a new instance of PyHooked
        hk.handler = self.foo # set the handler function
        # thread the call to hook, otherwise we block the GUI
        thread = threading.Thread(target=hk.hook) 
        # start hooking
        thread.start()

    def foo(self,args):
        if isinstance(args, KeyboardEvent):
            print(args.key_code)
            if args.current_key == 'A' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
                self.label.setText("Ctrl + A was pressed")

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    w = MyWindow() 
    w.show() 
    sys.exit(app.exec_())
