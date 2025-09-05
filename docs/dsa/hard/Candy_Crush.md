# Problem: Candy Crush

⚠️ Error generating content: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 23
}
]

## Java Solution
```java
// Candy Crush
// Difficulty: Medium

class CandyCrush {
    public int[][] candyCrush(int[][] board) {
        int m = board.length;
        int n = board[0].length;
        boolean changed = true;

        while (changed) {
            changed = false;
            // Find and crush candies
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < n; j++) {
                    if (board[i][j] != 0) {
                        int count = 1;
                        // Check horizontally
                        int k = j + 1;
                        while (k < n && board[i][k] == board[i][j]) {
                            count++;
                            k++;
                        }
                        if (count >= 3) {
                            changed = true;
                            for (int l = j; l < j + count; l++) {
                                board[i][l] = 0;
                            }
                        }
                        //Check vertically
                        count = 1;
                        k = i + 1;
                        while (k < m && board[k][j] == board[i][j]) {
                            count++;
                            k++;
                        }
                        if (count >= 3) {
                            changed = true;
                            for (int l = i; l < i + count; l++) {
                                board[l][j] = 0;
                            }
                        }
                    }
                }
            }

            // Drop candies
            for (int j = 0; j < n; j++) {
                int emptyRow = m - 1;
                for (int i = m - 1; i >= 0; i--) {
                    if (board[i][j] != 0) {
                        board[emptyRow][j] = board[i][j];
                        if (emptyRow != i) {
                            board[i][j] = 0;
                        }
                        emptyRow--;
                    }
                }
            }
        }
        return board;
    }
}
```