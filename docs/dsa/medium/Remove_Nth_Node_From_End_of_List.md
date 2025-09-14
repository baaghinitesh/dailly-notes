# Problem: Remove Nth Node From End of List

## Summary of Approach

The problem is to remove the nth node from the end of a singly linked list.  The most efficient approach uses two pointers.  We initialize a `fast` pointer and a `slow` pointer, both initially pointing to the head of the list.  The `fast` pointer moves `n` steps ahead of the `slow` pointer.  Then, both pointers move forward together until the `fast` pointer reaches the end of the list. At this point, the `slow` pointer will be positioned `n` nodes before the end, i.e., just before the node to be removed.  We then remove the node pointed to by `slow`'s `next` pointer by adjusting the pointers accordingly.  Handling edge cases, such as an empty list or `n` being larger than the list length, is crucial.

## Time and Space Complexity
- Time: O(L) where L is the length of the linked list. We traverse the list at most twice.
- Space: O(1). The algorithm uses only a constant amount of extra space to store the pointers.

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

        // Move 'first' pointer n + 1 steps ahead
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