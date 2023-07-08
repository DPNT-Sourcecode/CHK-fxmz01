from lib.solutions.CHK.checkout_solution import _counter, _discountpack_counts, checkout


def test_empty():
    assert checkout("") == 0


def test_badtype_input():
    assert checkout(1) == -1


def test_non_existing_sku():
    assert checkout("X") == -1
    assert checkout("A X") == -1


def test_single_items():
    assert checkout("A") == 50
    assert checkout("B") == 30
    assert checkout("C") == 20


def test_multiple_items():
    assert checkout("A A") == 100
    assert checkout("A C A") == 120


def test_discounted_items():
    assert checkout("A A A") == 130
    assert checkout("A A A A") == 130 + 50
    assert checkout("A A A A B B") == 130 + 50 + 45
    assert checkout("A A A B B B") == 130 + 45 + 30
    assert checkout("A A A C") == 130 + 20


def test_spacing():
    # It is not specified how the items are separated in the input,
    # or even if they are
    assert checkout("AA") == 100
    assert checkout(" AA ") == 100
    assert checkout("A A") == 100
    assert checkout(" A A ") == 100

def test_counter():
    assert _counter("A B A") == {"A": 2, "B": 1}


def test_discountpack_counts():
    assert _discountpack_counts(4, 2) == (2, 0)
    assert _discountpack_counts(4, 3) == (1, 1)
    assert _discountpack_counts(10, 3) == (3, 1)


# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+
