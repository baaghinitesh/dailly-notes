# Problem: Path Sum

## Summary of Approach

The Path Sum problem aims to determine if a path exists from the root to a leaf node in a binary tree such that the sum of the nodes along that path equals a given target sum.  The approach typically uses Depth-First Search (DFS), either recursively or iteratively.

A recursive approach explores the left and right subtrees, adding the current node's value to the running sum.  If a leaf node is reached and the running sum matches the target, the function returns `true`.  If the sum exceeds the target at any point, that branch is pruned.

An iterative approach employs a stack (or queue for Breadth-First Search, though less common for this problem) to simulate the recursive calls.  It systematically explores nodes, keeping track of the running sum for each path.


## Time and Space Complexity

- **Time: O(N)** where N is the number of nodes in the binary tree. In the worst case, the algorithm visits every node in the tree.

- **Space: O(H)** where H is the height of the binary tree.  This accounts for the recursive call stack in the recursive approach or the stack used in the iterative approach.  In the worst case (a skewed tree), H can be equal to N.  In the best case (a balanced tree), H is log₂N.

## Java Solution
```java
/**
 * Path Sum
 * Difficulty: Easy
 * Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.
 * A leaf is a node with no children.
 */
class PathSum {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) {
            return false;
        }
        if (root.left == null && root.right == null) {
            return targetSum == root.val;
        }
        return hasPathSum(root.left, targetSum - root.val) || hasPathSum(root.right, targetSum - root.val);
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