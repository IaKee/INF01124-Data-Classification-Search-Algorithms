# Radix sort for variable length strings
def radixSortString(array):
    maxLen = -1
    for string in array: # Find longest string
        strLen = len(string)
        if strLen > maxLen:
            maxLen = strLen
    oa = ord('a') - 1; # First character code
    oz = ord('z') - 1; # Last character code
    n = oz - oa + 2; # Number of buckets (+empty character)
    buckets = [[] for i in range(0, n)] # The buckets
    for position in reversed(range(0, maxLen)):
        for string in array:
            index = 0 # Assume "empty" character
            if position < len(string): # Might be within length
                index = ord(string[position]) - oa
            buckets[index].append(string) # Add to bucket
        del array[:]
        for bucket in buckets: # Reassemble array in new order
            array.extend(bucket)
            del bucket[:]
    return array

arr = ["arroz", "banana", "ata", "aa", "a", "b", "z"]
print("Array inicial: ", arr)
arr = radixSortString(arr)
print("Sorted array:", arr)