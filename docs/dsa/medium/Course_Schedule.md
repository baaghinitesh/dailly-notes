# Problem: Course Schedule

## Summary of Approach

The Course Schedule problem determines if it's possible to finish all courses given a set of prerequisites.  The approach typically involves using topological sort.  We build a directed graph where nodes represent courses and edges represent prerequisites (A -> B means course B requires course A).  Then, we perform a topological sort using either Kahn's algorithm or Depth-First Search (DFS).

Kahn's algorithm iteratively removes nodes with no incoming edges, adding them to the result. If a cycle is detected (no nodes with zero in-degree exist before all nodes are processed), it's impossible to finish all courses.

DFS recursively explores the graph, marking nodes as visited and recursively processing their neighbors.  If a visited node is encountered again during recursion (a cycle), it's impossible to finish all courses.  The order of finishing nodes (in post-order traversal for DFS) represents a topological ordering if no cycle is detected.


## Time and Space Complexity

- Time: O(V + E) where V is the number of courses (vertices) and E is the number of prerequisites (edges).  Both Kahn's algorithm and DFS have this time complexity.  Building the graph itself is also O(V + E).

- Space: O(V + E)  This is dominated by the space used to represent the graph (adjacency list or adjacency matrix) and the recursion stack for DFS or the queue for Kahn's algorithm.  In the worst-case scenario (a fully connected graph), E could be O(V²), but it's usually smaller in real-world scenarios.

## Java Solution
```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/*
 * Question: Course Schedule (Medium)
 * Given the number of courses and a list of prerequisites, determine if it is possible to finish all courses.
 * There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
 * You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
 * For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
 * Return true if you can finish all courses. Otherwise, return false.
 */
class CourseSchedule {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        Map<Integer, List<Integer>> adj = new HashMap<>();
        int[] inDegree = new int[numCourses];

        for (int[] pre : prerequisites) {
            adj.computeIfAbsent(pre[1], k -> new ArrayList<>()).add(pre[0]);
            inDegree[pre[0]]++;
        }

        List<Integer> queue = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.add(i);
            }
        }

        int count = 0;
        while (!queue.isEmpty()) {
            int course = queue.remove(0);
            count++;
            if (adj.containsKey(course)) {
                for (int neighbor : adj.get(course)) {
                    inDegree[neighbor]--;
                    if (inDegree[neighbor] == 0) {
                        queue.add(neighbor);
                    }
                }
            }
        }

        return count == numCourses;
    }
}
```