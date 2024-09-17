import numpy as np, shutil, tqdm
import pandas as pd, os, pickle, math

os.chdir('/home/anirudhkailaje/Documents/04_Misc/05_SideProjects/Automated-Planogram-Creation/tests/')
shutil.copy('../src/Planogram_Packing_algo_v3.py', './Planogram_Packing_algo_v3.py')

from Planogram_Packing_algo_v3 import *

if not os.path.exists('./test_results/'):
    os.mkdir('./test_results/')

for file in os.listdir('./test_results/'):
    os.remove(os.path.join('./test_results/', file))

testobj_dir = './testobjs/'
image_paths = [file for file in os.listdir('../assets/product_images')]
tests = os.listdir(testobj_dir)
tests.sort(key=lambda x: int(x.split('_')[-1].split('.tst')[0]))
for i in tqdm.tqdm(range(len(tests))):
    test = tests[i]

    test_num = int(test.split('_')[-1].split('.tst')[0])
    with open(os.path.join(testobj_dir, test), 'rb') as f:
        dims, products = pickle.load(f)
    # print(dims)
    bin_max_width, total_machine_height = dims
    max_height = min(20, total_machine_height)
    bins = []
    added_products = 1
    run = 0
    while added_products != 0:
        bins, added_products = fit_products_into_bins(products, bin_max_width, total_machine_height, bins)
        run += 1
    simulate_vending_machine(bins, bin_max_width, total_machine_height, path='./test_results/', filename=f'TestNum{test_num}_{run}.jpg')
    used_height = 0
    for bin in bins:
        used_height += bin.current_height

    assert(used_height <= total_machine_height)