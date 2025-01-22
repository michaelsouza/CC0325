import requests
from io import BytesIO
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from numpy.linalg import svd
import pandas as pd

def image_svd(image):
    # Convert the image to a NumPy array
    matrix_A = np.array(image, dtype=float)  # Ensure the array is of type float for SVD

    # Calculate the SVD of A
    U, s, V = svd(matrix_A, full_matrices=False)

    # Ensure that the singular values are sorted in descending order
    if not np.all(s == np.sort(s)[::-1]):
        raise ValueError("The singular values are not sorted in descending order.")

    return matrix_A, U, s, V

def svd_size(U, s, V):
    # Calculate the storage size of SVD components
    return U.size + s.size + V.size

def compress_image_svd(image_original, K):
    """
    Load an image, calculate its SVD, keep the k largest singular values,
    and reconstruct the compressed image.

    Args:
        image_original (PIL.Image.Image): Original image (PIL Image object).
        K (list of int): List of numbers of largest singular values to keep.

    Returns:
        tuple: A tuple containing:
            - images_small (list of PIL.Image.Image): List of reconstructed images.
            - compression_ratios (list of float): List of compression ratios corresponding to each k.
    """
    compression_ratios = []
    images_small = []
    try:
        matrix_A, U, s, V = image_svd(image_original)
        matrix_size_original = matrix_A.shape[0] * matrix_A.shape[1]
        for k in K:
            if k == 0:
                # Create a black image
                matrix_A_small = np.zeros_like(matrix_A)
                compression_ratio = 1  # No compression possible
            else:
                # Ensure k does not exceed the number of singular values
                k = min(k, len(s))
                U_small = U[:, :k]
                s_small = s[:k]
                V_small = V[:k, :]
                matrix_A_small = U_small @ np.diag(s_small) @ V_small
                compression_ratio = 1 - svd_size(U_small, s_small, V_small) / matrix_size_original

            # Clip values to valid pixel range and convert to uint8
            matrix_A_small = np.clip(matrix_A_small, 0, 255).astype(np.uint8)

            # Convert the reconstructed matrix back to a PIL image
            img_small = Image.fromarray(matrix_A_small)
            images_small.append(img_small)
            compression_ratios.append(compression_ratio)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    # Create a DataFrame to display compression ratios
    df = pd.DataFrame({"k": K, "compression_ratio": compression_ratios})
    print(df)
    return images_small, compression_ratios

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        print(f"Failed to download image. Status code: {response.status_code}")
        exit()
    return BytesIO(response.content)

if __name__ == "__main__":
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Portrait_of_Sir_Isaac_Newton%2C_1689_%28brightened%29.jpg/800px-Portrait_of_Sir_Isaac_Newton%2C_1689_%28brightened%29.jpg"
    image_data = download_image(image_url)

    K = [0, 10, 50, 100, 150, 200, 300]  # Different values of k to test

    # Open the original image in grayscale
    image_original = Image.open(image_data).convert("L")

    # Compress the image for each value of k
    images_small, compression_ratios = compress_image_svd(image_original, K)

    if images_small is None:
        print("Image compression failed.")
        exit()

    # Plot the original and reconstructed images
    num_images = len(images_small)
    plt.figure(figsize=(20, 5 * ((num_images // 4) + 1)))  # Adjust figure size as needed

    # Plot the Original Image
    plt.subplot(2, 4, 1)
    plt.imshow(image_original, cmap="gray")
    plt.title("Original Image")
    plt.axis("off")

    # Plot the Compressed Images
    for i in range(num_images):
        plt.subplot(2, 4, i + 2)
        plt.imshow(images_small[i], cmap="gray")
        plt.title(f"Compressed (k = {K[i]})\nCompression Ratio: {compression_ratios[i]:.2f}")
        plt.axis("off")

    plt.tight_layout()
    plt.show()
