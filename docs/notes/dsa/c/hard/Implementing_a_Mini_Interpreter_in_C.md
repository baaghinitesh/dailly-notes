---
title: "Implementing a Mini Interpreter in C"
language: "c"
difficulty: "hard"
section: "dsa"
tags: "dsa, c, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/206/1200/630"
update_count: 0
---

# Implementing a Mini Interpreter in C

## Problem Understanding
The problem is asking to implement a mini interpreter in C, which can parse and evaluate simple arithmetic expressions. The key constraints are that the interpreter should be able to handle expressions with addition, subtraction, multiplication, and division, as well as parentheses to group expressions. The problem is non-trivial because it requires a deep understanding of parsing and evaluating expressions, as well as handling errors and edge cases.

## Approach
The approach used to solve this problem is a recursive descent parser, which breaks down the input into smaller sub-problems and solves them recursively. The parser uses a grammar to define the structure of the expressions, and it uses a set of functions to parse each part of the expression. The parser also uses an abstract syntax tree (AST) to represent the parsed expression, which makes it easier to evaluate the expression. The approach works by using a set of functions to parse each part of the expression, and then using the AST to evaluate the expression.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The time complexity is O(n) because the parser needs to iterate over each character in the input string once to parse the expression. The recursive descent parser uses a set of functions to parse each part of the expression, and each function only needs to iterate over a portion of the input string. |
| Space  | O(n)  | The space complexity is O(n) because the parser needs to store the parsed expression in an abstract syntax tree (AST), which can grow up to the size of the input string. The parser also needs to store the tokens and variables, which can also grow up to the size of the input string. |

## Algorithm Walkthrough
```
Input: "2 + 3 * 4"
Step 1: Split the input into tokens: ["2", "+", "3", "*", "4"]
Step 2: Parse the expression: 
  - Parse the term: "2"
  - Parse the operator: "+"
  - Parse the term: "3 * 4"
    - Parse the factor: "3"
    - Parse the operator: "*"
    - Parse the factor: "4"
Step 3: Create the AST:
  - Create a node for the operator: "+"
  - Create a node for the term: "2"
  - Create a node for the term: "3 * 4"
    - Create a node for the operator: "*"
    - Create a node for the factor: "3"
    - Create a node for the factor: "4"
Step 4: Evaluate the AST:
  - Evaluate the node for the term: "2" → 2
  - Evaluate the node for the term: "3 * 4"
    - Evaluate the node for the factor: "3" → 3
    - Evaluate the node for the factor: "4" → 4
    - Apply the operator: "*" → 3 * 4 = 12
  - Apply the operator: "+" → 2 + 12 = 14
Output: 14
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is Input Empty?"}
    B -->|Yes| C[Return NULL]
    B -->|No| D[Split Input into Tokens]
    D --> E[Parse Expression]
    E -->|Term| F[Parse Term]
    E -->|Operator| G[Parse Operator]
    F -->|Factor| H[Parse Factor]
    G -->|ADD| I[Create ADD Node]
    G -->|SUB| J[Create SUB Node]
    G -->|MUL| K[Create MUL Node]
    G -->|DIV| L[Create DIV Node]
    H -->|Number| M[Create Number Node]
    H -->|Identifier| N[Create Identifier Node]
    H -->|(Expression)| O[Create Expression Node]
    I --> P[Evaluate ADD Node]
    J --> Q[Evaluate SUB Node]
    K --> R[Evaluate MUL Node]
    L --> S[Evaluate DIV Node]
    P --> T[Return Result]
    Q --> T
    R --> T
    S --> T
```

## Key Insight
> **Tip:** The key insight to this problem is to use a recursive descent parser to break down the input into smaller sub-problems and solve them recursively, and to use an abstract syntax tree (AST) to represent the parsed expression, which makes it easier to evaluate the expression.

## Edge Cases
- **Empty/null input**: If the input is empty or null, the parser will return NULL.
- **Single element**: If the input is a single element, such as a number or an identifier, the parser will create an AST node for that element and return it.
- **Invalid operator**: If the input contains an invalid operator, such as "^" or "%", the parser will return an error.

## Common Mistakes
- **Mistake 1**: Not checking for null or empty input before parsing the expression.
- **Mistake 2**: Not handling errors properly, such as division by zero or invalid operators.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The parser will still work correctly, but it may not be as efficient as it could be.
- "Can you do it in O(1) space?" → No, the parser needs to store the parsed expression in an abstract syntax tree (AST), which can grow up to the size of the input string.
- "What if there are duplicates?" → The parser will handle duplicates correctly, but it may not be as efficient as it could be.

## C Solution

