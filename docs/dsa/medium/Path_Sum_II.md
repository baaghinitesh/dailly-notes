# Problem: Path Sum II

## Summary of Approach

The Path Sum II problem requires finding all root-to-leaf paths in a binary tree that sum up to a target value.  The solution uses a Depth-First Search (DFS) approach.  We recursively traverse the tree.  For each node, we:

1. **Subtract the node's value from the remaining sum.** This keeps track of the remaining sum needed to reach the target.

2. **Check for base cases:**
   - If we reach a leaf node:
     - If the remaining sum is 0, we've found a valid path.  We add a copy of the current path to the result list.
     - Otherwise, we've reached a leaf node without the sum matching the target; we backtrack.
   - If the remaining sum becomes negative, we know it's impossible for any path stemming from this node to reach the target. We backtrack.

3. **Recursively explore the left and right subtrees.**  Before each recursive call, we add the current node's value to the path list (to build the path). After the recursive call returns, we remove the current node's value from the path list (to backtrack properly).


This approach systematically explores all possible root-to-leaf paths and efficiently identifies those that meet the target sum.  The use of a path list and backtracking ensures we can reconstruct all valid paths.

## Time and Space Complexity
- Time: O(N*log N)  or O(N*M) where N is the number of nodes in the tree and M is the maximum length of any path (which can be equal to the tree height in the worst case,  log N for a balanced tree or N for a skewed tree). Each node might be visited multiple times as the paths are explored, and in the worst case we may need to build a path list of length M for each valid path.
- Space: O(N) or O(M) in the worst case. This is primarily due to the recursive call stack (depth of the recursion is the height of the tree, which can be N in a skewed tree) and the space used to store the path (which is bounded by M) during the DFS traversal. The result list also consumes space proportional to the number of valid paths found, which in the worst case, might be proportional to N.

## Java Solution
```java
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
```