# Problem: Remove Nth Node From End of List

## Summary of Approach

The problem is to remove the nth node from the end of a singly linked list.  The optimal approach uses two pointers.  We initialize a `fast` pointer and a `slow` pointer, both initially pointing to the head of the list.  The `fast` pointer moves `n` steps ahead of the `slow` pointer.  Then, both pointers move forward simultaneously, maintaining a distance of `n` between them. When the `fast` pointer reaches the end of the list, the `slow` pointer is `n` nodes away from the end, pointing to the node *before* the node to be removed.  We then simply update the `slow` pointer's `next` pointer to skip over the node to be removed.  This avoids the need for a full traversal or extra storage to track node positions.  A special case needs to be handled for removing the head node.

## Time and Space Complexity
- Time: O(N) - We traverse the list once to position the pointers.
- Space: O(1) - We use only a constant number of extra variables (the two pointers).

## Java Solution
```java
/**
 * Remove Nth Node From End of List
 * Difficulty: Medium
 */
class RemoveNthNodeFromEndOfList {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode first = dummy;
        ListNode second = dummy;

        // Move 'first' pointer n+1 nodes ahead
        for (int i = 0; i <= n; i++) {
            first = first.next;
        }

        // Move both pointers until 'first' reaches the end
        while (first != null) {
            first = first.next;
            second = second.next;
        }

        // Remove the nth node from the end
        second.next = second.next.next;

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