```c
// Problem: Implementing a Mini Interpreter
// Language: C
// Difficulty: Hard
// Time Complexity: O(n) — where n is the length of the input string
// Space Complexity: O(n) — for storing the tokens and variables
// Approach: Recursive descent parser — breaking down the input into smaller sub-problems

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Define the maximum length of a token
#define MAX_TOKEN_LENGTH 100

// Define the types of tokens
typedef enum {
    TOKEN_UNKNOWN,
    TOKEN_IDENTIFIER,
    TOKEN_KEYWORD,
    TOKEN_OPERATOR,
    TOKEN_LITERAL,
    TOKEN_EOF
} TokenType;

// Define the structure for a token
typedef struct {
    TokenType type;
    char value[MAX_TOKEN_LENGTH];
} Token;

// Define the structure for an abstract syntax tree node
typedef struct ASTNode {
    char value[MAX_TOKEN_LENGTH];
    struct ASTNode* left;
    struct ASTNode* right;
} ASTNode;

// Function to create a new token
Token* createToken(TokenType type, char* value) {
    Token* token = (Token*)malloc(sizeof(Token));
    token->type = type;
    strcpy(token->value, value);
    return token;
}

// Function to create a new abstract syntax tree node
ASTNode* createASTNode(char* value) {
    ASTNode* node = (ASTNode*)malloc(sizeof(ASTNode));
    strcpy(node->value, value);
    node->left = NULL;
    node->right = NULL;
    return node;
}

// Function to parse the input string and generate an abstract syntax tree
ASTNode* parse(char* input) {
    // Edge case: empty input → return NULL
    if (input == NULL || strlen(input) == 0) {
        return NULL;
    }

    // Split the input into tokens
    Token* tokens = (Token*)malloc(sizeof(Token) * (strlen(input) + 1));
    int tokenCount = 0;
    char* token = strtok(input, " ");
    while (token != NULL) {
        tokens[tokenCount] = *createToken(TOKEN_LITERAL, token);
        tokenCount++;
        token = strtok(NULL, " ");
    }
    tokens[tokenCount].type = TOKEN_EOF;

    // Define the grammar for the mini interpreter
    // Expression → Term ((ADD | SUB) Term)*
    // Term → Factor ((MUL | DIV) Factor)*
    // Factor → Number | Identifier | (Expression)

    // Function to parse an expression
    ASTNode* parseExpression(Token** tokens) {
        ASTNode* node = parseTerm(tokens);
        while ((*tokens)->type == TOKEN_OPERATOR && ((*tokens)->value[0] == '+' || (*tokens)->value[0] == '-')) {
            ASTNode* operatorNode = createASTNode((*tokens)->value);
            operatorNode->left = node;
            (*tokens)++;
            operatorNode->right = parseTerm(tokens);
            node = operatorNode;
        }
        return node;
    }

    // Function to parse a term
    ASTNode* parseTerm(Token** tokens) {
        ASTNode* node = parseFactor(tokens);
        while ((*tokens)->type == TOKEN_OPERATOR && ((*tokens)->value[0] == '*' || (*tokens)->value[0] == '/')) {
            ASTNode* operatorNode = createASTNode((*tokens)->value);
            operatorNode->left = node;
            (*tokens)++;
            operatorNode->right = parseFactor(tokens);
            node = operatorNode;
        }
        return node;
    }

    // Function to parse a factor
    ASTNode* parseFactor(Token** tokens) {
        if ((*tokens)->type == TOKEN_LITERAL) {
            ASTNode* node = createASTNode((*tokens)->value);
            (*tokens)++;
            return node;
        } else if ((*tokens)->type == TOKEN_IDENTIFIER) {
            ASTNode* node = createASTNode((*tokens)->value);
            (*tokens)++;
            return node;
        } else if ((*tokens)->type == TOKEN_OPERATOR && (*tokens)->value[0] == '(') {
            (*tokens)++;
            ASTNode* node = parseExpression(tokens);
            (*tokens)++;
            return node;
        } else {
            // Edge case: invalid token → return NULL
            return NULL;
        }
    }

    // Start parsing the input
    ASTNode* root = parseExpression(&tokens[0]);

    // Free the tokens
    free(tokens);

    return root;
}

// Function to evaluate the abstract syntax tree
int evaluate(ASTNode* node) {
    if (node == NULL) {
        // Edge case: NULL node → return 0
        return 0;
    }

    if (node->left == NULL && node->right == NULL) {
        // Leaf node → return the value
        return atoi(node->value);
    } else {
        // Internal node → apply the operator
        int leftValue = evaluate(node->left);
        int rightValue = evaluate(node->right);
        if (strcmp(node->value, "+") == 0) {
            return leftValue + rightValue;
        } else if (strcmp(node->value, "-") == 0) {
            return leftValue - rightValue;
        } else if (strcmp(node->value, "*") == 0) {
            return leftValue * rightValue;
        } else if (strcmp(node->value, "/") == 0) {
            // Edge case: division by zero → return error
            if (rightValue == 0) {
                printf("Error: division by zero\n");
                return 0;
            }
            return leftValue / rightValue;
        } else {
            // Edge case: invalid operator → return error
            printf("Error: invalid operator\n");
            return 0;
        }
    }
}

int main() {
    char input[100];
    printf("Enter an expression: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0; // Remove the newline character

    ASTNode* root = parse(input);
    if (root == NULL) {
        printf("Error: unable to parse the input\n");
    } else {
        int result = evaluate(root);
        printf("Result: %d\n", result);
    }

    return 0;
}
```
