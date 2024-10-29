#include <iostream>
#include <vector>
#include <chrono>
#include <cassert>
#include <cstdlib> // For rand() and srand()
#include <ctime>   // For time()
#include <fstream> // For ofstream
using namespace std;

// Function to initialize a matrix with random values using rand() % 100
void initializeMatrix(vector<double> &mat, int n) {
    for (int i = 0; i < n * n; ++i) {
        mat[i] = rand() % 100;
    }
}

// Standard matrix multiplication
void standardMatrixMultiply(const vector<double> &A, const vector<double> &B, vector<double> &C, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

// Block matrix multiplication
void blockMatrixMultiply(const vector<double> &A, const vector<double> &B, vector<double> &C, int n, int blockSize) {
    for (int i = 0; i < n; i += blockSize) {
        for (int k = 0; k < n; k += blockSize) {
            for (int j = 0; j < n; j += blockSize) {
                // Compute min to handle edge cases
                int i_max = min(i + blockSize, n);
                int k_max = min(k + blockSize, n);
                int j_max = min(j + blockSize, n);
                
                for (int ii = i; ii < i_max; ++ii) {
                    for (int kk = k; kk < k_max; ++kk) {
                        double a_val = A[ii * n + kk];
                        for (int jj = j; jj < j_max; ++jj) {
                            C[ii * n + jj] += a_val * B[kk * n + jj];
                        }
                    }
                }
            }
        }
    }
}

void profile_matmat(int n, const vector<int> &blockSizes, 
                   const vector<double> &A, const vector<double> &B,
                   std::ofstream &outputFile) {
    // Initialize result matrices
    vector<double> C_std(n * n, 0.0);
    vector<double> C_blk(n * n, 0.0);

    // Measure time for standard matrix multiplication
    auto tic = chrono::high_resolution_clock::now();
    standardMatrixMultiply(A, B, C_std, n);
    auto toc = chrono::high_resolution_clock::now();
    auto time_std = chrono::duration_cast<chrono::microseconds>(toc - tic).count();

    outputFile << n << ", " << 1 << ", " << time_std << std::endl;
    std::cout << n << ", " << 1 << ", " << time_std << std::endl;

    // Iterate over block sizes
    for (int blockSize : blockSizes) {
        if (blockSize > n) continue; // Skip invalid block sizes

        // Reset C_blk
        fill(C_blk.begin(), C_blk.end(), 0.0);

        // Measure time for block matrix multiplication
        tic = chrono::high_resolution_clock::now();
        blockMatrixMultiply(A, B, C_blk, n, blockSize);
        toc = chrono::high_resolution_clock::now();
        auto time_block = chrono::duration_cast<chrono::microseconds>(toc - tic).count();
        outputFile << n << ", " << blockSize << ", " << time_block << std::endl;
        std::cout << n << ", " << blockSize << ", " << time_block << std::endl;

        // Verify correctness with a tolerance for floating-point operations
        const double epsilon = 1e-6;
        for (int i = 0; i < n * n; ++i) {
            assert(abs(C_std[i] - C_blk[i]) < epsilon);
        }
    }
}

int main() {
    std::string filename = "output.txt";
    std::ofstream outputFile(filename); // Open a file for writing output

    // Seed the random number generator
    srand(static_cast<unsigned int>(time(0)));

    // Write header to file and console
    outputFile << "MatrixSize,BlockSize,Time(us)" << std::endl;
    std::cout << "MatrixSize,BlockSize,Time(us)" << std::endl;

    // Define matrix sizes and block sizes
    vector<int> matrix_sizes = {200, 300, 400, 500, 600, 700, 750, 800, 850, 900};
    vector<int> block_sizes = {4, 8, 16, 32, 64};

    for (int n : matrix_sizes) {
        // Initialize matrices A and B
        vector<double> A(n * n);
        vector<double> B(n * n);
        initializeMatrix(A, n);
        initializeMatrix(B, n);

        // Profile standard and block matrix multiplication
        profile_matmat(n, block_sizes, A, B, outputFile);
    }

    return EXIT_SUCCESS;
}
