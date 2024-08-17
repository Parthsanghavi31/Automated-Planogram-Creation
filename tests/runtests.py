import numpy as np, shutil
import pandas as pd, os, pickle

shutil.copy('../Planogram_Packing_algo_v3.py', './Planogram_Packing_algo_v3.py')

from Planogram_Packing_algo_v3 import *

if not os.path.exists('./test_results/'):
    os.mkdir('./test_results/')

testobj_dir = './testobjs/'
image_paths = [file for file in os.listdir('../assets/product_images')]

for test in os.listdir(testobj_dir):
    with open(os.path.join(testobj_dir, test), 'rb') as f:
        dims, products = pickle.load(f)
        
    bin_max_width, total_machine_height = dims
    max_height = 20

    added_products = 1

    while added_products != 0:
        bins, added_products = fit_products_into_bins(products, bin_max_width, max_height, total_machine_height)

    simulate_vending_machine(bins, bin_max_width, total_machine_height, path='./test_results/', filename=test.replace('tst', 'jpg'))
    

        
