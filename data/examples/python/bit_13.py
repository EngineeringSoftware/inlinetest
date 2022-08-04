from inline import Here

def final_hash(self):
    """
    Calls all the other methods to process the input. Pads the data, then splits into
    blocks and then does a series of operations for each block (including expansion).
    For each block, the variable h that was initialized is copied to a,b,c,d,e
    and these 5 variables a,b,c,d,e undergo several changes. After all the blocks are
    processed, these 5 variables are pairwise added to h ie a to h[0], b to h[1] and so on.
    This h becomes our final hash which is returned.
    """
    self.padded_data = self.padding()
    self.blocks = self.split_blocks()
    for block in self.blocks:
        expanded_block = self.expand_block(block)
        a, b, c, d, e = self.h
        for i in range(0, 80):
            if 0 <= i < 20:
                f = (b & c) | ((~b) & d)
                Here().given(b, 1).given(c, -1).given(d, 1).check_eq(f, 1)
                k = 0x5A827999
            elif 20 <= i < 40:
                f = b ^ c ^ d
                Here().given(b, 1).given(c, -1).given(d, 1).check_eq(f, -1)
                k = 0x6ED9EBA1
            elif 40 <= i < 60:
                f = (b & c) | (b & d) | (c & d)
                Here().given(b, 1).given(c, -1).given(d, 1).check_eq(f, 1)
                k = 0x8F1BBCDC
            elif 60 <= i < 80:
                f = b ^ c ^ d
                Here().given(b, 1).given(c, -1).given(d, 1).check_eq(f, -1)
                k = 0xCA62C1D6
            a, b, c, d, e = (
                self.rotate(a, 5) + f + e + k + expanded_block[i] & 0xFFFFFFFF,
                a,
                self.rotate(b, 30),
                c,
                d,
            )
    self.h = (
        self.h[0] + a & 0xFFFFFFFF,
        self.h[1] + b & 0xFFFFFFFF,
        self.h[2] + c & 0xFFFFFFFF,
        self.h[3] + d & 0xFFFFFFFF,
        self.h[4] + e & 0xFFFFFFFF,
    )
    return "%08x%08x%08x%08x%08x" % tuple(self.h)
