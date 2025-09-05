import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/*
Given an array of scores, return a new array where each element is the relative rank of the corresponding score.
For example:
scores = [10, 3, 8, 9, 4]
ranks = ["4", "5", "2", "1", "3"]
Medium
*/
class RelativeRanks {
    public String[] findRelativeRanks(int[] score) {
        int n = score.length;
        int[][] scoreWithIndex = new int[n][2];
        for (int i = 0; i < n; i++) {
            scoreWithIndex[i][0] = score[i];
            scoreWithIndex[i][1] = i;
        }
        Arrays.sort(scoreWithIndex, (a, b) -> b[0] - a[0]);
        String[] ranks = new String[n];
        for (int i = 0; i < n; i++) {
            if (i == 0) {
                ranks[scoreWithIndex[i][1]] = "Gold Medal";
            } else if (i == 1) {
                ranks[scoreWithIndex[i][1]] = "Silver Medal";
            } else if (i == 2) {
                ranks[scoreWithIndex[i][1]] = "Bronze Medal";
            } else {
                ranks[scoreWithIndex[i][1]] = String.valueOf(i + 1);
            }
        }
        return ranks;
    }
}