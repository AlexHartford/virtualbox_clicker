import virtualbox
from virtualbox.library import LockType

from pynput import mouse, keyboard

vbox = virtualbox.VirtualBox()
session = virtualbox.Session()
machine = vbox.find_machine('Windows10')

print('session state:', session.state)

machine.lock_machine(session, LockType.shared)

print('session state:', session.state)

# session.console.mouse.put_mouse_event_absolute(250, 250, 0, 0, 1)
# session.console.keyboard.put_keys("Hello, world!")

# session.unlock_machine()

listening = False

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

def on_press(key):
    if key == keyboard.Key.esc:
        listening = not listening
        return False  # stop listener
    print(key)

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()
# mouse_listener.join()
# keyboard_listener.join()

while(True):
    while(listening):
        continue

session.unlock_machine()