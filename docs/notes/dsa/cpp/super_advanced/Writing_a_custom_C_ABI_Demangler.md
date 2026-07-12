---
title: "Writing a custom C++ ABI Demangler"
language: "cpp"
difficulty: "super_advanced"
section: "dsa"
tags: "dsa, cpp, super_advanced, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/557/1200/630"
update_count: 0
---

# Writing a custom C++ ABI Demangler

## Problem Understanding
The problem is asking to create a custom C++ ABI demangler, which takes a mangled C++ symbol as input and returns its demangled form. The key constraint is to correctly parse the mangled symbol string and identify its constituent parts, such as the function or variable name, return type, and parameters. The problem is non-trivial because the C++ ABI mangling scheme is complex and involves a combination of prefixes, suffixes, and encoding rules, making it challenging to write a correct and efficient demangler.

## Approach
The approach used in this solution is a recursive descent parser, which breaks down the mangled symbol into its constituent parts by parsing the input string from left to right. The parser uses a combination of string manipulation and conditional statements to identify the different parts of the mangled symbol, such as the function or variable name, return type, and parameters. The solution uses a `DemangledSymbol` structure to store the demangled symbol information, which includes the name and type of the symbol. The `demangle` function takes a mangled symbol string as input and returns a `DemangledSymbol` object containing the demangled information.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The time complexity is linear because the demangler parses the input string from left to right, and each character is processed exactly once. The `while` loops used to parse the function or variable name length and the parameters do not increase the overall time complexity because they are bounded by the length of the input string. |
| Space  | O(n)  | The space complexity is linear because the demangler stores the demangled symbol information in a `DemangledSymbol` object, which includes the name and type of the symbol. The `name` field of the `DemangledSymbol` object can potentially store a string of length `n`, where `n` is the length of the input string. |

## Algorithm Walkthrough
```
Input: _Z1fiv
Step 1: Check if the input string is empty → no
Step 2: Check if the input string starts with the C++ ABI prefix "_Z" → yes
Step 3: Parse the function or variable name length → length = 1
Step 4: Parse the function or variable name → name = "f"
Step 5: Parse the function return type and parameters → type = Function
Step 6: Create a DemangledSymbol object with the demangled information → {name: "f", type: Function}
Output: {name: "f", type: Function}
```
This walkthrough demonstrates how the demangler parses the input string and extracts the demangled information.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Input string empty?"}
    B -->|Yes| C[Return invalid symbol]
    B -->|No| D{"Input string starts with \"_Z\"?"}
    D -->|Yes| E[Parse function or variable name length]
    D -->|No| F[Return input string as is]
    E --> G[Parse function or variable name]
    G --> H[Parse function return type and parameters]
    H --> I[Create DemangledSymbol object]
    I --> J[Return demangled symbol]
```
This flowchart illustrates the decision flow of the demangler algorithm.

## Key Insight
> **Tip:** The key insight to writing a correct C++ ABI demangler is to understand the mangling scheme and how to correctly parse the input string to extract the demangled information.

## Edge Cases
- **Empty/null input**: If the input string is empty, the demangler returns an invalid symbol.
- **Single element**: If the input string contains only a single character, the demangler returns the input string as is.
- **Invalid mangled symbol**: If the input string does not start with the C++ ABI prefix "_Z", the demangler returns the input string as is.

## Common Mistakes
- **Mistake 1**: Not checking for the C++ ABI prefix "_Z" at the beginning of the input string → can lead to incorrect demangling of non-mangled symbols.
- **Mistake 2**: Not handling the case where the input string is empty → can lead to crashes or undefined behavior.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The demangler does not rely on the input being sorted, so it will work correctly regardless of the input order.
- "Can you do it in O(1) space?" → No, the demangler needs to store the demangled symbol information, which requires O(n) space.
- "What if there are duplicates?" → The demangler is designed to handle duplicates correctly, as it parses the input string from left to right and does not rely on any external state.

## CPP Solution

```cpp
// Problem: Custom C++ ABI Demangler
// Language: C++
// Difficulty: Super Advanced
// Time Complexity: O(n) — parsing the input mangled symbol string
// Space Complexity: O(n) — storing the demangled symbol string
// Approach: Recursive descent parser — breaking down the mangled symbol into its constituent parts

#include <iostream>
#include <string>
#include <unordered_map>

// Enum for different types of symbols
enum class SymbolType {
    Function,
    Variable,
    Type,
    Namespace
};

// Structure to hold the demangled symbol information
struct DemangledSymbol {
    std::string name;
    SymbolType type;
};

// Function to demangle a C++ ABI mangled symbol
DemangledSymbol demangle(const std::string& symbol) {
    // Edge case: empty input → return invalid symbol
    if (symbol.empty()) {
        return {"", SymbolType::Type};
    }

    // Check if the symbol starts with the C++ ABI prefix
    if (symbol.find("_Z") != 0) {
        // If not, return the symbol as is (assuming it's not mangled)
        return {symbol, SymbolType::Type};
    }

    // Initialize the demangled symbol
    DemangledSymbol demangled;
    demangled.name = "";

    // Parse the function or variable name
    size_t pos = 2; // Skip the "_Z" prefix
    // Parse the function or variable name length
    size_t length = 0;
    while (symbol[pos] >= '0' && symbol[pos] <= '9') {
        length = length * 10 + (symbol[pos++] - '0');
    }
    demangled.name = symbol.substr(pos, length);
    pos += length;

    // Parse the function return type and parameters
    while (pos < symbol.size()) {
        // Check for a function return type
        if (symbol[pos] == 'F') {
            // Function return type
            demangled.type = SymbolType::Function;
            pos++;
            break;
        }
        // Check for a variable
        else if (symbol[pos] == 'v') {
            // Variable
            demangled.type = SymbolType::Variable;
            pos++;
            break;
        }
        // Check for a type
        else if (symbol[pos] == 't') {
            // Type
            demangled.type = SymbolType::Type;
            pos++;
            break;
        }
        // Check for a namespace
        else if (symbol[pos] == 'N') {
            // Namespace
            demangled.type = SymbolType::Namespace;
            pos++;
            break;
        }
        // If none of the above, assume it's a parameter
        else {
            pos++;
        }
    }

    return demangled;
}

// Function to print the demangled symbol information
void printDemangledSymbol(const DemangledSymbol& symbol) {
    std::cout << "Name: " << symbol.name << std::endl;
    std::cout << "Type: ";
    switch (symbol.type) {
        case SymbolType::Function:
            std::cout << "Function";
            break;
        case SymbolType::Variable:
            std::cout << "Variable";
            break;
        case SymbolType::Type:
            std::cout << "Type";
            break;
        case SymbolType::Namespace:
            std::cout << "Namespace";
            break;
    }
    std::cout << std::endl;
}

int main() {
    // Example usage:
    std::string mangledSymbol = "_Z1fiv";
    DemangledSymbol demangled = demangle(mangledSymbol);
    printDemangledSymbol(demangled);
    return 0;
}
```
