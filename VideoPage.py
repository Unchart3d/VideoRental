import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class VideoPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Page")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Title Label
        label = tk.Label(root, text="Videos Available Today", font=("Arial", 24))
        label.pack(pady=10)

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

        # Remove Video Button
        self.remove = tk.Button(frame, text="Remove Video", command=self.remove_video)
        self.remove.pack(side="left", pady=10, padx=10)

        # Save Button
        self.save = tk.Button(frame, text="Save to file", command=self.save_video)
        self.save.pack(side="left", pady=10, padx=10)

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
            # Create a string representing the video
            video_info = f"{video_name} | {video_year} | {video_director} | {video_rating} | {video_genre}"
            self.videos.append(video_info)
            self.listbox.insert(tk.END, video_info)
            self.clear_fields()

            # Save changes to file
            self.update_file()

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
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                     ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for video in self.videos:
                        file.write(video + "\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def open_file(self):
        # Open a file and load its contents into the listbox
        file_path = filedialog.askopenfilename(title="Open a file", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.listbox.delete(0, tk.END)
            self.videos = []

            with open(file_path, 'r') as file:
                for line in file:
                    video = line.strip()
                    self.videos.append(video)
                    self.listbox.insert(tk.END, video)

    def update_file(self):
        # Overwrite the file with the current list of videos
        try:
            with open("demofile.txt", 'w') as file:
                for video in self.videos:
                    file.write(video + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating file: {str(e)}")

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
