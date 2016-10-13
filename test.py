from pyhooked import Hook, KeyboardEvent

h = Hook()

def f(event):
 if isinstance(event, KeyboardEvent):
  print(event.pressed_key)
 if event.pressed_key == ['Q']:
  h.stop()

h.handler = f

if __name__ == '__main__':
 h.hook()
