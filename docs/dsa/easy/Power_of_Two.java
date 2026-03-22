// Problem: Power of Two
// Difficulty: easy
// Time Complexity: O(log n)
// Space Complexity: O(1)
public class PowerOfTwo {
    public boolean isPowerOfTwo(int n) {
        // Check if n is less than or equal to 0, in which case it cannot be a power of two
        if (n <= 0) return false;
        
        // Use bitwise AND operation to check if n is a power of two
        // If n is a power of two, its binary representation has exactly one '1' bit
        // Subtracting 1 from n flips all bits to the right of the rightmost '1' bit
        // Therefore, if n is a power of two, n & (n - 1) will be zero
        return (n & (n - 1)) == 0;
    }
}