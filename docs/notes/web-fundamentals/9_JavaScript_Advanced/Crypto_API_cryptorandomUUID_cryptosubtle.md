---
title: "Crypto API: crypto.randomUUID(), crypto.subtle"
topic: "Crypto API: crypto.randomUUID(), crypto.subtle"
section: "web-fundamentals"
tags: "web-fundamentals, crypto-api, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/web-fundamentals%20Crypto%20API%20crypto.randomUUID(),%20crypto.subtle%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![Crypto API](https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Cryptography.svg/1200px-Cryptography.svg.png)

## Introduction
The **Crypto API** is a set of APIs provided by modern web browsers to enable web applications to perform various cryptographic operations, such as generating random numbers, hashing, and encryption. The `crypto.randomUUID()` and `crypto.subtle` APIs are two of the most commonly used APIs in this set. These APIs are essential for building secure web applications, and every web developer should have a good understanding of how to use them. In this article, we will delve into the details of these APIs, their internal workings, and provide code examples to demonstrate their usage.

> **Note:** The `crypto` API is only available in secure contexts, such as HTTPS, to prevent man-in-the-middle attacks.

## Core Concepts
The `crypto.randomUUID()` API generates a random UUID (Universally Unique Identifier), which is a 128-bit number that is unique across both space and time. The `crypto.subtle` API provides a set of methods for performing various cryptographic operations, such as hashing, encryption, and decryption.

* **UUID (Universally Unique Identifier):** A 128-bit number that is unique across both space and time.
* **Hashing:** A one-way function that takes input data of any size and produces a fixed-size output, known as a message digest.
* **Encryption:** The process of converting plaintext data into ciphertext data, which can only be decrypted with a secret key.

> **Tip:** Use the `crypto.randomUUID()` API to generate unique identifiers for objects in your web application.

## How It Works Internally
The `crypto.randomUUID()` API uses a pseudorandom number generator (PRNG) to generate a random UUID. The PRNG is seeded with a random value, which is generated using various sources, such as the system clock, network packets, and keyboard input.

The `crypto.subtle` API uses a combination of algorithms, such as AES (Advanced Encryption Standard) and RSA (Rivest-Shamir-Adleman), to perform cryptographic operations. The choice of algorithm depends on the specific method being used, such as `encrypt()` or `decrypt()`.

Here is a high-level overview of the steps involved in generating a random UUID using the `crypto.randomUUID()` API:

1. Seed the PRNG with a random value.
2. Generate a random 128-bit number using the PRNG.
3. Format the random number as a UUID string.

> **Warning:** Do not use the `crypto.randomUUID()` API to generate cryptographically secure random numbers, as it is not designed for this purpose. Instead, use the `crypto.getRandomValues()` API.

## Code Examples
### Example 1: Basic usage of `crypto.randomUUID()`
```javascript
// Generate a random UUID
const uuid = crypto.randomUUID();
console.log(uuid); // Output: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```
### Example 2: Using `crypto.subtle` to encrypt data
```javascript
// Generate a random key
const key = await crypto.subtle.generateKey(
  {
    name: "AES-GCM",
    length: 256,
  },
  true,
  ["encrypt", "decrypt"]
);

// Encrypt data
const data = new TextEncoder("utf-8").encode("Hello, World!");
const encryptedData = await crypto.subtle.encrypt(
  {
    name: "AES-GCM",
    iv: new Uint8Array(12), // initialization vector
  },
  key,
  data
);
console.log(encryptedData); // Output: Uint8Array
```
### Example 3: Using `crypto.subtle` to decrypt data
```javascript
// Decrypt data
const decryptedData = await crypto.subtle.decrypt(
  {
    name: "AES-GCM",
    iv: new Uint8Array(12), // initialization vector
  },
  key,
  encryptedData
);
const originalData = new TextDecoder("utf-8").decode(decryptedData);
console.log(originalData); // Output: "Hello, World!"
```
## Visual Diagram
```mermaid
graph TD
    A[Generate Random UUID] -->|crypto.randomUUID()| B[Format UUID String]
    B -->|return| C[Web Application]
    C -->|use UUID| D[Store Data]
    D -->|retrieve data| E[Web Application]
    E -->|use crypto.subtle| F[Encrypt Data]
    F -->|return encrypted data| G[Store Encrypted Data]
    G -->|retrieve encrypted data| H[Web Application]
    H -->|use crypto.subtle| I[Decrypt Data]
    I -->|return decrypted data| J[Web Application]
```
This diagram illustrates the flow of data through the `crypto` API, from generating a random UUID to encrypting and decrypting data using the `crypto.subtle` API.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| `crypto.randomUUID()` | O(1) | O(1) | Fast and secure | Not suitable for cryptographic purposes | Generating unique identifiers |
| `crypto.subtle` | O(n) | O(n) | Secure and flexible | Complex API | Cryptographic operations, such as encryption and decryption |
| `Math.random()` | O(1) | O(1) | Fast and simple | Not secure | Non-cryptographic purposes, such as games or simulations |
| `window.crypto.getRandomValues()` | O(1) | O(1) | Secure and fast | Limited availability | Cryptographic purposes, such as generating random numbers |

