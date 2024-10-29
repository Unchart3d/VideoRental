import tkinter as tk
import subprocess
from customer_information import CustomerManagementApp
from VideoPage import VideoPage
from tkinter import messagebox


class VideoHomepage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Homepage")
        self.root.geometry("1000x500")
        
        title_frame = tk.Frame(self.root, height=40)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        title_frame.grid_propagate(False)
                
        title_label = tk.Label(title_frame, text="Video Store Homepage", bg="gray", font=("Noteworthy", 36))
        title_label.pack(pady=5)
        
        self.root.grid_columnconfigure(0, weight=1)  # Column 1
        self.root.grid_columnconfigure(1, weight=0)  # Column for the line
        self.root.grid_columnconfigure(2, weight=1)  # Column 2
        
        l1 = tk.Label(self.root, text="Video Inventory", anchor='n', font=("Noteworthy", 36))
        l1.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0))
        
        line = tk.Frame(self.root, width=2, bg="black")
        line.grid(row=1, column=1, rowspan=4, sticky=tk.NS)
        
        l2 = tk.Label(self.root, text="Customer Information", anchor='n', font=("Noteworthy", 36))
        l2.grid(row=1, column=2, sticky=tk.NSEW, padx=10, pady=(10, 0))
        
        self.root.grid_rowconfigure(1, weight=1) 
        self.root.grid_rowconfigure(2, weight=1)        
        #column 1 buttons
        
        b1 = tk.Button(self.root, text= "+ Add Videos", height=5, command=self.open_addvid, font=('Noteworthy', 18))
        b1.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        
        #column 2 buttons
        
        b3 = tk.Button(self.root, text= "+ Add Customer", height=5, command=self.open_addcus, font=('Noteworthy', 18))
        b3.grid(row=4, column=2, sticky='ew', padx=5, pady=5)
        
        #button functionality
   
    def open_addcus(self):
        new_window = tk.Toplevel(self.root)
        CustomerManagementApp(new_window)
        
        
    def open_addvid(self):
        new_window = tk.Toplevel(self.root)
        VideoPage(new_window)  

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoHomepage(root)
    root.mainloop()

