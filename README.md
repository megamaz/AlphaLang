# AlphaLang
An esoteric programming language I designed that uses all letters of the alphabet, both uppercase and lowercase, for a total of 52 letters 

# Syntax
Lowercase letters map to different instructions, and uppercase letters are used for a base26 number system (where `A` is 0, and `BA` is 26.)

Instructions are indexed based on where the letter is in the alphabet. By example, letter `c` is the third letter, so its index is `02` (start-from-zero indexing)

When an instruction is used, the used letter becomes the first letter of the alphabet. This means that using instruction `d`, would make the alphabet shift to being `defghijklmnopqrstuvwxyzabc`, meaning that `g` is now index `03`.

Storage is a queue. You can push to the bottom, and pop from the top. 

There are a total of 13 instructions;
```
[value] refers to a numerical value (uppercase letters), or a reference to 01 / 02.

00 - Do nothing.
01 - Contains the last popped value
02 - Queue's bottom value
03 - Push [value]
04 - Pop
05 - Input -> Takes one character and pushes its UTF-8 value
06 - Output -> Outputs the current top's UTF-8 value
07 - Add -> Pops two values and pushes their sum
08 - Substract -> Pops two values and pushes their difference (if A is popped first and B is popped second, then push A - B)
09 - Multiply -> Pops two values and pushes their product
10 - NOT -> Pops one value. If it's 0, push 1. If it's non-zero, push 0. in technical terms, queue.push(queue.pop() == 0)
11 - Skip [value] -> Skips that amount of instructions. Numerical values count as one grouped instruction (this means that "CEF" and "A" are both one instruction)
12 - -1 -> Marks the numerical value as negative, separate from the actual value itself. This means that "mAB" will count as two instructions.
```
Any letters whos ID is >= 13 will be considered "out of bounds", and instead of throwing an error will instead do nothing. The alphabet will still be shifted accordingly, even if the instruction itself did not do anything.

# Samples
### Hello World
Here's a simple, unoptimized, "Hello World" program. (It's unoptimized since it does not make use of the queue system and pops / repushes repeated letters.)
```
dCUjnqDXwadEEjptwEHcgjBGptwDJcgjEHptwEKcgjEEptwDWc
```
### While Loop
Here's an infinite while loop
```
adHIhseF
```
the `a` instruction resets the alphabet, and the `seF` skips -5 back to the `a`. the `dHIh` is a useless command that pushes then pops.
