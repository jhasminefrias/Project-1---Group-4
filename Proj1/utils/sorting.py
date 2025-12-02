class Sorting:
    @staticmethod
    def bubble_sort(arr, compare):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if compare(arr[j], arr[j+1]) > 0:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
