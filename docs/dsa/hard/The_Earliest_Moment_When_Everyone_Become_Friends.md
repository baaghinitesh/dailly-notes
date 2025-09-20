# Problem: The Earliest Moment When Everyone Become Friends

## Summary of Approach

The problem "The Earliest Moment When Everyone Become Friends" seeks to find the earliest time at which a group of people all become connected, given a series of friendships that form over time.  The approach typically involves using a Union-Find data structure.

The algorithm iterates through the friendships, ordered by time. For each friendship, it uses the Union-Find data structure to check if the two individuals belong to the same set (connected component). If they are not, it unites their sets, effectively connecting them.  After each friendship is processed, it checks if only one set (connected component) remains; if so, all individuals are connected, and this timestamp is the earliest moment everyone became friends. If the friendships are unordered, it would involve sorting them first.


## Time and Space Complexity
- Time: O(E log E + Eα(E,N)) or O(E log E) if sorting is the dominant operation, where E is the number of friendships (edges) and N is the number of people (nodes).  α(E,N) is the inverse Ackermann function, which grows incredibly slowly and can be considered a constant for all practical purposes. O(E log E) dominates because sorting takes longer than Union-Find operations. If the friendships are already sorted, the Time complexity becomes O(Eα(E,N)) which can be approximated to O(E)
- Space: O(N) to store the Union-Find data structure (parent array or similar).  The space required to store the friendships themselves is not usually factored into the space complexity analysis, unless it is exceptionally large compared to the number of people.

## Java Solution
```java
import java.util.*;

/*
You are given an integer n, the number of people in a circle. The people are numbered from 1 to n.
You are also given a 2D integer array logs, where logs[i] = [timestamp, personA, personB] indicates that personA and personB became friends at timestamp timestamp. Each timestamp is unique.
Initially, no one is friends with anyone.
Return the earliest moment when everyone became friends.

Difficulty: Medium
*/
class TheEarliestMomentWhenEveryoneBecomeFriends {
    public int earliestAcq(int n, int[][] logs) {
        Arrays.sort(logs, (a, b) -> a[0] - b[0]);
        UnionFind uf = new UnionFind(n);
        for (int[] log : logs) {
            int time = log[0];
            int personA = log[1];
            int personB = log[2];
            if (uf.union(personA, personB)) {
                if (uf.count == 1) {
                    return time;
                }
            }
        }
        return -1;
    }

    private class UnionFind {
        int[] parent;
        int[] rank;
        int count;

        UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            count = n;
            for (int i = 0; i < n; i++) {
                parent[i] = i;
            }
        }

        int find(int i) {
            if (parent[i] == i) {
                return i;
            }
            return parent[i] = find(parent[i]);
        }

        boolean union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI != rootJ) {
                if (rank[rootI] < rank[rootJ]) {
                    parent[rootI] = rootJ;
                } else if (rank[rootI] > rank[rootJ]) {
                    parent[rootJ] = rootI;
                } else {
                    parent[rootJ] = rootI;
                    rank[rootI]++;
                }
                count--;
                return true;
            }
            return false;
        }
    }
}
```