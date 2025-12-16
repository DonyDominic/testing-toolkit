@test
def test_addition():
    assert 1 + 1 == 2

@test
def test_subtraction():
    assert 5 - 3 == 2

@test
def test_fail():
    assert 10 == 5    # will fail
