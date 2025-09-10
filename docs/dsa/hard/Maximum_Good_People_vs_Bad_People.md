# Problem: Maximum Good People vs Bad People

## Summary of Approach

The "Maximum Good People vs Bad People" problem aims to find the maximum number of good people you can have in a group, given constraints represented by a matrix.  Each row in the matrix represents a statement made by a person, indicating whether another person is good or bad.  The goal is to find an assignment of "good" or "bad" to each person that satisfies the maximum number of these statements, without creating any contradictions (e.g., someone saying person A is good while another says person A is bad).

The most efficient approach usually involves exploring all possible assignments of "good" or "bad" to each person. This can be done systematically using bit manipulation or recursion.  For each assignment, we check the number of satisfied statements. The assignment that maximizes the satisfied statements is the solution.  Optimization techniques like memoization or dynamic programming can be applied (although they might not drastically improve the time complexity in the worst case).


## Time and Space Complexity
- Time: O(2<sup>n</sup> * m), where n is the number of people and m is the number of statements (rows in the matrix).  This is because we potentially need to iterate through all 2<sup>n</sup> possible assignments of good/bad to each person, and for each assignment, we need to check m statements.

- Space: O(n) or O(m) depending on the implementation.  O(n) space might be needed to store the current assignment of good/bad for each person. O(m) may be needed to store the statement matrix (if a copy is created). In some cases, with careful in-place operations, the space complexity might be even lower, approaching O(1). Note that recursive approaches might also incur additional space complexity due to the call stack.

## Java Solution
```java
/*
Question: Maximum Good People vs Bad People
Difficulty: Medium

You are given a 0-indexed 2D integer array statements of size n x n where statements[i][j] represents the statement made by the ith person about the jth person.
statements[i][j] = 0 represents that the ith person thinks the jth person is bad.
statements[i][j] = 1 represents that the ith person thinks the jth person is good.
statements[i][j] = 2 represents that the ith person does not know whether the jth person is good or bad.

Return the maximum number of people who can be good.


Example 1:
Input: statements = [[2,1,2],[1,2,2],[2,0,1]]
Output: 2
Explanation:
- Person 0 thinks person 1 is good and person 2 is bad.
- Person 1 thinks person 0 is good and person 2 is bad.
- Person 2 thinks person 1 is good.

Let's assume person 1 is good. Then person 0 is good, and person 2 is bad.
Let's assume person 1 is bad. Then person 0 is bad, and person 2 is good.
The maximum number of good people is 2.

Example 2:
Input: statements = [[1,1,1],[1,1,1],[1,1,1]]
Output: 3
Explanation: All people can be good.


Constraints:
n == statements.length == statements[i].length
1 <= n <= 15
statements[i][j] is either 0, 1, or 2.
*/
class MaximumGoodPeopleVsBadPeople {
    public int maximumGood(int[][] statements) {
        int n = statements.length;
        int maxGood = 0;
        for (int i = 0; i < (1 << n); ++i) {
            int goodCount = 0;
            boolean possible = true;
            boolean[] good = new boolean[n];
            for (int j = 0; j < n; ++j) {
                if ((i >> j) % 2 == 1) {
                    good[j] = true;
                    goodCount++;
                }
            }

            for (int j = 0; j < n; ++j) {
                for (int k = 0; k < n; ++k) {
                    if (statements[j][k] != 2) {
                        boolean isGood = good[k];
                        boolean statement = statements[j][k] == 1;
                        if (good[j] && isGood != statement) {
                            possible = false;
                            break;
                        }
                    }
                }
                if (!possible) break;
            }
            if (possible) maxGood = Math.max(maxGood, goodCount);
        }
        return maxGood;
    }
}
```