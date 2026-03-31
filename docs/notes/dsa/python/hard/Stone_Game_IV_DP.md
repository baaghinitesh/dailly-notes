---
title: "Stone Game IV DP"
language: "python"
difficulty: "hard"
section: "dsa"
tags: "dsa, python, hard, leetcode, algorithms, coding-interview"
banner: "https://image.pollinations.ai/prompt/dsa%20Stone%20Game%20IV%20DP%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Stone Game IV DP

## Problem Understanding
The problem is asking whether the first player can win a game where two players take turns removing a square number of stones from a pile of `n` stones. The key constraint is that the game is won by the player who makes the last move, and a player can only remove a square number of stones in their turn. This problem is non-trivial because the number of possible moves is large, and a naive approach would involve trying all possible moves and their outcomes, resulting in exponential time complexity. The game has a complex structure, as the optimal move depends on the current state of the game and the possible moves of the opponent.

## Approach
The algorithm strategy used is dynamic programming with memoization, where we store the results of subproblems to avoid redundant computation. The intuition behind this approach is that the game can be divided into subproblems, where each subproblem represents the game state after a certain number of moves. By memoizing the results of these subproblems, we can efficiently determine whether the first player can win the game. The algorithm uses a dictionary to store the memoized results, where the key is the current state of the game (i.e., the number of stones remaining) and the value is a boolean indicating whether the first player can win from that state. The approach handles the key constraints by only considering moves that remove a square number of stones and by using memoization to avoid redundant computation.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates over all possible states of the game (i.e., all numbers from 1 to `n`), and for each state, it tries all possible moves (i.e., all square numbers less than or equal to the current state). The time complexity is linear because the number of possible moves is proportional to the square root of the current state, and the sum of the square roots of all numbers from 1 to `n` is proportional to `n`. |
| Space  | O(n)  | The algorithm uses a dictionary to store the memoized results, where the key is the current state of the game (i.e., the number of stones remaining) and the value is a boolean indicating whether the first player can win from that state. The space complexity is linear because the dictionary stores at most `n` elements. |

## Algorithm Walkthrough
```
Input: n = 7
Step 1: Initialize memo dictionary and call dp(7)
  - memo = {}
  - dp(7) is called, which checks if 7 is in memo
  - Since 7 is not in memo, dp(7) tries all possible moves
    - Try move 1: remove 1 stone, dp(6) is called
    - Try move 4: remove 4 stones, dp(3) is called
    - Try move 9: remove 9 stones, but 9 > 7, so this move is not possible
Step 2: Evaluate dp(6) and dp(3)
  - dp(6) tries all possible moves
    - Try move 1: remove 1 stone, dp(5) is called
    - Try move 4: remove 4 stones, dp(2) is called
    - Try move 9: remove 9 stones, but 9 > 6, so this move is not possible
  - dp(3) tries all possible moves
    - Try move 1: remove 1 stone, dp(2) is called
    - Try move 4: remove 4 stones, but 4 > 3, so this move is not possible
Step 3: Evaluate dp(5), dp(2), and dp(2)
  - dp(5) tries all possible moves
    - Try move 1: remove 1 stone, dp(4) is called
    - Try move 4: remove 4 stones, dp(1) is called
    - Try move 9: remove 9 stones, but 9 > 5, so this move is not possible
  - dp(2) tries all possible moves
    - Try move 1: remove 1 stone, dp(1) is called
    - Try move 4: remove 4 stones, but 4 > 2, so this move is not possible
Step 4: Evaluate dp(4), dp(1), dp(1), and dp(1)
  - dp(4) tries all possible moves
    - Try move 1: remove 1 stone, dp(3) is called
    - Try move 4: remove 4 stones, dp(0) is called
    - Try move 9: remove 9 stones, but 9 > 4, so this move is not possible
  - dp(1) tries all possible moves
    - Try move 1: remove 1 stone, dp(0) is called
    - Try move 4: remove 4 stones, but 4 > 1, so this move is not possible
  - Since dp(0) returns False, dp(1) returns True
Step 5: Backtrack and determine the final result
  - Since dp(1) returns True, dp(4) returns False
  - Since dp(4) returns False, dp(5) returns True
  - Since dp(5) returns True, dp(6) returns False
  - Since dp(6) returns False, dp(7) returns False
Output: False
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize memo dictionary]
    B --> C["Call dp(n)"]
    C --> D{"Is n in memo?"}
    D -->|Yes| E["Return memo[n"]]
    D -->|No| F[Try all possible moves]
    F --> G["Call dp(n - move)"]
    G --> H{"Is dp(n - move) False?"}
    H -->|Yes| I[Return True]
    H -->|No| J[Continue trying moves]
    J --> F
    I --> K[Store result in memo]
    K --> E
```
## Key Insight
> **The key insight is that the game can be solved using dynamic programming by memoizing the results of subproblems, allowing us to avoid redundant computation and efficiently determine whether the first player can win the game.**

