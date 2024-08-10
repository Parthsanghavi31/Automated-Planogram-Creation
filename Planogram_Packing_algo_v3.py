import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
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
        self.products = []

    def can_add_product(self, product):
        return (self.current_width + product.width <= self.max_width and
                self.current_height + product.height <= self.max_height)

    def add_product(self, product):
        if self.can_add_product(product):
            self.products.append(product)
            self.current_width += product.width
            self.current_height = max(self.current_height, product.height)
            print(f"Added Product {product.id} to bin: Current bin dimensions are width={self.current_width}/{self.max_width}, height={self.current_height}/{self.max_height}")
            return True
        print(f"Failed to add Product {product.id}: Exceeds bin dimensions with width={product.width}, height={product.height} when added to current width={self.current_width}, height={self.current_height}")
        return False

    def __repr__(self):
        return f"Bin(width={self.current_width}/{self.max_width}, height={self.current_height}/{self.max_height}, products={self.products})"

def fit_products_into_bins(products, bin_max_width, max_height, total_machine_height, bins = []):
    total_height_used = 0
    skipped_products = []

    # sorting by considering both the dimesnisons
    products.sort(key=lambda x: (x.height * x.width / x.height), reverse=True)
    print(products)

    for product in products:
        placed = False #Is product placed? Place in existing bins, else create new bin?
        for bin in bins:
            if bin.can_add_product(product) and total_height_used + bin.current_height <= total_machine_height:
                if bin.add_product(product):
                    print(product)
                    placed = True
                    break

        if not placed:
            if total_height_used + product.height <= total_machine_height:
                new_bin = Bin(bin_max_width, max_height)
                if new_bin.add_product(product):
                    bins.append(new_bin)
                    total_height_used += new_bin.current_height
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
                    break
            if not placed:
                print(f"Product {product.id} ultimately could not be placed.")

    return bins

def simulate_vending_machine(bins, bin_max_width, total_machine_height):
    # Setup plot
    fig, ax = plt.subplots()

    y_offset = 0  # Start y_offset from 0 (bottom of the plot)

    # Draw the overall vending machine border in the darkest shade of gray
    machine_border = plt.Rectangle((0, 0), bin_max_width, total_machine_height, 
                                   edgecolor='black', facecolor='none', linewidth=3)
    ax.add_patch(machine_border)

    for bin_idx, bin in enumerate(bins):
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
            plt.text(x_offset + product.width / 2, y_offset + product.height / 2, f"P{product.id}", 
                     ha='center', va='center', fontsize=8)

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

    plt.show()


def main():
    # products = [
    #     Product(1, 6, 10), Product(2, 4, 4), Product(3, 3, 5), Product(4, 6, 4),
    #     Product(5, 1, 7), Product(6, 6, 5), Product(7, 6, 4), Product(8, 6, 8),
    #     Product(9, 7, 6), Product(10, 1, 1), Product(11, 1, 1), Product(12, 2, 1),
    #     Product(13, 1, 1), Product(14, 1, 1), Product(15, 1, 1), Product(16, 1, 1),
    #     Product(17, 3, 4)
    # ]
    products = []
    bin_max_width = 10
    max_height = 20
    total_machine_height = 25
    scaling_factor = 3.5

    product_df = pd.read_csv('./products.csv')
    for i in range(len(product_df)):
        products.append(Product(product_df.iloc[i].SKU, ceil(product_df.iloc[i].Width/scaling_factor), ceil(product_df.iloc[i].Height/scaling_factor)))

    bins = fit_products_into_bins(products, bin_max_width, max_height, total_machine_height)
    bins = fit_products_into_bins(products, bin_max_width, max_height, total_machine_height, bins)
    
    for product in products:
        print(product)
        
    print("\nFitted into bins:")
    for bin in bins:
        print(bin)
    
    grid_df = simulate_vending_machine(bins, bin_max_width, total_machine_height)
    print("\nPlanogram Layout")
    print(grid_df)

if __name__ == "__main__":
    main()



# P6, P8  not included