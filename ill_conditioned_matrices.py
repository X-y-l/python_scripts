import numpy as np

# Generates an nxn Hilbert matrix.
def hilbert_matrix(n):
    return np.array([[1/(i+j-1) for i in range(1, n+1)] for j in range(1, n+1)])

# Solves the linear system Ax = b using numpy's linalg.solve.
def solve_system(A, b):
    return np.linalg.solve(A, b)

# Adds a small amount of noise to the matrix A.
def add_noise(A, epsilon):
    return A + epsilon * np.random.rand(*A.shape)

# Runs the experiment for a n x n Hilbert matrix and noise level epsilon.
def experiment(n, epsilon):
    H = hilbert_matrix(n)
    cond = np.linalg.cond(H)
    print(f"Hilbert matrix of shape {H.shape} with condition number {cond:.3f}")
    b = np.ones(n)
    x_exact = solve_system(H, b)
    H_noisy = add_noise(H, epsilon)
    x_noisy = solve_system(H_noisy, b)
    error = np.abs(x_exact - x_noisy).max()
    print(f"Maximum error: {error:.3e}")


experiment(10, 1e-8)