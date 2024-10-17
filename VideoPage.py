import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class Video:
    def __init__(self, name, year, director, rating, genre, rental_status="Available"):
        self.name = name
        self.year = year
        self.director = director
        self.rating = rating
        self.genre = genre
        self.rental_status = rental_status
        
    def __str__(self):
        return f"{self.name} | {self.year} | {self.director} | {self.rating} | {self.genre} | {self.rental_status}"
    
    def check_out(self):
        if self.rental_status == "Available":
            self.rental_status = "Checked Out"
            return True
        return False
    
    def return_video(self):
        if self.rental_status == "Checked Out":
            self.rental_status = "Available"
            return True
        return False

class VideoPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Page")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        #Initialize editing
        self.is_editing = False
        self.current_edit_index = None
        
        self.original_items = []

        # Title Label
        label = tk.Label(root, text="Videos Available Today", font=("Arial", 24))
        label.pack(pady=10)
        
        frame2 = tk.Frame(root)

        self.search_label = tk.Label(frame2, text="Search Videos", font=("Arial", 12))
        self.search_label.grid(row=0, column=0, columnspan=2, pady=10)  

        self.search = tk.Entry(frame2, width=30)
        self.search.grid(row=1, column=0, sticky="nsew", pady=10)  

        self.search_button = tk.Button(frame2, text="Search", command=self.search_videos)
        self.search_button.grid(row=1, column=1, sticky="nsew", pady=10)  

        frame2.pack() 


        # Frame for the entry fields
        frame1 = tk.Frame(root)

        # Video Name Entry
        self.vidlabel = tk.Label(frame1, text="Video Name", font=("Arial", 12))
        self.vidlabel.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.video = tk.Entry(frame1, width=30)
        self.video.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Year Entry
        self.yearlabel = tk.Label(frame1, text="Year", font=("Arial", 12))
        self.yearlabel.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.year = tk.Entry(frame1, width=30)
        self.year.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        # Director Entry
        self.dirlabel = tk.Label(frame1, text="Director", font=("Arial", 12))
        self.dirlabel.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        self.director = tk.Entry(frame1, width=30)
        self.director.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        # Rating Entry
        self.ratlabel = tk.Label(frame1, text="Rating", font=("Arial", 12))
        self.ratlabel.grid(row=0, column=3, padx=10, pady=5, sticky="nsew")
        self.rating = tk.Entry(frame1, width=30)
        self.rating.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")

        # Genre Entry
        self.genlabel = tk.Label(frame1, text="Genre", font=("Arial", 12))
        self.genlabel.grid(row=0, column=4, padx=10, pady=5, sticky="nsew")
        self.genre = tk.Entry(frame1, width=30)
        self.genre.grid(row=1, column=4, padx=10, pady=5, sticky="nsew")

        # Pack the frame with entry fields
        frame1.pack(padx=20, pady=20, expand=True, fill="both")

        # Set grid weights for even spacing
        for col in range(5):
            frame1.grid_columnconfigure(col, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_rowconfigure(1, weight=1)

        # Frame for buttons
        frame = tk.Frame(root)

        # Add Video Button
        self.add = tk.Button(frame, text="Add Video", command=self.add_video)
        self.add.pack(side="left", pady=10, padx=10)
        
        # Edit Video Button
        self.edit = tk.Button(frame, text="Edit Video", command=self.edit_or_apply)
        self.edit.pack(side="left", pady=10, padx=10)

        # Remove Video Button
        self.remove = tk.Button(frame, text="Remove Video", command=self.remove_video)
        self.remove.pack(side="left", pady=10, padx=10)

        # Save Button
        self.save = tk.Button(frame, text="Save to file", command=self.save_video)
        self.save.pack(side="left", pady=10, padx=10)
        
        self.checkout = tk.Button(frame, text="Check Out", command=self.check_out_video)
        self.checkout.pack(side="left", pady=10, padx=10)
        
        self.return_video = tk.Button(frame, text="Return", command=self.return_video)
        self.return_video.pack(side="left", pady=10, padx=10)

        # Pack the button frame
        frame.pack()

        # Listbox to display the videos
        self.listbox = tk.Listbox(root, height=20, width=100, bg="lightgrey",
                                  activestyle='dotbox', font=("Arial", 18), fg="black")
        self.listbox.pack()

        # Store videos in a list
        self.videos = []

        # Automatically open the file dialog after window initialization
        self.root.after(100, self.open_file)

    def add_video(self):
        # Get the input values
        video_name = self.video.get().strip()
        video_year = self.year.get().strip()
        video_director = self.director.get().strip()
        video_rating = self.rating.get().strip()
        video_genre = self.genre.get().strip()

        # Check if all fields are filled
        if not all([video_name, video_year, video_director, video_rating, video_genre]):
            messagebox.showwarning("Input Error", "Please fill in all the fields.")
        else:
            new_video = Video(video_name, video_year, video_director, video_rating, video_genre)
            
            self.videos.append(new_video)
            
            self.listbox.insert(tk.END, str(new_video))
            
            self.clear_fields()
            
            self.update_file()
            
            self.original_items = [str(video) for video in self.videos]
            
    def edit_or_apply(self):
        if not self.is_editing:
            self.edit_video()
        else:
            self.apply_edits()
            
    def edit_video(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            video = self.videos[selected_index[0]]
            
            self.video.delete(0, tk.END)
            self.video.insert(0, video.name)
            
            self.year.delete(0, tk.END)
            self.year.insert(0, video.year)

            self.director.delete(0, tk.END)
            self.director.insert(0, video.director)

            self.rating.delete(0, tk.END)
            self.rating.insert(0, video.rating)

            self.genre.delete(0, tk.END)
            self.genre.insert(0, video.genre)
            
            self.is_editing = True
            self.current_edit_index = selected_index[0]
            
            self.edit.config(text="Apply Changes")
        else:
            messagebox.showwarning("Selection Error", "Please select a video to edit.")
            
    def apply_edits(self):
        video_name = self.video.get().strip()
        video_year = self.year.get().strip()
        video_director = self.director.get().strip()
        video_rating = self.rating.get().strip()
        video_genre = self.genre.get().strip()
        
        if not all([video_name, video_year, video_director, video_rating, video_genre]):
            messagebox.showwarning("Input Error", "Please fill in all the fields.")
        else:
            video = self.videos[self.current_edit_index]
            video.name = video_name
            video.year = video_year
            video.director = video_director
            video.rating = video_rating
            video.genre = video_genre
            
        self.listbox.delete(self.current_edit_index)
        self.listbox.insert(self.current_edit_index, str(video))
        
        self.clear_fields()
        
        self.update_file()
        
        self.is_editing = False
        self.current_edit_index = None
        self.edit.config(text="Edit Video")

    def remove_video(self):
        # Get the selected video index
        selected_index = self.listbox.curselection()
        if selected_index:
            # Ask for confirmation before removing
            if messagebox.askokcancel("Warning", "Are you sure?"):
                self.videos.pop(selected_index[0])
                self.listbox.delete(selected_index)

                # Save changes to file
                self.update_file()
        else:
            messagebox.showwarning("Selection error", "Please select a video to delete")

    def save_video(self):
    # Save the videos to a file chosen by the user
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for video in self.videos:
                    # Save each video's information, including rental status
                        file.write(str(video) + "\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")


    def check_out_video(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            video = self.videos[selected_index[0]]
            
            if video.check_out():
                self.listbox.delete(selected_index)
                self.listbox.insert(selected_index, str(video))
                self.update_file()
            else:
                messagebox.showwarning("Check out Error", "This video is already checked out.")
        else:
            messagebox.showwarning("Selection Error", "Please select a video to check out.")
            
    def return_video(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            video = self.videos[selected_index[0]]
            
            if video.return_video():
                self.listbox.delete(selected_index)
                self.listbox.insert(selected_index, str(video))
                self.update_file()
            else:
                messagebox.showwarning("Return Error", "This video is already available.")
        else:
            messagebox.showwarning("Selection Error", "Please select a video to return.")
            
            
    def open_file(self):
        # Open a file and load its contents into the listbox
        file_path = filedialog.askopenfilename(title="Open a file", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.listbox.delete(0, tk.END)
            self.videos = []

            with open(file_path, 'r') as file:
                for line in file:
                    video_info = line.strip().split(" | ")
                    if len(video_info) == 6:
                        video = Video(video_info[0],  video_info[1], video_info[2], video_info[3], video_info[4], video_info[5])
                        self.videos.append(video)
                        self.listbox.insert(tk.END, str(video))
            
            self.original_items = [str(video) for video in self.videos]

    def update_file(self):
        # Overwrite the file with the current list of videos
        try:
            with open("demofile.txt", 'w') as file:
                for video in self.videos:
                    file.write(str(video) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating file: {str(e)}")
            
    def search_videos(self):
        if self.search_button['text'] == "Search":
            search_term = self.search.get().strip()
            listbox_items = self.listbox.get(0, tk.END)
            results = [item for item in listbox_items if search_term.lower() in item.lower()]
        
            self.listbox.delete(0, tk.END)
            for result in results:
                self.listbox.insert(tk.END, results)
                
            if results:
                self.search_button.config(text="Undo Search")
        else:
            self.listbox.delete(0, tk.END)
            for item in self.original_items:
                self.listbox.insert(tk.END, item)
                
            self.search_button.config(text="Search")
            self.search.delete(0, tk.END)

    def clear_fields(self):
        # Clear the input fields
        self.video.delete(0, tk.END)
        self.year.delete(0, tk.END)
        self.director.delete(0, tk.END)
        self.rating.delete(0, tk.END)
        self.genre.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPage(root)
    root.mainloop()
