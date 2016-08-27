import time


def test_sleep():
    print("This test will pass after sleep")
    time.sleep(2)
    assert True