// Question: The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (You may want to display this pattern in a fixed font for better legibility)
// P   A   H   N
// A P L S I I G
// Y   I   R
// And then read line by line: "PAHNAPLSIIG"
// Write the code that will take a string and make this conversion given a number of rows:
// Difficulty: Medium

class ZigzagConversion {
    public String convert(String s, int numRows) {
        if (numRows == 1 || numRows >= s.length()) return s;

        StringBuilder[] sb = new StringBuilder[numRows];
        for (int i = 0; i < numRows; i++) sb[i] = new StringBuilder();

        int i = 0;
        int down = 0;
        for (char c : s.toCharArray()) {
            sb[i].append(c);
            if (i == numRows - 1) down = 1;
            else if (i == 0) down = 0;

            i += down == 0 ? 1 : -1;
        }

        StringBuilder result = new StringBuilder();
        for (StringBuilder str : sb) result.append(str);

        return result.toString();
    }
}