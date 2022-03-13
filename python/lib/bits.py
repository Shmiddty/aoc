def hextobits(hxchr):
    i = int(hxchr, 16)
    return [(i>>3)&1, (i>>2)&1, (i>>1)&1, i&1]
