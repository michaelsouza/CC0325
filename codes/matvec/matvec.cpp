#include <vector>
#include <chrono> // Include chrono for timing
#include <iostream> // Add this line to fix the linter errors
#include <fstream> // Include fstream for file operations
#include <cblas.h> // Include BLAS header for dgemv function

void matvec(const double* matrix, const double* vector, double* result, int nrows) {
    for (int i = 0; i < nrows; ++i) {
        for (int j = 0; j < nrows; ++j) {
            result[i] += matrix[i * nrows + j] * vector[j];
        }
    }
}

void matvec_blas(const double* matrix, const double* vector, double* result, int nrows) {
    cblas_dgemv(CblasRowMajor, CblasNoTrans, nrows, nrows, 1.0, matrix, nrows, vector, 1, 0.0, result, 1);
}

void fill_matrix(double* matrix, int nrows){
    for (int i = 0; i < nrows; ++i) {
        for (int j = 0; j < nrows; ++j) {
            matrix[i * nrows + j] = rand() / RAND_MAX;
        }
    }
}

void fill_vector(double* vector, int nrows){
    for (int i = 0; i < nrows; ++i) {
        vector[i] = rand() / RAND_MAX;
    }
}


void profile_matvec(std::vector<int> NROWS) {
    std::string filename = "output.txt";
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

int main() {
    std::vector<int> NROWS = {100, 200, 300, 500, 800, 1000, 2000, 5000, 10000, 15000, 20000};
    profile_matvec(NROWS);
    return EXIT_SUCCESS;
}