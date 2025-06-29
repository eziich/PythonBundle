import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import yt_dlp

class YouTubeDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x350")
        self.root.configure(bg='white')
        
        self.download_path = ""
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="YouTube Video Downloader", font=("Arial", 18, "bold"), bg='white').pack(pady=(0, 20))
        
        tk.Label(main_frame, text="YouTube URL:", font=("Arial", 11, "bold"), bg='white').pack(anchor="w")
        self.url_entry = tk.Entry(main_frame, font=("Arial", 11), width=50)
        self.url_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(main_frame, text="Download Folder:", font=("Arial", 11, "bold"), bg='white').pack(anchor="w")
        dest_frame = tk.Frame(main_frame, bg='white')
        dest_frame.pack(fill="x", pady=(5, 25))
        
        self.dest_entry = tk.Entry(dest_frame, font=("Arial", 11))
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.dest_entry.insert(0, "Select folder...")
        self.dest_entry.config(state='readonly')
        
        tk.Button(dest_frame, text="Browse", command=self.browse_folder, font=("Arial", 10), bg='lightblue').pack(side="right")
        
        self.download_btn = tk.Button(
            main_frame, 
            text="DOWNLOAD VIDEO", 
            command=self.start_download,
            font=("Arial", 14, "bold"),
            bg='green',
            fg='white',
            width=18,
            height=2
        )
        self.download_btn.pack()
        
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 10), bg='white', fg='blue')
        self.status_label.pack(pady=(10, 0))
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.dest_entry.config(state='normal')
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)
            self.dest_entry.config(state='readonly')
        
    def start_download(self):
        if self.is_downloading:
            return
            
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not self.download_path:
            messagebox.showerror("Error", "Please select a download folder")
            return
            
        self.is_downloading = True
        self.download_btn.config(state="disabled", text="DOWNLOADING...", bg='orange')
        self.status_label.config(text="Starting download...")
        
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()
        
    def get_format_selector(self):
        return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', 'N/A').strip()
                speed = d.get('_speed_str', 'N/A').strip()
                self.status_label.config(text=f"Downloading... {percent} at {speed}")
            except:
                self.status_label.config(text="Downloading...")
        elif d['status'] == 'finished':
            self.status_label.config(text="Processing...")
        
    def download_video(self, url):
        try:
            format_selector = self.get_format_selector()
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'no_warnings': False,
                'ignoreerrors': False,
            }
            
            self.status_label.config(text="Fetching video info...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')
                    self.status_label.config(text=f"Found: {title[:50]}...")
                except Exception as e:
                    self.status_label.config(text=f"Error getting info: {str(e)}")
                    return
                
                ydl.download([url])
                
            self.status_label.config(text="Download completed!")
            messagebox.showinfo("Success", f"Download completed successfully to:\n{self.download_path}")
            
        except Exception as e:
            error_msg = str(e)
            self.status_label.config(text="Download failed!")
            messagebox.showerror("Error", f"Download failed:\n{error_msg}")
            
        finally:
            self.is_downloading = False
            self.download_btn.config(state="normal", text="DOWNLOAD VIDEO", bg='green')
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    YouTubeDownloader().run()