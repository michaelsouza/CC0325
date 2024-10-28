#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using Matrix = vector<vector<double>>;

// Function to initialize a matrix with random values
void initializeMatrix(Matrix &mat, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            mat[i][j] = rand() % 100;
        }
    }
}

// Standard matrix multiplication
void standardMatrixMultiply(const Matrix &A, const Matrix &B, Matrix &C, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = 0;
            for (int k = 0; k < n; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Block matrix multiplication
void blockMatrixMultiply(const Matrix &A, const Matrix &B, Matrix &C, int n, int blockSize) {
    for (int i = 0; i < n; i += blockSize) {
        for (int j = 0; j < n; j += blockSize) {
            for (int k = 0; k < n; k += blockSize) {
                // Multiply the blocks
                for (int ii = i; ii < min(i + blockSize, n); ++ii) {
                    for (int jj = j; jj < min(j + blockSize, n); ++jj) {
                        double sum = 0;
                        for (int kk = k; kk < min(k + blockSize, n); ++kk) {
                            sum += A[ii][kk] * B[kk][jj];
                        }
                        C[ii][jj] += sum;
                    }
                }
            }
        }
    }
}

int main() {
    int n = 512; // Matrix size
    int blockSize = 64; // Block size for block multiplication

    // Initialize matrices A, B, and C
    Matrix A(n, vector<double>(n));
    Matrix B(n, vector<double>(n));
    Matrix C(n, vector<double>(n, 0));

    initializeMatrix(A, n);
    initializeMatrix(B, n);

    // Measure time for standard matrix multiplication
    auto start = chrono::high_resolution_clock::now();
    standardMatrixMultiply(A, B, C, n);
    auto end = chrono::high_resolution_clock::now();
    cout << "Standard matrix multiplication time: "
         << chrono::duration_cast<chrono::milliseconds>(end - start).count()
         << " ms" << endl;

    // Reset matrix C
    C = Matrix(n, vector<double>(n, 0));

    // Measure time for block matrix multiplication
    start = chrono::high_resolution_clock::now();
    blockMatrixMultiply(A, B, C, n, blockSize);
    end = chrono::high_resolution_clock::now();
    cout << "Block matrix multiplication time: "
         << chrono::duration_cast<chrono::milliseconds>(end - start).count()
         << " ms" << endl;

    return 0;
}
