# Problem: Shortest Path in a Grid with Obstacles Elimination

## Summary of Approach

The "Shortest Path in a Grid with Obstacles Elimination" problem involves finding the shortest path from a starting point to an ending point in a grid, where some cells are obstacles.  A crucial element is the ability to eliminate a limited number of obstacles along the path.  Several approaches can solve this, but a common and efficient one uses a variation of Dijkstra's algorithm or a Breadth-First Search (BFS).

The algorithm maintains a priority queue (for Dijkstra's) or a queue (for BFS) of states. Each state represents a position in the grid and the number of obstacles already eliminated.  The algorithm explores the grid cell-by-cell, considering moving to adjacent cells. If a cell is an obstacle, it can be eliminated if the remaining obstacle elimination count allows it.  The algorithm continues until the ending point is reached. The priority queue (Dijkstra's) uses a heuristic (like Manhattan distance) to prioritize cells closer to the destination, guaranteeing the shortest path is found first.  BFS explores level by level, finding the shortest path in unweighted graphs.  The key is tracking both the position and the remaining obstacles allowed to be removed.


## Time and Space Complexity
- Time: O(N*M*K*log(N*M*K))  where N and M are the dimensions of the grid, and K is the maximum number of obstacles allowed to be eliminated.  The log factor comes from using a priority queue in Dijkstra's algorithm.  For BFS, if we don't use a heuristic, it becomes O(N*M*K).
- Space: O(N*M*K)  The space complexity is dominated by the priority queue or queue which stores all possible states (each position in the grid combined with the remaining obstacles).  In the worst case, all cells and all obstacle removal counts need to be stored.

## Java Solution
```java
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
```