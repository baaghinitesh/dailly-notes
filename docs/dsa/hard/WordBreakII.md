## Summary of Approach

The Word Break II problem asks to find all possible sentences that can be formed by breaking a given string into words from a provided dictionary.  The solution typically employs a dynamic programming approach combined with backtracking.

1. **Dynamic Programming (DP):**  A DP table (often a vector or array) is used to store boolean values indicating whether a substring of the input string can be segmented into words from the dictionary.  This step avoids redundant calculations by pre-computing the feasibility of breaking substrings.

2. **Backtracking:** Once the DP table is built, backtracking is used to generate all possible sentence combinations. Starting from the end of the string, the algorithm recursively explores all valid word breaks found in the DP table. Each valid break leads to a recursive call, extending the current sentence until the beginning of the string is reached.  At each step, the found word is added to the current sentence.


## Time and Space Complexity

- **Time: O(n * 2<sup>n</sup>)**, where n is the length of the input string.  The DP step takes O(n²) time. However, the dominant factor is the backtracking step. In the worst case, each substring can be broken in multiple ways, leading to an exponential number of possible sentences. The number of sentences can be exponential, growing as high as 2<sup>n</sup> in the worst-case scenario (although this is rare).  The time to *construct* each sentence is linear in n.

- **Space: O(n + m + r),** where n is the length of the input string, m is the size of the dictionary, and r is the maximum length of the generated sentences.  The DP table requires O(n) space.  The dictionary occupies O(m) space. During backtracking, the recursion depth can be O(n), and the space used to store each sentence can be up to O(r).