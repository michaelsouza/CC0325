import numpy as np


def jacobi_eigenvalue(A, tol=1e-10, max_iterations=100):
    """
    Aplica o método de Jacobi para diagonalizar a matriz simétrica A.

    Parâmetros:
        A              : matriz simétrica (numpy.ndarray de forma (n,n))
        tol            : tolerância para os elementos fora da diagonal
        max_iterations : número máximo de iterações permitidas

    Retorna:
        eigenvalues : vetor com os autovalores (elementos da diagonal de A final)
        V           : matriz cujas colunas são os autovetores correspondentes
        n_iter      : número de iterações realizadas
    """
    # Certifica que A é uma cópia para não modificar a original
    A = A.copy()
    n = A.shape[0]
    # Inicializa a matriz de autovetores como a identidade
    V = np.eye(n)

    for iter_count in range(max_iterations):
        # Obtém a parte superior (excluindo a diagonal) e seus valores absolutos
        off_diag = np.triu(np.abs(A), k=1)
        # Encontra o maior elemento fora da diagonal e seus índices (i, j)
        max_val = np.max(off_diag)
        if max_val < tol:
            break
        # Índices do pivô
        i, j = np.unravel_index(np.argmax(off_diag), A.shape)

        # Calcula o ângulo de rotação
        if np.abs(A[j, j] - A[i, i]) < 1e-12:
            theta = np.pi / 4
        else:
            theta = 0.5 * np.arctan2(2 * A[i, j], A[j, j] - A[i, i])

        c = np.cos(theta)
        s = np.sin(theta)

        # Armazena os valores atuais para atualização
        a_ii = A[i, i]
        a_jj = A[j, j]
        a_ij = A[i, j]

        # Atualiza os elementos do bloco (i, j)
        A[i, i] = c**2 * a_ii - 2 * s * c * a_ij + s**2 * a_jj
        A[j, j] = s**2 * a_ii + 2 * s * c * a_ij + c**2 * a_jj
        A[i, j] = 0.0
        A[j, i] = 0.0

        # Atualiza os elementos das outras linhas/colunas
        for k in range(n):
            if k != i and k != j:
                a_ik = A[i, k]
                a_jk = A[j, k]
                A[i, k] = c * a_ik - s * a_jk
                A[k, i] = A[i, k]  # por simetria
                A[j, k] = s * a_ik + c * a_jk
                A[k, j] = A[j, k]

        # Atualiza a matriz de autovetores
        for k in range(n):
            v_ki = V[k, i]
            v_kj = V[k, j]
            V[k, i] = c * v_ki - s * v_kj
            V[k, j] = s * v_ki + c * v_kj

    eigenvalues = np.diag(A)
    return eigenvalues, V, iter_count + 1


# Exemplo de uso:
if __name__ == "__main__":
    # Definindo uma matriz simétrica (exemplo)
    B = np.random.rand(4, 4)
    Q, R = np.linalg.qr(B)
    D = np.arange(1, 5)
    A = Q @ np.diag(D) @ Q.T

    # Show A
    print("Matriz A:")
    print(A)

    # Aplicando o método de Jacobi
    eigenvalues, eigenvectors, n_iter = jacobi_eigenvalue(
        A, tol=1e-8, max_iterations=100
    )

    # Exibindo os resultados
    print("\nAutovalores:")
    print(eigenvalues)
    print("\nAutovetores (colunas):")
    print(eigenvectors)
    print("\nNúmero de iterações:", n_iter)
