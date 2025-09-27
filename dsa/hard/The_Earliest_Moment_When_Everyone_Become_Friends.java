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