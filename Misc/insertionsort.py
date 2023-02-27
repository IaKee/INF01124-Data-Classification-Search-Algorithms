swaps = 0

def insertionSort(arr):
    global swaps
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            swaps += 1
        arr[j + 1] = key
        #print(arr)
        print(arr)

# Driver code to test above
arr = [98, 95, 91, 43, 79, 28, 36, 35]
insertionSort(arr)
print("\n\nSorted array is:")
for i in range(len(arr)):
    for j in range(i+1):
        print("%d," % arr[j], end = '')
    print(" ")
print("Swaps: " + str(swaps))