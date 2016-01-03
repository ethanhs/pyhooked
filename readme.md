#PyHooked: a pure Python hotkey module
####About - 

[![Join the chat at https://gitter.im/IronManMark20/pyhooked](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/IronManMark20/pyhooked?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
PyHooked is a pure python keyboard hotkey that allows the creation of hotkeys in all Python implementations that support ctypes. Instead of messing around with low level Windows calls, just tell Hooked what your hotkey is and what function you want to call.

PyHooked supports IronPython (2.7), PyPy (newest repo version) and CPython (Tested:2.7,3.4,3.5 Most are likely to work) currently. It is pure Python, so porting should be very simple (see The Future below).

####Usage - 
It is really easy, just:
<pre>
from pyhooked import hook
def foo():
    print "foo"
hk=hook() #make a new instance of PyHooked
hk.Hotkey(["LCtrl","A"],foo) #add a new shortcut ctrl+a, that calls foo() when pressed
hk.listen() #start listening for key presses
</pre>
Read more in the [wiki](https://github.com/IronManMark20/PyHooked/wiki)!
####Installing

Just run `$ pip install git+https://github.com/IronManMark20/hooked.git`


####Alternatives -
[pyHook](http://sourceforge.net/projects/pyhook/) and [pyhk](https://github.com/schurpf/pyhk) inspired the creation of this project. They are great hotkey modules too!
####Extra - 
There is an example in the __init__.py file. You can run `python __init__.py` and it will start two hotkeys.
####License - 
PyHooked  Copyright (C) 2015  Ethan Smith
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions;
PyHooked is licensed under the LGPL v3, or at your choice, any later version. This program comes with the lgpl in a .txt file.

#####As of v0.6, the module is LGPL licensed, not under the GPL.

####The Future - 
Here are a few things that I would like to see:
* add support for args for called functions
* get mouse inputs
* support all scancodes found [here](https://msdn.microsoft.com/en-us/library/aa299374%28v=vs.60%29.aspx)
* Jython support
* Threads?
* ????<br>
I am open to feature requests. If you have ideas, let me know (ironmanmark20 (at) outlook.com). Or, even better, make your changes and a pull request!
