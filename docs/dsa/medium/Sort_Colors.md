# Problem: Sort Colors

## Summary of Approach

The "Sort Colors" problem requires sorting an array of integers representing colors (0, 1, and 2) in-place, without using any sorting library functions.  A common and efficient approach is the two-pointer (or three-pointer) technique.  We use two pointers, `low` and `high`, initialized to the beginning and end of the array, respectively.  A `mid` pointer iterates through the array.

The algorithm proceeds as follows:

1. **Iterate:** The `mid` pointer iterates through the array.
2. **0 encountered:** If `arr[mid] == 0`, swap `arr[mid]` and `arr[low]`, then increment both `low` and `mid`. This ensures all 0s are moved to the beginning.
3. **1 encountered:** If `arr[mid] == 1`, only increment `mid`.  The 1s will be in their correct position after processing the 0s and 2s.
4. **2 encountered:** If `arr[mid] == 2`, swap `arr[mid]` and `arr[high]`, then decrement `high`. This ensures all 2s are moved to the end.
5. **Repeat:** Continue until `mid` surpasses `high`.


This approach efficiently sorts the array in-place by partitioning it into three sections: 0s, 1s, and 2s.


## Time and Space Complexity
- Time: O(n) - The algorithm iterates through the array once.  Swapping elements takes constant time.
- Space: O(1) - The algorithm uses only a constant amount of extra space for the pointers (`low`, `mid`, `high`).

## Java Solution
```java
/*
Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

Difficulty: Medium
*/
class SortColors {
    public void sortColors(int[] nums) {
        int n = nums.length;
        int p0 = 0, p1 = 0;
        for (int i = 0; i < n; ++i) {
            if (nums[i] == 0) {
                swap(nums, i, p0);
                if (p0 < p1)
                    swap(nums, i, p1);
                p0++;
                p1++;
            } else if (nums[i] == 1) {
                swap(nums, i, p1);
                p1++;
            }
        }
    }
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```