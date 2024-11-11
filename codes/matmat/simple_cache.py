import numpy as np
from typing import Tuple
from collections import OrderedDict
from rich import print
from rich.table import Table
from rich.console import Console


class Memory:
    def __init__(self, cache_size: int = 16, cache_line_size: int = 4):
        """Initializes the Memory object with cache properties and counters.

        Args:
            cache_size (int, optional): The maximum number of elements that the cache can hold. Defaults to 16.
            cache_line_size (int, optional): Number of elements in a single cache line. Defaults to 4.

        Attributes:
            cache_size (int): The maximum number of elements that the cache can hold.
            cache (OrderedDict): A dictionary that maintains the order of insertion for cache entries using LRU policy.
            cache_hits (int): Counter for the number of successful cache lookups.
            cache_misses (int): Counter for the number of failed cache lookups.
            cache_line_size (int): Number of elements in a single cache line.
            main_memory (list): A list representing main memory storage.
            console (Console): A rich console for formatted outputs.

        Raises:
            ValueError: If cache_line_size is greater than cache_size or if cache_size is not divisible by cache_line_size.
        """
        self.cache_size = cache_size
        self.cache = OrderedDict()
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_line_size = cache_line_size  # number of elements in a cache line
        self.main_memory = []

        # Validate cache configuration
        if self.cache_line_size > self.cache_size:
            raise ValueError("Cache line size must be less than cache size")

        if self.cache_size % self.cache_line_size != 0:
            raise ValueError("Cache size must be divisible by cache line size")

        self.console = Console()

    def get(self, key):
        """Retrieves a key from the cache. If the key is not in the cache, it simulates a cache miss
        and loads the relevant cache line from main memory.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value from the cache or None if the key is loaded without an explicit value.
        """
        if key in self.cache:
            self.cache_hits += 1
            self.cache.move_to_end(key)  # Move the accessed key to the end to simulate LRU
            return self.cache[key]
        self.cache_misses += 1

        # Simulate loading the cache line containing the key from main memory
        for i, k in enumerate(self.main_memory):
            if k != key:
                continue
            cache_line_block = i // self.cache_line_size
            cache_line_begin = cache_line_block * self.cache_line_size
            cache_line_end = (cache_line_block + 1) * self.cache_line_size
            for j in range(cache_line_begin, cache_line_end):
                if j >= 0 and j < len(self.main_memory):
                    self.put(self.main_memory[j])
            break

    def put(self, key: str):
        """Puts a key into the cache and handles eviction if necessary.

        Args:
            key (str): The key to insert into the cache.
        """
        if len(self.cache) == self.cache_size:
            removed_key, _ = self.cache.popitem(last=False)  # Evict the oldest item (LRU)
        self.cache[key] = None

    def allocate_matrix(self, key: str, shape: Tuple[int, int]) -> np.ndarray:
        """Allocates a matrix in main memory and returns a zero-initialized numpy array.

        Args:
            key (str): The identifier for the matrix.
            shape (Tuple[int, int]): The dimensions of the matrix (rows, columns).

        Returns:
            np.ndarray: The allocated matrix initialized with zeros.

        Note:
            Each element is represented in main memory as "{key}_{i}_{j}".
        """
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.main_memory.append(f"{key}_{i}_{j}")
        return np.zeros(shape)

    def show_cache_statistics(self):
        """Displays the cache hit/miss statistics using rich formatting."""
        total_accesses = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_accesses) * 100 if total_accesses > 0 else 0.0

        # Estimated time in milliseconds (fictional)
        estimated_time = self.cache_hits + self.cache_misses * 100

        table = Table(title="Cache Statistics")        

        table.add_column("Metric", style="cyan", justify="left")
        table.add_column("Value", style="magenta", justify="right")

        table.add_row("Cache Line Size", str(self.cache_line_size))
        table.add_row("Cache Size", str(self.cache_size))
        table.add_row("Cache Hits", str(self.cache_hits))
        table.add_row("Cache Misses", str(self.cache_misses))
        table.add_row("Total Accesses", str(total_accesses))
        table.add_row("Hit Rate", f"{hit_rate:.2f}%")
        table.add_row("Estimated Time", f"{estimated_time:.1E} ms")

        self.console.print(table)

    def reset_cache_counters(self):
        """Resets the cache hit and miss counters and confirms the action."""
        self.cache_hits = 0
        self.cache_misses = 0
        self.console.print("[green]Cache hit and miss counters have been reset.[/green]")


