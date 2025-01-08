import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print

console = Console()

def classical_gram_schmidt(A):
    """Classical Gram-Schmidt orthogonalization."""
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for k in range(n):
        Q[:, k] = A[:, k]
        for j in range(k):
            R[j, k] = np.dot(Q[:, j], A[:, k])
            Q[:, k] -= R[j, k] * Q[:, j]
        R[k, k] = np.linalg.norm(Q[:, k])
        Q[:, k] /= R[k, k]
    return Q, R

def modified_gram_schmidt(A):
    """Modified Gram-Schmidt orthogonalization."""
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for k in range(n):
        R[k, k] = np.linalg.norm(A[:, k])
        Q[:, k] = A[:, k] / R[k, k]
        for j in range(k + 1, n):
            R[k, j] = np.dot(Q[:, k], A[:, j])
            A[:, j] -= R[k, j] * Q[:, k]
    return Q, R

def householder_qr(A):
    """QR decomposition using Householder reflections."""
    m, n = A.shape
    Q = np.eye(m)
    R = A.copy()

    for k in range(n):
        # Extract the vector to reflect
        x = R[k:, k]
        e1 = np.zeros_like(x)
        e1[0] = 1.0

        # Compute the Householder vector
        alpha = -np.sign(x[0]) * np.linalg.norm(x)
        u = x - alpha * e1
        v = u / np.linalg.norm(u)

        # Apply the Householder transformation to R
        R[k:, :] -= 2.0 * np.outer(v, np.dot(v, R[k:, :]))
        
        # Apply the Householder transformation to Q
        Q[:, k:] -= 2.0 * np.outer(Q[:, k:] @ v, v)

    return Q, R

def generate_hilbert_matrix(size):
    """
    Generate a Hilbert matrix of given size.
    
    Parameters:
    - size: The size of the Hilbert matrix (square matrix of shape (size, size)).
    
    Returns:
    - H: Hilbert matrix of shape (size, size).
    """
    H = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            H[i, j] = 1 / (i + j + 1)
    return H

def test_hilbert_matrix_precision(size):
    """
    Compare precision of classical, modified Gram-Schmidt, and Householder QR on a Hilbert matrix.
    
    Parameters:
    - size: Size of the Hilbert matrix.
    
    Returns:
    - results: Dictionary containing orthogonality errors for each method and improvement ratios.
    """
    A = generate_hilbert_matrix(size)
    
    with console.status("[bold green]Performing QR decompositions..."):
        # Classical Gram-Schmidt
        Q_classical, _ = classical_gram_schmidt(A.copy())
        orth_error_classical = np.linalg.norm(np.dot(Q_classical.T, Q_classical) - np.eye(size))
        
        # Modified Gram-Schmidt
        Q_modified, _ = modified_gram_schmidt(A.copy())
        orth_error_modified = np.linalg.norm(np.dot(Q_modified.T, Q_modified) - np.eye(size))
        
        # Householder QR
        Q_householder, _ = householder_qr(A.copy())
        orth_error_householder = np.linalg.norm(np.dot(Q_householder.T, Q_householder) - np.eye(size))
        
        # Calculate improvement ratios
        improvement_ratio_classical_modified = orth_error_classical / orth_error_modified
        improvement_ratio_classical_householder = orth_error_classical / orth_error_householder
        improvement_ratio_modified_householder = orth_error_modified / orth_error_householder
    
    results = {
        'Classical': orth_error_classical,
        'Modified': orth_error_modified,
        'Householder': orth_error_householder,
        'Classical_vs_Modified': improvement_ratio_classical_modified,
        'Classical_vs_Householder': improvement_ratio_classical_householder,
        'Modified_vs_Householder': improvement_ratio_modified_householder
    }
    
    return results

# Test with a Hilbert matrix of size 5x5
size = 10
hilbert_results = test_hilbert_matrix_precision(size)

# Create a table to display results
table = Table(title=f"QR Decomposition: Hilbert Matrix {size}x{size}")
table.add_column("Method", style="cyan", justify="left")
table.add_column("Orthogonality Error", style="magenta", justify="right")

# Add rows for each method
table.add_row("Classical Gram-Schmidt", f"{hilbert_results['Classical']:.6e}")
table.add_row("Modified Gram-Schmidt", f"{hilbert_results['Modified']:.6e}")
table.add_row("Householder QR", f"{hilbert_results['Householder']:.6e}")

console.print(table)
