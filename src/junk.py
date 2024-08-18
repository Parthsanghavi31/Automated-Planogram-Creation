import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Simple Table with Tkinter")

# Initialize lists to store column values
column1_values = []
column2_values = []

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Column1", "Column2"), show="headings")
tree.heading("Column1", text="Column 1")
tree.heading("Column2", text="Column 2")

# Add the Treeview widget to the window
tree.pack()

# Function to add a new row
def add_value():
    # Get values from entry fields
    value1 = entry1.get()
    value2 = entry2.get()
    
    # Insert values into the Treeview
    tree.insert("", "end", values=(value1, value2))
    
    # Append values to the lists
    column1_values.append(value1)
    column2_values.append(value2)
    
    # Clear entry fields
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)

# Function to update a selected row
def update_value():
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]  # Get the first selected item
        value1 = entry1.get()
        value2 = entry2.get()
        
        # Update the selected item in the Treeview
        tree.item(selected_item, values=(value1, value2))
        
        # Update the lists
        index = tree.index(selected_item)
        column1_values[index] = value1
        column2_values[index] = value2
        
        # Clear entry fields
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)

# Function to fill entry fields with selected row's data
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]  # Get the first selected item
        values = tree.item(selected_item, "values")
        
        # Fill entry fields with the selected row's data
        entry1.delete(0, tk.END)
        entry1.insert(0, values[0])
        entry2.delete(0, tk.END)
        entry2.insert(0, values[1])

# Function to delete a selected row
def delete_value():
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]  # Get the first selected item
        index = tree.index(selected_item)
        
        # Remove the item from the Treeview
        tree.delete(selected_item)
        
        # Remove the item from the lists
        del column1_values[index]
        del column2_values[index]

# Create a context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Delete", command=delete_value)

# Function to show the context menu
def show_context_menu(event):
    # Select the row under the cursor
    item = tree.identify_row(event.y)
    if item:
        tree.selection_set(item)
        context_menu.post(event.x_root, event.y_root)

# Entry fields for input
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry1.pack()
entry2.pack()

# Buttons to add and update values
add_button = tk.Button(root, text="Add", command=add_value)
update_button = tk.Button(root, text="Update", command=update_value)
add_button.pack()
update_button.pack()

# Bind the tree selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Bind right-click to show the context menu
tree.bind("<Button-3>", show_context_menu)

# Run the application
root.mainloop()