import pytest

from lib.solutions.CHK.checkout_solution import (
    _counter,
    checkout,
    get_items_price,
    remove_free_items,
)


def test_empty():
    assert checkout("") == 0


def test_badtype_input():
    assert checkout(1) == -1


# TODO Ideally these functions would follow a functional approach and not depend on hardcoded price and discount info, receiving them as args instead.


@pytest.mark.parametrize(
    "skus",
    [
        "Ñ",
        "A Ñ",
    ],
)
def test_non_existing_sku(skus):
    assert checkout(skus) == -1


@pytest.mark.parametrize(
    "skus, price",
    [
        ("A", 50),
        ("B", 30),
        ("C", 20),
    ],
)
def test_single_items(skus, price):
    assert checkout(skus) == price


@pytest.mark.parametrize(
    "skus, price",
    [
        ("A A", 100),
        ("A C A", 120),
    ],
)
def test_multiple_items(skus, price):
    assert checkout(skus) == price


@pytest.mark.parametrize(
    "skus, price",
    [
        ("A A A", 130),
        # Having sums rather than results on the right side facilitates
        # understanding where the numbers come from
        ("A A A A", 130 + 50),
        ("A A A A B B", 130 + 50 + 45),
        ("A A A B B B", 130 + 45 + 30),
        ("A A A C", 130 + 20),
    ],
)
def test_discounted_items(skus, price):
    assert checkout(skus) == price


@pytest.mark.parametrize(
    "skus",
    [
        "AA",
        " AA ",
        "A A",
        " A A ",
    ],
)
def test_spacing(skus):
    # It is not specified how the items are separated in the input,
    # or even if they are
    assert checkout(skus) == 100


@pytest.mark.parametrize(
    "skus, price",
    [
        (("AAAAA AAA A"), 200 + 130 + 50),
        (("AAAAA AAA A BB"), 200 + 130 + 50 + 45),
    ],
)
def test_multiple_discounted_items(skus, price):
    assert checkout(skus) == price


@pytest.mark.parametrize(
    "skus, price",
    [
        ("E B", 40 + 30),
        ("EE B", 40 * 2),
        ("EE BB", 40 * 2 + 30),
        ("EEE BB", 40 * 3 + 30),
        ("EEEE BB", 40 * 4),
    ],
)
def test_free_items_discounts(skus, price):
    assert checkout(skus) == price


def test_free_item_discount_not_applied_when_free_items_not_in_cart():
    assert checkout("EE") == 40 * 2


@pytest.mark.parametrize(
    "skus, price",
    [
        ("FF", 10 * 2),
        ("FFF", 10 * 2),
        ("FFFF", 10 * 2 + 10),
        ("FFF FFF", 10 * 2 * 2),
    ],
)
def test_free_discount_for_the_same_sku(skus, price):
    assert checkout(skus) == price


@pytest.mark.parametrize(
    "skus, price",
    [
        ("STX", 45),
        ("ZXS", 45),
        ("STX XYZ", 45 * 2),
        ("SSS", 45),
        # # When not all items can be added to a group offer, the cheapest ones are charged
        ("SST X", 45 + 17),
        ("SST XY", 45 + 17 + 20),
        # # We can mix group and bulk offers
        ("SST X AAA", 45 + 17 + 130),
        # # We can mix group and free item offers
        ("STX NNN M", 45 + 40 * 3),
    ],
)
def test_group_discount(skus, price):
    assert checkout(skus) == price


####################################
# Internals tests


def test_counter():
    assert _counter("A B A") == {"A": 2, "B": 1}


@pytest.mark.parametrize(
    "sku, count, price",
    [
        ("A", 2, 50 * 2),
        ("A", 3, 130),
        ("A", 4, 130 + 50),
        ("A", 5, 200),
        ("A", 6, 200 + 50),
        ("A", 8, 200 + 130),
        ("A", 9, 200 + 130 + 50),
    ],
)
def test_get_items_price(sku, count, price):
    assert get_items_price(sku, count) == price


@pytest.mark.parametrize(
    "before, after",
    [
        ({"E": 2}, {"E": 2}),
        ({"E": 2, "B": 1}, {"E": 2}),
        ({"E": 2, "B": 2}, {"E": 2, "B": 1}),
        ({"E": 5, "B": 3, "A": 1}, {"E": 5, "B": 1, "A": 1}),
    ],
)
def test_remove_free_items(before, after):
    assert remove_free_items(before) == after


