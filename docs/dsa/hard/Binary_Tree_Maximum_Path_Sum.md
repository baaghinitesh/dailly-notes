# Problem: Binary Tree Maximum Path Sum

## Summary of Approach

The problem is to find the maximum sum of a path between any two nodes in a binary tree.  The path doesn't need to pass through the root.

A recursive approach is most effective. For each node, we calculate the maximum path sum that *ends* at that node. This involves considering the maximum path sum from the left subtree, the maximum path sum from the right subtree, and adding the node's value.  We maintain a global variable `max_sum` to track the overall maximum path sum encountered so far.

Crucially, the maximum path sum might not necessarily end at any given node. It could be a path entirely within the left or right subtree, or a path connecting a node's left and right subtrees *through* the node itself.  Therefore, for each node, we also compute the maximum path sum that *includes* the current node as its peak (i.e., using both left and right subtrees if available).  This maximum path sum through a node is then compared against the global `max_sum`.

The recursion explores the entire tree, and for each node, a constant number of calculations are performed.


## Time and Space Complexity
- Time: O(N), where N is the number of nodes in the binary tree. Each node is visited exactly once during the recursive traversal.
- Space: O(H), where H is the height of the binary tree. This space is used for the recursive call stack. In the worst case (a skewed tree), H can be equal to N, resulting in O(N) space complexity.  In the best case (a balanced tree), H is log₂(N), resulting in O(log N) space complexity.

## Java Solution
```java
/**
 * Given a non-empty binary tree, find the maximum path sum.
 * For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections.
 * The path must contain at least one node and does not need to go through the root.
 *
 * Difficulty: Hard
 */
class BinaryTreeMaximumPathSum {
    int maxSum = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        maxPathSumHelper(root);
        return maxSum;
    }

    private int maxPathSumHelper(TreeNode node) {
        if (node == null) {
            return 0;
        }

        int leftSum = Math.max(0, maxPathSumHelper(node.left));
        int rightSum = Math.max(0, maxPathSumHelper(node.right));

        maxSum = Math.max(maxSum, leftSum + rightSum + node.val);

        return Math.max(leftSum, rightSum) + node.val;
    }

    public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }
}
```