#include <vector>
#include <chrono> // Include chrono for timing
#include <iostream> // Add this line to fix the linter errors
#include <fstream> // Include fstream for file operations
#include <cblas.h> // Include BLAS header for dgemv function

/**
 * @brief Performs matrix-vector multiplication using a naive implementation
 * @param matrix Pointer to the input matrix in row-major order
 * @param vector Pointer to the input vector
 * @param result Pointer to store the resulting vector
 * @param nrows Number of rows/columns in the square matrix
 */
void matvec(const double* matrix, const double* vector, double* result, int nrows) {
    for (int i = 0; i < nrows; ++i) {
        for (int j = 0; j < nrows; ++j) {
            result[i] += matrix[i * nrows + j] * vector[j];
        }
    }
}

/**
 * @brief Performs matrix-vector multiplication using BLAS dgemv function
 * @param matrix Pointer to the input matrix in row-major order
 * @param vector Pointer to the input vector
 * @param result Pointer to store the resulting vector
 * @param nrows Number of rows/columns in the square matrix
 */
void matvec_blas(const double* matrix, const double* vector, double* result, int nrows) {
    cblas_dgemv(CblasRowMajor, CblasNoTrans, nrows, nrows, 1.0, matrix, nrows, vector, 1, 0.0, result, 1);
}

/**
 * @brief Fills a matrix with random values between 0 and 1
 * @param matrix Pointer to the matrix to be filled
 * @param nrows Number of rows/columns in the square matrix
 */
void fill_matrix(double* matrix, int nrows){
    for (int i = 0; i < nrows; ++i) {
        for (int j = 0; j < nrows; ++j) {
            matrix[i * nrows + j] = rand() / RAND_MAX;
        }
    }
}

/**
 * @brief Fills a vector with random values between 0 and 1
 * @param vector Pointer to the vector to be filled
 * @param nrows Length of the vector
 */
void fill_vector(double* vector, int nrows){
    for (int i = 0; i < nrows; ++i) {
        vector[i] = rand() / RAND_MAX;
    }
}

/**
 * @brief Profiles the performance of matrix-vector multiplication for different matrix sizes
 * @param NROWS Vector containing different matrix sizes to test
 * @details Creates random matrices and vectors for each size, performs matrix-vector multiplication,
 *          measures execution time, and writes results to both console and a CSV file
 */
void profile_matvec(std::vector<int> NROWS) {
    // output file
    std::string filename = "output.csv";
    std::ofstream outputFile(filename); // Open a file for writing output

    // Write header to file and console
    outputFile << "NROWS,Time" << std::endl;
    std::cout << "NROWS,Time" << std::endl;

    // Loop through each NROWS value
    for(int nrows: NROWS){
        // Create a random matrix and vector
        std::vector<double> matrix(nrows * nrows, 0.0);
        std::vector<double> vector(nrows, 0.0);
        std::vector<double> result(nrows, 0.0);
        
        fill_matrix(matrix.data(), nrows);
        fill_vector(vector.data(), nrows);
        // Start the timer
        auto start = std::chrono::high_resolution_clock::now();

        // Call the matvec function
        matvec(matrix.data(), vector.data(), result.data(), nrows);
        // Call the matvec_blas function
        // matvec_blas(matrix.data(), vector.data(), result.data(), nrows);

        // Stop the timer
        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
        
        // Output to console and file
        std::cout << nrows << "," << duration.count() << std::endl;
        outputFile << nrows << "," << duration.count() << std::endl; // Write output to file
    }

    outputFile.close(); // Close the output file
    std::cout << "Results written to " << filename << std::endl;
}

/**
 * @brief Main function that runs the matrix-vector multiplication performance tests
 * @return EXIT_SUCCESS on successful execution
 */
int main() {
    std::vector<int> NROWS = {100, 200, 300, 500, 800, 1000, 2000, 5000, 10000, 15000, 20000};
    profile_matvec(NROWS);
    return EXIT_SUCCESS;
}