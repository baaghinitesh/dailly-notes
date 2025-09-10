# Problem: Find K Closest Elements

## Summary of Approach

The "Find K Closest Elements" problem aims to find the k closest elements to a given target value in a sorted array.  Several approaches can solve this.  A highly efficient approach leverages the sorted nature of the input array.  It uses binary search to find the element closest to the target, and then expands outwards from that point, comparing distances to the target until k elements are collected. This avoids unnecessary comparisons by focusing on the most likely candidates near the closest element. Another approach involves using a heap data structure but is generally less efficient than the binary search based approach.


## Time and Space Complexity

- **Time:** O(log n + k), where n is the length of the input array and k is the number of closest elements to return.  The O(log n) comes from the binary search to find the starting point. The O(k) comes from expanding outwards to collect the k closest elements.

- **Space:** O(k). This is the space required to store the k closest elements found.  In-place algorithms could reduce this but at the cost of increased time complexity.  The binary search approach, described above, uses constant extra space beyond the output.

## Java Solution
```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/*
Given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. The result should also be sorted in ascending order.

An integer a is closer to x than an integer b if |a - x| < |b - x|. If |a - x| == |b - x|, then the smaller integer is closer.

Example 1:
Input: arr = [1,2,3,4,5], k = 4, x = 3
Output: [1,2,3,4]

Example 2:
Input: arr = [1,2,3,4,5], k = 4, x = -1
Output: [1,2,3,4]

Constraints:
1 <= k <= arr.length
1 <= arr.length <= 104
arr is sorted in ascending order
-104 <= x <= 104
-104 <= arr[i] <= 104


Difficulty: Medium
*/
class FindKClosestElements {
    public List<Integer> findClosestElements(int[] arr, int k, int x) {
        int left = 0;
        int right = arr.length - k;

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (Math.abs(arr[mid] - x) > Math.abs(arr[mid + k] - x)) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        List<Integer> result = new ArrayList<>();
        for (int i = left; i < left + k; i++) {
            result.add(arr[i]);
        }
        return result;
    }
}
```