import sys

ALPHABET = [x for x in "abcdefghijklmnopqrstuvwxyz"]
queue = []

# https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def base26_to_base10(value: str) -> int:
    """Converts a base26 AlphaLang integer to base10"""
    number = ""
    b26alph = [x for x in "0123456789abcdefghijklmnop"]
    for v in value:
        number += b26alph[ALPHABET.index(v.lower())]
    return int(number, 26)

def base10_to_base26(value: int) -> str:
    """Converts a normal base10 integer to a  base26 AlphaLang integer"""
    number = ""
    b26alph = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    return ''.join([b26alph[i] for i in numberToBase(value, 26)])

def interpret(code: str):
    # we'll first split the code between instruction and values
    split_code = []
    value = ""
    register_1 = 0
    register_2 = 0

    for i in code:
        if i.upper() == i: # if i is uppercase
            value += i
        elif value != "": # this means we're no longer reading a value
            split_code.append(value)
            split_code.append(i)
            value = ""
        else: # this means we were never reading a value in the first place
            split_code.append(i)
    # now we can interpret the code

    reader_index = 0
    offset = 0
    next_value_is_negative = False
    while reader_index < len(split_code):
        c = split_code[reader_index]
        negate = (-1 if next_value_is_negative else 1)
        if c.upper() != c and len(c) == 1: # if this is an instruction
            index = ALPHABET.index(c)
            index -= offset
            offset = ALPHABET.index(c)
            index %= 26
            # now do the instruction
            if index == 3:
                a = 1 + next_value_is_negative
                queue.append(base26_to_base10(split_code[reader_index+a]) * negate)
                next_value_is_negative = False
            elif index == 4:
                register_1 = queue.pop(0)
            elif index == 5:
                queue.append(ord(input(""))[0])
            elif index == 6:
                if next_value_is_negative:
                    raise ValueError("Attempting to print a negative UTF-8 value")
                print(chr(queue[0]), end='')
            elif index == 7:
                v1 = queue.pop(0)
                v2 = queue.pop(0)
                queue.append(v1 + v2)
                register_1 = v2 # last popped value
            elif index == 8:
                v1 = queue.pop(0)
                v2 = queue.pop(0)
                queue.append(v1 - v2)
                register_1 = v2
            elif index == 9:
                v1 = queue.pop(0)
                v2 = queue.pop(0)
                queue.append(v1 * v2)
                register_1 = v2
            elif index == 10:
                register_1 = queue.pop(0)
                queue.push(0 if register_1 != 0 else 1)
            elif index == 11:
                a = 1 + next_value_is_negative
                value = base26_to_base10(split_code[reader_index+a]) * negate
                reader_index += value
                next_value_is_negative = False
            elif index == 12:
                next_value_is_negative = True

            # update the register
            if len(queue) != 0:
                register_2 = queue[-1]
        reader_index += 1

def instructions_to_alphalang(code: list[str]) -> str:
    """Function that takes an instruction string and converts it to AlphaLang code
    Each instruction is separated by a newline, with the value being a space away.
    If the value is negative, just add a `-` sign, the code will detect it and add
    the `-1` instruction automatically.

    - `PASS` -> Do nothing
    - `LASTP` -> Reference to last popped value
    - `QUEUEB` -> Reference to queue's bottom value
    - `PUSH [value]`
    - `POP`
    - `INPUT`
    - `OUTPUT`
    - `ADD`
    - `SUB` -> Substract
    - `MUL` -> Multiply
    - `NOT`
    - `SKIP [value]`
    """
    offset = 0
    final = ""
    indexes = {
        "PASS":0,
        "LASTP":1,
        "QUEUEB":2,
        "PUSH":3,
        "POP":4,
        "INPUT":5,
        "OUTPUT":6,
        "ADD":7,
        "SUB":8,
        "MUL":9,
        "NOT":10,
        "SKIP":11,
    }
    for i in code:
        line = i.split(" ")
        final += ALPHABET[(indexes[line[0]] + offset)%26]
        offset = indexes[line[0]] + offset
        offset %= 26
        if len(line) != 1:
            if line[1][0] == "-":
                offset = (offset + 12) % 26
                final += ALPHABET[offset]
                final += base10_to_base26(int(line[1][1:]))
            else:
                final += base10_to_base26(int(line[1]))
    return final

if __name__ == "__main__":
    result = instructions_to_alphalang(open("./readable_codes/helloworld.ral").read().splitlines())
    print(result)
    code = open("./codes/helloworld.al").read()
    interpret(code)
    