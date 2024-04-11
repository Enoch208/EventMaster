import time
import pyautogui
import keyboard

# Function to record mouse movements and clicks for a given duration
def record_actions(duration=5):
    actions = []
    start_time = time.time()

    while time.time() - start_time < duration:
        x, y = pyautogui.position()
        actions.append(("move", x, y))
        time.sleep(0.1)  # Adjust the sleep duration as needed

    return actions

# Function to record keyboard inputs for a given duration
def record_keyboard_actions(duration=5):
    recorded_actions = []
    start_time = time.time()

    while time.time() - start_time < duration:
        event = keyboard.read_event(suppress=True)
        recorded_actions.append(("keyboard", event))
        time.sleep(0.1)

    return recorded_actions

# Record both mouse and keyboard actions for 5 seconds
recorded_mouse_actions = record_actions(duration=5)
recorded_keyboard_actions = record_keyboard_actions(duration=5)

# Save the recorded actions to a Python script
with open('recorded_actions.py', 'w') as file:
    file.write(f'''
recorded_mouse_actions = {recorded_mouse_actions}
recorded_keyboard_actions = {recorded_keyboard_actions}
''')

# Generate a new script that replays the recorded actions in a loop
looped_script = f'''
import pyautogui
import time
import keyboard

recorded_mouse_actions = {recorded_mouse_actions}
recorded_keyboard_actions = {recorded_keyboard_actions}

# Function to replay recorded mouse actions
def replay_mouse_actions():
    for action in recorded_mouse_actions:
        if action[0] == "move":
            pyautogui.moveTo(action[1], action[2])
        time.sleep(0.1)  # Adjust the sleep duration as needed

# Function to replay recorded keyboard actions
def replay_keyboard_actions():
    for action in recorded_keyboard_actions:
        event = action[1]
        time.sleep(event.time)
        keyboard.press(event.name) if event.event_type == keyboard.KEY_DOWN else keyboard.release(event.name)

# Replay the recorded actions in a loop
while True:
    replay_mouse_actions()
    replay_keyboard_actions()
'''

with open('looped_script.py', 'w') as file:
    file.write(looped_script)
