import pandas as pd, os
import matplotlib.pyplot as plt
from math import ceil
import cv2, numpy as np


class Product:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Product(id={self.id}, width={self.width}, height={self.height})"

class Bin:
    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height
        self.current_width = 0
        self.current_height = 0
        self.total_area = 0
        self.products = []

    def can_add_product(self, product):
        return (self.current_width + product.width <= self.max_width and
                product.height <= self.max_height)

    def add_product(self, product):
        if self.can_add_product(product):
            self.products.append(product)
            self.current_width += product.width
            self.current_height = max(self.current_height, product.height)
            # print(f"Added Product {product.id} to bin: Current bin dimensions are width={self.current_width}/{self.max_width}, height={self.current_height}/{self.max_height}")
            return True
        # print(f"Failed to add Product {product.id}: Exceeds bin dimensions with width={product.width}, height={product.height} when added to current width={self.current_width}, height={self.current_height}")
        return False
    
    def rearrange_bin(self):
        self.products.sort(key=lambda x: (x.height), reverse=False)
        n = len(self.products)
        midpoint = (n//2)+(n%2)
        indeces = np.arange(n)
        rearranged_indeces = np.zeros(n)
        rearranged_indeces[0:midpoint] = indeces[-1::-2]
        rearranged_indeces[midpoint:] = indeces[0:-1:2]
        prod_copy = np.array(self.products)[rearranged_indeces.astype(int)]
        self.products = prod_copy.tolist()
        del prod_copy

    def __repr__(self):
        return f"Bin(width={self.current_width}/{self.max_width}, height={self.current_height}/{self.max_height}, products={self.products})"

def fit_products_into_bins(products, bin_max_width, total_machine_height, bins = []):
    total_height_used = 0; added_products = 0

    if len(bins) != 0:
        for bin in bins:
            total_height_used += bin.current_height

    skipped_products = []

    # sorting by considering both the dimesnisons
    products.sort(key=lambda x: (x.width), reverse=True)
    # print(products)

    for product in products:
        placed = False #Is product placed? Place in existing bins, else create new bin?
        for bin in bins:
            if (total_height_used+product.height<=total_machine_height):
                if bin.add_product(product):
                    # print(product)
                    added_products += 1
                    placed = True
                    total_height_used = 0
                    for bin in bins:
                        total_height_used += bin.current_height
                    break

        if not placed:
            if total_height_used + product.height <= total_machine_height:
                new_bin = Bin(bin_max_width, total_machine_height-total_height_used)
                if (total_height_used+product.height<=total_machine_height):
                    if new_bin.add_product(product):
                        bins.append(new_bin)
                        total_height_used += new_bin.current_height
                        added_products +=1
                else:
                    skipped_products.append(product)
            else:
                skipped_products.append(product)

    new_placements = False; first_run = True
    while new_placements or first_run:
        first_run = False
        new_placements = False
        for product in sorted(skipped_products, key=lambda x: (x.height, x.width)):
            placed = False
            for bin in bins:
                if bin.add_product(product):
                        placed = True
                        new_placements = True
                        added_products += 1
                        total_height_used = 0
                        for bin in bins:
                            total_height_used += bin.current_height
                        break
            # if not placed:
                # print(f"Product {product.id} ultimately could not be placed.")
    # simulate_vending_machine(bins, bin_max_width, total_machine_height)

    for bin in bins:
        bin.total_area = np.array([pr.width*pr.height for pr in bin.products]).sum()
    bins.sort(key = lambda x: x.total_area, reverse = True)
    return bins, added_products

def simulate_vending_machine(bins, bin_max_width, total_machine_height, fig=None, ax=None, path='./', filename='planogram.jpg'):
    internal_init = False
    if fig is None or ax is None:
        fig, ax = plt.subplots()
        internal_init = True

    y_offset = 0  # Start y_offset from 0 (bottom of the plot)
    # Draw the overall vending machine border in the darkest shade of gray
    machine_border = plt.Rectangle((0, 0), bin_max_width, total_machine_height, 
                                   edgecolor='black', facecolor='none', linewidth=3)
    ax.add_patch(machine_border)

    for bin_idx, bin in enumerate(bins):
        bin.rearrange_bin()
        x_offset = 0  # Reset x_offset for each new bin

        # Draw a dark gray border around each bin
        bin_border = plt.Rectangle((x_offset, y_offset), bin.max_width, bin.current_height, 
                                   edgecolor='darkgray', facecolor='none', linewidth=2)
        ax.add_patch(bin_border)

        for product in bin.products:
            # Draw each product as a rectangle
            rect = plt.Rectangle((x_offset, y_offset), product.width, product.height, 
                                 edgecolor='black', facecolor='lightblue')
            ax.add_patch(rect)

            # Add product ID text in the middle of the rectangle
            plt.text(x_offset + product.width / 2, y_offset + product.height / 2, f"{product.id}", 
                     ha='center', va='center', fontsize=8, rotation='vertical')

            # Move x_offset to the right by the width of the current product
            x_offset += product.width

        # Move y_offset upwards by the height of the bin (to stack bins vertically)
        y_offset += bin.current_height

    # Set the limits of the plot
    ax.set_xlim(0, bin_max_width)
    ax.set_ylim(0, total_machine_height)
    ax.set_aspect('equal')

    # Show x-ticks and y-ticks
    x_ticks = range(0, bin_max_width + 1)
    y_ticks = range(0, total_machine_height + 1)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # Display grid for better visualization
    plt.grid(True)
    plt.savefig(os.path.join(path, filename))
    if internal_init:
        plt.close()
    # del fig, ax
    # plt.show()

def main():
    products = []
    bin_max_width = 10
    
    total_machine_height = 25
    scaling_factor = 3.5
    path = './'
    product_df = pd.read_csv('../assets/products.csv')
    for i in range(len(product_df)):
        products.append(Product(product_df.iloc[i].Name, ceil(product_df.iloc[i].Width/scaling_factor), ceil(product_df.iloc[i].Height/scaling_factor)))

    added_products = 1

    while added_products != 0:
        bins, added_products = fit_products_into_bins(products, bin_max_width, total_machine_height)
    
    # for product in products:
        # print(product)
        
    # print("\nFitted into bins:")
    # for bin in bins:
        # print(bin)
    image_paths = [file for file in os.listdir('../assets/product_images')]
    # simulate_vending_machine(bins, bin_max_width, total_machine_height, path)
    # print("\nPlanogram Layout")

    # print(len(bins))
    # for bin in bins:
        # print(f"\n{bin}")

    used_height = 0
    for bin in bins:
        used_height += bin.current_height

    assert(used_height <= total_machine_height)
    
if __name__ == "__main__":
    main()



# P6, P8  not included