# -*- coding: utf-8 -*-
import random
import time


def test_multiple_of_2():
    print("Test multiple of 2")
    if random.randint(1,5) % 2 == 0:
        assert True
    else:
        assert False