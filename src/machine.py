import numpy as np
import pandas as pd
import casadi as csd
import os, time, matplotlib.pyplot as plt, logging
from objective_functions import *

class Product:
    def __init__(self, sku_num, width, height):
        self.SKU = sku_num
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"SKU: {self.SKU}, Dims: {self.width:2f}x{self.height:.2f}"
    
class VendingMachine:
    def __init__(self, name, grid_dims, scaling_factor, objectiveranking, exclusion_zone = None):
        self.name = name
        assert len(grid_dims) == 3, f"Grid Dimensions must be 3 dimensional. You've entered {len(grid_dims)} dimensions."
        self.grid_dims = grid_dims
        assert len(scaling_factor) == 3, f"Scaling factors must be 3 dimensional. You've entered {len(scaling_factor)} scaling dimensions."
        self.scaling_factors = scaling_factor
        """TODO: Need to assert/error handle incorrect objective ranking"""
        self.objective_ranking = objectiveranking
        self.exclusion_zones = exclusion_zone

    def __repr__(self) -> str:
        return f"Name: {self.name}\nGrid Dimensions: {self.grid_dims}"

    def formulate_optim_problem(self):
        pass

    def solve_optim_problem(self):
        pass

