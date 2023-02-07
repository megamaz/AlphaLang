import sys

alphabet = [x for x in "abcdefghijklmnopqrstuvwxyz"]
offset = 0
queue = []

def base26_to_base10(value: str) -> int:
    """Converts a base26 AlphaLang integer to base10"""
    number = ""
    b26alph = [x for x in "0123456789abcdefghijklmnop"]
    for v in value:
        number += b26alph[alphabet.index(v.lower())]
    return int(number, 26)

def interpret(code: str):
    # we'll first split the code between instruction and values
    split_code = []
    value = ""
    for i in code:
        if i.upper() == i: # if i is uppercase
            value += i
        elif value != "": # this means we're no longer reading a value
            split_code.append(value)
            split_code.append(i)
            value = ""
        else: # this means we were never reading a value in the first place
            split_code.append(i)
    
    print(split_code)

if __name__ == "__main__":
    code = open("../codes/helloworld.al")
    interpret(code)
    