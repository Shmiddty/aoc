import sys

def score(st):
    d = i = n = N = g = 0
    L = len(st)
    while i < L:
        ch = st[i]
        i += 1
        if g:
            if ch == '!':
                i += 1      # skip next
            elif ch == '>':
                g = 0       # end garbage
            else:
                N += 1      # score the garbage
        else:
            if ch == '{':
                d += 1      # begin group
            
            if ch == '}':
                n += d      # score the group
                d -= 1      # end group
            
            if ch == '<':
                g = 1       # begin garbage

    return n, N

inp = sys.stdin.read().strip()
print(score(inp))
