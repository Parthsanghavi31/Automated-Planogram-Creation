import casadi as csd
import numpy as np, math
from machine import *
from typing import List, Dict, Union, Optional



def space_objective(machine:VendingMachine, candidate_products: List[Product], 
                    m:csd.SX , n: csd.SX, s: csd.SX)-> csd.SX:
    L,B,H = machine.grid_dims

    for i in range(m):
        for j in range(n):
            k =  #how to get the depth of the customer???????
            objective -= h[i]*(x[j] != 0)*int(math.floor(H/candidate_products[]))

    return objective


