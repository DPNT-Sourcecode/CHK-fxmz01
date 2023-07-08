from lib.solutions.CHK.checkout_solution import _counter, _discountpacks, checkout


def test_empty():
    assert checkout("") == 0


def test_badtype_input():
    assert checkout(1) == -1


def test_non_existing_sku():
    assert checkout("X") == -1
    assert checkout("A X") == -1


def test_singleitems():
    assert checkout("A") == 50
    assert checkout("B") == 30
    assert checkout("C") == 20


def test_counter():
    assert _counter("A B A") == {"A": 2, "B": 1}


def test_discountpacks():
    assert _discountpacks(4, 2) == (2, 0)
    assert _discountpacks(4, 3) == (1, 1)
    assert _discountpacks(10, 3) == (3, 1)


# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+
