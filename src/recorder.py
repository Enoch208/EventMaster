from pynput import mouse, keyboard
import json
import time
from threading import Thread
from datetime import datetime
import os

class EventRecorder:
    def __init__(self):
        self.events = []
        self.recording = False
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
    def start_recording(self):
     
        os.makedirs("recordings", exist_ok=True)
        
        self.events = []
        self.recording = True
        self.start_time = time.perf_counter_ns() 
       
        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
    
    def _get_timestamp(self):
        return (time.perf_counter_ns() - self.start_time) / 1_000_000
    def _on_move(self, x, y):
        if self.recording:
            self.events.append({
                'type': 'mouse_move',
                'x': x,
                'y': y,
                'time': self._get_timestamp()
            })
    
    def _on_click(self, x, y, button, pressed):
        if self.recording:
            self.events.append({
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'time': self._get_timestamp()
            })
    
    def _on_scroll(self, x, y, dx, dy):
        if self.recording:
            self.events.append({
                'type': 'mouse_scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'time': self._get_timestamp()
            })
    
    def _on_press(self, key):
        if self.recording:
            self.events.append({
                'type': 'key_press',
                'key': str(key),
                'time': self._get_timestamp()
            })
    
    def _on_release(self, key):
        if self.recording:
            self.events.append({
                'type': 'key_release',
                'key': str(key),
                'time': self._get_timestamp()
            })
    
    def stop_recording(self):
        if self.mouse_listener and self.keyboard_listener:
            self.recording = False
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
    
    def save_recording(self, filename=None):
        if filename is None:
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(f"recordings/{filename}", 'w') as f:
            json.dump({
                'events': self.events,
                'metadata': {
                    'duration': self._get_timestamp(),
                    'event_count': len(self.events)
                }
            }, f, indent=2)
        return filename
