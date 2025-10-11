import java.util.*;

/*
Question: Given an array of strings, find the shortest string that contains all the strings in the array as substrings. This is known as the shortest superstring problem.
Difficulty: Hard
*/
class FindTheShortestSuperstring {
    public String shortestSuperstring(String[] words) {
        int n = words.length;
        int[][] overlap = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i == j) continue;
                int k = 0;
                while (k <= Math.min(words[i].length(), words[j].length())) {
                    if (words[i].endsWith(words[j].substring(0, k))) {
                        overlap[i][j] = k;
                    }
                    k++;
                }
            }
        }

        int[][] dp = new int[1 << n][n];
        int[][] p = new int[1 << n][n];
        Arrays.stream(dp).forEach(a -> Arrays.fill(a, Integer.MAX_VALUE));

        for (int i = 0; i < n; i++) {
            dp[1 << i][i] = words[i].length();
        }

        for (int mask = 1; mask < (1 << n); mask++) {
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) == 0) continue;
                for (int j = 0; j < n; j++) {
                    if ((mask & (1 << j)) != 0 || i == j) continue;
                    if (dp[mask][i] + words[j].length() - overlap[i][j] < dp[mask | (1 << j)][j]) {
                        dp[mask | (1 << j)][j] = dp[mask][i] + words[j].length() - overlap[i][j];
                        p[mask | (1 << j)][j] = i;
                    }
                }
            }
        }

        int minLen = Integer.MAX_VALUE;
        int minIdx = -1;
        for (int i = 0; i < n; i++) {
            if (dp[(1 << n) - 1][i] < minLen) {
                minLen = dp[(1 << n) - 1][i];
                minIdx = i;
            }
        }

        StringBuilder sb = new StringBuilder();
        int mask = (1 << n) - 1;
        int curr = minIdx;
        while (mask > 0) {
            int prev = p[mask][curr];
            sb.insert(0, words[curr].substring(overlap[prev][curr]));
            mask ^= (1 << curr);
            curr = prev;
        }
        return sb.toString();

    }
}