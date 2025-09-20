// Question: Given an array of positive integers nums and an integer target, return the minimum length of a subarray whose sum is greater than or equal to target. If no such subarray exists, return 0 instead.
// Difficulty: Medium

class MinimumSizeSubarraySum {
    public int minSubArrayLen(int target, int[] nums) {
        int minLen = Integer.MAX_VALUE;
        int windowStart = 0;
        int windowSum = 0;

        for (int windowEnd = 0; windowEnd < nums.length; windowEnd++) {
            windowSum += nums[windowEnd];

            while (windowSum >= target) {
                minLen = Math.min(minLen, windowEnd - windowStart + 1);
                windowSum -= nums[windowStart];
                windowStart++;
            }
        }

        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }
}