def matmatmul(memory: Memory, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Performs standard matrix multiplication with memory access simulation.

    Args:
        memory (Memory): The memory object for simulating cache behavior.
        A (np.ndarray): The first input matrix.
        B (np.ndarray): The second input matrix.
        C (np.ndarray): The result matrix (initialized to zeros).

    Returns:
        np.ndarray: The resulting matrix after multiplication.
    """
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(B.shape[0]):
                memory.get(f"A_{i}_{k}")
                memory.get(f"B_{k}_{j}")
                C[i, j] += A[i, k] * B[k, j]
    return C


def matmatmul_blocked(memory: Memory, A: np.ndarray, B: np.ndarray, C: np.ndarray, block_size: int = 2) -> np.ndarray:
    """Performs blocked matrix multiplication with memory access simulation.

    Args:
        memory (Memory): The memory object for simulating cache behavior.
        A (np.ndarray): The first input matrix.
        B (np.ndarray): The second input matrix.
        C (np.ndarray): The result matrix (initialized to zeros).
        block_size (int): The size of the block for the blocked multiplication.

    Returns:
        np.ndarray: The resulting matrix after blocked multiplication.
    """
    if block_size > A.shape[0] or block_size > A.shape[1] or block_size > B.shape[0] or block_size > B.shape[1]:
        raise ValueError("Block size must be less than or equal to the dimensions of the matrices")

    for i0 in range(0, A.shape[0], block_size):
        for j0 in range(0, B.shape[1], block_size):
            for k0 in range(0, B.shape[0], block_size):
                for i in range(i0, min(i0 + block_size, A.shape[0])):
                    for j in range(j0, min(j0 + block_size, B.shape[1])):
                        for k in range(k0, min(k0 + block_size, B.shape[0])):
                            memory.get(f"A_{i}_{k}")
                            memory.get(f"B_{k}_{j}")
                            C[i, j] += A[i, k] * B[k, j]
    return C


def main():
    # Cache configuration
    cache_size = 64
    cache_line_size = 4

    # Matrix configuration
    nrows = 32
    ncols = 32
    block_size = 16

    # Create a Memory object
    memory = Memory(cache_size=cache_size, cache_line_size=cache_line_size)

    # Allocate matrices in main memory
    A = memory.allocate_matrix("A", (nrows, ncols))
    B = memory.allocate_matrix("B", (nrows, ncols))

    # Fill the matrices with random values
    A[:] = np.random.rand(nrows, ncols)
    B[:] = np.random.rand(nrows, ncols)

    # Perform standard matrix multiplication
    C = memory.allocate_matrix("C", (nrows, ncols))
    C = matmatmul(memory, A, B, C)

    # Display cache statistics after standard multiplication
    memory.show_cache_statistics()

    # Reset cache counters before the next operation
    memory.reset_cache_counters()

    # Perform blocked matrix multiplication
    C_blocked = memory.allocate_matrix("C_blocked", (nrows, ncols))
    C_blocked = matmatmul_blocked(memory, A, B, C_blocked, block_size=2)

    # Display cache statistics after blocked multiplication
    memory.show_cache_statistics()

    # Check if the results are the same
    assert np.allclose(C, C_blocked), "The results of standard and blocked matrix multiplication do not match."


if __name__ == "__main__":
    main()
