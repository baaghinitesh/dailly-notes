---
title: "Diameter of Binary Tree Simple"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/945/1200/630"
update_count: 0
---

# Diameter of Binary Tree Simple

## Problem Understanding
The problem asks us to find the diameter of a binary tree, which is the length of the longest path between any two nodes in the tree. This path may or may not pass through the root. The key constraint is that the path must be between two nodes, and we are not allowed to reuse edges. What makes this problem non-trivial is that the naive approach of calculating all possible paths and finding the longest one would result in a time complexity of O(2^n), which is inefficient for large trees. The constraint of not being able to reuse edges also means we cannot simply use a standard graph traversal algorithm.

## Approach
Our approach to solving this problem is to use a Depth-First Search (DFS) strategy, where we calculate the height of each subtree while also keeping track of the diameter. The intuition behind this approach is that the diameter of a tree is equal to the maximum diameter of its subtrees, or the sum of the heights of its left and right subtrees. We use a recursive helper function to calculate the height of each subtree, and we update the diameter whenever we find a path that is longer than the current diameter. We use a class variable `self.diameter` to keep track of the diameter, and we return the height of the current tree.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We visit each node exactly once during the DFS traversal, where n is the number of nodes in the tree. |
| Space  | O(h)  | The recursion stack can go up to a height of h, where h is the height of the tree. In the worst case, the tree is skewed and h = n, resulting in O(n) space complexity. However, for a balanced tree, h = log(n), resulting in O(log n) space complexity. |

## Algorithm Walkthrough
```
Input: 
    1
   / \
  2   3
 / \
4   5
Step 1: Initialize diameter as 0 and call the helper function to calculate the height of the tree.
Step 2: Calculate the height of the left subtree of node 1 (node 2).
    - Calculate the height of the left subtree of node 2 (node 4).
        - Return 1 (height of node 4).
    - Calculate the height of the right subtree of node 2 (node 5).
        - Return 1 (height of node 5).
    - Update the diameter: max(0, 1 + 1) = 2.
    - Return 1 + max(1, 1) = 2 (height of node 2).
Step 3: Calculate the height of the right subtree of node 1 (node 3).
    - Return 1 (height of node 3).
Step 4: Update the diameter: max(2, 2 + 1) = 3.
Step 5: Return 1 + max(2, 1) = 3 (height of node 1).
Output: 3
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Node is None?"}
    B -->|Yes| C[Return 0]
    B -->|No| D[Calculate left height]
    D --> E[Calculate right height]
    E --> F{"Update diameter?"}
    F -->|Yes| G[Update diameter]
    F -->|No| H[Return height]
    G --> H
    H --> I["Return 1 + max("left height, right height")"]
```
## Key Insight
> **Tip:** The key insight here is to realize that the diameter of a tree can be calculated while calculating the height of the tree, which reduces the time complexity from O(2^n) to O(n).

## Edge Cases
- **Empty/null input**: If the input tree is empty, the function returns 0, which is correct because the diameter of an empty tree is 0.
- **Single element**: If the input tree has only one node, the function returns 0, which is correct because the diameter of a tree with only one node is 0.
- **Unbalanced tree**: If the input tree is unbalanced, the function still works correctly and returns the correct diameter.

## Common Mistakes
- **Mistake 1**: Not updating the diameter correctly. To avoid this, make sure to update the diameter whenever a longer path is found.
- **Mistake 2**: Not handling the edge case of an empty tree correctly. To avoid this, make sure to return 0 when the input tree is empty.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, but the time complexity remains O(n) because we are still visiting each node exactly once.
- "Can you do it in O(1) space?" → No, it's not possible to do it in O(1) space because we need to use a recursion stack to calculate the height of the tree.
- "What if there are duplicates?" → The algorithm still works correctly, but the duplicates do not affect the diameter of the tree.

## Python Solution

```python
# Problem: Diameter of Binary Tree Simple
# Language: python
# Difficulty: Easy
# Time Complexity: O(n) — single pass through the tree
# Space Complexity: O(h) — recursion stack for tree height
# Approach: Depth-First Search (DFS) — calculate diameter while calculating height

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # Initialize diameter as 0
        self.diameter = 0
        
        # Define a helper function to calculate the height of a tree
        def height(node: Optional[TreeNode]) -> int:
            # Edge case: empty tree
            if not node:
                return 0
            
            # Recursively calculate the height of the left and right subtrees
            left_height = height(node.left)  # calculate height of left subtree
            right_height = height(node.right)  # calculate height of right subtree
            
            # Update the diameter if the current path is longer
            self.diameter = max(self.diameter, left_height + right_height)  # update diameter
            
            # Return the height of the current tree
            return 1 + max(left_height, right_height)  # return height of current tree
        
        # Call the helper function to calculate the height of the tree
        height(root)  # calculate height of the tree
        
        # Return the diameter
        return self.diameter  # return diameter
```
