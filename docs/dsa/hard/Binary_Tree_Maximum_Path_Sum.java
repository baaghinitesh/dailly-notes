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