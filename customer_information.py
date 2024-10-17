import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
class CustomerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("800x700")

        # Customer Information Input 
        tk.Label(root, text="First Name").grid(row=0, column=0, padx=10, pady=10)
        self.first_name_input = tk.Entry(root)
        self.first_name_input.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Last Name").grid(row=0, column=2, padx=10, pady=10)
        self.last_name_input = tk.Entry(root)
        self.last_name_input.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(root, text="Address").grid(row=1, column=0, padx=10, pady=10)
        self.address_input = tk.Entry(root)
        self.address_input.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Phone Number").grid(row=1, column=2, padx=10, pady=10)
        self.phone_number_input = tk.Entry(root)
        self.phone_number_input.grid(row=1, column=3, padx=10, pady=10)

        tk.Label(root, text="Email Address").grid(row=2, column=0, padx=10, pady=10)
        self.email_input = tk.Entry(root)
        self.email_input.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for Actions
        self.add_customer_button = tk.Button(root, text="Add Customer", command=self.add_customer)
        self.add_customer_button.grid(row=3, column=0, padx=10, pady=10)

        self.update_customer_button = tk.Button(root, text="Update Customer", command=self.update_customer)
        self.update_customer_button.grid(row=3, column=1, padx=10, pady=10)

        self.delete_customer_button = tk.Button(root, text="Delete Customer", command=self.delete_customer)
        self.delete_customer_button.grid(row=3, column=2, padx=10, pady=10)

        self.save_to_file_button = tk.Button(root, text="Save to File", command=self.save_video)
        self.save_to_file_button.grid(row=3, column=3, padx=10, pady=10)

        # Listbox to Display Customers
        self.customer_listbox = tk.Listbox(root)
        self.customer_listbox.grid(row=4, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

        self.customers = []

    def add_customer(self):
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        address = self.address_input.get().strip()
        phone_number = self.phone_number_input.get().strip()
        email = self.email_input.get().strip()

        if not all([first_name, last_name, address, phone_number, email]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
        else:
            customer = f"{first_name} {last_name} - {phone_number} - {email} - {address}"
            self.customers.append(customer)
            self.customer_listbox.insert(tk.END, customer)
            self.clear_fields()
            messagebox.showinfo("Success", "Customer added")

    def update_customer(self):
        selected_index = self.customer_listbox.curselection()
        if selected_index:
            first_name = self.first_name_input.get().strip()
            last_name = self.last_name_input.get().strip()
            address = self.address_input.get().strip()
            phone_number = self.phone_number_input.get().strip()
            email = self.email_input.get().strip()

            if not all([first_name, last_name, address, phone_number, email]):
                messagebox.showwarning("Input Error", "Please fill in all fields")
            else:
                customer = f"{first_name} {last_name} - {phone_number} - {email} - {address}"
                self.customers[selected_index[0]] = customer
                self.customer_listbox.delete(selected_index)
                self.customer_listbox.insert(selected_index, customer)
                self.clear_fields()
                messagebox.showinfo("Success", "Customer updated")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to update")

    def delete_customer(self):
        selected_index = self.customer_listbox.curselection()
        if selected_index:
            self.customers.pop(selected_index[0])
            self.customer_listbox.delete(selected_index)
            messagebox.showinfo("Success", "Customer deleted")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to delete")

    def clear_fields(self):
        self.first_name_input.delete(0, tk.END)
        self.last_name_input.delete(0, tk.END)
        self.address_input.delete(0, tk.END)
        self.phone_number_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)


    # save file
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

    def save_to_file(self):
        with open("customers.txt", "w") as file:
            for customer in self.customers:
                file.write(customer + "\n")
        messagebox.showinfo("Success", "Customer data saved to customers.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagementApp(root)
    root.mainloop()
