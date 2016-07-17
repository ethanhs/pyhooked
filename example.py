from pyhooked import Hook


def foo():
    print("foo")


hk = Hook()  # make a new instance of PyHooked
hk.hotkey(["LCtrl", "A"], foo)  # add a new shortcut ctrl+a, that calls foo() when pressed
hk.listen()  # start listening for key presses
