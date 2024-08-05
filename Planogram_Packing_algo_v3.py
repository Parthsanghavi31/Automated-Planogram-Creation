import pandas as pd

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
            return True
        return False

    def __repr__(self):
        return f"Bin(width={self.current_width}/{self.max_width}, height={self.current_height}/{self.max_height}, products={self.products})"

def fit_products_into_bins(products, bin_max_width, max_height, total_machine_height):
    bins = []
    total_height_used = 0
    skipped_products = []

    # Sort products by a heuristic that considers both dimensions
    products.sort(key=lambda x: (x.height * x.width / x.height), reverse=True)

    for product in products:
        placed = False
        for bin in bins:
            if bin.can_add_product(product) and total_height_used + bin.current_height <= total_machine_height:
                if bin.add_product(product):
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

    for product in sorted(skipped_products, key=lambda x: (x.height, x.width)):
        placed = False
        for bin in bins:
            if bin.add_product(product):
                placed = True
                break
        if not placed:
            print(f"Product {product.id} ultimately could not be placed.")

    return bins

def simulate_vending_machine(bins):
    grid_rows = len(bins)
    grid = [['Empty' for _ in range(1)] for _ in range(grid_rows)]
    for i, bin in enumerate(bins):
        if bin.products:
            product_names = ', '.join([f"P{p.id}" for p in bin.products])
            grid[i][0] = product_names
    grid_df = pd.DataFrame(grid, columns=["Bin Contents"], 
                           index=[f"Row {i+1}" for i in range(grid_rows)])
    return grid_df

def main():
    products = [
        Product(1, 6, 3), Product(2, 6, 4), Product(3, 6, 5), Product(4, 6, 4),
        Product(5, 10, 7), Product(6, 6, 5), Product(7, 6, 4), Product(8, 6, 8),
        Product(9, 7, 6), Product(10, 1, 1), Product(11, 1, 1), Product(12, 2, 1),
        Product(13, 1, 1), Product(14, 1, 1), Product(15, 1, 1), Product(16, 1, 1),
        Product(17, 3, 4)
    ]
    bin_max_width = 10
    max_height = 20
    total_machine_height = 30

    bins = fit_products_into_bins(products, bin_max_width, max_height, total_machine_height)
    
    for product in products:
        print(product)
        
    print("\nFitted into bins:")
    for bin in bins:
        print(bin)
    
    grid_df = simulate_vending_machine(bins)
    print("\nPlanogram Layout")
    print(grid_df)

if __name__ == "__main__":
    main()



# P6, P8 