import tkinter as tk
import subprocess
from customer_information import CustomerManagementApp
from VideoPage import VideoPage
from tkinter import messagebox


class VideoHomepage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Homepage")
        self.root.geometry("800x600")
        
        title_frame = tk.Frame(self.root, height=40)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        title_frame.grid_propagate(False)
                
        title_label = tk.Label(title_frame, text="Video Store Homepage", bg="gray", font=("Arial", 24))
        title_label.pack(pady=5)

        

        search_frame = tk.Frame(self.root)
        search_frame.grid(row=1, column=0, pady=10, sticky="ew") 
 
        search_label = tk.Label(search_frame, text="Search:", font=("Noteworthy", 18))
        search_label.pack(side=tk.LEFT)
 
        self.search_entry = tk.Entry(search_frame, width=15, font=("Noteworthy", 18))
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))
 
        search_button = tk.Button(search_frame, text="Search", command=self.search, font=("Noteworthy", 18))
        search_button.pack(side=tk.LEFT, padx=(5, 0))

        
        
        self.root.grid_columnconfigure(0, weight=1)  # Column 1
        self.root.grid_columnconfigure(1, weight=0)  # Column for the line
        self.root.grid_columnconfigure(2, weight=1)  # Column 2
        
        l1 = tk.Label(self.root, text="Video Inventory", anchor='n')
        l1.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=(10, 0))
        
        line = tk.Frame(self.root, width=2, bg="black")
        line.grid(row=1, column=1, rowspan=4, sticky=tk.NS)
        
        l2 = tk.Label(self.root, text="Customer Information", anchor='n')
        l2.grid(row=1, column=2, sticky=tk.NSEW, padx=10, pady=(10, 0))
        
        self.root.grid_rowconfigure(1, weight=1)
        
        #column 1 buttons
        
        b1 = tk.Button(self.root, text= "+ Add Videos", height=3, command=self.open_addvid)
        b1.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        #column 2 buttons
        
        b3 = tk.Button(self.root, text= "+ Add Customer", height=3, command=self.open_addcus)
        b3.grid(row=2, column=2, sticky='ew', padx=5, pady=5)

        #button functionality

    def search(self):
        query = self.search_entry.get()
        messagebox.showinfo("Search", f"You searched for: {query}")

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


