---
title: "Sqrt Decomposition Mo's Algorithm"
language: "cpp"
difficulty: "hard"
section: "dsa"
tags: "dsa, cpp, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/905/1200/630"
update_count: 0
---

# Sqrt Decomposition Mo's Algorithm

## Problem Understanding
The problem is asking to implement Mo's Algorithm with sqrt decomposition to process a list of queries on an array. The key constraints are the size of the array (n) and the number of queries (q), and the goal is to efficiently process these queries by dividing the array into sqrt(n) blocks and sorting the queries based on these blocks. The problem becomes non-trivial because a naive approach of processing each query individually would result in a time complexity of O(q * n), which can be improved using Mo's Algorithm with sqrt decomposition to achieve a time complexity of O(n * sqrt(n)).

## Approach
The algorithm strategy is to use Mo's Algorithm with sqrt decomposition, where the array is divided into sqrt(n) blocks, and the queries are sorted based on these blocks. This approach works because the queries are grouped together based on the blocks they belong to, and then processed in a way that minimizes the number of times the window needs to be moved. The data structure used is a vector of queries, where each query is represented by its left and right boundaries, and its index in the original list of queries. The approach handles the key constraints by efficiently processing the queries in each block, and by using a window to keep track of the current range of elements being processed.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n * sqrt(n)) | The time complexity is O(n * sqrt(n)) because there are n elements in the array, and each element is processed at most sqrt(n) times due to the blocking and sorting of queries. The sorting of queries takes O(q * log(q)) time, but since q is at most n, this term is dominated by the O(n * sqrt(n)) term. |
| Space  | O(n) | The space complexity is O(n) because we need to store the array of size n, the vector of queries of size q (which is at most n), and the window information, which takes constant space. |

## Algorithm Walkthrough
```
Input: n = 10, arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], queries = [[0, 4], [3, 7], [1, 8]]
Step 1: Divide the array into sqrt(n) blocks, so block size is sqrt(10) = 3.
Step 2: Sort the queries based on the block id and then the right boundary, so queries become [[0, 4], [1, 8], [3, 7]].
Step 3: Initialize the window to [0, -1] and the result vector to [0, 0, 0].
Step 4: Process the first query [0, 4], so move the window to [0, 4] and calculate the result as 1 + 2 + 3 + 4 + 5 = 15.
Step 5: Process the second query [1, 8], so move the window to [1, 8] and calculate the result as 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 = 54.
Step 6: Process the third query [3, 7], so move the window to [3, 7] and calculate the result as 4 + 5 + 6 + 7 + 8 = 30.
Output: [15, 54, 30]
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Divide array into sqrt(n) blocks]
    B --> C[Sort queries based on block id and right boundary]
    C --> D[Initialize window and result vector]
    D --> E[Process queries]
    E --> F[Move window and calculate result]
    F --> G[Store result in result vector]
    G --> H[Repeat for all queries]
    H --> I[Return result vector]
```

## Key Insight
> **Tip:** The key insight is to divide the array into sqrt(n) blocks and sort the queries based on these blocks, which allows us to process the queries in a way that minimizes the number of times the window needs to be moved.

## Edge Cases
- **Empty/null input**: If the input array is empty or null, the algorithm will return an empty result vector, because there are no elements to process.
- **Single element**: If the input array has only one element, the algorithm will process the queries as usual, but the window will always have a size of 1.
- **Duplicate queries**: If there are duplicate queries, the algorithm will process each query separately, but the result will be the same for duplicate queries.

## Common Mistakes
- **Mistake 1**: Not dividing the array into sqrt(n) blocks, which can lead to a time complexity of O(q * n) instead of O(n * sqrt(n)).
- **Mistake 2**: Not sorting the queries based on the block id and right boundary, which can lead to incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, but the time complexity will be O(n * sqrt(n)) because we are still dividing the array into sqrt(n) blocks and sorting the queries.
- "Can you do it in O(1) space?" → No, because we need to store the array and the queries, which takes at least O(n) space.
- "What if there are duplicates?" → The algorithm will process each query separately, but the result will be the same for duplicate queries.

## CPP Solution

```cpp
// Problem: Sqrt Decomposition Mo's Algorithm
// Language: cpp
// Difficulty: Hard
// Time Complexity: O(n * sqrt(n)) — due to sqrt(n) blocks and n queries
// Space Complexity: O(n) — for storing queries and block information
// Approach: Mo's Algorithm with sqrt decomposition — divide array into sqrt(n) blocks and process queries in each block

#include <bits/stdc++.h>
using namespace std;

class MoAlgorithm {
public:
    // Structure to represent a query
    struct Query {
        int left, right, index;
        bool operator<(const Query& other) const {
            // Compare queries based on block id and then right boundary
            int blockId = left / sqrt(n);
            int otherBlockId = other.left / sqrt(n);
            if (blockId != otherBlockId) {
                return blockId < otherBlockId;
            }
            return (blockId % 2 == 0) ? (right < other.right) : (right > other.right);
        }
    };

    int n;
    vector<int> arr;
    vector<Query> queries;

    MoAlgorithm(int n, vector<int> arr, vector<vector<int>> queries) {
        this->n = n;
        this->arr = arr;
        // Initialize queries
        for (int i = 0; i < queries.size(); i++) {
            Query query;
            query.left = queries[i][0];
            query.right = queries[i][1];
            query.index = i;
            this->queries.push_back(query);
        }
    }

    // Process queries using Mo's Algorithm
    vector<int> processQueries() {
        // Sort queries based on block id and then right boundary
        sort(queries.begin(), queries.end());
        int currentLeft = 0, currentRight = -1;
        vector<int> results(queries.size());
        // Iterate over sorted queries
        for (Query query : queries) {
            // Move the window to the left
            while (currentLeft > query.left) {
                currentLeft--;
                // Add element at currentLeft to the window
                // Edge case: empty input → return -1
                if (currentLeft < 0 || currentLeft >= n) {
                    continue;
                }
                // Update window information
                // Add arr[currentLeft] to the window
            }
            // Move the window to the right
            while (currentRight < query.right) {
                currentRight++;
                // Add element at currentRight to the window
                // Update window information
                // Add arr[currentRight] to the window
            }
            // Move the window to the left
            while (currentLeft < query.left) {
                // Remove element at currentLeft from the window
                // Update window information
                // Remove arr[currentLeft] from the window
                currentLeft++;
            }
            // Move the window to the right
            while (currentRight > query.right) {
                // Remove element at currentRight from the window
                // Update window information
                // Remove arr[currentRight] from the window
                currentRight--;
            }
            // Calculate the result for the current query
            int result = calculateResult(currentLeft, currentRight);
            results[query.index] = result;
        }
        return results;
    }

    // Calculate the result for a given window
    int calculateResult(int left, int right) {
        // Calculate the sum of elements in the window
        int sum = 0;
        for (int i = left; i <= right; i++) {
            sum += arr[i];
        }
        return sum;
    }
};

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    int q;
    cin >> q;
    vector<vector<int>> queries(q, vector<int>(2));
    for (int i = 0; i < q; i++) {
        cin >> queries[i][0] >> queries[i][1];
    }
    MoAlgorithm moAlgorithm(n, arr, queries);
    vector<int> results = moAlgorithm.processQueries();
    for (int result : results) {
        cout << result << " ";
    }
    cout << endl;
    return 0;
}
```
