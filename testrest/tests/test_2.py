import random


def test_odd_even():
    print("This test will only pass if the generated random number is odd")
    if random.randint(2, 6) % 2 == 0:
        assert False
    else:
        assert True