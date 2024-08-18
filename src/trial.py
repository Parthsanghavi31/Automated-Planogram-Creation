import tkinter as tk, os
from tkinter import ttk
import pandas as pd
from math import ceil
from Planogram_Packing_algo_v3 import Product, Bin, fit_products_into_bins

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Manager")
        self.geometry("1024x768")
        self.products = []
        self.bins = []
        self.selected_products = []
        self.make_widgets()
        os.chdir('/home/anirudhkailaje/Documents/04_Misc/05_SideProjects/Automated-Planogram-Creation/src/')
        self.load_products('../assets/products.csv')

    def make_widgets(self):
        self.default_font = ("Helvetica", 14)

        # Machine dimensions input
        tk.Label(self, text="Machine Width:", font=self.default_font).grid(row=0, column=0)
        self.machine_width_entry = tk.Entry(self, font=self.default_font)
        self.machine_width_entry.grid(row=0, column=1)

        tk.Label(self, text="Total Height:", font=self.default_font).grid(row=1, column=0)
        self.total_height_entry = tk.Entry(self, font=self.default_font)
        self.total_height_entry.grid(row=1, column=1)

        # Search bar and button
        self.search_entry = tk.Entry(self, width=20, font=self.default_font)
        self.search_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search)

        # Product listbox
        self.product_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, font=self.default_font, activestyle="none")
        self.product_listbox.grid(row=4, column=0, columnspan=3, sticky="new")
        self.product_listbox.bind("<Return>", self.add_to_table)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Selected products table
        self.selected_product_table = ttk.Treeview(self, columns=("Name", "Width", "Height"), show="headings")
        self.selected_product_table.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky='new')
        self.selected_product_table.heading("Name", text="Product Name")
        self.selected_product_table.heading("Width", text="Width")
        self.selected_product_table.heading("Height", text="Height")

        # Generate and save buttons
        tk.Button(self, text="Generate Planogram", command=self.generate_planogram, font=self.default_font).grid(row=6, column=0)
        tk.Button(self, text="Save Configuration", command=self.save_configuration, font=self.default_font).grid(row=6, column=1)

    def load_products(self, path):
        df = pd.read_csv(path)
        self.products = [Product(row['Name'], ceil(row['Width']), ceil(row['Height'])) for index, row in df.iterrows()]
        self.update_product_listbox()

    def update_product_listbox(self):
        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            self.product_listbox.insert(tk.END, product.id)

    def add_to_table(self, event):
        selected_indices = self.product_listbox.curselection()
        for index in selected_indices:
            product = self.products[index]
            if product not in self.selected_products:  # Avoid duplicate entries
                self.selected_products.append(product)
                self.selected_product_table.insert("", "end", values=(product.id, product.width, product.height))

    def search(self, event=None):
        search_term = self.search_entry.get().lower()
        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            if search_term in product.id.lower():
                self.product_listbox.insert(tk.END, product.id)

    def generate_planogram(self):
        bin_max_width = int(self.machine_width_entry.get())
        total_machine_height = int(self.total_height_entry.get())
        self.bins, added_products = fit_products_into_bins(self.products, bin_max_width, total_machine_height)
        tk.messagebox.showinfo("Planogram Generated", f"{added_products} products were fitted into bins.")

    def save_configuration(self):
        tk.messagebox.showinfo("Save Configuration", "Configuration saved successfully.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
