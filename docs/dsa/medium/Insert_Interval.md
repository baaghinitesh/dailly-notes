# Problem: Insert Interval

## Summary of Approach

The "Insert Interval" problem involves inserting a new interval into a list of non-overlapping, sorted intervals. The goal is to produce a new list of non-overlapping, sorted intervals that includes the inserted interval.

The approach generally involves iterating through the sorted list of intervals.  We maintain a result list.  If the current interval from the input list does not overlap with the new interval, it's added directly to the result list. If there's an overlap, we merge the current interval with the new interval by expanding the start or end times as needed.  This merging continues as long as overlaps exist.  Finally, any remaining intervals from the input list are appended to the result list.


## Time and Space Complexity
- Time: O(N), where N is the number of intervals in the input list. This is because we iterate through the list at most once.  Merging intervals takes constant time for each overlap.
- Space: O(N). In the worst case, we might need to create a new list of intervals with the same size as the input list (e.g., if the new interval doesn't overlap with any existing intervals).  We may use a small constant amount of extra space for variables.

## Java Solution
```java
import java.util.ArrayList;
import java.util.List;

/*
 * Question: Insert Interval (Medium)
 * Given a list of non-overlapping intervals sorted by their start times, insert a given interval into the list such that the resulting list is also sorted by start times and remains non-overlapping (merge overlapping intervals if necessary).
 */
class InsertInterval {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> result = new ArrayList<>();
        int i = 0;

        // Add all intervals ending before the new interval starts
        while (i < intervals.length && intervals[i][1] < newInterval[0]) {
            result.add(intervals[i]);
            i++;
        }

        // Merge overlapping intervals
        while (i < intervals.length && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.add(newInterval);

        // Add remaining intervals
        while (i < intervals.length) {
            result.add(intervals[i]);
            i++;
        }

        return result.toArray(new int[result.size()][]);
    }
}
```