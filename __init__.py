import ctypes
from ctypes import wintypes
from collections import namedtuple
import thread
import time
KeyEvents=namedtuple("KeyEvents",(['event_type', 'key_code',
											 'scan_code', 'alt_pressed',
											 'time']))


class hook:
	"""Main class to create and track hotkeys. Use hook.Hotkey to make a new hotkey"""
	def __init__(self):
		self.fhot=[]
		self.list=[]
		self.handlers=[]
		self.IDs=[]
		self.oldID=0
		self.current_keys=[]
		#Scancodes and a few key codes
		self.keylist=["Null","Esc","1","2","3","4","5","6","7","8","9","0","-","=","Backspace","Tab","Q","W","E","R","T","Y","U","I","O","P","[","]","Return","LCtrl","A","S","D","F","G","H","J","K","L",";","'","`","LShift","\\","Z","X","C","V","B","N","M",",",".","/","RShift","Key*","LAlt","Space","Capslock","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","Numlock","ScrollLock","KeyHome","Up","KeyPgUp","Key-","Left","Key5","Right","Key+","End","Down","KeyPgDn","KeyIns","KeyDel","SYSRQ","","","F11","F12","","","LWin","RWin","MenuKey","RAlt","RCtrl"]
		#For a convention, I will take care of key codes only when needed, as I already started with scan codes (shift taken care of)
		#(NOTE: In Decimal!)Key=scan_code,key_code; LAlt=56,164; RAlt=56,165; SYSRQ=55,44;Key*=55,106; Numlock=Unk,255; LCtrl=29,162;RCtrl=29,163
	def print_event(self,e):
		func_called=False
		self.estr=str(e)
		start=self.estr.index("scan_code=")
		end=self.estr.index(",",start)
		scancode=int(str(e)[(start+10):end])
		start2=self.estr.index("key_code=")
		end2=self.estr.index(",",start2)
		try:
			keycode=int(str(e)[(start2+10):end2])
		except:
			keycode=0
		try:
				key=self.keylist[scancode]
		except:
			key=str(e)
		#alt keys
		if key=="LAlt":
			if keycode==64:
				key=self.keylist[56]
			elif keycode==65:
				key=self.keylist[94]
		#Ctrl keys
		if key=="LCtrl":
			if keycode==62:
				key=self.keylist[29]
			elif keycode==63:
				key=self.keylist[95]
		#append to current_keys when down
		if str(e.event_type)=="key down" and not (key in self.current_keys):
			self.current_keys.append(key)
			for id in self.IDs:
				if self.current_keys==id[1] or self.current_keys in id[1]:
					ind=id[1].index(self.current_keys)
					if not func_called:
						id[2][ind]()
					func_called=True
		#remove when released
		elif str(e.event_type)=="key up":
			try:
				self.current_keys.remove(key)
			except:
				pass
		else:
			pass
		
	def Hotkey(self,list=[],fhot=None):
		"""Adds a new hotkey. Definition: Hotkey(list=[],fhot=None) where list is the list of
		keys and fhot is the callback function"""
		self.list+=[list]
		self.fhot+=[fhot]
		self.IDs.append([self.oldID,self.list,self.fhot])
		self.oldID+=1
		if self.list is [] or self.fhot is None:
			raise Exception("Error: Empty key list or no callback function")
		else:
			self.handlers.append(self.print_event)
	def RemHotKey(self,*args):
		pass
	def listener(self):
		"""The listener listens to events and adds them to handlers"""
		from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
		import atexit
		event_types = {0x100: 'key down', #WM_KeyDown for normal keys
				   0x101: 'key up', #WM_KeyUp for normal keys
				   0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
				   0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
				  }
		def low_level_handler(nCode, wParam, lParam):
			"""
			Processes a low level Windows keyboard event.
			"""
			event = KeyEvents(event_types[wParam], lParam[0], lParam[1],
						  lParam[2] == 32, lParam[3])
			for h in self.handlers:
				h(event)
			#Be nice, return next hook
			return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
	
		CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
		#Get C pointer
		pointer = CMPFUNC(low_level_handler)
		windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
		windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
		hook_id = windll.user32.SetWindowsHookExA(0x00D, pointer,
											 windll.kernel32.GetModuleHandleW(None), 0)

		#Remove hook when done
		atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)
		while True:
			msg = windll.user32.GetMessageW(None, 0, 0,0)
			windll.user32.TranslateMessage(byref(msg))
			windll.user32.DispatchMessageW(byref(msg))
	def listen(self):
		"""Start listening for hooks"""
		self.listener()
def foo():
	print "foo"
def foobar():
	print "foobar"
if __name__ == '__main__':
	hk=hook()
	hk.Hotkey(["LCtrl","A"],foo)
	hk.Hotkey(["LCtrl","B"],foobar)
	hk.listen()
