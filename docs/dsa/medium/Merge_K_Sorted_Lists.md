# Problem: Merge K Sorted Lists

## Summary of Approach

The Merge K Sorted Lists problem involves merging k sorted linked lists into a single sorted linked list.  A common and efficient approach uses a priority queue (min-heap).  The algorithm works as follows:

1. **Initialization:** Create a min-heap data structure.  Insert the first node from each of the k sorted lists into the heap.  Each element in the heap is a pair (node value, list index) to track which list the node belongs to.

2. **Iteration:** While the heap is not empty:
   - Extract the minimum element (node) from the heap.  This is the next smallest node overall.
   - Add this node to the result list.
   - If the extracted node's list still has more nodes, insert the next node from that list into the heap.

3. **Result:** The resulting linked list contains all nodes from the k input lists, sorted in ascending order.


## Time and Space Complexity
- Time: O(N log k), where N is the total number of nodes across all k lists.  This is because inserting and extracting from a heap of size k takes O(log k) time, and we do this N times.

- Space: O(k). The space complexity is dominated by the heap, which at most contains one node from each of the k lists.  The output list's space is O(N), but this is not considered in space complexity analysis because the problem asks us to construct the output, so the result's space usage is not counted against the algorithm.

## Java Solution
```java
/**
 * Merge k Sorted Lists
 * Difficulty: Hard
 */
class MergeKSortedLists {
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) {
            return null;
        }

        return mergeSort(lists, 0, lists.length - 1);
    }

    private ListNode mergeSort(ListNode[] lists, int start, int end) {
        if (start == end) {
            return lists[start];
        }

        int mid = start + (end - start) / 2;
        ListNode left = mergeSort(lists, start, mid);
        ListNode right = mergeSort(lists, mid + 1, end);

        return mergeTwoLists(left, right);
    }

    private ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;

        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }

        tail.next = (l1 == null) ? l2 : l1;
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