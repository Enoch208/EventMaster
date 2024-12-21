import tkinter as tk
from tkinter import ttk, filedialog
from .recorder import EventRecorder
from .playback import EventPlayer
import os
from datetime import datetime
import threading
import ttkthemes

class ModernUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.recorder = EventRecorder()
        self.player = EventPlayer()
        
        self.theme = ttkthemes.ThemedStyle(parent)
        self.theme.set_theme("default")
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        
        self.style.configure('Main.TFrame', background='#FFFFFF')
        
        self.style.configure('Action.TButton',
                           padding=(20, 12),
                           font=('Helvetica', 10, 'bold'),
                           background='#2196F3',
                           foreground='#FFFFFF',
                           borderwidth=0)
        
        self.style.map('Action.TButton',
                       background=[('active', '#1976D2'), ('disabled', '#FFFFFF')],
                       foreground=[('disabled', '#757575')])
        
        self.style.configure('Secondary.TButton',
                           padding=(15, 10),
                           font=('Helvetica', 10),
                           background='#FFFFFF',
                           foreground='#2196F3',
                           borderwidth=1)
        
        self.style.map('Secondary.TButton',
                       background=[('active', '#F5F5F5'), ('disabled', '#FFFFFF')],
                       foreground=[('disabled', '#BDBDBD')])
        
        self.style.configure('Title.TLabel',
                           font=('Helvetica', 24, 'bold'),
                           foreground='#212121',
                           background='#FFFFFF',
                           padding=(0, 15))
        
        self.style.configure('Info.TLabel',
                           font=('Helvetica', 11),
                           foreground='#424242',
                           background='#FFFFFF',
                           padding=(5, 5))
        
        self.style.configure('Card.TFrame',
                           background='#FFFFFF',
                           relief='flat',
                           borderwidth=0)
        
        self.style.configure('TLabelframe',
                           background='#FFFFFF',
                           foreground='#212121',
                           padding=15)
        
        self.style.configure('TLabelframe.Label',
                           font=('Helvetica', 11, 'bold'),
                           foreground='#212121',
                           background='#FFFFFF')
        
        self.style.configure("Modern.Horizontal.TProgressbar",
                           thickness=6,
                           background='#2196F3',
                           troughcolor='#FFFFFF',
                           borderwidth=0)

    def setup_ui(self):
        self.configure(style='Main.TFrame', padding="30")
        
        title_frame = ttk.Frame(self, style='Main.TFrame')
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        ttk.Label(title_frame,
                 text="⚡ EventMaster pro",
                 style='Title.TLabel').pack()

        record_frame = ttk.LabelFrame(self,
                                    text="Recording",
                                    padding="20")
        record_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        self.filename_var = tk.StringVar()
        filename_frame = ttk.Frame(record_frame, style='Card.TFrame')
        filename_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(filename_frame,
                 text="📝 Recording name:",
                 style='Info.TLabel').pack(side='left')
        
        entry = ttk.Entry(filename_frame,
                         textvariable=self.filename_var,
                         width=35,
                         font=('Helvetica', 10))
        entry.pack(side='left', padx=10)

        btn_frame = ttk.Frame(record_frame, style='Card.TFrame')
        btn_frame.pack(fill='x', pady=5)
        
        self.record_btn = ttk.Button(btn_frame,
                                   text="🔴 Start Recording",
                                   style='Action.TButton',
                                   command=self.toggle_recording)
        self.record_btn.pack(pady=5)

        playback_frame = ttk.LabelFrame(self,
                                      text="Playback Controls",
                                      padding="20")
        playback_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        control_frame = ttk.Frame(playback_frame, style='Card.TFrame')
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame,
                  text="📂 Load Recording",
                  style='Secondary.TButton',
                  command=self.load_recording).pack(side='left', padx=5)
        
        self.play_btn = ttk.Button(control_frame,
                                 text="▶️ Play",
                                 style='Action.TButton',
                                 command=self.toggle_playback)
        self.play_btn.pack(side='left', padx=5)

        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(playback_frame,
                                      variable=self.progress_var,
                                      style="Modern.Horizontal.TProgressbar",
                                      length=300,
                                      mode='determinate')
        self.progress.pack(fill='x', pady=15)

        self.status_var = tk.StringVar(value="✨ Ready")
        status_label = ttk.Label(self,
                               textvariable=self.status_var,
                               style='Info.TLabel')
        status_label.grid(row=3, column=0, pady=10)

        list_frame = ttk.LabelFrame(self,
                                  text="Recent Recordings",
                                  padding="20")
        list_frame.grid(row=4, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        self.recording_list = tk.Listbox(list_frame,
                                       height=6,
                                       width=45,
                                       yscrollcommand=scrollbar.set,
                                       font=('Helvetica', 10),
                                       selectmode='single',
                                       bg='#FFFFFF',
                                       fg='#212121',
                                       selectbackground='#2196F3',
                                       selectforeground='#FFFFFF',
                                       borderwidth=1,
                                       highlightthickness=1,
                                       highlightcolor='#2196F3',
                                       highlightbackground='#FFFFFF')
        self.recording_list.pack(fill='both', expand=True, pady=5)
        scrollbar.config(command=self.recording_list.yview)

        self.update_recording_list()
        
        self.recording = False
        self.playing = False

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.record_btn.configure(text="⏹️ Stop Recording")
        self.status_var.set("🔴 Recording in progress...")
        self.recorder.start_recording()

    def stop_recording(self):
        self.recording = False
        self.record_btn.configure(text="🔴 Start Recording")
        
        filename = self.filename_var.get().strip()
        if not filename:
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        elif not filename.endswith('.json'):
            filename += '.json'
            
        saved_file = self.recorder.save_recording(filename)
        self.status_var.set(f"💾 Saved as: {saved_file}")
        self.recorder.stop_recording()
        self.filename_var.set("")
        self.update_recording_list()

    def toggle_playback(self):
        if not self.playing:
            self.start_playback()
        else:
            self.stop_playback()

    def start_playback(self):
        self.playing = True
        self.play_btn.configure(text="⏹️ Stop")
        self.status_var.set("▶️ Playing...")
        self.player.start_playback(self.update_progress)

    def stop_playback(self):
        self.playing = False
        self.play_btn.configure(text="▶️ Play")
        self.player.stop_playback()
        self.status_var.set("⏹️ Playback stopped")

    def load_recording(self):
        filename = filedialog.askopenfilename(
            initialdir="recordings",
            title="Select recording",
            filetypes=(("JSON files", "*.json"),)
        )
        if filename:
            metadata = self.player.load_recording(os.path.basename(filename))
            self.status_var.set(f"📂 Loaded: {os.path.basename(filename)}")

    def update_progress(self, value):
        self.progress_var.set(value)
        if value >= 100:
            self.playing = False
            self.play_btn.configure(text="▶️ Play")
            self.status_var.set("✅ Playback completed")

    def update_recording_list(self):
        self.recording_list.delete(0, tk.END)
        if os.path.exists("recordings"):
            for file in os.listdir("recordings"):
                if file.endswith(".json"):
                    self.recording_list.insert(tk.END, f"📄 {file}")

class RecorderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EventMaster pro")
        self.root.configure(bg='#FFFFFF')
        
        window_width = 550
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.root.resizable(True, True)
        
        self.app = ModernUI(self.root)
        self.app.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
