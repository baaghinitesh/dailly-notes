---
title: "Maximum Depth of Binary Tree"
language: "javascript"
difficulty: "easy"
section: "dsa"
tags: "dsa, javascript, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/10/1200/630"
update_count: 0
---

# Maximum Depth of Binary Tree

## Problem Understanding
The problem is asking to find the maximum depth of a binary tree, which is the number of nodes along the longest path from the root node down to the farthest leaf node. The key constraint is that we are dealing with a binary tree, where each node has at most two children (left and right). What makes this problem non-trivial is that we need to traverse the tree in a way that ensures we find the longest path, which requires a systematic approach to avoid missing any nodes or paths. The naive approach of simply counting the number of nodes or edges would not work because it does not take into account the structure of the tree.

## Approach
The algorithm strategy is to use a recursive depth-first search (DFS) to traverse the tree and find the maximum depth. The intuition behind this approach is that we can break down the problem of finding the maximum depth of the tree into smaller sub-problems of finding the maximum depth of the left and right subtrees. We use a recursive function to traverse the tree, and at each node, we return 1 plus the maximum depth of the left and right subtrees. This approach works because it ensures that we visit each node exactly once and consider all possible paths from the root to the leaves. We use a recursive call stack to keep track of the nodes to visit, which allows us to efficiently traverse the tree.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We visit each node exactly once, where n is the number of nodes in the tree. The time complexity is linear because we perform a constant amount of work at each node. |
| Space  | O(h)  | The space complexity is proportional to the height of the tree, where h is the height of the tree. This is because we use a recursive call stack to keep track of the nodes to visit, and the maximum depth of the call stack is equal to the height of the tree. In the worst case, the tree is completely unbalanced, and the height of the tree is equal to the number of nodes, resulting in a space complexity of O(n). |

## Algorithm Walkthrough
```
Input: 
     3
   /   \
  9   20
     /  \
    15   7

Step 1: maxDepth(3) = 1 + max(maxDepth(9), maxDepth(20))
Step 2: maxDepth(9) = 1 (because 9 is a leaf node)
Step 3: maxDepth(20) = 1 + max(maxDepth(15), maxDepth(7))
Step 4: maxDepth(15) = 1 (because 15 is a leaf node)
Step 5: maxDepth(7) = 1 (because 7 is a leaf node)
Step 6: maxDepth(20) = 1 + max(1, 1) = 2
Step 7: maxDepth(3) = 1 + max(1, 2) = 3

Output: 3
```
This example illustrates how the algorithm recursively traverses the tree and calculates the maximum depth.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is node null?"}
    B -->|Yes| C[Return 0]
    B -->|No| D[Calculate depth of left subtree]
    D --> E[Calculate depth of right subtree]
    E --> F["Return 1 + max("left depth, right depth")"]
```
This flowchart illustrates the decision flow of the algorithm, where we recursively calculate the depth of the left and right subtrees and return the maximum depth.

## Key Insight
> **Tip:** The key insight is to realize that the maximum depth of a tree can be calculated by recursively finding the maximum depth of the left and right subtrees and adding 1 to account for the current node.

## Edge Cases
- **Empty/null input**: If the input tree is empty (i.e., null), the algorithm returns 0, which is the correct result because an empty tree has no nodes.
- **Single element**: If the input tree has only one node, the algorithm returns 1, which is the correct result because a tree with one node has a depth of 1.
- **Unbalanced tree**: If the input tree is unbalanced (i.e., one subtree is much deeper than the other), the algorithm still returns the correct result because it recursively calculates the depth of each subtree and returns the maximum depth.

## Common Mistakes
- **Mistake 1**: Forgetting to handle the base case where the input tree is empty. To avoid this, always check for null input and return 0 in this case.
- **Mistake 2**: Not using recursion to calculate the depth of the left and right subtrees. To avoid this, use a recursive function to traverse the tree and calculate the depth of each subtree.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly because it does not rely on the input being sorted. The time complexity remains O(n), and the space complexity remains O(h).
- "Can you do it in O(1) space?" → No, it is not possible to calculate the maximum depth of a binary tree in O(1) space because we need to use a recursive call stack to keep track of the nodes to visit.
- "What if there are duplicates?" → The algorithm still works correctly because it does not rely on the uniqueness of the node values. The time complexity remains O(n), and the space complexity remains O(h).

## Javascript Solution

```javascript
// Problem: Maximum Depth of Binary Tree
// Language: javascript
// Difficulty: Easy
// Time Complexity: O(n) — visiting each node once in the worst case
// Space Complexity: O(h) — where h is the height of the tree, due to recursive call stack
// Approach: Recursive depth-first search — traversing the tree to find the maximum depth

/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {number}
 */
var maxDepth = function(root) {
    // Base case: if the tree is empty, return 0
    if (root === null) return 0; // Edge case: empty tree → return 0
    
    // Recursive case: return 1 plus the maximum depth of the left and right subtrees
    // We add 1 to account for the current node
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right)); // Recursively calculate the depth of each subtree
};
```
