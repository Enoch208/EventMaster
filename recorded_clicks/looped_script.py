import pyautogui
import time

recorded_mouse_actions = [('move', 234, 242), ('move', 234, 242), ('move', 287, 231), ('move', 413, 198), ('move', 407, 166), ('move', 384, 85), ('move', 376, 83), ('move', 370, 93), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96), ('move', 369, 96)]
recorded_keyboard_actions = ['f', 'm', 'space', 'space', 'k', 'n', 'n', 'v', 'space', 'backspace', 'backspace', 'ctrl']

# Function to replay recorded mouse actions
def replay_mouse_actions():
    for action in recorded_mouse_actions:
        if action[0] == "move":
            pyautogui.moveTo(action[1], action[2])
         # Adjust the sleep duration as needed

# Function to replay recorded keyboard actions
def replay_keyboard_actions():
    for key in recorded_keyboard_actions:
        time.sleep(0.1)
        pyautogui.press(key)

# Replay the recorded actions in a loop
while True:
    replay_mouse_actions()
    replay_keyboard_actions()
