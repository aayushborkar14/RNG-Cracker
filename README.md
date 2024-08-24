# PRNG Cracker

This is a tool to crack Merseene Twister PRNG. Sequence of `getrandbits(n)` for any n can be fed into the cracker, as a binary string, where it must have leading 0's to make it's length `n` bits.
The numbers can have missing bits at the `LSB` side, these can be represented by `x` (as `str` datatype).
The cracker will output the `state` which can be loaded with `random.setstate(state)` to reproduce the sequence.

## Example Usage

```python
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
```
