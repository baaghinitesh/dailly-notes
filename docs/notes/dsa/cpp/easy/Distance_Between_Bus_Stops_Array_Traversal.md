---
title: "Distance Between Bus Stops Array Traversal"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/248/1200/630"
update_count: 0
---

# Distance Between Bus Stops Array Traversal

## Problem Understanding
The problem requires finding the shortest distance between two bus stops in a circular route, given an array of distances between consecutive stops and the indices of the start and destination stops. The key constraint is that the bus can travel in either direction, and we need to find the minimum distance between the two stops. This problem is non-trivial because a naive approach would be to simply sum the distances between the start and destination stops, but this does not account for the possibility of traveling in the opposite direction, which could result in a shorter distance.

## Approach
The algorithm strategy is to use a two-pointer technique to track the total distance traveled and the distance between the start and destination stops. We first calculate the total distance by summing all distances in the array. Then, we calculate the distance between the start and destination stops by summing the distances between these two points. Finally, we return the minimum of these two distances, which represents the shortest distance between the two stops. This approach works because it considers both possible directions of travel and chooses the one that results in the minimum distance. The data structure used is a simple array, which is sufficient to store the distances between consecutive stops.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We make two passes through the array: one to calculate the total distance and one to calculate the distance between the start and destination stops. Each pass takes O(n) time, where n is the number of stops. |
| Space  | O(1)  | We use a constant amount of space to store the total distance and the distance between the start and destination stops, regardless of the size of the input array. |

## Algorithm Walkthrough
```
Input: distance = [1, 2, 3, 4], start = 0, destination = 1
Step 1: Initialize totalDistance = 0 and distanceBetweenStartAndDestination = 0
Step 2: Calculate totalDistance by summing all distances: totalDistance = 1 + 2 + 3 + 4 = 10
Step 3: Calculate distanceBetweenStartAndDestination by summing distances between start and destination: distanceBetweenStartAndDestination = 1
Step 4: Return minimum distance: min(distanceBetweenStartAndDestination, totalDistance - distanceBetweenStartAndDestination) = min(1, 10 - 1) = min(1, 9) = 1
Output: 1
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Calculate total distance}
    B --> C[Sum all distances in array]
    C --> D{Calculate distance between start and destination}
    D --> E[Sum distances between start and destination]
    E --> F{Return minimum distance}
    F --> G["Return min("distanceBetweenStartAndDestination, totalDistance - distanceBetweenStartAndDestination")"]
```

## Key Insight
> **Tip:** The key insight is to consider both possible directions of travel and choose the one that results in the minimum distance, which can be achieved by calculating the total distance and the distance between the start and destination stops.

## Edge Cases
- **Empty input array**: If the input array is empty, the function should return 0, as there are no stops to travel between.
- **Single element in input array**: If the input array contains only one element, the function should return 0, as there is only one stop and no distance to travel.
- **Start and destination are the same stop**: If the start and destination stops are the same, the function should return 0, as there is no distance to travel.

## Common Mistakes
- **Mistake 1: Not considering both directions of travel**: This can result in returning a distance that is not the minimum. To avoid this, always calculate the distance in both directions and return the minimum.
- **Mistake 2: Not handling edge cases**: This can result in incorrect results for special cases, such as an empty input array or a single element in the input array. To avoid this, always check for these edge cases and handle them correctly.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, as it only relies on the indices of the start and destination stops, not on the order of the distances.
- "Can you do it in O(1) space?" → No, the algorithm requires at least O(1) space to store the total distance and the distance between the start and destination stops.
- "What if there are duplicates in the input array?" → The algorithm still works correctly, as it only relies on the indices of the start and destination stops, not on the values of the distances.

## CPP Solution

```cpp
// Problem: Distance Between Bus Stops Array Traversal
// Language: C++
// Difficulty: Easy
// Time Complexity: O(n) — single pass through array
// Space Complexity: O(1) — constant space used
// Approach: two-pointer technique — track total distance traveled

class Solution {
public:
    int distanceBetweenBusStops(vector<int>& distance, int start, int destination) {
        // Handle edge case: start is greater than destination
        if (start > destination) {
            // Swap start and destination to ensure start is less than destination
            swap(start, destination);
        }
        
        // Initialize total distance and distance between start and destination
        int totalDistance = 0;
        int distanceBetweenStartAndDestination = 0;
        
        // Calculate total distance by summing all distances
        for (int i = 0; i < distance.size(); i++) {
            // Add current distance to total distance
            totalDistance += distance[i];
        }
        
        // Calculate distance between start and destination
        for (int i = start; i < destination; i++) {
            // Add current distance to distance between start and destination
            distanceBetweenStartAndDestination += distance[i];
        }
        
        // Return minimum distance between start and destination or the total distance minus the distance between start and destination
        return min(distanceBetweenStartAndDestination, totalDistance - distanceBetweenStartAndDestination);
    }
};
```
