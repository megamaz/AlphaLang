This code is filtered to only include letters.

Lowercase letters map to different instructions, and uppercase letters are used for a base26 number system (where A is 0, and BA is 26.)

Instructions are indexed based on where the letter is in the alphabet. By example, letter c is the third letter, so its index is 02 (start-from-zero indexing)

When an instruction is used, the used letter becomes the first letter of the alphabet. This means that using instruction d, would make the alphabet shift to being defghijklmnopqrstuvwxyzabc, meaning that g is now index 03.

Storage is a queue. You can push to the bottom, and pop from the top.

There are a total of 13 instructions;