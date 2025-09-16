# Problem: Merge Intervals

## Summary of Approach

The Merge Intervals problem aims to merge overlapping intervals in a list.  The approach typically involves sorting the intervals by their start times.  Then, we iterate through the sorted intervals, maintaining a stack or a result list.  If the current interval overlaps with the last interval in the stack/list (meaning the current interval's start time is less than or equal to the last interval's end time), we merge them by taking the minimum start time and the maximum end time. Otherwise, we add the current interval to the stack/list.  The final stack/list contains the merged intervals.

## Time and Space Complexity
- Time: O(n log n)  The dominant factor is the sorting step, which typically uses a comparison-based sorting algorithm like merge sort or quicksort with O(n log n) complexity. The iteration through the sorted intervals takes O(n) time.
- Space: O(n)  In the worst case (no overlapping intervals), the space used to store the result list will be proportional to the number of input intervals.  If using an in-place approach, the space complexity can be reduced to O(log n) due to the sorting algorithm's space usage.  However, an extra space of O(n) is often used for simplicity and readability.

## Java Solution
```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

/*
Merge Intervals

Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

Difficulty: Medium
*/
class MergeIntervals {
    public int[][] merge(int[][] intervals) {
        if (intervals == null || intervals.length <= 1) {
            return intervals;
        }

        // Sort intervals by start time
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        List<int[]> mergedIntervals = new ArrayList<>();
        int[] currentInterval = intervals[0];
        mergedIntervals.add(currentInterval);

        for (int i = 1; i < intervals.length; i++) {
            int[] nextInterval = intervals[i];
            if (nextInterval[0] <= currentInterval[1]) {
                // Overlap: merge intervals
                currentInterval[1] = Math.max(currentInterval[1], nextInterval[1]);
            } else {
                // No overlap: add next interval to merged list
                currentInterval = nextInterval;
                mergedIntervals.add(currentInterval);
            }
        }

        return mergedIntervals.toArray(new int[mergedIntervals.size()][]);
    }
}
```