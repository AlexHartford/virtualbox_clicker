import virtualbox
from virtualbox.library import LockType

from pynput import mouse, keyboard
import sys

vbox = virtualbox.VirtualBox()
session = virtualbox.Session()
machine = vbox.find_machine('Windows10')

machine.lock_machine(session, LockType.shared)

x = int(sys.argv[1])
y = int(sys.argv[2])

print('Will click at ({}, {}). Press esc to start.'.format(x, y))

global listening
listening = False

global scroll_count
scroll_count = 0

global move_count
move_count = 0

def click():
    click_press()
    click_release()

def click_press():
    global listening
    if listening:
        print('Clicking')
        session.console.mouse.put_mouse_event_absolute(x, y, 0, 0, 1)

def click_release():
    global listening
    if listening:
        print('Released')
        session.console.mouse.put_mouse_event_absolute(x, y, 0, 0, 0)

def on_move(x, y):
    global move_count
    if move_count == 300:
        move_count = 0
        click()
    else:
        move_count += 1

def on_click(x, y, button, pressed):
    click_press() if pressed else click_release()

def on_scroll(x, y, dx, dy):
    global scroll_count
    if scroll_count == 4:
        scroll_count = 0
        click()
    else:
        scroll_count += 1

def on_press(key):
    if key == keyboard.Key.shift_l:
        session.console.mouse.put_mouse_event_absolute(1, 0, 0, 0, 2)
    else:
        click_press()

def on_release(key):
    global listening
    if key == keyboard.Key.esc:
        listening = not listening
        print('Listening:', listening)
    elif key == keyboard.Key.shift_l:
        session.console.mouse.put_mouse_event_absolute(1, 0, 0, 0, 0)
        print('Unstuck')
    else:
        click_release()

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()
mouse_listener.join()
keyboard_listener.join()

session.unlock_machine()