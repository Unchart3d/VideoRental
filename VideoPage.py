import tkinter as tk
from tkinter import messagebox

class VideoPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Page")
        self.root.geometry("2000x1200")
        
        #Label
        label = tk.Label(root, text="Video's available today", font=("Arial", 24))
        label.pack()
        
        #Video input fields
        self.video = tk.Entry(root, width=40)
        self.video.pack(pady=10)
        
        #Buttons for video input
        frame = tk.Frame(root)
        self.add = tk.Button(frame, text="Add Video", command=self.add_video)
        self.add.pack(side="left", pady=10, padx=10)
        self.remove = tk.Button(frame, text="Remove Video", command=self.remove_video)
        self.remove.pack(side="left", pady=10, padx=10)
        self.more = tk.Button(frame, text="See More", command=self.more_info)
        self.more.pack(side="left", pady=10, padx=10)
        frame.pack()
        
        #Listbox for videos
        self.listbox = tk.Listbox(root, height=20, width=100, bg="lightgrey", 
                                  activestyle='dotbox', font=("Arial", 18), fg="black")
        self.listbox.pack()
        
        self.videos = []
        
    def add_video(self):
        video_name = self.video.get().strip()
        
        if not video_name:
            messagebox.showwarning("Input Error", "Please enter a video name.")
        else:
            self.videos.append(video_name)
            self.listbox.insert(tk.END, video_name)
            self.clear_fields()
    
    def remove_video(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.videos.pop(selected_index[0])
            self.listbox.delete(selected_index)
        else:
            messagebox.showwarning("Selection error", "Please select a video to delete")
            
    def more_info(self):
        pass
    
    def clear_fields(self):
        self.video.delete(0, tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPage(root)
    root.mainloop()