import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd, os
from math import ceil
import matplotlib.pyplot as plt
import tkinter.filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Planogram_Packing_algo_v3 import Product, Bin, fit_products_into_bins, simulate_vending_machine

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine Manager")
        self.geometry("1024x768")
        self.style = ttk.Style()
        self.configure_styles()
        self.products = []
        self.bins = []
        self.selected_products = []
        self.configure_gui()
        self.make_widgets()
        os.chdir('/home/anirudhkailaje/Documents/04_Misc/05_SideProjects/Automated-Planogram-Creation/src/')
        self.load_products()

    def configure_styles(self):
        # Theme and styles for ttk
        self.style.theme_use('clam')  # You can choose from 'alt', 'default', 'clam', 'classic', etc.
        self.style.configure('TButton', font=('Helvetica', 12), background='#ECECEC', borderwidth=1)
        self.style.configure('TLabel', font=('Helvetica', 12), background='#f0f0f0')
        self.style.configure('TEntry', font=('Helvetica', 12), relief=tk.FLAT)
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.map('TButton', background=[('active', '#E8E8E8')])

    def configure_gui(self):
        # Configure the resizing properties
        self.minsize(800, 600)  # Minimum size of the window

    def make_widgets(self):
        self.default_font = ("Helvetica", 14)

        # Main PanedWindow
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6, background='#f0f0f0')
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left side configuration
        self.left_frame = ttk.Frame(self.main_pane, style='TFrame')
        self.main_pane.add(self.left_frame, width=200)

        # Title Ribbon
        title_label = ttk.Label(self.left_frame, text="Vending Machine Planogram Manager", font=("Helvetica", 16, "bold"), background="gray", anchor="center")
        title_label.pack(fill=tk.X, padx=10, pady=5)

        # Machine dimensions input
        ttk.Label(self.left_frame, text="Machine Width:", font=self.default_font).pack(fill=tk.X)
        self.machine_width_entry = ttk.Entry(self.left_frame, font=self.default_font)
        self.machine_width_entry.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(self.left_frame, text="Total Height:", font=self.default_font).pack(fill=tk.X)
        self.total_height_entry = ttk.Entry(self.left_frame, font=self.default_font)
        self.total_height_entry.pack(fill=tk.X, padx=20, pady=5)

        # Search bar and label
        ttk.Label(self.left_frame, text="Search Products:", font=self.default_font).pack(fill=tk.X)
        self.search_entry = ttk.Entry(self.left_frame, font=self.default_font)
        self.search_entry.pack(fill=tk.X, padx=20, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search)

        # Product listbox
        self.product_listbox = tk.Listbox(self.left_frame, selectmode='extended', font=self.default_font, activestyle="none", relief=tk.FLAT)
        self.product_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.product_listbox.bind("<Return>", self.add_to_table)

        # Selected products table
        self.selected_product_table = ttk.Treeview(self.left_frame, columns=("Name", "Width", "Height"), show="headings")
        self.selected_product_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.selected_product_table.heading("Name", text="Product Name")
        self.selected_product_table.heading("Width", text="Width")
        self.selected_product_table.heading("Height", text="Height")

        # Right side configuration
        self.right_frame = ttk.Frame(self.main_pane, style='TFrame')
        self.main_pane.add(self.right_frame, width=400)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self.right_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Generate and save buttons
        ttk.Button(self.left_frame, text="Generate Planogram", command=self.generate_planogram).pack(fill=tk.X, padx=20, pady=5)
        ttk.Button(self.left_frame, text="Save Configuration", command=self.save_configuration).pack(fill=tk.X, padx=20, pady=5)

    def load_products(self, path=None):
        if not path:  # If no path is provided, ask the user to select a file
            path = fd.askopenfilename(
                title="Select Product CSV",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                initialdir=os.getcwd()  # Opens file dialog in the current working directory
            )
            if not path:  # If no file is selected, return
                return
        
        df = pd.read_excel(path)
        df.columns = ['Item Number','1st Description','2nd Description','Depth','Width','Height','Weight']
        df['Name'] = df['1st Description'] + ' ' + df['2nd Description']
        df.drop(['1st Description','2nd Description'], axis=1, inplace=True)
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
            if product not in self.selected_products:
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
        added_products = 1
        while added_products != 0:
            self.bins, added_products = fit_products_into_bins(self.selected_products, bin_max_width, total_machine_height, self.bins)

        self.ax.clear()
        simulate_vending_machine(self.bins, bin_max_width, total_machine_height, self.fig, self.ax)
        self.canvas.draw()
        all_prod =[]
        for bin in self.bins:
            for prod in bin.products:
                all_prod.append(prod)
        # messagebox.showinfo("Planogram Generated", f"{added_products} out of {len(self.selected_products)} products were fitted into bins.")

    def save_configuration(self):
        messagebox.showinfo("Save Configuration", "Configuration saved successfully.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
