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