This folder contains four Python scripts that implement the Hoare and Lomuto partitioning algorithms, which are commonly used in quicksort. The scripts are named based on the algorithm and the type of pivot used.

- `hoareAleatorio.py` implements the Hoare partitioning algorithm using a randomly chosen pivot element.
- `hoareMediana.py` implements the Hoare partitioning algorithm using the median of three pivot element selection strategy.
- `lomutoAleatorio.py` implements the Lomuto partitioning algorithm using a randomly chosen pivot element.
- `lomutoMediana.py` implements the Lomuto partitioning algorithm using the median of three pivot element selection strategy.

Each script takes an input file containing a list of integers, performs a quicksort using the selected partitioning algorithm, and writes the resulting sorted list to an output file. Additionally, each script generates a statistics file that contains information about the execution time and the number of comparisons and swaps performed during the sorting process.