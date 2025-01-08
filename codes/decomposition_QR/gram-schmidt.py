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
    Compare precision of classical and modified Gram-Schmidt on a Hilbert matrix.
    
    Parameters:
    - size: Size of the Hilbert matrix.
    
    Returns:
    - orth_error_classical: Orthogonality error for Classical Gram-Schmidt.
    - orth_error_modified: Orthogonality error for Modified Gram-Schmidt.
    - improvement_ratio: Ratio of classical error to modified error.
    """
    console.print(f"\n[bold blue]Testing Gram-Schmidt Methods on {size}x{size} Hilbert Matrix[/bold blue]")
    
    A = generate_hilbert_matrix(size)
    
    with console.status("[bold green]Performing Gram-Schmidt orthogonalizations..."):
        Q_classical, _ = classical_gram_schmidt(A.copy())
        Q_modified, _ = modified_gram_schmidt(A.copy())
    
        orth_error_classical = np.linalg.norm(np.dot(Q_classical.T, Q_classical) - np.eye(size))
        orth_error_modified = np.linalg.norm(np.dot(Q_modified.T, Q_modified) - np.eye(size))
        improvement_ratio = orth_error_classical / orth_error_modified
    
    return orth_error_classical, orth_error_modified, improvement_ratio

# Test with a Hilbert matrix of size 10x10
hilbert_results = test_hilbert_matrix_precision(10)

# Create a table to display results
table = Table(title="Gram-Schmidt Comparison Results")
table.add_column("Method", style="cyan")
table.add_column("Orthogonality Error", style="magenta")
table.add_row("Classical", f"{hilbert_results[0]:.6e}")
table.add_row("Modified", f"{hilbert_results[1]:.6e}")

console.print(table)
console.print(f"\n[bold green]Improvement ratio:[/bold green] {hilbert_results[2]:.2f}x")
