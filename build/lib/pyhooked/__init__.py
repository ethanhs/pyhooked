import ctypes
from ctypes import wintypes
from collections import namedtuple
import platform
__version__="0.0.6"
KeyEvents=namedtuple("KeyEvents",(['event_type', 'key_code',
											 'scan_code', 'alt_pressed',
											 'time']))

MouseEvents=namedtuple("MouseEvents",(['event_type','mouse_x','mouse_y']))
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
		self.keylist=["Null","Esc","1","2","3","4","5","6","7","8","9","0","-","=","Backspace","Tab","Q","W","E","R","T","Y","U","I","O","P","[","]","Return","LCtrl","A","S","D","F","G","H","J","K","L",";","'","`","LShift","\\","Z","X","C","V","B","N","M",",",".","/","RShift","Key*","LAlt","Space","Capslock","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","Numlock","ScrollLock","KeyHome","Up","KeyPgUp","Key-","Left","Key5","Right","Key+","End","Down","KeyPgDn","KeyIns","KeyDel","SYSRQ","","","F11","F12","","","LWin","RWin","MenuKey","RAlt","RCtrl","PrtSc"]
	def print_event(self,e):
		"""This parses through the keyboard events. You shouldn't ever need this. Actually, don't mess with this; you may break your computer."""
		if platform.python_implementation()=="PyPy":
			if "scan_code" in str(e):
				self.estr=str(e)
				start=self.estr.index("scan_code=")
				#PyPy seems to append an 'L' so search until that
				end=self.estr.index("L",start)
				scancode=int(str(e)[(start+10):end])
				start2=self.estr.index("key_code=")
				end2=self.estr.index("L",start2)
				try:
					keycode=int(str(e)[(start2+9):end2])
				except:
					keycode=0
				try:
					key=self.keylist[scancode]
				except:
					key=str(e)
		elif platform.python_implementation()=="CPython" or platform.python_implementation()=="IronPython":
			if "scan_code" in str(e):
				self.estr=str(e)
				start=self.estr.index("scan_code=")
				end=self.estr.index(",",start)
				scancode=int(str(e)[(start+10):end])
				start2=self.estr.index("key_code=")
				end2=self.estr.index(",",start2)
				try:
					keycode=int(str(e)[(start2+9):end2])
				except:
					keycode=0
				try:
					key=self.keylist[scancode]
				except:
					key=str(e)
		if str(e.event_type)=="move":
			key=[e.mouse_x,e.mouse_y]
		elif not ("scan_code" in str(e)):
			if e.event_type[0]=="l":
				key="LMouse"
			elif e.event_type[0]=="r":
				key="RMouse"
			elif e.event_type[:2]=="mi":
				key="MMouse"
			elif "wheel" in str(e.event_type):
				key="Wheel"
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
		#Workaround for PrtSc
		if key == "Key*":
			if keycode == 44:
				key = self.keylist[96]
		#append to current_keys when down
		if str(e.event_type)=="key down" or str(e.event_type)=="left down" or str(e.event_type)=="right down" or "wheel" in str(e.event_type):
			self.current_keys.append(key)
			for id in self.IDs:
				#This next bit is complex. Basically it checks all the hotkeys provided to see if they are in self.current_keys
				if all([(i in self.current_keys) for i in id[1]]):
					if len(id)==4:
						id[2](id[3])
					else:
						id[2]()
		#remove key when released
		elif str(e.event_type)=="key up" or str(e.event_type)=="left up" or str(e.event_type)=="right up":
			try:
				while key in self.current_keys:
					self.current_keys.remove(key)
			except:
				pass
		#append location for motion
		elif str(e.event_type)=="move":
			for i in self.current_keys:
				if len(i)>1:
					self.current_keys.remove(i)
			self.current_keys.append(key)
			for id in self.IDs:
				#This next bit is complex. Basically it checks all the hotkeys provided to see if they are in self.current_keys
				if all([(i in self.current_keys) for i in id[1]]):
					if len(id)==4:
						id[2](id[3])
					else:
						id[2]()
		else:
			print(e)
	def Hotkey(self,list=[],fhot=None,args=None):
		"""Adds a new hotkey. Definition: Hotkey(list=[],fhot=None) where list is the list of
		keys and fhot is the callback function"""
		if not (args is None):
			self.IDs.append([self.oldID,list,fhot,args])
		else:
			self.IDs.append([self.oldID,list,fhot])
		self.oldID+=1
		if self.list is [] or self.fhot is None:
			raise Exception("Error: Empty key list or no callback function.")
		elif len(self.IDs)==1:
			self.handlers.append(self.print_event)
			return (self.oldID-1)
	def RemHotKey(self,hkey):
		"""Remove a hotkey. Specify the id, the key list, or the function to remove the hotkey."""
		if str(type(hkey))=="<type 'int'>":
			for hotk in self.IDs:
					if hotk[0]==hkey:
						self.IDs.remove(hotk)
		elif str(type(hkey))=="<type 'list'>":
			for hotk in self.IDs:
				if hotk[1]==hkey:
					self.IDs.remove(hotk)
		elif str(type(hkey))=="<type 'function'>":
			for hotk in self.IDs:
				if hotk[2]==hkey:
					self.IDs.remove(hotk)
	def listener(self):
		"""The listener listens to events and adds them to handlers"""
		from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref, Structure
		import atexit
		event_types = {0x100: 'key down', #WM_KeyDown for normal keys
				   0x101: 'key up', #WM_KeyUp for normal keys
				   0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
				   0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
				  }
		mouse_types={0x200: 'move', #WM_MOUSEMOVE
					0x20A: 'wheel', #WM_MOUSEWHEEL
					0x20E: 'H_wheel', #WM_MOUSEHWHEEL
					0x204: 'right down', #WM_RBUTTONDOWN
					0x205: 'right up', #WM_RBUTTONUP 
					0x201: 'left down', #WM_LBUTTONDOWN
					0x202: 'left up', #WM_LBUTTONUP
					0x207: 'middle down', #WM_MBUTTONDOWN
					0x208: 'middle up'} #WM_MBUTTONUP
		def low_level_handler(nCode, wParam, lParam):
			"""
			Processes a low level Windows keyboard event.
			"""
			event = KeyEvents(event_types[wParam], lParam[0], lParam[1],
						  lParam[2] == 32, lParam[3])
			for h in self.handlers:
				h(event)
			#return next hook
			return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
		
		CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
		#Make a C pointer
		pointer = CMPFUNC(low_level_handler)
		windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
		windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
		hook_id = windll.user32.SetWindowsHookExA(0x00D, pointer,
											 windll.kernel32.GetModuleHandleW(None), 0)
		def low_level_handler_mouse(nCode, wParam, lParam):
			"""
			Processes a low level Windows mouse event.
			"""
			event = MouseEvents(mouse_types[wParam], lParam[0], lParam[1])
			for h in self.handlers:
				h(event)
			#return next hook
			return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
		pointer2 = CMPFUNC(low_level_handler_mouse)
		hook_id = windll.user32.SetWindowsHookExA(0x0E, pointer2,
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
def foo(*args):
	"""For the example, it prints 'foo'."""
	print("foo", args)
def foobar():
	"""For the example, it prints 'foobar'."""
	print("foobar")
def exiter():
	raise SystemExit
if __name__ == '__main__':
	hk=hook()
	hk.Hotkey(["LCtrl","A"],foo,args=("HI")) # hotkey 0
	hk.Hotkey(["LCtrl","C"],foobar) #hotkey 1
	hk.RemHotKey(1) # or you could use hk.RemHotKey(["LCtrl","B"]) or hk.RemHotKey(foobar)
	hk.Hotkey(['LCtrl','LAlt','C'],exiter) #allows you to exit
	hk.listen()
