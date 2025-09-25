# Problem: Daily Temperatures

## Summary of Approach

The Daily Temperatures problem aims to find, for each day, the number of days you have to wait until a warmer temperature occurs.  The approach uses a stack to efficiently track days and their temperatures.  We iterate through the temperatures.  For each temperature, we pop elements from the stack as long as the current temperature is warmer than the temperature at the top of the stack. When we pop an element, we calculate the difference in days (index difference) and store it in the result array corresponding to the popped day.  If the stack is empty or the current temperature is not warmer than the top of the stack, we push the current day and its temperature onto the stack.  Finally, any remaining days on the stack will have no warmer days in the future, so their waiting time is 0.


## Time and Space Complexity
- Time: O(N), where N is the number of temperatures.  While we might potentially iterate through the stack multiple times in the worst case, the total number of pushes and pops across the entire algorithm will never exceed N. Each element is pushed and popped at most once.
- Space: O(N) in the worst case. The stack could potentially hold all the temperatures if the temperatures are consistently decreasing.  In the best-case scenario (strictly increasing temperatures), the space complexity would be O(1).

## Java Solution
```java
/*
Daily Temperatures
Medium

Given an array of integers temperatures representing the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

Example 1:
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]

Example 2:
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Example 3:
Input: temperatures = [30,60,90]
Output: [1,1,0]
*/
class DailyTemperatures {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }

        return result;
    }
}
```