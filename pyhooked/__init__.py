"""
This file is part of pyhooked, an LGPL licensed pure Python hotkey module for Windows
Copyright (C) 2016 Ethan Smith
adapeted from

"""
import ctypes
from ctypes import wintypes
from ctypes import CFUNCTYPE, POINTER, c_int, c_uint, c_void_p
from ctypes import byref
import atexit
import platform


__version__ = '0.8.0'

cmp_func = CFUNCTYPE(c_int, c_int, wintypes.HINSTANCE, POINTER(c_void_p))

# redefine names to avoid needless clutter
GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
SetWindowsHookExA = ctypes.windll.user32.SetWindowsHookExA
GetMessageW = ctypes.windll.user32.GetMessageW
DispatchMessageW = ctypes.windll.user32.DispatchMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
CallNextHookEx = ctypes.windll.user32.CallNextHookEx
UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx

# specify the arguent and return types of functions
GetModuleHandleA.restype = wintypes.HMODULE
GetModuleHandleA.argtypes = [wintypes.LPCWSTR]
SetWindowsHookExA.restype = c_int
SetWindowsHookExA.argtypes = [c_int, cmp_func, wintypes.HINSTANCE, wintypes.DWORD]
GetMessageW.argtypes = [POINTER(wintypes.MSG), wintypes.HWND, c_uint, c_uint]
TranslateMessage.argtypes = [POINTER(wintypes.MSG)]
DispatchMessageW.argtypes = [POINTER(wintypes.MSG)]


def _callback_pointer(handler):
    """Create and return C-pointer"""
    return cmp_func(handler)



class KeyboardEvent(object):
    """Class to describe an event triggered by the keyboard"""
    def __init__(self, current_key=None, event_type=None, pressed_key=None, key_code=None):
        self.current_key = current_key
        self.event_type = event_type
        self.pressed_key = pressed_key
        self.key_code = key_code

class MouseEvent(object):
    """Class to describe an event triggered by the mouse"""
    def __init__(self, current_key=None, event_type=None, mouse_x=None, mouse_y=None):
        self.current_key = current_key
        self.event_type = event_type
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

# The following section contains dictionaries that map key codes and other event codes to the event type (e.g. key up)
# and the key or button doing the action (e.g. Tab)
MOUSE_ID_TO_KEY = {512: 'Move',
                           513: 'LButton',
                           514: 'LButton',
                           516: 'RButton',
                           517: 'RButton',
                           519: 'WheelButton',
                           520: 'WheelButton',
                           522: 'Wheel'}


MOUSE_ID_TO_EVENT_TYPE = {512: None,
                          513: 'key down',
                          514: 'key up',
                          516: 'key down',
                          517: 'key up',
                          519: 'key down',
                          520: 'key up',
                          522: None}

# stores the relation between keyboard event codes and the key pressed. Reference:
# https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
# seems to only work on 32 bits
if platform.architecture()[0] == '32bit':
    ID_TO_KEY = {8: 'Back',
             9: 'Tab',
             13: 'Return',
             20: 'Capital',
             27: 'Escape',
             32: 'Space',
             33: 'Prior',
             34: 'Next',
             35: 'End',
             36: 'Home',
             37: 'Left',
             38: 'Up',
             39: 'Right',
             40: 'Down',
             44: 'PrtScr',
             46: 'Delete',
             48: '0',
             49: '1',
             50: '2',
             51: '3',
             52: '4',
             53: '5',
             54: '6',
             55: '7',
             56: '8',
             57: '9',
             65: 'A',
             66: 'B',
             67: 'C',
             68: 'D',
             69: 'E',
             70: 'F',
             71: 'G',
             72: 'H',
             73: 'I',
             74: 'J',
             75: 'K',
             76: 'L',
             77: 'M',
             78: 'N',
             79: 'O',
             80: 'P',
             81: 'Q',
             82: 'R',
             83: 'S',
             84: 'T',
             85: 'U',
             86: 'V',
             87: 'W',
             88: 'X',
             89: 'Y',
             90: 'Z',
             91: 'Lwin',
             92: 'Rwin',
             93: 'App',
             95: 'Sleep',
             96: 'Numpad0',
             97: 'Numpad1',
             98: 'Numpad2',
             99: 'Numpad3',
             100: 'Numpad4',
             101: 'Numpad5',
             102: 'Numpad6',
             103: 'Numpad7',
             104: 'Numpad8',
             105: 'Numpad9',
             106: 'Multiply',
             107: 'Add',
             109: 'Subtract',
             110: 'Decimal',
             111: 'Divide',
             112: 'F1',
             113: 'F2',
             114: 'F3',
             115: 'F4',
             116: 'F5',
             117: 'F6',
             118: 'F7',
             119: 'F8',
             120: 'F9',
             121: 'F10',
             122: 'F11',
             123: 'F12',
             144: 'Numlock',
             160: 'Lshift',
             161: 'Rshift',
             162: 'Lcontrol',
             163: 'Rcontrol',
             164: 'Lmenu',
             165: 'Rmenu',
             186: 'Oem_1',
             187: 'Oem_Plus',
             188: 'Oem_Comma',
             189: 'Oem_Minus',
             190: 'Oem_Period',
             191: 'Oem_2',
             192: 'Oem_3',
             219: 'Oem_4',
             220: 'Oem_5',
             221: 'Oem_6',
             222: 'Oem_7',
             1001: 'mouse left',  # mouse hotkeys
             1002: 'mouse right',
             1003: 'mouse middle',
             1000: 'mouse move',  # single event hotkeys
             1004: 'mouse wheel up',
             1005: 'mouse wheel down',
             1010: 'Ctrl',  # merged hotkeys
             1011: 'Alt',
             1012: 'Shift',
             1013: 'Win',
             }
