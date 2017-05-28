# PyHooked: a pure Python hotkey module


[![Join the chat at https://gitter.im/IronManMark20/pyhooked](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/IronManMark20/pyhooked?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

### ATTENTION: pyhooked has been deprecated in favor of [keyboard](https://github.com/boppreh/keyboard) for new projects. This library is will no longer be supported. Please use one keyboard or one of the alternatives listed in Alternatives.

#### About - 
PyHooked is a pure python keyboard and mouse hotkey module that allows the creation of hotkeys in all Python implementations that support sane implementations of ctypes. Instead of messing around with low level Windows calls, just give Hooked a callback and tell it to start listening.

PyHooked supports IronPython (2.7.5+, incl. 2.7.6 RC2), PyPy (5.3.1+) and CPython (Tested:2.7 x86,3.4 x64,3.5 x86; Most are likely to work) currently. It is pure Python, so porting to other Python implementations and versions should be very simple.

#### Usage - 
Please see [example.py](https://github.com/ethanhs/pyhooked/blob/master/example.py) for a basic example.

If you are using it with a UI library, please see [example_gui.py](https://github.com/ethanhs/pyhooked/blob/master/example_gui.py)

Please note that the wiki is out of date, and needs to be updated.

#### Installing

Just run `$ pip install pyhooked` or
`$ pip install git+https://github.com/ethanhs/pyhooked.git` to get the latest version.


#### Alternatives -
[pyHook](http://sourceforge.net/projects/pyhook/) and [pyhk](https://github.com/schurpf/pyhk) inspired the creation of this project. They are great hotkey modules too!

[pywinauto](https://github.com/pywinauto/pywinauto) is an incredibly useful Windows automation library that also includes among a plethora of tools, a hotkey detection library.

#### License - 
PyHooked  Copyright (C) 2015  Ethan Smith
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions;
PyHooked is licensed under the LGPL v3, or at your choice, any later version. This program comes with the lgpl in a .txt file.

Pyhooked v0.8+ is based on work by Maxim Samokhvalov, who has my graditude for his work, and others in the PyWinAuto project, licensed under the BSD 3-clause license. The copyright notice is given below.

     Copyright (C) 2016 Maxim Samokhvalov
     Copyright (C) 2016 Vasily Ryabov
     Copyright (C) 2016 ethanhs
     All rights reserved.
    
     Redistribution and use in source and binary forms, with or without
     modification, are permitted provided that the following conditions are met:
    
     * Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    
     * Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.
    
     * Neither the name of pywinauto nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.
    
     * Neither the name of hooks.py nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 



#####As of v0.6, the module is LGPL licensed, not under the GPL.

####The Future - 
Here are a few things that I would like to see:
* ~~add support for args for called functions~~  __(DONE)__
* ~~get mouse inputs~~  __(DONE)__
* ~~support all scancodes found [here](https://msdn.microsoft.com/en-us/library/aa299374%28v=vs.60%29.aspx)~~  __(DONE)__
* Jython support
* ????<br>
I am open to feature requests. If you have ideas, let me know (mr.smittye (at) gmail). Or, even better, make your changes and a pull request!
