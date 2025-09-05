## Summary of Approach

Pascal's Triangle is a triangular array of numbers where each number is the sum of the two numbers directly above it.  The first and last numbers in each row are always 1.  The algorithm to generate it typically involves iteratively building each row based on the previous row.  This can be done using nested loops or dynamic programming techniques.  The approach focuses on calculating each element based on the previously computed elements in the preceding row.  For a given number of rows *n*, the algorithm constructs the triangle up to that row, efficiently leveraging the relationship between adjacent elements.


## Time and Space Complexity
- Time: O(n^2)  where 'n' is the number of rows.  This is because calculating each row requires a number of operations proportional to its length, and the lengths of the rows increase linearly with 'n'.
- Space: O(n^2) in a naive implementation that stores the entire triangle in memory.  This can be optimized to O(n) if you only need to store the current and previous rows during construction, discarding older rows.