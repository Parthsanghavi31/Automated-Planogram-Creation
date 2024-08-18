import numpy as np, shutil
import pandas as pd, os, pickle

shutil.copy('../Planogram_Packing_algo_v3.py', './Planogram_Packing_algo_v3.py')

from Planogram_Packing_algo_v3 import *

if not os.path.exists('./test_results/'):
    os.mkdir('./test_results/')

product_df = pd.read_csv('../assets/products.csv')
products = []
scaling_factor = 3.5

for i in range(len(product_df)):
    products.append(Product(product_df.iloc[i].Name, ceil(product_df.iloc[i].Width/scaling_factor), ceil(product_df.iloc[i].Height/scaling_factor)))

products = np.array(products)
num_products_total = len(products)
num_min_products = 2
num_trails_per_setting = 10
test_num = 0

for i in range(num_min_products, num_products_total):
    for _ in range(10):
        indeces = np.random.randint(0, num_products_total, i)
        assert(len(indeces) == i)
        bin_max_width = np.random.randint(10, 20)
        total_machine_height = np.random.randint(10, 35)
        with open(f'./testobjs/Test_{i}products_{test_num}.tst', 'wb') as f:
            pickle.dump(((bin_max_width, total_machine_height), products[indeces].tolist()), f)
        test_num += 1