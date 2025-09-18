# Problem: Sort Array By Parity

## Summary of Approach

The "Sort Array By Parity" problem involves rearranging the elements of an integer array such that all even numbers come before all odd numbers.  The approach typically involves two pointers: one pointing to the beginning of the array and another pointing to the end.  The algorithm iterates, swapping elements when an even number is found at the end pointer and an odd number is found at the beginning pointer.  This continues until the two pointers cross each other.  Alternatively, one can create a new array, filling it with even numbers first from the original array and then with odd numbers.


## Time and Space Complexity
- Time: O(n) - The algorithm iterates through the array at most once.  In the two-pointer approach, each element is visited and potentially swapped once.  Creating a new array and filling it also requires a single pass through the original array.
- Space: O(1) or O(n) - The two-pointer approach operates in-place, requiring only constant extra space for pointers. The approach that creates a new array requires O(n) space to store the resulting array.

## Java Solution
```java
//Sort Array By Parity
//Easy
class SortArrayByParity {
    public int[] sortArrayByParity(int[] nums) {
        int[] result = new int[nums.length];
        int evenIndex = 0;
        int oddIndex = nums.length - 1;

        for (int num : nums) {
            if (num % 2 == 0) {
                result[evenIndex++] = num;
            } else {
                result[oddIndex--] = num;
            }
        }
        return result;
    }
}
```