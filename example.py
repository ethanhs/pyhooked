from pyhooked import Hook, KeyboardEvent


def handle_events(args):

    if isinstance(args, KeyboardEvent):
        print(args.key_code)
        if args.current_key == 'A' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
            print("Ctrl + A was pressed")


hk = Hook()  # make a new instance of PyHooked
hk.handler=handle_events  # add a new shortcut ctrl+a, that calls foo() when pressed
hk.hook() #hook into the events, and listen to the presses