## Edge Cases
- **Empty/null input**: If the input `n` is 0, the function returns False, because there are no stones to remove, and the first player cannot win.
- **Single element**: If the input `n` is 1, the function returns True, because the first player can remove the only stone and win the game.
- **Large input**: If the input `n` is large, the function may take a long time to compute, because the number of possible moves is proportional to the square root of `n`. However, the memoization technique used in the dynamic programming approach helps to reduce the time complexity and make the function more efficient.

## Common Mistakes
- **Mistake 1: Not using memoization**: If we do not use memoization, the function will have exponential time complexity, because we will be recomputing the results of subproblems multiple times. To avoid this mistake, we should use a dictionary to store the memoized results.
- **Mistake 2: Not checking for the base case**: If we do not check for the base case where `n` is 0, the function will not work correctly. To avoid this mistake, we should add a base case to the recursive function to handle this situation.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not assume that the input is sorted, and it works correctly even if the input is not sorted. However, if the input is sorted, we may be able to use a more efficient algorithm.
- "Can you do it in O(1) space?" → No, the algorithm uses a dictionary to store the memoized results, which requires O(n) space. However, we can try to use a more space-efficient data structure, such as a bit array, to reduce the space complexity.
- "What if there are duplicates?" → The algorithm does not assume that the input is unique, and it works correctly even if there are duplicates. However, if there are duplicates, we may need to modify the algorithm to handle this situation correctly.

## Python Solution

```python
# Problem: Stone Game IV DP
# Language: python
# Difficulty: Hard
# Time Complexity: O(n) — dynamic programming using memoization
# Space Complexity: O(n) — memoization stores at most n elements
# Approach: Dynamic Programming — use memoization to store maximum score

class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        # Create a memoization dictionary to store the results of subproblems
        memo = {}
        
        # Define a helper function to perform the dynamic programming
        def dp(i: int) -> bool:
            # Base case: if there are no more stones, return False
            if i == 0:
                return False  # Edge case: no stones left → player cannot win
            
            # Check if the result is already memoized
            if i in memo:
                return memo[i]
            
            # Initialize a flag to indicate whether the current player can win
            can_win = False
            
            # Try all possible moves (remove a square number of stones)
            j = 1
            while j * j <= i:
                # Recursively check if the other player loses after this move
                if not dp(i - j * j):
                    can_win = True  # If the other player loses, the current player wins
                    break
                j += 1
            
            # Memoize the result of the current subproblem
            memo[i] = can_win
            return can_win
        
        # Call the helper function to determine if the first player can win
        return dp(n)

    # Brute force approach (commented out)
    # def winnerSquareGame_brute_force(self, n: int) -> bool:
    #     def dfs(i: int, player: int) -> bool:
    #         if i == 0:
    #             return player == 1  # Player 1 wins if they make the last move
    #         for j in range(1, int(i ** 0.5) + 1):
    #             if not dfs(i - j * j, 3 - player):  # Try all possible moves
    #                 return True
    #         return False
    #     return dfs(n, 1)

    # Key insight: the game can be solved using dynamic programming
    # The key insight is that the game can be divided into subproblems, where
    # each subproblem represents the game state after a certain number of moves.
    # By memoizing the results of these subproblems, we can avoid redundant
    # computation and solve the game efficiently.

# Example usage:
solution = Solution()
print(solution.winnerSquareGame(1))  # True
print(solution.winnerSquareGame(2))  # False
print(solution.winnerSquareGame(7))  # False
```
