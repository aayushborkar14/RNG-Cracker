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

    def crack(self, numbers) -> list[int]:
        outputs = []
        equations = []
        for num in numbers:
            if len(num) != 32:
                raise ValueError("Invalid number length")
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
        return self.solver.solve()


test_numbers = [bin(random.getrandbits(32))[2:].rjust(32, "0") for _ in range(624)]
rng_cracker = RNGCracker()
try:
    recovered_state = rng_cracker.crack(test_numbers)
    random.setstate((3, tuple(recovered_state + [0]), None))
    for i in range(624):
        assert int(test_numbers[i], 2) == random.getrandbits(32)
    print("Cracked successfully!")
except ValueError as e:
    print(e)
