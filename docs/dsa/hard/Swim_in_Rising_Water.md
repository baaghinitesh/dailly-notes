# Problem: Swim in Rising Water

## Summary of Approach

The "Swim in Rising Water" problem asks to find the shortest time it takes for water to reach a destination cell (target) from a source cell (usually the top-left corner) in a grid, given that water rises at a constant rate.  The grid contains elevation values.  This problem can be efficiently solved using a priority queue (like a min-heap) and Dijkstra's algorithm.

The algorithm works as follows:

1. **Initialization:** Create a min-heap priority queue containing the starting cell's coordinates and its elevation.  Initialize a distance array to track the minimum time to reach each cell (initialized to infinity for all cells except the starting cell, which is its elevation).

2. **Iteration:** While the priority queue is not empty:
    - Pop the cell with the minimum elevation (and thus minimum time to reach) from the priority queue.
    - If this cell is the target cell, return its minimum time.
    - Explore its neighbors (up, down, left, right). For each neighbor:
        - Calculate the maximum of the current cell's time and the neighbor's elevation (this represents the time needed to reach the neighbor).
        - If this time is less than the current minimum time to reach that neighbor, update the minimum time and add the neighbor to the priority queue.

3. **Result:** If the target cell is reached, the algorithm returns the minimum time; otherwise, there's no path to the target.


## Time and Space Complexity
- Time: O(N log N), where N is the number of cells in the grid. This is because in the worst case, we might need to process all cells, and each processing step involves a heap operation (log N).
- Space: O(N). This is primarily due to the priority queue and the distance array, both of which can store up to N elements in the worst case.

## Java Solution
```java
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
```