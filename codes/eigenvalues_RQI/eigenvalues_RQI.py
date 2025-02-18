import numpy as np
from numpy.linalg import norm, solve


def rayleigh_quotient_iteration(A, x0, max_iter=100, tol=1e-10):
    """
    Implements Rayleigh Quotient Iteration to find eigenvalue and eigenvector
    A: symmetric positive definite matrix
    x0: initial vector guess
    returns: eigenvalue, eigenvector
    """
    x = x0 / norm(x0)  # Normalize initial vector
    lambda_prev = 0

    for k in range(max_iter):
        # Compute Rayleigh quotient
        lambda_k = np.dot(x, A @ x)

        # Check convergence
        if abs(lambda_k - lambda_prev) < tol:
            return lambda_k, x

        # Solve (A - λI)x = y for y
        try:
            y = solve(A - lambda_k * np.eye(len(A)), x)
        except np.linalg.LinAlgError:
            # If singular, perturb lambda slightly
            y = solve(A - (lambda_k + 1e-10) * np.eye(len(A)), x)

        # Update x
        x = y / norm(y)
        lambda_prev = lambda_k

    return lambda_k, x


def orthogonalize_vector(v, previous_vectors):
    """
    Orthogonalize vector v against all previous eigenvectors
    """
    v = v.copy()
    for u in previous_vectors:
        v = v - np.dot(u, v) * u
    return v / norm(v) if norm(v) > 1e-10 else v


def deflate_matrix(A, eigenvalue, eigenvector):
    """
    Deflate matrix using the found eigenvalue and eigenvector
    A: original matrix
    eigenvalue: computed eigenvalue
    eigenvector: corresponding eigenvector
    returns: deflated matrix
    """
    # Normalize eigenvector
    v = eigenvector / norm(eigenvector)
    # Compute outer product
    return A - eigenvalue * np.outer(v, v)


def find_eigenvalues(A, num_eigenvalues=3, max_iter=100, tol=1e-10):
    """
    Find the eigenvalues of an SPD matrix
    A: symmetric positive definite matrix
    returns: list of 'num_eigenvalues' eigenvalues, list of corresponding eigenvectors
    """
    n = A.shape[0]
    eigenvalues = []
    eigenvectors = []

    # Make a copy of A to modify during deflation
    A_current = A.copy()

    for i in range(num_eigenvalues):
        # Initialize random vector
        x0 = np.random.rand(n)

        # Orthogonalize against previous eigenvectors
        if i > 0:
            x0 = orthogonalize_vector(x0, eigenvectors)

        # Find eigenvalue and eigenvector
        eigenvalue, eigenvector = rayleigh_quotient_iteration(
            A_current, x0, max_iter, tol
        )

        # Orthogonalize eigenvector against previous eigenvectors
        if i > 0:
            eigenvector = orthogonalize_vector(eigenvector, eigenvectors[:i])

        # Store results
        eigenvalues.append(eigenvalue)
        eigenvectors.append(eigenvector)

        # Deflate matrix
        A_current = deflate_matrix(A_current, eigenvalue, eigenvector)

    return eigenvalues, eigenvectors


# Example usage
if __name__ == "__main__":
    # Create a random SPD matrix for testing
    np.random.seed(42)  # For reproducibility
    n = 5
    # Generate random symmetric matrix and make it SPD
    A = np.random.rand(n, n)
    A = (A + A.T) / 2  # Make symmetric
    A = A @ A.T + np.eye(n)  # Make positive definite

    print("Original matrix A:")
    print(A)

    # Find three largest eigenvalues
    num_eigenvalues = 5
    eigenvalues, eigenvectors = find_eigenvalues(A, num_eigenvalues)

    print(f"\nFinding {num_eigenvalues} eigenvalues:")
    for i, (eigval, eigvec) in enumerate(zip(eigenvalues, eigenvectors)):
        print(f"\nEigenvalue {i+1}: {eigval}")
        print(f"Eigenvector {i+1}: {eigvec}")

        # Verify the result using original matrix A
        Av = A @ eigvec
        lambda_v = eigval * eigvec
        error = norm(Av - lambda_v) / norm(Av)
        print(f"Verification error: {error}")

        # Check orthogonality with previous eigenvectors
        if i > 0:
            for j in range(i):
                dot_product = np.abs(np.dot(eigenvectors[i], eigenvectors[j]))
                print(f"Orthogonality with eigenvector {j+1}: {dot_product}")

    # Compare with numpy's eigh (for validation)
    eigenvalues_np, _ = np.linalg.eigh(A)
    print("\nNumpy's largest eigenvalues (for comparison):")
    print(sorted(eigenvalues_np, reverse=True))
