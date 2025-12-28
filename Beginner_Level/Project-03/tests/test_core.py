from random import Random

def choose_secret(rng, lo, hi):
    return rng.randint(lo, hi)

def test_secret_in_range():
    rng = Random(123)
    lo, hi = 1, 100
    s = choose_secret(rng, lo, hi)
    assert lo <= s <= hi