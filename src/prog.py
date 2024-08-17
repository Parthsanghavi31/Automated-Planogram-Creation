import casadi as ca

# Define item sizes
item_sizes = [2, 5, 4, 7, 1, 3, 8]  # Example sizes
num_items = len(item_sizes)

# Define bin capacity
bin_capacity = 10  # Example bin capacity

# Define the maximum number of bins
max_bins = num_items  # Worst case, one item per bin

# Decision variables
x = ca.SX.sym('x', num_items, max_bins)  # x[i,j] is 1 if item i is in bin j
y = ca.SX.sym('y', max_bins)  # y[j] is 1 if bin j is used

# Objective function: minimize the number of bins used
objective = ca.sum1(y)

# Constraints list
constraints = []

# Each item must be placed in exactly one bin
for i in range(num_items):
    constraints.append(ca.sum1(x[i, :]) == 1)

# The total size of items in each bin must not exceed bin capacity
for j in range(max_bins):
    constraints.append(ca.dot(item_sizes, x[:, j]) <= bin_capacity * y[j])

# Convert constraints to a single vector
constraints = ca.vertcat(*constraints)

# Define the optimization problem
nlp = {'x': ca.vertcat(ca.reshape(x, -1, 1), y), 'f': objective, 'g': constraints}

# Create the solver
solver = ca.nlpsol('solver', 'ipopt', nlp)

# Initial guess
x0 = [0] * (num_items * max_bins) + [0] * max_bins

# Lower and upper bounds for variables
lbx = [0] * (num_items * max_bins) + [0] * max_bins
ubx = [1] * (num_items * max_bins) + [1] * max_bins

# Lower and upper bounds for constraints
num_constraints = len(constraints)
lbg = [0] * num_constraints
ubg = [1] * num_items + [ca.inf] * max_bins

# Solve the problem
solution = solver(x0=x0, lbx=lbx, ubx=ubx, lbg=lbg, ubg=ubg)

# Extract the solution
sol = solution['x'].full().flatten()

# Reshape the solution to interpret results
x_sol = sol[:num_items * max_bins].reshape((num_items, max_bins))
y_sol = sol[num_items * max_bins:]

# Print the results
print("Bin usage (y):", y_sol)
print("Item assignments (x):")
for i in range(num_items):
    for j in range(max_bins):
        if x_sol[i, j] > 0.5:
            print(f"Item {i} is placed in Bin {j}")

# Print the bins and their contents
bins = {i: [] for i in range(max_bins) if y_sol[i] > 0.5}
for i in range(num_items):
    for j in range(max_bins):
        if x_sol[i, j] > 0.5:
            bins[j].append(item_sizes[i])

print("Bins and their contents:")
for bin_index, contents in bins.items():
    print(f"Bin {bin_index}: {contents}")