else:
    ID_TO_KEY = {
        60129542152: 'Back',
        64424509449: 'Tab',
        120259084301: 'Return',
        249108103188: 'Capital',
        4294967323: 'Escape',
        244813135904: 'Space',
        # 33: 'Prior',
        # 34: 'Next',
        339302416419: 'End',
        304942678052: 'Home',
        322122547237: 'Left',
        309237645350: 'Up',
        330712481831: 'Right',
        343597383720: 'Down',
        360777252908: 'PrtScr',
        356482285614: 'Delete',
        47244640304: '0',
        8589934641: '1',
        12884901938: '2',
        17179869235: '3',
        21474836532: '4',
        25769803829: '5',
        30064771126: '6',
        34359738423: '7',
        38654705720: '8',
        42949673017: '9',
        128849018945: 'A',
        206158430274: 'B',
        197568495683: 'C',
        137438953540: 'D',
        77309411397: 'E',
        141733920838: 'F',
        146028888135: 'G',
        150323855432: 'H',
        98784247881: 'I',
        154618822730: 'J',
        158913790027: 'K',
        163208757324: 'L',
        214748364877: 'M',
        210453397582: 'N',
        103079215183: 'O',
        107374182480: 'P',
        68719476817: 'Q',
        81604378706: 'R',
        133143986259: 'S',
        85899346004: 'T',
        94489280597: 'U',
        201863462998: 'V',
        73014444119: 'W',
        193273528408: 'X',
        90194313305: 'Y',
        188978561114: 'Z',
        390842024027: 'Lwin',
        # 92: 'Rwin',
        # 93: 'App',
        # 95: 'Sleep',
        352187318368: 'Numpad0',
        339302416481: 'Numpad1',
        343597383778: 'Numpad2',
        347892351075: 'Numpad3',
        322122547300: 'Numpad4',
        326417514597: 'Numpad5',
        330712481894: 'Numpad6',
        304942678119: 'Numpad7',
        309237645416: 'Numpad8',
        313532612713: 'Numpad9',
        236223201386: 'Multiply',
        335007449195: 'Add',
        317827580013: 'Subtract',
        356482285678: 'Decimal',
        227633266799: 'Divide',
        253403070576: 'F1',
        257698037873: 'F2',
        261993005170: 'F3',
        266287972467: 'F4',
        270582939764: 'F5',
        274877907061: 'F6',
        279172874358: 'F7',
        283467841655: 'F8',
        287762808952: 'F9',
        292057776249: 'F10',
        373662154874: 'F11',
        377957122171: 'F12',
        296352743568: 'Numlock',
        180388626592: 'Lshift',
        231928234145: 'Rshift',
        124554051746: 'Lcontrol',
        124554051747: 'Rcontrol',
        # 164: 'Lmenu',
        # 165: 'Rmenu',
        # 186: 'Oem_1',
        # 187: 'Oem_Plus',
        # 188: 'Oem_Comma',
        # 189: 'Oem_Minus',
        # 190: 'Oem_Period',
        # 191: 'Oem_2',
        # 192: 'Oem_3',
        # 219: 'Oem_4',
        # 220: 'Oem_5',
        # 221: 'Oem_6',
        # 222: 'Oem_7',
        # 1001: 'mouse left',  # mouse hotkeys
        # 1002: 'mouse right',
        # 1003: 'mouse middle',
        # 1000: 'mouse move',  # single event hotkeys
        # 1004: 'mouse wheel up',
        # 1005: 'mouse wheel down',
        #124554051746: 'Ctrl',  # merged hotkeys
        240518168740: 'Alt',
        #180388626592: 'Shift',
        #390842024027: 'Win'
    }
