import java.util.LinkedList;
import java.util.Queue;

class ShortestPathInAGridWithObstaclesElimination {
    // Question: Given a m * n grid, where each cell is either 0 (empty) or 1 (obstacle).
    // In one step, you can move up, down, left or right.
    // You can also eliminate at most k obstacles.
    // Find the shortest path from the top left cell (0, 0) to the bottom right cell (m-1, n-1).
    // Difficulty: Hard

    public int shortestPath(int[][] grid, int k) {
        int m = grid.length;
        int n = grid[0].length;

        if (m == 0 || n == 0) return -1;

        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0, k, 0}); // {row, col, remainingObstacles, distance}

        boolean[][][] visited = new boolean[m][n][k + 1];
        visited[0][0][k] = true;

        int[][] dirs = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

        while (!queue.isEmpty()) {
            int[] curr = queue.poll();
            int row = curr[0];
            int col = curr[1];
            int obstacles = curr[2];
            int dist = curr[3];

            if (row == m - 1 && col == n - 1) return dist;

            for (int[] dir : dirs) {
                int newRow = row + dir[0];
                int newCol = col + dir[1];
                int newObstacles = obstacles;

                if (newRow >= 0 && newRow < m && newCol >= 0 && newCol < n) {
                    if (grid[newRow][newCol] == 1) {
                        if (newObstacles > 0) {
                            newObstacles--;
                        } else {
                            continue;
                        }
                    }
                    if (!visited[newRow][newCol][newObstacles]) {
                        visited[newRow][newCol][newObstacles] = true;
                        queue.offer(new int[]{newRow, newCol, newObstacles, dist + 1});
                    }
                }
            }
        }
        return -1;
    }
}