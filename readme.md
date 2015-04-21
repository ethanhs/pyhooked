#Hooked: a pure Python hotkey module
####About - 
Hooked is a pure python keyboard hotkey that allows the creation of hotkeys in all Python implementations that support ctypes. Instead of messing around with low level windows calls, just tell Hooked what your hotkey is and what function you want to call.
Hooked supports IronPython and CPython currently. It is pure Python, so porting should be very simple (see The Future below).
####Usage - 
It is really easy, just:
<pre>
from hooked import hook
def foo():
    print "foo"
hk=hook() #make a new instance of hooked
hk.Hotkey(["LCtrl","A"],foo) #add a new shortcut ctrl+a, that calls foo() when pressed
hk.listen() #start listening for key presses
</pre>
####Extra - 
There is an example in the hooked.py file. You can run `python hooked.py` and it will start two hotkeys.
####License - 
Hooked  Copyright (C) 2015  Ethan Smith
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions;
Hooked is licensed under the GPL v2, or at your choice, any later version. This program comes with the gpl in a .txt file.

####Alternative licensing - 
If you want to use this in a commercial product, or not under the GPL, contact me and I will consider allowing licensing under a different license.

####The Future - 
Here are a few things that I will be adding (subject to change without notice):
* get mouse inputs
* PyPy, Jython support
* Threads?
* ????<br>
I am open to feature requests. If you have ideas, let me know (mr.smittye(at)gmail.com). Or, even better, make your changes and a pull request!
