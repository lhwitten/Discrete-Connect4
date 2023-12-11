import numpy as np

def cheesed_array(arr):
    # Create a copy of the original array
    swapped_array = arr.copy()
    
    # Swap values in the temporary array
    swapped_array[arr == 1] = 2
    swapped_array[arr == 2] = 1
    
    return swapped_array

# Example usage:
original_array = np.array([[0, 1, 0], [2, 0, 1]])
result_array = cheesed_array(original_array)

print("Original Array:")
print(original_array)

print("\nArray after swapping values 1 and 2:")
print(result_array)