# Problem: Evaluate Reverse Polish Notation

## Summary of Approach

The Evaluate Reverse Polish Notation (RPN) problem involves evaluating an arithmetic expression written in Reverse Polish Notation.  RPN, also known as postfix notation, places operators *after* their operands.  The algorithm uses a stack to efficiently evaluate the expression.  It iterates through the RPN tokens (numbers and operators).  If a token is a number, it's pushed onto the stack. If a token is an operator, the algorithm pops the necessary number of operands from the stack, performs the operation, and pushes the result back onto the stack.  After processing all tokens, the final result is the top (and only) element on the stack.

## Time and Space Complexity
- Time: O(n)
- Space: O(n)

where n is the number of tokens in the RPN expression.  The algorithm iterates through each token once, performing constant-time operations for each (pushing/popping from the stack and arithmetic).  The space used by the stack is proportional to the maximum depth of the stack, which in the worst case (e.g., a deeply nested expression with many operands before an operator) can be as large as n.

## Java Solution
```java
import java.util.Stack;

/*
Evaluate Reverse Polish Notation
Medium
*/
class EvaluateReversePolishNotation {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String token : tokens) {
            if (token.equals("+")) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                stack.push(operand1 + operand2);
            } else if (token.equals("-")) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                stack.push(operand1 - operand2);
            } else if (token.equals("*")) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                stack.push(operand1 * operand2);
            } else if (token.equals("/")) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                stack.push(operand1 / operand2);
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }
}
```