# Problem: Find K-th Smallest Pair Distance

## Summary of Approach

The problem "Find K-th Smallest Pair Distance" aims to find the k-th smallest absolute difference between any two numbers in a given integer array `nums`.  The most efficient approach utilizes a combination of sorting and binary search.

1. **Sort the array:**  Sorting the input array `nums` allows us to efficiently explore potential pair distances.

2. **Binary Search the Distance:** We perform a binary search on the range of possible distances (from 0 to the maximum difference between two elements in the sorted array). For each potential distance `mid`, we count the number of pairs in the sorted array whose difference is less than or equal to `mid`. This count can be efficiently determined using a two-pointer technique.

3. **Refine the Search:** Based on the count obtained in step 2, we adjust the search space in the binary search. If the count is less than `k`, we need to search for larger distances; otherwise, we search for smaller distances.

4. **Return the Result:**  The binary search eventually converges to the `k`-th smallest pair distance.


## Time and Space Complexity
- Time: O(n log n + n log w), where n is the length of the input array and w is the range of possible distances (approximately the maximum element minus the minimum element). The O(n log n) term comes from sorting, and the O(n log w) term comes from the binary search which performs a linear scan (O(n)) for each distance considered in the logarithmic number of steps (log w).  In many cases, w is significantly smaller than n, making the overall complexity dominated by the sorting step.

- Space: O(1) or O(n) depending on the sorting algorithm used.  In-place sorting algorithms (like HeapSort) achieve O(1) space complexity, while others (like merge sort) might require O(n) auxiliary space.  The counting process in the binary search requires only a constant amount of extra space.

## Java Solution
```java
import java.util.Arrays;

/*
Find K-th Smallest Pair Distance

Difficulty: Hard

Given an integer array nums and an integer k, return the kth smallest distance among all the pairs of the array.

The distance of a pair (nums[i], nums[j]) is abs(nums[i] - nums[j]).

Example 1:

Input: nums = [1,3,1], k = 1
Output: 0
Explanation: Here are all the pairs:
(1,3) -> 2
(1,1) -> 0
(3,1) -> 2
Then the 1st smallest distance pair is (1,1), and its distance is 0.

Example 2:

Input: nums = [1,1,1], k = 2
Output: 0

Example 3:

Input: nums = [1,6,1], k = 3
Output: 5


Constraints:

n == nums.length
2 <= n <= 104
0 <= nums[i] <= 108
1 <= k <= n * (n - 1) / 2
*/
class FindKthSmallestPairDistance {
    public int smallestDistancePair(int[] nums, int k) {
        Arrays.sort(nums);
        int n = nums.length;
        int left = 0, right = nums[n - 1] - nums[0];
        while (left < right) {
            int mid = left + (right - left) / 2;
            int count = 0, j = 0;
            for (int i = 0; i < n; i++) {
                while (j < n && nums[j] - nums[i] <= mid) {
                    j++;
                }
                count += j - i - 1;
            }
            if (count < k) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }
}
```