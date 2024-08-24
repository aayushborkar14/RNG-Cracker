from typing import List


class Solver:
    def __init__(self):
        self.equations: List[int] = []
        self.outputs: List[int] = []

    def insert(self, equation: int, output: int) -> None:
        """
        Insert a new equation into the system if it increases the rank.
        """
        # Eliminate the new equation with existing equations
        for eq, o in zip(self.equations, self.outputs):
            lsb = eq & -eq
            if equation & lsb:
                equation ^= eq
                output ^= o

        if equation == 0:
            return

        # Update existing equations with the new equation
        lsb = equation & -equation
        for i in range(len(self.equations)):
            if self.equations[i] & lsb:
                self.equations[i] ^= equation
                self.outputs[i] ^= output

        # Add the new equation to the system
        self.equations.append(equation)
        self.outputs.append(output)

    def solve(self) -> List[int]:
        """
        Solve the system of equations and return the state.
        """
        num = 0
        for i, eq in enumerate(self.equations):
            if self.outputs[i]:
                # Assume every free variable is 0
                num |= eq & -eq

        # Convert the solution to a list of 624 32-bit integers
        state = [(num >> (32 * i)) & 0xFFFFFFFF for i in range(624)]
        return state


class Twister:
    N: int = 624
    M: int = 397
    A: int = 0x9908B0DF

    def __init__(self):
        # Initialize the state with binary representations
        self.state: List[List[int]] = [
            [(1 << (32 * i + (31 - j))) for j in range(32)] for i in range(self.N)
        ]
        self.index: int = 0

    def _xor(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise XOR operation on two lists."""
        return [x ^ y for x, y in zip(a, b)]

    def _and(self, a: List[int], x: int) -> List[int]:
        """Perform bitwise AND operation between a list and an integer."""
        return [v if (x >> (31 - i)) & 1 else 0 for i, v in enumerate(a)]

    def _rshift(self, a: List[int], x: int) -> List[int]:
        """Perform right shift operation on a list."""
        return [0] * x + a[:-x]

    def _lshift(self, a: List[int], x: int) -> List[int]:
        """Perform left shift operation on a list."""
        return a[x:] + [0] * x

    def get32bits(self) -> List[int]:
        """
        Generate and return the next 32-bit integer from the Mersenne Twister.
        """
        if self.index >= self.N:
            self._twist()

        y = self.state[self.index]
        y = self._xor(y, self._rshift(y, 11))
        y = self._xor(y, self._and(self._lshift(y, 7), 0x9D2C5680))
        y = self._xor(y, self._and(self._lshift(y, 15), 0xEFC60000))
        y = self._xor(y, self._rshift(y, 18))
        self.index += 1

        return y

    def _twist(self) -> None:
        """Perform the twisting operation to generate a new batch of numbers."""
        for kk in range(self.N):
            y = self.state[kk][:1] + self.state[(kk + 1) % self.N][1:]
            z = [y[-1] if (self.A >> (31 - i)) & 1 else 0 for i in range(32)]
            self.state[kk] = self._xor(
                self.state[(kk + self.M) % self.N], self._rshift(y, 1)
            )
            self.state[kk] = self._xor(self.state[kk], z)
        self.index = 0

    def getrandbits(self, bit: int) -> List[int]:
        """
        Get a specified number of random bits.
        """
        return self.get32bits()[:bit]
