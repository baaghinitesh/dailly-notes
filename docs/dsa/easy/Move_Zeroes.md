# Problem: Move Zeroes

## Summary of Approach

The "Move Zeroes" problem requires rearranging the elements of an array such that all the zeroes are moved to the end while maintaining the relative order of the non-zero elements.  A two-pointer approach is efficient. One pointer (`nonZeroIndex`) tracks the index where the next non-zero element should be placed. The other pointer (`currentIndex`) iterates through the array.  If `currentIndex` encounters a non-zero element, it's swapped with the element at `nonZeroIndex`, and both pointers advance. If `currentIndex` encounters a zero, only `currentIndex` advances.  This ensures that all non-zero elements are compacted to the beginning, effectively moving zeroes to the end.


## Time and Space Complexity
- Time: O(n) - The algorithm iterates through the array once. Swapping elements takes constant time.
- Space: O(1) - The algorithm operates in place; it doesn't use extra space proportional to the input size.

## Java Solution
```java
/*
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
Example 2:

Input: nums = [0]
Output: [0]
Example 3:

Input: nums = [0,0,1]
Output: [1,0,0]

Constraints:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1

Difficulty: Easy
*/
class MoveZeroes {
    public void moveZeroes(int[] nums) {
        int k=0;
        for(int i=0; i<nums.length; i++){
            if(nums[i]!=0){
                nums[k]=nums[i];
                k++;
            }
        }
        for(int i=k; i<nums.length; i++){
            nums[i]=0;
        }
    }
}
```