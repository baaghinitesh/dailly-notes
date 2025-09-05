// Question: Given a binary array nums and an integer k, return the minimum number of flips required to make all elements of nums equal. A flip is choosing a subarray of length k and inverting all elements in that subarray.
// Difficulty: Medium

class MinimumNumberOfKConsecutiveBitFlips {
    public int minKBitFlips(int[] nums, int k) {
        int n = nums.length;
        int flips = 0;
        int[] prefixSum = new int[n + 1];

        for (int i = 0; i < n; i++) {
            int current = prefixSum[i] % 2;
            if (nums[i] != current) {
                if (i + k > n) return -1; // Impossible to flip
                flips++;
                prefixSum[i + 1]++;
                prefixSum[i + k]--;
            }
            prefixSum[i + 1] += prefixSum[i];

        }

        return flips;

    }
}