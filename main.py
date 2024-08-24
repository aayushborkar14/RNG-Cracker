import random

from tqdm import trange

from solver import Solver, Twister


class RNGCracker:
    def __init__(self):
        self.solver = Solver()
        self.twister = Twister()

    def _process_string(self, s):
        if all(char == "x" for char in s):
            return "", True
        flag = True
        for i, char in enumerate(s):
            if char == "x":
                if i != len(s) - 1 and s[i + 1] not in {"x"}:  # Intermediate 'x'
                    flag = False
                    break
                elif i == 0:
                    flag = False
                    break
        if flag:
            s = s.rstrip("x")
        return s, flag

    def bits_needed(self, n):
        return 624 * 32 - len(self.solver.equations)

    def add_numbers(self, numbers):
        outputs = []
        equations = []
        for num in numbers:
            s, flag = self._process_string(num)
            if not flag:
                raise ValueError("Non-trailing x found")
            outputs.append(int(s, 2))
            equations.append(self.twister.getrandbits(len(s)))
        for i in trange(len(numbers)):
            for j in range(len(numbers[i])):
                self.solver.insert(
                    equations[i][j], (outputs[i] >> (len(numbers[i]) - 1 - j)) & 1
                )

    def crack(self):
        return (3, tuple(self.solver.solve() + [0]), None)


test_numbers = [bin(random.getrandbits(32))[2:].rjust(32, "0") for _ in range(624)]
rng_cracker = RNGCracker()
try:
    rng_cracker.add_numbers(test_numbers)
    print(f"Additional bits needed: {rng_cracker.bits_needed(624)}")
    recovered_state = rng_cracker.crack()
    random.setstate(recovered_state)
    for i in range(624):
        assert int(test_numbers[i], 2) == random.getrandbits(32)
    print("Cracked successfully!")
except ValueError as e:
    print(e)
