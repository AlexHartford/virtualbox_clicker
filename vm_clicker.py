import virtualbox
from virtualbox.library import LockType

from pynput import mouse, keyboard

vbox = virtualbox.VirtualBox()
session = virtualbox.Session()
machine = vbox.find_machine('Windows10')

print('session state:', session.state)

machine.lock_machine(session, LockType.shared)

print('session state:', session.state)

def click():
    global listening
    if listening:
        print('Clicking')
        session.console.mouse.put_mouse_event_absolute(813, 405, 0, 0, 1)
        session.console.mouse.put_mouse_event_absolute(813, 405, 0, 0, 0)

global listening
listening = False

def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    click()

def on_scroll(x, y, dx, dy):
    click()

def on_press(key):
    global listening
    if key == keyboard.Key.esc:
        listening = not listening
        print('Listening:', listening)
    click()

mouse_listener = mouse.Listener(on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()
mouse_listener.join()
keyboard_listener.join()

session.unlock_machine()