> **Interview:** Can you explain the difference between `crypto.randomUUID()` and `crypto.subtle`? How would you use each API in a web application?

## Real-world Use Cases
1. **Google Drive:** Uses the `crypto` API to generate unique identifiers for files and folders.
2. **Dropbox:** Uses the `crypto.subtle` API to encrypt and decrypt file data.
3. **Facebook:** Uses the `crypto` API to generate random numbers for cryptographic purposes.

## Common Pitfalls
1. **Using `crypto.randomUUID()` for cryptographic purposes:** This API is not designed for generating cryptographically secure random numbers.
```javascript
// Wrong
const randomBytes = crypto.randomUUID();
const key = await crypto.subtle.importKey(
  "raw",
  new Uint8Array(randomBytes),
  { name: "AES-GCM" },
  false,
  ["encrypt", "decrypt"]
);
```
```javascript
// Right
const randomBytes = new Uint8Array(32);
crypto.getRandomValues(randomBytes);
const key = await crypto.subtle.importKey(
  "raw",
  randomBytes,
  { name: "AES-GCM" },
  false,
  ["encrypt", "decrypt"]
);
```
2. **Using `crypto.subtle` without proper error handling:** This API can throw errors if the input data is invalid or if the operation fails.
```javascript
// Wrong
try {
  const encryptedData = await crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: new Uint8Array(12), // initialization vector
    },
    key,
    data
  );
} catch (error) {
  console.error(error);
}
```
```javascript
// Right
try {
  const encryptedData = await crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: new Uint8Array(12), // initialization vector
    },
    key,
    data
  );
} catch (error) {
  if (error instanceof TypeError) {
    console.error("Invalid input data");
  } else if (error instanceof Error) {
    console.error("Operation failed");
  } else {
    console.error(error);
  }
}
```
## Interview Tips
1. **What is the difference between `crypto.randomUUID()` and `crypto.subtle`?**
	* Weak answer: "I think `crypto.randomUUID()` generates a random UUID, while `crypto.subtle` is used for encryption and decryption."
	* Strong answer: "The `crypto.randomUUID()` API generates a random UUID, which is a 128-bit number that is unique across both space and time. The `crypto.subtle` API provides a set of methods for performing various cryptographic operations, such as hashing, encryption, and decryption."
2. **How would you use the `crypto` API to generate a random key for encryption?**
	* Weak answer: "I would use the `crypto.randomUUID()` API to generate a random UUID, and then use that as the key."
	* Strong answer: "I would use the `crypto.subtle.generateKey()` method to generate a random key, specifying the algorithm and key length. For example, `const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);`"
3. **What are some common pitfalls when using the `crypto` API?**
	* Weak answer: "I'm not sure, but I think you have to be careful when using the API."
	* Strong answer: "Some common pitfalls include using `crypto.randomUUID()` for cryptographic purposes, not handling errors properly, and not using the correct algorithms and key lengths for the specific use case."

## Key Takeaways
* The `crypto` API provides a set of methods for performing various cryptographic operations, such as generating random numbers, hashing, encryption, and decryption.
* The `crypto.randomUUID()` API generates a random UUID, which is a 128-bit number that is unique across both space and time.
* The `crypto.subtle` API provides a set of methods for performing various cryptographic operations, such as hashing, encryption, and decryption.
* Always use the correct algorithms and key lengths for the specific use case.
* Handle errors properly when using the `crypto` API.
* Use the `crypto.getRandomValues()` API to generate cryptographically secure random numbers.
* Use the `crypto.subtle.generateKey()` method to generate a random key for encryption.
* Be aware of the common pitfalls when using the `crypto` API, such as using `crypto.randomUUID()` for cryptographic purposes and not handling errors properly.