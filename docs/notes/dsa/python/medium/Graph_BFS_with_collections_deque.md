---
title: "Graph BFS with collections.deque"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, bfs, graph, collections"
banner: "https://image.pollinations.ai/prompt/dsa%20Graph%20BFS%20with%20collections.deque%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Graph BFS with collections.deque

![Graph BFS Python](https://image.pollinations.ai/prompt/dsa%20Graph%20BFS%20with%20collections.deque%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Use `collections.deque` as the BFS queue — `popleft()` is O(1) vs O(n) for `list.pop(0)`. Start from the source, mark visited, and process level by level. Returns shortest path distances from source.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(V + E) | Visit each vertex and edge once |
| Space  | O(V)     | Queue and visited set |

## Key Insight
> **Tip:** Always use `collections.deque` for BFS in Python, never `list`. `list.pop(0)` is O(n) because it shifts all elements; `deque.popleft()` is O(1).

## Python Solution

```python
# Problem: Graph BFS with collections.deque
# Language: Python
# Difficulty: Medium
# Time Complexity: O(V + E)
# Space Complexity: O(V)

from collections import deque, defaultdict
from typing import Dict, List

def bfs(graph: Dict[int, List[int]], start: int) -> Dict[int, int]:
    """Returns shortest distance from start to all reachable nodes."""
    dist = {start: 0}
    queue = deque([start])

    while queue:
        node = queue.popleft()  # O(1) — use deque, not list

        for neighbor in graph.get(node, []):
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

    return dist


# Example: Number of Islands (BFS variant)
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def bfs_island(r, c):
        queue = deque([(r, c)])
        visited.add((r, c))
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols \
                   and grid[nr][nc] == '1' \
                   and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs_island(r, c)
                count += 1

    return count
```
