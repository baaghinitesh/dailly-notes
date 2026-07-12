---
title: "Maximum Binary Tree"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/149/1200/630"
update_count: 0
---

# Maximum Binary Tree

## Problem Understanding
The problem is asking to construct a maximum binary tree from a given array of integers. The maximum binary tree is a binary tree where each node has a value greater than or equal to its children. The key constraint is that the tree must be constructed recursively, and the algorithm should handle edge cases such as empty input, single element, and duplicate values. The problem is non-trivial because a naive approach would require iterating through the array multiple times to construct the tree, resulting in a high time complexity.

## Approach
The algorithm strategy is to recursively construct the binary tree by finding the maximum value in the array and partitioning the array around it. This approach works because the maximum value in the array will be the root of the tree, and the values to its left and right will be the left and right subtrees, respectively. The algorithm uses a recursive function to construct the tree, and a helper function to get subarrays from the original array. The approach handles key constraints such as empty input and single element by returning null or a single node tree, respectively.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the array once to find the maximum value, and then recursively constructs the left and right subtrees. The recursive calls have a time complexity of O(n) because each node is visited once. The overall time complexity is O(n) because the recursive calls are made in a divide-and-conquer manner. |
| Space  | O(n)  | The algorithm uses a recursive call stack to construct the tree, which has a space complexity of O(n) because each recursive call adds a layer to the call stack. The algorithm also uses a helper function to get subarrays from the original array, which has a space complexity of O(n) because a new subarray is created in each recursive call. |

## Algorithm Walkthrough
```
Input: [3, 2, 1, 6, 0, 5]
Step 1: Find the maximum value (6) and its index (3) in the array
Step 2: Create a new tree node with the maximum value (6)
Step 3: Recursively construct the left subtree with the subarray [3, 2, 1]
    Step 3.1: Find the maximum value (3) and its index (0) in the subarray
    Step 3.2: Create a new tree node with the maximum value (3)
    Step 3.3: Recursively construct the left subtree with the subarray [2, 1]
        Step 3.3.1: Find the maximum value (2) and its index (0) in the subarray
        Step 3.3.2: Create a new tree node with the maximum value (2)
        Step 3.3.3: Recursively construct the left subtree with the subarray [1]
            Step 3.3.3.1: Create a new tree node with the value (1)
    Step 3.4: Recursively construct the right subtree with the subarray []
Step 4: Recursively construct the right subtree with the subarray [0, 5]
    Step 4.1: Find the maximum value (5) and its index (1) in the subarray
    Step 4.2: Create a new tree node with the maximum value (5)
    Step 4.3: Recursively construct the left subtree with the subarray [0]
        Step 4.3.1: Create a new tree node with the value (0)
    Step 4.4: Recursively construct the right subtree with the subarray []
Output: A maximum binary tree with the root node (6) and left and right subtrees
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Find Maximum Value]
    B --> C{"Is Maximum Value Found?"}
    C -->|Yes| D[Create Tree Node]
    D --> E[Recursively Construct Left Subtree]
    E --> F[Recursively Construct Right Subtree]
    F --> G[Return Tree Node]
    C -->|No| H[Return Null]
    subgraph Recursively Construct Left Subtree
        E --> E1[Find Maximum Value in Left Subarray]
        E1 --> E2{"Is Maximum Value Found in Left Subarray?"}
        E2 -->|Yes| E3[Create Tree Node for Left Subtree]
        E2 -->|No| E4[Return Null]
    subgraph Recursively Construct Right Subtree
        F --> F1[Find Maximum Value in Right Subarray]
        F1 --> F2{"Is Maximum Value Found in Right Subarray?"}
        F2 -->|Yes| F3[Create Tree Node for Right Subtree]
        F2 -->|No| F4[Return Null]
```

## Key Insight
> **Tip:** The key insight to solving this problem is to find the maximum value in the array and partition the array around it to recursively construct the left and right subtrees.

## Edge Cases
- **Empty/null input**: If the input array is empty or null, the algorithm returns null.
- **Single element**: If the input array has only one element, the algorithm returns a tree with a single node containing that element.
- **Duplicate values**: If the input array has duplicate values, the algorithm will construct a tree with the maximum value as the root node, and the duplicate values will be partitioned into the left and right subtrees.

## Common Mistakes
- **Mistake 1**: Not handling the edge case of empty input. → To avoid this, add a check for null or empty input at the beginning of the algorithm.
- **Mistake 2**: Not recursively constructing the left and right subtrees. → To avoid this, make sure to call the recursive function for both the left and right subtrees.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, but the time complexity may be improved by using a modified algorithm that takes advantage of the sorted input.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n) space to store the recursive call stack and the tree nodes.
- "What if there are duplicates?" → The algorithm will construct a tree with the maximum value as the root node, and the duplicate values will be partitioned into the left and right subtrees.

## Java Solution

```java
// Problem: Maximum Binary Tree
// Language: Java
// Difficulty: Medium
// Time Complexity: O(n) — recursive construction of binary tree
// Space Complexity: O(n) — recursive call stack and tree nodes
// Approach: Recursive tree construction — find maximum value and partition array accordingly

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
    public TreeNode constructMaximumBinaryTree(int[] nums) {
        // Edge case: empty input → return null
        if (nums == null || nums.length == 0) {
            return null;
        }
        
        // Find the maximum value and its index in the array
        int maxIndex = 0;
        for (int i = 1; i < nums.length; i++) {
            // Check if current value is greater than the max value found so far
            if (nums[i] > nums[maxIndex]) {
                maxIndex = i;
            }
        }
        
        // Create a new tree node with the maximum value
        TreeNode root = new TreeNode(nums[maxIndex]);
        
        // Recursively construct the left and right subtrees
        // by partitioning the array around the maximum value
        int[] leftSubarray = getSubarray(nums, 0, maxIndex);
        int[] rightSubarray = getSubarray(nums, maxIndex + 1, nums.length);
        
        // Edge case: empty subarray → return null
        if (leftSubarray != null) {
            // Recursively construct the left subtree
            root.left = constructMaximumBinaryTree(leftSubarray);
        }
        
        // Edge case: empty subarray → return null
        if (rightSubarray != null) {
            // Recursively construct the right subtree
            root.right = constructMaximumBinaryTree(rightSubarray);
        }
        
        return root;
    }
    
    // Helper function to get a subarray from the original array
    private int[] getSubarray(int[] nums, int start, int end) {
        // Edge case: empty subarray → return null
        if (start >= end) {
            return null;
        }
        
        // Create a new subarray
        int[] subarray = new int[end - start];
        System.arraycopy(nums, start, subarray, 0, end - start);
        return subarray;
    }
}
```
