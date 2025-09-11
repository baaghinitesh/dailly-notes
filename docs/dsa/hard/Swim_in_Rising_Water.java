// You are given an n x n integer matrix grid where grid[i][j] represents the height of cell (i, j).
//
// We are initially at cell (0, 0), and we want to reach cell (n - 1, n - 1). Every cell has a cost, which is its height.
//
// We can move in four directions: up, down, left, or right.
//
// We are given an integer k. We want to find the minimum k such that we can reach the cell (n - 1, n - 1).
//
// Difficulty: Hard
class SwimInRisingWater {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        int left = 0, right = n * n - 1;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (canReach(grid, mid, n)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    private boolean canReach(int[][] grid, int threshold, int n) {
        boolean[][] visited = new boolean[n][n];
        int[] dx = {0, 0, 1, -1};
        int[] dy = {1, -1, 0, 0};
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});
        visited[0][0] = true;
        while (!queue.isEmpty()) {
            int[] curr = queue.poll();
            int x = curr[0];
            int y = curr[1];
            if (x == n - 1 && y == n - 1) {
                return true;
            }
            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i];
                int ny = y + dy[i];
                if (nx >= 0 && nx < n && ny >= 0 && ny < n && !visited[nx][ny] && grid[nx][ny] <= threshold) {
                    queue.offer(new int[]{nx, ny});
                    visited[nx][ny] = true;
                }
            }
        }
        return false;
    }
}