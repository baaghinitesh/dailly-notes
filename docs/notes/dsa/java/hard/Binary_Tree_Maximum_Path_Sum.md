---
title: "Binary Tree Maximum Path Sum"
language: "java"
difficulty: "hard"
section: "dsa"
tags: "dsa, java, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/555/1200/630"
update_count: 0
---

# Binary Tree Maximum Path Sum

## Problem Understanding
The Binary Tree Maximum Path Sum problem asks us to find the maximum path sum in a binary tree, where a path can be any sequence of nodes from a starting node to any node in the tree. The key constraint is that the path must be a connected sequence of nodes, and each node can only be visited once. What makes this problem non-trivial is that a naive approach, such as simply summing all node values, would not account for the possibility that a path may not include all nodes in the tree. Furthermore, the problem requires us to consider all possible paths in the tree, not just those that start at the root or end at a leaf node.

## Approach
The approach used to solve this problem is a Depth-First Search (DFS) with a recursive helper function, specifically designed to calculate the maximum path sum. The algorithm works by recursively exploring all possible paths in the tree, keeping track of the maximum path sum found so far. The recursive helper function `maxGain` calculates the maximum path sum for each node, considering the maximum gain from the left and right subtrees. The `maxPathSum` variable is updated whenever a new maximum path sum is found. This approach works because it considers all possible paths in the tree and ensures that each node is visited only once.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm visits each node in the tree exactly once, resulting in a linear time complexity. The recursive function calls are made for each node, but each node is only visited once. |
| Space  | O(h)  | The space complexity is determined by the maximum recursion depth, which is equal to the height of the tree. In the worst case, the tree is completely unbalanced, and the recursion depth is equal to the number of nodes in the tree. However, for a balanced binary tree, the height is logarithmic in the number of nodes. |

## Algorithm Walkthrough
```
Input: 
     1
    / \
   2   3

Step 1: maxGain(1)
  - leftGain = maxGain(2) = 2
  - rightGain = maxGain(3) = 3
  - maxPathSum = max(maxPathSum, 1 + 2 + 3) = 6
  - return 1 + max(2, 3) = 4

Step 2: maxGain(2)
  - leftGain = maxGain(null) = 0
  - rightGain = maxGain(null) = 0
  - maxPathSum = max(maxPathSum, 2 + 0 + 0) = 2
  - return 2 + max(0, 0) = 2

Step 3: maxGain(3)
  - leftGain = maxGain(null) = 0
  - rightGain = maxGain(null) = 0
  - maxPathSum = max(maxPathSum, 3 + 0 + 0) = 3
  - return 3 + max(0, 0) = 3

Output: 6
```
This example demonstrates the algorithm's ability to find the maximum path sum in a binary tree.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is node null?"}
    B -->|Yes| C[Return 0]
    B -->|No| D[Calculate leftGain and rightGain]
    D --> E{"Update maxPathSum?"}
    E -->|Yes| F[Update maxPathSum]
    E -->|No| G["Return node.val + max("leftGain, rightGain")"]
    F --> G
```
This flowchart illustrates the algorithm's decision flow and data transformation.

## Key Insight
> **Tip:** The key insight is to consider the maximum gain from the left and right subtrees for each node, and update the maximum path sum accordingly.

## Edge Cases
- **Empty/null input**: If the input tree is null, the algorithm returns 0, as there are no nodes to consider.
- **Single element**: If the input tree has only one node, the algorithm returns the value of that node, as it is the only possible path sum.
- **Unbalanced tree**: If the input tree is highly unbalanced, the algorithm's recursion depth may be large, resulting in increased space complexity.

## Common Mistakes
- **Mistake 1**: Not considering the case where a node's value is negative, which can affect the maximum path sum. To avoid this, ensure that the `maxGain` function returns the maximum of the current node's value and 0.
- **Mistake 2**: Not updating the `maxPathSum` variable correctly. To avoid this, ensure that the `maxPathSum` is updated with the maximum of its current value and the current path sum.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, as it considers all possible paths in the tree, regardless of the node values.
- "Can you do it in O(1) space?" → No, the algorithm requires O(h) space due to the recursive function calls, where h is the height of the tree.
- "What if there are duplicates?" → The algorithm still works correctly, as it considers all possible paths in the tree and returns the maximum path sum.

## Java Solution

```java
// Problem: Binary Tree Maximum Path Sum
// Language: Java
// Difficulty: Hard
// Time Complexity: O(n) — single pass through the tree, visiting each node once
// Space Complexity: O(h) — maximum recursion depth, where h is the height of the tree
// Approach: Depth-First Search with recursive helper function — to calculate the maximum path sum

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
    private int maxPathSum = Integer.MIN_VALUE; // Initialize maxPathSum as negative infinity

    public int maxPathSum(TreeNode root) {
        // Base case: if the tree is empty, return 0
        if (root == null) return 0;

        // Recursive helper function to calculate the maximum path sum
        maxGain(root); // Start the recursion from the root node

        // Return the maximum path sum found
        return maxPathSum;
    }

    // Recursive helper function to calculate the maximum path sum
    private int maxGain(TreeNode node) {
        // Base case: if the node is null, return 0
        if (node == null) return 0;

        // Recursively calculate the maximum path sum for the left and right subtrees
        int leftGain = Math.max(maxGain(node.left), 0); // leftGain should be non-negative
        int rightGain = Math.max(maxGain(node.right), 0); // rightGain should be non-negative

        // Update maxPathSum if the current path sum is greater
        maxPathSum = Math.max(maxPathSum, node.val + leftGain + rightGain); // Update maxPathSum

        // Return the maximum path sum for the current node
        return node.val + Math.max(leftGain, rightGain); // Return the maximum gain
    }
}
```
