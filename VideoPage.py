import tkinter as tk
from tkinter import ttk, messagebox
import os
import customer_information

DEFAULT_FILE_PATH = "videos_data.txt"


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

def load_customers_from_file(file_path="customers.txt"):
    customers = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                customer_info = line.strip().split(" - ")
                if len(customer_info) == 5:
                    customer = {
                        "first_name": customer_info[0],
                        "last_name": customer_info[1],
                        "email": customer_info[2],
                        "address": customer_info[3],
                        "phone_number": customer_info[4]
                    }
                    customers.append(customer)
    return customers

class VideoPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Page")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Initialize editing
        self.is_editing = False
        self.current_edit_index = None
        self.original_items = []

        # Title Label
        label = tk.Label(root, text="Videos Available Today", font=("Arial", 24))
        label.pack(pady=10)

        # Frame for search functionality
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
        self.create_form_fields(frame1)
        frame1.pack(padx=20, pady=20, expand=True, fill="both")

        # Frame for buttons
        self.create_buttons(root)

        # Treeview to display the videos as a table
        columns = ('Name', 'Year', 'Director', 'Rating', 'Genre', 'Rental Status')
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=150)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Store videos in a list
        self.videos = []

        # Dictionary to store rented videos with customer emails
        self.rented_videos = {}

        # Automatically open the file dialog after window initialization
        self.root.after(100, self.open_file)

    def create_form_fields(self, frame):
        labels = ["Video Name", "Year", "Director", "Rating", "Genre"]
        entries = []
        for idx, label_text in enumerate(labels):
            label = tk.Label(frame, text=label_text, font=("Arial", 12))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=1, column=idx, padx=10, pady=5, sticky="nsew")
            entries.append(entry)

        self.video, self.year, self.director, self.rating, self.genre = entries
        for col in range(5):
            frame.grid_columnconfigure(col, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def create_buttons(self, root):
        frame = tk.Frame(root)

        self.add = tk.Button(frame, text="Add Video", command=self.add_video)
        self.add.pack(side="left", pady=10, padx=10)

        self.edit = tk.Button(frame, text="Edit Video", command=self.edit_or_apply)
        self.edit.pack(side="left", pady=10, padx=10)

        self.remove = tk.Button(frame, text="Remove Video", command=self.remove_video)
        self.remove.pack(side="left", pady=10, padx=10)

        self.save = tk.Button(frame, text="Save to file", command=self.save_video)
        self.save.pack(side="left", pady=10, padx=10)

        self.checkout = tk.Button(frame, text="Check Out", command=self.check_out_video)
        self.checkout.pack(side="left", pady=10, padx=10)

        self.return_video_btn = tk.Button(frame, text="Return", command=self.return_video)
        self.return_video_btn.pack(side="left", pady=10, padx=10)

        self.rented_by = tk.Button(frame, text="Rented By", command=self.rented_by)
        self.rented_by.pack(side="left", pady=10, padx=10)

        frame.pack()

        # Store references to all buttons
        self.buttons = [self.add, self.edit, self.remove, self.save, self.checkout, self.return_video_btn, self.rented_by]

    def add_video(self):
        video_name = self.video.get().strip()
        video_year = self.year.get().strip()
        video_director = self.director.get().strip()
        video_rating = self.rating.get().strip()
        video_genre = self.genre.get().strip()

        if not all([video_name, video_year, video_director, video_rating, video_genre]):
            messagebox.showwarning("Input Error", "Please fill in all the fields.")
        else:
            new_video = Video(video_name, video_year, video_director, video_rating, video_genre)
            self.videos.append(new_video)

            self.tree.insert('', tk.END, values=(new_video.name, new_video.year, new_video.director,
                                                 new_video.rating, new_video.genre, new_video.rental_status))
            self.clear_fields()
            self.update_file()

    def edit_or_apply(self):
        if not self.is_editing:
            self.edit_video()
        else:
            self.apply_edits()

    def edit_video(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.add.config(state="disabled")
            self.remove.config(state="disabled")
            self.checkout.config(state="disabled")
            self.return_video_btn.config(state="disabled")

            item = self.tree.item(selected_item)
            video = item['values']

            self.video.delete(0, tk.END)
            self.video.insert(0, video[0])

            self.year.delete(0, tk.END)
            self.year.insert(0, video[1])

            self.director.delete(0, tk.END)
            self.director.insert(0, video[2])

            self.rating.delete(0, tk.END)
            self.rating.insert(0, video[3])

            self.genre.delete(0, tk.END)
            self.genre.insert(0, video[4])

            self.is_editing = True
            self.current_edit_index = selected_item
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
            video = self.videos[int(self.tree.index(self.current_edit_index))]
            video.name = video_name
            video.year = video_year
            video.director = video_director
            video.rating = video_rating
            video.genre = video_genre

            self.tree.item(self.current_edit_index, values=(video.name, video.year, video.director,
                                                            video.rating, video.genre, video.rental_status))

            self.add.config(state="normal")
            self.remove.config(state="normal")
            self.checkout.config(state="normal")
            self.return_video_btn.config(state="normal")

            self.clear_fields()
            self.update_file()

            self.is_editing = False
            self.current_edit_index = None
            self.edit.config(text="Edit Video")

    def remove_video(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askokcancel("Warning", "Are you sure?"):
                index = int(self.tree.index(selected_item))
                self.videos.pop(index)
                self.tree.delete(selected_item)
                self.update_file()
        else:
            messagebox.showwarning("Selection error", "Please select a video to delete")

    def check_out_video(self):
        selected_item = self.tree.selection()
        if selected_item:
            video = self.videos[int(self.tree.index(selected_item))]
            if video.check_out():
                customer_info = self.select_customer()
                if customer_info:
                    customer_email = customer_info[2]
                    self.rented_videos[video.name] = customer_email
                    self.tree.item(selected_item, values=(video.name, video.year, video.director,
                                                          video.rating, video.genre, video.rental_status))
                    
                    with open("rented_videos.txt", "a") as file:
                        file.write(f"{video.name} - {customer_email}\n")
                    self.update_file()
            else:
                messagebox.showwarning("Check out Error", "This video is already checked out.")
        else:
            messagebox.showwarning("Selection Error", "Please select a video to check out.")

    def return_video(self):
        selected_item = self.tree.selection()
        if selected_item:
            video = self.videos[int(self.tree.index(selected_item))]
            if video.return_video():
                self.rented_videos.pop(video.name, None)
                self.tree.item(selected_item, values=(video.name, video.year, video.director,
                                                      video.rating, video.genre, video.rental_status))
                self.update_file()
            else:
                messagebox.showwarning("Return Error", "This video is already available.")
        else:
            messagebox.showwarning("Selection Error", "Please select a video to return.")

    def open_file(self):
        if os.path.exists(DEFAULT_FILE_PATH):
            self.tree.delete(*self.tree.get_children())
            self.videos = []

            with open(DEFAULT_FILE_PATH, 'r') as file:
                for line in file:
                    video_info = line.strip().split(" | ")
                    if len(video_info) == 6:
                        video = Video(video_info[0], video_info[1], video_info[2],
                                      video_info[3], video_info[4], video_info[5])
                        self.videos.append(video)
                        self.tree.insert('', tk.END, values=(video.name, video.year, video.director,
                                                             video.rating, video.genre, video.rental_status))

    def save_video(self):
        try:
            with open(DEFAULT_FILE_PATH, 'w') as file:
                for video in self.videos:
                    file.write(str(video) + "\n")
                messagebox.showinfo("Save Successful", "The video data has been saved!")
                
            self.root.lift()
            self.root.focus_force()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def update_file(self):
        try:
            with open(DEFAULT_FILE_PATH, 'w') as file:
                for video in self.videos:
                    file.write(str(video) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating file: {str(e)}")

    def search_videos(self):
        search_term = self.search.get().strip().lower()

        self.tree.delete(*self.tree.get_children())
        self.root.update()

        results = [video for video in self.videos if (
                search_term in video.name.lower() or
                search_term in video.year.lower() or
                search_term in video.director.lower() or
                search_term in video.rating.lower() or
                search_term in video.genre.lower()
        )]

        for video in results:
            self.tree.insert('', tk.END, values=(video.name, video.year, video.director,
                                                 video.rating, video.genre, video.rental_status))
        self.root.update()
        if not results:
            messagebox.showinfo("No Results", "No videos matched your search.")

    def rented_by(self):
        self.root.lift()
        self.root.focus_force()
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            video_name = item['values'][0]

            rentals = []
            
            with open("rented_videos.txt", "r") as file:
                for line in file:
                    rental_info = line.strip().split(" - ")
                    if rental_info[0] == video_name:
                        rentals.append(rental_info[1])
                    
            if rentals:
                rental_details = []
                for email in rentals:
                    customer_info = customer_information.get_customer_info_by_email(email)
                    if customer_info:
                        name = f"{customer_info.get('first_name', 'Unknown')} {customer_info.get('last_name', 'Unknown')}"
                        phone = customer_info.get("phone", "No phone number available")
                        rental_details.append(f"Name: {name}\nEmail: {email}\nPhone: {phone}")

            # Display all past renters in a popup
                rental_history = "\n\n".join(rental_details)
                messagebox.showinfo("Rental History", f"Past rentals for '{video_name}':\n\n{rental_history}")
            else:
                messagebox.showerror("Rented By", "No rental information found for this movie.")
        else:
            messagebox.showerror("Selection Error", "Please select a video to check renter information.")

    def clear_fields(self):
        self.video.delete(0, tk.END)
        self.year.delete(0, tk.END)
        self.director.delete(0, tk.END)
        self.rating.delete(0, tk.END)
        self.genre.delete(0, tk.END)

    def select_customer(self):
        self.root.lift()
        self.root.focus_force()
        for button in self.buttons:
            button.config(state="disabled")

        customer_window = tk.Toplevel(self.root)
        customer_window.title("Select Customer")
        customer_window.geometry("400x300")
        
        customer_window.attributes("-topmost", True)

        # Create a Treeview to display customers
        customer_tree = ttk.Treeview(customer_window, columns=("First Name", "Last Name", "Email"), show="headings")
        customer_tree.heading("First Name", text="First Name")
        customer_tree.heading("Last Name", text="Last Name")
        customer_tree.heading("Email", text="Email")
        customer_tree.pack(fill=tk.BOTH, expand=True)

        # Populate the Treeview with customer data
        for customer in self.get_customers():
            customer_tree.insert("", tk.END, values=(customer["first_name"], customer["last_name"], customer["email"]))


        selected_customer = None

        def confirm_selection():
            nonlocal selected_customer
            selected_item = customer_tree.selection()
            if selected_item:
                selected_customer = customer_tree.item(selected_item, "values")
                customer_window.destroy()
            else:
                messagebox.showwarning("Selection Error", "Please select a customer.")

        confirm_button = tk.Button(customer_window, text="Confirm", command=confirm_selection)
        confirm_button.pack(pady=10)

        customer_window.wait_window()
        for button in self.buttons:
            button.config(state="normal")
        return selected_customer

    def get_customers(self):
        return load_customers_from_file()


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = VideoPage(root)
    root.mainloop()
