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