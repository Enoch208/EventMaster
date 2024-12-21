import os
import json
from pathlib import Path

def ensure_recordings_dir():
    """Create the recordings directory if it doesn't exist"""
    Path("recordings").mkdir(exist_ok=True)

def list_recordings():
    """Return a list of all recording files in the recordings directory"""
    ensure_recordings_dir()
    recordings = []
    for file in os.listdir("recordings"):
        if file.endswith(".json"):
            try:
                with open(os.path.join("recordings", file), 'r') as f:
                    data = json.load(f)
                    recordings.append({
                        'filename': file,
                        'duration': data['metadata']['duration'],
                        'event_count': data['metadata']['event_count']
                    })
            except (json.JSONDecodeError, KeyError):
              
                continue
    return recordings

def delete_recording(filename):
    """Delete a recording file"""
    try:
        os.remove(os.path.join("recordings", filename))
        return True
    except OSError:
        return False

def validate_filename(filename):
    """Validate and clean a filename"""
    
    filename = os.path.basename(filename)
    
    
    if not filename.endswith('.json'):
        filename += '.json'
        
  
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
        
    return filename
