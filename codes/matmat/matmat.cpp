#include <iostream> // input and output operations
#include <iomanip> // manipulating input/output stream formatting
#include <vector> // using vectors
#include <chrono> // time-related functions
#include <random> // generating random numbers
#include <cmath> // mathematical functions
#include <cassert> // debugging purposes
#include <fstream> // file operations
// Function to initialize a matrix with random values
void initialize_matrix(std::vector<double>& M, int N) {
    std::mt19937 gen(42); // Fixed seed for reproducibility
    std::uniform_real_distribution<> dis(0.0, 1.0);

    for (int i = 0; i < N * N; ++i) {
        M[i] = dis(gen);
    }
}

// Standard matrix multiplication (naïve triple-nested loop)
// Computes C = A * B
// A, B, and C are stored in row-major order in 1D std::vector<double>
void matmul_standard(const std::vector<double>& A, const std::vector<double>& B,
                     std::vector<double>& C, int N) {
    // For each row of A
    for (int i = 0; i < N; ++i) {
        // For each column of B
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            // Compute the dot product of the i-th row of A and j-th column of B
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}

// Blocked matrix multiplication
// Computes C = A * B using blocking to improve cache performance
void matmul_blocked(const std::vector<double>& A, const std::vector<double>& B,
                    std::vector<double>& C, int N, int block_size) {
    // Loop over blocks
    for (int ii = 0; ii < N; ii += block_size) {
        for (int jj = 0; jj < N; jj += block_size) {
            for (int kk = 0; kk < N; kk += block_size) {
                // Loop within blocks
                for (int i = ii; i < std::min(ii + block_size, N); ++i) {
                    for (int j = jj; j < std::min(jj + block_size, N); ++j) {
                        double sum = C[i * N + j]; // Use existing value in C
                        for (int k = kk; k < std::min(kk + block_size, N); ++k) {
                            sum += A[i * N + k] * B[k * N + j];
                        }
                        C[i * N + j] = sum;
                    }
                }
            }
        }
    }
}

// Function to compare two matrices for equality within a tolerance
bool compare_matrices(const std::vector<double>& M1, const std::vector<double>& M2, int N) {
    double epsilon = 1e-6; // Tolerance for floating-point comparison
    for (int i = 0; i < N * N; ++i) {
        if (std::abs(M1[i] - M2[i]) > epsilon) {
            return false;
        }
    }
    return true;
}

int main() {
    // output file
    std::string filename = "output.csv";
    std::ofstream outputFile(filename);

    // Matrix sizes
    std::vector<int> N = {128, 256, 384, 512, 640, 768, 896, 1024};
    // Block sizes
    std::vector<int> block_sizes = {2, 4, 8, 16, 32};

    // Output the total execution times and speedups
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "MatrixSize,BlockSize,Time(s),Speedup\n";
    // Write to output file
    outputFile << "MatrixSize,BlockSize,Time(s),Speedup\n";

    double time_standard = 0.0;
    std::vector<double> A, B, C_standard;
    int n = 0;
    for (size_t i = 0; i < N.size(); ++i) {
        n = N[i];
        // Matrices A, B, and C are stored in row-major order
        A.resize(n * n);
        B.resize(n * n);
        C_standard.resize(n * n);
        // Initialize matrices with random values
        initialize_matrix(A, n);
        initialize_matrix(B, n);
        // Variables to accumulate execution times
        time_standard = 0.0;
        // Execute standard matrix multiplication 3 times
        for (int run = 0; run < 3; ++run) {
            // Reset C_standard
            std::fill(C_standard.begin(), C_standard.end(), 0.0);

            auto start = std::chrono::high_resolution_clock::now();
            matmul_standard(A, B, C_standard, n);
            auto end = std::chrono::high_resolution_clock::now();

            std::chrono::duration<double> elapsed = end - start;
            time_standard += elapsed.count();
        }
        // Write to output file
        outputFile << n << "," << 1 << "," << time_standard << "," << 1 << "\n";
        // Write to console
        std::cout << n << "," << 1 << "," << time_standard << "," << 1 << "\n";
    }

    // Execute blocked matrix multiplication for different block sizes
    std::vector<double> C_blocked(n * n);
    for (size_t idx = 0; idx < block_sizes.size(); ++idx) {
        const int block_size = block_sizes[idx];
        double time_blocked = 0.0;
        // Accumulate time over 3 runs
        for (int run = 0; run < 3; ++run) {
            // Reset C_blocked
            std::fill(C_blocked.begin(), C_blocked.end(), 0.0);

            auto start = std::chrono::high_resolution_clock::now();
            matmul_blocked(A, B, C_blocked, n, block_size);
            auto end = std::chrono::high_resolution_clock::now();

            std::chrono::duration<double> elapsed = end - start;
            time_blocked += elapsed.count();
        }

        assert(compare_matrices(C_standard, C_blocked, n));

        const double speedup = time_standard / time_blocked;
        // Write to output file
        outputFile << n << "," << block_size << "," << time_blocked << "," << speedup << "\n";
        // Write to console
        std::cout << n << "," << block_size << "," << time_blocked << "," << speedup << "\n";
    }

    return 0;
}
