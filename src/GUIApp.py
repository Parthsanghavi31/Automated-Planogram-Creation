import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, TkinterDnD
import pandas as pd
from Planogram_Packing_algo_v3 import *

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Planogram")
        self.geometry("800x600")
        self.configure(bg="white")
        # self.dnd = TkinterDnD(self)
        self.product_list = []

        # Setup GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Machine Dimensions
        self.dim_label = tk.Label(self, text="Machine dim.:", font=("Helvetica", 14))
        self.dim_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.width_entry = tk.Entry(self, width=5, font=("Helvetica", 14))
        self.width_entry.grid(row=0, column=1, padx=5, pady=10)
        self.width_entry.insert(0, "10")

        self.height_entry = tk.Entry(self, width=5, font=("Helvetica", 14))
        self.height_entry.grid(row=0, column=2, padx=5, pady=10)
        self.height_entry.insert(0, "25")

        # Planogram Display
        self.planogram_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        self.planogram_frame.grid(row=1, column=4, rowspan=8, padx=10, pady=10)

        self.planogram_canvas = tk.Canvas(self.planogram_frame, bg="white", width=400, height=400)
        self.planogram_canvas.pack()

        # Search Bar
        self.search_label = tk.Label(self, text="Search", font=("Helvetica", 14))
        self.search_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = tk.Entry(self, width=20, font=("Helvetica", 14))
        self.search_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_products)

        # Product List
        self.product_listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Helvetica", 14), activestyle="none")
        self.product_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        # self.dnd.bindtarget(self.product_listbox, self.on_product_drag, 'text/uri-list')

        # Load Products from CSV
        self.load_products()

        # Reserve and Swap Buttons
        self.reserve_button = tk.Button(self, text="Reserve", font=("Helvetica", 14))
        self.reserve_button.grid(row=3, column=0, columnspan=1, padx=5, pady=10, sticky="ew")

        self.swap_button = tk.Button(self, text="Swap", font=("Helvetica", 14))
        self.swap_button.grid(row=3, column=1, columnspan=1, padx=5, pady=10, sticky="ew")

        # Generate Planogram Button
        self.generate_button = tk.Button(self, text="Generate Planogram", font=("Helvetica", 14), command=self.generate_planogram)
        self.generate_button.grid(row=3, column=2, padx=5, pady=10, sticky="ew")

    def load_products(self):
        # Clear current list
        self.product_listbox.delete(0, tk.END)

        # Load products from CSV
        product_df = pd.read_csv('./assets/products.csv')
        for _, row in product_df.iterrows():
            product_name = row['Name']
            self.product_listbox.insert(tk.END, product_name)

    def filter_products(self, event=None):
        search_term = self.search_entry.get().lower()
        self.product_listbox.delete(0, tk.END)
        product_df = pd.read_csv('./assets/products.csv')
        for _, row in product_df.iterrows():
            product_name = row['Name']
            if search_term in product_name.lower():
                self.product_listbox.insert(tk.END, product_name)

    def on_product_drag(self, event):
        data = event.data
        # Here we would handle the drop action

    def generate_planogram(self):
        bin_max_width = int(self.width_entry.get())
        total_machine_height = int(self.height_entry.get())
        products = []  # Fetch products and create Product objects here

        # This is where the bin packing and simulation would happen
        bins = []
        added_products = 1
        run = 0
        test_num = 1

        while added_products != 0:
            bins, added_products = fit_products_into_bins(products, bin_max_width, total_machine_height, bins)
            run += 1

        simulate_vending_machine(bins, bin_max_width, total_machine_height, path='./test_results/', filename=f'TestNum{test_num}_{run}.jpg')

        # Update the canvas with the planogram image
        self.update_planogram_canvas()

    def update_planogram_canvas(self):
        # Load and display the generated planogram
        pass  # Implement the actual image loading and display here

if __name__ == "__main__":
    app = Application()
    app.mainloop()
