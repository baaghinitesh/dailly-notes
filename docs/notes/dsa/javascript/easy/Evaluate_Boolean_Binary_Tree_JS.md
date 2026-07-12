---
title: "Evaluate Boolean Binary Tree JS"
language: "javascript"
difficulty: "easy"
section: "dsa"
tags: "dsa, javascript, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/694/1200/630"
update_count: 0
---

# Evaluate Boolean Binary Tree JS

## Problem Understanding
The problem is asking to evaluate a Boolean binary tree where each node represents a Boolean value (0 or 1) or a Boolean operator (2 for OR, 3 for AND). The key constraint is that the tree must be evaluated recursively, and the implication of this is that the solution must handle the tree's height and potential null values. What makes this problem non-trivial is that a naive approach might not handle the recursive nature of the tree correctly, leading to incorrect evaluations or stack overflow errors.

## Approach
The algorithm strategy is to use recursive tree traversal to evaluate each node based on its operator and children. The intuition behind this is that the tree can be broken down into smaller sub-problems, each of which can be solved recursively. The approach works by first checking if the tree is empty or if the current node is a leaf node, in which case it returns the node's value. Then, it recursively evaluates the left and right subtrees and combines the results based on the current node's operator. The data structure used is a binary tree, which is chosen because it naturally represents the problem's structure.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm visits each node in the tree exactly once, where n is the number of nodes in the tree. The recursive calls do not overlap, so the time complexity is linear. |
| Space  | O(h)  | The space complexity is determined by the maximum depth of the recursive call stack, which is equal to the height of the tree (h). In the worst case, the tree is skewed, and the height is equal to the number of nodes (n), resulting in a space complexity of O(n). However, for a balanced tree, the height is logarithmic in the number of nodes (h = log n), resulting in a space complexity of O(log n). |

## Algorithm Walkthrough
```
Input: 
       2
      / \
     1   3
        / \
       0   1
Step 1: Evaluate the root node (2)
  - Left child: 1 (leaf node) → return 1
  - Right child: 3 (operator node)
    - Evaluate left child of 3: 0 (leaf node) → return 0
    - Evaluate right child of 3: 1 (leaf node) → return 1
    - Combine results: 0 && 1 → return 0
Step 2: Combine results of root node (2)
  - Left child: 1
  - Right child: 0
  - Combine results: 1 || 0 → return 1
Output: true
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is node null?"}
    B -->|Yes| C[Return false]
    B -->|No| D{"Is node a leaf node?"}
    D -->|Yes| E[Return node value]
    D -->|No| F[Recursively evaluate left child]
    F --> G[Recursively evaluate right child]
    G --> H{"Is node an OR operator?"}
    H -->|Yes| I[Return left || right]
    H -->|No| J["Return left && right"]
```

## Key Insight
> **Tip:** The key to solving this problem is to recognize that the tree can be evaluated recursively, and that each node's value can be determined based on its operator and children.

## Edge Cases
- **Empty/null input**: If the input tree is null, the function returns false.
- **Single element**: If the input tree has only one node, the function returns the node's value.
- **Tree with only one child**: If the input tree has nodes with only one child, the function will still work correctly, as it checks for the existence of both children before evaluating them.

## Common Mistakes
- **Mistake 1**: Not handling the base case of an empty tree correctly → to avoid this, make sure to check for null nodes at the beginning of the function.
- **Mistake 2**: Not combining the results of the recursive calls correctly → to avoid this, make sure to use the correct operator (OR or AND) based on the node's value.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not assume any specific ordering of the input tree, so it will still work correctly even if the tree is sorted.
- "Can you do it in O(1) space?" → No, the algorithm uses recursive calls, which require O(h) space, where h is the height of the tree. It is not possible to evaluate the tree in O(1) space.
- "What if there are duplicates?" → The algorithm does not assume that the input tree has unique values, so it will still work correctly even if there are duplicates.

## Javascript Solution

```javascript
// Problem: Evaluate Boolean Binary Tree
// Language: javascript
// Difficulty: Easy
// Time Complexity: O(n) — recursive traversal of the tree
// Space Complexity: O(h) — recursive call stack, where h is the height of the tree
// Approach: Recursive tree traversal — evaluate each node based on its operator and children

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
 * @return {boolean}
 */
var evaluateTree = function(root) {
    // Base case: if the tree is empty, return false
    if (!root) return false; // Edge case: empty tree → return false
    
    // If the node is a leaf node, return its value
    if (!root.left && !root.right) return root.val === 1; // leaf node → return its value
    
    // Recursively evaluate the left and right subtrees
    let leftVal = evaluateTree(root.left); // evaluate left subtree
    let rightVal = evaluateTree(root.right); // evaluate right subtree
    
    // Evaluate the current node based on its operator and children
    if (root.val === 2) return leftVal || rightVal; // OR operator
    else if (root.val === 3) return leftVal && rightVal; // AND operator
};

// Example usage:
// Create a sample binary tree:
//       2
//      / \
//     1   3
//        / \
//       0   1
let root = {
    val: 2,
    left: {
        val: 1,
        left: null,
        right: null
    },
    right: {
        val: 3,
        left: {
            val: 0,
            left: null,
            right: null
        },
        right: {
            val: 1,
            left: null,
            right: null
        }
    }
};

console.log(evaluateTree(root)); // Output: true
```
