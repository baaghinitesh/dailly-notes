# Problem: Median of Two Sorted Arrays

## Summary of Approach

The "Median of Two Sorted Arrays" problem aims to find the median of two sorted arrays efficiently.  A naive approach would involve merging the two arrays and then finding the median. However, this is inefficient.  A more optimal approach uses a divide-and-conquer strategy.  We can avoid fully merging the arrays by employing binary search. The algorithm focuses on finding a partition point in both arrays such that the elements to the left of this point in both arrays constitute the smaller half of the combined array.  By recursively narrowing down the search space using binary search on the smaller array, we efficiently identify the partition points and subsequently compute the median.  The key insight is that the partition points must satisfy a specific condition related to the elements immediately before and after them to ensure we have the correct number of elements on each side to represent the median.

## Time and Space Complexity
- Time: O(log(min(m, n))) where 'm' and 'n' are the lengths of the input arrays.  This is due to the binary search performed on the smaller array.
- Space: O(1). The algorithm uses constant extra space, regardless of the input size.  It operates primarily in-place.

## Java Solution
```java
// Median of Two Sorted Arrays
// Difficulty: Hard

class MedianOfTwoSortedArrays {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length;
        int n = nums2.length;
        if (m > n) {
            return findMedianSortedArrays(nums2, nums1); // Ensure nums1 is shorter
        }
        int low = 0, high = m;
        while (low <= high) {
            int partitionX = (low + high) / 2;
            int partitionY = (m + n + 1) / 2 - partitionX;
            int maxLeftX = (partitionX == 0) ? Integer.MIN_VALUE : nums1[partitionX - 1];
            int minRightX = (partitionX == m) ? Integer.MAX_VALUE : nums1[partitionX];
            int maxLeftY = (partitionY == 0) ? Integer.MIN_VALUE : nums2[partitionY - 1];
            int minRightY = (partitionY == n) ? Integer.MAX_VALUE : nums2[partitionY];
            if (maxLeftX <= minRightY && maxLeftY <= minRightX) {
                if ((m + n) % 2 == 0) {
                    return (double) (Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2;
                } else {
                    return (double) Math.max(maxLeftX, maxLeftY);
                }
            } else if (maxLeftX > minRightY) {
                high = partitionX - 1;
            } else {
                low = partitionX + 1;
            }
        }
        throw new IllegalArgumentException();
    }
}
```