## Bucket Sort: Premium Study Notes

**1. Introduction**

Bucket Sort is a distribution-based sorting algorithm that works by distributing the elements of an array into a number of buckets or containers.  Each bucket is then sorted individually, either using a different sorting algorithm (often insertion sort for small buckets) or recursively using bucket sort itself. Finally, the sorted buckets are concatenated to produce the fully sorted output.  Bucket sort is efficient when the input is uniformly distributed over a range.  Its performance is highly dependent on the distribution of input data;  a skewed distribution can lead to significantly degraded performance.  Unlike comparison-based sorting algorithms like merge sort or quicksort, bucket sort doesn't rely on comparing elements directly; instead, it leverages the distribution of data to achieve sorting. This makes it a non-comparison sort.


**2. Core Concepts**

* **Buckets:**  The fundamental data structure in bucket sort. These are typically lists or arrays used to hold a subset of the input elements. The number of buckets is a crucial parameter that affects the algorithm's efficiency.

* **Distribution Function:**  A function that maps each input element to a specific bucket. This function is critical for the efficiency of the algorithm. A good distribution function will distribute elements evenly across the buckets.  A common approach is to use a hash function or a simple division-based mapping (e.g., `bucketIndex = floor(elementValue / bucketRange)`).

* **Bucket Size:** The number of elements each bucket can hold.  This can be fixed or variable.  Variable bucket size can adapt to uneven data distributions more effectively.

* **Individual Bucket Sorting:** Once elements are distributed, each bucket needs to be sorted individually.  This is often done with a simple algorithm like insertion sort, which is efficient for small, nearly-sorted lists.  Alternatively, bucket sort can be applied recursively to each bucket.

* **Concatenation:** After each bucket is sorted, the sorted buckets are concatenated to form the final sorted array.


**3. Practical Examples**

**Example 1: Sorting floating-point numbers between 0 and 1**

Let's sort the array `[0.897, 0.565, 0.656, 0.123, 0.665, 0.343, 0.912]` using 5 buckets.

1. **Distribution:** We'll use the simple division-based mapping: `bucketIndex = floor(element * 5)`.  This maps each element to a bucket based on its value.

2. **Bucketing:**
    * Bucket 0: [0.123]
    * Bucket 1: [0.343]
    * Bucket 2: [0.565]
    * Bucket 3: [0.656, 0.665]
    * Bucket 4: [0.897, 0.912]

3. **Sorting Buckets:** Each bucket is already sorted (or requires only trivial sorting in this example).

4. **Concatenation:** Concatenating the buckets gives the sorted array: `[0.123, 0.343, 0.565, 0.656, 0.665, 0.897, 0.912]`

**Example 2 (Illustrating recursive application):**  If a bucket contains a significant number of elements, instead of using insertion sort, we can recursively apply bucket sort to that bucket.  This adds a layer of complexity but can improve performance for uneven distributions.

**Code Example (Python):**  This example utilizes insertion sort for individual buckets.

```python
def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and key < bucket[j]:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key

def bucket_sort(arr, num_buckets):
    buckets = [[] for _ in range(num_buckets)]
    for num in arr:
        index = int(num * num_buckets) # assumes numbers are between 0 and 1
        buckets[index].append(num)

    for bucket in buckets:
        insertion_sort(bucket)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr

arr = [0.897, 0.565, 0.656, 0.123, 0.665, 0.343, 0.912]
sorted_arr = bucket_sort(arr, 5)
print(sorted_arr)
```


**4. Conclusion**

Bucket sort offers an efficient alternative to comparison-based sorting algorithms when the input data is uniformly distributed.  Its average-case time complexity is O(n+k), where n is the number of elements and k is the number of buckets.  However, its worst-case complexity can be O(n^2) if the data is highly clustered in a few buckets.  The choice of the distribution function and the method used to sort individual buckets significantly impacts the algorithm's performance. The optimal number of buckets often depends on the data and needs to be determined empirically or through analysis of the data distribution.  It's crucial to understand the limitations of bucket sort and to choose an appropriate sorting algorithm based on the characteristics of the input data.