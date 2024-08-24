from z3 import *


class PRNGCracker:
    w = 32  # word size
    n = 624  # degree of recursion
    m = 397  # middle term
    r = 31  # separation point of one word
    a = 0x9908B0DF  # bottom row of matrix A
    u = 11  # tempering shift
    s = 7  # tempering shift
    t = 15  # tempering shift
    l = 18  # tempering shift
    b = 0x9D2C5680  # tempering mask
    c = 0xEFC60000  # tempering mask

    def temper(self, state):
        y = state
        y = y ^ (y >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return y

    def untemper(self, out):
        y1 = BitVec("y1", self.w)
        y2 = BitVec("y2", self.w)
        y3 = BitVec("y3", self.w)
        y4 = BitVec("y4", self.w)
        y = BitVecVal(out, self.w)
        s = Solver()
        s.add(y2 == y1 ^ LShR(y1, self.u))
        s.add(y3 == y2 ^ ((y2 << self.s) & self.b))
        s.add(y4 == y4 ^ ((y3 << self.t) & self.c))
        s.add(y == y4 ^ LShR(y4, self.l))
        s.check()

        return s.model()[y1].as_long()
