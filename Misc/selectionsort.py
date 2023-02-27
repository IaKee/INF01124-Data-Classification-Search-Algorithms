# Python program for implementation of Selection
# Sort
import sys
swaps = 0

A = [42, 47, 90, 73, 29, 29, 19, 31]

# Traverse through all array elements
for i in range(len(A)):

    # Find the minimum element in remaining 
    # unsorted array
    min_idx = i
    for j in range(i + 1, len(A)):
        if A[min_idx] > A[j]:
            min_idx = j

    # Swap the found minimum element with 
    # the first element        
    if A[i]!=A[min_idx]: #chatinho velho
        swaps += 1
    A[i], A[min_idx] = A[min_idx], A[i]

    print(A)

# Driver code to test above
print("Sorted array")
#for i in range(len(A)):
#    print("%d" % A[i]),
print("Swaps:", swaps)