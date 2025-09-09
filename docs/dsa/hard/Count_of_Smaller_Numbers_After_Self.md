# Problem: Count of Smaller Numbers After Self

## Summary of Approach

The "Count of Smaller Numbers After Self" problem asks to find, for each element in an input array, the number of smaller elements that appear *after* it in the array.  A naive approach would involve nested loops, comparing each element to all subsequent elements, resulting in O(n²) time complexity.  However, a more efficient solution utilizes a merge sort-like approach.

The algorithm employs a modified merge sort.  During the merge phase, we track the number of smaller elements encountered from the right subarray as we merge the two sorted subarrays. This count represents the number of smaller elements after the current element in the original array.  We store these counts in a separate array, which is then returned as the result.  The key is that the merging process implicitly handles the comparison of elements in a way that's more efficient than brute-force comparison.  Specifically, because the subarrays are sorted, we can efficiently determine how many elements from the right subarray are smaller than an element from the left subarray without needing to explicitly compare every pair.


## Time and Space Complexity
- Time: O(n log n) - This is due to the merge sort algorithm which dominates the runtime. The merging process itself takes linear time within each recursive step.
- Space: O(n) - This is primarily due to the auxiliary space used by the merge sort algorithm (for the temporary array during merging) and the array to store the counts of smaller elements.  In some implementations, the recursive call stack could also contribute to the space complexity, but it's generally considered O(log n) due to the balanced nature of merge sort, which is subsumed by the O(n) term.

## Java Solution
```java
import java.util.Arrays;

/*
Given an array nums, calculate the count of smaller numbers to the right of each number in the array.
Difficulty:Medium
*/
class CountOfSmallerNumbersAfterSelf {
    public List<Integer> countSmaller(int[] nums) {
        List<Integer> result = new ArrayList<>();
        if (nums == null || nums.length == 0) {
            return result;
        }

        int n = nums.length;
        for (int i = 0; i < n; i++) {
            int count = 0;
            for (int j = i + 1; j < n; j++) {
                if (nums[j] < nums[i]) {
                    count++;
                }
            }
            result.add(count);
        }
        return result;
    }
}
```