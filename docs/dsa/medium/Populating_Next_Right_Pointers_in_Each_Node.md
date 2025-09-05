# Problem: Populating Next Right Pointers in Each Node

## Summary of Approach

The problem "Populating Next Right Pointers in Each Node" involves modifying a perfect binary tree (or a complete binary tree up to a certain level) such that each node's `next` pointer points to the next node on the same level.  The solution uses a level-order traversal (breadth-first search) to process the nodes level by level.  We utilize a queue to manage the traversal.  For each level, we iterate through the nodes in the queue, setting the `next` pointer of the current node to the next node in the queue.  The key is that the order of nodes in the queue naturally reflects the level-order traversal, allowing us to easily link adjacent nodes on the same level.


## Time and Space Complexity
- Time: O(N)
- Space: O(W)

where N is the total number of nodes in the tree, and W is the maximum width (maximum number of nodes at any level) of the tree.  In a perfect binary tree, W = O(N). In a skewed tree, W = O(1).  Therefore, the space complexity is O(N) in the worst case (a perfect binary tree) and O(1) in the best case (a completely skewed tree).

## Java Solution
```java
/*
Given a perfect binary tree, populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

Example:

Input:
     1
   /  \
  2    3
 / \  / \
4  5  6  7

Output:
     1 -> NULL
   /  \
  2 -> 3 -> NULL
 / \  / \
4->5->6->7 -> NULL

Difficulty: Medium
*/
class PopulatingNextRightPointersInEachNode {
    class Node {
        public int val;
        public Node left;
        public Node right;
        public Node next;

        public Node() {}

        public Node(int _val) {
            val = _val;
        }

        public Node(int _val, Node _left, Node _right, Node _next) {
            val = _val;
            left = _left;
            right = _right;
            next = _next;
        }
    };

    public Node connect(Node root) {
        if (root == null) return null;
        Node levelStart = root;
        while (levelStart != null) {
            Node curr = levelStart;
            while (curr != null) {
                if (curr.left != null) {
                    curr.left.next = curr.right;
                }
                if (curr.right != null && curr.next != null) {
                    curr.right.next = curr.next.left;
                }
                curr = curr.next;
            }
            levelStart = levelStart.left;
        }
        return root;
    }
}
```