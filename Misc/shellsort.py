swaps = 0

def shellSort(alist):
    sublistcount = len(alist)//2
    while sublistcount > 0:

      for startposition in range(sublistcount):
        gapInsertionSort(alist,startposition,sublistcount)

      print("After increments of size",sublistcount,
                                   "The list is",alist)

      sublistcount = sublistcount // 2

def gapInsertionSort(alist,start,gap):
    global swaps

    for i in range(start+gap,len(alist),gap):

        currentvalue = alist[i]
        position = i

        while position>=gap and alist[position-gap]>currentvalue:
            alist[position]=alist[position-gap]
            position = position-gap
            swaps += 1

        alist[position]=currentvalue


alist = [56, 30, 60, 59, 45, 26, 72, 38, 25, 49, 94, 93, 89, 60, 65, 16]
shellSort(alist)
print(alist)
print("Swaps:",swaps)