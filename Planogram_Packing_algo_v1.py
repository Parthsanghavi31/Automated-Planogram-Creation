import pandas as pd

class Product:
    def __init__(self, id, height, width):
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
    
def fit_products_into_bins(products, bin_max_width):
    bins = []

    # No need to sort products by height unless it aligns with specific packing requirements
    for product in products:  # Consider products in their natural order or sort them based on your preference
        best_bin = None
        min_space_left = float('inf')

        # Find the best bin that leaves the least space after adding this product
        for bin in bins:
            if bin.current_width + product.width <= bin.max_width:
                space_left = bin.max_width - (bin.current_width + product.width)
                if space_left < min_space_left:
                    min_space_left = space_left
                    best_bin = bin

        # Add the product to the best bin found, or create a new bin if no suitable bin exists
        if best_bin is not None:
            best_bin.add_products(product)
        else:
            new_bin = Bin(bin_max_width)
            new_bin.add_products(product)
            bins.append(new_bin)

    return bins
   
   

def simulate_vending_machine(products, bins):
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
        Product(1, 2, 3),
        Product(2, 3, 4),
        Product(3, 4, 5),
        Product(4, 3, 4),
        Product(5, 6, 7),
        Product(6, 4, 5),
        Product(7, 4, 4),
        Product(8, 6, 8),
        Product(9, 3, 6),
        Product(10, 3, 5),
               
    ]
    
    bin_max_width = 10
    
    bins = fit_products_into_bins(products, bin_max_width)
    
    for product in products:
        print(product)
        
    print("\nFitted into bins:")
    print(len(bins))
    
    for bin in bins:
        print(bin) 
    
    grid_df = simulate_vending_machine(products, bins)
    print("\n Planogram Layout")
    print(grid_df)
    
if __name__ == "__main__":
    main()