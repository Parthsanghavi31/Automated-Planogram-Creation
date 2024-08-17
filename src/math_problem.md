# Initial problem design. 

Want to minimize the space wastage. The volume is described as l,b,h in scaling units. as in lX, bX, HX, where X is some scaling factor. 

The objective is to minimize the following. 
$$L*B*H - \sum_{i = 1}^m \sum_{j=1}^n \left(\min(h_i)*\mathbb{1}(x_j)*(\lfloor H/z_j\rfloor \right)$$
Wher $\mathbb{1}$ is the indicator function.

## Decision Variables and known constraints.
 - $x_j \in \text{SKU if occupied, 0 otherwise}$
 - $0 \leq m \leq L$ where m is the number of rows in the planogram. 
 - $0 \leq n \leq B$ where n is the number of columns.
 - $h[m]$, $h^Th >0 $ where h is the height of the each row. 
 - $s[k]$, $s^Ts > 0$ where s is a boolean array of k candidate products that indicates if the product is chosen to be added in the planogram.
  

