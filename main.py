from solver import Solver
import random


class RNGCracker:
    def __init__(self):
        self.solver = Solver()

    def crack(self, numbers):
        bit_length = 32

        for num in numbers:
            binary_equation = [None] * bit_length
            known_bits = 0

            # Parse the number with 'x' representing unknown digits
            for i, char in enumerate(reversed(num)):
                if char != "x":
                    binary_equation[i] = int(char)
                    known_bits += 1

            # If we have enough information, add to solver
            if known_bits > 0:
                equation_value = 0
                equation_bits = 0

                for i, bit in enumerate(binary_equation):
                    if bit is not None:
                        equation_value |= bit << (bit_length - 1 - i)
                        equation_bits |= 1 << (bit_length - 1 - i)

                self.solver.insert(equation_bits, equation_value)

        # Try to solve and find the state
        try:
            state = self.solver.solve()
            return state
        except Exception as e:
            raise ValueError(
                f"{624*32 - len(self.solver.equations)} bits of more information are required"
            ) from e


test_numbers = [bin(random.getrandbits(32))[2:] for _ in range(624)]
rng_cracker = RNGCracker()
try:
    recovered_state = rng_cracker.crack(test_numbers)
    print("Recovered RNG state:", recovered_state)
    random.setstate((3, tuple(recovered_state + [0]), None))
    for i in range(624):
        assert int(test_numbers[i], 2) == random.getrandbits(32)
except ValueError as e:
    print(e)
