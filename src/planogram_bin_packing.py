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

