import pandas as pd

class Product:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
    
    def __repr__(self) -> str:
        return f"Product id is {self.id}, and it's dimension is {self.height} and {self.width}"
    
class Bin:
    def __init__(self, max_width):
        self.max_width = max_width
        self.current_width = 0
        self.max_height = 0
        self.products = []
        
    def add_products(self, product):
        
        if self.current_width + product.width <= self.max_width:
            self.products.append(product)
            self.current_width += product.width
            self.max_height = max(self.max_height, product.height)
            
            print(f"Product {product.id} added to bin with current width {self.current_width}/{self.max_width}")
            return True
        print(f"Could not add {product.id} to the bin. Bin is Full or remaining space of {self.max_width - self.current_width} < new product's width of {product.width}")
        return False
    
    def __repr__(self):
        return f"Bin(Current Width: {self.current_width}/{self.max_width}, Products: {self.products})"
    
def fit_products_into_bins(products, bin_max_width, max_bins):
    bins = [Bin(bin_max_width) for _ in range(max_bins)]
    skipped_products = [] 
   
    for product in sorted(products, key=lambda x: x.width, reverse=True):
        placed = False
        for bin in bins:
            if bin.add_products(product):
                placed = True
                break
        
        if not placed:
            skipped_products.append(product)
    # print("\n Total number of Skipped products ", len(skipped_products))

    for product in sorted(skipped_products, key=lambda x: x.width):  # Smaller products first
        placed = False
        for bin in bins:
            if bin.add_products(product):
                placed = True
                break
        if not placed:
            print(f"Could not finally place Product {product.id}. All bins are full.")

    return bins


def simulate_vending_machine(bins):
    # Set up one bin per row, so number of rows equals the number of bins
    grid_rows = len(bins)
    grid_columns = 1  # One column since only one bin per row

    # Initialize the grid with empty cells
    grid = [['Empty'] for _ in range(grid_rows)]  # Create a list of lists with single 'Empty' entries

    # Fill the grid with product names from the bins
    for i, bin in enumerate(bins):
        if bin.products:
            product_names = ', '.join([f"P{p.id}" for p in bin.products])
            grid[i][0] = product_names  # Each bin in its own row

    # Create DataFrame to display the grid
    grid_df = pd.DataFrame(grid, columns=["Bin Contents"], 
                                index=[f"Row {i+1} (Bin {i+1} Width {bins[i].max_width})" for i in range(grid_rows)])
    return grid_df   
            
def main():
    products = [
        Product(1, 6, 10), Product(2, 4, 4), Product(3, 3, 5), Product(4, 6, 4),
        Product(5, 1, 7), Product(6, 6, 5), Product(7, 6, 4), Product(8, 6, 8),
        Product(9, 7, 6), Product(10, 1, 1), Product(11, 1, 1), Product(12, 2, 1),
        Product(13, 1, 1), Product(14, 1, 1), Product(15, 1, 1), Product(16, 1, 1),
        Product(17, 3, 4)
    ]
    
    bin_max_width = 10
    max_bins = 4
    
    bins = fit_products_into_bins(products, bin_max_width, max_bins)
    
    for product in products:
        print(product)
        
    print("\nFitted into bins:")
    print(len(bins))
    
    for bin in bins:
        print(bin) 
    
    grid_df = simulate_vending_machine(bins)
    print("\n Planogram Layout")
    print(grid_df)
    
if __name__ == "__main__":
    main()
    
    
            
        
        
        
        