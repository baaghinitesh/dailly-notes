# Problem: Find N Unique Integers Sum up to Zero

## Summary of Approach

The problem asks to find `N` unique integers that sum up to zero.  A simple and efficient approach leverages the properties of integers. We can construct a solution by creating a sequence of integers from `-N/2` to `N/2 -1` (if `N` is even) or from `-(N-1)/2` to `(N-1)/2` (if `N` is odd). This sequence inherently sums to zero due to the cancellation of positive and negative pairs.  If `N` is even, we include `0` as the middle element of the array which doesn't affect the sum. We then simply need to return this sequence of integers as an array.


## Time and Space Complexity
- Time: O(N) - Creating the array of integers takes linear time proportional to N.
- Space: O(N) - The space used by the array of integers is proportional to N.

## Java Solution
```java
/*
Given an integer n, return any array containing n unique integers that sum up to 0.

Example 1:
Input: n = 5
Output: [-7,-1,1,3,4]
Explanation: These are unique integers and sum up to 0.

Example 2:
Input: n = 3
Output: [-1,0,1]

Example 3:
Input: n = 1
Output: [0]

Constraints:
1 <= n <= 1000
*/
/*
Difficulty: Easy
*/
class FindNUniqueIntegersSumUpToZero {
    public int[] sumZero(int n) {
        int[] result = new int[n];
        int sum = 0;
        for (int i = 0; i < n - 1; i++) {
            result[i] = i + 1;
            sum += result[i];
        }
        result[n - 1] = -sum;
        return result;
    }
}
```