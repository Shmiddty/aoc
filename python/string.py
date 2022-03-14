def lower(string): return string.lower()

def tokens(string, delimeter = ' '):
    return string.split(delimeter)

def words(string):
    return tokens(string.strip())

def digits(string):
    import re
    return map(int, re.findall(r'(-?\d+)', string))

def concat(*strs):
    return ''.join(map(str, strs))
