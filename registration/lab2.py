equivalent = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
    'A': 27,
    'B': 28,
    'C': 29,
    'D': 30,
    'E': 31,
    'F': 32,
    'G': 33,
    'H': 34,
    'I': 35,
    'J': 36,
    'K': 37,
    'L': 38,
    'M': 39,
    'N': 40,
    'O': 41,
    'P': 42,
    'Q': 43,
    'R': 44,
    'S': 45,
    'T': 46,
    'U': 47,
    'V': 48,
    'W': 49,
    'X': 50,
    'Y': 51,
    'Z': 52,
    ' ': 53,
    '1': 54,
    '2': 55,
    '3': 56,
    '4': 57,
    '5': 58,
    '6': 59,
    '7': 60,
    '8': 61,
    '9': 62,
    '_': 63,
    ',': 64,
    '-': 65,
}

p = 7
q = 13
euler = (p - 1) * (q - 1)
n = p * q
e = 31
open_key = (e, n)
d = 0.1
k = 1
while d != int(d):
    d = (k * euler + 1) / e
    k += 1

closed_key = (d, n)


def cipher(string, equivalent=equivalent, open_key=open_key):
    symbols_codes = []
    str_symbols = ''
    cipher_symbols_codes = []
    for letter in string:
        symbols_codes.append(equivalent[letter])

    for number in symbols_codes:
        cypher = (number ** open_key[0]) % open_key[1]
        cipher_symbols_codes.append(cypher)

    for symbol in cipher_symbols_codes:
        if symbol < 10:
            str_symbols += '0' + str(symbol)
        else:
            str_symbols += str(symbol)

    # print(cipher_symbols_codes)
    return str_symbols


def uncipher(cipher_symbols_codes, closed_key, equivalent):
    new_symbols_codes = []
    new_string = ''
    for number in cipher_symbols_codes:
        cypher = (number ** closed_key[0]) % closed_key[1]
        new_symbols_codes.append(cypher)

    for code in new_symbols_codes:
        for key, value in equivalent.items():
            if code == value:
                new_string += key

    return new_string


def uncipher_str(str_symbols, closed_key=closed_key, equivalent=equivalent):
    cnt = 0
    s = ''
    cipher_symbols_codes = []
    for symbol in str_symbols:
        s += symbol
        cnt += 1
        if cnt == 2:
            cipher_symbols_codes.append(int(s))
            s = ''
            cnt = 0
    # print(cipher_symbols_codes, 'aaa')
    new_symbols_codes = []
    new_string = ''
    for number in cipher_symbols_codes:
        cypher = (number ** closed_key[0]) % closed_key[1]
        new_symbols_codes.append(cypher)

    for code in new_symbols_codes:
        for key, value in equivalent.items():
            if code == value:
                new_string += key

    return new_string
