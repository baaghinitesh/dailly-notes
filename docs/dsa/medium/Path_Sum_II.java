/**
 * Path Sum II
 * Medium
 * Given a binary tree and a target sum, find all root-to-leaf paths where each path's sum equals the target sum.
 * A leaf is a node with no children.
 */
import java.util.ArrayList;
import java.util.List;

class PathSumII {
    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) {
            return result;
        }
        List<Integer> currentPath = new ArrayList<>();
        findPath(root, targetSum, currentPath, result);
        return result;
    }

    private void findPath(TreeNode node, int targetSum, List<Integer> currentPath, List<List<Integer>> result) {
        currentPath.add(node.val);
        if (node.left == null && node.right == null) {
            if (node.val == targetSum) {
                result.add(new ArrayList<>(currentPath));
            }
        } else {
            if (node.left != null) {
                findPath(node.left, targetSum - node.val, currentPath, result);
            }
            if (node.right != null) {
                findPath(node.right, targetSum - node.val, currentPath, result);
            }
        }
        currentPath.remove(currentPath.size() - 1);
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