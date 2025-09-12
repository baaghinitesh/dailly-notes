# Problem: Remove Duplicates from Sorted List II

## Summary of Approach

The problem "Remove Duplicates from Sorted List II" asks to remove all nodes with duplicate values from a sorted linked list, leaving only unique nodes.  The solution iterates through the linked list.  A "dummy" node is often used to simplify handling the head of the list.  We maintain a pointer to the current node being examined and a pointer to the previous node. If the current node's value is the same as the next node's value (a duplicate), the current node is skipped by connecting the previous node to the node after the current one. If the current node's value is different from the next node's value (not a duplicate), the pointers are simply moved forward.  This process continues until the end of the list is reached. The resulting list contains only unique nodes.


## Time and Space Complexity
- Time: O(N) - The algorithm iterates through the linked list once, where N is the number of nodes.
- Space: O(1) - The algorithm uses a constant amount of extra space to store pointers.  It doesn't use any additional data structures whose size depends on the input size.

## Java Solution
```java
/**
 * Remove Duplicates from Sorted List II
 * Difficulty: Medium
 * Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the head of the modified linked list.
 *
 * Example 1:
 * Input: head = [1,2,3,3,4,4,5]
 * Output: [1,2,5]
 *
 * Example 2:
 * Input: head = [1,1,1,2,3]
 * Output: [2,3]
 *
 * Constraints:
 * The number of nodes in the list is in the range [0, 300].
 * -100 <= Node.val <= 100
 * The list is guaranteed to be sorted.
 */
class RemoveDuplicatesFromSortedListII {
    public ListNode deleteDuplicates(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode prev = dummy;
        ListNode curr = head;

        while (curr != null) {
            boolean duplicate = false;
            while (curr.next != null && curr.val == curr.next.val) {
                duplicate = true;
                curr = curr.next;
            }

            if (duplicate) {
                prev.next = curr.next;
            } else {
                prev = curr;
            }
            curr = curr.next;
        }

        return dummy.next;
    }

    public class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }
}
```