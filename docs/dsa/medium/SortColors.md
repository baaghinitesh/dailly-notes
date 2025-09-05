## Summary of Approach

The "Sort Colors" problem asks to sort an array of 0s, 1s, and 2s in-place.  A highly efficient approach uses a three-pointer technique.  We maintain three pointers: `p0`, `p1`, and `p2`.

- `p0`: Points to the last index of the 0s section.  Everything before `p0` is a 0.
- `p1`: Points to the current element being considered.
- `p2`: Points to the first index of the 2s section. Everything after `p2` is a 2.


The algorithm iterates through the array with `p1`.

- If `arr[p1]` is 0, we swap `arr[p1]` and `arr[p0]`, then increment both `p0` and `p1`.
- If `arr[p1]` is 1, we simply increment `p1`.
- If `arr[p1]` is 2, we swap `arr[p1]` and `arr[p2]`, then decrement `p2`.

This process partitions the array into three sections: 0s, 1s, and 2s, efficiently sorting the array in-place.  Note that the swaps are done carefully to avoid overwriting unsorted elements.


## Time and Space Complexity
- Time: O(n) - The algorithm iterates through the array once.  While there are swaps, the number of swaps is proportional to n in the worst case.
- Space: O(1) - The algorithm uses only a constant amount of extra space to store the pointers.