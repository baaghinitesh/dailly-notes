/*
Question: Array Nesting
Difficulty: Medium

You are given an integer array nums of length n where nums[i] is in the range [0, n - 1].
You are tasked to find the length of the longest chain formed by repeatedly selecting an element from the array,
then replacing the selected element with the element at its index in the array.

For example:
nums = [5,4,0,3,1,6,2]
The longest chain is [5,6,2,3,1,0,4], length = 7.
*/
class ArrayNesting {
    public int arrayNesting(int[] nums) {
        int maxLen = 0;
        boolean[] visited = new boolean[nums.length];
        for (int i = 0; i < nums.length; i++) {
            if (!visited[i]) {
                int len = 0;
                int current = i;
                while (!visited[current]) {
                    visited[current] = true;
                    current = nums[current];
                    len++;
                }
                maxLen = Math.max(maxLen, len);
            }
        }
        return maxLen;
    }
}