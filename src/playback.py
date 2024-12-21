from pynput import mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import json
import time
import threading
import os

class EventPlayer:
    def __init__(self):
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        self.playing = False
        self.play_thread = None
        self.recording = None  

    def load_recording(self, filename):
        try:
            if os.path.isfile(filename):
                filepath = filename
            else:
                filepath = f"recordings/{filename}"
                
            with open(filepath, 'r') as f:
                self.recording = json.load(f)
                return self.recording['metadata']
        except Exception as e:
            print(f"Error loading recording: {e}")
            self.recording = None
            return None

    def play_events(self, progress_callback=None):
        if not self.recording:
            print("No recording loaded")
            return

        events = self.recording['events']
        self.playing = True
        
        for i, event in enumerate(events):
            if not self.playing:
                break

            if progress_callback:
                progress = (i + 1) / len(events) * 100
                progress_callback(progress)

            if i > 0:
                time_diff = event['time'] - events[i-1]['time']
                time.sleep(time_diff / 1000)

            self._play_event(event)

        self.playing = False
        if progress_callback:
            progress_callback(100)

    def _play_event(self, event):
        event_type = event['type']
        
        if event_type == 'mouse_move':
            self.mouse_controller.position = (event['x'], event['y'])
        
        elif event_type == 'mouse_click':
            self.mouse_controller.position = (event['x'], event['y'])
            if event['pressed']:
                self.mouse_controller.press(eval(f"mouse.Button.{event['button'].split('.')[-1]}"))
            else:
                self.mouse_controller.release(eval(f"mouse.Button.{event['button'].split('.')[-1]}"))
        
        elif event_type == 'mouse_scroll':
            self.mouse_controller.scroll(event['dx'], event['dy'])
        
        elif event_type in ['key_press', 'key_release']:
            try:
                if 'Key.' in event['key']:
                    
                    key_name = event['key'].split('.')[-1]
                    key = getattr(Key, key_name)
                else:
                
                    key = event['key'].strip("'")
                
                if event_type == 'key_press':
                    self.keyboard_controller.press(key)
                else:
                    self.keyboard_controller.release(key)
            except (AttributeError, ValueError) as e:
                print(f"Error processing key event: {event['key']}")

    def start_playback(self, progress_callback=None):
        self.play_thread = threading.Thread(target=self.play_events, args=(progress_callback,))
        self.play_thread.start()

    def stop_playback(self):
        self.playing = False
        if self.play_thread:
            self.play_thread.join()