event_types = {0x100: 'key down',  # WM_KeyDown for normal keys
               0x101: 'key up',  # WM_KeyUp for normal keys
               0x104: 'key down',  # WM_SYSKEYDOWN, used for Alt key.
               0x105: 'key up',  # WM_SYSKEYUP, used for Alt key.
               }
# these are used for specifying the hook type we want to make
WH_KEYBOARD_LL = 0x00D
WH_MOUSE_LL = 0x0E
# the Windows quit message, if the program quits while listening.
WM_QUIT = 0x0012


class Hook(object):
    """"Main hotkey class used to and listen for hotkeys. Set an event handler to check what keys are pressed."""

    def __init__(self):
        """Initializer of the Hook class, creates class attributes"""
        self.handler = 0
        self.pressed_keys = []
        self.keyboard_id = None
        self.mouse_id = None
        self.mouse_is_hook = False
        self.keyboard_is_hook = True

    def hook(self, keyboard=True, mouse=False):
        """Hook mouse and/or keyboard events"""
        self.mouse_is_hook = mouse
        self.keyboard_is_hook = keyboard

        # check that we are going to hook into at least one device
        if not self.mouse_is_hook and not self.keyboard_is_hook:
            raise Exception("You must hook into either the keyboard and/or mouse events")

        if self.keyboard_is_hook:
            def keyboard_low_level_handler(code, event_code, kb_data_ptr):
                """Used to catch keyboard events and deal with the event"""
                try:
                    key_code = 0xFFFFFFFF & kb_data_ptr[0] #key code
                    current_key = ID_TO_KEY[key_code]
                    event_type = event_types[0xFFFFFFFF & event_code]

                    if event_type == 'key down': # add key to those down to list
                        self.pressed_keys.append(current_key)

                    if event_type == 'key up': # remove when no longer pressed
                        self.pressed_keys.remove(current_key)

                    # wrap the keyboard information grabbed into a container class
                    event = KeyboardEvent(current_key, event_type, self.pressed_keys,key_code)

                    # if we have an event handler, call it to deal with keys in the list
                    if self.handler != 0:
                        self.handler(event)

                finally:
                    # TODO: fix return here to use non-blocking call
                    return CallNextHookEx(self.keyboard_id, code, event_code, kb_data_ptr)

            keyboard_pointer = _callback_pointer(keyboard_low_level_handler)

            self.keyboard_id = SetWindowsHookExA(WH_KEYBOARD_LL, keyboard_pointer,
                                                               GetModuleHandleA(None),
                                                               0)

        if self.mouse_is_hook:
            def mouse_low_level_handler(code, event_code, kb_data_ptr):
                """Used to catch and deal with mouse events"""
                try:
                    current_key = MOUSE_ID_TO_KEY[event_code] #check the type of event (see MOUSE_ID_TO_KEY for a list)
                    if current_key != 'Move': #if we aren't moving, then we deal with a mouse click
                        event_type = MOUSE_ID_TO_EVENT_TYPE[event_code]
                        #the first two members of kb_data_ptr hold the mouse position, x and y
                        event = MouseEvent(current_key, event_type, kb_data_ptr[0], kb_data_ptr[1])

                        if self.handler != 0:
                            self.handler(event)

                finally:
                    # TODO: fix return here to use non-blocking call
                    return CallNextHookEx(self.mouse_id, code, event_code, kb_data_ptr)

            mouse_pointer = _callback_pointer(mouse_low_level_handler)
            self.mouse_id = SetWindowsHookExA(WH_MOUSE_LL, mouse_pointer,
                                                            GetModuleHandleA(None), 0)

        atexit.register(UnhookWindowsHookEx, self.keyboard_id)
        atexit.register(UnhookWindowsHookEx, self.mouse_id)

        message = wintypes.MSG()
        while self.mouse_is_hook or self.keyboard_is_hook:
            msg = GetMessageW(byref(message), 0, 0, 0)
            if msg == -1:
                self.unhook_keyboard()
                self.unhook_mouse()
                exit(0)

            elif msg == 0:  # GetMessage return 0 only if WM_QUIT
                exit(0)
            else:
                TranslateMessage(byref(message))
                DispatchMessageW(byref(message))

    def unhook_mouse(self):
        """Stop listening to the mouse"""
        if self.mouse_is_hook:
            self.mouse_is_hook = False
            UnhookWindowsHookEx(self.mouse_id)

    def unhook_keyboard(self):
        """Stop listening to the keyboard"""
        if self.keyboard_is_hook:
            self.keyboard_is_hook = False
            UnhookWindowsHookEx(self.keyboard_id)