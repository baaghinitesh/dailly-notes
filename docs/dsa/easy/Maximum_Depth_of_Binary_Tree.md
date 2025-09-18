# Problem: Maximum Depth of Binary Tree

## Summary of Approach

The Maximum Depth of Binary Tree problem aims to find the maximum depth (height) of a given binary tree.  The approach uses Depth-First Search (DFS), specifically a recursive solution.  The function recursively explores the left and right subtrees of each node.  For each node, the depth is calculated as 1 plus the maximum depth of its left and right subtrees. The base case is an empty tree (null node), which has a depth of 0.  The maximum depth across all paths from the root to the leaves is then returned.  Iterative solutions using a stack or queue are also possible, but the recursive solution is often considered more concise and easier to understand.

## Time and Space Complexity
- Time: O(N) where N is the number of nodes in the binary tree.  This is because each node is visited exactly once.
- Space: O(H) where H is the height of the binary tree. In the worst case (a skewed tree), H can be equal to N, resulting in O(N) space complexity.  This space is used for the recursive call stack.  For a balanced tree, H would be log₂(N), leading to O(log₂(N)) space complexity.

## Java Solution
```java
/**
 * Given the root of a binary tree, return its maximum depth.
 * A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
 * Difficulty: Easy
 */
class MaximumDepthOfBinaryTree {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        } else {
            int leftDepth = maxDepth(root.left);
            int rightDepth = maxDepth(root.right);
            return Math.max(leftDepth, rightDepth) + 1;
        }
    }

    public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode() {}
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }
}
```