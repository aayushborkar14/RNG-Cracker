from z3 import *


class MT19937(object):
    def __init__(self, seed=5489):
        self.state = [0] * 624
        self.f = 1812433253
        self.m = 397
        self.u = 11
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.index = 624
        self.lower_mask = (1 << 31) - 1
        self.upper_mask = 1 << 31

        # update state
        self.state[0] = seed
        for i in range(1, 624):
            self.state[i] = self.int32(
                self.f * (self.state[i - 1] ^ (self.state[i - 1] >> 30)) + i
            )

    def twist(self):
        for i in range(624):
            temp = self.int32(
                (self.state[i] & self.upper_mask)
                + (self.state[(i + 1) % 624] & self.lower_mask)
            )
            temp_shift = temp >> 1
            if temp % 2 != 0:
                temp_shift = temp_shift ^ 0x9908B0DF
            self.state[i] = self.state[(i + self.m) % 624] ^ temp_shift
        self.index = 0

    def temper(self, in_value):
        y = in_value
        y = y ^ (y >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return y

    def get_random_number(self):
        if self.index >= 624:
            self.twist()
        out = self.temper(self.state[self.index])
        self.index += 1
        return self.int32(out)

    def int32(self, number):
        return int(0xFFFFFFFF & number)


class PRNGCracker:
    def __init__(self, state):
        self.state = state
        self.w = 32  # word size
        self.n = 624  # degree of recursion
        self.m = 397  # middle term
        self.r = 31  # separation point of one word
        self.a = 0x9908B0DF  # bottom row of matrix A
        self.u = 11  # tempering shift
        self.s = 7  # tempering shift
        self.t = 15  # tempering shift
        self.l = 18  # tempering shift
        self.b = 0x9D2C5680  # tempering mask
        self.c = 0xEFC60000  # tempering mask

    def temper(self, state):
        y = state
        y = y ^ (y >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return y

    def untemper(self, y):
        y = self.undoTemperShiftL(y)
        y = self.undoTemperShiftT(y)
        y = self.undoTemperShiftS(y)
        y = self.undoTemperShiftU(y)
        return y

    def undoTemperShiftL(self, y):
        last14 = y >> 18
        final = y ^ last14
        return final

    def undoTemperShiftT(self, y):
        first17 = y << 15
        final = y ^ (first17 & self.c)
        return final

    def undoTemperShiftS(self, y):
        a = y << 7
        b = y ^ (a & self.b)
        c = b << 7
        d = y ^ (c & self.b)
        e = d << 7
        f = y ^ (e & self.b)
        g = f << 7
        h = y ^ (g & self.b)
        i = h << 7
        final = y ^ (i & self.b)
        return final

    def undoTemperShiftU(self, y):
        a = y >> 11
        b = y ^ a
        c = b >> 11
        final = y ^ c
        return final

    def crack(self, numbers):
        bitvecs = []
        for i, num in enumerate(numbers):
            if len(num) > self.w:
                raise Exception(f"Number {num} is too big for the word size")
            num = num.rjust(self.w, "0")
            bitvecs.append(BitVec(f"num{i}", self.w))

    def crack_file(self, filename):
        f = open(filename, "r")
        numbers = []
        for line in f:
            if line.strip():
                numbers.append(line.strip())
        self.crack(numbers)
